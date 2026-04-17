---
id: SPEC-APPROVAL-GATE
title: "L0 Approval Gate Formalization"
status: executing
intent: Formalize L0 external communication governance from prose to typed protocol
trust_score: 0.865
autonomy_level: L4
shaped_by: [architect, product, quality, agent]
decisions_referenced: [DEC-1, DEC-2, DEC-3, DEC-4, DEC-5, DEC-6]
source_signals:
  - RETRO-2026-04-12-humanlayer-approval-SIG-1
  - RETRO-2026-04-12-humanlayer-approval-SIG-2
  - RETRO-2026-04-12-humanlayer-approval-SIG-3
  - RETRO-2026-04-12-humanlayer-approval-SIG-4
  - RETRO-2026-04-12-humanlayer-approval-SIG-5
  - SIG-2026-04-13-approval-gate-ceremony-tax
  - RETRO-2026-04-13-codelayer-pivot-SIG-1
created: 2026-04-13
---

# SPEC-APPROVAL-GATE — L0 Approval Gate Formalization

## Intent

*Pass 2: Product-Minded Leader*

**Why this exists:** Brien's L0 governance rule ("external communication always requires explicit approval, no exceptions") is enforced by prompt adherence alone. This is the equivalent of a security policy that exists only in a wiki page — it works until it doesn't, and when it fails, there is no trace of the failure. The gap is not that the system acts without permission. The gap is that there is no structured record of what was proposed, what was decided, and why. Denials vanish. Modifications are invisible. Approvals have no expiration.

**Outcome:** Every L0 action (Slack, email, PR, calendar) produces a typed approval record that Brien can review, modify, deny with comment, or time-box elevate. The system builds an audit trail that enables pattern detection — not for ML (deferred) but for Brien's own situational awareness of what his AI agents are attempting to do on his behalf.

**Who benefits:** Brien directly. His consulting practice operates across multiple clients with NDA-protected boundaries. A Slack message to the wrong channel or an email with leaked context is an irreversible reputational event. The gate converts a "trust me" contract into a "verify then act" protocol.

**Behavioral change:** The system shifts from "I will not send external messages" (negative constraint, unverifiable) to "I will construct a typed approval, persist it, present it, and block until decided" (positive protocol, auditable). Brien shifts from hoping the prompt holds to reviewing a structured queue.

**What doesn't matter (v1):** Dashboard UI, multi-channel notification routing, cross-machine sync. These are Phase 3+ concerns.

**Critical design constraint:** The gate must create friction proportional to risk, not proportional to communication volume. A uniform full-gate on all L0 actions reintroduces the ceremony tax Intent was designed to eliminate. See SIG-2026-04-13-approval-gate-ceremony-tax. V1 ships with full gate (safe default, collects training data). V2 introduces contextual action trust with three friction tiers (see Phase 2 below).

## Shape

*Pass 1: Practitioner-Architect*

### Technical Approach

Six deliverables, each independently testable:

1. **IntentApproval Entity Schema** — YAML-frontmatter markdown files in `.intent/approvals/`. Fields: id (ULID-based per SPEC-003), intent_id, signal_id, autonomy_level, action_type (enum: slack_message, email, pr_create, calendar_change), action_target, original_payload, approved_payload, status (pending/approved/denied/expired), requested_at, decided_at, decided_by, comment (required on deny), ttl_seconds, expires_at.

2. **Gate Skill (`intent-approval-gate`)** — Skills Engine methodology module at `methodology/meta/approval-gate.md`. Intercepts at the action boundary. Zero changes to existing skills — the gate is a cross-cutting concern that wraps outbound actions. Process: construct IntentApproval -> persist to `.intent/approvals/` -> present to Brien -> block until decided -> return approved payload or raise denial.

3. **Auto-Accept Rules Config** — `.intent/config/approval-rules.yml`. Maps autonomy levels to actions. L4 auto-approves. L0 requires human. L2 gates above budget threshold. Config is executable — the gate skill reads it at invocation time, not at startup.

4. **TTL with Revalidation** — Per-action-type TTL defaults in the rules config (15m Slack, 60m email, 120m PR, 30m calendar). On expiry: status transitions to expired, `intent.approval.expired` event fires, system revalidates by regenerating the approval with fresh context. Never auto-deny (DEC-4).

5. **Time-Boxed Elevation** — Elevation entity persisted in `.intent/elevations/`. Fields: id, scope (action types), elevated_to (autonomy level), expires_at, reason, created_at. The gate skill checks active elevations before requiring human input. Auto-expires. Full audit trail.

