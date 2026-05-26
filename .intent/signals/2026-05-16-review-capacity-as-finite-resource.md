---
id: SIG-038
timestamp: 2026-05-16T00:00:00Z
source: knowledge-ingest
confidence: 0.8
trust: 0.35
autonomy_level: L1
status: promoted
cluster: trust-framework
author: agent
related_intents:
  - INT-014
referenced_by:
  - THM-005
  - THM-002
parent_signal: null
---

# The human review gate is the bottleneck relocated — not a new finding, the founding thesis

## Summary

This is **not a new consideration**. It is Intent's founding thesis (THM-002) rediscovered at a new location. The bottleneck never disappeared when AI collapsed execution — it *relocated*. It moved upstream to specification, and it also moved to the **human review/approval gate**. Humans are the bottleneck. They always were. Jira (a work-in-progress queue) and peer code review (a synchronous human gate) are the *legacy instrumentation* of exactly this constraint under Agile — coordination machinery that exists precisely because human review capacity is finite and must be rationed.

The Rahul playbook ("ship everything in a weekend → drown in review tasks → lose the efficiency") is a low-rigor restatement of the same law. It carries no evidential weight; it is corroboration that the constraint is universally felt.

## The actual risk

Intent's trust framework rations the **wrong axis**. Trust scoring answers "can *this one signal* be auto-resolved without a human?" — a per-item question. It does not model the **aggregate draw on the human**. The L0 approval gate (SPEC-APPROVAL-GATE) and the voluntary strategic-request channel both consume the same scarce resource: Brien's attention. Activating many L2 (agent decides, human approves) or L3 (human monitors) signals at once saturates that gate.

The failure mode is precise and almost embarrassing: **Intent recreates the ceremony tax it was built to eliminate.** The L0 approval queue becomes the new Jira backlog — an un-modeled, un-rationed human-attention queue. The system can be locally trust-correct on every individual signal and globally over-subscribed. Per-signal autonomy without an aggregate-capacity model is just a relocated queue, not a removed one.

## The narrow novelty

Not "humans are a bottleneck" (that is THM-002, founding, obvious). The narrow, architectural gap is: **Intent has no WIP-limit / queue model for the human gate.** Queue theory already names the missing primitives — Little's Law (queue length = arrival rate × service time), WIP limits, back-pressure. Agile's Jira and peer-review queues are the cautionary *precedent*, not a new domain. Intent should instrument the human gate the way good flow systems do, instead of leaving it implicit.

## Proposed Actions

1. Introduce a system-level **concurrent-review budget**: a cap on simultaneously-active L2/L3 signals, distinct from per-signal trust.
2. Add **back-pressure in the Router**: defer low-urgency L2/L3 activation when the review queue is saturated (WIP limit, not unbounded fan-out).
3. Express this explicitly as THM-002 sharpened — connect the signal, the theme, and the founding "ceremony tax" framing so the lineage is legible.
4. Carried open question: what is Brien's actual review throughput (items/day), and how should it parameterize the cap?

Promoted to **INT-014** (human-gate capacity model).
</content>
