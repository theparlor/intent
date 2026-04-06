---
title: Federate knowledge base across Core and bounded engagements using inherit/promote/isolate flows
id: DDR-004
type: decision
created: 2026-04-05
updated: 2026-04-05
depth_score: 2
depth_signals:
  file_size_kb: 3.3
  content_chars: 3009
  entity_count: 0
  slide_count: 0
  sheet_count: 0
  topic_count: 0
  has_summary: 0
vocab_density: 0.33
status: accepted
confidence: 0.85
origin: human
addresses:
  - PER-001/PP-003
persona: PER-001
journey_stage: JRN-001#compile-understanding
sources:
  - raw/research/2026-04-05-three-layer-architecture-formalized.md
---
# DDR: Federated Knowledge Base Architecture

## Context

Intent's three-layer architecture works for a single project. Brien's practice operates multiple concurrent engagements plus a Core IP library. Each engagement needs its own domain knowledge base (client-specific personas, journeys, DDRs) but should benefit from Core improvements and contribute generalizable insights back.

Brien already solves an analogous problem with his federated glossary architecture: org-specific terms stay in each engagement's `glossary.md`, general terms live in `memory/glossary.md`. This is the same pattern extended to the full three-layer architecture.

## Decision

Three directional flows govern the federation:

1. **Inherit Down (Core → Engagement):** Engagements inherit Core schema (knowledge-engine/AGENTS.md), templates, archetypes, and universal themes via `Core:ID` references and a `_core_refs.md` inheritance manifest.

2. **Promote Up (Engagement → Core):** Generalizable insights are sanitized (strip client names, metrics, individuals) and promoted to Core knowledge base. Requires pattern recognition across 2+ engagements, or single-engagement evidence that's clearly universal.

3. **Never Leak Sideways (Engagement ↛ Engagement):** Client-specific content never flows directly between engagements. Cross-pollination goes through Core as the sanitization layer.

Maps to Beer's VSM: Core = System 4+5 (intelligence + identity), engagements = System 1 (operations), federation = System 2+3 (coordination + management).

## Alternatives Considered

| Alternative | Pros | Cons | Why Rejected |
|-------------|------|------|-------------|
| Monolithic knowledge base (all engagements in one) | Simplest, maximum cross-pollination | NDA violations, confidentiality nightmare | Non-starter for consulting practice |
| Fully isolated (no inheritance) | Maximum safety | Each engagement starts from zero, no compounding | Defeats the purpose of a practice |
| Copy-based inheritance (snapshot Core into engagement) | Works offline | Creates stale copies that drift from Core | Reference-based inheritance is better |

## Consequences

**Positive:**
- Every engagement benefits from accumulated Core intelligence
- Core grows richer with each engagement (compounding practice knowledge)
- Confidentiality boundaries are enforced by architecture, not discipline
- Mirrors Brien's existing Workspaces topology (familiar, proven)

**Negative:**
- Promotion requires sanitization effort (cost of moving insight to Core)
- Reference-based inheritance requires Core to be accessible (not offline)
- More complex than a single-knowledge-base setup

## Validation Criteria

- [ ] First engagement knowledge base scaffolded with `_core_refs.md` referencing Core archetypes
- [ ] First promotion from engagement to Core with sanitized artifact
- [ ] Lint catches a cross-engagement reference as a confidentiality violation
- [ ] Core template update is available to new engagement without manual distribution
