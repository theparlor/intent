---
id: RETRO-2026-04-12-humanlayer-approval-SIG-2
type: signal
category: observability-gap
severity: medium
source: session-analysis
detected: 2026-04-12
topic: humanlayer-approval
status: promoted
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

## Triage, 2026-07-08

Disposition: still pending in practice, though extensively designed. spec/.intent/specs/SPEC-APPROVAL-GATE.md exists with status: executing and lists this exact signal (by ID) plus its four siblings as source_signals, so the provenance chain is direct and confirmed, not inferred. The spec's IntentApproval entity schema answers every concrete ask across the cluster: id/status/requested_at/decided_at/decided_by/comment fields close the audit-trail gap (SIG-2), ttl_seconds/expires_at plus a revalidation-on-expiry protocol close the TTL gap (SIG-3), and original_payload/approved_payload/modification_detected close the approve-with-modification gap (SIG-4). .intent/config/approval-rules.yml is live on disk with per-action-type TTLs matching this cluster's proposed values exactly (15m Slack, 60m email). What is NOT yet true: .intent/approvals/ contains only _TEMPLATE.md, no live IntentApproval entity has ever been written, and no PreToolUse hook intercepts L0 actions at the tool-call boundary the way the spec describes. So the practical complaint this cluster raises, Brien cannot today reconstruct "what did I approve last Tuesday", remains true: the protocol is fully specified but not yet operational. Needed control: wire the gate skill to a live hook and confirm the first real IntentApproval entity gets written and read back.
