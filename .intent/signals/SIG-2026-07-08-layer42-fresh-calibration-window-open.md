---
id: SIG-2026-07-08-layer42-fresh-calibration-window-open
created: 2026-07-08
type: road-readiness-calibration-window-open
status: active
severity: medium
confidence: 0.9
trust: 0.8
review_class: warn-only-calibration-window-open
road_ready_gate: true
decision_owner: Brien (L2, promote/retire/ratify at window close)
parent_signal: SIG-2026-07-03-layer42-recall-unmeasured
related:
  - Core/frameworks/intent/hooks/autonomy-posture-check-layer-4.2.sh
  - Core/frameworks/intent/hooks/lexical-layer-freeze.yaml
  - Core/frameworks/intent/spec/autonomy-flight-model-ratification-tracker.md
  - Core/frameworks/intent/spec/2026-07-03-autonomy-grant-pause-drift-audit.md
  - .intent/signals/SIG-2026-06-12-layer42-calibration-review.md
  - .intent/signals/SIG-2026-06-28-flight-model-30day-ratification-readiness.md
  - .intent/signals/SIG-2026-07-03-layer42-recall-unmeasured.md
  - Workspaces/.context/PENDING_DECISIONS.md (row 3)
---

# Layer 4.2 fresh warn-only calibration window is now open (WINDOW OPEN, not a review result)

This is a bookkeeping signal, not a measurement. It opens the one remaining prerequisite the
promote/retire decision has been waiting on since 2026-07-03: a calibration window that runs
against the widened recall grammar, not the near-silent original extractor. **Nothing is
promoted, retired, or flipped to block mode here.** That remains Brien's L2 call at window close.

## Why a fresh window, not a continuation of prior data

The two prior calibration reads (14-day, 2026-06-12; 30-day, 2026-06-28) both measured a
detector later found to have 1.7 percent would-block-eligible recall against the 231-entry
lexical ground truth (`SIG-2026-07-03-layer42-recall-unmeasured.md`). A clean-looking FP rate
against a near-silent detector is not evidence of readiness, it is an artifact of the detector
almost never firing. The grammar was widened the same day (commit `9c0e6bf`,
`hooks/autonomy-posture-check-layer-4.2.sh` sections 2.2b to 2.2d) to 77.1 percent recall,
adversarially verified and trimmed. Telemetry since that commit landed reflects the new grammar,
but the formal calibration window (the one the promote decision will cite) starts now, with a
clean boundary, so the read is unambiguous about what grammar version it covers.

## Verified before opening the window: grammar is active, mode is warn-only

- Repo file: `Core/frameworks/intent/hooks/autonomy-posture-check-layer-4.2.sh`. Last commit
  touching this file is `9c0e6bf` (the widening commit); working tree is clean on this file
  (no uncommitted drift).
- Live hook: `~/.claude/hooks/autonomy-posture-check-layer-4.2.sh` is a symlink to the repo
  file above (`diff` confirms byte-identical). Registered in `~/.claude/settings.json` under
  `hooks.Stop`, matcher `*`.
- The script's final block is an unconditional `exit 0` with the comment "WARN-ONLY: always
  pass. Never emit a block decision." No block-mode env toggle exists yet, so there is no risk
  of an accidental flip during this window.
- Live telemetry confirms the mode field: the most recent line in
  `~/.claude/logs/autonomy-posture-layer42.jsonl` at window-open time reads
  `"mode":"warn-only"`, timestamped `2026-07-08T04:46:05Z`, minutes before this window opened.

**Conclusion: the widened grammar is active and the hook is warn-only. No activation step was
needed** (both were already true); this signal documents the evidence and starts the clock.

## Window parameters

- **Start:** `2026-07-08T04:53:12Z`
- **End:** `2026-07-18T04:53:12Z` (10 days)
- **Window length rationale:** the 2026-06-12 review used a 14-day window, but the 2026-07-03
  audit (`spec/2026-07-03-autonomy-grant-pause-drift-audit.md`, Phase 2, steps 5-6) explicitly
  superseded that default for this specific re-run: "do not compress this to 3-5 days... use
  whatever window (likely 7-10 days) is needed to see the fire rate on a corrected extractor,
  and manually eyeball every fire," with a stated floor of "minimum 7 days of live traffic."
  10 days is the upper bound of that explicit recommendation, chosen because this is the first
  window run against the widened grammar and a longer read reduces the chance of a vacuous
  clean result from low session volume in any single week.
