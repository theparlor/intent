---
id: THM-003
type: theme
created: 2026-04-05
updated: 2026-04-05
depth_score: 2
depth_signals:
  file_size_kb: 2.4
  content_chars: 2033
  entity_count: 0
  slide_count: 0
  sheet_count: 0
  topic_count: 0
  has_summary: 0
vocab_density: 0.98
name: Intent as Team-Scale Karpathy
confidence: 0.75
origin: agent
sources:
  - raw/research/2026-04-02-karpathy-llm-knowledge-bases.md
  - raw/research/2026-04-05-three-layer-architecture-formalized.md
related_personas:
  - PER-001
  - PER-002
related_decisions:
  - DDR-003
signals:
  - SIG-025
---
# Theme: Intent as Team-Scale Karpathy

## Insight

Karpathy's system has one human curator and one LLM agent. Intent extends this to multiple human curators (teams), multiple agent roles (subagents with trust-gated autonomy), and formal governance (trust scoring, contracts, ARB). The positioning: "Karpathy showed what one person can do with a compiled knowledge base. Intent shows what a team can do with a compiled operating model."

## Evidence

- [Karpathy LLM Knowledge Bases](../raw/research/2026-04-02-karpathy-llm-knowledge-bases.md) — "At the moment it's not a fully autonomous process. I add every source manually, one by one and I am in the loop."
- [Three-Layer Architecture](../raw/research/2026-04-05-three-layer-architecture-formalized.md) — Beer's VSM provides the formal model: Layer 1 = System 4+5 (intelligence + identity), Layer 2 = System 2+3 (coordination + management), Layer 3 = System 1 (operations). Multi-agent coordination requires these governance layers.
- Eugen Alpeza (thread): "The jump from personal research wiki to enterprise operations is where it gets brutal. Thousands of employees, millions of records, tribal knowledge that contradicts itself across teams."
- Intent's six subagent architecture (signal-capture, enricher, spec-writer, contract-verifier, observer, coordinator) provides the multi-agent coordination Karpathy's solo pattern doesn't need.

## Implications

- This is a positioning insight, not just a technical one. It frames Intent's market differentiation.
- The contamination mitigation pattern (origin tracking) becomes more critical at team scale — one person's agent-generated content becomes another person's assumed-human input.
- Trust scoring and autonomy levels (L0-L4) are the governance mechanism that makes team-scale compilation safe.

## Open Questions

- At what team size does the knowledge base need access control (some artifacts owned by specific teams/roles)?
- Does the knowledge base need conflict resolution when two team members' ingested sources contradict each other?
