---
title: Event Catalog
type: framework
maturity: final
confidentiality: shareable
reusability: universal
domains:
  - consulting-operations
created: 2026-03-31
technologies:
  - slack
depth_score: 4
depth_signals:
  file_size_kb: 18.8
  content_chars: 18462
  entity_count: 1
  slide_count: 0
  sheet_count: 0
  topic_count: 1
  has_summary: 0
vocab_density: 0.11
related_entities:
  - {pair: consulting-operations ↔ teresa-torres, count: 66, strength: 0.111}
  - {pair: consulting-operations ↔ marty-cagan, count: 63, strength: 0.094}
  - {pair: consulting-operations ↔ subaru, count: 44, strength: 0.121}
  - {pair: consulting-operations ↔ slack, count: 41, strength: 0.124}
  - {pair: consulting-operations ↔ jeff-patton, count: 40, strength: 0.085}
---
# Event Catalog

> 26 events, 7 emission mechanisms, OTel-compatible schema. What gets captured and how, from GitHub Actions to agent self-emission. Extended with pause/resume, human contact, LLM-as-judge, error-retry-escalate protocols (12-factor integration) and L0 approval gate (SPEC-APPROVAL-GATE). Both 2026-04-13.

## Why Events?

Intent's observe layer depends on structured events flowing through the system. Without events, observation is manual — someone has to go look at what happened. With events, observation is automatic: the system tells you what happened, when, and in what context.

Events follow OpenTelemetry conventions. Every event includes a timestamp, source, trace ID (which Intent the work belongs to), and span context (parent-child relationships in the work hierarchy). This isn't just for compatibility with existing observability tools — it's because OTel's trace/span model is structurally isomorphic to how work flows through Intent.

## Event Schema

All events are stored in `.intent/events/events.jsonl` as newline-delimited JSON. Each event follows this schema:

```json
{
  "version": "0.1.0",
  "event": "signal.created",
  "timestamp": "2026-03-28T14:30:00Z",
  "trace_id": "intent-uuid",
  "span_id": "work-unit-uuid",
  "parent_id": "parent-span-uuid",
  "source": "github-action",
  "data": {
    "signal_id": "SIG-001",
    "confidence": 0.92,
    "title": "Work needs a formal ontology"
  }
}
```

Key fields:

- **version:** Schema version (semver). Current: 0.1.0
- **event:** Event name from the catalog below
- **timestamp:** ISO 8601
- **trace_id:** Maps to an Intent — all work units under one intent share a trace
- **span_id:** Unique ID for this specific work unit
- **parent_id:** The parent work unit (null for top-level)
- **source:** What emitted this event (github-action, agent, entire.io, manual, etc.)
- **data:** Event-specific payload

## The 25 Events

### Notice Phase

| Event | Description | Trigger |
|-------|-------------|--------|
| `signal.created` | New signal captured from work, research, or conversation | PR merged with file in `.intent/signals/` |
| `intent.proposed` | Intent created, linking signals to desired change | PR merged with file in `.intent/intents/` |
| `intent.approved` | Intent approved to proceed to spec | PR review approved on intent file |

### Spec Phase

| Event | Description | Trigger |
|-------|-------------|--------|
| `spec.written` | Spec created with narrative, acceptance criteria, and contract assertions | PR merged with file in `.intent/specs/` |
| `spec.staged` | Spec moves from draft to ready-for-execution | Label applied or status field changed |
| `decision.recorded` | Significant decision documented with context and rationale | Manual emission when decision is recorded |

### Execute Phase

| Event | Description | Trigger |
|-------|-------------|--------|
| `contract.started` | Agent begins executing a contract | Agent session start (self-emitting) |
| `contract.assertion.passed` | A contract assertion passes | Test runner (self-emitting agent) |
| `contract.assertion.failed` | A contract assertion fails | Test runner (self-emitting agent) |
| `contract.completed` | All assertions pass and contract is fulfilled | Agent session end (self-emitting) |
| `execution.paused` | Agent suspends execution waiting for external event | Agent self-emitting (see Pause/Resume Protocol) |
| `execution.resumed` | Agent resumes from checkpoint after external event | Webhook, human response, or timer (see Pause/Resume Protocol) |
| `execution.error_retry` | Agent retried a failed tool call with error context appended | Agent self-emitting (see Error-Retry-Escalate) |
| `execution.escalated` | Agent exhausted retries and escalated to human or higher trust level | Agent self-emitting (see Error-Retry-Escalate) |
| `human_input.requested` | Agent proactively requested human input as a strategic choice | Agent self-emitting (see Human Contact as Capability) |
| `human_input.received` | Human responded to a request_human_input call | Webhook or signal callback |
| `intent.approval.requested` | L0 action intercepted, IntentApproval entity constructed and presented | Gate skill (see Approval Gate Protocol) |
| `intent.approval.decided` | Brien approved or denied an L0 action | Gate skill after Brien's decision |
| `intent.approval.expired` | Approval TTL elapsed without decision, triggering revalidation | Gate skill TTL monitor |
| `intent.approval.elevated` | L0 action auto-approved via active time-boxed elevation | Gate skill elevation check |
| `capability.released` | Reusable building block added to the system | PR merged with capability code |
| `feature.released` | Feature ships to production | Deployment pipeline |

