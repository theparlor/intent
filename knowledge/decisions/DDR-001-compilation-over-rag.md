---
title: Use compilation (persistent knowledge base) over retrieval (RAG) for domain knowledge
id: DDR-001
type: decision
created: 2026-04-05
updated: 2026-04-05
depth_score: 2
depth_signals:
  file_size_kb: 3.1
  content_chars: 2620
  entity_count: 0
  slide_count: 0
  sheet_count: 0
  topic_count: 0
  has_summary: 0
vocab_density: 0.00
status: accepted
confidence: 0.85
origin: human
addresses:
  - PER-001/PP-003
  - PER-002/PP-002
persona: PER-001
journey_stage: JRN-001#compile-understanding
sources:
  - raw/research/2026-04-02-karpathy-llm-knowledge-bases.md
  - raw/research/2026-04-05-three-layer-architecture-formalized.md
---
# DDR: Compilation Over RAG for Domain Knowledge

## Context

Intent needs a mechanism to persist and grow domain understanding across the team. Two patterns exist:
1. **RAG (Retrieval-Augmented Generation):** Embed documents in a vector store, retrieve relevant chunks per query, re-derive understanding on every interaction.
2. **Compilation (Karpathy pattern):** LLM reads raw sources and compiles a structured, interlinked wiki. Understanding is built once and incrementally updated.

Karpathy explicitly chose compilation and found it sufficient at ~100 articles / ~400K words with no vector store — the LLM navigates via auto-maintained index files and brief summaries.

## Decision

Intent's Layer 1 uses the **compilation pattern**: raw sources are ingested into a persistent, LLM-maintained knowledge base with structured artifacts (personas, journeys, DDRs, themes, domain models), cross-references via [[wikilinks]], and confidence scoring. No vector database. No embeddings. Navigation via `_index.md`.

## Alternatives Considered

| Alternative | Pros | Cons | Why Rejected |
|-------------|------|------|-------------|
| RAG (vector store) | Works at any scale, no compilation step | Re-derives understanding per query, no persistent cross-refs, no contradiction detection, no coverage tracking | Doesn't compound. Every query starts from scratch. |
| Hybrid (compile + vector fallback) | Best of both worlds | Added complexity, unclear when to use which | Deferred — may be needed at scale but premature now |
| Manual knowledge management | Full human control | Doesn't scale, knowledge decays | The problem we're solving |

## Consequences

**Positive:**
- Knowledge compounds across sessions — each ingest builds on prior understanding
- Contradictions and coverage gaps are detectable (lint operation)
- Cross-references are persistent, not re-derived
- Human-readable artifacts (markdown) — no opaque vector embeddings

**Negative:**
- Compilation step takes time (a single source touches 10-15 pages)
- LLM hallucinations during compilation persist and compound (Steph Ango's contamination concern)
- May hit scaling limits at team-scale knowledge bases (100K+ pages)

## Validation Criteria

- [ ] First ingest successfully compiles raw sources into interlinked knowledge artifacts
- [ ] Query operation returns answers with citations to compiled artifacts, not raw sources
- [ ] Lint operation detects a real contradiction or coverage gap
- [ ] Confidence scores change meaningfully as new sources are ingested
