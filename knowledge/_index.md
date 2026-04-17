---
title: Domain Knowledge Base Index
type: index
depth_score: 4
depth_signals:
  file_size_kb: 5.9
  content_chars: 5655
  entity_count: 0
  slide_count: 0
  sheet_count: 0
  topic_count: 0
  has_summary: 0
vocab_density: 0.71
maintained_by: agent
last_compiled: 2026-04-13
artifact_count: 22
---
# Knowledge Base — Master Index

> This file is the primary entry point for all knowledge base operations. The LLM reads it first when answering queries, ingesting sources, or running lint passes. It is maintained automatically — do not edit manually.

## Personas (2)

- [[PER-001-practitioner-architect]] — Senior IC/tech lead who sees the gap between Agile and AI-augmented reality. Primary adoption persona. 4 pain points identified.
- [[PER-002-solo-knowledge-worker]] — Researcher/analyst who uses LLMs to compile domain knowledge. Karpathy pattern's native user. 3 pain points identified.

## Journeys (2)

- [[JRN-001-adopt-intent]] — PER-001 discovers Intent, scaffolds it, compiles domain knowledge, experiences double-loop learning. 5 stages, 3 moments of truth.
- [[JRN-002-build-knowledge-base]] — PER-002 builds a compiled knowledge base from scratch following the Karpathy pattern. 4 stages, 2 moments of truth.

## Design Decisions (7)

- [[DDR-001-compilation-over-rag]] — **Accepted.** Use compilation (persistent knowledge base) over retrieval (RAG) for domain knowledge. Addresses PER-001/PP-003, PER-002/PP-002.
- [[DDR-002-three-layer-architecture]] — **Accepted.** Domain Wiki + Transformation OS + Software Spec/Code as three independent, bidirectionally coupled layers.
- [[DDR-003-bidirectional-coupling]] — **Accepted.** Full bidirectional coupling with six data flows. Flow 5 (double-loop) is the critical path.
- [[DDR-004-federated-wiki]] — **Accepted.** Federate knowledge base across Core and bounded engagements. Inherit down, promote up, never leak sideways.
- [[DDR-005-knowledge-engine-boundary]] — **Accepted.** Intent (methodology), Knowledge Engine (product), and Knowledge Farm (instance) are three distinct things. Coincidence clause: Brien's farm feeds Intent by domain overlap, not architecture.
- [[DDR-006-12-factor-agent-patterns]] — **Accepted.** HumanLayer 12-factor agent integration: pause/resume, human-contact-as-capability, LLM-as-judge, error-retry-escalate, stateful-system/stateless-invocations. Event catalog 15→22. (2026-04-13)
- [[DDR-007-ke-mcp-query-write-back]] — **Accepted.** Query write-back is first-class in intent-knowledge MCP. Conditional auto-enrichment with confidence gating. 5-tool surface (ingest/query/lint/enrich/status). Federation boundary enforcement. Confidence: 0.85.
- [[DDR-008-trust-as-orientation-proxy]] — **Accepted.** Trust scoring incorporates orientation quality modifier (persona confidence, DDR coverage, source freshness, contradiction density). Trust decays with time since validation. IG&C threshold formalized. Confidence: 0.8.

## Themes (4)

- [[THM-001-compilation-over-retrieval]] — The knowledge base compiles understanding once and keeps it current, rather than re-deriving per query. Confidence: 0.85.
- [[THM-002-bottleneck-shift]] — When AI collapses implementation, the constraint moves from delivery velocity to specification quality. Confidence: 0.9.
- [[THM-003-team-scale-karpathy]] — Intent extends Karpathy's solo pattern to teams with multi-agent coordination and formal governance. Refined: "what one person knows" vs. "how a group decides and moves." Confidence: 0.8.
- [[THM-004-spec-governed-execution]] — Intent occupies a fourth SDD position beyond Böckeler's taxonomy (spec-first/anchored/as-source): specs as contracts verified through trust gates and observe. Confidence: 0.8.

## Domain Models (2)

- [[DOM-001-work-ontology]] — The seven-level work hierarchy: Signal → Intent → Spec → Contract → Atom → Capability → Feature/Product.
- [[DOM-002-knowledge-ontology]] — The six Layer 1 artifact types (PER, JRN, DDR, THM, DOM, RAT) and their relationships.

## Design Rationale (3)

- [[RAT-001-generating-systems]] — The knowledge base is a generating system (Alexander), not documentation. Pattern language that generates specs through rules of combination.
- [[RAT-002-double-loop-learning]] — Flow 5 (Observe → Wiki) is the most important data flow. Without it, only single-loop optimization is possible. Now validated by Boyd's OODA learning loop (Richards 2020). (Argyris, Beer, Seiden, Boyd)
- [[RAT-003-dual-circuit-architecture]] — Boyd's dual-circuit model (fast IG&C + learning loop) validates Intent's two-speed architecture. Trust scoring determines which circuit dominates. Incestuous amplification is the governance failure mode overwatch prevents. (Boyd, Richards 2020)

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
| Decisions | 8 | 0.85 |
| Themes | 4 | 0.84 |
| Domain Models | 2 | 0.78 |
| Design Rationale | 3 | 0.85 |
| Entity Dossiers | 1 | 0.65 |
| **Total** | **22** | **0.79** |

## Raw Research Sources (11)

| File | Date | Type | Confidence |
|------|------|------|------------|
| intent-methodology-v1 | 2026-03-28 | methodology | — |
| karpathy-llm-knowledge-bases | 2026-04-02 | primary-source | 0.95 |
| three-layer-architecture-formalized | 2026-04-05 | synthesis | — |
| automotive-oem-industry-research | 2026-04-06 | industry-research | 0.65 |
| rvk7895-llm-knowledge-bases | 2026-04-12 | implementation-analysis | 0.85 |
| karpathy-gist-llm-wiki | 2026-04-12 | primary-source | 0.95 |
| fowler-sdd-tools-survey | 2026-04-12 | industry-analysis | 0.9 |
| chet-richards-boyds-ooda-loop | 2026-04-12 | academic-paper | 0.95 |
| rotifer-compile-dont-search-agent-memory | 2026-04-12 | industry-analysis | 0.85 |
| karpathy-power-to-the-people | 2026-04-12 | primary-source | 0.9 |
| chi2024-llm-generated-personas | 2026-04-12 | academic-paper | 0.75 |

---

_Last compiled: 2026-04-13 — 7 raw research sources ingested (SIG-032). Created RAT-003, THM-004, DDR-007, DDR-008. Updated THM-003, RAT-002. 3 carry-forward signals (SIG-033/034/035). Artifact count 16→22._
