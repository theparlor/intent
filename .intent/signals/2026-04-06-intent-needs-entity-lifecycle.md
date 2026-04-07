---
id: SIG-033
timestamp: 2026-04-06T18:00:00Z
source: conversation
confidence: 0.9
trust: 0.5
autonomy_level: L2
status: active
cluster: work-ontology-design
author: brien
related_intents: []
referenced_by: []
parent_signal: SIG-001
---
# Intent framework lacks an entity lifecycle primitive

## Observation

The work ontology (Signal → Intent → Spec → Contract → Capability → Feature → Product) tracks work items through a pipeline. But some things in the system are not work items — they are **durable entities that accumulate state over time**. A persona, a knowledge artifact, an archetype, a company dossier — these are created once, enriched repeatedly, freshened periodically, occasionally deprecated or merged.

Signals are ephemeral observations. Intents are promotable work items. Neither captures the lifecycle of a persistent entity. The persona system design exposed this: a persona is CREATED through an intake pipeline (work), but then EXISTS as a durable entity that the work ontology operates ON but doesn't OWN.

## Implication

The framework needs a concept of **entities** alongside work items. Entities have lifecycles (created → active → enriched → stale → deprecated → archived). They are the *nouns* the work ontology's *verbs* act upon. Without this, every durable artifact built through Intent becomes a parallel system that the framework can't track, version, or reason about.

This is not just a persona problem. The Knowledge Engine's compiled artifacts, the archetype composites, engagement dossiers — all are entities, not work items.

## Design Constraint

- Entity lifecycle must be orthogonal to the work ontology — an entity can be in any lifecycle state while work items flow through it
- Entities must support contribution (one entity enriching another)
- Entity freshness must be observable (feeds the Notice phase via lint)
- Must not add ceremony — entity lifecycle tracking should be metadata, not process
