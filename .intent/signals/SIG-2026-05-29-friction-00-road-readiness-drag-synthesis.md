---
id: SIG-2026-05-29-friction-00-road-readiness-drag-synthesis
created: 2026-05-29
type: road-readiness-friction
status: captured
severity: critical
confidence: 0.95
trust: 0.7
author: brien (via session capture)
friction_class: meta-synthesis
road_ready_gate: true
gates: [intent, coherence-engineering, parallax]
cluster: SIG-2026-05-29-friction
related:
  - SIG-2026-05-29-friction-01-stop-hook-lexical-arms-race
  - SIG-2026-05-29-friction-02-catch-net-brittleness-bidirectional
  - SIG-2026-05-29-friction-03-per-turn-preaction-tax
  - SIG-2026-05-29-friction-04-proceed-tax-paradox
  - SIG-2026-05-29-friction-05-midflight-tool-blocks-bypass-incantations
  - Core/frameworks/intent/spec/autonomy-flight-model-v1-DRAFT.md
  - Core/frameworks/intent/spec/autonomy-posture-check-layer-4.2-DRAFT.md
  - Core/frameworks/intent/spec/closure-discipline-enforcement.md
  - SIG-2026-05-26-risk-aversion-overtune-vs-trust-framework
  - feedback_audit_vs_writethrough
  - feedback_autonomy_grant_drift_pattern
---

# Road-readiness Drag synthesis — the enforcement layer is accreting reactively, unmeasured, and is itself the blocker

## The request that produced this cluster

Brien (2026-05-29): *"Are there specific instructions or memories from working
with me, or hooks, or other things we have implemented that pause you or slow you
down — explicitly add them to a series of signals of to-be-investigated friction
in our modeling and approach that need to be operationalized better before we can
consider Intent and Coherence and Parallax to be road ready."*

This is the index/synthesis signal for that series (children: friction-01…05).

## The headline

We have built a large, live, monotonically-growing behavioral-enforcement layer to
correct one dominant drift (caution-bias toward asking-before-acting) and a second
(symptom-patch-disguised-as-resolution). Each addition was filed as a **`status:
resolved` control-upgrade** and treated as a win. **No one has measured the
aggregate.** The sum of these "wins" is unbounded, unmeasured **Drag** — the exact
force the autonomy-flight-model names (`W/T/L/D`) and the exact force the flight
model's own ratification backlog does not instrument.

This is not a complaint about any single hook. Each hook is individually defensible.
The friction is **structural and emergent**: the layer has no value term, no Drag
budget, no convergence proof, and no operator-portability story. You cannot hand
another human a framework whose discipline is a 34 KB regex that grew check-by-check
and whose own design spec admits it can't converge (friction-01).

## What is actually wired right now (verified 2026-05-29)

`~/.claude/settings.json` wires **15 hook scripts** across PreToolUse / PostToolUse /
Stop / SessionStart. The two behavioral-discipline drift classes alone consume a
**6-layer stack each**:

| Layer | Caution-bias (autonomy-grant) | Symptom-patch (closure-discipline) |
|---|---|---|
| 1 — memory/anchor | SessionStart `AUTONOMY GRANT POSTURE` + `feedback_*` | SessionStart `CLOSURE-DISCIPLINE POSTURE` + `feedback_*` |
| 2 — spec | `autonomy-grant-enforcement.md` | `closure-discipline-enforcement.md` |
| 3 — skill | `autonomy-grant-drift-detector` | (shared) |
| 4 — lexical Stop hook | `autonomy-grant-stop-check.sh` (6 CHECKs, **34 KB**) | `closure-discipline-stop-check.sh` (**11 KB**) |
| 4.2 — structural Stop hook | `…layer-4.2-DRAFT.md` (warn-only, **unshipped**) | — |
| 5 — PreToolUse artifact gate | `autonomy-grant-dispatch-prompt-check.sh` | `closure-discipline-signal-check.sh` |

Plus: `native-connector-precedence-check.sh`, `skill-intake-gate-check.sh`,
`forge-shim-gate-check.sh`, `forge-signal-cadence-stop-check.sh`,
`engagement-signal-cadence-check.sh`, `overwatch-staleness-check.sh`,
`overwatch-nested-init-check.sh`, `signal-recorder-silent-check.sh`,
`count-check.sh`.

## Why this is a road-readiness gate (not just an annoyance)

The flight-model spec (`autonomy-flight-model-v1-DRAFT.md`) already proves the theory:

- **§1** — *"A gate with no value term operationalizes caution, not strategy.
  Intent's stated purpose is to operationalize strategy. v1 misses its own brief."*
- **§3** — **Stall** (acting too cautiously → Observe loop starves → calibration
  corpus stops growing → gate tightens next cycle) is *"the worse crash for Intent
  specifically."* The enforcement layer is a stall-generating machine: it rewards
  asking and penalizes un-asked action, with no counter-incentive on over-asking
  (see `SIG-2026-05-26-risk-aversion-overtune-vs-trust-framework`).

The flight model is the **designed** replacement. It is **blocked on 4 ratification
dependencies** (calibration-corpus λ-fit, Witness mandatory-recorder WS-DDR, 5 Cast
bravery-prior intakes, `panel-critique-v2-balanced` Forge operator) and the structural
Layer 4.2 check is **warn-only / not live**. So today the lexical arms-race layer is
the *only* thing actually running — the thing its own author says cannot converge.