### Approval Gate (L0 Governance)

| Event | Description | Trigger |
|-------|-------------|--------|
| `approval.requested` | L0 action intercepted, approval entity created, waiting for human decision | Gate skill constructs IntentApproval entity |
| `approval.decided` | Human approved (with optional modification) or denied (with required comment) | Brien responds to approval request |
| `approval.expired` | Approval TTL elapsed, triggering revalidation with fresh context | Timer expiry on pending approval |

### Observe Phase

| Event | Description | Trigger |
|-------|-------------|--------|
| `trace.completed` | Agent completes execution, all traces aggregated | Entire.io session hook |
| `observation.written` | Observe layer reads traces and writes findings | Log file watcher or scheduled job |
| `observation.evaluated` | LLM-as-judge evaluated execution output against spec criteria | Observe agent (see LLM-as-Judge Protocol) |
| `system.health` | Periodic emission of system health metrics | Scheduled cron (Zapier or GitHub Action) |

## Emission Mechanisms

Events don't all come from the same place. Intent uses 7 distinct emission mechanisms, reflecting the reality that work happens across many surfaces:

### 1. GitHub Action (9 events — 41% coverage)
The primary emission source. A GitHub Action watches for file changes in `.intent/` directories and emits the corresponding event. Covers: `signal.created`, `intent.proposed`, `intent.approved`, `spec.written`, `spec.staged`, `decision.recorded`, `capability.released`, `feature.released`, `system.health`.

### 2. Self-Emitting Agent (14 events — 54% coverage)
AI agents emit events during execution. Contract lifecycle: `contract.started`, `contract.assertion.passed`, `contract.assertion.failed`, `contract.completed`. Execution control: `execution.paused`, `execution.resumed`, `execution.error_retry`, `execution.escalated`. Human contact: `human_input.requested`. Approval gate: `intent.approval.requested`, `intent.approval.decided`, `intent.approval.expired`, `intent.approval.elevated`. Observation: `observation.evaluated`. Requires agent instrumentation.

### 3. Entire.io Session Hook (1 event)
Entire.io captures end-to-end execution traces. When a session completes, it emits `trace.completed` with aggregated span data.

### 4. Log File Watcher (1 event)
A file system watcher monitors `.intent/events/` for new observation files and emits `observation.written`.

### 5. Zapier (1 event)
External signal ingestion. When signals come from outside the development workflow (customer support tickets, Slack conversations, analytics anomalies), a Zapier integration can emit `signal.created`.

### 6. Webhook / External Callback (1 event)
When a human responds to a `human_input.requested` event or an external system completes a long-running operation, webhooks emit `human_input.received` or `execution.resumed`. This is the primary resume trigger for paused agents.

### 7. Manual (fallback)
Any event can be manually emitted by adding a line to `events.jsonl`. This is the escape hatch for events that don't yet have automated emission.

## Implementation Phases

The event system rolls out incrementally:

1. **Manual emission** — Write events by hand to validate the schema
2. **GitHub Action** — Automate the 9 events triggered by file changes
3. **Agent self-emission** — Instrument Claude Code to emit contract events
4. **Entire.io integration** — Connect trace completion to event stream
5. **External signals** — Set up Zapier or webhook ingestion
6. **OTel upgrade** — Migrate from JSONL to full OTel collector for production teams

## Pause/Resume Protocol

Agents need to suspend execution when waiting for external events (human approval, webhook callbacks, long-running operations, external API responses). The pause/resume protocol formalizes this as a first-class execution pattern.

### Checkpoint Serialization

When an agent emits `execution.paused`, it serializes a checkpoint to the event data:

