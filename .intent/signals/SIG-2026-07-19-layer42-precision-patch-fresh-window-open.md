---
id: SIG-2026-07-19-layer42-precision-patch-fresh-window-open
created: 2026-07-19
type: road-readiness-calibration-window-open
status: active
severity: medium
confidence: 0.9
trust: 0.8
review_class: warn-only-calibration-window-open
road_ready_gate: true
decision_owner: Brien (L2, promote/retire/ratify at window close)
parent_signal: SIG-2026-07-08-layer42-fresh-calibration-window-open
related:
  - Core/frameworks/intent/hooks/autonomy-posture-check-layer-4.2.sh
  - Core/frameworks/intent/hooks/tests/test_layer42_precision.py
  - Core/frameworks/intent/hooks/tests/fixtures/layer42/
  - Core/frameworks/intent/hooks/lexical-layer-freeze.yaml
  - Core/frameworks/intent/spec/autonomy-flight-model-ratification-tracker.md
  - .intent/signals/SIG-2026-06-12-layer42-calibration-review.md
  - .intent/signals/SIG-2026-07-03-layer42-recall-unmeasured.md
  - .intent/signals/SIG-2026-07-08-layer42-fresh-calibration-window-open.md
  - Core/products/_intake/2026-07-19-decision-surfaces-retrofit/layer42-calibration-promote-retire.md
---

# Layer 4.2 second warn-only calibration window is now open, post-precision-patch (WINDOW OPEN, not a review result)

This is a bookkeeping signal, not a measurement, mirroring SIG-2026-07-08's own framing. It opens
the second post-widening calibration window, run against the grammar after the 2026-07-19
false-positive precision patch (five named categories plus one general recommendation-with-reveal
discriminator; see `hooks/autonomy-posture-check-layer-4.2.sh` section 2.3b and
`hooks/tests/test_layer42_precision.py`). **Nothing is promoted, retired, or flipped to block mode
here.** That remains Brien's L2 call at window close.

## Why a fresh window, not a continuation of the 07-08 to 07-18 window

The first widened-grammar window (2026-07-08 to 2026-07-18, `SIG-2026-07-08-layer42-fresh-calibration-window-open.md`)
logged 14 would-block fires across 590 Stop events. A full-population manual read (WINDOW-CLOSE
READ, `Core/products/_intake/2026-07-19-decision-surfaces-retrofit/layer42-calibration-promote-retire.md`)
classified 3 as true positive, 10 as false positive, 1 as an ambiguous swing case, and found the
false-positive mode had moved from the already-fixed stopword/pronoun mis-parse to legitimate-gate
misclassification: prod-write and external-comms L0 language, OAuth-only actions, Fable-budget and
L2-threshold language, enforcement-standing-rule-change language, and same-turn self-quotation of a
trigger phrase (plus a sixth, general recommendation-with-reveal discriminator found necessary
during fixture testing to fully clear the confirmed set). The RECOMMENDED option in that surface
was explicit: patch those categories, then re-window, not promote on the 07-08 to 07-18 numbers as
they stood. This signal is that re-window.

## What changed since the 07-08 window (verified before opening this one)

- Patch lands in the same commit as this signal (see the repo log for the exact sha; this file
  does not self-reference it to avoid a chicken-and-egg placeholder). Adds a fifth gate
  (`gate_not_legit_deferral`) to the existing four-gate estimator, computed from six content-based
  discriminators (`CAT1_L0_RE` through `CAT6_RECOMMENDATION_RE`), fully commented in the hook file.
- Fixture-verified: all 14 real in-window firings from the 07-08 to 07-18 window preserved verbatim
  as inert test data (`hooks/tests/fixtures/layer42/`), replayed against the patched hook. The 3
  confirmed true positives still fire, the 10 confirmed false positives no longer fire, and the 1
  swing case now resolves to not-would-block (documented explicitly in the test, not silently).
- Regression: `test_response_lint.py` (18/18), `test_closure_fixture_exemption.py` (11/11),
  `test_layer42_precision.py` (14/14) all green against the patched hook.
- Mode: still warn-only, unchanged. The script's final block is still an unconditional `exit 0`. No
  block-mode toggle exists.

## Window parameters

- **Start:** `2026-07-19T18:31:57Z`
- **End:** `2026-07-29T18:31:57Z` (10 days, matching the 07-08 window's length rationale: the
  2026-07-03 audit's stated floor of minimum 7 days, likely 7 to 10, applied again here since this
  window tests a new patch against live traffic, not a re-read of old data).
