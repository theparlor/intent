---
id: THM-002
type: theme
created: 2026-04-05
updated: 2026-04-05
depth_score: 2
depth_signals:
  file_size_kb: 2.6
  content_chars: 2042
  entity_count: 0
  slide_count: 0
  sheet_count: 0
  topic_count: 0
  has_summary: 0
vocab_density: 1.47
name: The Bottleneck Shifts from Execution to Specification
confidence: 0.90
origin: agent
sources:
  - raw/research/2026-03-28-intent-methodology-v1.md
  - raw/research/2026-04-02-karpathy-llm-knowledge-bases.md
related_personas:
  - PER-001
related_journeys:
  - JRN-001
related_decisions:
  - DDR-002
signals:
  - SIG-001
---
# Theme: The Bottleneck Shifts from Execution to Specification

## Insight

When AI collapses implementation from weeks to hours, the constraint moves from delivery velocity to specification quality. Every methodology built around the assumption that implementation is the bottleneck — Waterfall, Agile, Scrum — is optimizing for a constraint that no longer binds. Cagan has said this for years. AI made the argument undeniable.

## Evidence

- [Intent Methodology v1](../raw/research/2026-03-28-intent-methodology-v1.md) — "For thirty years, software development methodology has been organized around a single assumption: implementation is the bottleneck. That assumption is breaking."
- [Karpathy LLM Knowledge Bases](../raw/research/2026-04-02-karpathy-llm-knowledge-bases.md) — Karpathy's intellectual arc: vibe coding (Feb 2025) → power to the people (Apr 2025) → bespoke software (Feb 2026) → knowledge bases (Apr 2026). "Once code generation is 'solved enough,' the frontier moves to knowledge orchestration."
- Ari's team (founding empirical evidence): "Their tickets became specifications for bots to run. Their refinement meetings became heavily design oriented."
- Sprint planning, velocity tracking, and backlog grooming all become irrelevant when the unit of work is a spec, not a sprint.

## Implications

- The operating model should optimize for spec quality, not delivery throughput.
- Domain knowledge compilation (Layer 1) directly improves spec quality — the more compiled the understanding, the better the specification, the better the agent output.
- "Spec quality" is the new velocity metric. A good spec is "the shortest document that makes the agent dangerous."
- Retrospectives should ask "what was missing from the spec?" not "how can we go faster?"

## Open Questions

- Is this shift experienced equally across all software domains, or are some domains (embedded, safety-critical) still execution-bottlenecked?
- How do teams that haven't adopted AI agents yet experience this shift? Is it a cliff or a gradient?
