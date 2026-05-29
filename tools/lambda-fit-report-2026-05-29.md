---
title: Lambda Fit Report — 2026-05-29 (REAL FIT)
type: report
status: final
date: 2026-05-29
supersedes: lambda-fit-v1-report.md (provisional run with tool failure — see Tool Failure note below)
fit_source: Core/frameworks/intent/tools/lambda_fit.py
corpus: Core/frameworks/intent/tools/extracted-corpus-2026-05-29/
related:
  - Core/frameworks/intent/spec/autonomy-flight-model-v1-DRAFT.md (§8, §15, §16)
  - Core/frameworks/intent/tools/lambda_fit.py
  - Core/frameworks/intent/tools/extract_calibration_corpus.py
  - Core/frameworks/intent/tools/apply_lambda_settings.py
  - Core/frameworks/intent/tools/skip_rules.py
---
# Lambda Fit Report — 2026-05-29 (REAL FIT)

This report supersedes the earlier provisional 2026-05-29 run in which all three pipeline tools
returned zero output due to a `skip_rules.py` bug that prevented walkers from entering `.intent/`
and `.context/` directories. That bug has been fixed (KEEP_DOTDIRS exemption). This report records
the REAL fit from the corrected pipeline.

**Corpus: 441 labeled-gold + 66 symptom-repaired (vs. prior 0 / 0)**
**Products fit: 34**

---

## Fix Applied

`skip_rules.py` now has a `KEEP_DOTDIRS` exemption. The walkers correctly traverse `.intent/` and
`.context/` directories, which are the signal stores. Verified:

```
intent_signal_inventory.py /Users/brien/Workspaces → ~1551 artifacts / 460 labeled-gold
extract_calibration_corpus.py → 441 labeled-gold / 66 symptom-repaired / 39 products
```

Note: `intent_signal_inventory.py` reports ~460 labeled-gold while `extract_calibration_corpus.py`
reports 441. The difference is that the corpus extractor applies the full closure-DoD check
(requires BOTH `upstream_control_path` AND `catch_mechanism` to be concrete, not pending/tbd/none),
whereas the inventory tool uses a looser signal count. The 441 is the authoritative labeled-gold count
for the fit.

---

## Fit Model

Per `lambda_fit.py` (SPEC-INTENT-AUTONOMY-FLIGHT-MODEL-001 §8):

```
stall_loss      = 1 - closure_rate
containment_gap = sym_rep_rate / max(closure_rate, 0.1)

λ_fit           = 1.0 × (1 + 0.5 × stall_loss)     [α = 0.5, λ_baseline = 1.0]
lift_investment = 0.3 × containment_gap              [β = 0.3]

λ_apply_now     = λ_fit        if lift_investment < 0.06   (NONE / OPTIONAL)
                  midpoint      if 0.15 ≤ lift_inv < 0.30   (RECOMMENDED)
                  baseline 1.0  if lift_inv ≥ 0.30          (REQUIRED-BEFORE-λ-RAISE)

Topology adjustments (per §16) layer on top of per-product λ_apply_now. Not encoded
in these fit values — applied at runtime by the autonomy gate surface matrix.
```

Limitations of v1 (unchanged from lambda_fit.py):
- Overspeed proxy is weak: no `autonomy_level` / `lambda_used` per signal (schema v2 pending)
- α=0.5 and β=0.3 are heuristic — re-tune when forward-instrumented data accumulates
- λ_baseline is 1.0 globally; per-actor topology adjustments are NOT encoded here

---

## Per-Product Fit Table — 2026-05-29 REAL

All values computed by `lambda_fit.py` from `extracted-corpus-2026-05-29/labeled-gold-v1.jsonl`
(441 rows) and `symptom-repaired-v1.jsonl` (66 rows). No manual computation.

