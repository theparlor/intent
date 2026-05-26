---
signal_id: SIG-PLAN-ARTIFACT-CONVENTION-GATE1-2026-05-20
title: Plan-artifact-convention Gate 1 closed — Throughline pilot complete
severity: low
detected: 2026-05-20
status: resolved
source: exec-subagent (Claude Sonnet 4.6, upgrade plan execution wave)
trust_score: 0.95
autonomy: L4
upstream_control_path: Core/frameworks/intent/spec/plan-artifact-convention.md §6 Gate 1 ratification path; PLAN-THROUGHLINE-001 pilot_notice field
catch_mechanism: plan-artifact-convention §6 gate checklist; PLAN-THROUGHLINE-001 PLAN-THROUGHLINE-002 retro feeds Gate 3 (DoR/DoD definition); overwatch sweeps intent framework .intent/signals/
pipeline_survival: Gate 1 is closed; Gate 2 is unclear (check plan-artifact-convention §6); Gate 3 (DoR/DoD for plans) is now the next priority; convention adjustments from Throughline retro are input
---
# SIG-PLAN-ARTIFACT-CONVENTION-GATE1-2026-05-20 — Plan-Artifact-Convention Gate 1 Closed

## What happened

PLAN-THROUGHLINE-001 (the Throughline MVP plan) was explicitly designated as the pilot for the plan-artifact-convention spec at `Core/frameworks/intent/spec/plan-artifact-convention.md`. Per that spec's §6 ratification path, Gate 1 closes on "pilot complete."

**Throughline pilot is complete as of 2026-05-20.** The plan was created (2026-04-23), the schema decision (TC-004) blocked execution for 20 days, PCU Phase 5 delivered the mechanism (2026-05-13), and this execution wave (2026-05-20) completed all remaining tasks:
- VT-001..VT-003 vision-thread stubs authored
- 5 WS-DDRs retrofitted with thread_hooks
- CE DEFINITION.md §10 updated
- Parallax CONTEXT.md updated
- SPEC-001 ratified (status: accepted)
- PLAN-THROUGHLINE-001 retro written and appended

## Learnings for convention refinement

From PLAN-THROUGHLINE-001 retro (§Convention adjustments):

1. **Add `autonomy:` field per task**, not just at plan level. Some tasks are L2 (Brien co-authorship), others L4. The plan template should expose this per task.

2. **IDD-loop-seam signal rule.** At every EXECUTE → OBSERVE transition, a `resolved` signal closes the loop AND a companion `captured` signal opens the next one. The gap between Phase 5 completion and this execution wave was 7 days with no active Notice anchor — precisely the failure mode this convention should prevent.

3. **Retro as append-not-separate is correct default.** For single-scope pilots, the plan file is the natural retro location. Separate file when plan scope spans multiple products or extended time.

## Next for plan-artifact-convention

- Gate 3 (DoR/DoD definition for plans) is the next ratification gate; Throughline retro is the input.
- The convention should explicitly specify the IDD-loop-seam signal rule as a required artifact at plan execution close.
- Check Gate 2 status in the spec before claiming sequential progress.

## Closure DoD

- [x] Pilot plan (PLAN-THROUGHLINE-001) completed and retro written
- [x] Convention adjustments documented in retro §Convention adjustments
- [x] Signal emitted to intent framework .intent/signals/ per T7 of PLAN-THROUGHLINE-001
- [x] upstream_control_path: plan-artifact-convention.md §6 gate checklist
- [x] catch_mechanism: convention spec §6 gate tracking; overwatch sweeps intent .intent/signals/
- [x] pipeline_survival: Gate 3 (DoR/DoD) is next; Throughline retro feeds it
