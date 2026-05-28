---
id: SIG-2026-05-28-stop-hook-check-6-trailing-observation
created: 2026-05-28
type: control-upgrade
status: resolved
severity: high
trigger: CHECK 6 implementation — trailing-observation-after-proposal drift class
closes: SIG-2026-05-27-pause-drift-cross-reference-sweep-after-prompt-rework (upstream_control_path gap)
upstream_control_path: Core/frameworks/intent/hooks/autonomy-grant-stop-check.sh
catch_mechanism: Stop hook CHECK 6 fires on every response; audit log ~/.claude/audit/autonomy-grant-stop-detections.log records CHECK6-CAUGHT events; telemetry at ~/.claude/logs/autonomy-stop-check.jsonl; 10/10 test cases passing
pipeline_survival: Hook installed at ~/.claude/hooks/ symlink; telemetry tracks trigger frequency; CHECK 6 tests in /tmp/test_check6.sh reproducible
related:
  - Core/frameworks/intent/hooks/autonomy-grant-stop-check.sh
  - feedback_pause_drift_meta_signal_on_nudge
  - SIG-2026-05-27-pause-drift-cross-reference-sweep-after-prompt-rework
  - SIG-2026-05-28-stop-hook-regex-extension-implicit-queue
---

# CHECK 6 deployed: trailing-observation-after-proposal detector

## What this closes

The incident signal `SIG-2026-05-27-pause-drift-cross-reference-sweep-after-prompt-rework`
declared an `upstream_control_path` gap:

> `Core/frameworks/intent/hooks/autonomy-grant-stop-check.sh` — needs new pattern class
> for "trailing-observation-after-proposal" detection. Heuristic: response ends with a
> sentence that comments on the structure/quality/implication of work surfaced earlier
> in the same response, without an action verb in the imperative or first-person past tense.

CHECK 6 closes that gap. The hook now catches responses that deliver
diagnosis/recommendation/analysis/artifact and then stop at a trailing analytical sentence
rather than executing the next authorized step.

## Drift pattern caught

Response shape: `[diagnosis] + [recommendation] + [artifact/analysis] + [analytical closer]`

The analytical closer reads as a complete deliverable. Structurally it is a hand-off pause.

Canonical incident: "stopped at a closing comment about delta-from-original"
(`"The biggest delta from the original prompt is that it bypasses Cortège entirely."`)
— clean factual sentence, no forbidden keyword from CHECK 5, but same drift class.

## Trigger phrases (last ~400 chars anchor)

All phrases anchored to last 400 characters of response (conservative vs CHECK 5's 1000):

| Phrase pattern | Example |
|---|---|
| `the biggest (delta\|difference\|change\|shift\|gap) (from\|with\|between\|compared to)` | "The biggest delta from the original is..." |
| `the most (interesting\|notable\|striking\|important\|significant) (aspect\|part\|thing\|point\|piece)` | "The most notable aspect is..." |
| `worth noting[: ]` / `worth noting that` | "Worth noting: option B has..." |
| `notable:` | "Notable: the flag semantics differ." |
| `of note:` | "Of note: this bypasses Stage 5." |
| `one (observation\|thing to watch\|thing to note\|thing worth noting)` | "One observation: the CONNECT flag..." |
| `the key insight (here \|is )` | "The key insight here is..." |
| `it.s worth (pointing out\|noting\|flagging)` | "It's worth noting that..." |

## False-positive gates (four stacked — ANY pass suppresses CHECK 6)

**(a) Dispatch gate** — `HAS_DISPATCH=1`: a concrete action was dispatched in this
response (regex: `dispatching|launching N sub-agent|agent(|model:`). Analytical
observations after a dispatch are legitimate narrative, not drift.

**(b) Closure-DoD gate** — response contains all three closure assertions:
`upstream_control_path:` + `catch_mechanism:` + `pipeline_survival:` (colon-form,
per `feedback_closure_dod_literal_terms`). This is legitimate signal closure, not drift.

**(c) Recommendation-with-reveal gate** — response contains a recommendation marker
AND `unless you('d)? prefer` / `unless you would prefer` / `alternatively[,.]`.
This is the required decisioning-discipline rule 6 form (recommend + reveal alternative).
Also applied as an additional gate to CHECK 4 to prevent CHECK 4 from over-firing
on the "unless you prefer B because [reason]" recommendation-with-reveal form.

**(d) L2-info-gap gate** — response contains `info gap:` / `l2 decision` /
`brien needs to decide` / `l2 item[^s]`. This is legitimate decision surfacing,
not drift.

## Test results

10/10 passing (6 block + 4 pass):

| Case | Type | Result |
|---|---|---|
| C6-B1: biggest delta closer | BLOCK | PASS |
| C6-B2: worth noting closer | BLOCK | PASS |
| C6-B3: most interesting aspect | BLOCK | PASS |
| C6-B4: key insight closer | BLOCK | PASS |
| C6-B5: of note closer | BLOCK | PASS |
| C6-B6: one observation closer | BLOCK | PASS |
| C6-P1: dispatch present | PASS | PASS |
| C6-P2: closure-DoD assertions present | PASS | PASS |
| C6-P3: recommendation-with-reveal | PASS | PASS |
| C6-P4: L2 info gap named | PASS | PASS |

## Side fix: CHECK 4 over-fire on recommendation-with-reveal

Discovered during test design: CHECK 4's `unless.*prefer` pattern was
catching `"unless you prefer B because [reason]"` — the REQUIRED
recommendation-with-reveal form. CHECK 4 now gates on
`C4_HAS_REC_REVEAL`: recommendation marker + `unless you('d)? prefer`
together. "Prefer" variants are recommendation-reveals; "redirect /
tell me otherwise / stop me" variants remain conditional-queue.
