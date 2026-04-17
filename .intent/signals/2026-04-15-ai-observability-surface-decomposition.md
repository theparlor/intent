---
type: signal
stage: draft-spec
date: 2026-04-15
origin: observability-methodology discussion (Brien + Claude, Opus 1M session)
severity: high
scope: intent-framework-observability + cross-vendor AI instrumentation
tags:
  - observability
  - semantic-conventions
  - distributed-tracing
  - otel
  - ai-instrumentation
  - multi-vendor
  - markus-pitch
related_signals:
  - 2026-03-28-otel-for-work.md (SIG-002)
  - 2026-03-30-otel-deployment-spectrum.md (SIG-017)
related_specs:
  - pending — semantic-conventions-for-ai-work (this document is the precursor)
pitch_status: "Draft — intended as push-ready content for Chris Markus review"
---
# Signal / Draft Spec: AI Observability Surface Decomposition

## Why This Exists

SIG-002 established OTel as the format. SIG-017 established the deployment spectrum (JSONL → Grafana → Kafka). Neither answered: **what do we actually observe, per AI surface, and how much of that is natural vs. bolted-on?**

Semantic conventions are a design exercise. OTel has conventions for HTTP, databases, messaging. It does NOT have conventions for "skill invocation," "persona render," "pipeline stage," "agent iteration," "tool gate." We have to define them.

Before writing the schema, we need the constraint map: **what signal is naturally emitted at each AI surface we care about?** Natural signal drives schema viability. A schema that requires deep bolt-on instrumentation at every surface is a schema that never ships.

This document is the constraint decomposition. The schema design happens downstream once the constraints are clear.

---

## Surface Inventory — Three Tiers by Instrumentation Access

### Tier 1 — Natural OTel Fit (no bolt-on, minimal adapter)

These surfaces emit the signals we need through documented, first-class extension points. The schema wraps rather than invents.

| Surface | Natural Signal Source | Span Boundary | Coverage |
|---------|----------------------|---------------|----------|
| **Claude Code (CLI + VS Code ext.)** | Hooks: `PreToolUse`, `PostToolUse`, `Stop`, `SessionStart`. Arbitrary shell command on each event. | Hook-wrapped tool calls are natural spans: PreToolUse = span start, PostToolUse = span end. | Tool-level granularity. Token counts via transcript scan. Session transcripts in `~/.claude/projects/[session]/*.jsonl`. |
| **Claude Agent SDK** | `query()` function exposes hooks, per-message metadata stream (tokens, duration, tool calls). Huryn's 2026-04-14 article confirms: "OTEL exports full traces to Langfuse or any OTLP backend." | Entire query() call is a trace; each hook event is a span. | Excellent — designed for embedded observability. |
| **OpenAI Agents SDK / Responses API** | Returns structured metadata (tokens, tool calls, logprobs). OpenTelemetry Python has an OpenAI auto-instrumentation library that emits spans without application code changes. | Per-completion spans; tool call spans auto-generated. | Good — the OTel community has solved this. Enterprise OpenAI dashboards already consume these spans. |
| **Brien's own Python products** (library-index, fieldbook, etc.) | Direct OTel SDK instrumentation — `otel_config.py` already in library-index. | Manual span wrapping at pipeline stage boundaries. | Full control; best fidelity. |
| **Harness hooks** (bash-level PreToolUse/PostToolUse) | Same as Claude Code row. Hooks are OS-level shell invocations. | Hook invocation = span. | Trivial to instrument; choice pending on whether hook spans join the main trace or stay in a sibling trace. |

### Tier 2 — Partial Fit (adapters required)

Signal exists but is not shaped for direct OTel consumption. Adapter layer needed between native telemetry and OTel format.

