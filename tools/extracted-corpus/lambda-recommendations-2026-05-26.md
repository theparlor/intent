# Initial λ Recommendations (v0 heuristic)

Generated 2026-05-26 from 229 closure-compliant + 61 symptom-repaired signals.

## Method

Per-product closure rate = `resolved / (resolved + symptom_repaired + open)`.

- `closure_rate < 30%` → **RAISE** λ × 1.3-1.5
- `30% ≤ rate < 60%` → **HOLD**
- `closure_rate ≥ 60%` → **CONFIRM-AND-PROBE** λ × 1.1-1.2

These are v0 starting points, not fits. Schema-v2 forward-instrumented data + `lambda_fit.py` will replace these once available.

## Per-product recommendations

| Product | Resolved | Sym-rep | Open | Closure rate | Recommendation | Rationale |
|---|---:|---:|---:|---:|---|---|
| Core/products/cast | 83 | 13 | 54 | 55% | **HOLD** | λ unchanged — operating in envelope |
| ROOT (Workspaces-wide) | 24 | 2 | 48 | 32% | **HOLD** | λ unchanged — operating in envelope |
| Work | 6 | 10 | 25 | 15% | **RAISE** | λ × 1.3-1.5 — drift accumulating; thrust needed to drive closure |
| Core/products/org-design-tooling | 9 | 9 | 31 | 18% | **RAISE** | λ × 1.3-1.5 — drift accumulating; thrust needed to drive closure |
| Core/products/library-index | 3 | 3 | 10 | 19% | **RAISE** | λ × 1.3-1.5 — drift accumulating; thrust needed to drive closure |
| Core/frameworks/coherence-engineering | 8 | 5 | 13 | 31% | **HOLD** | λ unchanged — operating in envelope |
| Core/products/forge | 18 | 1 | 6 | 72% | **CONFIRM-AND-PROBE** | λ × 1.1-1.2 — closing well; push higher via shadow autonomy |
| Core/frameworks/intent | 9 | 1 | 4 | 64% | **CONFIRM-AND-PROBE** | λ × 1.1-1.2 — closing well; push higher via shadow autonomy |
| Core/products/voices | 6 | 0 | 0 | 100% | **CONFIRM-AND-PROBE** | λ × 1.1-1.2 — closing well; push higher via shadow autonomy |
| Core/products/fieldbook | 5 | 2 | 3 | 50% | **HOLD** | λ unchanged — operating in envelope |
| Core/products/conduit | 8 | 2 | 1 | 73% | **CONFIRM-AND-PROBE** | λ × 1.1-1.2 — closing well; push higher via shadow autonomy |
| Core/products/studio-control | 3 | 1 | 3 | 43% | **HOLD** | λ unchanged — operating in envelope |
| Core/products/library-index-mcp | 4 | 7 | 0 | 36% | **HOLD** | λ unchanged — operating in envelope |
| Core/products/pulse | 3 | 0 | 1 | 75% | **CONFIRM-AND-PROBE** | λ × 1.1-1.2 — closing well; push higher via shadow autonomy |
| Core/products/loom | 4 | 0 | 1 | 80% | **CONFIRM-AND-PROBE** | λ × 1.1-1.2 — closing well; push higher via shadow autonomy |
| Core/products/parallax | 3 | 0 | 2 | 60% | **CONFIRM-AND-PROBE** | λ × 1.1-1.2 — closing well; push higher via shadow autonomy |
| Core/products/digital-declutter | 4 | 1 | 3 | 50% | **HOLD** | λ unchanged — operating in envelope |
| Core/products/warp | 5 | 0 | 1 | 83% | **CONFIRM-AND-PROBE** | λ × 1.1-1.2 — closing well; push higher via shadow autonomy |
| Core/products/witness | 3 | 0 | 2 | 60% | **CONFIRM-AND-PROBE** | λ × 1.1-1.2 — closing well; push higher via shadow autonomy |
| Core/products/cortege | 4 | 0 | 2 | 67% | **CONFIRM-AND-PROBE** | λ × 1.1-1.2 — closing well; push higher via shadow autonomy |
| Core/products/throughline | 2 | 0 | 1 | 67% | **CONFIRM-AND-PROBE** | λ × 1.1-1.2 — closing well; push higher via shadow autonomy |
| Core/products/reference-substrate | 3 | 0 | 1 | 75% | **CONFIRM-AND-PROBE** | λ × 1.1-1.2 — closing well; push higher via shadow autonomy |
| Core/products/topography | 4 | 0 | 0 | 100% | **CONFIRM-AND-PROBE** | λ × 1.1-1.2 — closing well; push higher via shadow autonomy |
| Core/frameworks/methodology-library | 0 | 2 | 0 | 0% | **RAISE** | λ × 1.3-1.5 — drift accumulating; thrust needed to drive closure |
| Core/frameworks/investment | 1 | 1 | 0 | 50% | **HOLD** | λ unchanged — operating in envelope |
| Core/frameworks/measurement | 1 | 0 | 0 | 100% | **CONFIRM-AND-PROBE** | λ × 1.1-1.2 — closing well; push higher via shadow autonomy |
| Core/frameworks/intent-site | 0 | 0 | 1 | 0% | **RAISE** | λ × 1.3-1.5 — drift accumulating; thrust needed to drive closure |
| Core/frameworks/transformation | 1 | 0 | 0 | 100% | **CONFIRM-AND-PROBE** | λ × 1.1-1.2 — closing well; push higher via shadow autonomy |
| Core/frameworks/governance | 1 | 0 | 0 | 100% | **CONFIRM-AND-PROBE** | λ × 1.1-1.2 — closing well; push higher via shadow autonomy |
| Core/frameworks/design-systems | 1 | 0 | 0 | 100% | **CONFIRM-AND-PROBE** | λ × 1.1-1.2 — closing well; push higher via shadow autonomy |
| Core/frameworks/protocols | 0 | 1 | 0 | 0% | **RAISE** | λ × 1.3-1.5 — drift accumulating; thrust needed to drive closure |
| Core/frameworks/knowledge-engine | 2 | 0 | 0 | 100% | **CONFIRM-AND-PROBE** | λ × 1.1-1.2 — closing well; push higher via shadow autonomy |
| Core/frameworks/product-academy | 0 | 0 | 1 | 0% | **RAISE** | λ × 1.3-1.5 — drift accumulating; thrust needed to drive closure |
| Core/frameworks/assessment | 1 | 0 | 0 | 100% | **CONFIRM-AND-PROBE** | λ × 1.1-1.2 — closing well; push higher via shadow autonomy |

## Aggregate λ-bias signal

Products with closure_rate < 30% are the strongest stall indicators per SPEC-INTENT-AUTONOMY-FLIGHT-MODEL-001 §3. 
Small-N products with closure_rate ≥ 60% (Witness, Cortège, Warp, Reference-substrate) reflect single-owner attention at low signal volume — useful as upper-envelope confirmation, not lower-envelope evidence.

## Application

1. Each product's `.intent/INTENT.md` adds `lambda_settings.default:` set to (current_baseline × multiplier).
2. Until per-product baselines are established, treat the default at 1.0 and multiply per the table.
3. Per-surface overrides remain governed by the autonomy-gate-surface-matrix (`Core/frameworks/intent/spec/autonomy-gate-surface-matrix-v0-DRAFT.md`).

## Outcome-label distribution (gold)

- `airworthy-and-resolved`: 229

## Outcome-label distribution (symptom-repaired)

- `symptom-repaired-gate-too-tight`: 61

## Next step

Fit per-product λ from these counts. The fit script is the next tool to author (`lambda_fit.py`); ratification dependency for promoting SPEC-INTENT-AUTONOMY-FLIGHT-MODEL-001 from draft to accepted.