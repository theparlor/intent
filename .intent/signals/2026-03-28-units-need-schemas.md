---
id: SIG-005
date: 2026-03-28
source: cowork-session
confidence: medium
related_intents: []
status: resolved
upstream_control_path: ".intent/templates/; bin/lib/id_gen.sh; DEC-INTENT-020"
catch_mechanism: "YAML frontmatter plus markdown body is the adopted hybrid (answers the Open Question below); ULID-based IDs (DEC-INTENT-020) give every entity a unique, timestamp-sortable ID; status fields function as the state machine; the intent-events GitHub Action gives git-tracked observability"
verification_command: "ls /Users/brien/Workspaces/Core/frameworks/intent/.intent/templates/"
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

What's the right balance between structured YAML (easy for agents) and readable markdown (easy for humans)? YAML frontmatter + markdown body may be the right hybrid.

## Triage, 2026-07-08

Disposition: control exists now. The open question resolved itself in practice: every entity type in the repo (signal, intent, spec, decision atom) uses YAML frontmatter plus a markdown body. Contract never became its own file type (see the linked triage note on SIG-001, work-ontology), so "start with Contract" did not happen literally, but the schema goal (visible, versioned, testable, observable) is met by the types that did ship.
