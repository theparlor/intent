---
title: Humanlayer Approval Patterns
type: framework
maturity: final
confidentiality: shareable
reusability: universal
domains:
  - product-taxonomy-operating-models
topics:
  - knowledge-engine
  - knowledge-primitives
created: 2026-04-13
technologies:
  - slack
depth_score: 5
depth_signals:
  file_size_kb: 13.9
  content_chars: 13951
  entity_count: 1
  slide_count: 0
  sheet_count: 0
  topic_count: 3
  has_summary: 0
vocab_density: 0.07
related_entities:
  - {pair: slack ↔ consulting-operations, count: 51, strength: 0.026}
  - {pair: slack ↔ jira, count: 20, strength: 0.084}
  - {pair: product-taxonomy-operating-models ↔ knowledge-primitives, count: 18, strength: 0.72}
  - {pair: knowledge-primitives ↔ knowledge-engine, count: 18, strength: 0.667}
  - {pair: product-taxonomy-operating-models ↔ knowledge-engine, count: 18, strength: 0.529}
---
# HumanLayer Approval Patterns: Applicability to Intent Orchestrator

**Date:** 2026-04-12
**Source:** github.com/humanlayer/humanlayer (monorepo, Go daemon + TypeScript MCP + Tauri WUI)
**Target:** Intent orchestrator L0 external communication gate formalization
**Status:** Analysis complete — architectural patterns extracted, mapping proposed

---

## Executive Summary

HumanLayer's architecture has pivoted from a Python decorator library (`@require_approval`) to a **daemon-based MCP approval gateway** (CodeLayer). The current system is a Go daemon (`hld`) that intercepts Claude Code tool calls via MCP, blocks execution until human approval, and returns structured allow/deny responses. Three patterns are directly applicable to formalizing Brien's L0 external communication gate:

1. **Structured approval request/response** — typed data model with correlation IDs
2. **MCP permission prompt tool** — zero-integration-surface interception
3. **Event-driven decision routing** — channel-based async with SSE fallback

The key architectural insight: HumanLayer treats approval as a **first-class data type with its own lifecycle**, not a boolean flag on a function call. This is the missing piece in Intent's current L0 gate.

---

## Pattern 1: Structured Approval Calls

### What HumanLayer Does

Every approval is a persisted entity with full lifecycle tracking:

```
Approval {
  ID           string          // "local-" + UUID
  RunID        string          // Links to session run
  SessionID    string          // Parent session
  ToolUseID    *string         // Claude's tool_use_id for correlation
  Status       enum            // pending | approved | denied
  CreatedAt    time.Time
  RespondedAt  *time.Time
  ToolName     string          // "Edit", "Write", "Bash", etc.
  ToolInput    json.RawMessage // Arbitrary JSON — the actual tool args
  Comment      string          // Reviewer's comment or auto-accept reason
}
```

Create request requires only `run_id`, `tool_name`, `tool_input`. Decision requires `decision` (approve/deny) + `comment` (required on deny, optional on approve).

### Mapping to Intent Orchestrator

Brien's autonomy levels (L0-L4) currently exist as **prose governance** in CLAUDE.md and the trust-score formula. There is no typed approval entity. The pattern to adopt:

```yaml
# Proposed: IntentApproval entity
approval:
  id: "intent-appr-{uuid}"
  intent_id: "INTENT-{slug}"          # Which intent triggered this
  signal_id: "SIG-{nnn}"              # Which signal detected the need
  autonomy_level: L0                   # Why this requires approval
  action_type: "external_communication" # slack | email | pr | calendar
  action_target: "#channel or recipient"
  action_payload: { ... }             # The exact message/PR/event
  status: pending | approved | denied | expired
  requested_at: ISO8601
  decided_at: ISO8601 | null
  decided_by: "brien" | "auto:{rule}"
  comment: string                      # Required on deny
```

