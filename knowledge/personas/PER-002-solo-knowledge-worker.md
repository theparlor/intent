---
id: PER-002
type: persona
created: 2026-04-05
updated: 2026-04-05
depth_score: 2
depth_signals:
  file_size_kb: 2.8
  content_chars: 2238
  entity_count: 0
  slide_count: 0
  sheet_count: 0
  topic_count: 0
  has_summary: 0
vocab_density: 0.00
name: Solo Knowledge Worker
slug: solo-knowledge-worker
confidence: 0.60
origin: agent
sources:
  - raw/research/2026-04-02-karpathy-llm-knowledge-bases.md
related_journeys:
  - JRN-002
related_decisions:
  - DDR-001
related_themes:
  - THM-001
  - THM-003
pain_points:
  - "PP-001: Knowledge decays faster than it can be manually organized"
  - "PP-002: RAG retrieves but doesn't compile — understanding must be re-derived every query"
  - "PP-003: No product packages the knowledge compilation pattern for non-engineers"
---
# Persona: Solo Knowledge Worker

## Who

A researcher, analyst, or deep specialist who uses LLMs extensively. Could be Karpathy himself — someone who spends "more tokens manipulating knowledge than writing code." They work solo or in a small team. They need to build persistent, compounding understanding of a domain, not just get transactional answers.

This persona represents the Karpathy pattern's native user — the person Intent extends from individual practice to team practice.

## Behaviors

- Drops source material (papers, articles, reports) into a folder and expects the LLM to compile it
- Navigates via index files and summaries rather than search or RAG
- Runs periodic health checks (lint) to find contradictions and gaps
- Values Obsidian as an IDE for knowledge, not just a note-taking app
- Has built "a hacky collection of scripts" and wants a real product

## Needs & Pain Points

- PP-001: Knowledge decays faster than it can be manually organized. The Extended_Brain Substack critique applies: Luhmann's Zettelkasten is the exercise, Karpathy's wiki is the report from the trainer.
- PP-002: RAG retrieves but doesn't compile. Every query re-derives understanding from scratch. The knowledge base compiles once and keeps current — cross-references already there, contradictions already flagged.
- PP-003: No product packages this pattern for non-engineers. Glen Rhodes: "It requires you to be Andrej Karpathy to set it up." Ole Lehmann: "Whoever packages this for normal people is sitting on something massive."

## Evidence

- [Karpathy LLM Knowledge Bases](../raw/research/2026-04-02-karpathy-llm-knowledge-bases.md) — "A large fraction of my recent token throughput goes less into manipulating code and more into manipulating knowledge."
- Karpathy's wiki: ~100 articles, ~400K words on a single topic. No vector DB needed.
- Lex Fridman: generates temporary mini-knowledge-bases for voice-mode interaction on runs.
- Vamshi Reddy: "Every business has a raw/ directory. Nobody's ever compiled it."

## Open Questions

- Does this persona ever need the full Intent loop (spec→execute→observe), or do they stop at Layer 1?
- What's the contamination risk for solo vs. team use? (Ango's concern applies differently at scale)
