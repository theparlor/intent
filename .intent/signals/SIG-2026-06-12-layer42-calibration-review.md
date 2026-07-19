---
id: SIG-2026-06-12-layer42-calibration-review
created: 2026-06-12
type: road-readiness-calibration
status: captured
severity: medium
confidence: 0.9
trust: 0.8
review_class: warn-only-calibration-result
road_ready_gate: true
parent_signal: SIG-2026-05-29-friction-01-stop-hook-lexical-arms-race
decision_owner: Brien (L2 — promote/retire/ratify are NOT autonomous)
related:
  - Core/frameworks/intent/hooks/lexical-layer-freeze.yaml
  - Core/frameworks/intent/hooks/autonomy-posture-check-layer-4.2.sh
  - Core/frameworks/intent/hooks/autonomy-grant-stop-check.sh
  - Core/frameworks/intent/spec/autonomy-flight-model-ratification-tracker.md
  - SIG-2026-05-30-roadready-execution-closure
---

# Layer 4.2 — 14-day warn-only calibration result (GATHER-AND-SURFACE)

Scheduled review per `layer-42-calibration-review-2026-06-12`. One-time gather.
**Nothing here was promoted, retired, ratified, or written into the freeze** —
those are Brien's L2 decisions. This is the evidence + a recommendation.

## The sunset trigger
`lexical-layer-freeze.yaml:sunset.trigger` — "Layer 4.2 completes its 14-day
warn-only calibration with measured false-positive rate < 5%." → retire CHECKs 1-6
or demote to dated fallback; a CHECK with ~0 blocks over the window is retired outright.

## The window (clean — exactly 14 days)
- Source: `~/.claude/logs/autonomy-posture-layer42.jsonl`
- Span: 2026-05-29T21:41Z → 2026-06-12T12:59Z
- **Total warn-only runs: 749**
- **`would_block`=1 fires: 3**
- **would-block rate: 0.40%**

## False-positive assessment — all 3 fires are FP, one shared failure mode
`would_block` = (unmatched next-action claim) AND (4-gates pass). The target
extractor grabbed **stop-words/pronouns**, not real deferred-action verbs:

| ts | extracted target | actual tail (truncated) | verdict |
|----|------------------|-------------------------|---------|
| 2026-06-01 | `each` | "I'll commit **each** verify-gated as it lands, then run Wave-R3" — forward plan, legitimately not yet executed | FP (quantifier mis-parse) |
| 2026-06-05 | `that` | "...otherwise **that's** the panel I'd convene" — recommendation-first w/ reveal, compliant | FP (pronoun mis-parse) |
| 2026-06-09 | `that` | "I'll run it; if you'd rather...first, I'll do **that** instead" — recommendation-first w/ reveal, compliant | FP (pronoun mis-parse) |

**Zero true autonomy-drift catches in 14 days.** A stop-word filter on the
target extractor (`each/that/it/this/them/...`) would have suppressed all three →
true would-block rate ≈ 0%.

## Two FP framings (both surfaced honestly)
- **Against run volume (the friction tax):** 3 / 749 = **0.40% < 5% → trigger PASSES.**
- **Against fires (precision):** 3 / 3 = **100% of fires are FP.** The gate has not
  yet fired correctly even once. Promoting to block *today* ships a gate whose only
  observed live behavior is noise.

## CHECK retire/demote evidence (autonomy-grant lexical layer, block-by-check)
From `drag_dashboard.py` (77 total blocks): CHECK5=45 · CHECK4=11 · CHECK7=8 ·
CHECK1=7 · CHECK6=4 · CHECK2=2 · **CHECK3=0 (absent)**.
- **Retire outright:** CHECK3 (0 blocks). Near-zero: CHECK2 (2).
- **High-yield, demote last:** CHECK5 (45 — the only one carrying real weight).
- **Middle, demote to dated fallback:** CHECK1/4/6/7.

## Recommendation (Brien's L2 call — not executed)
The numeric trigger is met (0.40% < 5%), BUT do **not** promote-to-block as a clean
single step, because the precision signal says the fire condition currently catches
only noise. Sequence instead:
1. **Patch first:** add the stop-word/pronoun filter to the Layer 4.2 target
   extractor (one-line; suppresses all 3 known FPs). Re-confirm ≈0% would-block.
2. **Then promote** Layer 4.2 warn-only → block.
3. **Retire** CHECK3 outright + CHECK2; **demote** CHECK1/4/6/7 to a dated fallback;
   keep/last-demote CHECK5.
4. Update `lexical-layer-freeze.yaml:sunset` with the executed schedule and close
   `SIG-2026-05-29-friction-01`.

Steps 1-4 are L2 (touch the gate model + freeze). Surfaced for decision; not taken.