| Surface | Natural Signal Source | Adapter Needed | Coverage |
|---------|----------------------|----------------|----------|
| **Claude Cowork** | Sub-agent spawn events visible in UI; sandboxed VM creates an opacity boundary. `/schedule` artifacts emit files. | Poll Cowork's session artifacts; translate to spans post-hoc. OR instrument only the boundary (what goes in, what comes out). | Boundary-level only — can't trace into the sandboxed VM at tool granularity. |
| **Claude Managed Agents** | BRAIN/HANDS/SESSION anatomy — session is a persistent event log per Huryn. Pricing emits billing-grade telemetry ($0.08/session-hour). Per-tool permission events logged. | Unknown whether Anthropic exports OTLP natively. If not, adapter polls session logs and translates. | Depends on Anthropic's telemetry surface maturity. Flag as TBD until verified. |
| **Gemini / Vertex AI** | Google Cloud Trace native; OTel bridge exists via `opentelemetry-exporter-gcp-trace`. Tool-calling metadata returned as structured fields. | Cloud Trace → OTLP bridge (already a shipped library). Semantic attributes may need remapping. | Good once bridge is configured. |
| **GitHub Copilot (Enterprise)** | Admin audit logs; Application Insights integration available for Enterprise tenants. | Azure Monitor → OTLP adapter. Audit-log-level only, not per-keystroke. | Enterprise-access-dependent. Not available on consumer/Pro tiers. |
| **Claude Dispatch / Remote Control / Web Sessions** | Dispatch orchestration events visible at UI layer; underlying session is Code or Cowork (inherits their tier). | Trace context propagation from phone-initiated request to desktop execution requires convention work. | Tier inherited from underlying surface (Code or Cowork). |
| **Claude Channels** | Telegram/Discord bridge — the bridge itself is an external message queue. | Webhook-level instrumentation; bridge service emits OTel spans per bridged event. | Possible but requires bridge-adjacent wiring. |

### Tier 3 — No Natural Fit (bolt-on or skip)

Signal is not client-accessible. Instrumenting requires either provider cooperation, screen scraping, or accepting that this surface is unobservable.

| Surface | Why No Natural Fit | Options |
|---------|-------------------|---------|
| **Claude Chat (consumer web/desktop/mobile)** | Closed client. No hooks, no local instrumentation, no SDK. | Client-side transcript export only (opaque to processing). User-level signal (what was asked, what was returned) but no internal spans. |
| **ChatGPT (consumer)** | Same — closed product. Custom GPT Actions (webhooks) are externally observable but span-less. | Webhook-level observation for Actions. Otherwise, skip. |
| **Gemini (consumer web)** | Same closure. | Skip or treat as black box. |
| **GitHub Copilot (Pro / Individual tier)** | IDE plugin with limited extension API for audit-style telemetry. | Skip unless Enterprise tier. |

**Decision implication:** Tier 3 surfaces should be treated as trace-boundary terminals. Signal enters the trace (user query), leaves the trace (response), and the internal work is opaque. This is an honest architectural position, not a failure.

---

---

## Event Taxonomy — What We Actually Observe

**Vocabulary precision before namespace choice.** "AI" is ambiguous: it spans LLMs, classical ML, inference systems, agents, and whatever marketing departments want it to mean. "Ai.*" as a namespace is noise. What we actually observe is more precise:

### Dimension 1 — What Kind of Computation Happened

| Term | Scope | Examples |
|------|-------|----------|
| **Inference** | Any model producing an output from an input. Provider-neutral. | LLM completion, embedding generation, vision classification, RAG retrieval |
| **LLM Completion** | Specifically a transformer-based language model generating text | Claude, GPT, Gemini text generation |
| **Tool Invocation** | An external capability called by an LLM via function-calling protocol | File read, web fetch, database query, MCP tool call |
| **Agent Iteration** | One cycle of an agent's reasoning loop (observation → thought → action → observation) | Claude Code's autonomous loop; Managed Agent's internal iteration up to 20x |
| **Session Boundary** | Lifecycle event for an agent/conversation container | Session start, session end, context compact, conversation handoff |
| **Hook Invocation** | A governance/guardrail check fired at a tool boundary | PreToolUse, PostToolUse, Stop, SessionStart |

These are **primitive event types**. They are orthogonal to each other — a single agent iteration may contain multiple LLM completions and multiple tool invocations.

### Dimension 2 — Where It Happened

| Term | Scope | Examples |
|------|-------|----------|
| **Provider** | The vendor of the model/platform | `anthropic`, `openai`, `google`, `microsoft`, `meta` |
| **Surface** | The specific implementation the user interacts with | `claude-code`, `claude-cowork`, `claude-agent-sdk`, `openai-chat-completions`, `gemini-vertex`, `copilot-ide` |
| **Model** | The specific model identity | `claude-sonnet-4-6`, `gpt-5`, `gemini-2.5-pro`, `text-embedding-3-large` |

These are **context attributes** on events. They answer "where did this happen" without changing what kind of event it is.

### Dimension 3 — What Work It Belongs To

