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
| .claude | 396 | 0% | 0% | 1.5 | **1.5** | ✓ NONE |
| Core/products/cast | 208 | 40% | 6% | 1.3 | **1.3** | ✓ NONE |
| ROOT (Workspaces-wide) | 74 | 32% | 3% | 1.338 | **1.338** | ✓ NONE |
| Core/products/org-design-tooling | 51 | 18% | 18% | 1.412 | **1.0** | 🛑 REQUIRED-BEFORE-λ-RAISE |
| Work/Consulting | 29 | 0% | 0% | 1.5 | **1.5** | ✓ NONE |
| Core/products/forge | 27 | 67% | 4% | 1.167 | **1.167** | ✓ NONE |
| Core/frameworks/coherence-engineering | 27 | 30% | 18% | 1.352 | **1.176** | ⚠ RECOMMENDED |
| Core/products/library-index | 16 | 19% | 19% | 1.406 | **1.0** | 🛑 REQUIRED-BEFORE-λ-RAISE |
| Work | 16 | 38% | 62% | 1.312 | **1.0** | 🛑 REQUIRED-BEFORE-λ-RAISE |
| Core/frameworks/intent | 14 | 64% | 7% | 1.179 | **1.179** | ✓ NONE |
| Core/products/conduit | 11 | 73% | 18% | 1.136 | **1.136** | · OPTIONAL |
| Core/products/library-index-mcp | 11 | 36% | 64% | 1.318 | **1.0** | 🛑 REQUIRED-BEFORE-λ-RAISE |
| Core/products/voices | 10 | 60% | 0% | 1.2 | **1.2** | ✓ NONE |
| Core/products/fieldbook | 10 | 50% | 20% | 1.25 | **1.25** | · OPTIONAL |
| Core/products/digital-declutter | 8 | 50% | 12% | 1.25 | **1.25** | · OPTIONAL |
| Core/products/studio-control | 8 | 38% | 12% | 1.312 | **1.312** | · OPTIONAL |
| Core/products/cortege | 7 | 57% | 0% | 1.214 | **1.214** | ✓ NONE |
| Core/products/warp | 7 | 71% | 0% | 1.143 | **1.143** | ✓ NONE |
| Core/products/parallax | 6 | 50% | 0% | 1.25 | **1.25** | ✓ NONE |
| Core/products/witness | 5 | 60% | 0% | 1.2 | **1.2** | ✓ NONE |
| Core/products/throughline | 5 | 40% | 0% | 1.3 | **1.3** | ✓ NONE |
| Core/products/loom | 5 | 80% | 0% | 1.1 | **1.1** | ✓ NONE |
| Core/products/pulse | 4 | 75% | 0% | 1.125 | **1.125** | ✓ NONE |
| Core/products/reference-substrate | 4 | 75% | 0% | 1.125 | **1.125** | ✓ NONE |
| Core/products/topography | 4 | 100% | 0% | 1.0 | **1.0** | ✓ NONE |
| Work/Advising | 3 | 0% | 0% | 1.5 | **1.5** | ✓ NONE |
| Core/frameworks/investment | 2 | 50% | 50% | 1.25 | **1.0** | 🛑 REQUIRED-BEFORE-λ-RAISE |
| Core/frameworks/transformation | 2 | 50% | 0% | 1.25 | **1.25** | ✓ NONE |
| Core/frameworks/design-systems | 2 | 50% | 0% | 1.25 | **1.25** | ✓ NONE |
| Core/frameworks/knowledge-engine | 2 | 100% | 0% | 1.0 | **1.0** | ✓ NONE |
| Core/frameworks/methodology-library | 2 | 0% | 100% | 1.5 | **1.0** | 🛑 REQUIRED-BEFORE-λ-RAISE |
| Core/frameworks/measurement | 1 | 100% | 0% | 1.0 | **1.0** | ✓ NONE |
| Core/frameworks/assessment | 1 | 100% | 0% | 1.0 | **1.0** | ✓ NONE |
| Core/frameworks/governance | 1 | 100% | 0% | 1.0 | **1.0** | ✓ NONE |
| Core/frameworks/protocols | 1 | 0% | 100% | 1.5 | **1.0** | 🛑 REQUIRED-BEFORE-λ-RAISE |
| Core/frameworks/intent-site | 1 | 0% | 0% | 1.5 | **1.5** | ✓ NONE |
| Core/frameworks/product-academy | 1 | 0% | 0% | 1.5 | **1.5** | ✓ NONE |

## Lift-action distribution

- **REQUIRED-BEFORE-λ-RAISE**: 7
- **RECOMMENDED**: 1
- **OPTIONAL**: 4
- **NONE**: 25

