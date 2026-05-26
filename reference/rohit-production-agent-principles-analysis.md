---
title: Rohit's 10 Production Agent Principles — Full Analysis and Intent Framework Mapping
type: reference
frameworks:
  - double-loop-learning
depth_score: 4
depth_signals:
  file_size_kb: 12.1
  content_chars: 11794
  entity_count: 1
  slide_count: 0
  sheet_count: 0
  topic_count: 0
  has_summary: 0
vocab_density: 0.25
source: Rohit @rohit4verse, 'How to Build a Production-Grade AI Agent' (X/Twitter, Feb 14 2026)
source_url: "https://x.com/rohit4verse/status/2022709729450201391"
analyzed: 2026-04-12
analyst: Brien + Claude (Cowork session)
relevance: high — validates Intent architecture, surfaces specific implementation gaps
---
# Rohit's 10 Production Agent Principles — Full Analysis

> Source: Rohit @rohit4verse, "How to Build a Production-Grade AI Agent" (Feb 14, 2026)
> Context: Brien shared this article during a Cowork session focused on persona enrichment, Knowledge Engine architecture, and Cowork plugin design. The article's 10 principles were mapped against Intent's three-layer architecture and the work Brien is building.

## The Article's Core Thesis

Over 40% of agentic AI projects fail — not because of the models, but due to inadequate risk controls, poor architecture, and unclear business value. Chatbots passively generate text. Agents actively execute actions. That architectural difference introduces massive material risk. The article outlines 10 engineering principles that separate production-grade agent systems from fragile demos.

---

## Principle-by-Principle Mapping to Intent

### Principle 1: Define the Agent Boundary and Threat Model

**Rohit's argument:** The core vulnerability is the confused deputy problem. Agents have elevated permissions (API keys, DB access). Teams must map every API connection, tool invocation, and data access point before deployment. Prompt injection appears in 73% of production deployments. Defense must exist entirely outside the LLM reasoning loop.

**Intent mapping:** Maps to the Notice phase. Intent's trust scoring (clarity × 0.30 + blast_radius × 0.20 + reversibility × 0.20 + testability × 0.20 + precedent × 0.10) IS a threat model — it evaluates every signal before the system acts on it. The L0-L4 autonomy levels ARE the boundary definition: what the agent can do alone vs. what requires human approval.

**Gap:** Intent's threat model is conceptual (trust scores). Rohit's is operational (map every API connection, document attack vectors). The MCP server implementations need an explicit attack surface document before deployment.

### Principle 2: Contracts Everywhere — Inputs, Outputs, Tool Schemas

**Rohit's argument:** Strictly typed schemas with Pydantic/Zod. Server-side validation. Structured error responses so the LLM can self-correct and retry. Idempotency keys. Versioned schemas. "The LLM does not actually understand your API, it simply pattern matches."

**Intent mapping:** Maps to the Spec phase. Intent's contracts (CON-NNN artifacts) are verifiable assertions — same concept, different layer. But Intent's MCP tool schemas lack the operational rigor Rohit describes.

**Gap:** See SIG-031. Intent MCP servers need structured error payloads, idempotency keys for write operations, and schema versioning.

### Principle 3: Secure Tool Execution — Authentication, RBAC, Sandboxing

**Rohit's argument:** Principle of least privilege everywhere. Short-lived certificates. Zero trust architecture. Human-in-the-loop approval registry for high-impact operations.

**Intent mapping:** Maps to the Execute phase. Intent's trust levels map to Rohit's approval registry:
- L0 (< 0.2): Human drives = Rohit's "requires human approval"
- L1 (0.2-0.4): Agent suggests = Rohit's "verify before registration"
- L2 (0.4-0.6): Agent proposes, human approves = Rohit's "RBAC check at execution"
- L3 (0.6-0.85): Agent executes, human monitors = Rohit's "sandboxed execution"
- L4 (≥ 0.85): Full autonomy = Rohit's "circuit breakers only"