- **Grammar version under test:** commit `9c0e6bf` (`feat(l42): deferred-claim grammar widens
  recall 1.7% to 77.1%, adversarially trimmed`), unchanged since 2026-07-03.
- **Mode:** warn-only, unchanged. No block-mode toggle exists.

## Where warn events accrue

- **Telemetry (every Stop event, baseline and fires):**
  `~/.claude/logs/autonomy-posture-layer42.jsonl` (one JSON line per Stop, fields include
  `ts`, `would_block`, `next_actions`, `gates_pass`, `has_tool_use`, `mode`, `tail`).
  Baseline line count at window open: 1,920 lines (pre-window history; the window's rows are
  everything with `ts >= 2026-07-08T04:53:12Z`).
- **Fires only (human-readable):**
  `~/.claude/audit/autonomy-posture-layer42-detections.log` (one line per `would_block=1`
  fire, format `[ts] L42-WOULDBLOCK session=... next=... tail='...'`).
  Baseline line count at window open: 13 lines (pre-window history; the window's rows are
  everything timestamped on or after window open).

## How the false-positive rate will be computed (consistent with the 2026-06-12 and 2026-06-28 reads)

Both prior reviews reported two framings side by side. This window reports both again, plus
the manual-eyeball step the 2026-07-03 audit added as a requirement (not optional this time,
because a clean read on this detector needs a human check that fires are genuine catches, not
a repeat of the pronoun/quantifier artifact):

1. **Against run volume (the friction-tax framing):** `would_block=1` fires in the window
   divided by total warn-only Stop runs in the window (all rows with `ts` in
   `[2026-07-08T04:53:12Z, 2026-07-18T04:53:12Z)`). Sunset trigger per
   `hooks/lexical-layer-freeze.yaml`: this ratio must be under 5 percent to pass the numeric
   trigger.
2. **Against fires (the precision framing):** of the fires in that same window, the count that
   a manual read of the `tail` field confirms is a genuine deferred-action claim (not a
   compliant recommendation-with-reveal, not an anaphoric reference the closed-class filter
   missed) divided by total fires. This is the number the 06-12 and 06-28 reviews found
   equally important: a 5-percent-or-under rate against volume with 0 percent precision on
   fires is not a pass.
3. **Recall context (new, carried over from the widening work, not re-measured mechanically):**
   this window cannot directly re-measure recall against the 231-entry ground truth (that
   corpus is historical, not live traffic). What it can do is note, for the record, whether any
   fire in the window looks like a genuine catch at all, since the prior state was zero genuine
   catches in 44 days of warn-only running. A window with at least one manually-confirmed
   genuine catch is a materially different result than another all-noise window, even if both
   pass the under-5-percent volume trigger.

## Re-surface condition (explicit)

When this window closes (2026-07-18T04:53:12Z or later, whichever review actually runs), the
promote/retire/ratify decision returns to Brien with: total runs, total fires, FP rate against
volume, FP rate against fires (manually eyeballed), and any genuine catches found. This is the
fourth surfacing of this same decision (06-12, 06-28, 07-03, and the window this signal opens);
the difference this time is that the underlying detector can now actually fire on real drift,
so a clean read means something it did not mean before. Until that review is written, this
signal stays `status: active`, not `resolved` and not `captured`: it is a live window, not a
completed action.

## Verification (window is live, not just claimed)

```bash
# Grammar commit unchanged since 2026-07-03, working tree clean on the hook file
cd /Users/brien/Workspaces/Core/frameworks/intent
git log -1 --format='%H %s' -- hooks/autonomy-posture-check-layer-4.2.sh
git status --porcelain hooks/autonomy-posture-check-layer-4.2.sh
# expect: commit 9c0e6bf..., empty status output

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
# expect: 1920 and 13 respectively (this window's rows are everything appended after this count)
```

upstream_control_path: none yet, this is a measurement window, not a control; the control this
window feeds is the promote/retire decision itself (Brien, L2), executed at
`lexical-layer-freeze.yaml:sunset` when the decision lands.
catch_mechanism: none yet by design, the review-at-close is the catch mechanism and it does not
exist as an automated re-check (no scheduled task fires this review; the 2026-07-03 audit's
step 13 explicitly deferred a scheduled re-check until "Phase 2 proves the underlying metric is
trustworthy," which is exactly this window's job). Whoever opens the review at close should
follow the same read protocol this signal documents, not re-derive it.
pipeline_survival: not applicable, nothing has shipped; this is a window-open marker only.
