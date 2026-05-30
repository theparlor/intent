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
- **Status:** TOOLING FIXED + verified 2026-05-29. Root bug found and fixed:
  `tools/skip_rules.py` skipped `.intent/`/`.context/` dirs (a 2026-05-28
  sibling-walker-skip regression), so `intent_signal_inventory.py` returned 0
  artifacts. Now returns **1,551 artifacts / 460 labeled-gold**. Real λ re-fit in
  progress (replacing provisional manual-compute values an earlier broken-tool run
  produced; the destroyed 2026-05-26 corpus was restored from git). Tools:
  `intent_signal_inventory.py`, `extract_calibration_corpus.py`, `lambda_fit.py`,
  `apply_lambda_settings.py`.
- **DoR (entry):** inventory script runs clean over all `**/.intent/signals/` +
  `decisions` corpora; signal-schema backfill gap (W/T/L/D fields) assessed.
- **DoD (exit):** structured `(inputs, outcome, grant_correctness)` rows produced; λ fit
  per product, persisted to each product's `.intent/INTENT.md` `lambda_settings`. Closure
  signal cites the fit source + row count. `upstream_control_path:` = the fit pipeline;
  `catch_mechanism:` = λ-refit triggers (flight-model §16).
- **Pull trigger:** ready now; gated only on Brien starting the v2 train.
- **Update 2026-05-30:** the λ-orphan upstream control is now INSTALLED —
  `apply_lambda_settings.py --commit` (tree-aware write-through) + `lambda_orphan_check.py`
  (durable catch-net, exit 2 on any uncommitted managed λ block). This closes the
  `catch_mechanism` the DoD called for: a λ-fit no longer leaves uncommitted orphans across
  repos (the SYMPTOM-REPAIRED/UPSTREAM-PENDING gap from the cross-session synthesis §6).
  Commit a0b8ead (theparlor/intent).

## D2 — Witness mandatory-recorder WS-DDR
- **Status:** ✓ SATISFIED — already ratified as **WS-DDR-098** (2026-05-26, Brien
  direct authorization). This tracker's prior "NOT STARTED" was stale; the
  flight-model spec also cited the wrong number (WS-DDR-090 → corrected to 098 on
  2026-05-29). No new DDR needed (the speculative WS-DDR-102 draft was retired).
- **DoR:** Witness ingest path stable enough to mandate; WS-DDR drafted in
  `Workspaces/.context/DECISIONS.md` per DDR template.
- **DoD:** WS-DDR ratified + governance commit pushed (per `feedback_ratification_includes_governance_commit`); products emitting autonomy decisions route through Witness; non-routing products flagged "Intent-decorated, not Intent-enabled."
- **Pull trigger:** Brien-set — this is a governance decision, not an L4 execution.
- **Blocks:** D-WIRE (the shadow-autonomy protocol §9 needs Witness as recorder).

## D3 — Cast bravery-prior intakes (min 5)
- **Status:** ✓ SATISFIED — 5 registry entries exist (bravery-prior-batch, 2026-05-26):
  steve-jobs, andy-grove, marc-andreessen, paul-graham, ben-horowitz — each with
  risk_appetite + decision_stance + panel_role (bold-prior) metadata (provenance field
  backfilled 2026-05-29). Slate matches flight-model §10. Browser regen pending to surface in UI.
- **DoR:** persona-intake pipeline ready (it is); slate confirmed by Brien (the bold-prior
  selection is a judgment call — info gap → his to set).
- **DoD:** ≥5 registry entries in `Core/products/cast/farm/registry/` with risk-appetite
  + decision-stance fields; closure signal lists slugs.
- **Pull trigger:** Brien confirms the slate, then intake is L4-executable.

## D4 — Forge `panel-critique-v2-balanced` operator
- **Status:** ✓ DONE (emit side) 2026-05-29. The operator existed as a 2026-05-26 draft
  that emitted only QUALITATIVE variance (low/mod/high); upgraded to emit a TYPED
  per-facet uncertainty vector over §4's 7 estimands — `per_persona` never merged (Voices
  law), `point_estimate`=median, `dispersion`=max−min, plus `cross_bucket_split.gap`.
  Files: `Core/products/forge/outputs/claude-code/critique/panel-critique-v2-balanced/`
  (SKILL.md + variance-estimate.md). Panel: Torres + Cagan (safety; Cagan→
  engineering-excellence-advisor for eng/ops artifacts) + 2 bold (deterministic
  ops-rigorous×conviction pairing) + per-run wildcard. Consumer side (deterministic model
  reading the block) = §15 step-6 D-WIRE. presets.yml integration pending.
- **DoR:** D3 personas exist (panel needs bold priors to compose); §10 recipe finalized.
- **DoD:** operator rendered in `Core/products/forge/`; emits variance as a typed estimate
  the deterministic model consumes; closure signal shows a sample panel run.
- **Pull trigger:** after D3.

## D-WIRE — Wire the deterministic flight model (the barrier step)
- **Status:** All four §11 deps SATISFIED (2026-05-29) AND the D-WIRE implementation is
  now **BUILT** (2026-05-30): `Core/frameworks/intent/tools/flight_model.py` — the
  deterministic coupled-forces layer consuming panel-critique-v2-balanced's typed variance
  vector, emitting W/T/L/D + autonomy band + envelope (stall/airworthy/overspeed) +
  recommended action. 16/16 tests incl. the value-term/stall test. λ scalar w/ per-surface
  override (§12); hooks 1–7 remain the deterministic floor. **First live reading is a STALL** —
  fed the measured Drag (0.958 overhead from `drag-report.json`), T = strategic_value × λ does
  not clear D, so the model diagnoses the current enforcement layer itself as the stall crash
  §3 warns of. (Commit 44aadb2, theparlor/intent.) Remaining to v1→v2 ratification: the 30-day
  shadow flight-test (Layer 4.2 warn-only since 2026-05-29 → 2026-06-28), then ratify and mark
  `signal-scoring.md` superseded. The build is done; the flight-test window is not.
- **§12 defaults (resolved 2026-05-29, Brien-override-able):** (1) λ is SCALAR with
  per-surface overrides per §16 — not a vector. (2) Hooks 1–7 remain the deterministic
  FLOOR; the flight model computes the band ABOVE them via an envelope-check layer
  between Layer 5 and the band — per §13/§14. (3) fail-forward vs rollback is a COCKPIT
  choice for novel cases, deterministic for in-corpus patterns — per §6. (4) detection
  latency stays folded into Lift (no 5th force) until calibration data argues otherwise.
- **DoD:** flight model computes autonomy band; hooks 1–5 remain the deterministic floor
  in front; shadow-autonomy flight-test (§9) begins; after 30 days of flight-test data,
  ratify v1→v2 and mark `signal-scoring.md` superseded.

---

## The near-term sunset train (does NOT wait for D-WIRE)

1. ✓ DONE — Layer 4.2 built (8/8 tests pass) + wired live in **warn-only** mode
   2026-05-29 (`~/.claude/settings.json` Stop array; hook
   `hooks/autonomy-posture-check-layer-4.2.sh`). This IS the §9 shadow flight-test
   running; the 14-day calibration clock starts now.
2. Run 14-day calibration; `drag_dashboard.py` + Layer 4.2 telemetry report FP rate.
3. If FP < 5% → promote Layer 4.2 to block; **retire CHECK 3 (0 fires) and CHECK 2
   (1 fire) immediately**, demote the rest per measured block-rate.
4. Update `lexical-layer-freeze.yaml:sunset` with the executed schedule; close
   `SIG-2026-05-29-friction-01`.

This train is the cheapest path to convergence and is the recommended next pull.
