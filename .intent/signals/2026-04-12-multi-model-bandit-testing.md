---
id: SIG-039
title: "Multi-armed bandit testing across model-pipeline configurations can optimize persona compilation quality"
timestamp: 2026-04-12T16:30:00Z
source: cowork-session
author: brien
confidence: 0.85
trust: 0.7
autonomy_level: L1
status: active
severity: medium
cluster: persona-fidelity
related_signals: [SIG-036, SIG-037, SIG-038]
related_intents: [INT-005, INT-016]
referenced_by:
  - "SIG-036 (multi-model adversarial synthesis — the quality hypothesis)"
  - "LLM landscape April 2026 — GLM-5.1, Qwen, Opus, Sonnet all viable"
---

# SIG-039: Multi-Armed Bandit Testing for Persona Pipeline Optimization

## What was noticed

The persona synthesis pipeline currently has a hardcoded configuration: fetch with whatever's available, synthesize with Opus, score with Opus. This is the "default arm" in bandit terms — the configuration we always pull. But we have no evidence that this is the optimal configuration, and the landscape of available models is changing fast enough that the optimal configuration probably shifts over time.

The multi-armed bandit framing makes this explicit:

**Arms** = model-pipeline configurations. Each arm is a complete fetch→synthesize→score pipeline with specific models at each stage:
- Arm A: Sonnet-fetch + Opus-synthesis (current default)
- Arm B: GLM-5.1-fetch + Opus-synthesis (cheaper fetching, same quality synthesis)
- Arm C: GLM-5.1-fetch + GLM-5.1-synthesis (fully cheap — how much quality do we lose?)
- Arm D: Sonnet-fetch + Sonnet-synthesis (mid-tier throughout)
- Arm E: Opus-fetch + Opus-synthesis (maximum quality — is it worth the cost?)
- Arm F: Any-fetch + dual-model-adversarial-synthesis (SIG-036's approach — two frontier models, disagreements flagged)

**Reward signal** = persona fidelity, measured through the eval layer (SIG-038):
- Agreement rate across models (Layer 2 content eval)
- Prediction accuracy on held-out material (does the persona correctly predict stances found in sources not included in the synthesis corpus?)
- Human validation score (Layer 3 fidelity eval — Brien's "would they actually say this?" score)
- Cost per quality unit (fidelity score / API cost)

**Explore** = occasionally route a synthesis through a non-default pipeline configuration. When a persona is being freshened or a new person is being ingested, randomly (with epsilon probability) choose a non-default arm.

**Exploit** = converge on the best configuration per persona TYPE, not globally. The key insight is that different persona types likely have different optimal configurations:
- **Prolific bloggers** (Huryn, Cagan) — massive corpus, many sources. Cheap fetching is fine because the signal-to-noise ratio is high. Synthesis quality matters more.
- **Sparse-but-dense thinkers** (Singer, Wardley) — small corpus, every sentence matters. Extraction quality at the fetch stage is critical. Frontier model fetching may be worth the cost.
- **Historical figures or academics** — source material is formal, well-structured. Cheap models may handle extraction well. Synthesis needs to read between the lines.
- **Practitioners who mostly speak** (podcasters, conference speakers) — transcription quality is the bottleneck, not model quality. MacWhisper output quality may matter more than which LLM synthesizes it.

## Implementation approach

Each pipeline configuration writes to a separate synthesis file:
```
corpus/[name]/
├── synthesis-opus-default.md        # Arm A output
├── synthesis-glm-opus.md            # Arm B output
├── synthesis-adversarial.md         # Arm F output
└── eval-reports/
    ├── arm-a-eval-2026-04-12.yaml   # Eval scores for Arm A
    ├── arm-b-eval-2026-04-12.yaml   # Eval scores for Arm B
    └── comparison-2026-04-12.md     # Cross-arm comparison
```

A comparison agent reads all available synthesis files for a persona, runs the eval layer against each, and produces a ranked comparison. Over time, the bandit algorithm (Thompson sampling or UCB1) shifts probability mass toward the best-performing arm for each persona type.

## Why L1 autonomy

This is L1 (agent assists, human decides) because:
- The bandit infrastructure doesn't exist yet — it needs to be designed and built
- The explore/exploit tradeoff involves cost decisions (running multiple pipelines costs real API dollars)
- The persona type classification is Brien's judgment call for now
- The reward signal (eval scores) requires the eval layer from SIG-038 to exist first

This signal should progress to L2 once the eval layer is operational and Brien has established the initial persona type taxonomy.

## Connection to SIG-036

SIG-036 identified multi-model adversarial synthesis as a quality mechanism. This signal extends that insight: adversarial synthesis is one arm in a larger optimization framework. The bandit approach lets us systematically compare adversarial synthesis against simpler (cheaper) alternatives and determine when the added cost is justified.
