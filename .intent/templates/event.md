---
version: "1.0"
event: ""           # signal.created | intent.proposed | intent.accepted | spec.written | spec.approved | contract.verified | contract.failed | execution.started | execution.completed | agent.trace.captured | decision.recorded | cluster.formed | atom.created | arb.reviewed | digest.generated
timestamp: ""       # ISO 8601: YYYY-MM-DDTHH:MM:SSZ
trace_id: ""        # Intent-level trace (INT-XXX or session ID)
span_id: ""         # Work-unit-level span (SIG-XXX, SPEC-XXX, etc.)
parent_id: ""       # Parent span for hierarchy
source: ""          # cli | mcp | github-action | slack | agent
---
# Event: [event type]

## Data Payload

Structured data specific to this event type. Minimum fields:

- **id:** The artifact ID that triggered this event
- **title:** Human-readable summary
- **actor:** Who or what caused this event (human name or agent identifier)

## Schema Notes

- Events are append-only to `.intent/events/events.jsonl`
- Each event is one JSON line (JSONL format)
- Schema is OTel-compatible: version, event, timestamp, trace_id, span_id, parent_id, source, data
- Events are never modified after emission
- The GitHub Action emits events on push when .intent/ files change
- CLI tools emit events immediately on artifact creation

## Event Types Reference

| Event | Trigger | Data Fields |
|-------|---------|-------------|
| signal.created | New signal captured | id, title, source, confidence |
| intent.proposed | New intent created | id, title, signals[], proposer |
| intent.accepted | Intent approved for speccing | id, accepted_by, accepted_date |
| spec.written | New spec drafted | id, title, intent, author |
| spec.approved | Spec approved for execution | id, approved_by, approved_date |
| contract.verified | Contract assertion passed | id, spec, verified_by, method |
| contract.failed | Contract assertion failed | id, spec, failure_reason |
| execution.started | Agent begins work on spec | spec_id, agent, started_at |
| execution.completed | Agent finishes work | spec_id, agent, duration, outcome |
| agent.trace.captured | Agent reasoning recorded | trace_id, agent, file_path |
| decision.recorded | Architectural decision made | id, title, status |
| cluster.formed | Signals grouped into cluster | cluster_id, signal_ids[], name |
| atom.created | Atomized work item created | id, title, product, size |
| arb.reviewed | ARB review completed | atom_id, verdict, concerns[] |
| digest.generated | Periodic digest produced | period, signal_count, intent_count |
