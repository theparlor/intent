---
title: "RAT-004, Verifier at the seam: what VibeThinker-3B contributes to Intent's comparator architecture"
id: RAT-004
type: design-rationale
maturity: draft
status: terminal
confidentiality: internal
reusability: adaptable
confidence: 0.75
created: 2026-09-16
source_record: raw/research/2026-09-16-vibethinker-3b-verifiable-reasoning.md
lineage:
  - https://github.com/theparlor/intake/issues/18
attribution:
  external_source: "Xu, Liu, Wang, Min, Dai, Yin, Chen, Zhou, Zhang (Sina Weibo), VibeThinker-3B technical report, arXiv 2606.16140v1, 2026-06-15"
  mapping_author: "Brien Tate, via intake #18 (2026-06-20) and this host session (2026-09-16)"
affects:
  - spec/typed-evaluation-verdicts.md
  - spec/autonomy-gate-surface-matrix-v0-DRAFT.md
  - /Users/brien/Workspaces/Core/frameworks/coherence-engineering/positions/optimization-iteration.md
  - /Users/brien/Workspaces/Core/frameworks/coherence-engineering/contracts/
related:
  - knowledge/design-rationale/RAT-002-double-loop-learning.md
  - knowledge/design-rationale/RAT-003-dual-circuit-architecture.md
  - spec/SPEC-INTENT-SEAM-DECOMPOSITION-001.md
---
# RAT-004, Verifier at the seam

## Plain language first

**What this is.** A small model from Sina Weibo, VibeThinker-3B, does something at answer
time that looks exactly like a piece of architecture Intent already specifies: it puts a
checker at a boundary and lets the checker's verdict decide which candidate wins. It is
outside evidence that the shape is right, and it hands over one part Intent was missing.

**What Intent was missing.** Intent's typed-evaluation-verdicts spec is careful about what a
single verdict is allowed to do. It says nothing about what happens when five verdicts land
on the same artifact. Today the answer everywhere in Brien's tree is "all five must pass",
which gives a corpus one bit of information and no way to say which of two failing documents
is closer to good. VibeThinker's aggregation function is a better answer and it is one line
of arithmetic.

**What changed here, concretely.** Three edits, all small and all reversible. A composition
rule was added to the typed-verdicts spec as a candidate with a falsification test. A sixth
missing facet was added to the autonomy gate matrix's own list of missing facets. The paper
was registered as a partial sibling at Coherence Engineering's Optimization / Iteration
position. Nothing that was already ratified was rewritten.

**What was rejected, and why it matters.** The June capture proposed that a constraint seam
should aggregate by strict AND, so that one violation drives coherence to zero. The paper
deliberately does not do that, and the reason is the useful part: a function that zeroes on
any failure cannot rank imperfect candidates, and ranking imperfect candidates is the entire
output. That rejection is the most valuable thing in this note.

**Who should read what.** If you only want the decisions, read sections 2, 3 and 6. If you
want the verified mechanics and the numbers, read
[the source record](../../raw/research/2026-09-16-vibethinker-3b-verifiable-reasoning.md).

---

## 1. What survives contact with the primary source

