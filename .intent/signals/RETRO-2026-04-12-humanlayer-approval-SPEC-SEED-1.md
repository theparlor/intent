---
id: RETRO-2026-04-12-humanlayer-approval-SPEC-SEED-1
type: spec-seed
source: session-analysis
created: 2026-04-12
topic: humanlayer-approval
status: needs-shaping
promotes_signals:
  - RETRO-2026-04-12-humanlayer-approval-SIG-1
  - RETRO-2026-04-12-humanlayer-approval-SIG-2
  - RETRO-2026-04-12-humanlayer-approval-SIG-3
  - RETRO-2026-04-12-humanlayer-approval-SIG-4
  - RETRO-2026-04-12-humanlayer-approval-SIG-5
implements_decisions:
  - RETRO-2026-04-12-humanlayer-approval-DEC-1
  - RETRO-2026-04-12-humanlayer-approval-DEC-2
  - RETRO-2026-04-12-humanlayer-approval-DEC-3
  - RETRO-2026-04-12-humanlayer-approval-DEC-4
  - RETRO-2026-04-12-humanlayer-approval-DEC-5
  - RETRO-2026-04-12-humanlayer-approval-DEC-6
---

# Spec Seed: L0 Approval Gate Formalization

> This is a spec seed — structured enough to shape into a formal SPEC but not yet through the four-persona interrogation (Shape/Outcome/Contract/Readiness). Next step: run through spec-shaping protocol.

## Problem

L0 external communication governance (Slack, email, PR creation, calendar changes) relies on prompt adherence. No typed approval entity. No audit trail. No structured feedback on denial. No TTL. No modification capture.

## Proposed Capability

### 1. IntentApproval Entity

```yaml
approval:
  id: "intent-appr-{uuid}"
  intent_id: "INTENT-{slug}"
  signal_id: "SIG-{nnn}"
  autonomy_level: L0
  action_type: slack_message | email | pr_create | calendar_change
  action_target: "channel or recipient"
  original_payload: { ... }     # What the system proposed
  approved_payload: { ... }     # What Brien approved (may differ)
  status: pending | approved | denied | expired
  requested_at: ISO8601
  decided_at: ISO8601 | null
  decided_by: "brien" | "auto:{rule}" | "auto:elevation-{id}"
  comment: string               # Required on deny, optional on approve
  ttl_seconds: int              # Per action_type default
  expires_at: ISO8601           # requested_at + ttl
```

### 2. Gate Skill (`intent-approval-gate`)

New Skills Engine methodology module:
- **Trigger:** Any L0 action detected across all skills
- **Input:** Action type, target, payload, originating skill/intent
- **Process:** Construct IntentApproval → persist → present to Brien → block until decision
- **Output:** Approved payload (original or modified) OR denial with comment
- **Integration:** Zero-change to existing skills — gate intercepts at the action boundary

### 3. Auto-Accept Rules Config

```yaml
# .intent/config/approval-rules.yml
rules:
  - match: { autonomy_level: L4 }
    action: auto_approve
    comment_template: "L4 autonomy: {action_type}"

  - match: { autonomy_level: L3 }
    action: auto_approve
    comment_template: "L3 autonomy: {action_type}"

  - match: { autonomy_level: L0 }
    action: require_human

  - match: { autonomy_level: L2, estimated_cost_pct: { gt: 10 } }
    action: require_human
    comment_template: "L2 budget gate: {estimated_cost_pct}% of weekly"

ttl:
  slack_message: 900      # 15 minutes
  email: 3600             # 1 hour
  pr_create: 7200         # 2 hours
  calendar_change: 1800   # 30 minutes

on_expiry: revalidate     # Regenerate with fresh context, don't auto-deny
```

### 4. Elevation Entity

```yaml
elevation:
  id: "elev-{uuid}"
  scope: [slack_message]        # Which action types
  elevated_to: L3               # Auto-approve at this level
  expires_at: ISO8601
  reason: "Brien granted session elevation"
  created_at: ISO8601
```

### 5. New OTel Events (3)

| Event | Trigger | Payload |
|-------|---------|---------|
| `intent.approval.requested` | Gate creates approval | Full IntentApproval |
| `intent.approval.decided` | Brien decides | Decision + comment + payloads |
| `intent.approval.expired` | TTL exceeded | Approval ID + action |

## Scope Boundaries

**In scope:**
- IntentApproval entity schema and persistence
- Gate skill specification
- Auto-accept rules config
- TTL with revalidation
- Time-boxed elevation
- 3 new OTel events

**Out of scope (deferred):**
- Daemon/persistent process architecture
- Multi-channel routing (Slack bot, mobile push)
- Approval dashboard UI
- Cross-machine approval sync
- Pattern detection on modification deltas (future ML layer)

## External Pattern Reference

Full HumanLayer architectural analysis: `Core/frameworks/intent/knowledge-engine/analysis/humanlayer-approval-patterns.md`

## Next Step

Run through spec-shaping protocol (4-persona interrogation: Shape → Outcome → Contract → Readiness) to produce formal SPEC-NNN.
