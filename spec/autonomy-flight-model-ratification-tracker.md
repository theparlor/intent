---
title: Autonomy Flight Model — Ratification Tracker (the staged second level)
id: SPEC-INTENT-FLIGHT-MODEL-RATIFICATION-TRACKER-001
created: 2026-05-29
status: staging
scope: framework
related:
  - Core/frameworks/intent/spec/autonomy-flight-model-v1-DRAFT.md
  - Core/frameworks/intent/spec/autonomy-posture-check-layer-4.2-DRAFT.md
  - Core/frameworks/intent/hooks/lexical-layer-freeze.yaml
  - Core/frameworks/intent/tools/drag_dashboard.py
  - Core/frameworks/intent/.intent/signals/SIG-2026-05-29-friction-00-road-readiness-drag-synthesis.md
---

# Autonomy Flight Model — Ratification Tracker

> **What this is.** The "second level" Brien staged on 2026-05-29 ("hit the first
> level and stage the second"). The **first level is done** (lexical layer capped,
> aggregate Drag instrumented, flight model published as successor). This document
> stages the path that lets the lexical layer actually *sunset*: the four ratification
> dependencies from `autonomy-flight-model-v1-DRAFT §11`, turned into ready-to-pull
> work items with entry/exit gates and a dependency order.
>
> **What "staged" means — and the autonomy boundary.** Nothing here is auto-executed.
> These items are **L2+ by design**: D2 is a governance WS-DDR (ratification gate), the
> others touch the gate model itself, require cross-product coordination, or carry real
> design decisions only Brien can set (λ priors, Cast risk-appetite stances, panel
> composition). They are NOT L4 reversible-local work. Staging = the work is shaped,
> sequenced, and pull-ready; the pull is Brien's. Each item, when executed, emits a
> closure-discipline-compliant signal (flight-model §15).

## Dependency order (from flight-model §15)

```
D1 calibration-corpus λ-fit ──┐
                              ├──► D-WIRE deterministic flight model as autonomy-band layer
D2 Witness mandatory-recorder ┤        (hooks 1–5 remain the deterministic floor in front)
D3 Cast bravery-prior intakes ┤              │
D4 panel-critique-v2-balanced ┘              ▼
                                   SHADOW-AUTONOMY flight-test (§9) ──► sunset CHECKs 1–6
```

D1–D4 are largely parallel; D-WIRE has a hard barrier (needs all four). The lexical-layer
sunset (`lexical-layer-freeze.yaml`) fires off the **Layer 4.2 calibration result**, which
can run on D1+D2 alone — it does not wait for the full flight model. Two release trains:
**(a) near-term** Layer 4.2 → sunset; **(b) v2** full flight-model wiring.

---

## D1 — Calibration-corpus λ-fit
- **Status:** SCAFFOLDED (furthest along). Tools exist:
  `tools/intent_signal_inventory.py` (v1, re-grounded to real schema),
  `tools/extract_calibration_corpus.py`, `tools/lambda_fit.py`,
  `tools/apply_lambda_settings.py`.
- **DoR (entry):** inventory script runs clean over all `**/.intent/signals/` +
  `decisions` corpora; signal-schema backfill gap (W/T/L/D fields) assessed.
- **DoD (exit):** structured `(inputs, outcome, grant_correctness)` rows produced; λ fit
  per product, persisted to each product's `.intent/INTENT.md` `lambda_settings`. Closure
  signal cites the fit source + row count. `upstream_control_path:` = the fit pipeline;
  `catch_mechanism:` = λ-refit triggers (flight-model §16).
- **Pull trigger:** ready now; gated only on Brien starting the v2 train.

## D2 — Witness mandatory-recorder WS-DDR
- **Status:** NOT STARTED. Governance gate (L0-class — a ratified DDR).
- **DoR:** Witness ingest path stable enough to mandate; WS-DDR drafted in
  `Workspaces/.context/DECISIONS.md` per DDR template.
- **DoD:** WS-DDR ratified + governance commit pushed (per `feedback_ratification_includes_governance_commit`); products emitting autonomy decisions route through Witness; non-routing products flagged "Intent-decorated, not Intent-enabled."
- **Pull trigger:** Brien-set — this is a governance decision, not an L4 execution.
- **Blocks:** D-WIRE (the shadow-autonomy protocol §9 needs Witness as recorder).

## D3 — Cast bravery-prior intakes (min 5)
- **Status:** NOT STARTED. Initial slate (flight-model §10): Jobs, Grove, Andreessen,
  Graham, Horowitz — each needs risk-appetite + decision-stance metadata for panel routing.
- **DoR:** persona-intake pipeline ready (it is); slate confirmed by Brien (the bold-prior
  selection is a judgment call — info gap → his to set).
- **DoD:** ≥5 registry entries in `Core/products/cast/farm/registry/` with risk-appetite
  + decision-stance fields; closure signal lists slugs.
- **Pull trigger:** Brien confirms the slate, then intake is L4-executable.

## D4 — Forge `panel-critique-v2-balanced` operator
- **Status:** NOT STARTED. Renders the §10 composition (2 conservative / 2 bold / 1
  wildcard) and outputs variance-across-panel as the typed uncertainty input for §4.
- **DoR:** D3 personas exist (panel needs bold priors to compose); §10 recipe finalized.
- **DoD:** operator rendered in `Core/products/forge/`; emits variance as a typed estimate
  the deterministic model consumes; closure signal shows a sample panel run.
- **Pull trigger:** after D3.

## D-WIRE — Wire the deterministic flight model (the barrier step)
- **Status:** BLOCKED on D1–D4.
- **DoD:** flight model computes autonomy band; hooks 1–5 remain the deterministic floor
  in front; shadow-autonomy flight-test (§9) begins; after 30 days of flight-test data,
  ratify v1→v2 and mark `signal-scoring.md` superseded.

---

## The near-term sunset train (does NOT wait for D-WIRE)

1. Ship Layer 4.2 in **warn-only** mode (design + scaffold already L4 per its spec;
   live activation needs Brien sign-off on matcher scope).
2. Run 14-day calibration; `drag_dashboard.py` + Layer 4.2 telemetry report FP rate.
3. If FP < 5% → promote Layer 4.2 to block; **retire CHECK 3 (0 fires) and CHECK 2
   (1 fire) immediately**, demote the rest per measured block-rate.
4. Update `lexical-layer-freeze.yaml:sunset` with the executed schedule; close
   `SIG-2026-05-29-friction-01`.

This train is the cheapest path to convergence and is the recommended next pull.
