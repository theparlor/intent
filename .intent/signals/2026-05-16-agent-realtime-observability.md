---
id: SIG-036
timestamp: 2026-05-16T00:00:00Z
source: knowledge-ingest
confidence: 0.7
trust: 0.4
autonomy_level: L2
status: captured
cluster: observe-product
author: agent
related_intents: []
referenced_by:
  - THM-005
parent_signal: null
---

# Running agents fail silently — Observe has no real-time degradation detection

## Summary

External corroboration (Rahul playbook, THM-005) of a gap Intent already half-names: autonomous agents "fail silently — the output becomes garbage around day 9, and nobody notices." Intent's Observe product is schema-ready (15→22 event types, events.jsonl) but has no visualization and no owned mechanism that detects *quality degradation of a running enrichment/execution agent over time*. Overwatch (RAT-003) detects incestuous amplification at the reasoning level; it does not watch for slow output rot in long-running L3/L4 loops.

## Signal Value

The "garbage by day 9" failure is the operational form of the staleness/decay problem (DDR-008). Intent's autonomy model authorizes L3/L4 agents to run with monitoring or circuit-breakers only — but "monitoring" is currently undefined as a concrete observable. This is the difference between an Observe *schema* and an Observe *product*.

## Proposed Actions

1. Define a concrete "agent health" observable (output-quality trend against the multiplicative fitness function) emitted on the event stream.
2. Specify the circuit-breaker trigger for L3/L4 in measurable terms, not "monitoring."
3. Feed into Observe product v1 scoping — this is a forcing function for visualization.
</content>
