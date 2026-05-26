---
decision_id: RETRO-2026-04-30-closure-discipline-1
title: Build multi-layer closure-discipline hook architecture paralleling autonomy-grant-enforcement
date: 2026-04-30
status: accepted
source: retroactive-extraction
session_date: 2026-04-30
references:
  - Core/frameworks/intent/spec/closure-discipline-enforcement.md
  - Core/frameworks/intent/spec/autonomy-grant-enforcement.md
  - Core/frameworks/intent/spec/signal-stream.md
---
# Multi-layer closure-discipline hook architecture paralleling autonomy-grant

## Context
Recurring drift pattern surfaced multiple times in single session: symptom-patch disguised as resolution. Model declared "complete" / "resolved" while only patching visible symptom. The closure-DoD policy at `Core/frameworks/intent/spec/signal-stream.md` already required `upstream_control_path:` + `catch_mechanism:` for status:resolved — but the policy wasn't enforced at write boundary. Memory + reinforcement haven't closed the drift across N=3+ instances. Same architectural shape as autonomy-grant drift before its hooks: policy exists, in-flight enforcement absent.

## Decision
Install 5-layer mechanism mirroring autonomy-grant-enforcement architecture exactly:
- Layer 1: Spec — `Core/frameworks/intent/spec/closure-discipline-enforcement.md`
- Layer 2: SessionStart hook — `closure-discipline-check.sh` (loads posture)
- Layer 3: Memory file — `~/.claude/projects/.../memory/feedback_closure_discipline.md`
- Layer 4: Stop hook (response text) — `closure-discipline-stop-check.sh` (blocks completion-claim language without upstream-control mention)
- Layer 5: PreToolUse hook (signal-file artifacts) — `closure-discipline-signal-check.sh` (blocks signal-file writes with status:resolved lacking required frontmatter)

Layer 5 is new vs. autonomy-grant pattern — autonomy-grant catches purely conversational drift; closure-discipline drift produces a durable signal-file artifact that needs gating at the write tool layer.

## Alternatives Considered
- Extend the existing autonomy-grant hook to cover both: rejected per Wardley advice in panel critique — different drift shapes (proposal-framing pre-action vs false-completion post-action), different trigger windows. Two hooks is correct. Wait for N=3 to extract shared lib.
- Single Stop hook with combined detection: rejected as conflating signals; separate hooks give cleaner audit logs.
- Re-train via prompts only: rejected because that approach has been tried and failed across the recurring drift instances; reinforcement-resistant.

## Consequences
Future sessions start with both autonomy-grant + closure-discipline hooks active. Bare-choice / proposal-framing on L4-eligible work continues to be caught by autonomy-grant. False-completion claims and signal-file writes with insufficient frontmatter are now caught by closure-discipline. If a third drift pattern emerges with the same architectural shape (write-boundary linguistic-pattern enforcement), extract a shared `behavioral-discipline-hook` library at that point.

Audit logs at `~/.claude/audit/closure-discipline-{stop,signal}-detections.log`. Bypass flags (logged): `CLOSURE_DISCIPLINE_{,STOP_,SIGNAL_}BYPASSED=1`.
