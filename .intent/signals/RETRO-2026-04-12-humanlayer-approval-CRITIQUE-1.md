---
id: RETRO-2026-04-12-humanlayer-approval-CRITIQUE-1
type: critique
source: session-analysis
created: 2026-04-12
topic: humanlayer-approval
severity: high
status: promoted
---

# Critique: L0 Governance Gap — Prose Enforcement of Highest-Stakes Gate

## The Problem

Brien's most critical governance boundary — L0 external communication — has the weakest enforcement mechanism in the system. It relies entirely on Claude's prompt adherence to CLAUDE.md instructions: "always require Brien's explicit approval. No exceptions."

Every other autonomy level (L1-L4) can fail gracefully because the consequences are internal (files, research, budget). L0 failures are external and irreversible (messages sent, PRs created, calendar invites dispatched).

## Why This Persisted

1. **It worked well enough.** Claude is generally reliable at following L0 instructions. The failure mode is silent — not "it sent unauthorized messages" but "there's no audit trail, no structured feedback, no pattern detection."
2. **No external pattern vocabulary.** Until the HumanLayer analysis, there wasn't a concrete reference architecture for what "formalized approval gates" looks like in an AI agent context.
3. **Priority competition.** Intent's development focused on the Notice→Spec→Execute pipeline, the Knowledge Engine, and persona system. L0 governance was "working" and didn't surface as urgent.
4. **Brien recognized but didn't prioritize.** His self-statement ("I fell short thus far") confirms awareness of the gap. The HumanLayer analysis converted latent awareness into actionable architecture.

## The Risk

Prompt-adherence governance is:
- **Fragile under context pressure.** Long sessions, heavy tool use, and complex multi-step workflows increase the chance of an L0 action slipping through without explicit approval.
- **Unauditable.** No record of what was approved, denied, or modified. Cannot answer "what did I send last week?"
- **Non-composable.** Can't build pattern detection, template improvement, or compliance narratives on top of conversational approvals.
- **Model-dependent.** Different models (Opus vs Sonnet) may have different adherence profiles for prose governance. Typed gates are model-independent.

## The Fix

See SPEC-SEED-1 for the proposed IntentApproval entity, gate skill, auto-accept rules, and TTL system. The core insight from HumanLayer: treat approval as a data type with a lifecycle, not a boolean flag checked by prompt adherence.

## Triage, 2026-07-08

Disposition: still pending in practice, though extensively designed. spec/.intent/specs/SPEC-APPROVAL-GATE.md exists with status: executing and lists this exact signal (by ID) plus its four siblings as source_signals, so the provenance chain is direct and confirmed, not inferred. The spec's IntentApproval entity schema answers every concrete ask across the cluster: id/status/requested_at/decided_at/decided_by/comment fields close the audit-trail gap (SIG-2), ttl_seconds/expires_at plus a revalidation-on-expiry protocol close the TTL gap (SIG-3), and original_payload/approved_payload/modification_detected close the approve-with-modification gap (SIG-4). .intent/config/approval-rules.yml is live on disk with per-action-type TTLs matching this cluster's proposed values exactly (15m Slack, 60m email). What is NOT yet true: .intent/approvals/ contains only _TEMPLATE.md, no live IntentApproval entity has ever been written, and no PreToolUse hook intercepts L0 actions at the tool-call boundary the way the spec describes. So the practical complaint this cluster raises, Brien cannot today reconstruct "what did I approve last Tuesday", remains true: the protocol is fully specified but not yet operational. Needed control: wire the gate skill to a live hook and confirm the first real IntentApproval entity gets written and read back.
