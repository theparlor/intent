---
id: SIG-037
title: "Persona system needs five product capabilities: discovery, sourcing, model-agnostic synthesis, bandit testing, and eval-driven development"
timestamp: 2026-04-12T16:00:00Z
source: cowork-session
author: brien
confidence: 0.9
trust: 0.9
autonomy_level: L3
status: active
severity: high
cluster: persona-fidelity
related_signals: [SIG-036, SIG-038, SIG-039]
related_intents: [INT-005, INT-016]
referenced_by:
  - "SPEC-001 (entity schema)"
  - "SPEC-002 (intake pipeline)"
  - "SIG-036 (multi-model adversarial synthesis)"
---

# SIG-037: Persona System Needs Five Product Capabilities

## What was noticed

The persona system is being developed as a collection of enrichment tasks — fetch some content, run a synthesis, store the result. But the gaps Brien identified across multiple sessions reveal something more fundamental: this is a product with five distinct capability areas, each with its own maturity curve, quality model, and autonomy progression. Treating it as "just more Knowledge Engine operations" produces the same mistake Agile teams make when they treat infrastructure as "just more stories" — the systemic investment never happens because no individual task justifies it.

The five capabilities, in dependency order:

1. **Discovery** — Finding who matters. Citation graph crawling, dissent detection, tangential domain exploration. Currently Brien-directed (L0); needs to progress toward agent-suggested (L1) and eventually agent-discovered-with-approval (L2-L3).

2. **Content Sourcing** — Getting their actual voice. Web fetch, podcast transcription, audiobook pipelines, YouTube captions, academic papers, community content. The "unguarded voice" hierarchy (GitHub > podcasts > workshops > interviews > blog > book) emerged from Opus synthesis and fundamentally changes sourcing priorities.

3. **Model-Agnostic Synthesis** — Separating mechanical fetching from subjective interpretation. Local/cheap models handle conversion to clean markdown. Frontier models handle voice pattern recognition, reasoning chain extraction, and attribution. Raw markdown always preserved for re-interpretation as models improve.

4. **Multi-Armed Bandit Testing** — Pipeline configurations as arms, fidelity metrics as rewards. Different persona types (prolific bloggers vs. sparse-but-dense thinkers vs. historical figures) may have different optimal pipeline configurations. Without systematic testing, we'd never know.

5. **Eval-Driven Development** — The governance layer. Three tiers of evaluation (structural, content, fidelity) that gate depth score advancement. Without this, the system produces confident-sounding personas with no mechanism to detect whether they're faithful to the source material.

## Why product framing changes the development approach

When you treat these as enrichment tasks, each one gets built in isolation — a fetch script here, a synthesis prompt there, a manual review when Brien has time. The interactions between them are accidental. When you treat them as a product:

- **Discovery feeds Sourcing** — every synthesis produces "discover these people" signals, creating a self-expanding graph.
- **Sourcing feeds Synthesis** — the "unguarded voice" hierarchy determines which sources get priority processing, not just which get fetched first.
- **Synthesis feeds Bandit Testing** — every synthesis pass is an experiment that can be compared against alternative pipeline configurations.
- **Bandit Testing feeds Evals** — reward signals come from the eval layer, not from Brien's subjective impression.
- **Evals feed Discovery** — low fidelity scores on a persona trigger sourcing of additional material, which may reveal new people worth discovering.

The loop is the product. Breaking any link collapses it back to disconnected enrichment tasks.

## Connection to existing architecture

This signal supersedes the implicit assumption in SPEC-002 (intake pipeline) that the pipeline is linear and complete. SPEC-002's six stages (Identify → Harvest → Assess → Render → Connect → Schedule) are a good starting point for Capability 2 (Sourcing) and the first pass of Capability 3 (Synthesis), but they don't account for iterative improvement, multi-model comparison, or eval gating. The persona product spec needs to wrap SPEC-002 in a larger system that includes feedback loops.
