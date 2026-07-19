---
id: RETRO-2026-04-12-humanlayer-approval-SIG-5
type: signal
category: self-recognition
severity: high
source: brien-statement
detected: 2026-04-12
topic: humanlayer-approval
status: promoted
---

# Brien Recognizes Approval Gate as Unfulfilled Original Intent

## Signal

Brien stated: "this sounds like it matches my original intent but I fell short thus far." This is a self-recognition that the L0 governance design was always meant to be formalized but remained at the prose level. The HumanLayer analysis provided the external pattern vocabulary to name what was missing.

## Evidence

- Direct Brien statement in session
- L0 governance has existed since CLAUDE.md creation (early 2026)
- No implementation work on approval formalization has occurred in ~2 months
- Brien immediately asked to capture this as signal + intent — confirming this is a priority gap, not a backlog item

## Implication

This is a high-priority gap that Brien has been carrying as implicit knowledge. Formalizing it now prevents further drift and establishes the approval gate as a specifiable, contractable capability within Intent.

## Recommended Action

Create formal intent for L0 approval gate formalization. Use this session's analysis as the spec seed. Route through Notice → Spec → Execute → Observe.

## Triage, 2026-07-08

Disposition: still pending in practice, though extensively designed. spec/.intent/specs/SPEC-APPROVAL-GATE.md exists with status: executing and lists this exact signal (by ID) plus its four siblings as source_signals, so the provenance chain is direct and confirmed, not inferred. The spec's IntentApproval entity schema answers every concrete ask across the cluster: id/status/requested_at/decided_at/decided_by/comment fields close the audit-trail gap (SIG-2), ttl_seconds/expires_at plus a revalidation-on-expiry protocol close the TTL gap (SIG-3), and original_payload/approved_payload/modification_detected close the approve-with-modification gap (SIG-4). .intent/config/approval-rules.yml is live on disk with per-action-type TTLs matching this cluster's proposed values exactly (15m Slack, 60m email). What is NOT yet true: .intent/approvals/ contains only _TEMPLATE.md, no live IntentApproval entity has ever been written, and no PreToolUse hook intercepts L0 actions at the tool-call boundary the way the spec describes. So the practical complaint this cluster raises, Brien cannot today reconstruct "what did I approve last Tuesday", remains true: the protocol is fully specified but not yet operational. Needed control: wire the gate skill to a live hook and confirm the first real IntentApproval entity gets written and read back.