**Road-ready means:** an operator who is not Brien can adopt Intent/Coherence/Parallax
and get disciplined autonomy without (a) a 34 KB regex they can't reason about, (b)
secret bypass env-vars they must memorize, (c) a per-turn latency tax no one budgeted,
or (d) a gate that structurally produces stall. None of those four hold today.

## The operationalization backlog (what "better" looks like)

1. **Instrument aggregate Drag before adding the next check.** The audit logs and
   `~/.claude/logs/autonomy-stop-check.jsonl` telemetry already exist per-hook.
   Nothing rolls them up. Build one Drag dashboard: total fire rate, false-positive
   rate, per-turn pre-action latency, cumulative hook count over time. Make the
   accretion visible. This is the `feedback_audit_vs_writethrough` lesson applied to
   the enforcement layer itself: the catch-nets need a catch-net.
2. **Ship the structural replacement, then sunset the lexical layer on a measured
   schedule.** Layer 4.2 (positive-execution posture) + flight-model decision-compute
   replace "match forbidden phrases" with "verify the right thing happened." Set an
   explicit retirement date for CHECKs 1–6 once the structural check clears
   calibration — otherwise the regex layer lives forever as belt-and-suspenders Drag.
3. **Make every bypass data-driven, not a secret incantation** (friction-05).
4. **Adopt a "no net-new lexical CHECK without a sunset clause + a Drag-budget
   debit" rule.** The next CHECK-N must show the aggregate FP rate and per-turn cost
   it adds, and what it will be retired against.
5. **Treat the flight-model ratification backlog as the critical path for all three
   products' road-readiness**, not as one product's internal spec.

## Trust factors

- Clarity: 0.95 — Brien named the friction and the road-readiness frame explicitly.
- Blast radius: org-wide — governs every session's behavior across every product.
- Reversibility: high for the inventory; medium for the layer (sunsetting hooks is
  reversible but the lexical layer drifts back without a Drag budget).
- Testability: high — Drag is measurable; the flight-model loss function is computable.
- Precedent: this is the same drift class as the trust-framework-contradiction signal
  (2026-05-26) and the audit-vs-writethrough exemplar, generalized to the whole layer.

## Remediation log

**2026-05-29 — first level landed** (Brien: *"hit the first level and stage the second"*).
- **Capped:** lexical layer frozen at CHECK 6 — `Core/frameworks/intent/hooks/lexical-layer-freeze.yaml`.
- **Instrumented:** `Core/frameworks/intent/tools/drag_dashboard.py`. First aggregate-Drag
  reading: **1,463 Stop-hook runs (2026-04-15→05-29), 61 blocks, 4.17% block rate →
  95.8% of runs changed nothing. CHECK 3 = 0 fires, CHECK 2 = 1 fire** (retire candidates).
  Cap-guard armed (exit 2 on accretion-drift).
- **Published successor:** `autonomy-flight-model-v1-DRAFT.md` header note +
  `autonomy-grant-enforcement.md §"The cap"`; Layer-6 telemetry row updated
  ("no feedback loop yet" → the dashboard IS the loop).
- **Staged second level:** `autonomy-flight-model-ratification-tracker.md` — D1–D4 +
  the near-term sunset train (Layer 4.2 calibration → retire CHECK 2/3, demote the rest).

Status stays **captured** (open): the lexical layer still runs at ~96% overhead.
Convergence = the *sunset*, which is staged, not done. First-level remediation +
measurement are in place; this is not `resolved`.

## Companion: the F-series (live operational friction)

A parallel session, working this same standing instruction during 2026-05-29 Cast work,
captured a complementary catalog — `SIG-2026-05-29-road-readiness-friction-series`
(items F-1..F-8). That series captures **live operational instances**; this series
(friction-00..05) captures the **structural / measurement thesis**. Two halves of ONE
backlog, not duplicates. Mapping:

| F-series (live instance) | ↔ this series (structural) |
|---|---|
| **F-1** regex can HANG the Stop hook (self-DoS, ugrep backtracking) — S1 | friction-01 + friction-02 |
| **F-8** closure hook false-fires on conversational words (observed live) — S2 | friction-02 (false-positive class) |
| **F-4** closure-discipline NOT enforced on automated writers (asymmetry) — S1 | friction-00 — **new angle** |
| **F-2 / F-3** render_all non-deterministic + verify/produce conflation — S2 | friction-03 (per-turn tax) adjacent |
| **F-5 / F-6 / F-7** repo-topology / data-substrate / index drift — S3 | coherence debt |

The first-level rollout already touches several: the freeze stops new regexes (F-1 root),
Layer 4.2's structural approach is the template for F-8, and the `skip_rules.py` fix this
session is the same catch-net-brittleness class as F-1/F-8. **Reconciliation pending
Brien:** unify the numbering into one backlog or keep as a paired series; F-1 and F-4
(both S1) warrant their own ratifiable specs.

## Open (for Brien / ratification review)

- Is the Drag dashboard a Witness consumer, a Topography surface, or a standalone
  inventory tool extending `intent_signal_inventory.py`?
- Who owns the sunset schedule for the lexical CHECKs — Tower (Loom) or a dated DDR?
- Does "road-ready" require the flight model *shipped*, or the lexical layer *capped
  and measured* with the flight model as the published successor path? (Recommend the
  latter as the nearer-term gate; the former as the v2 milestone.)
