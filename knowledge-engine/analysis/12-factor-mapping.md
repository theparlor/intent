---
title: 12 Factor Mapping
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
frameworks:
  - double-loop-learning
depth_score: 5
depth_signals:
  file_size_kb: 19.7
  content_chars: 18737
  entity_count: 2
  slide_count: 0
  sheet_count: 0
  topic_count: 3
  has_summary: 0
vocab_density: 0.27
related_entities:
  - {pair: consulting-operations ↔ slack, count: 41, strength: 0.132}
  - {pair: knowledge-primitives ↔ product-taxonomy-operating-models, count: 18, strength: 0.72}
  - {pair: knowledge-engine ↔ knowledge-primitives, count: 18, strength: 0.667}
  - {pair: knowledge-engine ↔ product-taxonomy-operating-models, count: 18, strength: 0.529}
  - {pair: knowledge-engine ↔ matthew-skelton, count: 13, strength: 0.035}
---
# 12-Factor Agents → Intent Framework Mapping

> **Source:** [humanlayer/12-factor-agents](https://github.com/humanlayer/12-factor-agents) by Dex (HumanLayer)
> **Target:** Intent Framework (Core/frameworks/intent/) — methodology + Knowledge Engine + Knowledge Farm
> **Date:** 2026-04-12
> **Purpose:** Map each factor to existing Intent concepts. Surface gaps where 12-factor covers territory we don't.

---

## Orientation

The 12-factor-agents manifesto is an **implementation-level** guide for building LLM-powered agents in production. Intent is an **operating-model-level** framework for orchestrating human-AI work across the Notice→Spec→Execute→Observe loop. They operate at different altitudes:

| Dimension | 12-Factor Agents | Intent Framework |
|-----------|-----------------|------------------|
| **Primary concern** | How to build a single agent well | How to orchestrate a system of work |
| **Unit of analysis** | One agent's control loop | Signal → Intent → Spec → Contract → Capability → Feature → Product |
| **Audience** | AI engineers writing agent code | System designers composing human-AI workflows |
| **Key metaphor** | Stateless reducer over events | Continuous transformation OS with trust-gated autonomy |

This altitude difference means: Intent rarely contradicts 12-factor — it operates above it. The gaps are downward (Intent doesn't specify agent internals) rather than lateral (competing models for the same problem).

---

## Factor-by-Factor Mapping

### Factor 1: Natural Language → Tool Calls
**12-Factor:** LLM converts natural language to structured JSON; deterministic code routes execution.

**Intent equivalent:** The **Skill Graph** (methodology × persona × platform) is the structured output layer. Skills are the "tool calls" — each skill is a typed, composable unit that deterministic code (the skills engine platform renderer) routes. The **spec-shaping protocol** converts natural language intents into agent-ready specs with 10 structured dimensions.

**Coverage:** Full overlap at the architectural level. Intent doesn't prescribe JSON schema design for individual tool calls — that's below its altitude.

---

### Factor 2: Own Your Prompts
**12-Factor:** Don't outsource prompt engineering to frameworks. Treat prompts as first-class code.

**Intent equivalent:** **SKILL.md files** are first-class prompt artifacts — version-controlled, testable, composable. The three-layer rendering (methodology × persona × platform) means prompts are never black-boxed. The **platform spec** layer explicitly controls how prompts render per environment (Claude Code, Copilot, system-prompts).

**Coverage:** Strong alignment. Intent's skill architecture is essentially the "own your prompts" principle elevated to a composable system. The persona layer goes further — 12-factor doesn't address voice/perspective as a prompt dimension.

---

### Factor 3: Own Your Context Window
**12-Factor:** Everything is context engineering. Build custom context formats. Control what goes in.

**Intent equivalent:** The **Context Resolver** is the direct analog — it determines what knowledge, signals, and state get loaded into any given agent invocation. The **Knowledge Engine** (compiled knowledge base, not RAG — DDR-001) is the context supply chain. The **federation model** (inherit down, promote up, never leak sideways) is a context access control policy.

**Coverage:** Intent goes deeper here. The Knowledge Engine's compilation model, confidence scoring, and federation are more sophisticated context engineering than 12-factor describes. 12-factor treats context as a single-agent concern; Intent treats it as a system-level concern with cross-engagement boundaries.

---

### Factor 4: Tools Are Just Structured Outputs
**12-Factor:** Tools are JSON the LLM outputs; deterministic code decides what to actually execute. The LLM decides *what*, your code controls *how*.

**Intent equivalent:** The **Contract** layer in the work ontology (Signal → Intent → Spec → **Contract** → Capability → Feature → Product). Contracts define verification criteria independently of execution. The **trust model** adds a gate between "LLM decided what" and "code executes how" — the trust score determines whether execution proceeds automatically (L3-L4) or requires human approval (L0-L2).

**Coverage:** Intent adds a trust dimension that 12-factor lacks. 12-factor assumes all tool calls execute (with optional human-in-the-loop). Intent makes the execution gate a first-class, scored decision.

---

### Factor 5: Unify Execution State and Business State
**12-Factor:** Don't separate "what step are we on" from "what's happened." Infer execution state from the context window. One source of truth.

**Intent equivalent:** The **Intent Journal** and **event system** (events.jsonl, 15 OTel-compatible events). Intent's trace identity model — "an Intent is a Trace, everything under it is a Span" — unifies execution and business state by design. The **signal amplification** system (reference frequency, time-decayed scoring) means execution history IS business state.

**Coverage:** Strong alignment in principle. However, Intent's state model is distributed (signals, events, specs across files) rather than a single context window. This is a deliberate architectural choice (DDR-002, three-layer architecture) — the compiled knowledge base, transformation OS, and software spec layers each carry state. 12-factor's "single context window" model is simpler but doesn't scale to multi-agent, multi-engagement orchestration.

**Tension:** Intent's three-layer state is more powerful but violates the "one source of truth" simplicity that 12-factor advocates. The resolution: each individual agent invocation CAN have unified state (via context resolver), while the system-level state remains distributed. This is worth being explicit about.

---

### Factor 6: Launch/Pause/Resume with Simple APIs
**12-Factor:** Agents should be easy to start, pause (for long-running ops), and resume (via webhooks). The gap: most frameworks can't pause between tool selection and tool execution.

**Intent equivalent:** The **MCP server architecture** (intent-notice:8001, intent-spec:8002, intent-observe:8003) provides the launch API. The **trust model's** L0-L2 levels are architecturally a pause-for-approval mechanism. **SPEC-003's** entity lifecycle (created → active → enriched → stale → deprecated → archived) provides state management for paused entities.

**Gap identified:** Intent doesn't have an explicit **pause/resume protocol** at the agent execution level. The trust model gates execution but doesn't formalize "agent is waiting for external event X." The session concurrency model (WS-DDR-018, SESSION_QUEUE.md) addresses multi-session coordination but not mid-execution pause/resume of a single agent run. **This is a real gap** — especially for the Fieldbook expense pipeline (INTAKE waits for receipt image) and any webhook-triggered resumption.

---

### Factor 7: Contact Humans with Tool Calls
**12-Factor:** Human contact is a tool call (RequestHumanInput), not a mode switch. Enables outer-loop agents (Agent→Human flow vs. Human→Agent).

**Intent equivalent:** The **trust model** implicitly handles this — L0-L2 specs require human approval, which is functionally "contacting a human." The **signal capture system's** Tier 3 (Slack reactions/slash commands) and the planned Tier 5 (AI plugins) are human-contact channels. The **spec-shaping protocol's** four-persona interrogation is a structured human-contact pattern.

**Gap identified:** Intent treats human contact as a **governance constraint** (trust levels gate execution), not as an **agent capability** (a tool the agent can invoke). The 12-factor framing is more flexible — the agent decides WHEN to contact a human, not just WHETHER it's allowed to proceed. Intent's L0 says "always ask Brien." 12-factor says "the agent has a tool called ask_human and uses judgment about when to invoke it." **This is a meaningful architectural difference** — Intent's model is top-down (governance says when), 12-factor's is bottom-up (agent decides when).

The autonomy grant system partially addresses this (L3+ agents execute without approval), but doesn't give agents the inverse capability: proactively requesting human input as a strategic choice rather than a compliance requirement.

---

### Factor 8: Own Your Control Flow
**12-Factor:** Build your own loop: summarization, caching, LLM-as-judge, context compaction, rate limiting, durable pause. The critical feature request: interrupt and resume between tool selection and invocation.

**Intent equivalent:** The **Notice→Spec→Execute→Observe loop** IS the control flow. The **spec-shaping protocol** (4-pass interrogation) is a structured control flow for spec creation. The **signal enrichment pipeline** (Source Adapter → Dedup → Context → Trust Scorer → Classifier → Router) is explicit control flow for signal processing.

**Coverage:** Intent owns control flow at the methodology level. However, it doesn't prescribe how individual agent implementations should structure their internal loops. The Skills Engine platform renderers could be the place where this gets codified — each platform spec could define its control flow patterns.

**Gap identified:** No explicit pattern for **LLM-as-judge** within the framework. The contract verification system (CON-KE-001 through CON-KE-010) defines WHAT to verify, but doesn't specify that an LLM should evaluate the output. The trust model scores specs, not outputs. Adding an **observe-phase LLM evaluation** pattern would close this.

---

### Factor 9: Compact Errors into Context Window
**12-Factor:** Self-healing: append errors to context, let LLM retry with awareness. Cap retries (~3), then escalate.

**Intent equivalent:** The **Observe phase** captures execution outcomes. The **signal system** can surface errors as signals. The **event catalog's** 15 events include failure states. The **double-loop learning** (Observe → Knowledge, DDR-003) means errors feed back into the compiled knowledge base.

**Gap identified:** Intent doesn't have an explicit **error-as-context** pattern for individual agent runs. The Observe phase captures what happened, but doesn't prescribe "append the error to the context window and retry." This is below Intent's altitude — it's an agent implementation pattern, not an orchestration pattern. However, the Skills Engine platform specs COULD codify this as a standard behavior: "on tool failure, append error context and retry up to N times before escalating to trust-level-appropriate human."

---

### Factor 10: Small, Focused Agents
**12-Factor:** 3-10 steps per agent. Bigger context = worse performance. One agent, one job.

**Intent equivalent:** The **Skills Engine architecture** (methodology × persona × platform) is inherently composable — each skill is small and focused. The **skill graph** composes small skills into chains via the intent-orchestrator. The **parallel pipeline template** launches focused agents simultaneously.

**Coverage:** Strong alignment. Intent's composability model IS the small-focused-agent principle applied at the methodology level. The 3-10 step heuristic maps well to individual skills. The orchestrator handles composition.

---

### Factor 11: Trigger From Anywhere, Meet Users Where They Are
**12-Factor:** Slack, email, SMS, cron, webhooks. Agents as digital coworkers.

**Intent equivalent:** The **signal capture system's 5-tier adapter architecture** is the direct analog:
- Tier 1: MCP Server (Claude Code, Cowork, Cursor)
- Tier 2: CLI (bin/intent-signal)
- Tier 3: Slack (reaction/slash command)
- Tier 4: GitHub native (labels, comments)
- Tier 5: AI plugins (ChatGPT, Copilot, Codex)

**Coverage:** Full overlap. Intent's adapter architecture is more structured than 12-factor's "trigger from anywhere" — it explicitly defines tiers, enrichment pipelines, and dedup. The Scheduled Tasks MCP and cron capabilities extend this further.

---

### Factor 12: Agent as Stateless Reducer
**12-Factor:** Agent is a pure function: fold/reduce over an event stream. Stateless.

**Intent equivalent:** The **event system** (events.jsonl, OTel traces) is an event stream. The **Notice→Spec→Execute→Observe loop** is a reducer over signals. The **signal amplification** (time-decayed scoring over reference events) is literally a fold operation.

**Coverage:** Conceptual alignment, different formalization. Intent doesn't claim agents are stateless reducers — it claims the SYSTEM is a continuous transformation loop. The distinction matters: 12-factor says each agent invocation is pure; Intent says the loop maintains state across invocations via the knowledge base and signal log. Intent is stateful by design (compiled knowledge, entity lifecycles), with individual agent calls being stateless within their context window.

---

### Factor 13 (Appendix): Pre-fetch Context
**12-Factor:** If you know the model will need data X, fetch it deterministically before the LLM call.

**Intent equivalent:** The **Context Resolver** does exactly this — it pre-loads relevant knowledge, signals, and state before agent invocation. DDR-001 (compilation over RAG) is the extreme version: pre-compute ALL the context rather than fetching on demand.

**Coverage:** Intent goes further. DDR-001's compilation model is pre-fetching elevated to an architectural principle. The Knowledge Engine's compiled artifacts are permanently pre-fetched context.

---

## Gap Summary

### Gaps Where 12-Factor Covers Territory Intent Doesn't

| # | Gap | 12-Factor Factor | Severity | Resolution Path |
|---|-----|------------------|----------|-----------------|
| G1 | **No explicit pause/resume protocol** for mid-execution agent suspension | F6 (Launch/Pause/Resume) | High | Add a PAUSE event type to the event catalog + define resume-from-checkpoint semantics in SPEC-003's entity lifecycle |
| G2 | **Human contact as agent capability vs. governance constraint** — agents can't proactively request input as a strategic tool call | F7 (Contact Humans) | High | Add `request_human_input` as a first-class signal type that agents can emit at any trust level, distinct from trust-gated approval |
| G3 | **No LLM-as-judge pattern** in the Observe phase | F8 (Own Control Flow) | Medium | Define an observation contract type where an LLM evaluates output quality against spec criteria before marking execution complete |
| G4 | **No error-retry-escalate pattern** at the agent execution level | F9 (Compact Errors) | Low | Codify in Skills Engine platform specs as standard agent behavior. Below Intent's altitude but worth standardizing. |
| G5 | **Stateful vs. stateless tension** not explicitly resolved | F12 (Stateless Reducer) | Low | Document the resolution: system is stateful (knowledge base + signals), individual agent invocations are stateless within their context window. The context resolver is the bridge. |

### Areas Where Intent Goes Deeper Than 12-Factor

| Area | Intent Concept | 12-Factor Gap |
|------|---------------|---------------|
| **Trust-gated autonomy** | 5-level trust model with scored execution gates | 12-factor has no concept of earned autonomy or trust scoring |
| **Multi-agent orchestration** | Skill graph, intent-orchestrator, parallel pipeline | 12-factor addresses single-agent design only |
| **Knowledge compilation** | DDR-001, Knowledge Engine, federation model | 12-factor's "context engineering" is per-invocation; Intent's is permanent |
| **Cross-engagement governance** | Federation (inherit down, promote up, never leak sideways), confidentiality tiers | 12-factor has no multi-tenant or access control model |
| **Signal amplification** | Time-decayed scoring, co-reference clustering, emergent signal clusters | 12-factor doesn't address how signals gain or lose importance over time |
| **Persona-driven prompts** | 189-entity persona system composing into skill renderings | 12-factor says "own your prompts" but doesn't address voice, perspective, or persona as prompt dimensions |
| **Double-loop learning** | Observe → Knowledge feedback (Argyris) | 12-factor is single-loop: errors feed back into current context, not into a permanent knowledge base |

---

## Architectural Interpretation

The 12-factor model and Intent framework are **complementary, not competitive.** They map to different layers of the same system:

```
┌─────────────────────────────────────────────┐
│  Intent Framework (Operating Model)          │
│  Notice → Spec → Execute → Observe           │
│  Trust model, signal system, knowledge base   │
├─────────────────────────────────────────────┤
│  12-Factor Agents (Agent Implementation)      │
│  Context engineering, control flow, tools      │
│  Pause/resume, error handling, human contact   │
├─────────────────────────────────────────────┤
│  LLM APIs (Infrastructure)                    │
│  Token management, model selection, streaming  │
└─────────────────────────────────────────────┘
```

The 12-factor principles should inform how **Skills Engine platform renderers** build individual agent runs. Each platform spec (claude-code, copilot, system-prompts) could codify:
- Factor 3/13: Context resolver pre-fetches compiled knowledge
- Factor 5: Agent invocations receive unified state from context resolver
- Factor 6: Skills support pause/resume via signal emission
- Factor 8: Platform-specific control flow (retry, judge, escalate)
- Factor 9: Standard error-to-context-to-retry behavior
- Factor 10: Skills remain small; orchestrator composes

The 5 identified gaps (G1-G5) represent genuine additions to Intent's surface area, with G1 (pause/resume) and G2 (human contact as capability) being the most architecturally significant.

---

## Recommended Actions

1. **G1 — Pause/Resume:** Add `PAUSE` and `RESUME` event types to the event catalog. Define checkpoint serialization in SPEC-003. Priority: high (Fieldbook pipeline needs this).
2. **G2 — Human Contact as Tool:** Create a `request_human_input` signal type. Distinguish from trust-gated approval. Let agents decide WHEN to ask, not just WHETHER they're allowed. Priority: high (outer-loop agent pattern is powerful).
3. **G3 — LLM-as-Judge:** Add an `evaluate` operation to the Observe phase. Define observation contracts with LLM-scored acceptance criteria. Priority: medium.
4. **G4 — Error Pattern:** Codify retry-escalate behavior in Skills Engine platform specs. Not an Intent-level change. Priority: low.
5. **G5 — State Model Documentation:** Add a "State Philosophy" section to ARCHITECTURE.md clarifying the stateful-system / stateless-invocation resolution. Priority: low.
