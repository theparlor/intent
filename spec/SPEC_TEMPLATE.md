---
title: Spec Template
type: reference
maturity: final
confidentiality: shareable
reusability: universal
domains:
  - consulting-operations
created: 2026-03-28
technologies:
  - jira
  - slack
thought_leaders:
  - josh-seiden
depth_score: 4
depth_signals:
  file_size_kb: 4.3
  content_chars: 3588
  entity_count: 3
  slide_count: 0
  sheet_count: 0
  topic_count: 1
  has_summary: 0
vocab_density: 0.56
related_entities:
  - {pair: josh-seiden ↔ marty-cagan, count: 101, strength: 0.204}
  - {pair: josh-seiden ↔ teresa-torres, count: 88, strength: 0.203}
  - {pair: jeff-patton ↔ josh-seiden, count: 81, strength: 0.276}
  - {pair: josh-seiden ↔ outcomes-over-output, count: 68, strength: 0.364}
  - {pair: consulting-operations ↔ teresa-torres, count: 66, strength: 0.111}
---
# Spec Template: Intent → Shape → Contract

> The unit of work in the **Intent** methodology. This replaces the Jira ticket.
> A ticket tracks *status*. A spec communicates *intent*.
>
> Part of: [Intent: Development Operating System](../../../reference/DEVELOPMENT_OPERATING_SYSTEM.md) | [Intent Product Concept](../../../../Work/Lab/Pipeline/ideas/INTENT_CONCEPT_BRIEF.md)

---

## How to Use

Copy everything below the `---` line into a new file. Name it descriptively:
`specs/library-index-nightly-refresh.md`, `specs/workspace-health-check.md`, etc.

The spec serves two audiences simultaneously:
1. **You, later** — when you revisit and ask "why did I build this?"
2. **The agent** — when Claude Code needs enough context to execute autonomously.

A good spec is the shortest document that makes the agent dangerous.

---

<!-- COPY FROM HERE -->

# {Title}

> One sentence. What this is, in plain language.

**Status:** `draft` | `ready` | `in-flight` | `landed` | `parked`
**Created:** YYYY-MM-DD
**Last touched:** YYYY-MM-DD

---

## 1. Intent

_The "notice" crystallized. What you observed, why it matters, and the outcome you want. Write this for the version of you who forgot the context._

### What I Noticed

<!-- The trigger. What's broken, missing, or possible? What pain or opportunity surfaced? -->


### Why It Matters Now

<!-- Timing. Why this, why now? What's the cost of waiting? What does this unlock? -->


### Desired Outcome

<!-- One sentence. Not a feature description — a state of the world after this ships.
     Think Seiden: "What behavior changes? What becomes true that wasn't?" -->


---

## 2. Shape

_The architect's fat-marker sketch. Enough structure to constrain the solution, not so much that you're writing pseudocode. Think boundaries, not blueprints._

### Approach

<!-- How should this work, at the level of a whiteboard sketch? What's the mental model?
     Name the moving parts and how they relate. Analogies welcome. -->


### Boundaries

<!-- What's IN scope and what's explicitly OUT. Draw the fence. -->

**In:**
-

**Out:**
-

### Key Decisions

<!-- Choices you've already made that the agent shouldn't revisit.
     Architecture calls, library picks, patterns to follow or avoid. -->

-

### Open Questions

<!-- Things you haven't decided yet. If the agent hits one of these, it should stop and ask. -->

-

### Prior Art

<!-- Existing code, docs, or references the agent should read before starting.
     File paths, URLs, or "look at how X already works." -->

-

---

## 3. Contract

_How we know it's done. Observable outcomes, not task checkboxes. These are what the `observe` step checks against._

### Done When

<!-- Concrete, verifiable statements. Each one should be testable by running something,
     reading something, or observing something — not by opinion. -->

- [ ]
- [ ]
- [ ]

### Smoke Test

<!-- The single quickest way to verify this works end-to-end.
     "Run X, expect Y." The agent should be able to execute this. -->

```
```

### Failure Modes to Watch

<!-- What could go wrong? What should the agent check for or handle gracefully?
     Edge cases, known gotchas, things that broke last time. -->

-

### Observability

<!-- How will you know this keeps working after it ships?
     Logs, metrics, Entire.io traces, git evidence — whatever fits. -->

-

---

## Notes

<!-- Scratchpad. Context that doesn't fit above. Links to Granola transcripts,
     NotebookLM sessions, Slack threads, related specs. Anything the agent
     might need but that isn't part of the formal spec. -->

