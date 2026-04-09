---
title: Intent Methodology
type: spec
maturity: draft
created: 2026-03-28
thought_leaders:
  - jeff-patton
  - teresa-torres
summary: "A spec-driven SDLC for the AI-augmented practitioner. Replaces Agile ceremony overhead with a continuous loop — notice, spec, execute, observe — where specification quality is the bottleneck, not delivery velocity."
depth_score: 5
depth_signals:
  file_size_kb: 9.5
  content_chars: 8223
  entity_count: 2
  slide_count: 0
  sheet_count: 0
  topic_count: 0
  has_summary: 1
vocab_density: 0.62
related_entities:
  - {pair: teresa-torres ↔ marty-cagan, count: 82, strength: 0.3}
  - {pair: jeff-patton ↔ marty-cagan, count: 63, strength: 0.24}
  - {pair: teresa-torres ↔ consulting-operations, count: 62, strength: 0.031}
  - {pair: teresa-torres ↔ jeff-patton, count: 60, strength: 0.368}
  - {pair: jeff-patton ↔ consulting-operations, count: 47, strength: 0.024}
---
# Intent Methodology

> **Purpose**: How work flows from idea to running software when AI collapses implementation to hours.
>
> **Version**: 1.0 — 2026-03-28
>
> **Origin**: A conversation with engineer Ari, who described his team's empirical discovery of the same shift — then pressure-tested against Cagan's product model, Patton's story mapping, and Torres' continuous discovery.

---

## The Shift

For thirty years, software development methodology has been organized around a single assumption: *implementation is the bottleneck*. Waterfall managed it with upfront planning. Agile managed it with iterative delivery. Scrum managed it with two-week timebox ceremonies that make the slow, expensive act of building software legible to the business.

That assumption is breaking.

When an AI agent can implement a well-specified feature in hours — not sprints — the entire gravitational center of the SDLC shifts left. The hard problem was never delivery. It was always discovery. Cagan has been saying this for years: the best teams spend their energy on figuring out *what to build and why*, not on managing the mechanics of building it. AI just made the argument undeniable.

Here's what collapses when implementation gets fast:

| Ceremony | Original Purpose | What Happens When Implementation Is Hours |
|----------|-----------------|------------------------------------------|
| Sprint Planning | Forecast what fits in two weeks | Irrelevant — there's nothing to forecast when the unit of work is a spec, not a sprint |
| Daily Standup | Surface blockers across a team | No team to coordinate. Blockers are spec ambiguity, not resource contention |
| Velocity Tracking | Predict future throughput | Throughput is no longer the constraint. Spec quality is |
| Backlog Grooming | Prioritize and size upcoming work | Sizing is meaningless. Prioritization still matters — but it's strategic, not operational |
| Sprint Review | Demo what shipped | Ship continuously. Observe continuously. No artificial ceremony boundary |
| Retrospective | Improve team process | Still valuable — but the unit of reflection is the spec-execute-observe cycle, not the sprint |

Ari's team discovered this empirically. Their tickets became "specifications for bots to run." Their refinement meetings became "heavily design oriented." Their PRDs moved outside Jira because the tool was optimizing for tracking status, not communicating intent.

---

## The Loop

```
        ┌──────────┐
        │  NOTICE  │ ← Something is broken, missing, or possible
        └────┬─────┘
             │
             ▼
        ┌──────────┐
        │   SPEC   │ ← Crystallize into Intent → Shape → Contract
        └────┬─────┘
             │
             ▼
        ┌──────────┐
        │ EXECUTE  │ ← Agent builds against the spec
        └────┬─────┘
             │
             ▼
        ┌──────────┐
        │ OBSERVE  │ ← Does reality match the contract?
        └────┬─────┘
             │
             └──────────→ back to NOTICE
```

### Notice

The first phase is *paying attention*. A notice is anything that creates a gap between the world as it is and the world as it should be. The discipline is *not* to jump straight to solutions. When two or three notices cluster around the same area, a spec is warranted.

This is the Patton insight: don't start with the solution. Start with the story of what's happening and who it's happening to.

### Spec