Intake issue [#18](https://github.com/theparlor/intake/issues/18) built four mappings from a
secondary write-up, with the technical report explicitly marked unread. Here is the state of
each after reading the report.

| Mapping proposed in June | Status after the primary source |
|---|---|
| CLR is an independent reinvention of "typed comparator at a seam" | **Survives, and strengthens.** Every structural feature matches: a boundary, a typed pass or fail verdict at that boundary, an aggregate over verdicts, and a consumption rule that keeps the self-graded judge out of the closure position. The paper adds an empirical size for the gain: +2.7 to +6.1 points across six benchmarks with zero parameters added. |
| CLR supplies the missing composition rule that separates constraint seams from descriptive seams | **Survives as "supplies a composition rule". Does not survive as "separates the two seam types".** The function is `(mean of verdicts)^M`, a power-mean. It is strictly between an average and a minimum, and it is deliberately graded, not dominating. It is a good default for any seam that aggregates several pass-or-fail checks. It does not, on its own, distinguish a constraint seam from a descriptive one. See section 6.1. |
| MGPO is the coefficient of bravery applied at training time | **Interpretation only, and the symbol was wrong.** MGPO's boundary weight is `w(q) = exp(-gamma * D_ME(p(q) || 0.5))`. The paper's only `lambda` is Long2Short's reward-redistribution magnitude, fixed at 0.2, which is unrelated. The conceptual rhyme (spend effort where outcomes are still uncertain) survives; the claim of one shared parameter does not. See section 6.2. |
| Long2Short makes per-seam gain and loop speed literal | **Survives, and sharpens.** The formula only redistributes among trajectories that are already correct, and it is zero-sum, so group-level reward is unchanged. That is the precise statement of "faster loop at constant coherence": you may not buy speed from the correctness budget, only from the redundancy budget inside the correct set. |
| Spectrum-to-Signal is "point at the topology, not the decision stream" inside a training pipeline | **Survives, and gains a measurable operator.** See section 4. |
| Specialist by design, so autonomy is bounded by verifiability at the seam | **Reframed, and materially improved.** The paper's Parametric Compression-Coverage Hypothesis is a claim about what a capability costs, not a prohibition on what may run without a verifier. See section 3. |

---

## 2. Opportunity A: a composition rule for typed verdicts

### The gap in the current spec

`spec/typed-evaluation-verdicts.md` types one verdict and governs what that one verdict may
be consumed for. It has no rule for aggregating several verdicts over one artifact. Every
live aggregation in the tree today is strict AND. The clearest instance is the CON-COH
contract family in Coherence Engineering: five machine-assertable contracts, each returning
PASS or FAIL per file, aggregated so that one violation makes the run FAIL. The first-run
record at
`/Users/brien/Workspaces/Core/frameworks/coherence-engineering/contracts/runs/CON-COH-005-first-run-2026-06-10.md`
reads "FAIL, 1 violation" over a corpus where four of five contracts passed everywhere.

Strict AND gives the corpus one bit. It cannot answer "which document is closest to
coherent", which is the question a repair pass actually needs.

### The rule borrowed

Given `M` binary verdicts `v[1..M]` over one artifact from judges of the same
`criteria_origin`, aggregate as

```
r = ( (1/M) * sum_m v[m] ) ^ M
```

Two properties are why this is the right default rather than min or mean.

1. **It stays positive until everything fails.** With `M = 5`, four of five passing yields
   0.328 and three of five yields 0.078. Both are bad; the first is visibly less bad. Strict
   AND returns zero for both and destroys the ordering. Any comparator whose job includes
   "rank the imperfect candidates" needs a graded function, and almost all of Brien's
   comparators have that job.
2. **Strictness is derived, not tuned.** The exponent is the number of checks. Add a sixth
   contract to CON-COH and the same pass fraction scores lower, automatically. There is no
   tolerance knob to argue about in review, because tolerance is a consequence of how broadly
   you decided to audit.

### What changes, concretely

`spec/typed-evaluation-verdicts.md` gains a section 7, "Composing several verdicts over one
artifact", carrying the rule as a **candidate** with the falsification test below. The
consumption rule in section 3 of that spec is untouched: a composed `r` inherits the lowest
`criteria_origin` of its inputs, so five self-graded checks compose to a self-graded number
and still may not close a spec.

### Falsification test (run before this stops being a candidate)

Take the CON-COH corpus run, which already has per-file, per-contract PASS and FAIL for five
contracts. Compute three orderings of the files: strict AND, plain mean, and the power-mean.
Hand-label a sample of 30 files by how much repair each actually needs. The claim is
falsified if the power-mean ordering does not correlate better with the hand labels than the
plain mean, or if it collapses into the same one-bit partition as strict AND on this corpus.

**Not run in this session.** The test is specified; it needs a scoring pass over the corpus
and 30 hand labels, which is Brien's judgment, not an agent's. Queued.

---

## 3. Opportunity B: verifier strength as a facet of the autonomy gate

### The rule as captured in June, and why it was too strong

The capture proposed: **autonomy level is bounded by verifiability at the seam. No
comparator, no high L-level.** Open question 3 in that capture asked whether this forecloses
L3 and above on any seam without a hard verifier.

The primary source answers it. VibeThinker does not say unverifiable work must be forbidden.
It says verifiable reasoning is *parameter-dense*, meaning it compresses into a small core,
while open-domain competence is *parameter-expansive*, meaning it needs breadth. That is a
statement about price. The same model that reaches 94.3 on AIME26 sits at 70.2 on
GPQA-Diamond against 80 to 92 for the large models, and the authors name the gap rather than
hide it.

### The rule that survives

> Autonomy at a seam is bounded by the **consumption authority its comparator has earned**,
> and the price of a higher-authority comparator is **coverage**, not permission.

This lands cleanly on machinery Intent already has. `typed-evaluation-verdicts.md` already
ranks comparators by `criteria_origin`: `self` is cheap, same-lineage, and capped at
inner-loop authority; `derived` requires an exterior judge that wrote its own criteria and is
the only origin allowed to close. VibeThinker is the external instance of the cheap end of
that ladder being genuinely useful: a same-lineage, self-graded, sampled comparator bought
real points, and it bought them precisely because it was consumed at ranking authority and
never at closure authority. The benchmark, an exterior verifier, kept the closure position.

The practical consequence is the opposite of a prohibition. A seam with no hard verifier is
not barred from L3; it is told what L3 costs there, which is a foreign judge or a human in
the closure position while the cheap self-graded judge does the ranking underneath.

### What changes, concretely

`spec/autonomy-gate-surface-matrix-v0-DRAFT.md` (SPEC-INTENT-AUTONOMY-SURFACE-MATRIX-001)
carries a numbered list at section 4, "Missing facets this matrix exposes", with five
entries. This adds a sixth: **comparator authority at the seam**. The matrix's existing
deterministic-precondition column is a verifiability construct, but it is binary, the hook
fires or it does not, and it carries no term for how much authority the seam's comparator has
earned or what buying more would cost. That is the gap the facet names.

The spec is `status: draft` and section 4 exists to collect exactly this kind of entry, so
the edit is additive and reversible.

**A note on which file.** Intake #18's target would naturally have been
`spec/autonomy-gate-matrix.md`, which is what a reader sees in the main checkout. That file
is **untracked**: it is the prior-Claude v0.1 source, and it was elevated into the tracked
`autonomy-gate-surface-matrix-v0-DRAFT.md` on 2026-05-26 (that spec's own frontmatter records
the ingestion, with `source_artifact` pointing at
`raw/competitors/2026-05-25-prior-claude-source-artifacts.md`). Editing the untracked copy
would have put the facet somewhere no other session can see. The tracked spec is the one that
got the edit.

---

## 4. Opportunity C: select on coverage, not on loss

Open question 5 in the capture asked for an operator that measures whether topology has been
prematurely collapsed during a converge phase. The paper supplies one, and it is cheap.

Diversity-Exploring Distillation picks, for each domain, the intermediate checkpoint that
produces **more valid solutions** on a probing set, rather than the checkpoint with the lowest
validation loss. Then it merges the domain specialists at the parameter level.

The transferable operator: **at each converge step, count the distinct valid solutions the
current state can still produce against a fixed probe set. A falling count is the collapse
signal.** Loss going down while the valid-solution count goes down is premature collapse,
stated as two numbers rather than as a judgment call.

This is the same instinct as the dissent-preservation conservation law that Coherence
Engineering already enforces at its Judgment / Critique position, arrived at from the other
direction: dissent preservation forbids flattening disagreement; the valid-solution count
measures whether flattening happened anyway.

### What changes, concretely

A partial-sibling row at Coherence Engineering's Optimization / Iteration position
(`positions/optimization-iteration.md`, section 4, External candidates). Partial, not full:
CLR generates `K` candidates, scores them, and selects. It never mutates a candidate on the
basis of its score, so by that document's own disambiguation rule it supplies a
`deterministic_metric_fn` and a select-from-K pattern, not a loop.

---

## 5. Thread B: the tiered-router slot, rejected for now with a named trigger

The capture filed a second thread: VibeThinker-3B as a candidate in the local model tier,
"route verifiable work cheap, reserve Claude for high-judgment synthesis", with open question
7 asking whether it earns a slot or overlaps existing capacity. Three facts checked on this
machine on 2026-09-16 decide it.

1. **It cannot be an agent worker.** The model card states the model "was not trained on
   tool-calling or agent-based programming data" and the authors advise against function
   calling, API orchestration, and autonomous coding agents. Every routed workload in Brien's
   pipelines is agent-shaped. This model can only be handed a self-contained problem and
   asked for an answer.
2. **There is no router to slot it into.** `/Users/brien/Workspaces/Core/tools/litellm-gateway/`
   is `status: available-route-not-default`, and its own CONTEXT.md says "not yet running, no
   API keys provisioned, not registered as a LaunchAgent". Nothing is listening on port 4000.
   The premise that the model "slots into the existing Ollama tier" is false: the Ollama tier
   exists as two entries in a config file for a gateway that has never started.
3. **It would not overlap, which is the one point in its favour.** Ollama is running locally
   and serving gemma3:12b, gemma3:4b, qwen2.5:14b, llama3.1:8b, llama3.2, llama4:scout, and
   two embedding models. Every one is a general-purpose instruct model. There is no
   verifiable-reasoning specialist on the box. Open question 7's worry about overlap is
   answered: no overlap.

**Ruling: do not pull the weights, do not spec an eval.** Pulling a 6 GB model with no
consumer is machinery without a closed loop. The named trigger that would reverse this: a
recurring workload of self-contained, verifier-checkable subproblems appears in a live
pipeline, and the litellm gateway is actually running. Both conditions, not either. Queued
with that trigger rather than as an open-ended "eval later".

---

## 6. Rejected, with reasons

### 6.1 Rejected: constraint seams aggregate by strict AND

The capture proposed that constraint-seam gain should be non-linear such that "one violation
drives aggregate coherence toward zero regardless of how many descriptive claims passed", and
offered strict AND or min as the candidate shape.

The paper does not do this, and the reason is instructive. A function that returns zero on any
failure returns zero for every candidate on any hard problem, and the method's entire output
is a ranking over candidates. Strict AND would make CLR return nothing on exactly the
problems it exists to solve. The power-mean is the design choice that keeps discrimination
alive under near-universal imperfection.

So the borrowed rule is the composition function in section 2, offered for **any** seam that
aggregates several pass-or-fail checks. It is not offered as the thing that types a seam as
constraint rather than descriptive. That typing needs a different discriminator and this
paper does not supply one. The capture's open question 2, about what the analogous comparator
is for descriptive seams without a hard verifier, remains genuinely open and is now sharper:
section 3 says the answer is not a different function, it is a more expensive judge.

### 6.2 Rejected: one lambda governs both training-time and runtime bravery

MGPO's boundary weight uses `gamma` against a max-entropy divergence from 0.5. Long2Short's
`lambda` is a reward-redistribution magnitude fixed at 0.2. They are different parameters in
different stages doing different jobs, and neither is a runtime autonomy coefficient. The
capture's open question 4 asked whether a single lambda governs both; the answer from the
source is no, and the rhyme should be cited as a rhyme.

### 6.3 Rejected: treating the June numbers as verified

Four of the capture's mechanism claims were wrong and one number was wrong. The full diff is
section 7 of
[the source record](../../raw/research/2026-09-16-vibethinker-3b-verifiable-reasoning.md).
The capture's own confidence line said the framework mapping was interpretation and the
primary source was unread, which was honest; the corrections here are the cost of the three
months between capture and reading, not a fault in the capture.

---

## 7. The capture's open questions, dispositioned

| # | Question | Disposition |
|---|---|---|
| 1 | Does nonlinear claim composition beat linear weighting at Intent comparators, and what shape? | **Shape answered** by the source: power-mean with exponent equal to the check count, not soft-min. **Empirical half open**, with a falsification test specified in section 2 against the CON-COH corpus. Queued. |
| 2 | What is the comparator for descriptive seams with no hard verifier? | **Open, and sharper.** Section 3 argues the answer is not a different aggregation function but a costlier judge: a `derived`-origin exterior comparator in the closure position, with the cheap self-graded one ranking underneath. |
| 3 | Is "autonomy bounded by verifiability" too strong? | **Answered: yes, as written.** Replaced by the consumption-authority formulation in section 3, which prices autonomy rather than forbidding it. |
| 4 | Is there a single lambda governing training-time and runtime bravery? | **Answered: no.** Section 6.2. |
| 5 | What operator measures premature topology collapse during a converge phase? | **Answered.** Count of distinct valid solutions against a fixed probe set, falling while loss falls. Section 4. |
| 6 | Does Long2Short map to a loop-speed objective that does not trade away coherence, expressible without token count? | **Yes, and the mechanism is the constraint.** Redistribution is confined to the already-correct set and is zero-sum, so speed is bought from redundancy inside the correct set and never from the correctness budget. The token-count-free statement is: redistribute gain among outputs that already pass the seam, holding the seam's aggregate gain constant. |
| 7 | Does a 3B verifiable-reasoning specialist earn a tier-router slot? | **Answered: not now.** Section 5, with a two-condition trigger. |
| 8 | Do the report's definitions survive contact with the actual math? | **Answered: mostly, with four corrections and one number.** Section 7 of the source record. |

---

## 8. Confidence and what would change this note

Confidence 0.75. The mechanism record is high confidence, read directly from the paper's
formulations. The mappings are interpretation, unchanged in kind from the capture; what
changed is that they are now interpretation of the real mechanisms rather than of a summary.

This note is wrong if the falsification test in section 2 shows the power-mean ordering is no
better than a plain mean on the CON-COH corpus. In that case section 2 is withdrawn and the
composition-rule candidate comes out of `typed-evaluation-verdicts.md`, leaving sections 3
and 4 standing on their own.
