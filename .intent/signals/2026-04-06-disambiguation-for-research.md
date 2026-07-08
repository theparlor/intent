---
id: SIG-036
timestamp: 2026-04-06T18:00:00Z
source: conversation
confidence: 0.9
trust: 0.8
autonomy_level: L3
status: resolved
upstream_control_path: "Core/products/cast/engine/schema/registry-entity.yaml (disambiguation block: anchors, anti_anchors, canonical_urls, verified)"
catch_mechanism: "identity fields are stored per-entity in the registry schema, not per research session, and are reusable across every future query for that entity"
verification_command: "grep -n -A3 'DISAMBIGUATION BLOCK' /Users/brien/Workspaces/Core/products/cast/engine/schema/registry-entity.yaml"
cluster: methodology-adoption
author: brien
related_intents: []
referenced_by: []
parent_signal: null
---
# Named-human research requires disambiguation anchors

## Observation

Brien identified that common names (e.g., "Aakash Gupta") produce thousands of false matches during web research. The persona intake pipeline must carry disambiguation context — facts that uniquely identify the target human, anti-anchors that exclude common false matches, and verified canonical URLs.

This is not unique to personas. Company research (multiple companies named "Atlas"), domain research (overlapping terminology), and any entity research face the same problem. Disambiguation is a general capability needed by the INGEST intent type.

## Implication

Every entity identity record should include:
- `anchors`: Facts that uniquely identify THIS entity (AND logic during search)
- `anti_anchors`: Common false matches to exclude (NOT logic during search)
- `canonical_urls`: Ground-truth pages verified by a human
- `verified`: Boolean — has a human confirmed this identity graph is clean?

The INGEST pipeline should treat disambiguation as a required substep, not an optional enhancement. For high-ambiguity entities, the pipeline should pause for human verification before proceeding with corpus harvesting.

## Design Constraint

- Disambiguation must be stored with the entity, not the research session (it's reusable)
- Anti-anchors must be actively used during every research query, not just initial intake
- The verified flag must be set by a human, not auto-set by the agent

## Triage, 2026-07-08

Disposition: control exists now, verified live. Core/products/cast/engine/schema/registry-entity.yaml has a full DISAMBIGUATION BLOCK with anchors, anti_anchors, canonical_urls, and a verified flag, exactly the four fields this signal specified, with the same AND/NOT logic description (anchors confirm, anti_anchors exclude).
