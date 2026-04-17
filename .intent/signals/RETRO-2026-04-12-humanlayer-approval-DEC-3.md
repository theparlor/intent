---
id: RETRO-2026-04-12-humanlayer-approval-DEC-3
type: decision
source: session-analysis
decided: 2026-04-12
topic: humanlayer-approval
status: decided
---

# Time-Boxed Elevation Over Per-Request Bypass

## Context

HumanLayer has `DangerouslySkipPermissions` with optional `ExpiresAt` — a session-level bypass with time expiry. Brien's workflow includes focused sessions where L0 friction is counterproductive ("just send freely for the next hour").

## Decision

Implement scoped elevation: Brien can temporarily elevate specific action types (e.g., slack_message, email) from L0 → L3 for a defined duration. Auto-expires. Full audit trail maintained (decisions logged as `decided_by: "auto:elevation-{id}"`).

## Alternatives Considered

1. **Global bypass** — rejected; too broad, loses audit trail
2. **Per-request approval only** — rejected; creates friction in focused sessions
3. **No elevation mechanism** — rejected; Brien will work around it informally, losing governance

## Consequences

- Requires elevation entity (scope, expires_at, elevated_to, reason)
- Approval records during elevation show auto-approve with elevation reference
- Risk: Brien over-uses elevation → mitigated by per-action-type scoping and audit trail