6. **3 OTel Events** — `intent.approval.requested`, `intent.approval.decided`, `intent.approval.expired`. Emitted via the existing events pipeline (fsync+flock wrapper, pending SPEC-004 SQLite migration).

### File Layout

```
.intent/
  approvals/           <- IntentApproval entity files (ULID-named .md)
  elevations/          <- Elevation entity files (ULID-named .md)
  config/
    approval-rules.yml <- Auto-accept rules + TTL defaults
Core/products/skills-engine/
  methodology/meta/
    approval-gate.md   <- Gate skill methodology module
```

### Boundaries

**In scope:** Entity schemas, gate skill spec, rules config, TTL logic, elevation entity, 3 OTel events.

**Out of scope:** Daemon architecture (DEC-5), multi-channel routing, dashboard UI, cross-machine sync, ML pattern detection. These are explicitly deferred — the file-based single-machine model is sufficient for v1.

### Constraining Decisions

- **DEC-1:** IntentApproval as first-class entity (not a boolean gate, not prose)
- **DEC-2:** Approve-with-modification captures the delta between original and approved payload
- **DEC-3:** Time-boxed elevation over per-request bypass (reversible, auditable)
- **DEC-4:** TTL revalidates on expiry, never auto-denies (system regenerates with fresh context)
- **DEC-5:** Daemon architecture deferred (single-user, file-based v1)
- **DEC-6:** Auto-accept rules as executable config (not hardcoded logic)
- **SPEC-003:** ULID-based IDs for all new entities
- **CLAUDE.md L0 rule:** External communication always requires Brien's explicit approval — this spec formalizes that rule, does not weaken it

## Contract

*Pass 3: Design-Quality Advocate*

### Acceptance Criteria

