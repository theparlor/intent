---
id: RETRO-2026-04-13-approval-gradient-DEC-2
type: decision
source: brien-directive
decided: 2026-04-13
topic: approval-gradient
status: decided
---

# Phase 1 Ships Full Gate to Collect Training Data

## Context

Brien flagged that uniform L0 gating reintroduces ceremony tax. However, contextual trust scoring requires data — precedent, familiarity, modification rates — that doesn't exist yet.

## Decision

Phase 1 ships with full gate on all L0 actions (safe default). Every approval record captures the data Phase 2 needs: action_type, action_target, original_payload, approved_payload, modification_detected, decision, comment. Phase 1 is temporary friction that earns permanent intelligence.

## Alternatives Considered

1. **Ship gradient immediately** — rejected; no training data exists, trust scores would be guesses
2. **Skip Phase 1, go directly to log-only for routine actions** — rejected; "routine" hasn't been defined by data yet
3. **Ship with manual trust overrides** — rejected; adds complexity without data to guide overrides

## Consequences

- Brien will experience full-gate friction on all L0 actions temporarily
- Every decision Brien makes builds the training set
- Phase 2 trigger: ≥ 20 approval records with ≥ 3 distinct targets
- Explicit expectation: Phase 1 is not permanent