Attribution back to the work hierarchy. This is the layer that makes observability a governance artifact, not just a performance metric.

- The Intent framework work hierarchy (intent → spec → contract)
- The composable product layer (engagement, product, skill, persona, pipeline stage)
- The autonomy/governance layer (autonomy level, gate state)

---

## Five-Layer Event Model

Raw emissions from surfaces become valuable through transformation. Each layer serves different consumers.

| Layer | What It Is | Example | Consumer |
|-------|-----------|---------|----------|
| **L1 — Raw Events** | Direct emissions from a surface | "Claude Code PostToolUse hook fired for Bash with exit_code=0 at t=1713200400" | Storage only; rarely consumed directly |
| **L2 — Homogenized Events** | Raw events normalized to schema regardless of source | "tool.invocation completed, provider=anthropic, tool=Bash, duration_ms=142, outcome=success" | Dashboards, ad-hoc queries, replay |
| **L3 — Derived Events** | New events computed from sequences/combinations of L2 | "session.ended.within_budget" (computed from cumulative token count + stop event), "skill.chain.completed" (computed from skill invocation sequence) | Alerts, automated reactions, conditional logic |
| **L4 — Time Series / Aggregates** | Rollups over L2/L3 across time | "tokens/hour/engagement", "error-rate/surface/day", "persona-render-latency p95/week" | Trend analysis, capacity planning, rate-limit detection |
| **L5 — Intent Signals** | Human-interpretable observations that feed the work hierarchy | "Cortège IDENTIFY sweep completed with 12 paywall-blocked sources across Tier B — reconsider per-persona paid-tier strategy" | Notice → Spec → Execute → Observe cycle |

**Key design insight:** each layer can be a *consumer* of lower layers and a *producer* for higher layers. The observability system isn't a flat event stream; it's a stack with clear upward transformation.

---

## What Makes an Event Valuable (Capture Criteria)

Not every raw event deserves persistence. The cost of capture (storage, transport, processing) must be justified by derived value. Four criteria govern inclusion:

1. **Actionability** — does observing this event enable a decision or response that couldn't be made without it? (A budget threshold crossing is actionable; a successful read of a known file is background.)
2. **Non-derivability** — can this signal be reconstructed from other captured data, or does it require capture at the moment of occurrence? (Tool-call exit code is non-derivable; total session cost is derivable from per-call costs.)
3. **Downstream feed** — does this event feed a dashboard, alert, automated reaction, or Intent signal? If nothing consumes it, capture is waste.
4. **Aggregation value** — does rolling this up across time reveal patterns the raw data doesn't? (Token usage rollups reveal burn patterns; individual token counts don't.)

**Pragmatic rule:** L1 captures everything the surface emits naturally (low cost because natural). L2 homogenizes only what meets criterion 1 or 2. L3-L5 derive only what meets criterion 3 or 4.

---

## Revised Semantic Conventions — Domain-Native Namespaces

The `ai.*` namespace is retired as ambiguous. The `brien.*` namespace is retired as brand-tied. The replacement is a set of domain-native namespaces that mirror the event taxonomy above.

### L1/L2 — Primitive Event Attributes (provider-neutral)

```yaml
# What kind of computation
inference.type:          # "llm_completion" | "embedding" | "classification" | "vision" | "rag_retrieval"
inference.streaming:     # bool — was this a streamed response

# LLM-specific (when inference.type == "llm_completion")
llm.prompt.tokens:       # integer
llm.completion.tokens:   # integer
llm.prompt.cached:       # integer (prompt-cache hits)
llm.cost.usd:            # float — derived from model + tokens

# Tool invocation
tool.name:               # "Read" | "Bash" | "WebFetch" | MCP tool id
tool.protocol:           # "claude-hook" | "function-calling" | "mcp" | "responses-api"
tool.args_digest:        # SHA-256 of args (not content — PII safety)
tool.result_digest:      # SHA-256 of result
tool.outcome:            # "success" | "error" | "timeout" | "blocked_by_gate"

# Agent iteration (loop cycle within an agent reasoning span)
agent.iteration.index:   # int — 0-based iteration count within the parent span
agent.iteration.reason:  # "tool_result_received" | "self_correct" | "max_turns" | "done"

# Session / conversation boundary
session.lifecycle:       # "started" | "compacted" | "ended_clean" | "ended_error" | "handed_off"
session.id:              # stable identifier

# Hook invocation (governance boundary)
hook.type:               # "PreToolUse" | "PostToolUse" | "Stop" | "SessionStart"
hook.verdict:            # "pass" | "block" | "warn"
```

