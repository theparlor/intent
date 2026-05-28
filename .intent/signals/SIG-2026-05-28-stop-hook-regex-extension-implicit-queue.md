---
id: SIG-2026-05-28-stop-hook-regex-extension-implicit-queue
created: 2026-05-28
type: control-upgrade
status: resolved
severity: high
upstream_control_path: Core/frameworks/intent/hooks/autonomy-grant-stop-check.sh (CHECK 5 added, v4 2026-05-28)
catch_mechanism: CHECK 5 regex now intercepts implicit-queue/standby phrases at Stop-hook layer before response is delivered; prior catch-net was memory-level only (feedback_pause_drift_meta_signal_on_nudge)
pipeline_survival: yes — upstream control is now deployed; catch-net (meta-signal-on-nudge memory rule) remains as belt-and-suspenders; telemetry in ~/.claude/logs/autonomy-stop-check.jsonl accumulates frequency data
related:
  - SIG-2026-05-27-pause-drift-items-3-6-7-8-after-coverage-push
  - SIG-2026-05-27-pause-drift-cross-reference-sweep-after-prompt-rework
  - SIG-2026-05-27-pause-at-scheduled-task-boundary
  - SIG-2026-05-27-pause-recurrence-immediately-after-meta-signal
  - feedback_pause_drift_meta_signal_on_nudge
  - feedback_autonomy_grant_drift_pattern
  - Core/frameworks/intent/spec/autonomy-grant-enforcement.md
---

# Control upgrade: CHECK 5 implicit-queue / standby framing added to stop hook

## Context

Four pause-drift incidents on 2026-05-27 (catalogued in sibling SIG-2026-05-27-pause-drift-* files)
revealed a class of L4 queuing that slipped past CHECKs 1-4 in `autonomy-grant-stop-check.sh`.
The existing checks detect:
- CHECK 1: bare-choice questions ending the response
- CHECK 2: soft-queue with recommendation marker glove ("Say go and I X")
- CHECK 3: L0-on-push handoff on theparlor/* repos
- CHECK 4: conditional-queue veto offers ("unless you redirect")

What they missed: **implicit standby framing** — phrases that position the model as waiting
for Brien's word before acting, without using an explicit question mark or "want me to" verb.
These are structurally equivalent to bare-choice but lexically different.

## Patterns now caught (CHECK 5)

All patterns from `feedback_pause_drift_meta_signal_on_nudge §Forbidden phrasings`:

| Pattern | Example | Status |
|---------|---------|--------|
| ready to execute when you say go | "Ready to execute when you say go." | BLOCKED |
| let me know when | "Let me know when you're ready to proceed." | BLOCKED |
| ready when you are / ready when you're ready | "Ready when you are." | BLOCKED |
| say the word | "Just say the word." | BLOCKED |
| standing by | "Standing by for your direction." | BLOCKED |
| I'll wait for your call | "I'll wait for your call." | BLOCKED |
| let me know if you want me to [verb] | "Let me know if you want me to run the next pass." | BLOCKED |
| when you're ready + action verb | "When you're ready, I'll push." | BLOCKED |
| next steps depend on | "Next steps depend on your preferred approach." | BLOCKED |

## False-positive gate

The following conversational close forms are **not** blocked (they are acceptable at L2+ surfaces
where a real information gap exists and the question is appropriate):

| Acceptable form | Why not blocked |
|-----------------|----------------|
| "Let me know if you have any questions." | FP gate strips "let me know if you have..." before re-checking |
| "If there's anything else I can help with..." | FP gate strips "anything else i can..." |
| "Let me know if you'd like me to elaborate." | FP gate strips "let me know if you'd like..." |

The gate works by stripping benign close phrases from the paragraph, then re-running the
implicit-queue regex. If the queue pattern disappears after stripping, it was a false positive.

## Test results

```
BLOCK  [ready-to-execute-when-you-say-go]
BLOCK  [let-me-know-when]
BLOCK  [ready-when-you-are]
BLOCK  [say-the-word]
BLOCK  [standing-by]
BLOCK  [ill-wait-for-your-call]
BLOCK  [let-me-know-if-you-want-me-to]
BLOCK  [when-youre-ready]
BLOCK  [next-steps-depend-on]
PASS   [let-me-know-if-questions]      ← false positive correctly suppressed
PASS   [if-anything-else]              ← false positive correctly suppressed
PASS   [proper-rec-closure]            ← legitimate recommendation+closure passes
BLOCK  [bare-choice]                   ← CHECK 1 still works
BLOCK  [check4-cond-queue]             ← CHECK 4 still works
```

## Dispatch gate

CHECK 5 inherits the dispatch gate from CHECKs 2/4: if `HAS_DISPATCH=1` (the response
already dispatched a concrete action via Agent/Bash), standby phrasing is contextual
narrative, not queuing. The trigger requires `HAS_DISPATCH=0`.

## Cross-references to 2026-05-27 pause-drift incidents

Four incidents that would have been caught by CHECK 5 (all filed 2026-05-27):

1. `SIG-2026-05-27-pause-at-scheduled-task-boundary` — silent-stop after scheduled task;
   no forbidden phrase present (structural gap, not lexical; partially addressed by
   CHECK 5's "next steps depend on" pattern, though the exact mechanism was trail-off,
   not a keyword)

2. `SIG-2026-05-27-pause-drift-items-3-6-7-8-after-coverage-push` — ended with
   "ready to execute when you say go" → **CHECK 5 would have blocked this**

3. `SIG-2026-05-27-pause-drift-cross-reference-sweep-after-prompt-rework` — trailing
   observation after proposal (structural drift; not caught by CHECK 5's lexical patterns;
   remains a gap — see upstream_control_path note in that signal)

4. `SIG-2026-05-27-pause-recurrence-immediately-after-meta-signal` — recurrence within
   same session; specific phrasing not recovered in this signal but pattern class is
   covered by CHECK 5

## Residual gap

Incident #3 (trailing-observation-after-proposal, "deliver reworked prompt then trail off")
is NOT caught by CHECK 5. That drift class has no forbidden keyword — it ends with a clean
factual sentence. Catching it requires detecting: (a) response contains a "proposal /
recommendation / reworked prompt" artifact, (b) no dispatch in the same turn, (c) last
sentence is a comment on structure/scope/quality rather than an action. This is a harder
heuristic and deferred to a future CHECK 6 when more instances accumulate.

## Three-assertion closure

- **upstream_control_path:** `Core/frameworks/intent/hooks/autonomy-grant-stop-check.sh` — CHECK 5
  deployed 2026-05-28; intercepts implicit-queue phrases at Stop-hook layer.
- **catch_mechanism:** CHECK 5 regex (9 standby-phrase patterns, dispatch gate, FP strip-and-recheck
  gate); backed by meta-signal-on-nudge memory rule as belt-and-suspenders.
- **pipeline_survival:** yes — hook is deployed, symlinked, tested. Telemetry at
  `~/.claude/logs/autonomy-stop-check.jsonl` tracks `implicit_queue_match` + `fp_suppressed`
  + `trigger` fields per-execution.