1. **Entity persistence:** Creating an IntentApproval writes a valid YAML-frontmatter markdown file to `.intent/approvals/` with all required fields populated.
2. **Approval lifecycle:** Status transitions follow the state machine: pending -> {approved, denied, expired}. No other transitions. No backward transitions.
3. **Deny requires comment:** Attempting to deny without a comment field fails with a descriptive error.
4. **Modify captures delta:** When Brien approves with modification, both `original_payload` and `approved_payload` are preserved. They must differ (otherwise it's a plain approve).
5. **TTL enforcement:** An approval created with `ttl_seconds: 900` and `requested_at: T` has `expires_at: T+900`. After expiry, status is `expired` and `intent.approval.expired` event fires.
6. **Revalidation on expiry:** Expired approvals trigger regeneration with fresh context, not auto-deny. The new approval is a new entity (new ID), linked to the expired one.
7. **Elevation scoping:** An active elevation for `slack_message` does not auto-approve `email`. Scope is per-action-type.
8. **Elevation expiry:** An elevation with `expires_at` in the past is ignored by the gate skill.
9. **Rules config parse:** `approval-rules.yml` is validated at gate invocation. Malformed YAML produces a clear error and falls back to "require human for everything" (fail-closed).
10. **Event emission:** All three OTel events fire at the correct lifecycle points with the full IntentApproval as payload.

### Failure Modes

- **Config missing:** Gate defaults to L0 (require human) for all actions. Fail-closed.
- **Persistence failure:** Gate blocks the action and surfaces the error. Never proceeds without a persisted approval record.
- **TTL race:** If Brien decides during the expiry window, the decision wins (decided_at < expires_at check).
- **Concurrent elevations:** Multiple active elevations for the same action type — use the most permissive (highest autonomy level). Log a warning signal.

### Verification Commands

```bash
# Entity schema validation
ls .intent/approvals/ | head -5          # Files exist with ULID names
grep "^status:" .intent/approvals/*.md   # All have valid status field

# Lifecycle test
intent-approval create --type slack_message --target "#general" --payload '{"text":"test"}'
intent-approval decide APPR-{id} --status approved
intent-approval decide APPR-{id} --status denied  # Should fail without --comment

# TTL test
intent-approval create --type slack_message --ttl 5  # 5-second TTL for testing
sleep 6
intent-approval show APPR-{id}  # Status should be expired

# Elevation test
intent-elevation create --scope slack_message --level L3 --duration 300
intent-approval create --type slack_message --target "#general" --payload '{"text":"test"}'
# Should auto-approve with decided_by: "auto:elevation-{id}"

# Event verification
tail -3 .intent/events/events.jsonl | jq '.event'
# Should show intent.approval.requested, intent.approval.decided or intent.approval.expired
```

## Agent Notes

*Pass 4: AI Agent Readiness Assessment*

### Trust Score Breakdown

| Dimension | Score | Weight | Weighted | Rationale |
|-----------|-------|--------|----------|-----------|
| Clarity | 0.95 | 0.30 | 0.285 | Seed is exceptionally detailed: entity schema defined, 6 decisions already made, scope boundaries explicit, HumanLayer patterns analyzed |
| 1/Blast radius | 0.85 | 0.20 | 0.170 | New files only. No overwrites. No external side effects until wired to real connectors. Worst case: unused files on disk |
| Reversibility | 0.90 | 0.20 | 0.180 | Schema + config + skill spec. All deletable. No data migration. No existing behavior changes. Existing skills untouched |
| Testability | 0.80 | 0.20 | 0.160 | Schema validation, config parsing, state machine, TTL math all testable in isolation. Integration with real Slack/email/PR connectors needs those connectors present |
| Precedent | 0.70 | 0.10 | 0.070 | HumanLayer provides strong external precedent. No internal precedent for approval entities in Intent (this is the first). SPEC-003 ULID pattern applies |
| **Total** | | | **0.865** | **L4 — Full autonomy** |

### Recommended Autonomy: L4

The spec is well-shaped enough to execute without per-step approval. The agent should build the schema, config, and skill spec, then present the complete set for review. The only L2 gate: if implementation reveals a schema conflict with existing `.intent/` structures, surface before proceeding.

### Required Reads Before Execution

1. `.intent/specs/SPEC-003-sig-022-ulid-migration.md` — ID generation pattern for new entities
2. `Core/products/skills-engine/methodology/meta/intent-journal.md` — Journal persistence patterns
3. `Core/products/skills-engine/methodology/meta/signal-scoring.md` — Trust formula reference
4. `.intent/events/events.jsonl` — Current event schema for OTel event design
5. `Core/frameworks/intent/knowledge-engine/analysis/humanlayer-approval-patterns.md` — Full HumanLayer analysis
6. `RETRO-2026-04-12-humanlayer-approval-DEC-{1-6}.md` — All six adopted decisions

### Ambiguity Flags — RESOLVED (2026-04-13, 12-factor integration)

All four flags resolved via the pause/resume protocol and human-contact-as-capability patterns from the 12-factor agent integration (DDR-006, v0.10.0):

1. **Presentation mechanism — RESOLVED.** The gate emits `human_input.requested` with `urgency: blocking` and `channel` field routing to the appropriate surface. In v1 (in-conversation): the agent pauses (`execution.paused` with checkpoint) and presents inline. If no conversation is active: the approval expires per TTL, triggering revalidation. The `channel` field in the event schema supports future routing to Slack, push notifications, or a dashboard without changing the gate's internal logic.

2. **Revalidation depth — RESOLVED.** On TTL expiry: re-present the same payload with a staleness warning. The checkpoint's `context_snapshot` preserves the original context. The revalidation creates a NEW IntentApproval entity with `linked_expired_id` pointing to the expired one. If Brien wants fresh context, he denies with a comment; the originating skill replans. Max 3 revalidation cycles (per `approval-rules.yml`) before persistent escalation.

3. **Elevation creation surface — RESOLVED.** Elevations are created via `request_human_input` in reverse — Brien responds to an approval with option 4 ("Elevate"), specifying scope and duration. The gate skill parses Brien's response and constructs the Elevation entity. No separate CLI needed for v1. The natural language surface is the conversation itself. Future: CLI (`intent-elevation create`) and Slack reaction patterns.

4. **Payload schema — RESOLVED.** Per-action-type payload schemas defined in `methodology/meta/approval-gate.md`: slack_message (channel + thread_ts + text + blocks), email (to + cc + subject + body + attachments), pr_create (repo + title + body + base + head + draft), pr_comment/issue_comment (repo + number + body), calendar_change (calendar_id + event_id + action + title + start + end + attendees + response).

### Phased Rollout (Brien's Ceremony Tax Constraint)

**Phase 1 — Full Gate (ships first, collects training data)**
All L0 actions go through the full gate: block, present, decide. This is the safe default. Every approval record captures: action_type, action_target, original_payload, approved_payload, modification_detected, decision, comment. This data is the training set for Phase 2.

**Phase 2 — Contextual Action Trust (ships when Phase 1 has enough data)**
Introduce per-action-instance trust scoring using four factors:

| Factor | Weight | Measures |
|--------|--------|----------|
| Precedent | 0.35 | Brien approved N similar actions (same target + similar payload) with low modification rate |
| Familiarity | 0.25 | Target is a channel/person Brien communicates with regularly |
| Novelty | 0.20 | Payload divergence from previously approved payloads to this target |
| Blast radius | 0.20 | Audience size, formality, reversibility (thread reply vs. channel broadcast) |

Three friction tiers based on contextual trust:

| Tier | Trust Range | Behavior | Brien's Experience |
|------|------------|----------|-------------------|
| Full gate | < 0.3 | Block, present, decide | Current approval entity lifecycle |
| Preview | 0.3 - 0.6 | Show summary, 1-tap confirm | Lightweight — sees it, confirms, no comment needed |
| Log-only | ≥ 0.6 | Record and proceed | Action executes immediately; Brien reviews async |

**Circuit breaker:** If Brien retroactively flags or modifies a log-only or preview action, trust for that pattern resets to 0. Self-elevation is earned and revocable.

**Learning loop:** Every decision updates contextual trust:
- Approve without modification → trust increases for this pattern
- Approve with modification → trust stays flat (close but not right)
- Deny → trust decreases significantly for this pattern
- Retroactive flag → trust resets to 0 (circuit breaker fires)

**Phase 2 trigger:** Phase 2 design work begins when Phase 1 has accumulated ≥ 20 approval records with ≥ 3 distinct action targets. Below that threshold, there's not enough data for meaningful trust scoring.

**Phase 2 trigger mechanism:** The gate skill itself checks the threshold on every invocation. When `.intent/approvals/` contains ≥ 20 records with ≥ 3 distinct `action_target` values, the gate emits a signal:
```
signal: "Phase 2 data threshold reached"
id: auto-generated
confidence: 1.0
trust: 0.3
status: captured
data:
  approval_count: N
  distinct_targets: N
  modification_rate: N%
```
This signal is the Phase 2 start trigger. It surfaces in `intent-status signals` and in the overwatch sweep. Brien doesn't need to remember to check.

**Phase 2 pre-work (execute DURING Phase 1, not after):**
1. **Payload similarity metric** — required by precedent (0.35 weight) and novelty (0.20 weight) factors. Combined: 55% of trust score depends on this. Start with template matching or structural fingerprinting. Test against Phase 1 approval records. See RETRO-2026-04-13-approval-gradient-CRITIQUE-1.
2. **Per-action-type payload schemas** — Slack (channel + text + blocks), email (to + subject + body), PR (repo + title + body + base), calendar (event details). Similarity may be action-type-specific.
3. **Familiarity decay function** — channels Brien hasn't messaged in 30 days shouldn't retain high familiarity. Define half-life.

These three items are blocking dependencies for Phase 2 implementation. They are NOT blocked by Phase 1 — design work can start immediately and validate against Phase 1 data as it accumulates.

**Phase 3 — Deferred Infrastructure**
Dashboard UI, multi-channel routing, cross-machine sync, ML pattern detection. Only if Phase 2 validates the gradient model.

### Implementation Sequence

1. Entity schemas (approval + elevation) — independent, no dependencies
2. Rules config YAML + validation — independent
3. OTel event definitions — independent
4. Gate skill methodology module — depends on 1-3
5. CLI commands (`intent-approval`, `intent-elevation`) — depends on 1
6. Integration wiring into existing skill boundary — depends on 4

Steps 1-3 are fully parallelizable. Step 4 composes them. Steps 5-6 are the integration layer.

### Lineage

- **RETRO-2026-04-12-humanlayer-approval-SPEC-SEED-1** — the shaped seed
- **RETRO-2026-04-12-humanlayer-approval-SIG-{1-5}** — the 5 originating signals
- **RETRO-2026-04-12-humanlayer-approval-DEC-{1-6}** — the 6 adopted decisions
- **RETRO-2026-04-12-humanlayer-approval-CRITIQUE-1** — the architectural critique
- **HumanLayer 12-factor-agents** — external pattern source (DEC-21 in Intent CLAUDE.md)
- **SPEC-003** — ULID ID generation pattern
- **SPEC-004** — Events persistence (pending SQLite migration)
- **CLAUDE.md L0 rule** — the governance rule this spec formalizes
