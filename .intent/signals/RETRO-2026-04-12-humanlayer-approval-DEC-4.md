---
id: RETRO-2026-04-12-humanlayer-approval-DEC-4
type: decision
source: session-analysis
decided: 2026-04-12
topic: humanlayer-approval
status: decided
---

# TTL Revalidates on Expiry, Never Auto-Denies

## Context

Approval requests for L0 actions may go stale if Brien context-switches. Need a TTL mechanism. HumanLayer has no TTL (commented-out code). Design from first principles.

## Decision

Approval requests carry TTL by action type (15m Slack, 60m email, 120m PR, 30m calendar). On expiry, the system **revalidates** (regenerates with fresh context) rather than auto-denying. A stale approval is not necessarily wrong — it just needs fresh context confirmation.

## Alternatives Considered

1. **No TTL** — rejected; stale actions are a correctness risk
2. **Auto-deny on expiry** — rejected; valid actions get lost, Brien has to re-request
3. **Auto-approve on expiry** — rejected; defeats the purpose of the gate

## Consequences

- Requires TTL config per action type
- Revalidation triggers a new approval request with updated context
- Brien sees "this was originally drafted 2 hours ago, here's the refreshed version"
