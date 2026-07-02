---
id: RETRO-2026-04-12-humanlayer-approval-SIG-1
type: signal
category: architecture-gap
severity: high
source: session-analysis
detected: 2026-04-12
topic: humanlayer-approval
status: promoted
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
