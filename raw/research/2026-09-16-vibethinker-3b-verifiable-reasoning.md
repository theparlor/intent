---
title: "VibeThinker-3B: Exploring the Frontier of Verifiable Reasoning in Small Language Models (arXiv 2606.16140v1)"
type: academic-paper
maturity: draft
status: terminal
confidentiality: internal
reusability: adaptable
created: 2026-09-16
source: "https://arxiv.org/abs/2606.16140"
source_html: "https://arxiv.org/html/2606.16140v1"
model_card: "https://huggingface.co/WeiboAI/VibeThinker-3B"
code: "https://github.com/WeiboAI/VibeThinker"
secondary_source_superseded: "https://www.marktechpost.com/2026/06/19/vibethinker-3b-a-3b-dense-reasoning-model-built-on-qwen2-5-coder-3b-with-the-spectrum-to-signal-post-training-pipeline/"
captured: 2026-09-16
origin: agent
confidence: 0.9
extraction_depth: high
authors: Sen Xu, Shixi Liu, Wei Wang, Jixin Min, Yingwei Dai, Zhibin Yin, Yirong Chen, Xin Zhou, Junlin Zhang
published: 2026-06-15 (arXiv v1, cs.AI / cs.CL)
lineage:
  - https://github.com/theparlor/intake/issues/18
relevant_to:
  - knowledge/design-rationale/RAT-004-verifier-at-the-seam.md
  - spec/typed-evaluation-verdicts.md
  - spec/autonomy-gate-matrix.md
  - spec/SPEC-INTENT-SEAM-DECOMPOSITION-001.md
---
# VibeThinker-3B, primary source record

## Plain language first

A nine-author team at Sina Weibo took a small, ordinary 3 billion parameter model and, using
only post-training (no new pretraining), pushed it to the same competition-math and coding
scores as models two to three hundred times its size. Two things in how they did it matter to
Brien's own work, and neither is about model size.

The first: they get a large part of that result at answer time, not training time, by having
the model write out 32 attempts, break each attempt into five checkable claims, grade each
claim pass or fail, and then rank the attempts by a score that punishes any failed claim
hard. That adds zero parameters. It is a comparator sitting at a seam, which is exactly the
shape Intent already specifies, and it hands over the one thing Intent's version does not
have: the arithmetic for combining several pass/fail judgments into one number.

The second: the paper states plainly why this only works on problems where an answer can be
checked, and it states it as an economics claim rather than a prohibition. Checkable
reasoning compresses into a small core. Open-domain knowledge does not; it needs breadth of
parameters. Translated out of model training and into Brien's autonomy ladder, that is a
statement about the price of autonomy at a seam, not a ban on autonomy where no verifier
exists.

This file is the verified record of what the paper actually says. The mapping onto Intent
and Coherence Engineering IP, and the rulings about what to adopt and what to reject, live
in [RAT-004](../../knowledge/design-rationale/RAT-004-verifier-at-the-seam.md).

