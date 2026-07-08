---
id: RETRO-2026-04-12-humanlayer-approval-SIG-1
type: signal
category: architecture-gap
severity: high
source: session-analysis
detected: 2026-04-12
topic: humanlayer-approval
---

# L0 Governance Is Prose, Not Protocol

## Signal

Brien's L0 external communication gate ("always require Brien's explicit approval") exists only as natural language instruction in CLAUDE.md. There is no typed approval entity, no persistence layer, no structured request/response cycle. Enforcement depends entirely on Claude's prompt adherence.

## Evidence

- CLAUDE.md autonomy grants section defines L0 as "always require Brien's explicit approval. No exceptions."
- No IntentApproval entity exists in the intent journal schema
- No approval records are captured anywhere in the governance system
- HumanLayer SDK models approval as a first-class data type with full lifecycle (pending → decided), demonstrating the pattern that's missing

## Implication

L0 governance is the highest-stakes gate in Brien's system (Slack messages, emails, PR creation, calendar changes). Running it on prompt adherence alone means: no audit trail, no replay capability, no structured feedback loop when actions are denied.

## Recommended Action

Adopt the IntentApproval entity pattern from HumanLayer analysis. See `Core/frameworks/intent/knowledge-engine/analysis/humanlayer-approval-patterns.md` for full design.

## Triage, 2026-07-08

Disposition: still pending in practice, though extensively designed. spec/.intent/specs/SPEC-APPROVAL-GATE.md exists with status: executing and lists this exact signal (by ID) plus its four siblings as source_signals, so the provenance chain is direct and confirmed, not inferred. The spec's IntentApproval entity schema answers every concrete ask across the cluster: id/status/requested_at/decided_at/decided_by/comment fields close the audit-trail gap (SIG-2), ttl_seconds/expires_at plus a revalidation-on-expiry protocol close the TTL gap (SIG-3), and original_payload/approved_payload/modification_detected close the approve-with-modification gap (SIG-4). .intent/config/approval-rules.yml is live on disk with per-action-type TTLs matching this cluster's proposed values exactly (15m Slack, 60m email). What is NOT yet true: .intent/approvals/ contains only _TEMPLATE.md, no live IntentApproval entity has ever been written, and no PreToolUse hook intercepts L0 actions at the tool-call boundary the way the spec describes. So the practical complaint this cluster raises, Brien cannot today reconstruct "what did I approve last Tuesday", remains true: the protocol is fully specified but not yet operational. Needed control: wire the gate skill to a live hook and confirm the first real IntentApproval entity gets written and read back.
