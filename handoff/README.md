---
title: Readme
type: framework
maturity: final
confidentiality: shareable
reusability: universal
domains:
  - consulting-operations
created: 2026-04-13
thought_leaders:
  - marty-cagan
  - jeff-patton
  - teresa-torres
  - josh-seiden
  - tim-herbig
frameworks:
  - double-loop-learning
depth_score: 4
depth_signals:
  file_size_kb: 3.4
  content_chars: 2642
  entity_count: 6
  slide_count: 0
  sheet_count: 0
  topic_count: 1
  has_summary: 0
vocab_density: 0.76
related_entities:
  - {pair: marty-cagan ↔ teresa-torres, count: 185, strength: 0.371}
  - {pair: jeff-patton ↔ teresa-torres, count: 121, strength: 0.32}
  - {pair: jeff-patton ↔ marty-cagan, count: 121, strength: 0.271}
  - {pair: marty-cagan ↔ product-engineering-coaching, count: 96, strength: 0.089}
  - {pair: coaching-methodology ↔ marty-cagan, count: 92, strength: 0.089}
---
# Intent Handoff Package — README

## Session: April 5, 2026
## Topic: Integrating Karpathy's LLM Knowledge Base pattern into Intent as a three-layer compiled knowledge system

---

## Contents (read in order)

| # | File | What It Is | Format |
|---|------|-----------|--------|
| 00 | `00-HANDOFF-CONTEXT-AND-PROMPT.md` | **START HERE.** Agent prompt + full session context. Every decision, architectural detail, and prioritized next steps. | Markdown |
| 01 | `01-karpathy-llm-knowledge-bases-full-picture.md` | Complete capture of Karpathy's tweet, thread, community discourse, tools, resources, and intellectual arc. The primary source material. | Markdown |
| 02 | `02-karpathy-x-intent-structural-parallels.docx` | Formal side-by-side architecture mapping. Five deep parallels, comparison tables, eight incorporation recommendations. | Word (.docx) |
| 03 | `03-three-layer-architecture-formalized.md` | Full technical architecture grounded in product frameworks (Torres, Patton, Cagan, Seiden, Herbig) and cybernetic theory (Beer, Argyris, Boyd, Alexander). Includes file system layout, six bidirectional flows, traceability chain, tech stack. | Markdown |
| 04 | `04-SOURCE-MANIFEST-AND-ATTRIBUTION.md` | Every URL surfaced across all research passes. Categorized by topic, annotated with extraction completeness, flagged for re-access priority. The provenance layer. | Markdown |

---

## How to Hand Off

1. Open a new Claude Code or Cowork session
2. Load all five files as context (or paste file 00 as your first message and attach the rest)
3. Tell the agent: "Read all attached context files starting with 00. These contain the full architectural decisions from a research session. Begin by reading the Intent codebase at github.com/theparlor/intent, then proceed with the prioritized next steps in file 00, section 8."
4. If the agent needs to go deeper on any source, file 04 has the full URL manifest with extraction priority recommendations

---

## Key Decisions Made in This Session

1. Intent absorbs Karpathy's LLM Knowledge Base pattern as **Layer 1** (domain knowledge base) of a three-layer architecture
2. Domain wiki and software specs remain **independent but fully bidirectionally coupled** through Intent's loop
3. The domain wiki both **compiles from raw research** AND **generates synthetic artifacts** (personas, journeys, designs)
4. Six bidirectional data flows connect all three layers, including **double-loop learning** (observe → domain wiki) and **single-loop learning** (observe → spec corpus)
5. The architecture is grounded in five product strategy frameworks and four cybernetic traditions
