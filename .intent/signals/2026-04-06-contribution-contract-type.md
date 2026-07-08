---
id: SIG-035
timestamp: 2026-04-06T18:00:00Z
source: conversation
confidence: 0.85
trust: 0.5
autonomy_level: L2
status: resolved
upstream_control_path: "Core/frameworks/intent/spec/SPEC-003-intent-framework-entity-extensions.md Extension 3 (CONTRIBUTION Contract Type) + CON-010"
catch_mechanism: "before/after snapshot diff; non-regression dimensions must be empty-diff, verified per entity contribution event"
verification_command: "grep -n 'Extension 3' /Users/brien/Workspaces/Core/frameworks/intent/spec/SPEC-003-intent-framework-entity-extensions.md"
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

## Triage, 2026-07-08

Disposition: control exists now, verified live. SPEC-003 Extension 3 (CONTRIBUTION Contract Type) adds exactly the fifth contract type this signal proposed, with the same fields (source_entity, target_composite, dimensions, non_regression) and the same before/after-diff verification method. CON-010 (Contribution Non-Regression) is the enforceable contract.
