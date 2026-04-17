---
id: RETRO-2026-04-12-humanlayer-approval-DEC-1
type: decision
source: session-analysis
decided: 2026-04-12
topic: humanlayer-approval
status: decided
---

# Adopt IntentApproval as First-Class Entity

## Context

L0 external communication governance exists as prose in CLAUDE.md. HumanLayer SDK models approval as a persisted entity with full lifecycle (pending → approved/denied), correlation IDs, timestamps, and structured feedback. Brien's Intent framework has 15 OTel events and 5 autonomy levels but no approval entity bridging them.

## Decision

Adopt the IntentApproval entity pattern. Every L0 action generates a typed approval record persisted to the intent journal with: id, intent_id, signal_id, autonomy_level, action_type, action_target, action_payload, status, timestamps, decided_by, and comment.

## Alternatives Considered

1. **Keep prose governance** — rejected; unauditable, non-replayable, relies on prompt adherence
2. **Simple boolean gate** — rejected; loses the structured feedback (comment, modified payload) that makes denials actionable
3. **Full daemon architecture (HumanLayer-style)** — deferred; overbuilt for single-user workflow

## Consequences

- Requires new entity schema in intent journal
- Requires gate skill in Skills Engine
- Enables audit trail, pattern detection, and approval chain replay
- Foundation for future multi-channel routing

## Source

HumanLayer analysis: `Core/frameworks/intent/knowledge-engine/analysis/humanlayer-approval-patterns.md`
