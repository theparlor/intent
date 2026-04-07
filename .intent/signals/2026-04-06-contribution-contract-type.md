---
id: SIG-035
timestamp: 2026-04-06T18:00:00Z
source: conversation
confidence: 0.85
trust: 0.5
autonomy_level: L2
status: active
cluster: work-ontology-design
author: brien
related_intents: []
referenced_by: []
parent_signal: SIG-033
---
# Contribution contracts: a new contract type for entity composition

## Observation

The four contract types (interface, behavior, quality, integration) cover how code works. But the persona system's archetype enrichment model introduced a new verifiable assertion: "when a named human is added, the archetype it contributes to should get measurably richer along declared dimensions."

This is a **contribution contract** — a verifiable assertion about how entities compose upward. Examples:
- Adding Mary Barra should enrich the manufacturing-CEO archetype's voice_patterns and mental_models
- Adding a 16th CEO should not degrade the archetype's existing stances
- The archetype's evidence.md should grow, and its source-humans.yaml should list the new contributor

## Implication

Add CONTRIBUTION as a fifth contract type:
- **Interface contract**: API shape (unchanged)
- **Behavior contract**: Execution correctness (unchanged)
- **Quality contract**: Performance/reliability (unchanged)
- **Integration contract**: System interactions (unchanged)
- **Contribution contract**: Entity composition — verifies that adding entity A to composite B enriches B along declared dimensions without degrading existing content

Contribution contracts are testable: before/after diff of the archetype, dimension-specific checks, non-regression on existing content.

## Design Constraint

- Must be direction-aware (upward contribution, not downward inheritance)
- Must declare which dimensions are affected (voice_patterns, mental_models, stances, etc.)
- Must be non-destructive by default — failing a contribution contract should block the merge, not silently degrade the composite
