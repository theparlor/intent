---
title: "Adopt three-layer architecture: Domain Knowledge Base + Transformation OS + Software Spec/Code"
id: DDR-002
type: decision
created: 2026-04-05
updated: 2026-04-05
thought_leaders:
  - john-kotter
  - mik-kersten
  - matthew-skelton
  - richard-rumelt
frameworks:
  - transformation-operating-system
depth_score: 4
depth_signals:
  file_size_kb: 3.8
  content_chars: 2780
  entity_count: 5
  slide_count: 0
  sheet_count: 0
  topic_count: 0
  has_summary: 0
vocab_density: 0.36
related_entities:
  - {pair: mik-kersten ↔ matthew-skelton, count: 17865, strength: 0.993}
  - {pair: mik-kersten ↔ john-kotter, count: 17862, strength: 0.991}
  - {pair: richard-rumelt ↔ mik-kersten, count: 17857, strength: 0.995}
  - {pair: john-kotter ↔ matthew-skelton, count: 17857, strength: 0.99}
  - {pair: richard-rumelt ↔ matthew-skelton, count: 17856, strength: 0.995}
status: accepted
confidence: 0.90
origin: human
addresses:
  - PER-001/PP-003
  - PER-001/PP-004
persona: PER-001
journey_stage: JRN-001#compile-understanding
sources:
  - raw/research/2026-04-05-three-layer-architecture-formalized.md
  - raw/research/2026-04-02-karpathy-llm-knowledge-bases.md
---
# DDR: Three-Layer Architecture

## Context

Intent's original architecture was a single loop (Notice→Spec→Execute→Observe) with work artifacts in `.intent/`. Karpathy's LLM Knowledge Base pattern revealed a missing layer: compiled domain understanding that feeds the loop but exists independently of it.

Brien's critical insight: Karpathy builds a knowledge artifact (output = understanding). Intent builds a generative engine (output = running software). The two are complementary, not competing.

## Decision

Adopt a three-layer architecture where each layer is independent but bidirectionally coupled:

1. **Layer 1 — Domain Knowledge Base** (`raw/` + `knowledge/`): Self-organizing compiled knowledge base from research. Personas, journeys, DDRs, themes, domain models. Governed by `knowledge-engine/AGENTS.md`.
2. **Layer 2 — Transformation Operating System** (`.intent/` + `spec/` methodology): The notice→spec→execute→observe loop. Domain-agnostic process.
3. **Layer 3 — Software Specification & Code** (generated specs + `src/`): What the system produces.

Six bidirectional data flows couple the layers, with Flow 5 (Observe → Knowledge, double-loop learning) being the most critical.

## Alternatives Considered

| Alternative | Pros | Cons | Why Rejected |
|-------------|------|------|-------------|
| Absorb knowledge base into .intent/ | Simpler directory structure | Conflates methodology artifacts with domain artifacts; can't use knowledge base independently | Violates separation of concerns |
| Knowledge base as external service | Scales better, accessible from anywhere | Adds infrastructure dependency, breaks files-as-universal-interface principle | Against Intent's design philosophy |
| Knowledge base as Layer 3 output only | Simpler data flow | Loses bidirectional coupling; knowledge base can't feed Notice or inform Spec authoring | Defeats the purpose |

## Consequences

**Positive:**
- Each layer can evolve independently (knowledge base can grow without changing the loop)
- Bidirectional coupling enables double-loop learning (Argyris)
- Karpathy's proven pattern provides Layer 1's technical substrate
- Maps cleanly to Beer's VSM (L1=S4+5, L2=S2+3, L3=S1)

**Negative:**
- More complex than a single-layer system
- Six data flows must be implemented and maintained
- New contributors must understand three layers, not one

## Validation Criteria

- [ ] A raw source ingested into Layer 1 produces knowledge artifacts that are queried during Layer 2 spec authoring
- [ ] An observation from Layer 3 execution updates a Layer 1 knowledge artifact (Flow 5 working)
- [ ] Lint on Layer 1 produces signals consumed by Layer 2 Notice (Flow 1 working)