```json
{
  "event": "execution.paused",
  "timestamp": "2026-04-13T10:30:00Z",
  "trace_id": "intent-uuid",
  "span_id": "work-unit-uuid",
  "source": "agent",
  "data": {
    "reason": "awaiting_human_input | awaiting_webhook | awaiting_timer | awaiting_dependency",
    "checkpoint": {
      "spec_id": "SPEC-NNN",
      "contract_id": "CON-NNN",
      "step_index": 3,
      "context_snapshot": "base64-encoded or reference to context file",
      "tools_completed": ["tool_a", "tool_b"],
      "tools_remaining": ["tool_c"],
      "next_action": "Description of what to do when resumed"
    },
    "resume_trigger": {
      "type": "webhook | human_response | timer | signal",
      "endpoint": "https://...",
      "timeout_seconds": 86400,
      "fallback": "escalate_to_human | retry | abandon"
    }
  }
}
```

### Resume Semantics

When the external event fires, the system emits `execution.resumed` and the agent reconstructs state from the checkpoint:

1. Load the checkpoint from the most recent `execution.paused` event for this trace
2. Restore context: spec, contract, completed steps, remaining steps
3. Append the external event's payload to context (the human's answer, the webhook data, etc.)
4. Continue execution from `next_action`

If `timeout_seconds` elapses without a resume trigger, the system executes the `fallback` action.

### Integration with Trust Model

- **L0 specs:** Use the formal approval gate protocol (`approval.requested` → `approval.decided`/`approval.expired`) rather than generic pause/resume. All external communications (Slack, email, PR, calendar) route through this gate.
- **L1-L2 specs:** Pause is mandatory before executing high-blast-radius tool calls. Resume requires human approval signal.
- **L3 specs:** Pause is optional — agent may pause for external data but not for approval.
- **L4 specs:** Pause only for external dependencies (webhooks, timers). Never for approval.

## Human Contact as Capability

Distinct from trust-gated approval (top-down governance), `request_human_input` is a tool the agent can invoke as a **strategic choice** (bottom-up capability). The agent decides WHEN to ask a human, not just WHETHER it's allowed to proceed.

### When Agents Should Request Human Input

- **Ambiguity resolution:** The spec is unclear and the agent needs clarification before proceeding
- **Domain expertise:** The agent recognizes it lacks domain knowledge to make a judgment call
- **Risk assessment:** The agent identifies a decision with consequences it can't fully evaluate
- **Preference elicitation:** Multiple valid approaches exist and the agent wants the human's preference
- **Confirmation of novel action:** The agent is about to do something it hasn't done before in this context

### Event Schema

```json
{
  "event": "human_input.requested",
  "data": {
    "question": "Plain language question for the human",
    "context": "Why the agent is asking — what it knows, what it doesn't",
    "options": ["Option A", "Option B", "Let me decide"],
    "urgency": "blocking | informational | deferred",
    "channel": "slack | signal | cli | mcp",
    "timeout_seconds": 3600,
    "fallback_action": "Description of what agent will do if no response"
  }
}
```

### Relationship to Trust Levels

| Trust Level | Governance Gate (existing) | Strategic Request (new) |
|-------------|--------------------------|------------------------|
| L0 | Human drives all | Agent can still request specific input |
| L1 | Human decides | Agent enriches AND can ask targeted questions |
| L2 | Human approves | Agent can request input on ambiguous sub-decisions |
| L3 | Human monitors | Agent can request input when domain expertise needed |
| L4 | Circuit breaker only | Agent can request input for novel situations |

The key distinction: governance gates are **mandatory** (the agent MUST stop). Strategic requests are **voluntary** (the agent CHOOSES to ask). Both produce pause/resume events, but the trigger is different — compliance vs. judgment.

## LLM-as-Judge Protocol

After execution completes, the Observe phase can invoke an LLM to evaluate whether the output actually satisfies the spec's intent — not just its contracts. Contracts verify mechanical correctness; LLM-as-judge evaluates semantic quality.

### When to Use LLM-as-Judge

- **Spec has qualitative criteria:** "The documentation should be clear and well-organized"
- **Output requires domain judgment:** Code review, content quality, design coherence
- **Contract coverage is incomplete:** The spec describes intent that can't be fully captured in assertions
- **Novel execution:** First time this type of spec has been executed — no precedent to compare against

### Evaluation Schema

