---
id: INT-014
title: "Human-gate capacity model — ration aggregate attention, not just per-signal trust"
status: proposed
proposed_by: "knowledge-ingest-2026-05-16"
proposed_date: 2026-05-16T00:00:00Z
accepted_date:
signals: [SIG-038]
specs: []
owner: "brien"
priority: now
product: execute
---
# Human-gate capacity model

## Problem

Intent's founding thesis (THM-002) is that the bottleneck shifts when AI collapses execution. The under-stated half of that thesis: **the bottleneck relocates to the human, it does not disappear.** Specification is one new location. The **review/approval gate is the other.** Humans are the bottleneck; Jira and peer code review are the legacy instrumentation of exactly that constraint under Agile — queues built to ration finite human attention.

Intent's trust framework currently rations the wrong axis. Trust scoring is **per-signal** ("can this one item be auto-resolved?"). Nothing models the **aggregate draw on the human**. The L0 approval gate (SPEC-APPROVAL-GATE) and the strategic-request channel both spend the same scarce resource — Brien's attention — with no shared budget. Activating many L2/L3 signals at once saturates the gate.

Failure mode: **Intent recreates the ceremony tax it was built to eliminate.** The L0 approval queue becomes the new Jira backlog. Every signal can be locally trust-correct while the system is globally over-subscribed. A relocated queue is not a removed queue.

## Desired Outcome

Model the human gate as a finite-capacity flow stage with explicit WIP limits and back-pressure — the way good flow systems (Reinertsen, Kanban) model any constrained resource — so Intent does not silently rebuild Jira inside its own autonomy pipeline.

### Scope

1. **Concurrent-review budget** — a system-level cap on simultaneously-active L2/L3 signals, distinct from per-signal trust. Trust decides *eligibility*; the budget decides *admission*.
2. **Router back-pressure** — when the review queue is at WIP limit, the Router defers low-urgency L2/L3 activation rather than fanning out unbounded. Queue theory primitives: Little's Law, WIP limit, arrival vs. service rate.
3. **Gate observability** — surface current queue depth / throughput as a first-class Observe signal (depends on SIG-036: the gate is one of the running things that fails silently when saturated).
4. **Throughput calibration** — measure Brien's actual review rate (items/day) and parameterize the cap; do not hardcode a guess.

## Evidence

- **SIG-038** — the bottleneck relocated, not a new finding; trust rations the wrong axis; Jira/peer-review are the cautionary precedent.
- **THM-002** — bottleneck-shift founding thesis; this intent is its sharpening at the approval gate.
- **THM-005** — external (low-rigor) corroboration that the constraint is universally felt ("drown in review tasks → lose the efficiency").
- Dependency: **SIG-037** (always-on hosting) — a saturated gate while the practitioner is offline is the worst case; capacity model and hosting model are coupled.

## Constraints

- Per-signal trust scoring (DDR-008) is unchanged — this adds an orthogonal admission control layer, it does not modify the trust formula.
- Must not reintroduce sprint/ceremony semantics. This is a flow WIP limit, not a planning cadence.
- The budget is a property of the *human*, not of any one engagement — it spans all active contexts competing for the same attention.

## Specs to generate from this intent

- SPEC-human-gate-wip-limit (concurrent-review budget + Router back-pressure)
- SPEC-gate-throughput-observability (queue depth/throughput as Observe signal; couples to SIG-036)
</content>
