---
id: JRN-001
type: journey
created: 2026-04-05
updated: 2026-04-05
depth_score: 2
depth_signals:
  file_size_kb: 4.1
  content_chars: 3783
  entity_count: 0
  slide_count: 0
  sheet_count: 0
  topic_count: 0
  has_summary: 0
vocab_density: 1.06
name: Adopting Intent as Team Operating Model
persona: PER-001
confidence: 0.60
origin: agent
sources:
  - raw/research/2026-03-28-intent-methodology-v1.md
  - raw/research/2026-04-05-three-layer-architecture-formalized.md
related_decisions:
  - DDR-001
  - DDR-002
  - DDR-003
---
# Journey: Adopting Intent as Team Operating Model

## Overview

A [[PER-001-practitioner-architect]] recognizes that Agile ceremonies are optimizing for a constraint (delivery speed) that AI has dissolved. They discover Intent, adopt it for their team, and evolve from ceremony-driven coordination to a continuous loop with compiled domain knowledge.

Start: Frustration with sprint overhead + AI agent adoption
End: Team operating on Notice→Spec→Execute→Observe loop with a living compiled knowledge base

## Stages

### Stage: Notice the Gap

- **Steps:** Practitioner notices that AI agents execute well-specified work in hours but most specs are ambiguous. Sprint ceremonies feel disconnected from the actual work. Tickets track status, not intent.
- **Emotions:** Frustration, recognition ("I knew something was off"), excitement ("there might be a better way")
- **Pain points:** PER-001/PP-001, PER-001/PP-002
- **Touchpoints:** AI coding tools (Claude Code, Cursor), Jira/Linear, team standup
- **Moment:** The moment they realize the agent built exactly the wrong thing — and it was the spec's fault, not the agent's.

### Stage: Discover Intent

- **Steps:** Finds Intent through thought leadership content (blog, talk, peer recommendation). Reads the methodology. Recognizes their own experience in the shift description. Reads the Karpathy connection.
- **Emotions:** Validation ("someone named the thing I've been feeling"), curiosity
- **Pain points:** None — this is the relief stage
- **Touchpoints:** Intent site, methodology page, concept brief

### Stage: Scaffold

- **Steps:** Adds `.intent/` to their repo. Captures first signals. Uses CLI tools. Gets the team to try a single spec-driven cycle instead of a sprint.
- **Emotions:** Cautious optimism, mild friction ("where does this replace what we already do?")
- **Pain points:** Learning curve of new artifact types. Explaining to teammates who haven't felt the shift yet.
- **Touchpoints:** `intent-signal`, `intent-spec`, `.intent/` directory, team Slack

### Stage: Compile Understanding

- **Steps:** Drops research (user interviews, analytics, competitor docs) into `raw/`. Runs ingest. Watches the knowledge base compile personas, journeys, DDRs. Queries the knowledge base during spec authoring. Experiences the first "the knowledge base knew something I'd forgotten" moment.
- **Emotions:** Delight ("this is the compilation payoff"), growing trust
- **Pain points:** PER-001/PP-003 (now being addressed)
- **Touchpoints:** `raw/`, `knowledge/`, knowledge-engine/AGENTS.md operations

### Stage: Observe and Learn

- **Steps:** Code ships. Observations flow back. Knowledge lint surfaces a contradiction between persona assumptions and actual user behavior. Persona confidence drops. Journey map gets revised. DDR gets validated or invalidated.
- **Emotions:** Insight ("we were wrong about X"), confidence in the system
- **Pain points:** PER-001/PP-004 (now being addressed)
- **Touchpoints:** `observations/`, knowledge base updates, lint output

## Moments of Truth

1. **First spec failure:** Agent builds wrong thing → practitioner realizes the spec was ambiguous, not the agent broken. This is the moment they understand THM-002.
2. **First compilation payoff:** Query returns an answer with citations to compiled artifacts the practitioner had forgotten about. The knowledge base knows more than any individual.
3. **First double-loop learning:** Observation contradicts a persona assumption → knowledge base updates → next spec is better because the domain model is better. The system questioned its own assumptions.

## Evidence

- [Intent Methodology v1](../raw/research/2026-03-28-intent-methodology-v1.md) — Ari's team discovered this journey empirically
- [Three-Layer Architecture](../raw/research/2026-04-05-three-layer-architecture-formalized.md) — Frameworks mapped to each stage
