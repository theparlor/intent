---
title: Autonomy-Grant Enforcement — Mechanism-Level Intervention
id: SPEC-INTENT-AUTONOMY-GRANT-ENFORCEMENT-001
updated: 2026-05-19
related:
  - Core/frameworks/methodology-library/meta/autonomous-investigation.md
  - Core/frameworks/methodology-library/meta/signal-scoring.md
  - Core/products/org-design-tooling/.intent/signals/RETRO-2026-04-21-autonomy-grant-reinforcement-SIG-1.md
  - Core/frameworks/coherence-engineering/.intent/signals/SIG-COH-DEBT-018.md
  - Core/frameworks/intent/hooks/autonomy-grant-check.sh
  - Core/products/org-design-tooling/.intent/signals/SIG-AUTONOMY-DRIFT-POST-STAGE-2026-05-13.md
depth_score: 4
depth_signals:
  file_size_kb: 12.0
  content_chars: 10973
  entity_count: 0
  slide_count: 0
  sheet_count: 0
  topic_count: 0
  has_summary: 0
vocab_density: 0.09
date: 2026-04-22
status: accepted
scope: universal
author: "intent framework (mechanism-level response to SIG-COH-DEBT-018 + RETRO-2026-04-21-autonomy-grant-reinforcement-SIG-1)"
layer_4_versions:
  - {version: v1 (2026-04-28), change: Initial Layer 4 Stop hook — bare-choice-without-recommendation pattern}
  - {version: v2 (2026-05-13), change: Layer 2 spec amendment — soft-queue framing on pre-authorized continuation (SIG-AUTONOMY-DRIFT-POST-STAGE-2026-05-13), hook_landed: 2026-05-13}
layer_5_versions:
  - {version: v1 (2026-05-19), change: Layer 5 PreToolUse dispatch-prompt check — blocks proposal-framing injected into subagent prompts before dispatch (SIG-PROCESS-DRIFT-PR-STYLE-REVIEW-2026-05-19), hook_landed: 2026-05-19}
---
# Autonomy-Grant Enforcement

## Purpose

Installs the mechanism-level intervention that closes the recurring autonomy-grant
drift pattern. Memory (`feedback_autonomy_grant_drift_pattern`) has been in place
for multiple sessions and has not prevented drift. Signal (SIG-PERSONAS-013) has
been in place and has not prevented drift. Brien-in-the-loop reinforcement IS
effective but is not scalable.

This spec defines the mechanism that reinforces the autonomy posture
pre-emptively at session boundary — a simulated in-loop reinforcement that
fires before the first response.

## Problem statement

**Observable pattern (2026-04-21):** In a single session on main thread, drift
toward proposal-framing recurred four times despite L4 autonomy grant being
explicit in memory. Brien reinforced the posture twice mid-execution with
messages like *"autonomy grant check maintains all similar signal and demand
execute as previously"*. Both reinforcements were immediately effective —
execution resumed without further asking.

**Hypothesis (from `RETRO-2026-04-21-autonomy-grant-reinforcement-SIG-1`):**
Memory-as-loaded-context is consulted when an agent decides to consult it;
drift occurs precisely at the decision points where the agent does NOT consult
it. The load-bearing question is how to make the autonomy posture
load-bearing on every decision, not just the ones the agent thinks to anchor.

**Observed closure mechanisms:**

| Mechanism | Effectiveness | Problem |
|---|---|---|
| Memory (`feedback_autonomy_grant_drift_pattern`) | Partial | Fades across session length, consulted inconsistently |
| Signal (SIG-PERSONAS-013 / SIG-COH-DEBT-018) | Logged only | Doesn't fire pre-emptively |
| Brien mid-session reinforcement | Highly effective | Not scalable; requires Brien in loop |
| **This spec (SessionStart hook)** | **Pre-emptive anchor** | Requires `~/.claude/` deploy |

## Design

### Layered defense (following build-intake precedent)

The build-intake enforcement pattern (SIG-045, 5-layer defense) is the
reference architecture. This spec deploys Layer 1 (session-start banner +
posture anchor) as the minimum viable mechanism. Layers 2–5 remain future
iterations if drift rate doesn't drop.