### Context — Where It Happened

```yaml
provider.name:           # "anthropic" | "openai" | "google" | "microsoft" | "meta" | "local"
surface.id:              # "claude-code" | "claude-cowork" | "claude-agent-sdk" | "openai-responses" | "gemini-vertex" | ...
model.name:              # "claude-sonnet-4-6" | "gpt-5" | "gemini-2.5-pro" | "text-embedding-3-large"
model.version:           # provider-specific version string
```

### Work Attribution — What This Belongs To

Brand-neutral. These namespaces align with the Intent framework and the composable product architecture without naming any human.

```yaml
# Intent framework hierarchy — identical to SIG-002 mapping
intent.id:               # UUID — parent trace context
intent.spec.id:
intent.contract.id:
intent.signal.id:        # set only when this span IS a signal emission
intent.stage:            # "notice" | "spec" | "execute" | "observe"

# Work attribution (brand-neutral — was "brien.*")
work.engagement:         # engagement slug, null for Core work
work.product:            # "skills-engine" | "persona-library" | ...
work.skill:              # skill slug when executing
work.persona:            # persona slug when voice is being rendered
work.platform:           # rendering target — "claude-code" | "agent-sdk" | "copilot" | ...
work.pipeline.stage:     # "identify" | "harvest" | "assess" | "render" | "connect" | "schedule"
work.orchestration:      # "explicit-graph" | "single-call" | "nested"

# Governance
governance.autonomy:     # "L0" | "L1" | "L2" | "L3" | "L4"
governance.gate:         # "passed" | "surfaced" | "bypassed"
governance.reversible:   # bool — did the gate-check mark this as reversible
```

### L3/L4/L5 — Derived Events and Signals

Derived events inherit the span schema from their sources but add a computation-attribution layer.

```yaml
derived.type:            # "budget_threshold" | "error_rate_spike" | "chain_completion" | ...
derived.source_spans:    # array of span IDs that contributed to this derivation
derived.computation:     # identifier for the rule that produced this (for replay / debugging)

# When the derived event is promoted to a signal (L5)
signal.slug:             # human-readable signal name
signal.feeds_intent:     # intent.id the signal is directed to
signal.confidence:       # "low" | "medium" | "high"
signal.captured_at:      # ISO timestamp of signal emission (may be after source span closed)
```

---

## Where OTel-Native Fits, Where Adapters Fit, Where Bolt-On Fits

| Implementation Pattern | Surfaces | Effort | Fidelity |
|-----------------------|----------|--------|----------|
| **OTel-native direct emission** | Brien's Python products, Claude Code (via hook → OTel CLI), Claude Agent SDK, OpenAI Agents SDK | Low | High |
| **OTel adapter layer** | Cowork boundary, Managed Agents (TBD), Vertex AI, Copilot Enterprise | Medium | Medium-High |
| **Bolt-on instrumentation** | Webhook-observed events (Channels, Custom GPT Actions) | Medium | Low-Medium |
| **Trace-boundary terminal (no bolt-on)** | Claude Chat, ChatGPT consumer, Gemini consumer, Copilot individual | Zero | Zero — black box |

**The hook observability question resolves here:** harness hooks are Tier 1 natural-fit. A PreToolUse/PostToolUse hook emitting an OTel span to the JSONL Phase 0 store is 10-20 lines of bash. No new infrastructure. This is the simplest wiring in the entire surface inventory.

## The Markus-Pitch Angle

Why this is worth Markus's time:

1. **Nobody has published AI-work semantic conventions.** OTel has conventions for HTTP (2020), databases (2021), messaging (2022). There is no published convention for skill invocation / agent iteration / persona render / pipeline stage. First-mover has schema-shape influence if anyone else wants to adopt.

2. **The Intent-framework extension is genuinely novel.** Most AI observability work treats spans as operational telemetry. Brien's extensions wire spans back into the *work hierarchy* (intent → spec → contract). That's a different mental model: observability becomes governance artifact, not just performance metric.

3. **Surface decomposition is independent of schema.** The three-tier inventory above stands on its own regardless of whether the schema gets adopted. It's a useful artifact for anyone reasoning about multi-vendor AI observability.

