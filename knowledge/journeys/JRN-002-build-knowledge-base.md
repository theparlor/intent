---
id: JRN-002
type: journey
created: 2026-04-05
updated: 2026-04-05
depth_score: 2
depth_signals:
  file_size_kb: 3.2
  content_chars: 2820
  entity_count: 0
  slide_count: 0
  sheet_count: 0
  topic_count: 0
  has_summary: 0
vocab_density: 0.00
name: Building a Domain Knowledge Base from Scratch
persona: PER-002
confidence: 0.65
origin: agent
sources:
  - raw/research/2026-04-02-karpathy-llm-knowledge-bases.md
related_decisions:
  - DDR-001
---
# Journey: Building a Domain Knowledge Base from Scratch

## Overview

A [[PER-002-solo-knowledge-worker]] wants to build a compiled knowledge base on a domain. They follow the Karpathy pattern: drop sources, let the LLM compile, query against compiled knowledge, run periodic lint.

Start: Scattered sources (papers, articles, notes) with no structure
End: A ~100+ article knowledge base with cross-references, index, and compounding knowledge

## Stages

### Stage: Seed

- **Steps:** Create `raw/` and `knowledge/` directories. Write or adopt a knowledge-engine/AGENTS.md schema. Drop first 3-5 sources into `raw/`. Run initial ingest.
- **Emotions:** Setup friction ("is this going to be worth it?"), anticipation
- **Pain points:** PER-002/PP-003 (no packaged product for this)
- **Touchpoints:** File system, LLM agent, knowledge-engine/AGENTS.md

### Stage: Build Critical Mass

- **Steps:** Ingest 10-30 sources. Knowledge base grows to ~30 articles. Cross-references start forming meaningful clusters. Index becomes useful. First query returns a non-obvious answer.
- **Emotions:** Growing satisfaction, the "it's starting to compound" moment
- **Pain points:** PER-002/PP-001 (knowledge decays — but now the knowledge base is maintaining it)
- **Touchpoints:** `raw/` drop zone, knowledge artifacts, `_index.md`

### Stage: Compound

- **Steps:** Knowledge base at 50-100+ articles. Queries regularly return insights the user had forgotten. Lint finds contradictions that lead to genuine new understanding. The knowledge base knows more than the human.
- **Emotions:** Trust, reliance, occasional surprise
- **Pain points:** PER-002/PP-002 (solved — compilation replaces re-derivation)
- **Touchpoints:** Query interface, lint output, Obsidian graph view

### Stage: Generate

- **Steps:** Use compiled knowledge to generate artifacts: reports, slide decks, training data, specifications. The knowledge base becomes a generating system, not just a reference.
- **Emotions:** Leverage ("I couldn't have produced this without the knowledge base")
- **Touchpoints:** Marp slides, HTML visualizations, synthetic generation

## Moments of Truth

1. **First non-obvious answer:** Query returns something the user had ingested weeks ago and forgotten. The compilation payoff is tangible.
2. **First lint insight:** Lint finds a contradiction between two sources the user hadn't noticed. Real new understanding emerges from the system, not just the human.

## Evidence

- [Karpathy LLM Knowledge Bases](../raw/research/2026-04-02-karpathy-llm-knowledge-bases.md) — "After a while, the LLM 'gets' the pattern and the marginal document is a lot easier." His wiki grew to ~100 articles / ~400K words.
- Lex Fridman: temporary mini-knowledge-bases for voice interaction during runs — an ephemeral variant of this journey.
