---
id: SIG-PROJECTION-DIVERGENCE-2026-09-16
title: "Intent never measured what a Spec loses on its way down to a Contract, and the operator that would measure it sat in a chat log for three months"
type: signal
kind: gap
status: symptom-repaired, upstream-pending
severity: medium
confidence: high
created: 2026-09-16
discovered_by: host-pickup wave, intake issue 12
scope: intent framework, Spec plane, work-ontology levels 1 to 4
affects:
  - /Users/brien/Workspaces/Core/frameworks/intent/spec/work-ontology.md
  - /Users/brien/Workspaces/Core/frameworks/intent/spec/SPEC-INTENT-PROJECTION-DIVERGENCE-001.md
  - /Users/brien/Workspaces/Core/frameworks/intent/reference/goal-command-and-eval-prd-analysis.md
  - /Users/brien/Workspaces/Core/frameworks/intent/spec/README.md
related:
  - https://github.com/theparlor/intake/issues/12
lineage:
  - https://github.com/theparlor/intake/issues/12
upstream_control_path: "PARTIAL, and named as partial. /Users/brien/Workspaces/Core/frameworks/intent/hooks/closure-discipline-signal-check.sh is the one comparator of this family running in production, and it covers exactly one hard-coded seam (a resolved claim without its mechanism). The general operator is specified at /Users/brien/Workspaces/Core/frameworks/intent/spec/SPEC-INTENT-PROJECTION-DIVERGENCE-001.md but is NOT runnable: its per-seam tolerances and gain function are uncalibrated (OQ6, parked with a named unblocking condition, a corpus of ten real Spec-to-Contract pairs via Core/products/understudy). Until that corpus exists there is no write-through control on general Spec-to-Contract intent loss."
catch_mechanism: "PARTIAL. The unchecked Done-when box in the spec's section 3 is the honest standing flag that calibration is missing, and the Operators table in /Users/brien/Workspaces/Core/frameworks/intent/spec/README.md makes the operator reachable so the next session finds it rather than re-inventing it (which is the failure this signal records). No invariant or lint fires on uncalibrated tolerances, because there is nothing yet to compare against."
verification_command: "grep -c 'SPEC-INTENT-PROJECTION-DIVERGENCE-001' /Users/brien/Workspaces/Core/frameworks/intent/spec/README.md /Users/brien/Workspaces/Core/frameworks/intent/reference/external-patterns-index.md && grep -n 'upstream_control_path' /Users/brien/Workspaces/Core/frameworks/intent/hooks/closure-discipline-signal-check.sh"
---
# Projection divergence is unmeasured, and the design for measuring it was stranded

## Plain language

Intent's work ontology has always said that a Contract is the Spec's acceptance criteria
"extracted and made machine-executable". An extraction leaves a residue. In five months of
this repo running on its own loop, that residue has never been measured once. Every spec that
went through here threw some of itself away on the way down to its finish line, silently.

It used to not matter much, because a person read both the spec and the contract and
interpolated between them. It matters now, because an agent reads the contract and the
contract is all there is. The loss that a colleague used to absorb now ships.

## Two gaps, one signal

**Gap 1, the substantive one.** No instrument reads the difference between adjacent
work-ontology levels. The one exception is `closure-discipline-signal-check.sh`, which does
exactly this at one hard-coded seam: it blocks a signal claiming `status: resolved` that does
not carry the mechanism underneath the claim. That hook has caught real drift since May 2026.
Nobody noticed it was an instance of a general shape.

**Gap 2, the process one.** The operator that generalizes it was designed on 2026-06-16 in a
chat session, captured to an intake issue, triaged the next day with a verdict of "a Code
session will file this", and then sat for three months. The triage comment was correct about
what needed to happen and there was no mechanism that made it happen. Filing a design into an
issue tracker is not filing it into the framework.

## What landed

- `spec/SPEC-INTENT-PROJECTION-DIVERGENCE-001.md`, the operator as a spec-grade artifact in
  the house Intent, Shape, Contract form, with a plain-language layer.
- `reference/goal-command-and-eval-prd-analysis.md`, the completed source manifest, with the
  `/goal` mechanism verified against the vendor documentation and five corrections to the
  June capture.
- An Operators table in `spec/README.md` so the next session finds this rather than
  re-deriving it.

## What did not land, and why the status is not resolved

The operator is specified and not runnable. Its per-seam tolerances and its gain function are
empirical and cannot be honestly set from an armchair. Setting them needs a corpus of real
Spec-to-Contract pairs with known outcomes, which is `Core/products/understudy/` work and is
parked with that named unblocking condition.

So: the instance is repaired (the design is in the framework, reachable, sourced, and its
open questions are ruled), and the upstream control is partial (one production comparator at
one seam, no general one). `symptom-repaired, upstream-pending` is the honest value.

## The nearest-miss worth recording

Coherence engineering's README has listed a "drift detector" under "Not yet built" since
2026-05-20. It would have been easy, and wrong, to file this operator there. They are
siblings on orthogonal axes: coherence engineering's detector scans **many producers across
one surface**, and this one scans **one intent across altitudes**. The spec says so
explicitly in its section 2.11 boundary, and carries a frontmatter cross-reference to that
framework, which is the cross-reference discipline SIG-COH-DEBT-013 asked for.
