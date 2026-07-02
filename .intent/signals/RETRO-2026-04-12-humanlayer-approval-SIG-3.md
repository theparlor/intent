---
id: RETRO-2026-04-12-humanlayer-approval-SIG-3
type: signal
category: architecture-gap
severity: medium
source: session-analysis
detected: 2026-04-12
topic: humanlayer-approval
status: promoted
---

# No TTL on Approval Contexts — Stale Action Risk

## Signal

When an L0 action is drafted but Brien doesn't respond immediately (context switch, meeting, end of day), there is no expiration mechanism. A Slack message drafted 3 hours ago may no longer be contextually appropriate, but nothing prevents it from being approved and sent stale.

## Evidence

- HumanLayer itself has this gap (commented-out 5-minute timeout in `hld/mcp/server.go:195-198`)
- Brien's workflow includes frequent context switches between engagements (Subaru, ASA, Cargill)
- No TTL concept exists in current intent framework event catalog

## Implication

Stale approvals are a silent correctness risk. The message may reference outdated information, wrong tone for current context, or superseded decisions.

## Recommended Action

Implement TTL per action type (15m Slack, 60m email, 120m PR) with **revalidation on expiry** (regenerate with fresh context, don't auto-deny). See analysis Pattern 4.