**Key difference from HumanLayer:** Intent approvals are scoped to autonomy levels and action types, not tool names. An `Edit` tool call at L4 never generates an approval. A Slack message at L0 always does. The autonomy level IS the routing rule.

### What This Solves

Today, L0 governance is enforced by Claude's own prompt adherence — "always require Brien's explicit approval." This is:
- **Unauditable** — no record of what was approved/denied
- **Unstructured** — Brien approves by saying "yes" in chat, not by deciding on a typed request
- **Non-replayable** — can't reconstruct the approval chain for a session

A typed approval entity fixes all three.

---

## Pattern 2: MCP Permission Prompt Tool

### What HumanLayer Does

HumanLayer's most elegant pattern: Claude Code has a built-in `permission_prompt_tool` concept. The daemon sets this to an MCP tool name at session launch. Claude's runtime calls this MCP tool *before* executing any restricted tool. The MCP tool blocks until the human decides.

Response format:
```json
// Approved (with optional input modification)
{ "behavior": "allow", "updatedInput": { ... } }

// Denied
{ "behavior": "deny", "message": "Request denied by human reviewer" }
```

**Critical detail:** `updatedInput` means the reviewer can *modify* the proposed action, not just approve/deny. The human can correct the AI's Slack message before it sends.

### Mapping to Intent Orchestrator

This pattern maps directly to a **gate skill** in the Skills Engine:

```
intent-approval-gate (new skill)
  Trigger: Any L0 action detected (Slack send, email send, PR create, calendar change)
  Behavior:
    1. Construct IntentApproval entity from action context
    2. Persist to intent journal
    3. Present to Brien with full context (who, what, why, exact payload)
    4. Block until decision
    5. On approve: execute with original or modified payload
    6. On deny: record reason, return to orchestrator for replanning
```

The `updatedInput` pattern is especially valuable for Brien's workflow. When Claude drafts a Slack message, Brien should be able to:
- Approve as-is
- Edit the message and approve the edited version
- Deny with a reason that feeds back into the next attempt

### What This Solves

Current L0 flow: Claude says "I'd like to send this Slack message, shall I?" — Brien says "yes" or "change X" — Claude sends. This is conversational, not programmatic. The gate skill pattern makes it:
- **Interceptable** — the action is captured before execution
- **Modifiable** — Brien can edit the payload, not just approve/deny
- **Auditable** — every L0 action has a decision record
- **Consistent** — same gate regardless of which skill triggered the action

---

## Pattern 3: Event-Driven Decision Routing

### What HumanLayer Does

Two implementations exist in the codebase (revealing an architectural evolution):

**Polling (TypeScript/hlyr):** 1-second poll loop on approval status. Simple, works everywhere.

**Event-driven (Go/hld):** Channel-per-approval with event bus subscription:
```go
decisionChan := make(chan ApprovalDecision, 1)
s.pendingApprovals.Store(toolUseID, decisionChan)
select {
  case decision := <-decisionChan:  // Immediate on decision
  case <-ctx.Done():                // Context cancellation
}
```

Background goroutine subscribes to `EventApprovalResolved` events, routes to correct channel by `tool_use_id`.

**SSE for external consumers:** `GET /stream/events` with 30s keepalive, filterable by event type/session/run.

### Mapping to Intent Orchestrator

Intent already has an event catalog (15 OTel-compatible events, 6 emission mechanisms). The approval lifecycle maps to three new events:

| Event | When | Payload |
|-------|------|---------|
| `intent.approval.requested` | Gate skill creates approval | Full IntentApproval entity |
| `intent.approval.decided` | Brien approves/denies | Decision + comment + modified payload |
| `intent.approval.expired` | TTL exceeded (see below) | Approval ID + expiry reason |

These compose with existing events (`intent.signal.detected`, `intent.action.executed`) to create a complete audit trail.

**For Brien's workflow specifically:** The polling pattern is sufficient. Brien is in-conversation when approvals fire. The event-driven pattern becomes valuable if/when approvals route to a dashboard or mobile notification — future state, not immediate need.

