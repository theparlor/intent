---
id: SIG-038
timestamp: 2026-04-06T18:00:00Z
source: conversation
confidence: 0.95
trust: 0.85
autonomy_level: L4
status: active
cluster: methodology-adoption
author: brien
related_intents: []
referenced_by: []
parent_signal: null
---
# Standard taxonomies index but never constrain open-world substance

## Observation

Brien established a governing design principle during persona system design: entities have two parallel layers that never collapse into each other. Structured fields (NAICS, O*NET, tier bands) are how you find, aggregate, and roll up. Freeform substance (voice, mental models, unique signal, stances, frustration triggers) is what you actually use when rendering.

The structured fields never replace, filter, or constrain the freeform substance. If an observation doesn't fit any structured field, it doesn't get discarded — it lives in substance and becomes findable through semantic search.

Brien specifically called out: "we want to retain the open world aspects that ensures we do not skip or dilute or lose the actual unique material that Opus is capable of lensing in real time."

## Implication

This is a design constraint that applies to ALL entity schemas in the system, not just personas:
- Knowledge artifacts: structured metadata (type, domain, confidence) indexes the content; the content itself is unconstrained
- Archetypes: structured dimensions (role, industry, tier) define the query; the synthesis is freeform
- Contribution: structured dimension tags control what flows upward; the actual contributed content is open-world

Every entity model must have both an `index` block (standards-backed, machine-queryable) and a `substance` block (Opus-quality, never truncated to fit a field).

## Design Constraint

- No taxonomy gate: if an observation doesn't fit a structured field, it goes into substance, never into /dev/null
- Structured fields are additive context (parallel access paths), not replacement for content
- Lensing operates on substance, not on index — the index helps you find the entity, the substance is what you lens
