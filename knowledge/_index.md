---
title: Domain Knowledge Base Index
type: index
depth_score: 4
depth_signals:
  file_size_kb: 5.3
  content_chars: 5066
  entity_count: 0
  slide_count: 0
  sheet_count: 0
  topic_count: 0
  has_summary: 0
vocab_density: 1.18
maintained_by: agent
last_compiled: 2026-04-06
artifact_count: 16
---
# Knowledge Base — Master Index

> This file is the primary entry point for all knowledge base operations. The LLM reads it first when answering queries, ingesting sources, or running lint passes. It is maintained automatically — do not edit manually.

## Personas (2)

- [[PER-001-practitioner-architect]] — Senior IC/tech lead who sees the gap between Agile and AI-augmented reality. Primary adoption persona. 4 pain points identified.
- [[PER-002-solo-knowledge-worker]] — Researcher/analyst who uses LLMs to compile domain knowledge. Karpathy pattern's native user. 3 pain points identified.

## Journeys (2)

- [[JRN-001-adopt-intent]] — PER-001 discovers Intent, scaffolds it, compiles domain knowledge, experiences double-loop learning. 5 stages, 3 moments of truth.
- [[JRN-002-build-knowledge-base]] — PER-002 builds a compiled knowledge base from scratch following the Karpathy pattern. 4 stages, 2 moments of truth.

## Design Decisions (3)

- [[DDR-001-compilation-over-rag]] — **Accepted.** Use compilation (persistent knowledge base) over retrieval (RAG) for domain knowledge. Addresses PER-001/PP-003, PER-002/PP-002.
- [[DDR-002-three-layer-architecture]] — **Accepted.** Domain Wiki + Transformation OS + Software Spec/Code as three independent, bidirectionally coupled layers.
- [[DDR-003-bidirectional-coupling]] — **Accepted.** Full bidirectional coupling with six data flows. Flow 5 (double-loop) is the critical path.
- [[DDR-004-federated-wiki]] — **Accepted.** Federate knowledge base across Core and bounded engagements. Inherit down, promote up, never leak sideways.
- [[DDR-005-knowledge-engine-boundary]] — **Accepted.** Intent (methodology), Knowledge Engine (product), and Knowledge Farm (instance) are three distinct things. Coincidence clause: Brien's farm feeds Intent by domain overlap, not architecture.

## Themes (3)

- [[THM-001-compilation-over-retrieval]] — The knowledge base compiles understanding once and keeps it current, rather than re-deriving per query. Confidence: 0.85.
- [[THM-002-bottleneck-shift]] — When AI collapses implementation, the constraint moves from delivery velocity to specification quality. Confidence: 0.9.
- [[THM-003-team-scale-karpathy]] — Intent extends Karpathy's solo pattern to teams with multi-agent coordination and formal governance. Confidence: 0.75.

## Domain Models (2)

- [[DOM-001-work-ontology]] — The seven-level work hierarchy: Signal → Intent → Spec → Contract → Atom → Capability → Feature/Product.
- [[DOM-002-knowledge-ontology]] — The six Layer 1 artifact types (PER, JRN, DDR, THM, DOM, RAT) and their relationships.

## Design Rationale (2)

- [[RAT-001-generating-systems]] — The knowledge base is a generating system (Alexander), not documentation. Pattern language that generates specs through rules of combination.
- [[RAT-002-double-loop-learning]] — Flow 5 (Observe → Wiki) is the most important data flow. Without it, only single-loop optimization is possible. (Argyris, Beer, Seiden)

## Entity Dossiers (1)

- [[DSR-IND-001-automotive-oem-us]] — US Automotive OEM industry dossier. $680B market, 16.2M units, EV transition, SDV trend, tariff disruption, operating model transformation opportunity. Confidence: 0.65. Public.

## Engagement Knowledge Farms

Engagement-scoped artifacts live in their engagement Knowledge Farms per the federation model. See: Work/Consulting/Engagements/[Client]/knowledge/

- **Subaru**: 4 personas (PER-003–006), 2 dossiers (DSR-COM-001, DSR-CTX-001), 1 raw research file

## Coverage Summary

| Artifact Type | Count | Avg Confidence |
|---------------|-------|----------------|
| Personas | 2 | 0.63 |
| Journeys | 2 | 0.63 |
| Decisions | 5 | 0.84 |
| Themes | 3 | 0.83 |
| Domain Models | 2 | 0.78 |
| Design Rationale | 2 | 0.83 |
| Entity Dossiers | 1 | 0.65 |
| **Total** | **16** | **0.76** |

---

_Last compiled: 2026-04-06 — Engagement-scoped artifacts federated to Subaru Knowledge Farm. Core retains methodology-only artifacts._