| Layer | Mechanism | Status |
|---|---|---|
| 1. SessionStart banner | Hook injects posture as additional context at session boot | **Deployed** (`autonomy-grant-check.sh`, 2026-04-22) |
| 2. 4-gate pre-flight helper | Documented protocol walked mentally before any "ask" | Documented below; enforcement is behavioral |
| 3. Soft-queue regex deepening (Stop hook v2) | Second detector in Stop hook — catches soft-queue tail phrases on pre-authorized continuation even when recommendation marker present | **Deployed** (`autonomy-grant-stop-check.sh`, 2026-05-13) |
| 4. Linguistic detector (Stop hook) | Regex scan of last assistant message for bare-choice-without-recommendation pattern; blocks stop and forces revision | **Deployed** (`autonomy-grant-stop-check.sh`, 2026-04-28) |
| 5. Dispatch-prompt pre-flight check | PreToolUse hook fires BEFORE subagent dispatch; scans the dispatch prompt for proposal-framing patterns ("Brien is the decider — your answers are PROPOSALS", `status: proposed`, "for Brien's review", etc.); blocks if detected without override token | **Deployed** (`autonomy-grant-dispatch-prompt-check.sh`, 2026-05-19) |
| 6. Drift telemetry | Log every gate-check + every catch for feedback loop | Partially deployed via Layer 4/5 audit logs; no active feedback loop yet |

### Layer 1: SessionStart hook

**Behavior:** on every new session start, Claude Code reads the autonomy
posture hook output and injects it as additional system context. The content
is load-bearing because it fires BEFORE the first response, anchoring the
posture independent of memory-consultation patterns.

**Hook script:** `Core/frameworks/intent/hooks/autonomy-grant-check.sh`

**Deploy target:** `~/.claude/hooks/autonomy-grant-check.sh` (symlink or copy)

**Registration:** `~/.claude/settings.json` hooks config — wire SessionStart
event to the script.

### The 4-gate check (Layer 2 — documented protocol)

For every decision that might otherwise be framed as a proposal:

1. **Reversible?** — can the action be undone without external side effects?
2. **Local blast?** — do changes land inside Workspaces, not in external
   systems (Slack, email, PRs, calendar, money movement)?
3. **Precedent?** — has a similar decision been made before, OR is there an
   explicit autonomy grant that covers this class?
4. **No info gap?** — is there no missing information that only Brien can
   supply (domain-specific knowledge, strategic direction, confidentiality)?

**If all 4 pass:** EXECUTE + SIGNAL. Do not propose. Do not queue for review.
Do not ask permission.

**If any fail:** surface the specific failing gate as the decision point, not
the whole decision.

### Forbidden inverse-discipline patterns

Architecturally equivalent to proposal-framing on L4-eligible work:

- `status: proposed` on reversible local decisions
- "Phase 2 retrofit" lists that split trivially-combinable work
- "design-then-execute" splits that add no safety value
- "would you like me to" framing when all 4 gates pass
- Queuing reversible work for approval instead of executing
- Ending a response with a question when execution was the right move
- **Bare-choice-instead-of-recommendation:** ending a response with "Want me to A, or B?" / "Should I X or Y?" without a preceding commitment marker. Layer 4 detector catches this pattern.
- **Soft-queue framing on pre-authorized continuation** — when the next stage is in the same pre-authorization envelope as work already executed in the session AND the 4-gate check would pass for the next stage, do NOT close the response with phrases that frame execution as awaiting permission. The recommendation-marker preceding such phrases does NOT redeem them; they are architecturally equivalent to bare-choice on pre-authorized work. Specifically forbidden tails after recommendation: `"Say go and I X"`, `"unless you want me to pause"`, `"want me to dispatch?"`, `"shall I proceed?"`, N-item "decision queue" framing on items that are synthesis inputs rather than L0-gated decisions.

  _Origin: SIG-AUTONOMY-DRIFT-POST-STAGE-2026-05-13 (PCU Wave 1b incident, 2026-05-13). Reinforcement chain: SIG-PERSONAS-013 → SIG-COH-DEBT-018 → RETRO-2026-04-21-autonomy-grant-reinforcement-SIG-1 → this amendment._

### Layer 4: Stop hook (linguistic detector)

**Behavior:** on every assistant turn-end, the Stop hook reads the last assistant message from the session transcript and runs two regex checks:

