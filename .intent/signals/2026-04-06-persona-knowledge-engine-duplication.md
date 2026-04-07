---
id: SIG-037
timestamp: 2026-04-06T18:00:00Z
source: conversation
confidence: 0.95
trust: 0.7
autonomy_level: L3
status: active
cluster: methodology-adoption
author: brien
related_intents: []
referenced_by: [SIG-027]
parent_signal: SIG-027
---
# Skills Engine personas and Knowledge Engine voices are duplicative representations of the same humans

## Observation

The Skills Engine has deep behavioral personas in `personas/personalities/` (Torres, Cagan, Patton, Dunford, Singer) with mental models, voice descriptions, and rendering notes. The Knowledge Engine has shallow `hero_authors` references in `voices/product.yaml` listing the same people with just name + key works + key concepts.

Neither system knows about the other's representation. Torres exists as a full persona file AND as a bullet point in a voice config. When Brien adds Pawel Huryn, he'd need to add him in both places with no shared schema, no shared source material, no shared freshening.

## Implication

A unified persona registry (`Core/personas/registry/`) should be the single source of truth for all human entities. Both the Skills Engine and Knowledge Engine become *rendering consumers* of this canonical registry — they generate their respective outputs (persona files, voice configs) from the same identity + corpus, not from independent manual authoring.

This is the specific instance of the entity lifecycle problem (SIG-033). A persona entity is created once, lives in the registry, and is rendered into multiple downstream formats.

## Design Constraint

- Migration must preserve all existing persona depth (Skills Engine personas are rich — don't lose that)
- Knowledge Engine voice configs should reference registry entities, not duplicate their content
- The registry is the authoritative source; downstream renderings are projections
