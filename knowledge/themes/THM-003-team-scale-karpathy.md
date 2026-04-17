---
id: THM-003
type: theme
created: 2026-04-05
updated: 2026-04-13
depth_score: 2
depth_signals:
  file_size_kb: 4.0
  content_chars: 3515
  entity_count: 0
  slide_count: 0
  sheet_count: 0
  topic_count: 0
  has_summary: 0
vocab_density: 0.57
name: Intent as Team-Scale Karpathy
confidence: 0.75
origin: agent
sources:
  - raw/research/2026-04-02-karpathy-llm-knowledge-bases.md
  - raw/research/2026-04-05-three-layer-architecture-formalized.md
  - raw/research/2026-04-12-karpathy-power-to-the-people.md
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

## Positioning Refinement (April 2026 — from "Power to the People" essay extraction)

Karpathy's "Power to the People" (April 2025) establishes the structural argument: LLMs inverted the historical technology diffusion pattern, benefiting individuals before institutions. His LLM Knowledge Base work (April 2026) is the personal operationalization of that power — one person compiling a personal operating intelligence.

**The precise framing opportunity:**
> Karpathy's Knowledge Base solves "what does one person know."
> Intent solves "how does a group decide and move."
> Different problems at different levels of abstraction. No one has built the second with the rigor Karpathy applied to the first.

**What Intent adds beyond Karpathy:**
- **Team coordination layer:** Knowledge bases are personal; operating models are collective
- **Durability:** A compiled operating model persists across team changes; individual KBs die when the person leaves
- **Organizational thesis:** The gap isn't individuals vs. corporations — it's adaptive teams vs. bureaucratic institutions

**The deepest limit Karpathy doesn't name:** Individual democratization doesn't solve collective coordination. Individual LLM leverage × team ≠ team-level LLM leverage. That's the gap Intent closes.

## Open Questions

- At what team size does the knowledge base need access control (some artifacts owned by specific teams/roles)?
- Does the knowledge base need conflict resolution when two team members' ingested sources contradict each other?
- Karpathy identifies a "window" where frontier capability is commodity-priced. How does Intent's positioning change if performance tiers emerge (training-time or test-time scaling)?
