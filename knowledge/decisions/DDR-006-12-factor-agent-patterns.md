---
title: 12-Factor Agent Pattern Integration
id: DDR-006
created: 2026-04-13
frameworks:
  - double-loop-learning
depth_score: 4
depth_signals:
  file_size_kb: 3.9
  content_chars: 3706
  entity_count: 1
  slide_count: 0
  sheet_count: 0
  topic_count: 0
  has_summary: 0
vocab_density: 0.27
status: decided
---
# DDR-006: 12-Factor Agent Pattern Integration

## Context

The [12-factor-agents](https://github.com/humanlayer/12-factor-agents) manifesto (HumanLayer/Dex) codifies 12+1 principles for building production LLM agents. A systematic mapping against Intent's architecture (see `knowledge-engine/analysis/12-factor-mapping.md`) identified 5 gaps where 12-factor covers territory Intent didn't.

The two frameworks operate at different altitudes: 12-factor is agent-implementation-level (how to build one agent well); Intent is operating-model-level (how to orchestrate a system of work). They stack cleanly — the question was whether to adopt the repo, rewrite our stack, or extract concepts.

## Decision

**Concept extraction, not adoption.** We integrated the 5 identified gaps as targeted additions to Intent's existing specs, event catalog, trust framework, and architecture docs. No external code was brought in. No structural redesign.

### What was added

| Gap | Resolution | Files Modified |
|-----|-----------|----------------|
| G1: Pause/Resume | `execution.paused` + `execution.resumed` events, checkpoint serialization schema, TTL + fallback semantics | event-catalog.md, SPEC-003, models.py |
| G2: Human Contact as Capability | `request_human_input` signal type (distinct from governance gates), `human_input.requested` + `human_input.received` events, urgency routing | signal-trust-framework.md, event-catalog.md, models.py |
| G3: LLM-as-Judge | `observation.evaluated` event, evaluation schema with multi-dimensional scoring, semantic gap detection → signal feedback | event-catalog.md, models.py |
| G4: Error-Retry-Escalate | `execution.error_retry` + `execution.escalated` events, retry cap + trust-aware escalation pattern | event-catalog.md, models.py |
| G5: State Philosophy | New "State Philosophy" section documenting stateful-system / stateless-invocation resolution, context resolver as bridge | ARCHITECTURE.md |

### New contracts

- **CON-012:** Checkpoint validity (TTL enforcement, span_id linkage)
- **CON-013:** Human input request independence (emittable at any trust level, urgency-aware pausing)
- **CON-014:** LLM-as-judge semantic gap detection (fail/conditional_pass → signal emission)

## Alternatives Considered

1. **Adopt the 12-factor repo as-is** — Rejected. It's a manifesto (prose), not a library. No code to adopt. Our framework operates at a higher altitude.
2. **Rewrite Intent to conform to 12-factor** — Rejected. Intent already covers or exceeds 12-factor in most areas (trust-gated autonomy, multi-agent orchestration, knowledge compilation, federation, signal amplification, persona-driven prompts, double-loop learning). Rewriting would be a downgrade.
3. **Ignore it** — Rejected. The 5 gaps were real, particularly G1 (pause/resume) and G2 (human contact as capability).

## Consequences

- Event catalog grows from 15 to 22 events (7 new)
- SPEC-003 gains Extension 5 (checkpoint primitive) and 3 new contracts (CON-012 through CON-014)
- Trust framework now has a dual model: governance gates (mandatory, top-down) + strategic requests (voluntary, bottom-up)
- Observe phase gains LLM-as-judge capability, closing the gap between mechanical contract verification and semantic spec satisfaction
- The state philosophy section makes explicit what was previously implicit about Intent's state model

## Validation Criteria

- [ ] All 22 events parseable by existing JSONL schema
- [ ] `request_human_input` signal emittable at L0-L4 (CON-013)
- [ ] Checkpoint TTL enforcement works (CON-012)
- [ ] LLM-as-judge fail verdict produces signal (CON-014)
- [ ] models.py EVENT_TYPES set matches event catalog count
