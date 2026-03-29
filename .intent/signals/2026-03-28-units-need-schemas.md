---
id: SIG-005
timestamp: 2026-03-28T12:00:00Z
source: cowork-session
author: brien
confidence: 0.6
trust: 0.5
autonomy_level: L2
status: active
cluster: work-ontology-design
parent_signal:
related_intents: []
---
# Signal: Work units need formal schemas to be agent-consumable

## Observation

Brien emphasized that the atomic building blocks need to be "visible, versioned, testable, and observable out of the box." This means every work unit (signal, intent, spec, contract, capability) must have a formal file schema — not just be a concept.

## Implication

Each unit type needs:

- **A file format** (YAML frontmatter + markdown body, or pure YAML for contracts)
- **A schema** that agents can parse and validate
- **A state machine** (e.g., intent: hypothesis → exploring → validated → invalidated)
- **A unique ID** that flows through the hierarchy (trace ID pattern)
- **Git tracking** (versioning is free)
- **Self-testing** (contracts carry assertions; specs carry contract references)

## Next Steps

Design the formal schemas for each unit type. Start with Contract (the atom) and work upward. The schema should be minimal but machine-parseable — an agent picking up a contract file should be able to execute against it without human explanation.

## Open Question

What’s the right balance between structured YAML (easy for agents) and readable markdown (easy for humans)? YAML frontmatter + markdown body may be the right hybrid.