| Product | n | gold | sym | open | closure% | λ_fit | λ_apply_now | lift_action |
|---|---:|---:|---:|---:|---:|---:|---:|---|
| Core/products/cast | 263 | 250 | 13 | 0 | 95% | 1.025 | **1.025** | NONE |
| ROOT (Workspaces-wide) | 54 | 49 | 5 | 0 | 91% | 1.046 | **1.046** | NONE |
| Core/products/forge | 24 | 23 | 1 | 0 | 96% | 1.021 | **1.021** | NONE |
| Core/products/org-design-tooling | 18 | 9 | 9 | 0 | 50% | 1.250 | **1.000** | REQUIRED-BEFORE-λ-RAISE |
| Core/frameworks/intent | 17 | 15 | 2 | 0 | 88% | 1.059 | **1.059** | NONE |
| Work | 17 | 6 | 11 | 0 | 35% | 1.324 | **1.000** | REQUIRED-BEFORE-λ-RAISE |
| Core/frameworks/coherence-engineering | 13 | 8 | 5 | 0 | 62% | 1.192 | **1.096** | RECOMMENDED |
| Core/products/library-index-mcp | 12 | 5 | 7 | 0 | 42% | 1.292 | **1.000** | REQUIRED-BEFORE-λ-RAISE |
| Core/products/conduit | 10 | 8 | 2 | 0 | 80% | 1.100 | **1.100** | OPTIONAL |
| Core/products/fieldbook | 7 | 5 | 2 | 0 | 71% | 1.143 | **1.143** | OPTIONAL |
| Core/products/library-index | 7 | 4 | 3 | 0 | 57% | 1.214 | **1.107** | RECOMMENDED |
| Core | 5 | 5 | 0 | 0 | 100% | 1.000 | **1.000** | NONE |
| Core/products/cortege | 5 | 5 | 0 | 0 | 100% | 1.000 | **1.000** | NONE |
| Core/products/digital-declutter | 5 | 4 | 1 | 0 | 80% | 1.100 | **1.100** | OPTIONAL |
| Core/products/voices | 5 | 5 | 0 | 0 | 100% | 1.000 | **1.000** | NONE |
| Core/products/warp | 5 | 5 | 0 | 0 | 100% | 1.000 | **1.000** | NONE |
| Core/products/loom | 4 | 4 | 0 | 0 | 100% | 1.000 | **1.000** | NONE |
| Core/products/pulse | 4 | 4 | 0 | 0 | 100% | 1.000 | **1.000** | NONE |
| Core/products/studio-control | 4 | 3 | 1 | 0 | 75% | 1.125 | **1.125** | OPTIONAL |
| Core/products/topography | 4 | 4 | 0 | 0 | 100% | 1.000 | **1.000** | NONE |
| Core/products/parallax | 3 | 3 | 0 | 0 | 100% | 1.000 | **1.000** | NONE |
| Core/products/reference-substrate | 3 | 3 | 0 | 0 | 100% | 1.000 | **1.000** | NONE |
| Core/products/witness | 3 | 3 | 0 | 0 | 100% | 1.000 | **1.000** | NONE |
| Core/frameworks/investment | 2 | 1 | 1 | 0 | 50% | 1.250 | **1.000** | REQUIRED-BEFORE-λ-RAISE |
| Core/frameworks/knowledge-engine | 2 | 2 | 0 | 0 | 100% | 1.000 | **1.000** | NONE |
| Core/frameworks/methodology-library | 2 | 0 | 2 | 0 | 0% | 1.500 | **1.000** | REQUIRED-BEFORE-λ-RAISE |
| Core/products/throughline | 2 | 2 | 0 | 0 | 100% | 1.000 | **1.000** | NONE |
| Core/frameworks/assessment | 1 | 1 | 0 | 0 | 100% | 1.000 | **1.000** | NONE |
| Core/frameworks/design-systems | 1 | 1 | 0 | 0 | 100% | 1.000 | **1.000** | NONE |
| Core/frameworks/governance | 1 | 1 | 0 | 0 | 100% | 1.000 | **1.000** | NONE |
| Core/frameworks/measurement | 1 | 1 | 0 | 0 | 100% | 1.000 | **1.000** | NONE |
| Core/frameworks/protocols | 1 | 0 | 1 | 0 | 0% | 1.500 | **1.000** | REQUIRED-BEFORE-λ-RAISE |
| Core/frameworks/transformation | 1 | 1 | 0 | 0 | 100% | 1.000 | **1.000** | NONE |
| Home | 1 | 1 | 0 | 0 | 100% | 1.000 | **1.000** | NONE |

**Note on "prior, not fit":** No products fall to topology-default prior in this run — all 34 had
at least 1 signal. `Work` and `ROOT (Workspaces-wide)` are exempt buckets (per apply_lambda_settings.py
EXCLUDE_PREFIXES); their fit values are recorded here for reference but are not applied to INTENT.md files.

