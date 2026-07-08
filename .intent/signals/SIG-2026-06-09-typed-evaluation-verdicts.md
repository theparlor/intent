---
id: SIG-2026-06-09-typed-evaluation-verdicts
type: signal
status: symptom-repaired, upstream-pending
severity: high
created: 2026-06-09
target: "Observe-loop LLM-as-Judge — P0 same-frame evaluation made structurally visible via typed verdicts"
discovered_during: "Parallax testing-triad grounding (2026-06-09): the grounding doc named the Observe-loop judge the stack's headline gap; the 5-lens triad panel restated it as a TYPING flaw — an eval-pattern judge at test-grade displacement (criteria_origin: self, same lineage) consumed at UAT-grade authority (spec closure)."
requested_by: brien (via workflow orchestration)
verification_command: "grep -c 'criteria_origin' /Users/brien/Workspaces/Core/frameworks/intent/spec/event-catalog.md && grep -q 'evaluator_repo' /Users/brien/Workspaces/Core/frameworks/intent/spec/event-catalog.md && grep -q 'MUST NOT.*close a spec at acceptance authority' /Users/brien/Workspaces/Core/frameworks/intent/spec/event-catalog.md && grep -q 'INV-INTENT-NO-SELF-GRADED-CLOSURE' /Users/brien/Workspaces/Core/frameworks/intent/spec/typed-evaluation-verdicts.md && echo VERIFIED"
upstream_control_path: "Write-through is the amended LLM-as-Judge protocol itself (spec/event-catalog.md §Verdict Typing — emitters MUST populate criteria_origin / evaluator_model / evaluator_repo; Observe-loop steps 6-7 refuse closure on a self pass). The named catch-net is PENDING: chain_audit invariant INV-INTENT-NO-SELF-GRADED-CLOSURE (register in Core/products/library-index/chain_audit_portfolio.py per the INV-LI-* pattern, or a repo-local chain_audit for intent if stood up first). Zero-violation-start discipline applies — date-scoped to post-2026-06-09 closures/emissions so day one fires clean."
catch_mechanism: "TODAY: spec-level normative invariant only (the consumption rule in event-catalog.md + typed-evaluation-verdicts.md §3). The closure-discipline hook family matches signal frontmatter keys, NOT observation.evaluated payloads in events.jsonl — adjacent, not covering. Status stays upstream-pending until INV-INTENT-NO-SELF-GRADED-CLOSURE runs green on day one."
pipeline_survival: "The rule survives as spec text (event-catalog.md amendment + typed-evaluation-verdicts.md) propagated to every .intent/ adopter; becomes machine-enforced when the chain_audit invariant registers."
reconsider_when:
  - "INV-INTENT-NO-SELF-GRADED-CLOSURE registers and fires zero violations on day one -> flip status to resolved."
  - "an emitter ships observation.evaluated without the three required fields after 2026-06-09 -> the write-through failed; prioritize the catch-net registration."
  - "a legitimate closure need arises that derived-criteria judging cannot serve (e.g., no exterior judge exists for the artifact class) -> the Brien-override path (decision.recorded) is the designed relief valve; if overrides become routine, the type system is miscalibrated — revisit."
---
# Typed evaluation verdicts — same-frame judging made visible and demoted

## What changed
1. **`spec/event-catalog.md`** (surgical amendment, dated 2026-06-09 in the header blockquote house style):
   - `observation.evaluated` schema now carries three REQUIRED fields: `criteria_origin: self|distilled|derived`, `evaluator_model`, `evaluator_repo: same-repo|external`.
   - New §Verdict Typing subsection states the normative consumption invariant: **a `criteria_origin: self` verdict MUST NOT close a spec at acceptance authority** — inner-loop instrument only; closure requires `derived` OR an explicitly recorded Brien override (`decision.recorded`).
   - Observe-loop integration steps 4/6/7 amended: a self-graded `pass` no longer marks a spec complete.
2. **`spec/typed-evaluation-verdicts.md`** (new addendum): rationale (P0 same-frame failure; the triad's typing-flaw diagnosis), the full six-field verdict type tuple, migration (pre-2026-06-09 events grandfathered as `criteria_origin: self` — visibly demoted, never deleted; closed specs not mechanically reopened), and the enforcement path naming `INV-INTENT-NO-SELF-GRADED-CLOSURE` as the catch-net.

## Why
The original protocol let an in-repo, same-lineage judge grade the spec's own prose criteria and feed the verdict straight into closure — a second camera at the same coordinate. The triad analysis showed the conflation precisely: eval mechanism, test-grade displacement, UAT-grade consumption. The fix makes the displacement label honest and load-bearing rather than deleting the judge — a same-frame fuzzy judge remains legitimate as the cheap fuzzy test it actually is.

## What remains (upstream-pending)
- Register `INV-INTENT-NO-SELF-GRADED-CLOSURE` in chain_audit (portfolio or repo-local) and demonstrate zero-violation start.
- Instrument the actual Observe-agent emitters to populate the three fields (the spec now requires it; no emitter code was changed in this pass).

## Triage, 2026-07-08

Disposition: still pending. Ran this signal's own verification_command directly: it prints VERIFIED, confirming the spec-level write-through (event-catalog.md's required fields, the MUST-NOT consumption rule, typed-evaluation-verdicts.md's invariant name) is in place exactly as claimed. But the signal's own reconsider_when clause is explicit that VERIFIED at the spec level is not the same as resolved: that requires INV-INTENT-NO-SELF-GRADED-CLOSURE to actually register in chain_audit and fire zero violations on day one. Searched Core/products/library-index/ and this repo for the invariant name: no registration found anywhere. Needed control: register the invariant per the named pattern (INV-LI-* precedent in the library-index chain_audit portfolio, or a repo-local chain_audit for intent if stood up first) and demonstrate the zero-violation start this signal specifies.
