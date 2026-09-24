---
id: SIG-2026-09-24-jev-stop-hook-family-kev-shadow-read
created: 2026-09-24
type: evaluation
status: observed
severity: low
confidence: 0.7
decision_owner: Brien (any change to a Stop hook is his; nothing here changed one)
related:
  - Core/products/_intake/2026-09-23-jev-system-one-evaluation/design.md (section 6.0 rank 2, section 7)
  - Core/frameworks/intent/.intent/traces/jev-hooks-2026-09-24/README.md
  - Core/frameworks/intent/hooks/lexical-layer-freeze.yaml
  - Core/frameworks/intent/.intent/signals/SIG-2026-06-12-layer42-calibration-review.md
upstream_control_path: "None changed. The lexical CHECKs 1 to 8 and Layer 4.2 stay exactly as frozen. The candidate control is a shadow column (P(queues) logged beside each CHECK fire in ~/.claude/logs/autonomy-stop-check.jsonl) that does not exist yet and would need a resident local model endpoint; it is a proposal for Brien, not a repair."
catch_mechanism: ".intent/traces/jev-hooks-2026-09-24/score_hooks.py re-scores any trace against the local labels; hooks/tests/test_layer42_precision.py remains the human-labeled catch for the hook itself. No new invariant, because no mechanism changed."
verification_command: "python3 .intent/traces/jev-hooks-2026-09-24/score_hooks.py --trace .intent/traces/jev-hooks-2026-09-24/trace-kev-hooks.jsonl"
---

# A local typed-decision model reads Stop-hook tails better than the regex family on blind labels, and worse than the humans on the hard cases

## What happened, in plain language

The eight autonomy CHECKs and Layer 4.2 are regexes for one question: did this turn hand back work it was
already allowed to do. On 190 real tails from the last four months (88 the CHECKs caught, 88 they did not, 14 the
humans labeled in July), a local open-weight decision model (Kev-4B, the Jev recreation) was asked that question
as one probability. Against a blind Sonnet read of the same tails it had better precision than the regexes
(0.45 against 0.37) at slightly lower recall (0.83 against 0.90). Used after the regex, it would have silenced
33 of 64 false fires and cost 4 true ones. On the 14 human-labeled firings it was at chance: it cannot tell a
legitimate deferral (an OAuth prompt, a budget window, a production write that is L0) from a handback, which is
the exact distinction the July regex patch encoded.

## What changes

Nothing. No hook was edited; the freeze holds. The trace (hashes and probabilities, no text) is in
.intent/traces/jev-hooks-2026-09-24/. The tails and labels stay local under ~/.claude/logs/jev-hook-eval/.

## The decision Brien is being handed

Whether to run the model in shadow beside the CHECKs for two weeks (needs a resident Kev endpoint on the hub,
about 8 GB of memory, and 0.5 s or less per Stop, which Kev-4B does not meet: 4.6 s contended, 1.05 s median on an idle server) before any
retire or demote conversation. Recommendation: yes to the shadow, no to any retirement on this evidence.
