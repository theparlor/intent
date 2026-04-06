---
id: DOM-001
type: domain-model
created: 2026-04-05
updated: 2026-04-05
depth_score: 2
depth_signals:
  file_size_kb: 2.9
  content_chars: 2524
  entity_count: 0
  slide_count: 0
  sheet_count: 0
  topic_count: 0
  has_summary: 0
vocab_density: 0.40
name: Intent Work Ontology
scope: bounded-context
confidence: 0.80
origin: human
sources:
  - raw/research/2026-03-28-intent-methodology-v1.md
  - raw/research/2026-04-05-three-layer-architecture-formalized.md
---
# Domain Model: Intent Work Ontology

## Definition

The seven-level hierarchy that replaces Agile's story/epic/initiative stack. Each level has a clear owner, clear transitions, and clear events.

## Elements

| Term | Definition | Layer |
|------|-----------|-------|
| **Signal** | An observation that creates a gap between the world as it is and the world as it should be. Immutable once captured. | Layer 2 (Notice) |
| **Intent** | A promoted cluster of signals with enough coherence to warrant action. "What needs to change." | Layer 2 (Notice→Spec) |
| **Spec** | The unit of work: Intent + Shape + Contract. "The shortest document that makes the agent dangerous." | Layer 2→3 (Spec) |
| **Contract** | How we know it's done. Observable outcomes, not task checkboxes. A smoke test the agent can run. | Layer 2→3 (Spec) |
| **Atom** | The smallest independently deployable unit of work. Agent executes against a spec to produce an atom. | Layer 3 (Execute) |
| **Capability** | A composed set of atoms that delivers a coherent user-facing function. | Layer 3 (Product) |
| **Feature / Product** | The highest level — what users experience. Composed of capabilities. | Layer 3 (Product) |

## Relationships

```
Signal ──(clusters into)──→ Intent ──(shaped into)──→ Spec ──(verified by)──→ Contract
                                                        │
                                                        ▼
                                                   Agent Execute → Atom → Capability → Feature → Product
                                                        │
                                                        ▼
                                                    Observe → Events
                                                        │
                                       ┌────────────────┴────────────────┐
                                       ▼                                 ▼
                              Knowledge update (Flow 5)              Spec update (Flow 6)
                              (double-loop)                     (single-loop)
```

## Boundaries

**In scope:** The lifecycle of work from observation to running code.
**Out of scope:** Organizational structure, team topology, hiring, budgeting. Intent assumes an empowered team (Cagan) but doesn't prescribe team shape.

**Adjacent bounded contexts:**
- [[DOM-002-knowledge-ontology]] — The artifact types in Layer 1 (personas, journeys, DDRs, themes)
- Signal trust framework — The scoring model that gates autonomy levels
