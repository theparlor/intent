---
id: SIG-2026-06-28-flight-model-30day-ratification-readiness
created: 2026-06-28
type: road-readiness-ratification-review
status: captured
severity: medium
confidence: 0.9
trust: 0.8
review_class: 30-day-shadow-flight-test-result
road_ready_gate: true
decision_owner: "Brien (L2, v1 to v2 ratification + spec-status edit are NOT autonomous)"
parent_signal: SIG-2026-05-30-roadready-execution-closure
related:
  - Core/frameworks/intent/spec/autonomy-flight-model-v1-DRAFT.md
  - Core/frameworks/intent/spec/autonomy-flight-model-ratification-tracker.md
  - Core/frameworks/intent/hooks/lexical-layer-freeze.yaml
  - Core/frameworks/intent/.intent/signals/SIG-2026-06-12-layer42-calibration-review.md
  - Core/frameworks/intent/tools/flight_model.py
  - Core/frameworks/intent/tools/drag_dashboard.py
  - Core/frameworks/methodology-library/meta/signal-scoring.md
---

# Autonomy Flight Model: 30-day shadow-flight-test review (GATHER-AND-SURFACE)

Scheduled review per `flight-model-30day-flighttest-review-2026-06-28`. One-time gather.
**Nothing was ratified, promoted, retired, or written into any spec.** v1->v2 ratification
and marking `signal-scoring.md` superseded are Brien's L2 decisions. This is evidence + a
recommendation.

## Headline: STILL STALL, and the stall deepened
Re-run today (2026-06-28):
- `flight_model.py --input sample-variance-estimate.yaml` -> **STALL**, band L0, binding
  constraint = **thrust**. T (= strategic_value x lambda = 0.600) does NOT clear D (Drag).
- D (Drag) = **0.971** today, vs **0.958** on 2026-05-30. **Drag rose.**

**Why Drag rose while activity "improved":** Drag = overhead fraction = (1 - block_rate).
The Stop-hook block rate fell from 4.17% (1,463 runs, May 30) to **2.90% (7,032 runs, today)**.
A lower block rate means MORE no-op hook runs accumulated -> a HIGHER overhead fraction. So
by the model's own metric the enforcement layer got marginally worse, not better.

**Did the lexical sunset reduce Drag enough to move off STALL? No, because the sunset never
executed.** `cap_guard`: live=7, baseline=7, sanctioned=0. CHECKs 1-7 are all still live.
`drag_dashboard` shows post-06-12 fires for CHECK2 (4) and CHECK3 (1), the very checks the
2026-06-12 calibration recommended retiring. The patch-then-promote-then-retire sequence
([[SIG-2026-06-12-layer42-calibration-review]] steps 1-4) was surfaced for Brien's L2 decision
and **was not pulled.** No CHECK retired -> hook overhead never dropped -> T still can't clear D.

## 30-day shadow-autonomy telemetry (flight-model §9)
Source: `~/.claude/logs/autonomy-posture-layer42.jsonl`. Window 2026-05-29T21:41Z ->
2026-06-28T12:06Z (exactly the 30-day flight-test).

| Metric | Value |
|--------|-------|
| Total warn-only runs | **1,486** |
| `would_block` fires | **8** (0.54% of runs) |
| first 14d (<=06-12) | 749 runs / 3 fires |
| back 16d (>06-12) | 737 runs / 5 fires |
| mode | warn-only (1,486/1,486) |
| **True autonomy-drift catches** | **0** |
| **Precision on fires** | **0/8 = 0%** |
| Agreement vs human-approved-allow | (1486-8)/1486 = **99.46%** |

**Agreement rate at L+1 has two honest readings, same as the 14-day result:**
- **Against run volume (friction tax):** 0.54% would-block << 5% FP threshold -> trigger PASSES.
- **Against fires (precision):** 100% of fires are false positives. The structural successor
  has not fired correctly even once in 30 days.

All 8 fires are the SAME failure mode flagged on 06-12: the target extractor grabs
quantifiers/pronouns/stop-words, not deferred-action verbs (`each`, `that`, `all`,
`team-configs`, `with`, `those.`, `that`). Every tail is a compliant recommendation-with-reveal
or a legitimate forward plan. The one-line stop-word filter recommended on 06-12 was never
applied -> the back half produced 5 more identical FPs.

## Ratification-readiness verdict (per ratification-tracker D-WIRE section)

| Dependency | State |
|-----------|-------|
| D1-D4 (the four §11 deps) | ✓ SATISFIED (2026-05-29) |
| D-WIRE built (`flight_model.py`) | ✓ DONE (2026-05-30), 16/16 tests |
| 30-day flight-test window | ✓ COMPLETE (2026-06-28), 1,486 runs logged |
| Successor demonstrated correct in live use | ✗ **NOT MET** (0/8 precision) |
| Drag cut so model clears STALL | ✗ **NOT MET** (STALL persists, Drag 0.958 -> 0.971) |

**The time-gate is met. The substantive preconditions are not.** The thing blocking a clean
v1->v2 flip is not more calendar time. It is the **staged-but-unpulled Drag cut.** The model
reads STALL precisely because the lexical layer it is meant to succeed is still fully live.
Ratifying v2 + sunsetting CHECKs 1-6 on the strength of a successor whose only observed live
behavior is noise (0% precision) would ship the stall the model is warning about.

## Recommendation (Brien's L2 call, NOT executed)
Ratify is gated on pulling the staged sunset, not on waiting. Sequence:
1. **Patch** Layer 4.2 target extractor: add the stop-word/pronoun filter (one-liner;
   suppresses all 8 known FPs). Re-confirm ~0% would-block over a short re-window.
2. **Promote** Layer 4.2 warn-only -> block (now that it fires only on real drift).
3. **Execute the sunset:** retire CHECK3 (0 blocks) + CHECK2 (near-zero) outright; demote
   CHECK1/4/6/7 to a dated fallback; keep/last-demote CHECK5 (the only high-yield check).
   Update `lexical-layer-freeze.yaml:sunset` with the executed schedule.
4. **Re-run `flight_model.py`**. Cutting Drag should move T past D, off STALL. That off-STALL
   reading is the evidence that makes v1->v2 coherent.
5. **THEN ratify** v1->v2 and mark `signal-scoring.md` superseded.

Net: the 30-day gather confirms the v1 thesis empirically (the lexical layer IS the stall, now
measured twice) but argues AGAINST ratifying today. Ratify after the Drag cut lands, with the
off-STALL reading as proof, not before.

Status: **captured**. Evidence + recommendation surfaced; the L2 ratification/sunset decision
is Brien's and was deliberately not taken.

## Triage, 2026-07-08

Disposition: still pending, register-tracking only, this is a Brien-gated L2 decision (the
signal's own text names it as such and this pass has no standing to rule on it). Confirmed
it is already represented in Workspaces/.context/PENDING_DECISIONS.md row 3, which carries a
2026-07-08 update of its own: the fresh Layer 4.2 warn-only calibration window opened today
(2026-07-08T04:53:12Z to 2026-07-18T04:53:12Z) against the widened recall grammar from commit
9c0e6bf. That window is the actual next evidence gate for this signal's own recommended
sequence (patch the target extractor, promote to block, execute the sunset, re-run
flight_model.py, then ratify). Status unchanged; fixed only a YAML frontmatter syntax error
(unquoted colon in decision_owner) that was breaking automated parsing of this file.
