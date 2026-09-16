---
id: SIG-VERIFIER-COMPOSITION-RULE-2026-09-16
title: "Intent types a single evaluation verdict but has no rule for composing several over one artifact; every live aggregation is strict AND"
type: signal
kind: gap
status: symptom-repaired, upstream-pending
severity: medium
confidence: high
created: 2026-09-16
discovered_by: host-pickup wave, intake issue 18
scope: intent framework, evaluation and comparator architecture
affects:
  - /Users/brien/Workspaces/Core/frameworks/intent/spec/typed-evaluation-verdicts.md
  - /Users/brien/Workspaces/Core/frameworks/intent/spec/autonomy-gate-surface-matrix-v0-DRAFT.md
  - /Users/brien/Workspaces/Core/frameworks/coherence-engineering/contracts/
  - /Users/brien/Workspaces/Core/frameworks/coherence-engineering/positions/optimization-iteration.md
related:
  - https://github.com/theparlor/intake/issues/18
  - https://arxiv.org/abs/2606.16140
lineage:
  - https://github.com/theparlor/intake/issues/18
upstream_control_path: "None yet. The candidate composition rule is written into spec/typed-evaluation-verdicts.md section 8 as a CANDIDATE, explicitly non-normative until its falsification test passes. Making it normative requires a scoring pass over the CON-COH corpus plus 30 hand labels from Brien, which is queued, not done. Until then no write-through control exists, because promoting an unvalidated aggregation function into the comparator path is the failure this signal is about."
catch_mechanism: "Partial. The existing invariant tools/typed_verdict_invariants.py (INV-INTENT-NO-SELF-GRADED-CLOSURE) already enforces that a self-graded verdict cannot close a spec, and the composed score inherits the lowest criteria_origin of its inputs, so a composed self-graded number cannot smuggle closure authority through aggregation. What is NOT caught: a future aggregation implemented as strict AND somewhere new. No invariant inspects aggregation shape."
verification_command: "grep -n 'Composing several verdicts over one artifact' /Users/brien/Workspaces/Core/frameworks/intent/spec/typed-evaluation-verdicts.md && grep -n 'Comparator authority at the seam' /Users/brien/Workspaces/Core/frameworks/intent/spec/autonomy-gate-surface-matrix-v0-DRAFT.md"
---

# The gap

`spec/typed-evaluation-verdicts.md` (2026-06-09) is careful about what **one**
`observation.evaluated` verdict is allowed to do: `criteria_origin` decides whether a verdict
may close a spec, gate an inner loop, or only route attention. It says nothing about what
happens when several verdicts land on the same artifact.

In practice the answer everywhere is strict AND. The clearest case is the CON-COH contract
family: five machine-assertable contracts over one corpus, and the first-run record at
`/Users/brien/Workspaces/Core/frameworks/coherence-engineering/contracts/runs/CON-COH-005-first-run-2026-06-10.md`
reads `verdict: FAIL, 1 violation` over a corpus where four of five contracts passed
everywhere. A corpus-wide audit returns one bit. It cannot answer which of two failing
documents is closer to good, which is the question a repair pass needs.

# Why it surfaced now

Intake issue 18 (2026-06-21, host-pending for three months) carried an analysis of
VibeThinker-3B built from a secondary write-up, with the technical report marked unread. The
report was read in this session. Its CLR stage aggregates `M = 5` binary claim verdicts as
`((1/M) * sum v)^M`, a power-mean, and buys 2.7 to 6.1 benchmark points across six benchmarks
with zero added parameters. That is the composition rule Intent lacked, and it arrives with a
reason for not being strict AND: a function that zeroes on any failure cannot rank imperfect
candidates, and ranking imperfect candidates is the entire output.

# What was repaired, and what was not

Repaired (the instance): the rule is written into `spec/typed-evaluation-verdicts.md` as a
new section 8, marked CANDIDATE, with the falsification test that would make it normative. A
sixth missing facet, comparator authority at the seam, was added to
`spec/autonomy-gate-surface-matrix-v0-DRAFT.md` section 4. Rationale, rejected alternatives
and the full disposition are in
`/Users/brien/Workspaces/Core/frameworks/intent/knowledge/design-rationale/RAT-004-verifier-at-the-seam.md`.

Not repaired (upstream): nothing prevents the next comparator from being written as strict
AND, and nothing validates the power-mean against Brien's own corpus. Both are queued. This
signal stays `symptom-repaired, upstream-pending` until the falsification test runs and the
rule either becomes normative with an invariant behind it or is withdrawn.

# Second-order finding

`spec/autonomy-gate-matrix.md` is present and untracked in the main checkout of
`/Users/brien/Workspaces/Core/frameworks/intent`. It is the prior-Claude v0.1 source that was
elevated into the tracked `autonomy-gate-surface-matrix-v0-DRAFT.md` on 2026-05-26. A session
reading the main checkout sees the untracked file first and would edit a copy no other
session can see. Not repaired here (deleting or committing another session's untracked file
is not this issue's business); recorded so the next reader is not fooled.
