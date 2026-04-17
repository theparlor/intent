---
id: RETRO-2026-04-12-humanlayer-approval-SIG-2
type: signal
category: observability-gap
severity: medium
source: session-analysis
detected: 2026-04-12
topic: humanlayer-approval
---

# L0 Actions Are Unauditable

## Signal

When Brien approves or denies an external communication action, no record is created. The decision exists only in conversation context, which is ephemeral. There is no way to answer "what did I approve last Tuesday?" or "how many Slack messages did I modify before sending?"

## Evidence

- Approval happens conversationally ("yes, send it" or "change X first")
- No approval entity is persisted to intent journal or any other store
- Session extracts capture decisions but not the approve/deny lifecycle of individual actions
- HumanLayer persists every approval with timestamps, comments, and correlation IDs

## Implication

Brien cannot reconstruct the approval chain for any session. This blocks pattern detection (e.g., "I always edit Slack messages to client X — maybe the template needs updating") and compliance narrative for engagements.

## Recommended Action

IntentApproval entity with `requested_at`, `decided_at`, `decided_by`, and required `comment` on deny. See analysis at `Core/frameworks/intent/knowledge-engine/analysis/humanlayer-approval-patterns.md`.
