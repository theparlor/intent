---
id: SIG-002
date: 2026-03-28
source: cowork-session
confidence: high
related_intents: []
status: new
---

# Signal: Distributed tracing is the right observability model for Intent work

## Observation

OpenTelemetry's tracing model maps directly onto the Intent work hierarchy. The same architecture designed to make complex async multi-service systems observable applies to complex async multi-agent work systems.

## Mapping

| OTel Concept    | Intent Equivalent       |
|-----------------|-------------------------|
| Trace           | Intent (parent context) |
| Span            | Spec (scoped work)      |
| Leaf Span       | Contract (execution)    |
| Span Event      | Signal (observation)    |
| Span Attributes | Governance metadata     |
| Trace ID        | Intent ID flowing through all children |

## Implication

Every state change in the Intent system (signal captured, intent validated, spec authored, contract started/passed/failed) should emit a structured event. These events can be:

1. **Minimal**: Append-only JSONL files in `.intent/events/` — git-tracked, local
2. **Medium**: OpenTelemetry SDK emitting to Grafana Tempo — queryable traces
3. **Full**: Datadog/Honeycomb — enterprise-grade with alerting

## Starting Point

Structured JSONL event emission + local HTML dashboard gets 80% of value with zero infrastructure. Upgrade path to OTel is clean because the event schema is already trace-shaped.

## Evidence

Entire.io already captures the execution layer (agent sessions). What's missing is the work layer — structured events linking signals → intents → specs → contracts with trace IDs.
