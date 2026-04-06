---
id: PER-001
type: persona
created: 2026-04-05
updated: 2026-04-05
depth_score: 2
depth_signals:
  file_size_kb: 3.8
  content_chars: 3077
  entity_count: 0
  slide_count: 0
  sheet_count: 0
  topic_count: 0
  has_summary: 0
vocab_density: 0.65
name: Practitioner-Architect
slug: practitioner-architect
confidence: 0.70
origin: agent
sources:
  - raw/research/2026-03-28-intent-methodology-v1.md
  - raw/research/2026-04-05-three-layer-architecture-formalized.md
related_journeys:
  - JRN-001
related_decisions:
  - DDR-001
  - DDR-002
  - DDR-003
related_themes:
  - THM-001
  - THM-002
pain_points:
  - "PP-001: Ceremony overhead consumes time that should go to discovery and specification"
  - "PP-002: AI agents execute well-specified work in hours but most specs are too ambiguous"
  - "PP-003: No systematic way to compile domain knowledge into agent-ready specifications"
  - "PP-004: Observations from running code don't feed back into domain understanding"
---
# Persona: Practitioner-Architect

## Who

Senior IC or tech lead (5-15+ years experience) who thinks in systems. They see the gap between what Agile promises and what it delivers in an AI-augmented world. They have organizational influence — enough to adopt new tools and methods within their team without executive permission, but not enough to mandate org-wide change.

They follow product thinkers (Cagan, Torres, Patton) and have read enough systems theory to recognize when a process is optimizing for the wrong thing. They're the person on the team who notices patterns before others do.

**Persona symbol:** △ (amber, `#f59e0b`)

## Behaviors

- Writes specs as communication artifacts, not tickets. Thinks in prose, not bullet points.
- Uses AI agents (Claude Code, Copilot, Cursor) daily for implementation. Has internalized that coding speed is no longer the bottleneck.
- Notices when something is wrong before they can articulate why. Captures observations informally (notes, Slack messages, PR comments) that never get systematized.
- Reviews agent output critically — understands that spec quality determines execution quality.
- Builds mental models of systems before touching code. Visual thinker.

## Needs & Pain Points

- PP-001: Ceremony overhead consumes time that should go to discovery and specification. Sprint planning, standups, and grooming sessions optimize for predictability, not for the quality of what's being specified.
- PP-002: AI agents execute well-specified work in hours but most specs are too ambiguous. The gap is not agent capability — it's specification quality. When the agent builds the wrong thing, the spec failed.
- PP-003: No systematic way to compile domain knowledge into agent-ready specifications. Research sits in docs, Slack, and heads. Personas are slide-deck artifacts, not living compilations. Journey maps decay the moment they're drawn.
- PP-004: Observations from running code don't feed back into domain understanding. The team learns things in production (user behavior, edge cases, broken assumptions) but has no mechanism to update the domain model. Single-loop learning only.

## Evidence

- [Intent Methodology v1](../raw/research/2026-03-28-intent-methodology-v1.md) — "When an AI agent can implement a well-specified feature in hours — not sprints — the entire gravitational center of the SDLC shifts left."
- [Three-Layer Architecture](../raw/research/2026-04-05-three-layer-architecture-formalized.md) — Cagan mapping: discovery = Layer 1, delivery = Layer 3, trust-gated autonomy maps to team empowerment.
- Ari conversation (founding empirical evidence): "Their tickets became specifications for bots to run."
- Intent's four-persona model defines this as the primary adoption persona.

## Open Questions

- What's the minimum viable knowledge base size before a practitioner-architect feels the compilation payoff?
- How do they currently share domain knowledge with agents? What's the workaround today?
- At what team size does the practitioner-architect need to delegate knowledge base curation vs. doing it themselves?
