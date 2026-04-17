---
id: RETRO-2026-04-12-humanlayer-approval-CRITIQUE-1
type: critique
source: session-analysis
created: 2026-04-12
topic: humanlayer-approval
severity: high
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
