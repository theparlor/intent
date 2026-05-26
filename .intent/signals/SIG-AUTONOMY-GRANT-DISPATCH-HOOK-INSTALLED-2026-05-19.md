---
id: SIG-AUTONOMY-GRANT-DISPATCH-HOOK-INSTALLED-2026-05-19
type: observe-stage-control-installed
status: resolved
date: '2026-05-19'
parent_signal: SIG-PROCESS-DRIFT-PR-STYLE-REVIEW-2026-05-19
upstream_control_path: /Users/brien/Workspaces/Core/frameworks/intent/hooks/autonomy-grant-dispatch-prompt-check.sh
catch_mechanism: PreToolUse hook on Agent dispatch + regression tests at Core/frameworks/intent/tests/test_autonomy_grant_dispatch_hook.sh (3-scenario TDD pass)
pipeline_survival: T1 drift-detected→block / T2 clean→silent / T3 override→silent; all 3 pass confirms regression caught
triggered_by:
  - "Structural-prevention candidate #1 from SIG-PROCESS-DRIFT-PR-STYLE-REVIEW-2026-05-19 §structural-prevention-candidates"
  - "Autonomy-grant spec Layer 5 slot was marked 'future iteration' — drift recurrence made it load-bearing"
---

# Observe — autonomy-grant dispatch-prompt hook installed (Layer 5)

## What landed

**Hook:** `Core/frameworks/intent/hooks/autonomy-grant-dispatch-prompt-check.sh`
**Symlink:** `~/.claude/hooks/autonomy-grant-dispatch-prompt-check.sh` → source above
**Event:** PreToolUse on `matcher: "Agent"` — fires BEFORE subagent dispatch, before any tokens consumed by the subagent
**Wired in:** `~/.claude/settings.json` PreToolUse Agent block (alongside `skill-intake-gate-check.sh`)
**Tests:** `Core/frameworks/intent/tests/test_autonomy_grant_dispatch_hook.sh` — 3/3 pass

## What it catches

Dispatch prompts that inject proposal-framing into L4-eligible reversible work:
- `Brien is the decider — your answers are PROPOSALS, not closures`
- `status: proposed` / `status:proposed` (with or without backticks)
- `for Brien's review` / `Brien to review` / `Brien to approve`
- `answers are proposals` / `proposals, not closures` / `not closures`
- `propose answers` / `propose your answers`
- `proposed, not ratified` / `submit for review`

## What it does NOT catch (by design)

Prompts that are genuinely L0 — verified external human review required — may use the override token:
`# AUTONOMY-OVERRIDE-PROPOSAL-FRAMING-INTENTIONAL: <one-line-justification>`

Override is logged to `~/.claude/audit/autonomy-grant-dispatch-detections.log`.

## Hook-as-safety-net framing

This hook is a SAFETY NET above the discipline, not the discipline itself.

The discipline is: parent sessions that understand the autonomy posture write dispatch prompts that execute + signal, not propose + queue. The memory entries (`feedback_autonomy_grant_drift_pattern.md`, `feedback_post_stage_handoff.md`), the SessionStart banner (Layer 1), and the 4-gate check (Layer 2) ARE the discipline.

The dispatch-prompt check (Layer 5) catches the case where a parent session's autonomy understanding was correct at the response layer (Stop hook passes, no soft-queue tail, no bare-choice ending) but the dispatch prompt itself was inconsistent with the posture. This is the specific drift vector in SIG-PROCESS-DRIFT-PR-STYLE-REVIEW-2026-05-19 that the Stop hook could not catch.

## Closure-discipline triad

`upstream_control_path:` `/Users/brien/Workspaces/Core/frameworks/intent/hooks/autonomy-grant-dispatch-prompt-check.sh` + wired in `~/.claude/settings.json` PreToolUse Agent matcher

`catch_mechanism:` PreToolUse hook fires on every Agent tool dispatch; pattern scan catches proposal-framing before subagent receives any tokens; block emits `{"decision": "block", "reason": "..."}` with correction guidance including 4-gate check + override token syntax

`pipeline_survival:` `Core/frameworks/intent/tests/test_autonomy_grant_dispatch_hook.sh` — T1 (drift detected → block), T2 (clean prompt → silent), T3 (override token → silent); hook regression caught if any of the 3 tests fail

## Cross-references

- Parent drift signal: `SIG-PROCESS-DRIFT-PR-STYLE-REVIEW-2026-05-19.md` (§structural-prevention-candidates #1)
- Spec (Layer 5 documented): `Core/frameworks/intent/spec/autonomy-grant-enforcement.md`
- Sibling hook (Stop, Layers 3/4): `Core/frameworks/intent/hooks/autonomy-grant-stop-check.sh`
- Audit log: `~/.claude/audit/autonomy-grant-dispatch-detections.log`
- Memory: `feedback_autonomy_grant_drift_pattern.md`, `feedback_post_stage_handoff.md`, `feedback_decision_framing.md`
