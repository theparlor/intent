---
id: SIG-032
timestamp: 2026-04-12T23:30:00Z
source: session-review
confidence: 0.85
trust: 0.8
autonomy_level: L3
status: resolved
cluster: knowledge-engine
author: brien
related_intents: []
referenced_by:
  - SIG-025
parent_signal: SIG-025
---
# Karpathy source manifest extraction backlog — 21 unfetched + 8 high-extraction sources never processed

The April 5 handoff package included `04-SOURCE-MANIFEST-AND-ATTRIBUTION.md` cataloging 82 distinct sources from the Karpathy × Intent research session. Two files from the zip (`04-SOURCE-MANIFEST-AND-ATTRIBUTION.md` and `README.md`) were never extracted into `handoff/` — they sat in Downloads for 7 days until discovered in session review on April 12.

**The extraction backlog includes:**

High-priority (directly relevant to active dev tracks):
1. **rvk7895/llm-knowledge-bases** — working Claude Code plugin implementing full /kb-init, compile, query, lint. Directly relevant to Knowledge Engine implementation.
2. **Karpathy GitHub Gist YAML templates** — verbatim frontmatter templates for wiki schema. Relevant to KE artifact templates.
3. **Martin Fowler SDD tools survey** — spec-driven development patterns (Kiro, spec-kit, Tessl). Relevant to Intent Spec product.
4. **Chet Richards OODA paper (PDF)** — detailed multi-path feedback diagrams mapping to Intent's bidirectional flows.
5. **CHI 2024 LLM-generated Personas study** — methodology confirming LLM personas indistinguishable from human-written. Relevant to persona pipeline validation.
6. **DEV Community agent memory article** — "Compile your knowledge, don't search it" — agent memory architecture relevant to MCP server design.
7. **Karpathy "Power to the People" essay** — LLMs benefiting individuals over institutions, relevant to Intent positioning.

Plus 14 additional unfetched sources (Section I of the manifest) of lower but non-zero extraction value.

**Why now:** Dev tracks (Knowledge Engine, persona system, Intent Spec product) are in tangentially overlapping spaces. Closing this loop before the next architectural review and interviews ensures the compiled knowledge base has full provenance and no blind spots from partially-read sources.

**Action:** L3 — extract high-priority sources in parallel, compile into `raw/research/` and update `knowledge/` artifacts. Surface any architectural implications as new signals.
