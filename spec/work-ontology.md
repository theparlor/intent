# Work Ontology

> The seven-level hierarchy that replaces tickets: Signal → Intent → Spec → Contract → Capability → Feature → Product. With three governance dimensions and an Agile comparison.

## Why an Ontology?

Agile's work unit is the "story" — a prose description of a user need. Stories are sorted into a backlog, estimated in points, and assigned to sprints. This worked when implementation was expensive and humans did all of it.

When AI collapses implementation from weeks to hours, stories become insufficient. Agents need verifiable contracts, not narrative descriptions. Teams need to see the whole hierarchy — from a raw observation to a shipped product — not just the next sprint's worth of tickets.

The work ontology is Intent's answer: a seven-level hierarchy where every level has a clear purpose, a clear owner, and clear transitions to the levels above and below.

## The Seven Levels

```
Signal
  ↓
Intent
  ↓
Spec
  ↓
Contract
  ↓
Capability
  ↓
Feature
  ↓
Product
```

### 1. Signal

Observations from work, research, conversation. Raw input. The atomic unit of "we noticed something."

Each signal carries a confidence score (how sure are we this matters?), a source (where did this come from?), and links to related intents. Multiple signals may point to the same intent — that convergence is itself a signal.

**Replaces:** Backlog items, feature requests, bug reports (when used as observation)
**Owner:** Anyone (signals come from all disciplines)
**Transitions to:** Intent (when someone decides this observation is worth acting on)

### 2. Intent

What we want to change. Declarative: "Users should be able to X." Connects signals to specs.

An intent is not a task. It's a declaration of desired change. It doesn't say how — it says what and why. One intent may spawn multiple specs. An intent can exist for weeks before anyone writes a spec for it, and that's fine — it's a placeholder for team attention.

**Replaces:** Epics, themes, OKR-level objectives
**Owner:** Product-Minded Leader (PM)
**Transitions to:** Spec (when the intent is approved and someone shapes it)

### 3. Spec

How we'll change it. Narrative + acceptance criteria. Humans write specs; agents use them as execution instructions.

The spec is the primary handoff artifact. It's written in prose (for humans to understand) with embedded assertions (for agents to verify). A good spec is readable as a document and executable as a contract.

**Replaces:** User stories, PRDs, technical design docs
**Owner:** Practitioner-Architect + Design-Quality Advocate (collaborative)
**Transitions to:** Contract (assertions extracted and made executable)

### 4. Contract

Verifiable assertions. The spec's acceptance criteria extracted and made machine-executable. A contract is "done" when all assertions pass.

Contracts are what make Intent deterministic. Instead of "the feature should feel fast," a contract says: "p95 latency < 200ms for the /api/search endpoint under 100 concurrent requests." Agents can execute against this. Humans can verify it.

**Replaces:** Acceptance criteria, definition of done, QA test plans
**Owner:** AI Agent (executes), Design-Quality Advocate (validates)
**Transitions to:** Capability (when contract passes and code is merged)

### 5. Capability

Building blocks. Reusable functions, components, patterns that contracts are composed of. A capability is a durable asset — it exists beyond the contract that created it.

**Replaces:** Components, services, libraries (the organizational framing, not the code itself)
**Owner:** Practitioner-Architect
**Transitions to:** Feature (when capabilities compose into user-facing behavior)

### 6. Feature

User-facing unit. One or more capabilities working together. Released to production. The thing users actually interact with.

**Replaces:** Features (same concept, different governance)
**Owner:** Product-Minded Leader + Design-Quality Advocate
**Transitions to:** Product (when features compose into a coherent offering)

### 7. Product

System. Multiple features forming a coherent offering. The top of the hierarchy — the thing the team is building.

**Owner:** Everyone

## Three Governance Dimensions

Work in Intent is governed across three orthogonal dimensions:

### Time Dimension
Continuous flow. No sprints. Work moves when dependencies resolve, not on calendar boundaries. The unit of time isn't "this sprint" — it's "this intent's lifecycle." Some intents resolve in hours. Some take weeks. Both are fine.

### Quality Dimension
Contracts are the source of truth. Code and design conform to contracts, not the reverse. Quality isn't a phase or a gate — it's a property of every level. A signal with low confidence is low-quality input. A spec without verifiable assertions is low-quality specification. A contract with passing assertions is high-quality output.

### Visibility Dimension
OpenTelemetry-compatible events at every transition. Work is observable at all times. The team never has to ask "what's the status?" — the event stream tells them. This replaces standups, status meetings, and the weekly "where are we?" conversations.

## Versus Agile

| Concept | Agile | Intent |
|---------|-------|--------|
| Work unit | Story (prose) | Contract (verifiable) |
| Organization | Sprint (time-boxed) | Intent (outcome-boxed) |
| Coordination | Ceremonies (standup, retro) | Events (observable) |
| Estimation | Points (guess) | Observation (actual) |
| Quality | QA phase | Contract assertion |
| Backlog | Prioritized list | Signal stream |
| Status | Standup report | Event dashboard |
| Learning | Retrospective | Observe cycle |

What Agile gets right and Intent keeps: cross-functional teams, iterative delivery, user focus, working software over documentation. What Intent changes: the coordination model, the work unit, the feedback mechanism, and the relationship between humans and AI.

## Where This Lives

- **Interactive artifact:** [Work System (React)](../artifacts/intent-work-system.jsx)
- **Site page:** [work-system.html](../docs/work-system.html)
