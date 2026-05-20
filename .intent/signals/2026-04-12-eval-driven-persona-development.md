---
id: SIG-038
title: "Eval-driven development is the missing governance layer for persona quality"
timestamp: 2026-04-12T16:15:00Z
source: cowork-session
author: brien
confidence: 0.9
trust: 0.9
autonomy_level: L3
status: active
severity: high
cluster: persona-fidelity
related_signals: [SIG-036, SIG-037, SIG-039]
related_intents: [INT-005, INT-016]
referenced_by:
  - "SPEC-001 (entity schema — depth_score field)"
  - "SIG-036 (multi-model adversarial synthesis — depth score validation)"
---

# SIG-038: Eval-Driven Development Is the Missing Governance Layer for Persona Quality

## What was noticed

There is currently no automated quality gate between "corpus was fetched" and "persona is usable." The depth score in SPEC-001's entity schema is computed by the synthesis agent itself — the same agent that wrote the persona also grades it. This is the LLM equivalent of a student grading their own exam.

The problem is not that the synthesis agent is dishonest. The problem is that it has no mechanism to detect its own failure modes:

- **Sycophantic voice synthesis** — the model produces a voice description that sounds like what Brien expects rather than what the source material shows. Without an independent check, the persona sounds confident and specific but may be unfaithful to the actual person's communication patterns.

- **Confabulated reasoning chains** — the model attributes a mental model to a persona based on pattern-matching from training data rather than from the corpus. The persona file says "Torres uses the Opportunity Solution Tree" because the model knows that from pre-training, not because it found it in the fetched corpus. Without traceability verification, the attribution is indistinguishable from hallucination.

- **Depth score inflation** — a persona that has been through one synthesis pass on thin material gets scored at depth 8 because the model filled gaps from training knowledge. The depth score should reflect corpus coverage, not model knowledge. Without structural checks on corpus-to-claim mapping, the score is meaningless.

- **Vocabulary contamination** — the model inserts its own characteristic phrases into the vocabulary fingerprint. "Let's unpack this" and "it's worth noting that" are Claude-isms, not persona-isms. Without vocabulary verification against actual quotes, the fingerprint is the model's voice, not the person's.

## Three eval layers needed

### Layer 1: Structural Evals (automated, every synthesis pass)

These are mechanical checks that can run without any model involvement:

- YAML parse check — does the entity file validate?
- Required fields populated — voice, mental_models, stances, frustration_triggers at minimum
- sources.yaml URLs resolve — are the referenced sources actually reachable?
- Processing log documents what was attempted vs. what succeeded
- Corpus file size > 0 for all referenced files
- Depth score has justification text, not just a number
- Claim count vs. source count ratio — a persona with 40 claims and 3 sources is suspicious

### Layer 2: Content Evals (semi-automated, post-synthesis)

These require a model but can run without human involvement:

- **Distinctiveness test** — give two adjacent personas (e.g., Torres and Cagan) the same question. Verify they answer differently. If they converge, at least one is underspecified.
- **Traceability test** — every claim in the synthesis must trace to a specific source URL. Claims that can't be traced are flagged as potentially confabulated.
- **Vocabulary verification** — terms in vocabulary_fingerprint must appear in actual quotes from the corpus, not just in the synthesis text.
- **Attribution accuracy** — ideas credited to the persona must be verified against source material. "Torres popularized the Opportunity Solution Tree" should have a source link.
- **Self-correction inventory** — documented "I used to think X, now I think Y" statements must be verified in source material. These are high-signal and easy to confabulate.
- **Reasoning chain completeness** — can the persona approach a novel problem using their frameworks (not just recite the frameworks)? Test by posing a scenario outside the corpus domain.

### Layer 3: Fidelity Evals (human-in-loop, periodic)

These require Brien's judgment:

- **Would-they-say-this test** — Brien reads a persona response and scores: "Would [author] actually say this?" Scale: definitely yes / probably yes / uncertain / probably not / definitely not.
- **Claim spot-check** — Brien picks 3-5 claims and checks them against sources. How many hold up?
- **Hedging accuracy** — does the persona hedge on topics where the corpus is thin? A persona that's confidently opinionated about everything is suspicious.
- **Voice register accuracy** — does it sound like the person in the right register? Book voice is different from podcast voice is different from tweet voice. The synthesis should capture register variation, not flatten it.

## Why this matters now

Without evals, the persona system has no feedback loop. It can only accumulate content — it can never improve quality. The bandit testing framework (SIG-039) needs a reward signal, and that reward signal IS the eval score. Without evals, bandits have nothing to optimize against. Without bandits, evals are just documentation of problems with no mechanism for systematic improvement.

The eval layer is the thing that turns the persona system from "a collection of files" into "a system that gets better."
