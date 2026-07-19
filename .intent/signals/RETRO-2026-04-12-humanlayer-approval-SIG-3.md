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

## Triage, 2026-07-08

Disposition: still pending in practice, though extensively designed. spec/.intent/specs/SPEC-APPROVAL-GATE.md exists with status: executing and lists this exact signal (by ID) plus its four siblings as source_signals, so the provenance chain is direct and confirmed, not inferred. The spec's IntentApproval entity schema answers every concrete ask across the cluster: id/status/requested_at/decided_at/decided_by/comment fields close the audit-trail gap (SIG-2), ttl_seconds/expires_at plus a revalidation-on-expiry protocol close the TTL gap (SIG-3), and original_payload/approved_payload/modification_detected close the approve-with-modification gap (SIG-4). .intent/config/approval-rules.yml is live on disk with per-action-type TTLs matching this cluster's proposed values exactly (15m Slack, 60m email). What is NOT yet true: .intent/approvals/ contains only _TEMPLATE.md, no live IntentApproval entity has ever been written, and no PreToolUse hook intercepts L0 actions at the tool-call boundary the way the spec describes. So the practical complaint this cluster raises, Brien cannot today reconstruct "what did I approve last Tuesday", remains true: the protocol is fully specified but not yet operational. Needed control: wire the gate skill to a live hook and confirm the first real IntentApproval entity gets written and read back.
