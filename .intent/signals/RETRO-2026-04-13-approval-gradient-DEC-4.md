---
id: RETRO-2026-04-13-approval-gradient-DEC-4
type: decision
source: session-design
decided: 2026-04-13
topic: approval-gradient
status: decided
---

# Three Friction Tiers Within L0

## Context

Not all L0 actions carry equal risk. A daily standup update to #subaru is categorically different from a first email to a new client. Uniform gating creates friction proportional to volume, not risk.

## Decision

Three tiers based on contextual action trust score:

| Tier | Trust | Behavior | Brien's Experience |
|------|-------|----------|-------------------|
| Full gate | < 0.3 | Block, present, decide | Full approval entity lifecycle |
| Preview | 0.3-0.6 | Show summary, 1-tap confirm | Lightweight — sees it, confirms, no comment needed |
| Log-only | ≥ 0.6 | Record and proceed | Action executes immediately, Brien reviews async |

## Alternatives Considered

1. **Binary (gate or don't)** — rejected; loses the middle ground where Brien wants awareness without friction
2. **Four tiers (add "silent")** — rejected; log-only is already minimal, silent = no governance
3. **Configurable per action type** — partially adopted; the trust model is configurable, but the tier thresholds are system-level

## Consequences

- Preview tier is the UX innovation — Brien sees what's happening without blocking
- Log-only tier requires async review surface (today: intent journal browsing; future: dashboard)
- Tier thresholds (0.3, 0.6) are initial — Brien tunes based on experience
