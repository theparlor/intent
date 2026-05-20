---
title: Closure Discipline Enforcement
type: framework
maturity: final
confidentiality: internal
reusability: adaptable
created: 2026-05-01
depth_score: 4
depth_signals:
  file_size_kb: 6.1
  content_chars: 5895
  entity_count: 0
  slide_count: 0
  sheet_count: 0
  topic_count: 0
  has_summary: 0
vocab_density: 0.51
---
# Closure-Discipline Enforcement

> Mechanism-level fix for symptom-patch-disguised-as-resolution drift.
> Parallel architecture to `autonomy-grant-enforcement.md`.

## The Drift Pattern

When closing a fix/audit/cleanup task, the model defaults to declaring
"resolved" / "complete" / "done" while only patching the visible symptom.
The upstream control that prevents recurrence is absent, untested, or
not-wired. The user has to push back to extract the actual upstream fix.

This violates the existing closure-DoD policy at
`Core/frameworks/intent/spec/signal-stream.md`:
- `status: resolved` REQUIRES `upstream_control_path:` AND `catch_mechanism:`
- Otherwise use `status: symptom-repaired, upstream-pending` or `deferred`

The policy exists. Memory + signals + reinforcement haven't closed the drift.
**This spec adds mechanism-level enforcement at write boundary.**

## Architectural Parallel

Mirror the autonomy-grant-enforcement architecture exactly:

| Layer | Autonomy-grant | Closure-discipline |
|---|---|---|
| 1. Spec | `autonomy-grant-enforcement.md` | `closure-discipline-enforcement.md` (this file) |
| 2. SessionStart hook | `autonomy-grant-check.sh` | `closure-discipline-check.sh` |
| 3. Memory file | `feedback_decision_framing.md` | `feedback_closure_discipline.md` |
| 4. Stop hook (text) | `autonomy-grant-stop-check.sh` | `closure-discipline-stop-check.sh` |
| 5. PreToolUse hook (artifact) | (n/a) | `closure-discipline-signal-check.sh` |

Layer 5 is new — autonomy-grant doesn't need an artifact-level check
because the drift it catches is purely conversational (proposal-framing in
response text). Closure-discipline drift produces a durable artifact (the
signal file) that outlives the conversation; that artifact must be gated.

## Detection Specifications

### Layer 4 — Stop hook (response text)

**Trigger:** Response text ends (last 1500 chars) with completion-claim
language.

**Completion-claim language (any of):**
- "complete." / "completed." / "done." / "resolved." / "fixed." / "shipped."
- "wave closed" / "wave landed" / "wave done" / "wave complete"
- "session-end" / "session over" / "session complete"
- "all done" / "all set" / "all resolved" / "all clear"
- "everything's working" / "everything works" / "fully working"
- "✅ done" / "✅ complete" / "✅ resolved" / "✅ fixed"

**Upstream-control mention (any of, anywhere in response):**
- "upstream control" / "upstream fix" / "upstream resolver"
- "wired into" / "in the pipeline" / "in render_all" / "in render pipeline"
- "stage in" / "stage of " (e.g., "Stage 1 of render_all")
- "invariant added" / "catch-net" / "catches future" / "future regression"
- "auto-extract" / "auto-flow" / "auto-populate" / "auto-fill"
- "permanent fix" / "won't recur" / "no recurrence" / "regression prevention"
- "extends [hook|policy|spec]" / "added to chain_audit" / "added invariant"
- "I-TAGLINE" / "I-V2MAX" / "I-FRAMEWORKS" / "I-DEPTH" — invariant IDs
  count as catch-net mention
- explicit honest statement of NO upstream control: "no upstream control
  installed" / "this is a one-shot" / "downstream-only" / "patched, not
  fixed" / "symptom-repaired"

**Block condition:** completion-claim present AND upstream-control absent.

**Block message:** Force the model to either (a) install upstream control
and rephrase, or (b) honestly downgrade to "symptom-repaired,
upstream-pending" with a follow-up signal capturing what the upstream
control would need to be.

### Layer 5 — PreToolUse hook (signal file writes)

**Trigger:** Write or Edit tool call targets a path matching
`*/.intent/signals/*.md`.

**Inspection:** Parse YAML frontmatter (if present). Look for `status:`
field.

**Block condition:** `status: resolved` (or `status: closed`, `status:
done`) AND missing BOTH `upstream_control_path:` AND `catch_mechanism:`.

**Block message:** Either add the required frontmatter fields or downgrade
status to `symptom-repaired, upstream-pending` per closure-DoD policy.

**Bypass:** `CLOSURE_DISCIPLINE_SIGNAL_BYPASSED=1` (logged).

## Failure-Open Discipline

Both hooks fail OPEN on parse errors, missing transcripts, malformed
input — same defensive pattern as autonomy-grant-stop-check.sh. Hooks
should never block legitimate work; they only catch a specific drift
shape.

## Audit Logs

- Stop-hook detections: `~/.claude/audit/closure-discipline-stop-detections.log`
- PreTool detections: `~/.claude/audit/closure-discipline-signal-detections.log`

Same format as autonomy-grant: timestamped one-liner with session_id and
sample of caught text.

## Bypass Flags

For tests, automation, or known-correct usage:
- Stop hook: `CLOSURE_DISCIPLINE_STOP_BYPASSED=1`
- Signal hook: `CLOSURE_DISCIPLINE_SIGNAL_BYPASSED=1`

Both are logged (so bypass is visible in audit).

## Doctrine Alignment

- "Errors are signals; resolved means upstream control installed, not
  ran the repair script" (memory: feedback_errors_are_signals.md)
- "Audit is catch-net, write-through is primary fix" (memory:
  feedback_audit_vs_writethrough.md)
- "Signal closure policy: resolved requires upstream control + file
  path + catch-mechanism" (memory: reference_signal_closure_policy.md)
- "Most direct path always wins" — these hooks ARE the direct fix at the
  mechanism layer; downstream reminding has been tried and failed.

## When This Spec Itself Updates

Drift patterns evolve. If the model learns to bypass the hook by
avoiding the trigger language (says "shipped" instead of "complete"
without saying anything in the upstream-control list), update the
detector regex. This is normal hook maintenance, same as autonomy-grant
v0 → v1.

If a third drift pattern emerges with the same architectural shape,
extract a shared `behavioral-discipline-hook` library at that point —
not before (per Wardley: don't optimize the second instance prematurely;
let pattern emerge across N=3+).