**Gap:** Intent has the model but not the enforcement mechanism. Rohit describes the engineering (certificates, HSMs, mutual TLS). Intent needs to decide which enforcement layer to use — potentially HumanLayer (Dex Horthy's product), which directly implements approval workflows.

### Principle 4: Context Engineering — Layered and Compact

**Rohit's argument:** Don't dump raw conversation history. Use intent detectors to decide when to retrieve memory. Summarize retrieved snippets. Target 10:1 compression ratios. Track what context was retrieved, why, and how it influenced decisions.

**Intent mapping:** THIS IS THE KNOWLEDGE ENGINE'S CORE VALUE PROPOSITION. Intent's "compilation over retrieval" principle is exactly Rohit's "summarize and inject compact summaries." The Knowledge Engine compiles understanding once and keeps it current — it doesn't do RAG. The compiled artifacts (personas, journeys, DDRs) ARE the 10:1 compressed context.

**Alignment:** Near-perfect. Intent already made this architectural decision. Rohit provides the engineering justification and the specific benchmark (10:1 compression, 40-50% overhead if you don't compress).

**New insight:** Rohit's "auditability" requirement — tracking context provenance — maps to Intent's traceability chain (raw → knowledge → spec → contract → code). The traceability chain IS context provenance.

### Principle 5: Knowledge Grounding as a Governed Tool

**Rohit's argument:** Treat retrieval as governed software. Hard tenant isolation at the data layer. Source governance (approved internal docs, verified external, blocked domains). Lineage tracking. Separate retrieval from execution — reading should never grant write access.

**Intent mapping:** Maps directly to the Knowledge Engine's federation model. Core = universal substrate, engagements = bounded instances. Intent's DDR on redaction at tool level = Rohit's "security trimming at retrieval time."

**Gap:** See SIG-032. Rohit's model is more granular — field-level classification (public/internal/confidential/restricted) vs. Intent's artifact-level federation boundaries.

### Principle 6: Planning and Orchestration as Control Flow

**Rohit's argument:** State machines for compliance-critical flows. React patterns for dynamic tasks (with explicit stop conditions). Planning-based orchestration with manager agents delegating to specialized sub-agents. Circuit breakers to prevent runaway costs.

**Intent mapping:** The Notice → Spec → Execute → Observe loop IS a state machine. The orchestrator (the loop itself) controls workflow state. The agent (Claude, in Brien's case) determines actions within constrained options. The disambiguation signal pattern IS Rohit's "stop condition" — when stuck, generate a signal asking a better question rather than looping.

**Alignment:** Strong. Intent's loop was designed as an orchestration pattern before Rohit described the engineering requirements for one.

### Principle 7: Memory and State as Architecture

**Rohit's argument:** Separate working memory (session-scoped, Redis) from long-term memory (vector DB, relational, time-series). Data classification matrix. Encryption at rest and in transit. Re-verify permissions on every read/write.

**Intent mapping:** Maps to the Knowledge Engine's three-layer architecture:
- Layer 1 (Compiled Knowledge Base) = Rohit's long-term memory
- Layer 2 (Transformation OS) = Rohit's working memory (current loop state)
- Layer 3 (Software Spec & Code) = Rohit's execution output

Intent's `.intent/events/events.jsonl` = Rohit's time-series store for event sequences.

**Gap:** Intent doesn't currently separate these as different storage tiers. Everything is in markdown files on disk. For production deployment (the hosted Knowledge Farm), this needs the storage architecture Rohit describes.

### Principle 8: Reliability Mechanics — Errors, Retries, Completion

**Rohit's argument:** Exponential backoff with jitter. Circuit breakers (10 errors in 60 seconds = open circuit). Graceful degradation (fall back to smaller models, keyword search). Checkpointing for mid-execution recovery. Explicit completion conditions.

**Intent mapping:** See SIG-033. The persona enrichment pipeline discovered the need for checkpointing empirically. Rohit provides the engineering pattern. The "write to disk after every batch" approach IS checkpointing — but it's a prompt instruction, not a mechanical enforcement.

**Key quote:** "Define incredibly explicit completion conditions: task explicitly completed, maximum iterations reached, timeouts exceeded, or unrecoverable error." This is exactly what the persona retrieval tasks lacked — they reported "done" at structural completeness rather than at exhaustive depth.

### Principle 9: Observability — Traces, Metrics, Logs with OpenTelemetry

**Rohit's argument:** OTel as vendor-neutral framework. Generative AI semantic conventions. Distributed tracing (root span → child spans for LLM calls, tool invocations, RAG retrieval, sub-agent handoffs). Financial cost tracking per session. Memory and workflow state as first-class observability citizens.

**Intent mapping:** This IS the Observe phase. Intent's event system uses OTel-compatible events. The trace identity model (Intent = Trace, Spec = Span, Contract = Leaf Span) is exactly Rohit's root-span → child-span hierarchy. Intent's Grafana dashboard spec tracks the same panels.

**Alignment:** Near-perfect. Intent was designed with this exact stack in mind. Rohit provides the production engineering details (context propagation across network boundaries, cost tagging, state as observability citizen).

### Principle 10: Evaluations and Governance — Regression, Drift, Safety Gates

**Rohit's argument:** Offline evaluation, regression testing, online monitoring. Golden datasets. LLM-as-judge (85% alignment with human experts when configured properly). PII protection. Safety filters. Audit trails. Drift monitoring (behavior changes despite unchanged code).

**Intent mapping:** Maps to the Observe → Notice feedback loop. Intent's "double-loop learning" (observe updates domain understanding, not just execution) IS drift monitoring at the methodology level. The signal trust decay (7-day half-life) IS a mechanism for detecting when signals are becoming stale.

**Gap:** Intent doesn't currently have automated evaluation pipelines or golden datasets. For production deployment, the Knowledge Engine needs regression tests (did recompilation change the personas in unexpected ways?) and drift detection (is the system's understanding of a domain drifting from reality?).

---

## Summary: What Intent Should Adopt

### Immediately applicable:
1. **Structured error payloads** in MCP server tool responses (Principle 2)
2. **Explicit completion conditions** encoded as code, not prompt instructions (Principle 8)
3. **Data classification matrix** at field level in knowledge artifact schema (Principle 5/7)

### For production deployment (hosted Knowledge Farm):
4. **Bearer token + mutual TLS** for the hosted MCP server (Principle 3)
5. **Storage tier separation** — fast store for working memory, durable store for compiled knowledge (Principle 7)
6. **Cost tracking** per session/query against the Knowledge Farm (Principle 9)

### For the Cowork plugin:
7. **Human-in-the-loop approval registry** mapping to L0-L2 trust levels (Principle 3)
8. **Circuit breakers** for dispatch tasks that are running away on cost (Principle 8)

### Validates existing design (no change needed):
9. Compilation over retrieval = context compression (Principle 4)
10. Federation boundaries = tenant isolation (Principle 5)
11. Notice→Spec→Execute→Observe = state machine orchestration (Principle 6)
12. OTel-compatible event system = production observability (Principle 9)
13. Trust decay + double-loop learning = drift monitoring (Principle 10)

---

## Cross-References

- **Dex Horthy's 12 Factor Agents** — complementary framework focused on coding agents specifically. Rohit is broader (enterprise agents). Both validate Intent's architecture.
- **Dex Horthy's context engineering** — Rohit's Principle 4 cites the same 40% overhead finding.
- **HumanLayer** — Dex's product directly implements Rohit's Principle 3 (approval workflows).
- **Intent signals generated:** SIG-031 (contract rigor), SIG-032 (data classification), SIG-033 (checkpointing), SIG-034 (architectural validation).
