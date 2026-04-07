---
id: SIG-036
timestamp: 2026-04-06T18:00:00Z
source: conversation
confidence: 0.9
trust: 0.8
autonomy_level: L3
status: active
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
