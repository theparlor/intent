---
id: SIG-038
timestamp: 2026-05-16T00:00:00Z
source: knowledge-ingest
confidence: 0.65
trust: 0.3
autonomy_level: L1
status: captured
cluster: trust-framework
author: agent
related_intents: []
referenced_by:
  - THM-005
parent_signal: null
---

# Human review capacity is a finite resource that should gate autonomy rollout

## Summary

The Rahul playbook's 90-day plan warns: "Don't try to ship everything in a weekend. You will overwhelm yourself with review tasks and lose all the efficiency you were trying to gain." Intent's trust framework models per-signal autonomy (L0–L4) but does not model the *aggregate human-review throughput ceiling* of the practitioner. Activating many L2 (agent decides, human approves) or L3 (human monitors) signals simultaneously can saturate the approval gate and the strategic-request channel, collapsing the efficiency the autonomy model is meant to produce.

## Signal Value

This is a genuinely new consideration, not corroboration. Trust scoring answers "can this one signal be auto-resolved?" It does not answer "given a finite human reviewer, how many in-flight L2/L3 signals can the system safely have at once?" The L0 approval gate (SPEC-APPROVAL-GATE) and strategic-request pattern both consume the same scarce resource: Brien's attention. Without a throughput model, the system can be locally trust-correct but globally over-subscribed.

## Proposed Actions

1. Add a system-level concept: concurrent-review budget (a cap on simultaneously-active L2/L3 signals, distinct from per-signal trust).
2. Consider a scheduler/back-pressure mechanism in the Router that defers low-urgency L2/L3 activation when the review queue is saturated.
3. Open question carried into THM-005: what is Brien's actual review throughput, and how should it parameterize the cap?
</content>
