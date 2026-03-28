# Signal: OpenTelemetry for Work Systems

ID: SIG-002
Date: 2026-03-28
Status: Captured

## Problem

Agile metrics (burndown, velocity, story points) are observability for humans, not systems. They don't capture causality or the actual shape of work.

## Insight

Apply OpenTelemetry's tracing model to work systems. A **Trace** is a complete request (from Signal to Product). Each **Span** is a work unit.

## OTel-to-Intent Mapping

| OTel Concept | Intent Equivalent | Why |
|---|---|---|
| Trace | Intent | Complete end-to-end request from user signal to delivered feature |
| Span | Spec | A piece of work with clear start/end, inputs/outputs |
| Leaf Span | Contract | The smallest unit: a fulfilled interface |
| Span Event | Signal | An observation that triggers a new trace |
| Tags | Metadata | Priority, team owner, SLA, etc. |
| Metrics | Health | Test coverage, deployment frequency, MTTR |

## Structured Work Events

Propose emitting structured JSONL events to `.intent/events/`:

```jsonl
{"timestamp": "2026-03-28T10:15:00Z", "event": "signal_captured", "signal_id": "SIG-001", "source": "design_session", "severity": "high"}
{"timestamp": "2026-03-28T10:20:00Z", "event": "intent_parsed", "intent_id": "INT-001", "signal_ids": ["SIG-001"], "confidence": 0.95}
{"timestamp": "2026-03-28T10:25:00Z", "event": "spec_written", "spec_id": "SPEC-001", "intent_id": "INT-001", "agent": "intent-parser-v2"}
{"timestamp": "2026-03-28T11:00:00Z", "event": "capability_tested", "capability_id": "CAP-001", "contract_id": "CON-001", "passed": true, "duration_ms": 450}
{"timestamp": "2026-03-28T12:00:00Z", "event": "feature_deployed", "feature_id": "FEA-001", "capabilities": ["CAP-001", "CAP-002"], "environment": "production"}
```

## Dashboard Queries

With OTel events, we can:

1. **Trace latency**: How long from Signal to Product?
2. **Critical path**: What specs are blocking features?
3. **Quality**: Which capabilities have the lowest test pass rate?
4. **Flow**: Are specs getting stuck at design review?
5. **Attribution**: Which signal led to which feature?

## Benefits

- **Causality**: Every product change is traceable back to original signal
- **Continuous observability**: Events flow in real-time, no periodic reporting
- **Agent-native**: Events are machine-emitted, machines can consume them
- **Async processing**: Tools can react to events without blocking

## Implementation

1. Define event schema (JSON Schema)
2. Create event emitter in agent tooling
3. Build simple event log viewer
4. Add event filtering to git log (via `.intent/events/` indexing)
