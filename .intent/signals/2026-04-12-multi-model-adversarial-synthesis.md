---
id: SIG-036
title: Multi-model adversarial synthesis eliminates sycophancy and bias in persona compilation and spec review
timestamp: 2026-04-12T14:00:00Z
source: cowork-session
author: brien
confidence: 0.85
trust: 0.7
autonomy_level: L2
status: active
cluster: persona-fidelity
referenced_by:
  - "Pawel Huryn, Cowork multi-LLM article"
  - "Dex Horthy, context engineering / harness engineering"
  - "LLM landscape April 2026 — multiple frontier models available"
---

# SIG-036: Multi-Model Adversarial Synthesis

## What was noticed

When rotating between LLM providers for persona enrichment and spec review, the different models' biases and blind spots can be used against each other to produce higher-fidelity output than any single model achieves alone.

## Three applications

### 1. Persona synthesis cross-validation
Run the same persona corpus through two different frontier models (e.g., Opus + GLM-5.1) for parallel synthesis. Where they agree on reasoning chains and voice registers, confidence is higher. Where they disagree, the delta IS the sycophancy signal — one model may be pattern-matching to what it thinks Brien wants to hear rather than what the source material actually shows.

### 2. Spec-shaping with genuine cognitive diversity
In the four-persona spec review (Triangle Architect, Diamond PM, Circle Design/QA, Circle-dot Agent), running different personas on different models produces genuine cognitive diversity — different priors about risk, value, and feasibility. Within a single model, the four personas share the same reasoning substrate and may converge toward sycophantic agreement. Across models, the disagreements are real.

### 3. Depth score validation
A persona scored at depth 11 by Opus should score similarly when evaluated by an independent model. If GLM-5.1 reads the same corpus and scores it at 8, the gap reveals areas where Opus's synthesis was optimistic rather than evidence-based.

## Architectural implication

The multi-model gateway (LiteLLM/OpenRouter) isn't just a cost optimization or rate limit workaround — it's a quality assurance mechanism. The Cowork plugin should be able to specify model-per-persona-role in the spec-shaping protocol, and the Opus synthesis pipeline should have an optional "adversarial verification" step where a second model reads the same corpus and produces an independent synthesis.

## Connection to depth scale v2.0

This mechanism directly enables depth 17 ("cross-persona validation — this persona's claims tested against adjacent personas") by extending the concept to cross-MODEL validation. A persona that survives adversarial synthesis across two frontier models has demonstrably lower sycophantic bias than one validated by a single model only.

## Triage, 2026-07-08

Disposition: still pending. No multi-model gateway (LiteLLM/OpenRouter) or dual-model adversarial synthesis step exists; Cast's persona pipeline remains single-model (Opus) per every synthesis file inspected across this pass. Same finding as the parallel org-design-tooling drain's RETRO-2026-04-12-final-adversarial-synthesis-SIG-038 disposition on this same date.