- **Grammar version under test:** the 2026-07-19 precision patch (five named false-positive
  categories plus the general recommendation-with-reveal discriminator), superseding commit
  `9c0e6bf` (the 2026-07-03 recall-widening commit, unchanged in substance, extended not replaced).
- **Mode:** warn-only, unchanged.

## Where warn events accrue

- **Telemetry (every Stop event, baseline and fires):** `~/.claude/logs/autonomy-posture-layer42.jsonl`.
  Baseline line count at window open: 2565 lines (pre-window history; the window's rows are
  everything with `ts >= 2026-07-19T18:31:57Z`).
- **Fires only (human-readable):** `~/.claude/audit/autonomy-posture-layer42-detections.log`.
  Baseline line count at window open: 26 lines (pre-window history; the window's rows are
  everything timestamped on or after window open).

## How the false-positive rate will be computed (consistent with prior reads)

Same three framings as the 07-08 window (volume, precision-on-fires manually eyeballed, recall
context), plus a fourth this window adds:

1. **Against run volume:** `would_block=1` fires divided by total warn-only Stop runs in
   `[2026-07-19T18:31:57Z, 2026-07-29T18:31:57Z)`. Sunset trigger per `lexical-layer-freeze.yaml`:
   under 5 percent.
2. **Against fires (precision framing):** of the fires in the window, the count a manual read
   confirms as a genuine deferred-action claim, divided by total fires.
3. **Recall context:** whether any fire in the window looks like a genuine catch at all (the
   detector must keep catching real drift, not just go quiet).
4. **Falsification check (new, per the decision surface's own recommended option):** if patching
   the five named categories plus the general discriminator does not raise the true-positive share
   of fires well above the 07-08 window's 21 to 29 percent (3 to 4 of 14), this patch's underlying
   read is wrong and the detector needs a different fix, not just another week of data.

## Re-surface condition (explicit)

When this window closes (`2026-07-29T18:31:57Z` or later, whichever review actually runs), the
promote/retire/ratify decision returns to Brien with: total runs, total fires, FP rate against
volume, FP rate against fires (manually eyeballed), any genuine catches found, and the
falsification check above. This is the sixth surfacing of this same decision lineage (06-12, 06-28,
07-03, 07-08 window, 07-19 window-close read, and the window this signal opens). Until that review
is written, this signal stays `status: active`, not `resolved` and not `captured`: it is a live
window, not a completed action.

## Verification (window is live, not just claimed)

```bash
cd /Users/brien/Workspaces/Core/frameworks/intent
git log -1 --format='%H %s' -- hooks/autonomy-posture-check-layer-4.2.sh
# expect: the 2026-07-19 precision-patch commit

# Live hook is the repo file, not a stale copy
diff ~/.claude/hooks/autonomy-posture-check-layer-4.2.sh \
     /Users/brien/Workspaces/Core/frameworks/intent/hooks/autonomy-posture-check-layer-4.2.sh
# expect: no output (identical)

# Mode is warn-only and telemetry is actively appending
tail -1 ~/.claude/logs/autonomy-posture-layer42.jsonl | python3 -c \
  "import json,sys; d=json.loads(sys.stdin.read()); print(d['ts'], d['mode'])"
# expect: a recent timestamp, "warn-only"

# Line counts at window open (for later window-delta math)
wc -l ~/.claude/logs/autonomy-posture-layer42.jsonl
wc -l ~/.claude/audit/autonomy-posture-layer42-detections.log
# expect: 2565 and 26 respectively (this window's rows are everything appended after this count)

# Precision-patch regression suite, all green
cd /Users/brien/Workspaces/Core/frameworks/intent
python3 hooks/tests/test_layer42_precision.py
python3 hooks/tests/test_response_lint.py
python3 hooks/tests/test_closure_fixture_exemption.py
# expect: 14/14, 18/18, 11/11
```

upstream_control_path: none yet, this is a measurement window, not a control; the control this
window feeds is the promote/retire decision itself (Brien, L2), executed at
`lexical-layer-freeze.yaml:sunset` when the decision lands.
catch_mechanism: none yet by design, same as the 07-08 window; the review-at-close is the catch
mechanism and it does not exist as an automated re-check. Whoever opens the review at close should
follow the same read protocol this signal documents (and the one it supersedes), not re-derive it.
pipeline_survival: not applicable, nothing has shipped beyond the warn-only detector patch itself;
this is a window-open marker only.
