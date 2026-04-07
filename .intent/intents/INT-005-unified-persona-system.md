---
id: INT-005
title: "Build unified persona system: Identity → Corpus → Rendering"
status: accepted
proposed_by: brien
proposed_date: 2026-04-06T18:00:00Z
accepted_date: 2026-04-06T18:00:00Z
signals: [SIG-037, SIG-038, SIG-039, SIG-040, SIG-036]
specs: [SPEC-001, SPEC-002]
owner: brien
priority: now
product: cross-cutting
---
# Build Unified Persona System: Identity → Corpus → Rendering

## Problem

The Skills Engine and Knowledge Engine maintain independent, duplicative representations of the same human entities. Torres exists as a deep behavioral persona AND as a bullet point in a voice config. There is no shared registry, no stored raw material, no freshening mechanism, and no way to compose named humans into grounded archetypes.

Five signals (SIG-036, SIG-037, SIG-038, SIG-039, SIG-040) establish: disambiguation is required for research accuracy, the two systems are duplicative, open-world substance must never be constrained by taxonomy, named-human corpus aggregation produces superior archetypes, and Pawel Huryn is the first test case.

## Desired Outcome

Brien can:
1. Say "ingest this human" in any phrasing and trigger a consistent pipeline
2. The pipeline creates an identity record with disambiguation anchors, harvests corpus from primary channels, assesses originality and relationships, generates downstream renderings (Skills Engine persona, Knowledge Engine voice reference)
3. Named humans automatically declare contribution dimensions to archetypes
4. Archetypes synthesize from contributed corpus — grounded, not stereotypical
5. Every entity at every level provides standalone value and contributes upward
6. Existing personas (Torres, Cagan, Patton, Dunford, Singer) are migrated without losing depth

## Evidence

- SIG-037: Skills Engine and Knowledge Engine confirmed duplicative via side-by-side audit
- SIG-038: Brien established open-world-over-taxonomy as governing design principle
- SIG-039: Archetype enrichment model designed and validated through CEO example
- SIG-040: Huryn research completed — ready for intake as first test case
- SIG-036: Aakash Gupta disambiguation example validated anchor/anti-anchor pattern

## Constraints

- Must work as file-native entities in `Core/personas/` (consistent with Workspaces architecture)
- Must support three entity types: named-human, archetype, class
- Schema must have parallel index (structured, standards-backed) and substance (open-world, freeform) blocks
- Migration of existing 5 personalities must be lossless
- Corpus storage must support reprocessing when models improve
- Primary channels must be registered for periodic freshening
