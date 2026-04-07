---
id: SIG-034
timestamp: 2026-04-06T18:00:00Z
source: conversation
confidence: 0.9
trust: 0.6
autonomy_level: L2
status: active
cluster: work-ontology-design
author: brien
related_intents: []
referenced_by: []
parent_signal: SIG-033
---
# Intent taxonomy needs an INGEST intent type

## Observation

The eight intent types (PREPARE, RESEARCH, COACH, DELIVER, EVALUATE, POSITION, EXPLORE, SCAN) are all about producing analysis or artifacts from existing knowledge. "Ingest this human" or "bring in this company's data" is different — it's ACQUIRE + TRANSFORM + REGISTER. The closest existing type is PREPARE, but PREPARE compiles context for a decision. Ingestion compiles raw material into a durable entity.

During persona intake design, the natural language trigger "ingest this human" had no matching intent type. Brien's phrasing variations ("add this person," "bring them in," "research them for our persona library," or just dropping a URL) all map to the same underlying operation: acquire source material, transform it into structured knowledge, register the resulting entity.

## Implication

Add INGEST to the intent taxonomy:
- **INGEST**: Acquire raw material → transform to structured knowledge → register durable entity
- Default skill chain: identify → harvest → assess → render → connect → schedule-freshening
- Target types: Person → persona pipeline, Company → dossier pipeline, Domain → knowledge compilation, Source → corpus ingestion

INGEST differs from RESEARCH in that it produces a *persistent entity*, not a *report*. It differs from PREPARE in that it acquires *new material*, not compiles *existing context*.

## Design Constraint

- INGEST must produce entities (the new entity primitive from SIG-033), not just artifacts
- INGEST must be idempotent — ingesting the same source twice should enrich, not duplicate
- INGEST must handle disambiguation (SIG-036) as a required substep for named humans
