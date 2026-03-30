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
