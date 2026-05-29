# λ Fit v1 — Per-Product Computed Values

Generated 2026-05-26 by `lambda_fit.py` from extracted calibration corpus.

## Fit model

```
  λ_fit             = 1.0 × (1 + 0.5 × stall_loss)
  lift_investment   = 0.3 × (sym_rep_rate / max(closure_rate, 0.1))
  λ_apply_now       = λ_fit  if lift_investment < 0.15
                      midpoint  if 0.15 ≤ lift_inv < 0.3
                      baseline  if lift_inv ≥ 0.3
```

**Key insight from the fit:** containment gap (symptom-repaired / closure-compliant) is a *Lift* problem, not a *Thrust* problem. Products with high containment_gap need to manufacture more lift (catch_mechanism + upstream_control_path coverage) BEFORE raising λ — otherwise λ raise produces more symptom-repaired, not more closure.

## Per-product fit (sorted by signal count)

| Product | n | Closure% | Sym% | λ_fit | λ_apply_now | Lift action |
|---|---:|---:|---:|---:|---:|---|
| Core/products/cast | 263 | 95% | 5% | 1.025 | **1.025** | ✓ NONE |
| ROOT (Workspaces-wide) | 54 | 91% | 9% | 1.046 | **1.046** | ✓ NONE |
| Core/products/forge | 24 | 96% | 4% | 1.021 | **1.021** | ✓ NONE |
| Core/products/org-design-tooling | 18 | 50% | 50% | 1.25 | **1.0** | 🛑 REQUIRED-BEFORE-λ-RAISE |
| Core/frameworks/intent | 17 | 88% | 12% | 1.059 | **1.059** | ✓ NONE |
| Work | 17 | 35% | 65% | 1.324 | **1.0** | 🛑 REQUIRED-BEFORE-λ-RAISE |
| Core/frameworks/coherence-engineering | 13 | 62% | 38% | 1.192 | **1.096** | ⚠ RECOMMENDED |
| Core/products/library-index-mcp | 12 | 42% | 58% | 1.292 | **1.0** | 🛑 REQUIRED-BEFORE-λ-RAISE |
| Core/products/conduit | 10 | 80% | 20% | 1.1 | **1.1** | · OPTIONAL |
| Core/products/fieldbook | 7 | 71% | 29% | 1.143 | **1.143** | · OPTIONAL |
| Core/products/library-index | 7 | 57% | 43% | 1.214 | **1.107** | ⚠ RECOMMENDED |
| Core/products/cortege | 5 | 100% | 0% | 1.0 | **1.0** | ✓ NONE |
| Core/products/digital-declutter | 5 | 80% | 20% | 1.1 | **1.1** | · OPTIONAL |
| Core/products/voices | 5 | 100% | 0% | 1.0 | **1.0** | ✓ NONE |
| Core/products/warp | 5 | 100% | 0% | 1.0 | **1.0** | ✓ NONE |
| Core | 5 | 100% | 0% | 1.0 | **1.0** | ✓ NONE |
| Core/products/loom | 4 | 100% | 0% | 1.0 | **1.0** | ✓ NONE |
| Core/products/pulse | 4 | 100% | 0% | 1.0 | **1.0** | ✓ NONE |
| Core/products/studio-control | 4 | 75% | 25% | 1.125 | **1.125** | · OPTIONAL |
| Core/products/topography | 4 | 100% | 0% | 1.0 | **1.0** | ✓ NONE |
| Core/products/parallax | 3 | 100% | 0% | 1.0 | **1.0** | ✓ NONE |
| Core/products/reference-substrate | 3 | 100% | 0% | 1.0 | **1.0** | ✓ NONE |
| Core/products/witness | 3 | 100% | 0% | 1.0 | **1.0** | ✓ NONE |
| Core/frameworks/investment | 2 | 50% | 50% | 1.25 | **1.0** | 🛑 REQUIRED-BEFORE-λ-RAISE |
| Core/frameworks/knowledge-engine | 2 | 100% | 0% | 1.0 | **1.0** | ✓ NONE |
| Core/products/throughline | 2 | 100% | 0% | 1.0 | **1.0** | ✓ NONE |
| Core/frameworks/methodology-library | 2 | 0% | 100% | 1.5 | **1.0** | 🛑 REQUIRED-BEFORE-λ-RAISE |
| Core/frameworks/assessment | 1 | 100% | 0% | 1.0 | **1.0** | ✓ NONE |
| Core/frameworks/design-systems | 1 | 100% | 0% | 1.0 | **1.0** | ✓ NONE |
| Core/frameworks/governance | 1 | 100% | 0% | 1.0 | **1.0** | ✓ NONE |
| Core/frameworks/measurement | 1 | 100% | 0% | 1.0 | **1.0** | ✓ NONE |
| Core/frameworks/transformation | 1 | 100% | 0% | 1.0 | **1.0** | ✓ NONE |
| Home | 1 | 100% | 0% | 1.0 | **1.0** | ✓ NONE |
| Core/frameworks/protocols | 1 | 0% | 100% | 1.5 | **1.0** | 🛑 REQUIRED-BEFORE-λ-RAISE |

## Lift-action distribution

- **REQUIRED-BEFORE-λ-RAISE**: 6
- **RECOMMENDED**: 2
- **OPTIONAL**: 4
- **NONE**: 22

## Products needing lift investment FIRST (do not raise λ yet)

