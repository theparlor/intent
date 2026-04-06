---
title: Full bidirectional coupling between all three layers (not unidirectional feed)
id: DDR-003
type: decision
created: 2026-04-05
updated: 2026-04-05
depth_score: 2
depth_signals:
  file_size_kb: 2.9
  content_chars: 2584
  entity_count: 0
  slide_count: 0
  sheet_count: 0
  topic_count: 0
  has_summary: 0
vocab_density: 0.77
status: accepted
confidence: 0.80
origin: human
addresses:
  - PER-001/PP-004
persona: PER-001
journey_stage: JRN-001#observe-learn
sources:
  - raw/research/2026-04-05-three-layer-architecture-formalized.md
---
# DDR: Full Bidirectional Coupling

## Context

The three-layer architecture could be coupled in multiple ways:
- **Unidirectional:** Raw → Knowledge → Loop → Specs → Code. Simple pipeline. No feedback.
- **Partially bidirectional:** Observations feed back to specs (single-loop) but not to the knowledge base.
- **Fully bidirectional:** All six flows active. Observations update the knowledge base (double-loop). Knowledge lint surfaces signals. Spec authoring queries the knowledge base.

Brien chose full bidirectional coupling based on Argyris' double-loop learning theory and Beer's 3-4 Homeostat concept.

## Decision

All six data flows are active and bidirectional:

1. Knowledge → Notice (lint surfaces signals)
2. Notice → Spec (queries knowledge base during authoring)
3. Spec → Execute (trust-gated agents)
4. Execute → Observe (events emitted)
5. **Observe → Knowledge (double-loop)** — observations update personas, journeys, DDRs
6. Observe → Specs (single-loop) — spec drift detection

Flow 5 is the critical path. Without it, the system can optimize execution but never question whether it's building the right thing.

## Alternatives Considered

| Alternative | Pros | Cons | Why Rejected |
|-------------|------|------|-------------|
| Unidirectional pipeline | Simplest to implement | No learning. Knowledge base becomes a static artifact. | Defeats the purpose of a living knowledge base |
| Single-loop only (Flow 6) | Simpler, still provides feedback | Can only optimize HOW it builds, not WHAT it builds | Argyris: this is the trap of single-loop learning |
| Full bidirectional | Richest learning, most adaptive | Most complex, requires all six flows | **Selected** — the complexity is the point |

## Consequences

**Positive:**
- System questions its own assumptions (double-loop)
- Knowledge base grows more accurate over time through empirical validation
- Boyd's shared orientation: agents sharing the knowledge base can act autonomously with less coordination

**Negative:**
- Six flows to implement and maintain
- Risk of feedback loops that amplify errors (hallucination compounding)
- Requires the observe phase to be sophisticated enough to detect domain-model-level insights, not just system metrics

## Validation Criteria

- [ ] A user behavior observation triggers a persona confidence decrease (Flow 5 working)
- [ ] A DDR's validation criteria are checked against observation data and the DDR status updates accordingly
- [ ] Knowledge lint produces a signal that leads to a spec that produces code that produces observations that update the knowledge base (full loop)
