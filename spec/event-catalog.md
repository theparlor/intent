---
title: Event Catalog
type: framework
maturity: final
confidentiality: shareable
reusability: universal
domains:
  - consulting-operations
created: 2026-03-31
technologies:
  - slack
depth_score: 4
depth_signals:
  file_size_kb: 6.7
  content_chars: 6024
  entity_count: 1
  slide_count: 0
  sheet_count: 0
  topic_count: 1
  has_summary: 0
vocab_density: 0.33
related_entities:
  - {pair: consulting-operations ↔ subaru, count: 795, strength: 0.427}
  - {pair: consulting-operations ↔ automotive-manufacturing, count: 770, strength: 0.416}
  - {pair: consulting-operations ↔ engagement-management, count: 498, strength: 0.269}
  - {pair: consulting-operations ↔ turnberry, count: 448, strength: 0.224}
  - {pair: consulting-operations ↔ foot-locker, count: 251, strength: 0.136}
---
# Event Catalog

> 15 events, 6 emission mechanisms, OTel-compatible schema. What gets captured and how, from GitHub Actions to agent self-emission.

## Why Events?

Intent's observe layer depends on structured events flowing through the system. Without events, observation is manual — someone has to go look at what happened. With events, observation is automatic: the system tells you what happened, when, and in what context.

Events follow OpenTelemetry conventions. Every event includes a timestamp, source, trace ID (which Intent the work belongs to), and span context (parent-child relationships in the work hierarchy). This isn't just for compatibility with existing observability tools — it's because OTel's trace/span model is structurally isomorphic to how work flows through Intent.

## Event Schema

All events are stored in `.intent/events/events.jsonl` as newline-delimited JSON. Each event follows this schema:

```json
{
  "version": "0.1.0",
  "event": "signal.created",
  "timestamp": "2026-03-28T14:30:00Z",
  "trace_id": "intent-uuid",
  "span_id": "work-unit-uuid",
  "parent_id": "parent-span-uuid",
  "source": "github-action",
  "data": {
    "signal_id": "SIG-001",
    "confidence": 0.92,
    "title": "Work needs a formal ontology"
  }
}
```

Key fields:

- **version:** Schema version (semver). Current: 0.1.0
- **event:** Event name from the catalog below
- **timestamp:** ISO 8601
- **trace_id:** Maps to an Intent — all work units under one intent share a trace
- **span_id:** Unique ID for this specific work unit
- **parent_id:** The parent work unit (null for top-level)
- **source:** What emitted this event (github-action, agent, entire.io, manual, etc.)
- **data:** Event-specific payload

## The 15 Events

### Notice Phase

| Event | Description | Trigger |
|-------|-------------|--------|
| `signal.created` | New signal captured from work, research, or conversation | PR merged with file in `.intent/signals/` |
| `intent.proposed` | Intent created, linking signals to desired change | PR merged with file in `.intent/intents/` |
| `intent.approved` | Intent approved to proceed to spec | PR review approved on intent file |

### Spec Phase

| Event | Description | Trigger |
|-------|-------------|--------|
| `spec.written` | Spec created with narrative, acceptance criteria, and contract assertions | PR merged with file in `.intent/specs/` |
| `spec.staged` | Spec moves from draft to ready-for-execution | Label applied or status field changed |
| `decision.recorded` | Significant decision documented with context and rationale | Manual emission when decision is recorded |

### Execute Phase

| Event | Description | Trigger |
|-------|-------------|--------|
| `contract.started` | Agent begins executing a contract | Agent session start (self-emitting) |
| `contract.assertion.passed` | A contract assertion passes | Test runner (self-emitting agent) |
| `contract.assertion.failed` | A contract assertion fails | Test runner (self-emitting agent) |
| `contract.completed` | All assertions pass and contract is fulfilled | Agent session end (self-emitting) |
| `capability.released` | Reusable building block added to the system | PR merged with capability code |
| `feature.released` | Feature ships to production | Deployment pipeline |

### Observe Phase

| Event | Description | Trigger |
|-------|-------------|--------|
| `trace.completed` | Agent completes execution, all traces aggregated | Entire.io session hook |
| `observation.written` | Observe layer reads traces and writes findings | Log file watcher or scheduled job |
| `system.health` | Periodic emission of system health metrics | Scheduled cron (Zapier or GitHub Action) |

## Emission Mechanisms

Events don't all come from the same place. Intent uses 6 distinct emission mechanisms, reflecting the reality that work happens across many surfaces:

### 1. GitHub Action (9 events — 60% coverage)
The primary emission source. A GitHub Action watches for file changes in `.intent/` directories and emits the corresponding event. Covers: `signal.created`, `intent.proposed`, `intent.approved`, `spec.written`, `spec.staged`, `decision.recorded`, `capability.released`, `feature.released`, `system.health`.

### 2. Self-Emitting Agent (3 events)
AI agents emit events during execution. When Claude Code starts working on a contract, it writes `contract.started`. As assertions pass or fail, it writes `contract.assertion.passed` or `contract.assertion.failed`. When done, `contract.completed`. Requires agent instrumentation.

### 3. Entire.io Session Hook (1 event)
Entire.io captures end-to-end execution traces. When a session completes, it emits `trace.completed` with aggregated span data.

### 4. Log File Watcher (1 event)
A file system watcher monitors `.intent/events/` for new observation files and emits `observation.written`.

### 5. Zapier (1 event)
External signal ingestion. When signals come from outside the development workflow (customer support tickets, Slack conversations, analytics anomalies), a Zapier integration can emit `signal.created`.

### 6. Manual (fallback)
Any event can be manually emitted by adding a line to `events.jsonl`. This is the escape hatch for events that don't yet have automated emission.

## Implementation Phases

The event system rolls out incrementally:

1. **Manual emission** — Write events by hand to validate the schema
2. **GitHub Action** — Automate the 9 events triggered by file changes
3. **Agent self-emission** — Instrument Claude Code to emit contract events
4. **Entire.io integration** — Connect trace completion to event stream
5. **External signals** — Set up Zapier or webhook ingestion
6. **OTel upgrade** — Migrate from JSONL to full OTel collector for production teams

## Where Events Live

- **Storage:** `.intent/events/events.jsonl` in each Intent-native repo
- **Interactive artifact:** [Event Catalog (React)](../artifacts/intent-event-catalog.jsx)
- **Site page:** [event-catalog.html](../docs/event-catalog.html)