- **Core/frameworks/methodology-library**: containment_gap=10.00, closure=0%, sym=100%. λ stays at baseline 1.0 until lift work lands (target: 1.5).
- **Core/frameworks/protocols**: containment_gap=10.00, closure=0%, sym=100%. λ stays at baseline 1.0 until lift work lands (target: 1.5).
- **Work**: containment_gap=1.83, closure=35%, sym=65%. λ stays at baseline 1.0 until lift work lands (target: 1.324).
- **Core/products/library-index-mcp**: containment_gap=1.40, closure=42%, sym=58%. λ stays at baseline 1.0 until lift work lands (target: 1.292).
- **Core/frameworks/investment**: containment_gap=1.00, closure=50%, sym=50%. λ stays at baseline 1.0 until lift work lands (target: 1.25).
- **Core/products/org-design-tooling**: containment_gap=1.00, closure=50%, sym=50%. λ stays at baseline 1.0 until lift work lands (target: 1.25).

## Products ready to apply fit λ directly

- **Core/products/fieldbook**: λ_apply_now=1.143 (closure=71%, sym/closure ratio=0.40)
- **Core/products/studio-control**: λ_apply_now=1.125 (closure=75%, sym/closure ratio=0.33)
- **Core/products/conduit**: λ_apply_now=1.1 (closure=80%, sym/closure ratio=0.25)
- **Core/products/digital-declutter**: λ_apply_now=1.1 (closure=80%, sym/closure ratio=0.25)
- **Core/frameworks/intent**: λ_apply_now=1.059 (closure=88%, sym/closure ratio=0.13)
- **ROOT (Workspaces-wide)**: λ_apply_now=1.046 (closure=91%, sym/closure ratio=0.10)
- **Core/products/cast**: λ_apply_now=1.025 (closure=95%, sym/closure ratio=0.05)
- **Core/products/forge**: λ_apply_now=1.021 (closure=96%, sym/closure ratio=0.04)
- **Core/frameworks/assessment**: λ_apply_now=1.0 (closure=100%, sym/closure ratio=0.00)
- **Core/frameworks/design-systems**: λ_apply_now=1.0 (closure=100%, sym/closure ratio=0.00)
- **Core/frameworks/governance**: λ_apply_now=1.0 (closure=100%, sym/closure ratio=0.00)
- **Core/frameworks/knowledge-engine**: λ_apply_now=1.0 (closure=100%, sym/closure ratio=0.00)
- **Core/frameworks/measurement**: λ_apply_now=1.0 (closure=100%, sym/closure ratio=0.00)
- **Core/frameworks/transformation**: λ_apply_now=1.0 (closure=100%, sym/closure ratio=0.00)
- **Core/products/cortege**: λ_apply_now=1.0 (closure=100%, sym/closure ratio=0.00)
- **Core/products/loom**: λ_apply_now=1.0 (closure=100%, sym/closure ratio=0.00)
- **Core/products/parallax**: λ_apply_now=1.0 (closure=100%, sym/closure ratio=0.00)
- **Core/products/pulse**: λ_apply_now=1.0 (closure=100%, sym/closure ratio=0.00)
- **Core/products/reference-substrate**: λ_apply_now=1.0 (closure=100%, sym/closure ratio=0.00)
- **Core/products/throughline**: λ_apply_now=1.0 (closure=100%, sym/closure ratio=0.00)
- **Core/products/topography**: λ_apply_now=1.0 (closure=100%, sym/closure ratio=0.00)
- **Core/products/voices**: λ_apply_now=1.0 (closure=100%, sym/closure ratio=0.00)
- **Core/products/warp**: λ_apply_now=1.0 (closure=100%, sym/closure ratio=0.00)
- **Core/products/witness**: λ_apply_now=1.0 (closure=100%, sym/closure ratio=0.00)
- **Core**: λ_apply_now=1.0 (closure=100%, sym/closure ratio=0.00)
- **Home**: λ_apply_now=1.0 (closure=100%, sym/closure ratio=0.00)

## Application path

1. Read `lambda-settings-by-product-v1.yaml` — contains paste-ready snippets per product.
2. For each product NOT in REQUIRED-BEFORE-λ-RAISE: paste the `lambda_settings:` block into that product's `.intent/INTENT.md`.
3. For products in REQUIRED-BEFORE-λ-RAISE: paste the block as-is (default stays at baseline 1.0), AND open a signal capturing the lift-investment work needed for that product.
4. After 30 days of post-fit data, re-run `extract_calibration_corpus.py` + `lambda_fit.py` to refit.
5. Layer per-actor topology adjustments per flight-model spec §16 §Defaults by actor topology (theparlor-solo +0.5-1.0; cross-human-comms locked at 0.0).

## Open dependencies

- Cast schema amendment (formalize risk_appetite / decision_stance / panel_role fields)
- PreToolUse `signal-recorder-silent` hook (mechanism for WS-DDR-098 enforcement)
- `panel-critique-v2-balanced` Forge operator (Cast bravery-prior personas need rendering)
- Schema v2 forward-instrumented signal data (will replace heuristic input derivation in next refit)

## Limitations of v1 (re-fit when these resolve)

- **Overspeed proxy is weak**: heuristic puts all closure-compliant signals at L≥W (airworthy). True overspeed indicators require explicit `autonomy_level` and `lambda_used` fields per signal-stream v2 schema.
- **λ baseline is 1.0 globally**: per-actor topology adjustments (per flight-model spec §16) layer on top — not yet automated.
- **α and β are heuristic** (0.5 and 0.3). They can be re-tuned when forward-instrumented data accumulates and a held-out test set is available.