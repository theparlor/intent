---
id: SIG-2026-07-03-layer42-recall-unmeasured
created: 2026-07-03
type: road-readiness-critique
status: captured
severity: high
confidence: 0.85
trust: 0.75
review_class: cross-model-adversarial-challenge
road_ready_gate: true
decision_owner: Brien (L2, changes what the next calibration window is even measuring)
parent_signal: SIG-2026-07-03-autonomy-grant-pause-drift-audit
reviewers:
  - Opus 4.8 (spot-check, confirmed all load-bearing claims in the 2026-07-03 audit and fix)
  - Fable 5 (breadth pass, found this)
related:
  - Core/frameworks/intent/spec/2026-07-03-autonomy-grant-pause-drift-audit.md
  - Core/frameworks/intent/hooks/autonomy-posture-check-layer-4.2.sh
  - Core/frameworks/intent/spec/autonomy-flight-model-ratification-tracker.md
  - .intent/signals/SIG-2026-06-12-layer42-calibration-review.md
  - .intent/signals/SIG-2026-06-28-flight-model-30day-ratification-readiness.md
---

# Layer 4.2's recall against real pause-drift has never been measured, and a first measurement puts it near zero

## What happened

Brien asked for the 2026-07-03 audit and fix to be put through a cross-model challenge: Opus 4.8 to
spot-check the load-bearing claims, then Fable 5 to range outward into angles neither Sonnet nor Opus
were set up to consider. Opus confirmed every checkable claim in the audit and the fix (two prior
signals exist and say what was claimed, the STOPWORD_TARGETS patch suppresses 8 of 9 historical fires
while honestly leaving `team-configs` open, the hook fails open and stays warn-only). Fable's breadth
pass surfaced something none of the prior work asked: every precision measurement on Layer 4.2 (the
06-12 review, the 06-28 review, this audit, Opus's check) counted false positives against a 9-fire
sample. Nobody measured whether the detector catches real hedges at all.

## The measurement (verified directly, not just relayed from the model chain)

`/Users/brien/.claude/audit/autonomy-grant-stop-detections.log` holds 231 lines of genuine
lexically-caught pause-drift (CHECK1-7 true positives, the exact behavior Layer 4.2 is meant to
structurally replace). Running `NEXT_ACTION_RE` (the claim-detection regex in
`autonomy-posture-check-layer-4.2.sh`) against each entry's logged tail:

- **17 of 231 (7.4%) matched.** This is a lower bound: only the last ~200 characters of each catch are
  logged, so the true match rate against full messages may be somewhat higher, but a spot-check of the
  5 most recent entries (2026-07-02 through 2026-07-03, phrasings like "say the word if instead you
  want to...", "Want me to look up the current fee balance...", "Say the word Tuesday and we run both
  tracks") shows zero matches, and these are exactly the natural-language hedge shapes Layer 4.2 exists
  to catch.

## Why this matters more than the team-configs residual

The 2026-07-03 audit and fix corrected a false-positive classification bug and left `team-configs` as
an honest, documented residual. That work is sound (Opus confirmed it) but was entirely about
precision. This finding says precision was never the binding constraint: a detector with ~7% recall
that also has near-perfect precision on a 9-fire sample is not close to ready, it has barely fired.
Continuing the calibration plan as originally sequenced (patch, then run a 7-10 day warn-only window,
then promote on a clean read) will very likely produce another clean-looking window for the wrong
reason: not because the detector got precise, but because it still rarely fires. A clean window under
current conditions is not evidence of readiness.

## Two structural issues, not just the recall gap

1. **Suppressed fires are telemetry-invisible.** The stopword-suppression fix (2026-07-03) makes a
   suppressed candidate indistinguishable from a genuinely-executed claim in the jsonl log (both log as
   `would_block:0`). 200 of 1735 `would_block:0` rows already carry non-empty `next_actions` (verified
   count). The next calibration window cannot be audited for what the suppression rule is actually
   doing without a reason field.
2. **The pronoun carve-out may be hiding real drift, not just noise.** The `STOPWORD_TARGETS` fix
   suppresses pronoun targets unconditionally (Fable: "the referent of 'I'll run that' is a real action
   named earlier in the response"). The 8/9 evidence justifying that suppression comes from a sample
   with zero true positives, so it cannot distinguish "pronoun implies false positive" from "we have
   not yet observed a pronoun-target true positive." This does not undo the 2026-07-03 fix (which is
   still correct given what was known), it means the fix's blast radius is larger than characterized.

## Also found (lower severity, not gating)

- The L2 promote/retire decision has now been surfaced through the same channel (a file in
  `.intent/signals/`) three times (06-12, 06-28, this audit) without reaching a surface Brien actually
  reads at session start. `SESSION_QUEUE.md` and `SESSION_HANDOFF.md` contain zero mentions of
  layer42/flight-model (verified via grep). The overwatch skill's "Signals Pending" section
  (`Core/products/forge/outputs/claude-code/meta/overwatch/SKILL.md` §Output Format) tracks staleness
  counts and thresholds but is not filtered to surface aged `decision_owner: Brien` items as an
  actionable list, so it would not have caught this specifically even though it exists and runs.
- The same entity-resolution axis this audit's own action plan sketched for the `team-configs` residual
  (does the extracted target resolve to a real file/entity, not just avoid being a stop-word) would
  also convert the pronoun carve-out from unconditional suppression into resolve-then-check, closing
  both open issues with one mechanism.

## Recommendation (surfaced, not executed, Brien's call given it changes what gets measured)

Before spending another calibration window on the current plan: widen `NEXT_ACTION_RE`'s claim grammar
to actually catch the phrasings the lexical layer already catches (question-form "Want me to...",
"say the word" deferrals) and re-measure recall against the full 231-entry ground truth (not just the
17-match tail proxy). Only once recall is at a level worth calibrating precision against does the
original patch-then-window-then-promote sequence produce a meaningful read. Full detail and the exact
mechanism Fable proposed: `Core/frameworks/intent/spec/2026-07-03-autonomy-grant-pause-drift-audit.md`
and this signal's `related` list above.

## Addendum (same day, prompted by Brien asking whether pre-summarized system output is being trusted as source of truth)

Measured how much the 7.4% figure above was itself an artifact of lossy telemetry: of the 231
sessions behind the detections log, only 37 (16%) still have their full transcript on disk, 194 (84%)
have already rotated away. On the 37 recoverable, re-running the match against the FULL last-assistant
message instead of the logged 200/300-char tail raised the match rate from 10.8% (4/37) to 27.0%
(10/37), more than double. The tail was discarding claim-bearing text that occurred earlier in the
message, exactly the failure mode Brien named unprompted while this investigation was live. For the
194 already-gone transcripts, this can never be corrected: the truncated tail is now the only record.

Fixed the proximate cause in `autonomy-posture-check-layer-4.2.sh`: the telemetry tail was
`LAST_TEXT[-200:]`, now `LAST_TEXT[-8000:]` (bounded against pathological input, not a fixed analysis
window; detection/gating logic untouched and re-verified unchanged). NOT fixed, flagged as a follow-up:
`autonomy-grant-stop-check.sh` (the lexical Stop-hook) has the identical pattern at 8 call sites
(200-300 char tails on `LAST_PARA`), left alone in this pass given the larger blast radius of a first
edit to a 664-line governance-critical file already flagged elsewhere for transcription risk.

Broader point, stated for the record: this system already has an architectural principle for exactly
this (Witness's conservation law, append-only + verbatim source preservation, no merge verb; Intent's
own `raw/` vs `knowledge/` separation where `raw/` is immutable and LLM-write-never). This hook family's
telemetry logging was not built to that standard. The gap is not missing architecture, it's an
un-applied one, and it is reasonable to assume other telemetry/log sinks in this system have the same
tail-truncation shape and have not been checked.

## Why this is `status: captured`, not `resolved`

No fix has shipped for the recall gap. This signal documents a measurement and a re-sequencing
recommendation. `catch_mechanism`: none yet, this is exactly the kind of gap a recall-tracking metric
in the calibration protocol should catch going forward, and does not today (§4 of the DRAFT spec only
tracks false-positive rate). `pipeline_survival`: not applicable, nothing has been changed yet.