---

## Lift-Action Distribution

| Lift action | Count |
|---|---:|
| NONE — apply λ_fit directly | 22 |
| OPTIONAL — apply λ_fit, monitor sym-rep | 4 |
| RECOMMENDED — invest in L, then raise | 2 |
| REQUIRED-BEFORE-λ-RAISE — build L first | 6 |

### Products requiring lift investment BEFORE raising λ

- **Core/products/org-design-tooling** (n=18): containment_gap=1.0, closure=50%, sym=50%.
  Build catch_mechanism + upstream_control_path coverage before raising above baseline 1.0.
  λ_fit target: 1.250 — unlock after lift investment.
- **Work** (n=17): containment_gap=1.833, closure=35%, sym=65%. Engagement-scoped bucket; exempt
  from INTENT.md application but signals the engagement-closure workflow needs attention.
- **Core/products/library-index-mcp** (n=12): containment_gap=1.400, closure=42%, sym=58%.
  High sym-rep rate — structural lift gap on this product.
- **Core/frameworks/investment** (n=2): containment_gap=1.0, closure=50%, sym=50%. Small n — treat
  with caution; one more resolved signal would shift it to RECOMMENDED.
- **Core/frameworks/methodology-library** (n=2): containment_gap=∞ (0 resolved), closure=0%, sym=100%.
  Zero resolved signals — all activity is symptom-repaired. Strong indicator of lift gap.
- **Core/frameworks/protocols** (n=1): containment_gap=∞ (0 resolved), closure=0%. Single sym-rep
  signal only. Small-n; flag for monitoring.

---

## Prior-Run Comparison

| Metric | Prior (tool-failed 2026-05-29) | This run (REAL 2026-05-29) |
|---|---:|---:|
| Labeled-gold | 0 (tool returned 0) | 441 |
| Symptom-repaired | 0 (tool returned 0) | 66 |
| Products fit | 0 | 34 |
| λ values applied | 28 (manual-compute, labeled tool-failed) | 25 updated + 1 added (tool-computed) |
| Source label | manual-compute (tool-failed) | lambda_fit.py (REAL) |

The provisional run's manually-computed λ values were clearly labeled as "manual-compute (tool-failed)"
and are now superseded. The sentinel-bounded blocks in each product's INTENT.md have been updated
in-place by `apply_lambda_settings.py`. The `last_fit: 2026-05-26` timestamp in the managed blocks
reflects the lambda_fit.py hardcoded date (its output template); the actual run date is 2026-05-29.

---

## Snapshot Integrity

The 2026-05-26 dated files in `extracted-corpus/` (the original output dir) are intact:

```
extracted-corpus/labeled-gold-v1.jsonl     — 229 rows (VERIFIED)
extracted-corpus/symptom-repaired-v1.jsonl — 61 rows  (VERIFIED)
```

The fresh corpus is in `extracted-corpus-2026-05-29/` (separate directory, no overwrites):

```
extracted-corpus-2026-05-29/labeled-gold-v1.jsonl     — 441 rows
extracted-corpus-2026-05-29/symptom-repaired-v1.jsonl — 66 rows
extracted-corpus-2026-05-29/lambda-fit-v1.json        — 34 products
extracted-corpus-2026-05-29/lambda-settings-by-product-v1.yaml
extracted-corpus-2026-05-29/lambda-fit-v1-report.md
```

---

## Files Modified by apply_lambda_settings.py