1. **Bare-choice pattern** (last 1000 chars): `(want me to|should i|should we|do you want me to|would you like me to|do you want to|want to|shall i)\s+[^?]{3,200}\bor\b\s+[^?]{3,200}\?`
2. **Recommendation marker** (full response, inclusive list): `i recommend`, `my recommendation`, `i'd recommend`, `recommendation:`, `my pick`, `i'd lean`, `my read`, `bottom line`, `tl;dr`, `i'd go with`, `i'd choose`, `going with`, `going to <verb>`, `my call`, `i'll <verb>`, `let's <verb>`, `**recommend`, `recommend.`, `locking in`, `committing to`, `the right move is`, `pick (a|one|the)`, `i'd say`, `my take`, `the move is`, `i lean`, `i'm going (with|to)`, etc.

**Trigger condition:** bare-choice present AND no recommendation marker anywhere in response → block.

**Block behavior:** emits `{"decision": "block", "reason": "..."}`. Claude Code does not stop the assistant; the reason is injected as context and the assistant continues to revise the response.

**Bypass:** `AUTONOMY_GRANT_STOP_BYPASSED=1` env var skips the check (no audit log entry needed because nothing was caught — the hook simply exits early).

**Audit log:** every catch is logged to `~/.claude/audit/autonomy-grant-stop-detections.log` for review and regex-tuning.

**Recursion guard:** the hook honors `stop_hook_active: true` (Claude Code sets this when the Stop hook has already fired in the current cycle), preventing infinite block-revise loops.

**Calibration:** designed conservative — false-negative bias preferred over false-positive. The recommendation regex is deliberately inclusive so legitimate responses with any commitment signal pass through; only egregious bare-choice patterns trigger.

**Hook script:** `Core/frameworks/intent/hooks/autonomy-grant-stop-check.sh`

**Deploy target:** `~/.claude/hooks/autonomy-grant-stop-check.sh` (symlink)

**Registration:** `~/.claude/settings.json` hooks config — `Stop` event with `matcher: "*"`.

### Layer 5: Dispatch-prompt pre-flight check (PreToolUse on Agent)

**Motivation:** Layers 1–4 operate within the parent session's response lifecycle. They do not inspect the prompts sent to dispatched subagents. The drift documented in SIG-PROCESS-DRIFT-PR-STYLE-REVIEW-2026-05-19 was injected at dispatch time — the parent session wrote proposal-framing instructions into the subagent prompt, and the subagent executed faithfully to spec. The spec was wrong; no existing hook caught it before the subagent ran.

**Behavior:** on every `Agent` tool-use call (PreToolUse event), the hook reads `tool_input.prompt`, scans for proposal-framing pattern variants, and blocks dispatch if detected — before the subagent has consumed any tokens.

**Detected patterns (case-insensitive, any match triggers):**
- `Brien is the decider`
- `your answers are PROPOSALS` / `responses are proposals` / `answers are proposals`
- `status: proposed` / `status:proposed` (with or without backticks)
- `not closures`
- `propose answers` / `propose your answers`
- `for Brien's review` / `for review by Brien` / `Brien to review` / `Brien to approve` / `Brien to decide`
- `proposed, not ratified` / `proposals, not closures`
- `submit for review`

**Override token:** any line in the dispatch prompt matching `# AUTONOMY-OVERRIDE-PROPOSAL-FRAMING-INTENTIONAL: <justification>` suppresses the hook and logs the override. Use only when the work is genuinely L0 (external human review required — e.g., Chris consent gate, cross-org legal review).

**Block behavior:** emits `{"decision": "block", "reason": "..."}` with full correction guidance including the 4-gate check protocol and the override token syntax.

**Bypass:** `AUTONOMY_GRANT_DISPATCH_BYPASSED=1` env var skips the check (logged to audit).

**Audit log:** `~/.claude/audit/autonomy-grant-dispatch-detections.log` — every catch, override, and bypass logged.

**Tests:** `Core/frameworks/intent/tests/test_autonomy_grant_dispatch_hook.sh` — three scenarios: T1 drift detected → block; T2 clean prompt → silent; T3 override token → silent.

**Hook script:** `Core/frameworks/intent/hooks/autonomy-grant-dispatch-prompt-check.sh`

