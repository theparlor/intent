---
title: Account-Connector Fabric Check
id: SPEC-INTENT-ACCOUNT-CONNECTOR-FABRIC-001
type: framework
maturity: final
confidentiality: internal
created: 2026-08-19
status: accepted
scope: universal
related:
  - Core/frameworks/intent/hooks/account-connector-fabric-check.sh
  - Core/frameworks/intent/hooks/tests/test_account_connector_fabric_check.py
  - Core/frameworks/intent/spec/autonomy-grant-enforcement.md
  - Core/frameworks/intent/spec/closure-discipline-enforcement.md
  - Core/frameworks/intent/spec/native-connector-precedence.md
  - "Workspaces repo: .intent/signals/SIG-DISPATCH-SESSION-NO-ACCOUNT-CONNECTORS-2026-08-19.md"
---
# Account-Connector Fabric Check

> SessionStart hook that warns, at second zero, when a session launched
> without the claude.ai account-connector fabric. Sibling of
> autonomy-grant-check.sh and closure-discipline-check.sh in architecture
> and registration.

## The failure it catches

On 2026-08-19 a dispatched worktree session launched with ZERO account
connectors: Era, Gmail, Google Drive, Google Calendar, Slack, Atlassian,
Granola, and Harvest were all absent from the tool roster. A
financial-analysis task (Era duplicate-charge enumeration) silently
blocked: the session burned effort on ToolSearch sweeps, registry probes,
and local-file fallbacks before concluding the connector layer itself was
missing. The fabric re-attached mid-session on its own. A second
dispatched session the same evening (the one that built this hook)
launched bare the same way, ten minutes after the first session observed
re-attachment.

The harm is not the absence; it is the SILENCE. Nothing in the session
said "you have no account connectors" until a task died against it.

Signal of record (Workspaces repo):
`.intent/signals/SIG-DISPATCH-SESSION-NO-ACCOUNT-CONNECTORS-2026-08-19.md`

## Empirical findings the design stands on (all verified 2026-08-19)

| # | Finding | Method | Design consequence |
|---|---------|--------|--------------------|
| 1 | SessionStart stdin carries NO MCP data: only session_id, transcript_path, cwd, hook_event_name, source | stdin-dumping probe hook on claude CLI 2.1.228 | The hook cannot sense the session roster; the model must |
| 2 | Account layer can be fully healthy while a session is bare: `claude mcp list` showed 11 of 11 claude.ai connectors Connected during a session that carried none of them | live comparison during the second bare session | Account-layer probes measure the wrong layer for this failure; do not build the detector on them |
| 3 | `claude mcp list` health-checks remote servers and costs seconds | timed invocation | Too slow for a per-start mechanical probe; excluded from the hook |
| 4 | Current builds name connector tools `mcp__claude_ai_<Name>__<verb>`; older surfaces used hex-UUID prefixes such as `mcp__2af7d4b6-...__` | headless probe session roster vs the 2026-05 precedence map and the origin signal | The directive teaches BOTH prefix schemes |
| 5 | `~/.claude.json` key `claudeAiMcpEverConnected` lists every connector name ever connected on this machine; it survived the outage window while per-connector registration entries did not exist anywhere in the file | direct reads during the bare window | Ever-connected is the expectation source: fast, local, zero network |
| 6 | `CLAUDE_CODE_CHILD_SESSION=1` appears on fabric-BEARING sessions too | probe env dump | Child/entrypoint env markers are telemetry, not gates |
| 7 | Fresh headless `claude -p` sessions attach the fabric; desktop-dispatched worktree child sessions were the bare ones in both observed incidents | probe runs plus the two incidents | Blast class is narrower than "all headless"; the hook stays global and cheap rather than class-gated |

## Architecture: sensor inversion

The hook is blind to the thing it guards (finding 1), so the design
inverts the sensor: the hook supplies expectation, contract, and telemetry;
the model, the only component that can see the session's tool roster,
performs the detection and emits the warning.

| Layer | Component | Role |
|---|---|---|
| 1. Expectation | `~/.claude.json` claudeAiMcpEverConnected | Should this machine have the fabric at all? Non-empty list = yes |
| 2. Directive | hook stdout, injected into session-start context | Orders the roster scan, prescribes the exact one-line warning, teaches both prefix schemes, cites the signal |
| 3. Sensor | the session's model, first reply | Scans active plus deferred tool names; emits the warning line when the fabric (or a task-needed class) is absent |
| 4. Telemetry | `~/.claude/audit/account-connector-fabric-checks.log` | One line per session start: session, source, entrypoint, child flag, cwd, expectation count, verdict |

## Detection contract

Task-critical classes (the 2026-08-19 blast roster) and their match
tokens inside `mcp__` tool names:

| Class | Current-scheme token | Legacy hex prefix |
|---|---|---|
| Era (personal finance) | `Era_Context` | `8f9971da` |
| Gmail | `Gmail` | `2af7d4b6` |
| Google Drive | `Google_Drive` | `af517670` |
| Google Calendar | `Google_Calendar` | `e84bacfb` |
| Slack | `Slack` | `bb5eb37b` |
| Atlassian (incl Rovo) | `Atlassian` | `4ae6210b` |
| Granola | `Granola` | `610554ec` |
| Harvest | `Harvest` | `0ab7ee41` |