---

## Pattern 4: Time-Limited Tokens (TTL)

### What HumanLayer Does

Notably, **HumanLayer does NOT implement approval TTL**. The code has a commented-out 5-minute timeout:

```go
// For the moment, we don't timeout approvals, but in the future
// may choose to add a timeout
// case <-time.After(5 * time.Minute):
//   return nil, fmt.Errorf("approval timeout")
```

However, there IS a TTL on **session-level permission bypass** (`DangerouslySkipPermissionsExpiresAt`). This is a time-boxed elevation, not a per-request expiry.

### Mapping to Intent Orchestrator

Brien's L0 actions are context-sensitive. A Slack message drafted 3 hours ago may no longer be appropriate. Implement TTL:

```yaml
approval_ttl:
  default: 30m                    # Approval request expires after 30 minutes
  by_action_type:
    slack_message: 15m            # Slack context decays fast
    email: 60m                    # Email is less time-sensitive
    pr_create: 120m               # PRs can wait
    calendar_change: 30m          # Calendar context is time-bound
  on_expiry: revalidate           # Don't auto-deny; regenerate with fresh context
```

**Key design decision:** On expiry, don't deny — **revalidate**. The action may still be correct but needs fresh context confirmation. This prevents stale approvals from silently executing AND prevents valid actions from being lost.

Also adopt the **time-boxed elevation** pattern for Brien's "just do it" sessions:

```yaml
# Brien says "send freely for the next hour"
elevation:
  scope: [slack_message, email]   # Which L0 actions are elevated
  expires_at: ISO8601             # Absolute expiry
  elevated_to: L3                 # Auto-approve with audit trail
  reason: "Brien granted session elevation"
```

This maps to HumanLayer's `DangerouslySkipPermissions` but with narrower scope (per-action-type, not global).

---

## Pattern 5: Auto-Accept Rules (Bypass Logic)

### What HumanLayer Does

Two bypass modes per session:
1. **DangerouslySkipPermissions** — auto-approves ALL tools (with optional time expiry)
2. **AutoAcceptEdits** — auto-approves only edit tools (Edit, Write, MultiEdit)

The `isEditTool()` function classifies tools. Non-edit tools always go through the gate.

### Mapping to Intent Orchestrator

Brien's L0-L4 levels already encode this, but the bypass logic should be formalized:

```yaml
auto_accept_rules:
  # L4: File creation within Workspaces
  - match: { action_type: "file_write", path_prefix: "Workspaces/" }
    decision: auto_approve
    comment: "L4 autonomy grant: file creation within Workspaces"

  # L3: Research operations
  - match: { action_type: "web_search" }
    decision: auto_approve
    comment: "L3 autonomy grant: research operations"

  # L0: External communication — NEVER auto-approve
  - match: { action_type: ["slack_message", "email", "pr_create", "calendar_change"] }
    decision: require_human
    comment: "L0 governance: external communication requires Brien"

  # L2: Budget decisions above threshold
  - match: { action_type: "budget_decision", estimated_cost_pct: { gt: 10 } }
    decision: require_human
    comment: "L2 governance: >10% weekly budget"
```

This makes the CLAUDE.md prose governance executable and auditable.

---

## Architectural Recommendations

### Adopt Now (Low effort, high value)

1. **IntentApproval entity** — Add to intent journal schema. Every L0 action gets a typed record with status, timestamps, and Brien's comment. This is the foundation everything else builds on.

2. **Required comment on deny** — HumanLayer enforces this; Intent should too. A denial without reason is wasted signal. The comment feeds back into the orchestrator for replanning.

3. **`updatedInput` pattern** — When Brien approves with modifications, capture both the original and modified payload. This is training data for improving future L0 drafts.

### Adopt Next (Medium effort, enables future state)

