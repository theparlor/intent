---
id: RETRO-2026-04-13-approval-gradient-DEC-6
type: decision
source: session-design
decided: 2026-04-13
topic: approval-gradient
status: decided
---

# Phase 2 Trigger: ≥ 20 Records with ≥ 3 Distinct Targets

## Context

Phase 2 (contextual action trust) requires enough data to compute meaningful precedent and familiarity scores. Shipping the gradient without data makes trust scores unreliable.

## Decision

Phase 2 design work begins when Phase 1 has accumulated:
- ≥ 20 approval records total (enough for pattern detection)
- ≥ 3 distinct action targets (enough for familiarity comparison)

Below that threshold, there's not enough data for meaningful contextual trust scoring.

## Alternatives Considered

1. **Time-based trigger (2 weeks)** — rejected; Brien might not generate 20 records in 2 weeks if engagement pace is slow
2. **Lower threshold (10 records)** — rejected; too few for stable precedent scoring
3. **No trigger, Brien decides** — rejected; Brien will forget to check; the system should surface readiness

## Consequences

- Phase 1 may run for 1-4 weeks depending on Brien's communication volume
- The system should emit a signal when threshold is reached ("approval data sufficient for Phase 2")
- Brien reviews Phase 1 data before Phase 2 ships to validate the trust model
