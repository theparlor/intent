---
signal_id: SIG-F-001-signal-closure-policy-gap
title: Intent framework lacks signal-closure policy — premature-closure pattern is structural, not local
severity: high
detected: 2026-04-16
status: open
last_triaged: 2026-06-17
source: cross-product-audit
trust_score: 0.95
autonomy: L3
related:
  - personas/SIG-006-yaml-parse-failure-pattern
  - personas/SIG-046-yaml-parse-failure-recurrence-premature-closure
  - personas/SIG-045-build-intake-enforcement
---
# Intent Framework Lacks Signal-Closure Policy

## Observation
Cross-product audit of 14 `.intent/signals/` directories (364 signals total) found ~21 signals (27% of all resolved signals) where `status: resolved` was applied after symptom repair without installing the upstream control that the signal's own Implication recommended. 5 cases are verifiably missing their promised artifact:

1. `personas/SIG-006-yaml-parse-failure-pattern.md` — validation gate never installed; recurred as SIG-046 in 8 days
2. `org-design-tooling/RETRO-2026-04-08-02.md` — interpreter health check never added to overwatch
3. `personas/RETRO-2026-04-08-persona-handoff-SIG-4.md` — claimed schema gate in persona-intake SKILL.md; only a one-line mention exists, no executable gate
4. `frameworks/intent/2026-04-13-overwatch-incestuous-amplification.md` — recommended updating overwatch SKILL.md; zero hits for "incestuous" in that file
5. `studio-control/RETRO-2026-04-08-030-sd-symlink-silent-failure.md` — no preventive script or pre-flight check installed

## Root Cause
`Core/frameworks/intent/spec/signal-stream.md` defines a lifecycle (`captured → active → clustered → promoted → dismissed`) but treats `resolved` as a free-text status field with **no closure criteria** and no DoD. Each product improvises. When a repair script is easier than a gate, closers pick the repair. The cost (recurrence, trust erosion, wasted audit cycles) is externalized to future sessions.

## Implication
Without a closure policy, the Intent framework cannot prevent the class of regression where "we fixed this" becomes "we'll fix it again next month." This defeats the Observe→Knowledge double-loop (decision #11): observations that should update domain understanding get short-circuited by symptom repairs that don't propagate.

The build-intake enforcement (SIG-045) addresses the intake side — work can't start without DoR. The closure side is the mirror: work can't close without DoD. Signal-closure is the specific instance of that mirror for the governance layer itself.

## Resolution (implemented 2026-04-16)

- **Closure criteria added to `spec/signal-stream.md`** under "Signal Lifecycle > Closure Criteria": `resolved` requires upstream control installed OR explicit deferral with rationale + reassess_by date. Intermediate state `symptom-repaired, upstream-pending` added for the repair-only case.
- **DoR/DoD library entry** DOD-SIG-CLOSURE-NN added to `knowledge-engine/templates/dor-dod-library.md` (see commit).
- **Operator memory** `feedback_errors_are_signals.md` updated with the closure-policy discipline.
- **Status corrections** applied to the 5 high-confidence cases listed above: moved from `resolved` → `symptom-repaired, upstream-pending` with cross-references.

## Follow-up Work (open)
- [ ] Tooling: `intent-signal lint` command that scans resolved signals and flags any missing Resolution-evidence section (upstream control citation).
- [ ] Backfill: audit the remaining ~16 suspect closures (keyword-heuristic flagged but not individually verified) and either install the upstream control or transition to `symptom-repaired, upstream-pending`.
- [ ] Overwatch integration: add "premature-closure detection" as a dimension — scan resolved signals for missing control evidence.
- [ ] DoR for signal capture: signals with Implication recommending upstream work should default-generate a spec stub when promoted, so the control has a home.

## Meta
This signal is itself a test of the new closure policy. It will NOT close as `resolved` until (1) the follow-up linter exists or is explicitly deferred with a date, and (2) the backfill audit is complete or explicitly deferred. Until then: `status: open`.

---

## Triage note — 2026-05-28 (still open)

**Status:** still open. No `intent-signal lint` command has been added to the CLI suite (`Core/frameworks/intent/bin/`). The ~16-signal backfill audit (keyword-heuristic flagged but not individually verified) has not been run. The closure-discipline spec and DoR/DoD library additions from 2026-04-16 ARE in place — those resolution items landed. But the signal's own meta-criteria require the linter OR explicit deferral with a date, which have not been set. The follow-up items remain in their original `[ ]` state.

---

## Triage note — 2026-06-17 (still open; prospective-side control landed)

**Disposition: stays open.** Re-verified `bin/` (intent-init, intent-intent, intent-knowledge, intent-signal, intent-spec, intent-status, mint-wsddr) — still NO `intent-signal lint` subcommand; `grep lint bin/intent-signal` is empty. The backfill audit of the ~16 suspect closures has still not run. The signal's own §Meta closure contract (linter exists OR explicit deferral-with-date, AND backfill complete OR deferred) remains unmet, so closing now would violate its own terms.

**What IS new since the 2026-05-28 triage:** the *prospective* (new-closure) side of the closure-policy gap now has an executable upstream control — `hooks/closure-discipline-signal-check.sh` (Layer 5 PreToolUse, created 2026-04-30, last touched 2026-06-12 for WS-DDR-113). It blocks any Write/Edit to `*/.intent/signals/*.md` that sets `status: resolved|closed|done` without both `upstream_control_path:` and `catch_mechanism:`. That is the write-through gate the closure policy needed — but it is a DIFFERENT control than the linter this signal named, and it only catches the interactive tool-layer write path (NOT direct/automated filesystem writers — see road-readiness F-4) and does NOT perform the retrospective backfill audit. Remaining gap narrowed to: (1) retrospective lint/backfill of historical resolved signals, (2) write-boundary coverage for automated batch writers. Keeping open rather than substituting the hook for the author's stated criteria.