4. **Gate skill in Skills Engine** — `intent-approval-gate` as a methodology module. Any skill that triggers an L0 action routes through this gate. Consistent interception surface.

5. **TTL with revalidation** — Approval requests expire and regenerate rather than silently dying. Prevents stale action execution.

6. **Time-boxed elevation** — "Send freely for 1 hour" pattern. Scoped to specific action types, auto-expires, maintains full audit trail.

### Defer (Requires infrastructure Brien doesn't need yet)

7. **Daemon architecture** — HumanLayer's Go daemon + SQLite + event bus is overbuilt for Brien's current single-user workflow. The approval entity and gate skill can live within the existing Skills Engine + intent journal.

8. **Multi-channel routing** — HumanLayer's SSE/webhook patterns become relevant when approvals route to a mobile app or dashboard. Brien is in-conversation today.

9. **Correlation by tool_use_id** — Useful when multiple approval requests are in flight. Brien's workflow is sequential enough that intent_id correlation is sufficient.

---

## Key Insight

HumanLayer's deepest architectural lesson isn't about approval mechanics — it's about **treating human decisions as first-class data**. Every approval is persisted, correlated, time-stamped, and commentable. The decision itself has a lifecycle (pending → decided) independent of the action it gates.

Brien's Intent orchestrator already has the event infrastructure (15 OTel events, 6 emission mechanisms) and the governance model (L0-L4 autonomy levels). What's missing is the **approval entity** that bridges them. Add the entity, add the gate skill, and L0 governance goes from "Claude follows a rule" to "the system enforces a protocol."

---

## Upstream Status: HumanLayer → CodeLayer Pivot (2026-04-13)

> **Added post-analysis.** HumanLayer has pivoted. The approval SDK is effectively dead upstream.

The same team (YC-backed, same GitHub org) rebuilt as **CodeLayer** (hlyr.dev/code) — an IDE for orchestrating Claude Code sessions. "Superhuman for Claude Code." The Go daemon architecture (`hld`, `hlyr`, `claudecode-go`) persists as IDE infrastructure, but the approval workflow engine is no longer the product.

**What this means for Intent:**
- The approval entity model we extracted is **orphaned upstream** — they moved away from it. Our implementation has zero upstream dependency. We took the pattern, not the product.
- The approval SDK (`humanlayer.md`) is still in the repo as legacy docs but the README now describes CodeLayer exclusively.
- **Two new patterns emerged from CodeLayer worth tracking:**
  1. **Staged human review gates** — review research before plan, review plan before code. Inverts traditional code review to maximize human leverage earlier. Directly reinforces Intent's thesis: the bottleneck is upstream of execution.
  2. **Intentional context compaction** — deliberate context window management as the primary quality lever. Relevant to how the gate skill presents approval context (compact, not verbose).
- No new approval workflow primitives, dashboards, or multi-session governance patterns beyond what we already captured.

**Signal:** See `RETRO-2026-04-13-codelayer-pivot-SIG-1.md` for the staged-review-gates pattern as a separate signal.

---

## Source References

| Component | Location in HumanLayer | Relevance |
|-----------|----------------------|-----------|
| Approval data model | `hld/store/store.go:237-248` | Direct adoption for IntentApproval entity |
| Auto-accept logic | `hld/approval/manager.go:40-65` | Pattern for L0-L4 bypass rules |
| MCP permission tool | `hld/mcp/server.go:166-201` | Gate skill architecture |
| Event-driven routing | `hld/mcp/server.go` + `hld/bus/events.go` | Future multi-channel routing |
| TTL (commented out) | `hld/mcp/server.go:195-198` | Validates TTL as a recognized need |
| OpenAPI spec | `hld/api/openapi.yaml` | Full REST API for approval CRUD |
| SSE streaming | `hld/api/handlers/sse.go` | Future dashboard/mobile pattern |
| Time-boxed bypass | `hld/approval/manager.go` (`DangerouslySkipPermissions`) | Elevation pattern for "just do it" sessions |
