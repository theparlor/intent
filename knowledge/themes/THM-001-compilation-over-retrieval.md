---
id: THM-001
type: theme
created: 2026-04-05
updated: 2026-04-05
depth_score: 2
depth_signals:
  file_size_kb: 2.6
  content_chars: 2096
  entity_count: 0
  slide_count: 0
  sheet_count: 0
  topic_count: 0
  has_summary: 0
vocab_density: 0.48
name: Compilation Over Retrieval
confidence: 0.85
origin: agent
sources:
  - raw/research/2026-04-02-karpathy-llm-knowledge-bases.md
  - raw/research/2026-04-05-three-layer-architecture-formalized.md
related_personas:
  - PER-001
  - PER-002
related_journeys:
  - JRN-001
  - JRN-002
related_decisions:
  - DDR-001
signals:
  - SIG-025
---
# Theme: Compilation Over Retrieval

## Insight

The compiled knowledge base compiles understanding once and keeps it current, rather than re-deriving knowledge on every query (RAG). Cross-references are already built. Contradictions are already flagged. The knowledge base is a persistent, compounding artifact — not a search index.

Karpathy's analogy: "raw/ is the source code, the LLM is the compiler, the wiki is the executable, health checks are the test suite, and queries are the runtime."

## Evidence

- [Karpathy LLM Knowledge Bases](../raw/research/2026-04-02-karpathy-llm-knowledge-bases.md) — Built ~100 articles / ~400K words with no vector database. LLM navigates via auto-maintained index and brief summaries. "Most people treat LLMs as transactional. This is fundamentally different."
- [Three-Layer Architecture](../raw/research/2026-04-05-three-layer-architecture-formalized.md) — "Compilation over retrieval" is Design Principle #1. Alexander's pattern languages provide the theoretical grounding: the knowledge base is a generating system, not documentation.
- Jason Paul Michaels (thread): "No vector database. No embeddings... Just markdown, FTS5, and grep. Every bug fix gets indexed. The knowledge compounds."

## Implications

- Intent's Layer 1 should be designed as a compiler, not a retrieval system. Artifacts are compiled once and incrementally updated — not regenerated from scratch.
- The `_index.md` + `log.md` navigation pattern replaces vector search. If the knowledge base grows beyond LLM context window capacity, consider `qmd` (Karpathy's local hybrid BM25/vector search) as a fallback, not a primary mechanism.
- Confidence scores on knowledge artifacts serve as the "test suite" — low confidence = the compilation is incomplete or unverified.

## Open Questions

- At what knowledge base size does the compilation model hit scaling limits? Karpathy's ~400K words fit in modern context windows, but team-scale knowledge bases could grow 10-100x.
- Is there a hybrid where compilation is primary but vector search provides a safety net for coverage gaps?