### Updated (existing managed block replaced — 25 products):
- `/Users/brien/Workspaces/Core/frameworks/coherence-engineering/INTENT.md`
- `/Users/brien/Workspaces/Core/frameworks/design-systems/INTENT.md`
- `/Users/brien/Workspaces/Core/frameworks/intent/.intent/INTENT.md`
- `/Users/brien/Workspaces/Core/frameworks/investment/.intent/INTENT.md`
- `/Users/brien/Workspaces/Core/frameworks/measurement/.intent/INTENT.md`
- `/Users/brien/Workspaces/Core/frameworks/methodology-library/.intent/INTENT.md`
- `/Users/brien/Workspaces/Core/frameworks/transformation/.intent/INTENT.md`
- `/Users/brien/Workspaces/Core/products/cast/.intent/INTENT.md`
- `/Users/brien/Workspaces/Core/products/conduit/.intent/INTENT.md`
- `/Users/brien/Workspaces/Core/products/cortege/.intent/INTENT.md`
- `/Users/brien/Workspaces/Core/products/digital-declutter/.intent/INTENT.md`
- `/Users/brien/Workspaces/Core/products/fieldbook/.intent/INTENT.md`
- `/Users/brien/Workspaces/Core/products/forge/.intent/INTENT.md`
- `/Users/brien/Workspaces/Core/products/library-index/.intent/INTENT.md`
- `/Users/brien/Workspaces/Core/products/library-index-mcp/.intent/INTENT.md`
- `/Users/brien/Workspaces/Core/products/loom/INTENT.md`
- `/Users/brien/Workspaces/Core/products/org-design-tooling/.intent/INTENT.md`
- `/Users/brien/Workspaces/Core/products/parallax/.intent/INTENT.md`
- `/Users/brien/Workspaces/Core/products/pulse/INTENT.md`
- `/Users/brien/Workspaces/Core/products/reference-substrate/.intent/INTENT.md`
- `/Users/brien/Workspaces/Core/products/studio-control/.intent/INTENT.md`
- `/Users/brien/Workspaces/Core/products/throughline/INTENT.md`
- `/Users/brien/Workspaces/Core/products/voices/INTENT.md`
- `/Users/brien/Workspaces/Core/products/warp/INTENT.md`
- `/Users/brien/Workspaces/Core/products/witness/.intent/INTENT.md`

### Added (new managed block — 1 product):
- `/Users/brien/Workspaces/Core/frameworks/knowledge-engine/INTENT.md`

### No-change (already idempotent — 4 products):
- `Core/frameworks/assessment`, `Core/frameworks/governance`,
  `Core/frameworks/protocols`, `Core/products/topography`

### Skipped (exempt buckets — 2):
- `ROOT (Workspaces-wide)` — exempt per EXCLUDE_PREFIXES
- `Work` — exempt per EXCLUDE_PREFIXES

### No INTENT.md found (2 buckets, not products):
- `Core` (root bucket, not a product)
- `Home` (root bucket, not a product)

---

## Tool Errors (verbatim)

No tool errors. All three tools ran cleanly:

```
extract_calibration_corpus.py:
  Extracting from /Users/brien/Workspaces...
  Wrote 441 labeled-gold rows -> .../extracted-corpus-2026-05-29/labeled-gold-v1.jsonl
  Wrote 66 symptom-repaired rows -> .../extracted-corpus-2026-05-29/symptom-repaired-v1.jsonl
  Processed 39 products. 441 labeled-gold + 66 symptom-repaired.

lambda_fit.py:
  Loaded 441 labeled-gold + 66 symptom-repaired rows.
  Fit complete: 34 products.
    REQUIRED-BEFORE-λ-RAISE: 6
    RECOMMENDED: 2
    OPTIONAL: 4
    NONE: 22

apply_lambda_settings.py (real apply):
  Loaded 34 product snippets.
  Added new block: 1
  Updated existing block: 25
  No change (idempotent): 4
  Skipped (exempt): 2
  No INTENT.md found: 2
```

One stderr warning from lambda_fit.py (expected, not an error):
```
  (no inventory.json found — open counts default to 0)
```
This means all `n_open` values are 0 in the fit table above. The extractor doesn't carry open-signal
counts into its JSONL output; they would come from a separate `inventory.json` in the workspace root.
The fit is still valid — open counts affect the denominator for closure_rate; with n_open=0, the
closure rate is derived from gold/(gold+sym) which is the correct closure-compliant fraction.

---

## Ratification Status for D1

Per SPEC-INTENT-AUTONOMY-FLIGHT-MODEL-001 §11.1:

- Signal inventory: COMPLETE (skip_rules bug fixed; 1551 artifacts / 460 labeled-gold per inventory tool)
- Corpus extraction: COMPLETE (441 labeled-gold, 66 symptom-repaired)
- λ fit: COMPLETE (34 products, tool-computed)
- λ persistence: COMPLETE (25 updated + 1 added in product INTENT.md files)
- Snapshot integrity: CONFIRMED (2026-05-26 dated v1 files intact at 229/61 rows)

**D1 status: COMPLETE.** This report is the ratification artifact for the calibration-corpus
inventory dependency of SPEC-INTENT-AUTONOMY-FLIGHT-MODEL-001.