4. **The bolt-on-minimization framing is architecturally disciplined.** A naïve "instrument everything" approach would require massive provider-specific work. Constraint-oriented decomposition reveals that Tier 1 covers Brien's 80% case today (because Brien's stack is Claude-heavy), and Tier 2 adapters extend to 95%. Tier 3 is the honest terminal.

**One-paragraph elevator for Markus:**
> "I've been mapping the observability surface of AI-native work to back into semantic conventions for distributed tracing. OTel has HTTP and database conventions; nothing for LLM inference, tool invocation, or agent iteration as distinct primitives. I built a three-tier surface decomposition (natural-fit, adapter-fit, bolt-on) plus a five-layer event model (raw → homogenized → derived → aggregated → signals). The schema uses domain-native namespaces — `inference.*`, `llm.*`, `tool.*`, `agent.*`, `session.*`, `hook.*` for primitives; `provider.*`, `surface.*`, `model.*` for context; `intent.*`, `work.*`, `governance.*` for attribution. Goal is trace context propagation across multi-surface AI work (phone → Dispatch → desktop Code → SDK-embedded agent) back into an Intent work hierarchy. I want your pressure-test on the event taxonomy and namespace design before I start instrumenting at scale."

## Open Decisions (Explicit Gaps — Brien to Direct)

1. **Hook span lineage:** when a harness-hook span fires, is it a child of the current work trace, or does it live in a sibling "governance" trace? Both are defensible.
2. **Digest-vs-content for args/results:** the schema defaults to hashes for PII safety. When client work is traced, is digest enough, or do we need selective content capture with an encryption layer?
3. **Managed Agents telemetry export:** need to verify with Anthropic whether Managed Agents emit OTLP natively or require adapter polling.
4. **Trace context propagation across Dispatch:** when a phone request enters Dispatch, is the trace ID generated on the phone or on the orchestrator? This is a standard OTel question but has Dispatch-specific answer.
5. ~~**Semantic convention naming namespace:** `ai.*` for provider-agnostic; `brien.*` for Intent-framework extensions.~~ **RESOLVED 2026-04-15:** `ai.*` retired as ambiguous; `brien.*` retired as brand-tied. Replaced by domain-native namespaces mirroring the event taxonomy: `inference.*`, `llm.*`, `tool.*`, `agent.*`, `session.*`, `hook.*` for primitives; `provider.*`, `surface.*`, `model.*` for context; `intent.*`, `work.*`, `governance.*` for attribution; `derived.*`, `signal.*` for computed layers. See revised schema sections above.

6. **Are any L3 derived events general enough to ship as reusable computations?** E.g., `budget_threshold_crossed` applies to any session. `chain_completion` applies to any skill chain. If we define a standard derivation library, other consumers of the semantic convention inherit them. If not, each consumer re-implements.

7. **L1 vs L2 capture locality:** should raw events be captured AT the surface (hook writes OTel span directly) or CLOSE to it (hook writes JSONL, separate process homogenizes to OTel)? The first is simpler but couples surfaces to OTel format; the second is more work but preserves option to change format later.

## Recommended Next Moves (Sequenced)

1. **Brien reads this document, names any missing surfaces or tier reclassifications.** (~15 min)
2. **Brien pushes to Markus for pressure-test on the schema.** Use the elevator paragraph; attach this doc.
3. **If schema survives review:** promote this signal to a formal Spec in `Core/frameworks/intent/.intent/specs/SPEC-NNN-ai-observability-semantic-conventions.md`. Pick a SPEC number.
4. **First implementation target:** instrument ONE skill (candidate: `cortege-fetch` from the agent-sdk signal) with the full schema. Validate that the attributes are queryable and answer real questions ("what was the token burn of yesterday's IDENTIFY sweep by engagement?"). This is the spec validation exercise.
5. **Second target:** replicate OTel wiring from library-index into Skills Engine, using the validated schema. This is where the per-product scaffolding convention (Tier 1 row) gets exercised at scale.

## Cross-Reference

- Precursor signals: SIG-002 (OTel model), SIG-017 (deployment spectrum)
- Companion signals emitted today: `pipeline-components-as-callable-agents` (persona library), `agent-sdk-as-new-rendering-target` (skills-engine), `orchestration-choice-first-class-decision` (intent framework)
- Source concepts: Pawel Huryn 2026-04-14 newsletter (OTel export via Agent SDK), Chris Markus peer architecture review (target audience)