**Deploy target:** `~/.claude/hooks/autonomy-grant-dispatch-prompt-check.sh` (symlink)

**Registration:** `~/.claude/settings.json` → `hooks.PreToolUse` → `matcher: "Agent"` (alongside existing `skill-intake-gate-check.sh`).

**Positioning vs Stop hook:** Layers 3/4 (Stop hook) catch drift in the parent session's response TEXT — "want me to dispatch?", bare-choice endings, soft-queue tails. Layer 5 catches drift in the CONTENT of what the parent dispatches — proposal-framing baked into the subagent's operating instructions. The two hooks are complementary. Stop hook = parent tone; dispatch hook = instruction content.

## Deployment

### One-time install (Brien / operator)

```bash
# From Workspaces root
ln -s "$PWD/Core/frameworks/intent/hooks/autonomy-grant-check.sh" \
      ~/.claude/hooks/autonomy-grant-check.sh
chmod +x Core/frameworks/intent/hooks/autonomy-grant-check.sh
```

Then add to `~/.claude/settings.json` under `hooks` → `SessionStart`:

```json
{
  "hooks": {
    "SessionStart": [
      {
        "matcher": "*",
        "hooks": [
          {
            "type": "command",
            "command": "~/.claude/hooks/autonomy-grant-check.sh"
          }
        ]
      }
    ]
  }
}
```

### Layer 5 install (one-time)

```bash
# From Workspaces root
ln -sf "$PWD/Core/frameworks/intent/hooks/autonomy-grant-dispatch-prompt-check.sh" \
      ~/.claude/hooks/autonomy-grant-dispatch-prompt-check.sh
chmod +x Core/frameworks/intent/hooks/autonomy-grant-dispatch-prompt-check.sh
```

Then ensure `~/.claude/settings.json` PreToolUse Agent matcher includes the hook:

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Agent",
        "hooks": [
          {"type": "command", "command": "$HOME/.claude/hooks/skill-intake-gate-check.sh"},
          {"type": "command", "command": "$HOME/.claude/hooks/autonomy-grant-dispatch-prompt-check.sh"}
        ]
      }
    ]
  }
}
```

### Verification

After install, start a new Claude Code session. The autonomy-grant banner
should appear as part of session-start context. If it doesn't, check:

1. `ls -la ~/.claude/hooks/autonomy-grant-check.sh` — file/symlink exists and is executable
2. `~/.claude/settings.json` — hook registration is syntactically valid
3. Session-start logs show the hook fired

## Success criteria

- **Immediate:** hook deployed; posture anchor appears in session-start context
  of at least one new session.
- **Observable:** at least one session runs without Brien needing to reinforce
  the autonomy posture mid-execution for L4-eligible work.
- **Durable:** across 10 consecutive sessions, zero proposal-framing slips on
  work that passes the 4-gate check. (Measured by absence of subsequent
  autonomy-grant reinforcement signals.)

## Status

`accepted` — 2026-04-22 (Layer 1 deployed). Layer 4 deployed 2026-04-28
in response to repeat bare-choice slips that Layer 1's posture anchor did
not prevent. Layer 4 audit log will inform whether Layers 3 and 5 need
deployment too.

Signal closure conditions:

- `RETRO-2026-04-21-autonomy-grant-reinforcement-SIG-1` — moves to
  `symptom-repaired` when hook is written; moves to `resolved` when hook is
  deployed to `~/.claude/hooks/` AND verified firing.
- `SIG-COH-DEBT-018` — same conditions. Mechanism-level intervention is the
  stated closure criterion in the signal body.
- **New (2026-04-28):** Layer 4 hook is deployed. Closure of the
  bare-choice-instead-of-recommendation drift requires audit-log-confirmed
  catches over multiple sessions without false-positive complaints from
  Brien.

## Related patterns

- **Build-intake gate** (SIG-045) — 5-layer defense precedent. Layers 1–2
  deployed manually; Layers 3–5 live.
- **Signal-detector Section 7** (V1–V5 lint for EXT schema) — parallel
  mechanism-level closure for chip-cascade traversal (2026-04-22).
- **Four-gate check as disciplinary primitive** — same shape as Intent arc
  (Notice/Spec/Execute/Observe): a compact test-of-readiness that fits in
  working memory and can be recited before decisions.
