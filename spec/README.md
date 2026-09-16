---
title: Readme
type: framework
maturity: final
confidentiality: shareable
reusability: universal
domains:
  - consulting-operations
created: 2026-03-29
depth_score: 2
depth_signals:
  file_size_kb: 1.5
  content_chars: 1232
  entity_count: 0
  slide_count: 0
  sheet_count: 0
  topic_count: 1
  has_summary: 0
vocab_density: 0.00
---
# Spec

> Shaped specifications — the team's highest-leverage work.

A spec is the unit of work. Not a ticket. Not a story. A *specification* that communicates intent clearly enough for an autonomous agent (human or AI) to execute against it.

Every spec has three parts:

| Part | Question | Purpose |
|------|----------|--------|
| **Intent** | Why are we doing this? | The outcome sought, the problem being solved, who benefits |
| **Shape** | What does good look like? | Constraints, boundaries, key interactions, design principles |
| **Contract** | How do we know it's done? | Acceptance criteria, what must not break, validation rules |

A good spec is the shortest document that makes the agent dangerous.

---

## Quality Heuristic

If the agent executes and the result is wrong, the spec failed — not the agent. This inverts the traditional blame model. The time you spend shaping the spec is the time you used to spend in refinement, code review, and rework — but concentrated where it has the highest leverage.

## What Lives Here

- **intent-methodology.md** — The Intent methodology spec
- **autonomous-operations-design.md** — The operations layer spec
- **intent-concept-brief.md** — The product concept spec

### Operators

An operator is a named instrument that runs *on* the work-ontology artifacts rather than
producing one. Operators live here beside the methodology specs; they do not get their own
directory and they do not get product names.

| Operator | Spec | What it scans |
|---|---|---|
| Seam decomposition | `SPEC-INTENT-SEAM-DECOMPOSITION-001.md` | The fan-out topology: one frozen Contract per sortie, so collision is designed out |
| Typed evaluation verdicts | `typed-evaluation-verdicts.md` | Every `observation.evaluated` verdict, typing it by criterion provenance so self-graded evaluation cannot close a spec |
| Projection divergence | `SPEC-INTENT-PROJECTION-DIVERGENCE-001.md` | One intent across work-ontology levels 1 to 4, measuring what the Spec loses on its way down to a checkable Contract. A differential amplifier for intent: rejects common mode, amplifies the differential, emits Signals at comparator crossings and `amplification_score` nudges in between |
