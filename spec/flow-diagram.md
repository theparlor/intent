---
title: Flow Diagram
type: framework
maturity: final
confidentiality: shareable
reusability: universal
domains:
  - consulting-operations
created: 2026-03-31
depth_score: 4
depth_signals:
  file_size_kb: 6.9
  content_chars: 6615
  entity_count: 0
  slide_count: 0
  sheet_count: 0
  topic_count: 1
  has_summary: 0
vocab_density: 0.15
---
# Flow Diagram

> Five concrete paths through the system with personas (Architect, PM, Design/QA, Agent) and event triggers at every transition.

## Why Flow Paths?

The Intent loop (Notice → Spec → Execute → Observe) is a model. Flow paths are what the model looks like in practice. Each path traces a specific scenario through the system, showing which personas are involved at each step, what events fire, and where the work goes next.

Flow paths answer the question practitioners always ask: "But what does this actually look like day-to-day?"

## The Four Personas

Intent recognizes four distinct personas who interact with the system differently:

### △ Practitioner-Architect (amber)
Senior ICs who see the system as a whole. They capture signals from execution patterns, write specs with architectural context, and review contracts for structural integrity. Primary phases: Notice, Spec.

### ◇ Product-Minded Leader (blue)
PMs who connect business signals to technical intents. They review signal confidence, approve intents for spec, and use observation data for stakeholder communication. Primary phases: Notice, Observe.

### ○ Design-Quality Advocate (purple)
Designers and QA who ensure specs are complete and contracts are verifiable. They write acceptance criteria, validate contract assertions, and flag quality issues in observation. Primary phases: Spec, Observe.

### ◉ AI Agent (green)
Claude Code, GitHub Actions, Entire.io — automated actors that execute contracts, emit events, and close traces. Primary phases: Execute, Observe.

## The Five Paths

### Path 1: Happy Path — Signal to Feature

The straightforward path from observation to shipped code.

1. **Notice:** Architect notices a pattern in agent traces → `signal.created`
2. **Notice:** PM reviews signal, links to intent → `intent.proposed`
3. **Notice:** PM approves intent to proceed → `intent.approved`
4. **Spec:** Architect writes spec with narrative and acceptance criteria → `spec.written`
5. **Spec:** Design/QA reviews, adds contract assertions → `spec.staged`
6. **Execute:** Agent picks up staged spec, begins work → `contract.started`
7. **Execute:** Agent runs assertions as it builds → `contract.assertion.passed`
8. **Execute:** All assertions pass → `contract.completed`
9. **Execute:** Capability ships → `capability.released`
10. **Execute:** Feature goes live → `feature.released`
11. **Observe:** Entire.io aggregates traces → `trace.completed`
12. **Observe:** Observation layer reads traces, writes findings → `observation.written`
13. **Notice:** Findings feed back as new signals → loop continues

### Path 2: Contract Failure Feedback Loop

What happens when an assertion fails — the system's self-correcting mechanism.

1. **Execute:** Agent working on contract → `contract.started`
2. **Execute:** An assertion fails → `contract.assertion.failed`
3. **Observe:** Failure triggers observation → `observation.written`
4. **Notice:** Observation surfaces as signal: "Contract assertions may be underspecified" → `signal.created`
5. **Spec:** Architect or Design/QA revisits spec, tightens criteria → `spec.written` (update)
6. **Spec:** Updated spec re-staged → `spec.staged`
7. **Execute:** Agent re-executes against tightened contract → `contract.started`

This loop is why Intent improves over time. Failures don't just get fixed — they improve the spec quality for future work.

### Path 3: Governance Escalation

When observation reveals something that needs human judgment, not just re-execution.

1. **Observe:** System health check reveals velocity drop → `system.health`
2. **Notice:** PM reviews health metrics, identifies intent that's stalled → `signal.created`
3. **Notice:** PM proposes corrective intent → `intent.proposed`
4. **Spec:** Team collaborates on root cause analysis, writes investigative spec → `spec.written`
5. **Spec:** Decision recorded about process change → `decision.recorded`
6. **Observe:** Team monitors whether intervention worked → `observation.written`

### Path 4: External Signal

Signals that originate outside the development workflow.

1. **Notice:** Customer support ticket flagged via Zapier → `signal.created`
2. **Notice:** PM triages signal, links to existing intent or creates new one → `intent.proposed`
3. **Notice:** Architect validates technical feasibility → `intent.approved`
4. **Spec → Execute → Observe:** Normal flow continues from here

This path demonstrates Intent's open boundary — signals aren't just internal observations. They flow in from any surface where the team interacts with reality.

### Path 5: Autonomous Pipeline

Fully automated flow where agents close the loop without human intervention.

1. **Observe:** Scheduled health check emits metrics → `system.health`
2. **Notice:** Agent reads metrics, identifies pattern → `signal.created`
3. **Spec:** Agent proposes spec from existing template → `spec.written`
4. **Spec:** Auto-staged (meets confidence threshold) → `spec.staged`
5. **Execute:** Agent executes → `contract.started` → `contract.completed`
6. **Observe:** Traces captured → `trace.completed`

This is the aspirational end state: the loop runs continuously with human oversight at governance checkpoints but autonomous execution for well-understood patterns.

## Trigger Matrix

Every event in the system has a trigger — the condition that causes it to fire. The trigger matrix maps events to their triggers, the phases they belong to, and which paths they appear in.

| Event | Phase | Trigger | Paths |
|-------|-------|---------|-------|
| `signal.created` | Notice | PR merge, Zapier, agent observation | 1, 2, 3, 4, 5 |
| `intent.proposed` | Notice | PM creates intent file | 1, 3, 4 |
| `intent.approved` | Notice | PR review approved | 1, 4 |
| `spec.written` | Spec | PR merged with spec | 1, 2, 3, 5 |
| `spec.staged` | Spec | Label/status change | 1, 2, 5 |
| `decision.recorded` | Spec | Manual | 3 |
| `contract.started` | Execute | Agent session start | 1, 2, 5 |
| `contract.assertion.passed` | Execute | Test pass | 1 |
| `contract.assertion.failed` | Execute | Test fail | 2 |
| `contract.completed` | Execute | All assertions pass | 1, 5 |
| `capability.released` | Execute | PR merge | 1 |
| `feature.released` | Execute | Deploy | 1 |
| `trace.completed` | Observe | Entire.io hook | 1, 5 |
| `observation.written` | Observe | File watcher | 1, 2, 3 |
| `system.health` | Observe | Cron | 3, 5 |

## Where Flow Diagrams Live

- **Interactive artifact:** [Flow Diagram (React)](../artifacts/intent-flow-diagram.jsx)
- **Site page:** [flow-diagram.html](../docs/flow-diagram.html)
