---
id: RETRO-2026-04-13-approval-gradient-DEC-3
type: decision
source: session-design
decided: 2026-04-13
topic: approval-gradient
status: decided
---

# Contextual Action Trust Uses 4-Factor Model

## Context

Brien's ceremony tax concern requires a gradient within L0, not a binary gate. Need a trust scoring model for individual action instances (not just action types).

## Decision

Contextual action trust = weighted combination of four factors:

| Factor | Weight | Measures |
|--------|--------|----------|
| Precedent | 0.35 | Brien approved N similar actions (same target + similar payload) with low modification rate |
| Familiarity | 0.25 | Target is a channel/person Brien communicates with regularly |
| Novelty | 0.20 | Payload divergence from previously approved payloads to this target |
| Blast radius | 0.20 | Audience size, formality, reversibility |

This mirrors Intent's spec-level trust formula (clarity × 0.30 + ...) but applied at the action granularity.

## Alternatives Considered

1. **Reuse spec-level trust formula directly** — rejected; factors don't map (clarity/testability don't apply to Slack messages)
2. **Simple frequency-based model** (approved N times → auto-approve) — rejected; frequency alone ignores payload novelty and target risk
3. **ML-based classification** — deferred to Phase 3; too heavy for the current data volume

## Consequences

- Requires payload similarity computation (see critique: unstated dependency)
- Requires per-target approval history aggregation
- Weights are initial — Brien tunes after observing Phase 2 behavior
