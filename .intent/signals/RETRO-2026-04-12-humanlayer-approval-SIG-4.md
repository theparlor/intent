---
id: RETRO-2026-04-12-humanlayer-approval-SIG-4
type: signal
category: pattern-opportunity
severity: low
source: session-analysis
detected: 2026-04-12
topic: humanlayer-approval
status: promoted
---

# Approve-With-Modification Pattern Missing

## Signal

HumanLayer's `updatedInput` field allows reviewers to modify the proposed action payload before approving. Brien already does this conversationally ("change X, then send") but the original draft and the modified version are not captured as a diff. This delta is training data for improving future L0 drafts.

## Evidence

- HumanLayer MCP response: `{ "behavior": "allow", "updatedInput": { ... } }`
- Brien's current workflow: verbal correction → Claude regenerates → Brien approves
- No structured capture of original vs. modified payload exists

## Implication

Without capturing the modification delta, the system can't learn which types of L0 actions Brien consistently edits. Pattern detection would enable proactive template improvement.

## Recommended Action

IntentApproval entity should store both `original_payload` and `approved_payload` when Brien modifies before approving.

## Triage, 2026-07-08

Disposition: still pending in practice, though extensively designed. spec/.intent/specs/SPEC-APPROVAL-GATE.md exists with status: executing and lists this exact signal (by ID) plus its four siblings as source_signals, so the provenance chain is direct and confirmed, not inferred. The spec's IntentApproval entity schema answers every concrete ask across the cluster: id/status/requested_at/decided_at/decided_by/comment fields close the audit-trail gap (SIG-2), ttl_seconds/expires_at plus a revalidation-on-expiry protocol close the TTL gap (SIG-3), and original_payload/approved_payload/modification_detected close the approve-with-modification gap (SIG-4). .intent/config/approval-rules.yml is live on disk with per-action-type TTLs matching this cluster's proposed values exactly (15m Slack, 60m email). What is NOT yet true: .intent/approvals/ contains only _TEMPLATE.md, no live IntentApproval entity has ever been written, and no PreToolUse hook intercepts L0 actions at the tool-call boundary the way the spec describes. So the practical complaint this cluster raises, Brien cannot today reconstruct "what did I approve last Tuesday", remains true: the protocol is fully specified but not yet operational. Needed control: wire the gate skill to a live hook and confirm the first real IntentApproval entity gets written and read back.