**Why this file exists at all:** intake issue
[#18](https://github.com/theparlor/intake/issues/18) captured this analysis in June 2026 from
a MarkTechPost write-up, with the technical report explicitly marked unread. The mechanism
claims and one number in that capture are wrong. Section 5 below is the claim-by-claim diff.

---

## 1. Citation and provenance

| Field | Value |
|---|---|
| Title | VibeThinker-3B: Exploring the Frontier of Verifiable Reasoning in Small Language Models |
| Authors | Sen Xu, Shixi Liu, Wei Wang, Jixin Min, Yingwei Dai, Zhibin Yin, Yirong Chen, Xin Zhou, Junlin Zhang |
| arXiv | 2606.16140v1, submitted 2026-06-15, cs.AI and cs.CL |
| Abstract page | https://arxiv.org/abs/2606.16140 |
| HTML rendering read | https://arxiv.org/html/2606.16140v1 |
| Weights | https://huggingface.co/WeiboAI/VibeThinker-3B, MIT license per the model card |
| Code | https://github.com/WeiboAI/VibeThinker |
| Predecessor | VibeThinker-1.5B (the paper describes itself as extending that work) |

**Base model, unresolved.** The technical report text says the model is built on
"Qwen2.5-Coder-3B base". The HuggingFace model card's `base_model` metadata says
`Qwen/Qwen2.5-3B` (the non-Coder variant). UNRESOLVED: the two primary surfaces disagree and
nothing read here settles it. The secondary write-up that intake #18 was built from asserted
Coder without noting the conflict.

**License, resolved.** The weights are MIT per the model card. An automated read of the arXiv
HTML returned "CC Zero"; that is the arXiv submission license for the paper document, not a
license on the weights. Intake #18's "MIT-licensed" claim stands.

---

## 2. The post-training pipeline, in the paper's own order

No pretraining. Eight sequential post-training stages on an off-the-shelf 3B base.

1. **SFT stage 1, broad coverage.** All quality-filtered reasoning data, aimed at maximizing
   task diversity and exposure to reasoning patterns.
2. **SFT stage 2, hard-sample focus.** Continued training on harder samples: reasoning traces
   longer than 5K tokens, filtered by error rate above 0.75.
3. **Math RL** using MGPO.
4. **Code RL**, aimed at executable logic rigor and boundary-case handling.
5. **STEM RL**, generalizing to multidisciplinary scientific problems.
6. **Long2Short Math RL**, optimizing token efficiency among correct trajectories while
   holding validation-set accuracy.
7. **Offline self-distillation**, folding high-quality trajectories from the prior stages
   back into one student by supervised fine-tuning.
8. **Instruct RL**, restoring strict adherence to constraint-heavy user instructions.

**Context handling.** RL is run directly at a single 64K long-context window. Progressive
context expansion was tried and rejected: the paper states that a high-truncation early stage
"weakens the model's long-thinking capability".

---

## 3. The four mechanisms, verified against the source math

### 3.1 CLR, Claim-Level Reliability Assessment (test-time, zero added parameters)

Two-stage procedure, using the same sampling parameters as standard evaluation.

- Generate `K = 32` candidate trajectories per problem.
- From each trajectory extract `M = 5` decision-relevant claims plus the final answer.
- Produce a binary verdict `v[k,m]` in {0, 1} per claim. The model is its own verifier.
- Trajectory reliability:

  ```
  r_k = ( (1/M) * sum_{m=1..M} v[k,m] ) ^ M
  ```

- Cluster candidate answers by equivalence, then select the cluster maximizing the
  reliability-weighted aggregate:

  ```
  Score(G) = sum over { k : y_k in G } of r_k
  ```

- Run the whole flow independently and average Pass@1. The HTML rendering reads: "we
  independently execute this entire test-time scaling flow 88 times and report the averaged
  Pass@1 performance as '+ CLR' in Table 2."

**What the aggregation function actually does.** It is the arithmetic mean of the verdicts
raised to the power of the claim count. It is not a minimum, not a strict AND, and not an
average. With `M = 5`:

| Claims passing | Mean of verdicts | `r_k` | What a strict AND would give | What a plain mean would give |
|---|---|---|---|---|
| 5 of 5 | 1.00 | 1.000 | 1.0 | 1.00 |
| 4 of 5 | 0.80 | 0.328 | 0.0 | 0.80 |
| 3 of 5 | 0.60 | 0.078 | 0.0 | 0.60 |
| 2 of 5 | 0.40 | 0.010 | 0.0 | 0.40 |
| 0 of 5 | 0.00 | 0.000 | 0.0 | 0.00 |

Two properties are load-bearing and neither is captured by "one weak claim collapses the
trajectory":

1. **A single failure costs about two thirds of the weight, not all of it.** The function
   stays strictly positive until every claim fails, so trajectories that are all imperfect
   can still be ranked against each other. A strict AND would zero the entire candidate set
   on any hard problem and destroy the ranking, which is the whole output of the method.
2. **Strictness scales with how much you check.** The exponent is `M`, the number of claims
   extracted. Check more claims and the same pass fraction yields a lower score. Tolerance
   is not a free parameter here; it is a consequence of the audit's own breadth.

### 3.2 SSP, the Spectrum-to-Signal Principle

The paper's statement: "the SFT phase is tasked with constructing a solution spectrum that
covers diverse valid methods, offering a broader candidate solution space for subsequent RL."
Broad coverage of valid approaches first (the Spectrum), then focused amplification of
correct reasoning against a verifier (the Signal).

### 3.3 Diversity-Exploring Distillation

This is a **checkpoint selection and merge rule**, not a diversity penalty running through
training. The paper: the SFT phase "does not aim for optimal imitation along a single
solution path, but instead prioritizes the construction of a broader candidate solution
space, providing a richer exploration basis for subsequent RL."

Operationally: evaluate intermediate checkpoints on domain-specific probing sets; for each
domain, the checkpoint that yields **more valid solutions** becomes that domain's specialist,
rather than the checkpoint with the lowest validation loss; then merge the domain specialists
at the parameter level.

The borrowable idea is the selection criterion. The thing selected on is coverage of the
solution space, not proximity to a single reference answer.

### 3.4 MGPO, MaxEnt-Guided Policy Optimization

Empirical group accuracy for a prompt `q` over `G` rollouts:

```
p(q) = (1/G) * sum_{i=1..G} indicator(r_i = 1)
```

Entropy-based prompt weight:

```
w(q) = exp( -gamma * D_ME( p(q) || p_0 ) ),  with p_0 = 0.5, gamma > 0
```

`D_ME` measures how far the empirical correctness `p(q)` sits from the maximum-entropy point
0.5. Prompts where correct and incorrect rollouts coexist, that is, prompts at the model's
current capability boundary, get the highest weight. The formulation section does not state a
numeric value for `gamma`.

Objective:

```
J_MGPO(theta) = E_{q, {y_i}} [ (1/G) sum_i (1/|y_i|) sum_t
    min( rho_{i,t}(theta) * w(q) * A_i,
         clip(rho_{i,t}(theta), -eps, +eps) * w(q) * A_i ) ]
```

### 3.5 Long2Short Math RL

Among the correct trajectories `C` only, define a brevity score from response length `L_i`:

```
s_i = 1 / L_i
```

Redistribute reward:

```
r'_i = r_i + lambda * (s_i - s_bar) / max_{j in C} | s_j - s_bar | ,  for i in C
```

with `lambda = 0.2` controlling maximum redistribution magnitude. The redistribution is
zero-sum by construction: `sum_{i in C} (r'_i - r_i) = 0`, so the group-level baseline reward
is preserved. Shorter correct answers are rewarded at the direct expense of longer correct
answers, and accuracy is not traded for brevity because only correct trajectories participate.

---

## 4. Results (Table 2 of the paper, as rendered in the HTML)

VibeThinker-3B, 3B parameters, and the comparison cluster:

| Model | Params | AIME25 | AIME26 | HMMT25 | BruMO25 | IMO-Ans | LCBv6 | OJBench | GPQA-D | IFEval | IFBench |
|---|---|---|---|---|---|---|---|---|---|---|---|
| **VibeThinker-3B** | **3B** | 91.4 | 94.3 | 89.3 | 93.8 | 76.4 | 80.2 | 38.6 | 70.2 | 93.4 | 74.5 |
| **VibeThinker-3B + CLR** | **3B** | 96.7 | 97.1 | 95.4 | 99.2 | 80.6 | n/a | n/a | 72.9 | n/a | n/a |
| GPT-OSS (high) | 120B | 92.5 | 93.2 | 90.0 | 92.5 | 75.6 | 81.9 | 41.5 | 80.1 | 89.5 | 69.5 |
| DeepSeek V3.2 | 671B | 93.1 | 94.2 | 90.2 | 96.7 | 78.3 | 80.8 | 48.4 | 82.4 | 92.6 | 60.7 |
| GLM-5 | 744B | 96.7 | 95.8 | 97.9 | n/a | 82.5 | 85.5 | 55.0 | 86.0 | 92.6 | 76.5 |
| Kimi K2.5 | 1T | 96.1 | 93.3 | 95.4 | 98.3 | 81.8 | 85.0 | 54.7 | 87.6 | 93.9 | 70.0 |
| Gemini 3 Pro | n/a | 96.0 | 91.7 | 97.5 | 98.3 | 83.1 | 87.4 | 58.8 | 91.9 | 91.9 | 70.4 |
| Qwen3.5-397B-A17B | 397B | n/a | 91.3 | 94.8 | n/a | 80.9 | 83.6 | n/a | 88.4 | 92.6 | 76.5 |

The CLR row carries values only on the six benchmarks where it was run. The blanks are blanks
in the source, not omissions here.

**The measured value of the test-time loop alone**, with zero added parameters:

| Benchmark | Base | + CLR | Delta |
|---|---|---|---|
| AIME25 | 91.4 | 96.7 | +5.3 |
| AIME26 | 94.3 | 97.1 | +2.8 |
| HMMT25 | 89.3 | 95.4 | +6.1 |
| BruMO25 | 93.8 | 99.2 | +5.4 |
| IMO-AnswerBench | 76.4 | 80.6 | +4.2 |
| GPQA-Diamond | 70.2 | 72.9 | +2.7 |

**Where the small model does not reach.** GPQA-Diamond at 70.2 against 80.1 to 91.9 for the
large models, and OJBench at 38.6 against 41.5 to 58.8. The paper names this directly: "The
gap to the strongest large models is more visible on broad knowledge-heavy evaluation,
especially GPQA-Diamond, than on competition mathematics or executable coding."

**Out of distribution.** The abstract states a 96.1 percent acceptance rate on recent unseen
LeetCode contests. Intake #18 carried a 123-of-128 first-attempt breakdown from the secondary
source; 123/128 is 96.09 percent, arithmetically consistent, but the breakdown itself was not
re-verified against the paper in this pass.

---

## 5. The Parametric Compression-Coverage Hypothesis

This is the paper's own framing of the "specialist by design" idea, and it is materially
different from a prohibition. Quoted from the source:

> "Foundational model capabilities differ ... in the structural form of their parameter
> demands. They can be broadly divided into parameter-dense capabilities and
> parameter-expansive capabilities. Verifiable reasoning exemplifies the former: its core
> challenge lies not in memorizing vast open-domain facts, but in performing search,
> constraint satisfaction, error correction, and multi-step composition within a structured
> solution space. Consequently, this class can be highly compressed into a compact and
> reusable reasoning core. In contrast, knowledge-intensive and general-purpose abilities
> align more closely with the latter."

And the paper's own hedge on the headline: "The main finding is not that a 3B model has fully
replaced leading general-purpose models, but that a small model can reach first-tier
performance on many verifiable reasoning tasks."

This is a claim about what a capability costs in parameters, not a claim that unverifiable
work must be forbidden.

---

## 6. Deployment and scope facts (model card, not the paper)

The paper contains no deployment guidance. These come from the HuggingFace model card:

- BF16 tensors. 3B parameters at BF16 is approximately 6 GB by arithmetic; the card does not
  state a file size.
- `transformers >= 4.54.0`.
- Recommended inference: `vLLM == 0.10.1`, `SGLang >= 0.4.9.post6`.
- Generation: `max_new_tokens: 102400`, `temperature: 1.0`, `top_p: 0.95`, `top_k` unset.
  Reasoning traces are long; a small token budget truncates answers.
- **Scope limitation, stated by the authors:** the model "was not trained on tool-calling or
  agent-based programming data", and they advise against using it for function calling, API
  orchestration, or autonomous coding agents. Intended use is competitive-style math, coding,
  and STEM reasoning where answers are verifiable.

That last bullet is new information relative to intake #18 and it decides Thread B. See
RAT-004 section 5.

---

## 7. Claim-by-claim diff against intake issue #18

Intake #18 was written from a secondary source with the technical report marked unread. This
table records what survived and what did not.

| # | Claim as captured in intake #18 | Verdict against the primary source |
|---|---|---|
| 1 | 3B dense, post-trained via SFT plus RL plus self-distillation, no pretraining | **Confirmed.** The pipeline is eight stages, not four; Instruct RL and Long2Short are separate stages. |
| 2 | Built on Qwen2.5-Coder-3B | **Unresolved.** Paper text says Qwen2.5-Coder-3B; model card metadata says Qwen/Qwen2.5-3B. |
| 3 | MIT licensed | **Confirmed** on the model card. |
| 4 | CLR: K=32, M=5, binary verdict per claim, equivalence clustering, reliability-weighted winner, zero added parameters | **Confirmed**, all of it. |
| 5 | CLR aggregation is "nonlinear, saturating, dominating: a single weak claim collapses the whole trajectory's reliability" | **Corrected.** The function is `(mean of verdicts)^M`. One failure of five leaves 0.328, not zero. It collapses to zero only when every claim fails. The capture's proposed reading, that constraint-seam gain drives "toward zero regardless of how many descriptive claims passed", is not what the paper does and would break the method. |
| 6 | Full CLR flow run 8 times, averaged | **Corrected to 88** in the arXiv HTML rendering, stated twice in consistent sentences. Flagged: 8 is a plausible reading of a rendering artifact, but nothing read here supports 8, and the primary text says 88. |
| 7 | Benchmark numbers (AIME26 94.3 to 97.1, HMMT25 89.3 to 95.4, IMO-Ans 76.4 to 80.6, LCBv6 80.2, GPQA-D 70.2 to 72.9, OJBench 38.6, BruMO25 93.8 to 99.2, IFEval 93.4, IFBench 74.5) | **All confirmed.** The capture missed AIME25 (91.4 to 96.7 with CLR), which is the single largest CLR gain after HMMT25. |
| 8 | Comparison cluster figures for GPT-OSS 120B, DeepSeek V3.2, GLM-5, Kimi K2.5 | **Confirmed.** |
| 9 | Diversity-Exploring Distillation "preserves multiple valid solution paths through both SFT stages and RL" | **Corrected.** It is a checkpoint selection and parameter-level merge rule: pick the checkpoint with more valid solutions rather than lowest validation loss, per domain, then merge the domain specialists. It does not run through RL. |
| 10 | MGPO maps to lambda, the coefficient of bravery | **Interpretation, and the symbol is wrong.** MGPO's boundary weight uses `gamma` in `w(q) = exp(-gamma * D_ME(p(q) || 0.5))`. The only `lambda` in the paper is Long2Short's reward-redistribution magnitude, fixed at 0.2, which is a different quantity entirely. The conceptual rhyme (spend learning effort at the capability boundary) survives; the claim of a shared parameter does not. |
| 11 | Long2Short rewards shorter correct answers, group mean unchanged | **Confirmed**, with the exact zero-sum formula and `lambda = 0.2`. |
| 12 | Single 64K RL window; progressive context expansion dropped because high-truncation warm-up hurt long reasoning | **Confirmed**, including the stated reason. |
| 13 | "Specialist by design, scoped only to verifier-confirmable tasks" | **Reframed by the source.** The paper states the Parametric Compression-Coverage Hypothesis: verifiable reasoning is parameter-dense and compresses; open-domain knowledge is parameter-expansive and needs coverage. That is a cost claim, not a scope prohibition. See section 5. |
| 14 | Deployment facts (6 GB BF16, transformers>=4.54.0, vLLM==0.10.1, SGLang>=0.4.9.post6, max_new_tokens 102400) | **Confirmed from the model card**, not from the paper. The 6 GB figure is arithmetic, not a stated file size. |
| 15 | Internal reference to "issue #13, dual-modality seam topology and descriptive vs constraint seam typing" | **Unresolvable as written.** theparlor/intake issue #13 is a New Stack article about Block's AI coding agents. The seam-typing material the capture meant is in this tree at `/Users/brien/Workspaces/Core/frameworks/intent/spec/SPEC-INTENT-SEAM-DECOMPOSITION-001.md` and `/Users/brien/Workspaces/Core/products/_intake/2026-07-07-three-plane-reconciliation/` (which is intake issue #27, filed 2026-07-07, after this capture). Corrected pointers used in RAT-004. |

---

## 8. What this file does not cover

- The VibeThinker-1.5B predecessor paper was not read.
- The GitHub repository code was not read; only the model card.
- The 123-of-128 LeetCode breakdown was not re-verified line by line against the paper.
- No numeric value for MGPO's `gamma` was found in the formulation section; it may appear in
  an appendix or hyperparameter table not surfaced by the targeted reads.
