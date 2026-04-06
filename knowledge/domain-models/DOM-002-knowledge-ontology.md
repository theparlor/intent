---
id: DOM-002
type: domain-model
created: 2026-04-05
updated: 2026-04-05
depth_score: 2
depth_signals:
  file_size_kb: 2.3
  content_chars: 1977
  entity_count: 0
  slide_count: 0
  sheet_count: 0
  topic_count: 0
  has_summary: 0
vocab_density: 0.51
name: Domain Knowledge Ontology
scope: bounded-context
confidence: 0.75
origin: agent
sources:
  - raw/research/2026-04-02-karpathy-llm-knowledge-bases.md
  - raw/research/2026-04-05-three-layer-architecture-formalized.md
---
# Domain Model: Domain Knowledge Ontology

## Definition

The artifact types that compose Layer 1's compiled domain knowledge. These are the "topic types" that the knowledge base self-organizes around — analogous to Karpathy's emergent page types (concept, entity, comparison) but formalized for product work.

## Elements

| Artifact | Prefix | Purpose | Confidence Source |
|----------|--------|---------|-------------------|
| **Persona** | PER | Who the users are, what they need, what frustrates them | Raw research (interviews, analytics) |
| **Journey Map** | JRN | How personas move through experiences, where pain occurs | Raw research + persona synthesis |
| **Design Decision Record** | DDR | What was decided, why, and how to validate it | Human judgment + domain synthesis |
| **Theme** | THM | Cross-cutting insights that emerge from multiple sources | Pattern recognition across research |
| **Domain Model** | DOM | Bounded contexts, glossaries, entity relationships, state machines | Structural analysis of the problem space |
| **Design Rationale** | RAT | Why-level reasoning connecting decisions to frameworks | Framework application + evidence |

## Relationships

```
Raw Source (raw/)
    ↓ (ingest)
Persona (PER) ←──→ Journey (JRN)
    ↓ pain points      ↓ stages
Design Decision (DDR) ←──→ Theme (THM)
    ↓ specs                  ↑
Spec (SPEC) ←── Domain Model (DOM)
    ↓                        ↑
Contract (CON)    Design Rationale (RAT)
```

Cross-references use `[[wikilinks]]`. Pain points are namespaced to personas (`PER-NNN/PP-NNN`). Confidence scores float between 0.0 and 1.0 based on evidence strength.

## Boundaries

**In scope:** Layer 1 artifact types and their relationships.
**Out of scope:** Layer 2 work artifacts (signals, intents, specs, contracts) — those are defined in [[DOM-001-work-ontology]]. Layer 3 code structure.

**The bridge:** DDRs link to Specs. Themes link to Signals. These are the coupling points between Layer 1 and Layers 2/3.