## Products needing lift investment FIRST (do not raise λ yet)

- **Core/frameworks/methodology-library**: containment_gap=10.00, closure=0%, sym=100%. λ stays at baseline 1.0 until lift work lands (target: 1.5).
- **Core/frameworks/protocols**: containment_gap=10.00, closure=0%, sym=100%. λ stays at baseline 1.0 until lift work lands (target: 1.5).
- **Core/products/library-index-mcp**: containment_gap=1.75, closure=36%, sym=64%. λ stays at baseline 1.0 until lift work lands (target: 1.318).
- **Work**: containment_gap=1.67, closure=38%, sym=62%. λ stays at baseline 1.0 until lift work lands (target: 1.312).
- **Core/products/org-design-tooling**: containment_gap=1.00, closure=18%, sym=18%. λ stays at baseline 1.0 until lift work lands (target: 1.412).
- **Core/products/library-index**: containment_gap=1.00, closure=19%, sym=19%. λ stays at baseline 1.0 until lift work lands (target: 1.406).
- **Core/frameworks/investment**: containment_gap=1.00, closure=50%, sym=50%. λ stays at baseline 1.0 until lift work lands (target: 1.25).

## Products ready to apply fit λ directly

- **Core/frameworks/intent-site**: λ_apply_now=1.5 (closure=0%, sym/closure ratio=0.00)
- **Core/frameworks/product-academy**: λ_apply_now=1.5 (closure=0%, sym/closure ratio=0.00)
- **.claude**: λ_apply_now=1.5 (closure=0%, sym/closure ratio=0.00)
- **Work/Advising**: λ_apply_now=1.5 (closure=0%, sym/closure ratio=0.00)
- **Work/Consulting**: λ_apply_now=1.5 (closure=0%, sym/closure ratio=0.00)
- **ROOT (Workspaces-wide)**: λ_apply_now=1.338 (closure=32%, sym/closure ratio=0.08)
- **Core/products/studio-control**: λ_apply_now=1.312 (closure=38%, sym/closure ratio=0.33)
- **Core/products/throughline**: λ_apply_now=1.3 (closure=40%, sym/closure ratio=0.00)
- **Core/products/cast**: λ_apply_now=1.3 (closure=40%, sym/closure ratio=0.16)
- **Core/products/digital-declutter**: λ_apply_now=1.25 (closure=50%, sym/closure ratio=0.25)
- **Core/products/parallax**: λ_apply_now=1.25 (closure=50%, sym/closure ratio=0.00)
- **Core/products/fieldbook**: λ_apply_now=1.25 (closure=50%, sym/closure ratio=0.40)
- **Core/frameworks/transformation**: λ_apply_now=1.25 (closure=50%, sym/closure ratio=0.00)
- **Core/frameworks/design-systems**: λ_apply_now=1.25 (closure=50%, sym/closure ratio=0.00)
- **Core/products/cortege**: λ_apply_now=1.214 (closure=57%, sym/closure ratio=0.00)
- **Core/products/witness**: λ_apply_now=1.2 (closure=60%, sym/closure ratio=0.00)
- **Core/products/voices**: λ_apply_now=1.2 (closure=60%, sym/closure ratio=0.00)
- **Core/frameworks/intent**: λ_apply_now=1.179 (closure=64%, sym/closure ratio=0.11)
- **Core/products/forge**: λ_apply_now=1.167 (closure=67%, sym/closure ratio=0.06)
- **Core/products/warp**: λ_apply_now=1.143 (closure=71%, sym/closure ratio=0.00)
- **Core/products/conduit**: λ_apply_now=1.136 (closure=73%, sym/closure ratio=0.25)
- **Core/products/pulse**: λ_apply_now=1.125 (closure=75%, sym/closure ratio=0.00)
- **Core/products/reference-substrate**: λ_apply_now=1.125 (closure=75%, sym/closure ratio=0.00)
- **Core/products/loom**: λ_apply_now=1.1 (closure=80%, sym/closure ratio=0.00)
- **Core/products/topography**: λ_apply_now=1.0 (closure=100%, sym/closure ratio=0.00)
- **Core/frameworks/measurement**: λ_apply_now=1.0 (closure=100%, sym/closure ratio=0.00)
- **Core/frameworks/assessment**: λ_apply_now=1.0 (closure=100%, sym/closure ratio=0.00)
- **Core/frameworks/governance**: λ_apply_now=1.0 (closure=100%, sym/closure ratio=0.00)
- **Core/frameworks/knowledge-engine**: λ_apply_now=1.0 (closure=100%, sym/closure ratio=0.00)

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