The prescribed warning is ONE line, opening the model's first reply:

    ⚠ ACCOUNT-CONNECTOR FABRIC ABSENT: 0 claude.ai connectors attached;
    missing <classes>.

Loudness ladder, as ordered by the directive:

1. Fabric fully absent: warning line always; if the task needs a missing
   class, surface the block to Brien BEFORE grinding local fallbacks, and
   recheck before declaring a task blocked (the fabric can re-attach
   mid-session; observed 2026-08-19).
2. Partial absence of a class the task needs: same one-line warning
   naming just the missing classes.
3. Fabric present, or the task plainly needs none of it: silence.

## False-alarm boundary

The deliverable requires zero false alarms in sessions where connectors
are intentionally absent, or an explicit record of why that cannot be
guaranteed. Both halves, explicitly:

**Mechanically distinguished (hard silence, no judgment involved):**

1. `ACCOUNT_CONNECTOR_FABRIC_BYPASSED=1` in the launching environment.
   For cron, launchd, CI, and scripted harnesses that intentionally run
   bare. This lever is REACHABLE because the unit is a process launch,
   which carries environment; contrast the 2026-07-31 finding
   (precedence-not-prohibition) that an env bypass on MCP tool calls was
   unreachable because tool calls carry none.
2. Machines or accounts with an empty or absent claudeAiMcpEverConnected
   list never see the directive at all. A fresh install, a CI container,
   or another adopter of this hooks repo without claude.ai connectors is
   structurally silent.

**Explicitly recorded as NOT mechanically distinguishable:** a session on
THIS machine, launched without the bypass env, whose operator nonetheless
intended it to run bare. Per-session intent is not inferable from
anything the hook can read: stdin carries no roster (finding 1), env
markers do not separate the classes (finding 6), and account-layer health
says nothing about the session (finding 2). For that remainder the check
is ADVISORY BY DESIGN: the model is instructed to weigh task relevance
and stay silent when the task plainly needs no connector, so an
intentionally bare session doing local-only work gets, at worst, nothing,
and a bare session that needs the fabric gets exactly the warning the
incident lacked.

## Out of scope, deliberately

- Re-attaching or repairing the fabric. This hook detects; it does not
  heal. Root cause of the 2026-08-19 detachment remains unobserved from
  the client side.
- Mechanical account-layer probing per start (`claude mcp list`): wrong
  layer (finding 2) and too slow (finding 3). It remains the right MANUAL
  probe when the warning fires and you want to know whether the account
  layer is also down.
- Routing policy for connector-dependent dispatches (send such tasks only
  to connector-bearing surfaces). That is the residual upstream need named
  in the origin signal; this hook is the detection control that makes the
  gap loud enough to route around by hand until routing exists.
- Local stdio MCP servers (library-index, filesystem, elgato): different
  attachment path, not part of the claude.ai fabric, not covered.

## Deployment

```bash
# From the intent repo root
bash hooks/install.sh   # symlinks account-connector-fabric-check.sh into ~/.claude/hooks/
```

Then add to `~/.claude/settings.json` under `hooks.SessionStart`, in the
existing matcher-`*` entry alongside autonomy-grant-check.sh and
closure-discipline-check.sh:

```json
{
  "type": "command",
  "command": "~/.claude/hooks/account-connector-fabric-check.sh",
  "timeout": 10,
  "statusMessage": "Connector fabric: checking claude.ai account-connector expectation"
}
```

### Verification

1. `python3 hooks/tests/test_account_connector_fabric_check.py` prints
   ALL TESTS PASSED.
2. Start a real session; the 🔌 block appears in session-start context.
3. `~/.claude/audit/account-connector-fabric-checks.log` gains one line
   per session start with a verdict field.
4. In a fabric-bare session, the model's first reply opens with the
   ⚠ ACCOUNT-CONNECTOR FABRIC ABSENT line naming the missing classes.

## Observability and drag posture

One local JSON read plus one audit append per session start, no network,
no subprocess; measured well under 100ms. The audit log is the feedback
loop: entrypoint and child-flag telemetry accumulate the correlation data
(which session classes launch bare, how often) that was missing when the
incident hit. If the warning proves noisy in practice, the audit log is
the evidence base for tuning, per the lexical-layer-freeze doctrine of
measuring before accreting.

## Closure DoD mapping for the origin signal

- upstream_control_path: this hook, registered in
  `~/.claude/settings.json` hooks.SessionStart, symlinked from
  `~/.claude/hooks/account-connector-fabric-check.sh` to the repo file.
- catch_mechanism: the hook fires on EVERY session start (startup,
  resume, clear, compact), so the failure class cannot recur silently;
  the test harness pins the contract; the audit log evidences firing.
- pipeline survival: registration lives in user settings, which no
  render pipeline touches; the symlink survives repo pulls; install.sh
  re-creates it idempotently.

## Maintenance

- Prefix-scheme drift: the claude_ai_* naming was observed 2026-08-19 on
  CLI 2.1.228; the hex-UUID scheme appears in the 2026-05 precedence map
  and CLAUDE.md native-connector table, which are now stale on that
  point (tracked as its own signal in the Workspaces repo). If Anthropic
  renames again, update WARN_CLASSES tokens in the hook and the table
  above, in the same commit.
- Roster drift: adding a task-critical connector class means one new row
  in WARN_CLASSES plus this spec's table. The expectation layer needs no
  change; it reads whatever claudeAiMcpEverConnected holds.