```json
{
  "event": "observation.evaluated",
  "data": {
    "spec_id": "SPEC-NNN",
    "evaluator_model": "opus-4.6",
    "criteria": [
      {
        "dimension": "completeness",
        "question": "Does the output address all requirements in the spec?",
        "score": 0.85,
        "evidence": "Covers sections 1-4, missing edge case in section 5"
      },
      {
        "dimension": "quality",
        "question": "Is the output well-structured and clear?",
        "score": 0.92,
        "evidence": "Clean organization, consistent style"
      }
    ],
    "overall_score": 0.88,
    "verdict": "pass | conditional_pass | fail",
    "recommendations": ["Address the edge case in section 5"],
    "contracts_passed": true,
    "semantic_gap": "Contracts all pass but section 5 edge case represents semantic gap"
  }
}
```

### Integration with Observe Loop

1. `contract.completed` fires (all mechanical assertions pass)
2. If spec has `evaluate: true` in frontmatter, trigger LLM-as-judge
3. LLM evaluates output against spec criteria (not contracts — the spec's prose intent)
4. `observation.evaluated` fires with scores and verdict
5. If verdict is `fail`: emit a new signal describing the gap → feeds back to Notice
6. If verdict is `conditional_pass`: emit signal + mark spec as complete with caveats
7. If verdict is `pass`: spec marked complete, no further action

This closes the gap between "contracts pass" (mechanical truth) and "the spec is satisfied" (semantic truth).

## Error-Retry-Escalate Pattern

Standard behavior for agent execution when tool calls fail. This pattern is codified at the platform level (Skills Engine platform specs) rather than the methodology level, but emits events into Intent's event stream.

### The Pattern

```
Tool call fails
  → Append error message + context to agent's working context
  → Increment retry counter for this tool
  → If retries < max_retries (default: 3):
      → LLM reads error context and adjusts approach
      → Emit execution.error_retry event
      → Re-attempt tool call
  → If retries >= max_retries:
      → Emit execution.escalated event
      → Route based on trust level:
          L0-L2: Notify human immediately
          L3: Log observation, continue if non-critical / pause if critical
          L4: Auto-degrade to L3 for this tool, retry with human monitoring
```

### Event Data

```json
{
  "event": "execution.error_retry",
  "data": {
    "tool_name": "create_file",
    "error": "Permission denied: /etc/hosts",
    "retry_number": 2,
    "max_retries": 3,
    "adjustment": "Switching to user-writable path"
  }
}
```

```json
{
  "event": "execution.escalated",
  "data": {
    "tool_name": "create_file",
    "error": "Permission denied after 3 attempts",
    "retry_count": 3,
    "escalation_target": "human_queue",
    "trust_level": "L3",
    "degraded_to": "L2"
  }
}
```

### Self-Healing Properties

- Errors become context, not dead-ends. The LLM reads the error and adapts.
- Retry caps prevent infinite loops (the "error spin-out" antipattern).
- Escalation is trust-aware — L4 agents degrade gracefully rather than failing hard.
- Every retry and escalation is an event, making the pattern fully observable.

## Approval Gate Protocol

L0 actions (Slack messages, emails, PR creation, calendar changes) are intercepted before execution. Instead of proceeding, the system creates an IntentApproval entity and waits for Brien's explicit decision. This formalizes the L0 governance rule as a first-class event-driven protocol rather than relying on implicit agent behavior.

### Event Data

```json
{
  "event": "approval.requested",
  "data": {
    "approval_id": "intent-appr-uuid",
    "intent_id": "INTENT-slug (if available)",
    "autonomy_level": "L0",
    "action_type": "slack_message | email | pr_create | calendar_change",
    "action_target": "channel or recipient",
    "original_payload": { },
    "originating_skill": "skill-name",
    "ttl_seconds": 900,
    "expires_at": "ISO8601"
  }
}
```

```json
{
  "event": "approval.decided",
  "data": {
    "approval_id": "intent-appr-uuid",
    "decision": "approved | denied",
    "decided_by": "brien | auto:elevation-uuid",
    "original_payload": { },
    "approved_payload": { },
    "comment": "string (required on deny)",
    "modification_detected": true
  }
}
```

```json
{
  "event": "approval.expired",
  "data": {
    "approval_id": "intent-appr-uuid",
    "action_type": "slack_message",
    "ttl_seconds": 900,
    "revalidation_triggered": true,
    "new_approval_id": "intent-appr-new-uuid"
  }
}
```

## Where Events Live

- **Storage:** `.intent/events/events.jsonl` in each Intent-native repo
- **Interactive artifact:** [Event Catalog (React)](../artifacts/intent-event-catalog.jsx)
- **Site page:** rendered at theparlor/intent-site <!-- broken link removed: ../docs/event-catalog.html (site moved to separate repo per CLAUDE.md; this repo has no docs/) -->
