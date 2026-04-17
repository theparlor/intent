---
id: RETRO-2026-04-13-approval-gradient-DEC-5
type: decision
source: session-design
decided: 2026-04-13
topic: approval-gradient
status: decided
---

# Circuit Breaker Resets Trust to Zero on Retroactive Flag

## Context

If the system self-elevates routine actions to log-only, trust can drift into unsafe territory. Need a mechanism to revoke earned trust when the system gets it wrong.

## Decision

If Brien retroactively flags or modifies a log-only or preview action, contextual trust for that pattern (target + action_type combination) resets to 0. The next action to that target goes through full gate. Trust must be re-earned from scratch.

Learning loop for all decisions:
- Approve without modification → trust increases
- Approve with modification → trust stays flat
- Deny → trust decreases significantly
- Retroactive flag → trust resets to 0

## Alternatives Considered

1. **Gradual decrease instead of reset** — rejected; if the system sent something wrong, the safe response is full reset, not gradual adjustment
2. **Reset per action type only** — rejected; too broad (resetting all Slack trust because one message was wrong)
3. **No circuit breaker** — rejected; earned trust without revocability is a safety gap

## Consequences

- Brien needs an "I didn't mean to send that" mechanism (retroactive flag)
- Trust patterns are per-(target, action_type) pair, not global
- System is self-correcting: wrong actions create immediate friction increase