The spec is the unit of work. Three parts:

**Intent** — Why it matters now and what outcome you want. Think Seiden: *what behavior changes? What becomes true that wasn't?*

**Shape** — The architect's fat-marker sketch. Boundaries (in/out), key decisions already made, open questions. Think Shape Up: appetite set, approach sketched, details left to the builder.

**Contract** — How we know it's done. Observable outcomes, not task checkboxes. A smoke test the agent can run.

A good spec is the shortest document that makes the agent dangerous.

**Quality heuristic**: If the agent executes and the result is wrong, the spec failed — not the agent.

### Execute

The agent builds against the spec. Key principle: **the agent can make implementation decisions the architect didn't specify.** The spec draws the boundaries. Inside those boundaries, the agent has autonomy.

### Observe

Check reality against the contract. But also notice *new* things: edge cases the spec missed, architectural questions surfaced, adjacent workflows affected. Those observations feed back into Notice.

---

## The Toolchain

```
  NOTICE          SPEC            EXECUTE         OBSERVE
  ┌──────────┐   ┌──────────┐   ┌──────────┐   ┌──────────┐
  │NotebookLM│   │  Cowork  │   │Claude Code│   │ Entire.io│
  │ research │   │ strategy │   │   CLI     │   │ observe  │
  │ synthesis│   │ shaping  │   │ execution │   │ reasoning│
  └──────────┘   └──────────┘   └──────────┘   └──────────┘

  ┌──────────────────────────────────────────────────────────┐
  │              Git + GitHub — source of truth               │
  └──────────────────────────────────────────────────────────┘
  ┌──────────────────────────────────────────────────────────┐
  │         launchd — scheduling for autonomous ops           │
  └──────────────────────────────────────────────────────────┘
```

| Tool | Role | Analogy |
|------|------|---------|
| **NotebookLM** | Research and synthesis before shaping | The library |
| **Cowork** | Strategy, spec authoring, architecture review | The architect's table |
| **Claude Code CLI** | Autonomous execution, building, nightly ops | The workshop floor |
| **Entire.io** | Agent observability alongside git commits | The black box recorder |
| **Git + GitHub** | Source of truth for code, specs, and design docs | The vault |
| **launchd** | Native macOS scheduling for autonomous workflows | The clock |

---

## What Replaces What

| Traditional Artifact | Replacement | Why |
|---------------------|-------------|-----|
| Jira ticket | Spec file (Intent / Shape / Contract) | A ticket tracks status. A spec communicates intent |
| Sprint backlog | `TASKS.md` | Priority-ordered. No velocity, no points, no sprint boundary |
| Epic / initiative | Design doc | Narrative-scale thinking in prose, not a ticket hierarchy |
| Status tracking | Git history + Entire.io | Commits are ground truth. Entire.io adds the *why* |
| Sprint review | Observe phase | Continuous, not ceremonial |
| Retrospective | Spec quality feedback loop | "What was missing from the spec?" |

### What's Kept

**Iterative delivery** — the loop is iterative. The boundary is the spec, not the sprint.

**Working software as measure of progress** — the contract makes this explicit.

**Responding to change** — Notice is designed for this. No waiting for the next sprint.

**Sustainable pace** — don't spec faster than you can observe.

---

## Heuristics

**When to spec vs. just do it**: If the agent needs to make decisions you haven't thought through, write a spec.

**When a spec is failing**: Execution is technically correct but wrong in spirit. Sharpen the shape.

**When to break a spec**: If you can't write a meaningful smoke test, the spec is too big.

**When to abandon a spec**: If the Intent is no longer the right goal, don't rework — write a new one.

---

## How This Scales

**Two people**: Specs are the coordination mechanism. Conflicts surface in the Shape section.

**Small team (3-5)**: Design docs become the coordination layer. Weekly sync, not daily.

**The limit**: Breaks down when coordination cost exceeds specification cost. With AI agents, that breakpoint is higher than it used to be.

---

*Intent Methodology v1.0 — 2026-03-28*
*Origin: Cowork session, grounded in Ari conversation and Cagan/Patton/Torres/Seiden frameworks*