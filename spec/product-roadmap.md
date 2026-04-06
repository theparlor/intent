---
title: Product Roadmap
type: framework
maturity: final
confidentiality: shareable
reusability: universal
domains:
  - consulting-operations
topics:
  - product-strategy
created: 2026-03-31
technologies:
  - slack
depth_score: 5
depth_signals:
  file_size_kb: 19.3
  content_chars: 18258
  entity_count: 1
  slide_count: 0
  sheet_count: 0
  topic_count: 2
  has_summary: 0
vocab_density: 0.11
related_entities:
  - {pair: consulting-operations ↔ subaru, count: 795, strength: 0.427}
  - {pair: consulting-operations ↔ automotive-manufacturing, count: 770, strength: 0.416}
  - {pair: consulting-operations ↔ engagement-management, count: 498, strength: 0.269}
  - {pair: consulting-operations ↔ turnberry, count: 448, strength: 0.224}
  - {pair: consulting-operations ↔ foot-locker, count: 251, strength: 0.136}
---
# Intent Product Roadmap

> Four products, one value stream. Each phase of the Intent loop is a product with its own maturity, users, and investment needs.

## The Framing

Intent isn't one product — it's four. Each phase of the loop (Notice → Spec → Execute → Observe) serves different users at different moments, has different maturity levels today, and needs different kinds of investment to grow. Treating them as a single monolith hides where we're strong and where we're starving.

Think of it like a manufacturing line. If the Notice station is capturing signals at high volume but the Spec station can't process them into actionable specs, the whole line backs up. The roadmap has to invest in the constraint, not just the loudest station.

```
┌──────────┐    ┌──────────┐    ┌──────────┐    ┌──────────┐
│  NOTICE  │ →  │   SPEC   │ →  │ EXECUTE  │ →  │ OBSERVE  │
│    △◇    │    │   △◇○    │    │   △◉     │    │   ◇○     │
│  capture │    │  shape   │    │  build   │    │  learn   │
└──────────┘    └──────────┘    └──────────┘    └──────────┘
     ↑                                              │
     └──────────────────────────────────────────────┘
```

Persona key: △ Practitioner-Architect · ◇ Product-Minded Leader · ○ Design-Quality Advocate · ◉ AI Agent

---

## Product 1: Notice

**What it does:** Captures observations — patterns, friction, insights, hunches — from wherever practitioners work, and lands them as structured signals in `.intent/signals/`.

**Primary users:** △ Practitioner-Architect (captures signals while building), ◇ Product-Minded Leader (reviews signal clusters for intent candidates)

### Current State

| Asset | Status | Location |
|-------|--------|----------|
| Signal schema | ✅ Defined | `.intent/templates/signal.md` |
| CLI capture tool | ✅ Built | `bin/intent-signal` |
| MCP servers (notice, spec, observe) | ✅ Built (in-memory) | `servers/notice.py`, `servers/spec.py`, `servers/observe.py` |
| GitHub Action (event emission) | ✅ Built | `.github/workflows/intent-events.yml` |
| Quickstart guide | ✅ Written | `docs/quickstart.md` |
| Signal capture architecture | ✅ Specced | `spec/signal-capture-system.md` |
| 24 active signals (SIG-001–024) | ✅ Captured | `.intent/signals/` |
| Slack integration | ⬜ Specced, not built | Tier 3 in capture spec |
| GitHub native capture | ⬜ Specced, not built | Tier 4 in capture spec |
| ChatGPT / Copilot / Codex plugins | ⬜ Specced, not built | Tier 5 in capture spec |
| Signal clustering / pattern detection | ⬜ Not started | — |
| Signal-to-intent promotion flow | ⬜ Not started | — |

### Maturity: **Operational**
The Notice product can be installed and used on a real repo today. A practitioner can capture signals from Claude Code, Cowork, Cursor, or the terminal. Events are emitted on push. What's missing is breadth (more capture surfaces) and intelligence (pattern detection, clustering, promotion suggestions).

### Next Investments

**Enhance (improve what exists):**
- Signal deduplication — detect when the same observation is captured from multiple surfaces
- Confidence scoring enrichment — automated scoring based on signal frequency, source diversity, and recency
- Signal review workflow — weekly digest of unclustered signals, suggested groupings

**Build (create what's missing):**
- Slack bot — reaction-based capture (`:signal:` emoji → PR with signal file)
- GitHub issue/PR label capture — `/signal` comment or `signal` label → signal file
- Signal-to-intent promotion — when 3+ signals cluster around a theme, suggest creating an intent

**Learn (validate assumptions):**
- Do practitioners actually capture signals in the flow of work, or do they batch them later?
- What's the signal-to-noise ratio? How many captured signals actually lead to intents?
- Which capture surfaces generate the highest-quality signals?

---

## Product 2: Spec

**What it does:** Transforms clustered signals into actionable specifications that AI agents can execute against. The shaping layer between "we noticed something" and "build this."

**Primary users:** △ Practitioner-Architect (writes specs), ◇ Product-Minded Leader (prioritizes which intents get specced), ○ Design-Quality Advocate (ensures specs meet quality bar)

### Current State

| Asset | Status | Location |
|-------|--------|----------|
| Work ontology (7 levels) | ✅ Defined | `spec/work-ontology.md` |
| Intent template | ✅ Built | `.intent/templates/intent.md` |
| Spec template | ✅ Built | `.intent/templates/spec.md` |
| Contract template | ✅ Built | `.intent/templates/contract.md` |
| All 13 work unit templates | ✅ Built | `.intent/templates/` (signal, intent, spec, contract, atom, cluster, product, team, decision, digest, event, arb-review, config) |
| `intent-spec` CLI tool | ✅ Built | `bin/intent-spec` |
| MCP spec tools | ✅ Built (in-memory) | `servers/spec.py` (create_spec, create_contract, verify_contract, assess_agent_readiness, list_specs) |
| Cross-functional shaping workflow | ✅ Conceptual (flow diagram) | `spec/flow-diagram.md` |
| Spec validation tooling | ⬜ Not started | — |
| Spec-to-agent handoff format | ⬜ Not started | — |

### Maturity: **Tooled**
The Spec product has templates, a CLI tool, and MCP server tooling. A practitioner can create intents, specs, and contracts from the terminal or Claude Code. What's missing is *validation* (is this spec agent-ready?) and a *structured handoff format* that agents can consume directly without human translation.

### Next Investments

**Enhance (improve what exists):**
- Codify the shaping flow into a checklist or interactive workflow — not just a diagram
- Define "spec completeness" criteria — what makes a spec agent-ready vs. human-ready

**Build (create what's missing):**
- Intent template (`.intent/templates/intent.md`) — frontmatter schema for proposed intents with status lifecycle: `proposed → accepted → specced → executing → complete`
- Spec template (`.intent/templates/spec.md`) — structured format that agents can parse: problem, constraints, acceptance criteria, contracts, test scenarios
- Contract template (`.intent/templates/contract.md`) — interface definitions that specs reference and agents implement against
- `intent-spec` CLI tool — create specs from the terminal, link to parent intents
- MCP tools: `intent_create_spec`, `intent_validate_spec` — spec creation and completeness checking from Claude Code / Cursor

**Learn (validate assumptions):**
- Is the 7-level ontology the right abstraction, or do teams need fewer levels?
- What's the minimum spec that an AI agent can execute against? Where's the line between "too vague" and "over-specified"?
- Does cross-functional shaping actually happen, or does the architect write specs solo?

---

## Product 3: Execute

**What it does:** The phase where AI agents (and humans) implement against specs. Intent is deliberately thin here — the agents bring their own capabilities. Execute's job is to ensure specs flow to agents and execution events flow back to Observe.

**Primary users:** △ Practitioner-Architect (orchestrates agents, reviews output), ◉ AI Agent (implements against specs)

### Current State

| Asset | Status | Location |
|-------|--------|----------|
| Event schema for execution events | ✅ Defined | `spec/event-catalog.md` |
| Trace propagation (trace_id through event chain) | ✅ Task-specced | `tasks/trace-propagation.md` |
| Entire.io agent trace capture | ✅ Configured | `.entire/settings.json` + `.entire/logs/` |
| Agent definitions (6 subagents) | ✅ Defined | `servers/AGENT_DEFINITIONS.md` |
| Spec-to-agent handoff | ⬜ Not started | — |
| Contract verification (pre/post execution) | ⬜ Not started | — |

### Maturity: **Defined + Instrumented**
Execute has the event types, trace propagation is task-specced with explicit code diffs, and Entire.io already captures agent reasoning alongside commits across all 4 repos. The CLAUDE.md agent handoff protocol functions as a de facto spec-to-agent handoff — agents read CLAUDE.md → read task specs → execute. What's missing is *formalization* of that handoff and *contract verification* tooling that checks outcomes against specs.

### Next Investments

**Enhance (improve what exists):**
- Refine execution event schema — what events do we actually need from agents? Start with the minimum: `execution.started`, `execution.completed`, `contract.verified`, `contract.failed`

**Build (create what's missing):**
- Agent trace adapter — a lightweight hook that agents can call to emit execution events to `events.jsonl`
- Contract verification tool — given a spec with contracts, check whether the implementation satisfies them (could be as simple as "run these tests")
- Entire.io integration — Brien already has Entire capturing agent reasoning alongside commits. Bridge that into Intent's event stream.

**Learn (validate assumptions):**
- How much execution observability do teams actually want? Full traces? Just start/stop? Only failures?
- Do agents need to *read* Intent specs natively, or is a human always translating?
- What's the right boundary between Intent's observability and tools like Entire.io that already instrument agent execution?

---

## Product 4: Observe

**What it does:** Makes the Intent event stream visible — dashboards, digests, pattern detection, feedback loops. The learning layer that closes the loop back to Notice.

**Primary users:** ◇ Product-Minded Leader (reads dashboards, identifies trends), ○ Design-Quality Advocate (monitors spec-to-outcome quality)

### Current State

| Asset | Status | Location |
|-------|--------|----------|
| Event schema (OTel-compatible) | ✅ Defined | `spec/event-catalog.md` |
| Event log format (JSONL) | ✅ Defined | `.intent/events/events.jsonl` (50 events) |
| 15 cataloged event types | ✅ Defined | `spec/event-catalog.md` |
| GitHub Action event emission | ✅ Built | `.github/workflows/intent-events.yml` |
| Observability stack spec (27KB) | ✅ Specced | `spec/observability-stack.md` |
| OTel Collector config | ✅ Built | `observe/otel-collector-config.yaml` |
| File tail adapter | ✅ Task-specced | `tasks/file-tail-adapter.md` |
| Grafana dashboard definition | ✅ Task-specced | `tasks/grafana-dashboard.md` |
| MCP observe server | ✅ Built (in-memory) | `servers/observe.py` (ingest_event, detect_spec_delta, detect_trust_drift, system_health, suggest_signals_from_events) |
| Signal clustering view | ⬜ Not started | — |
| Spec-to-outcome traceability | ⬜ Not started | — |
| Weekly digest / report | ⬜ Not started | — |
| Metrics (velocity, signal-to-spec ratio, etc.) | ⬜ Not started | — |

### Maturity: **Specced + Partially Built**
Observe has the richest specification surface of any product — a 27KB observability stack spec, OTel Collector config, file tail adapter design, Grafana dashboard definition, and a working (in-memory) MCP server with health and drift detection. What blocks it from becoming operational is the trace propagation chain (trace_id must be real before the file tail adapter can export meaningful spans to Grafana). The infrastructure is designed; it needs wiring.

### Next Investments

**Enhance (improve what exists):**
- Validate event schema against real data — are the 15 event types the right set? Which ones actually fire in practice?
- JSONL → queryable format — even a simple script that parses events.jsonl into a summary

**Build (create what's missing):**
- Intent dashboard (HTML, ships in `docs/`) — visualize the event stream: signal volume over time, signals by source, intent status lifecycle, spec completion rates
- Weekly digest generator — CLI or scheduled action that reads events.jsonl and produces a summary: new signals, intent movements, specs completed, contracts verified/failed
- Signal clustering view — group signals by related_intents or by keyword similarity, show which clusters are growing
- Spec-to-outcome trace — given a spec, show the chain: intent → spec → contracts → execution events → outcome

**Learn (validate assumptions):**
- What do leaders actually want to see? Signal volume? Spec throughput? Time-from-signal-to-shipped?
- Is JSONL sufficient for the event store, or does this need a real database at team scale?
- Does the Observe product generate new signals (closing the loop), or is it purely a reporting layer?

---

## Cross-Cutting Investments

Some work doesn't belong to a single product — it benefits the whole value stream.

**Repo scaffold installer** — one command that adds `.intent/` to any existing repo with all templates, directories, and optionally the MCP config and GitHub Action. Currently specced but not built as a single script.

**Marketing/docs site** — `theparlor/intent-site` is live at `theparlor.github.io/intent/` with 23 pages across three pillars (The Story, The System, The Build). Site has its own governance docs and roadmap at `../intent-site/tasks/ROADMAP.md`.

**Versioning and release process** — VERSION file (`2026.03.29-0.6.0`) and CHANGELOG exist.

**CLAUDE.md continuity** — Updated March 30 with four-product framing, agent handoff protocol, MCP server docs, and priority of work referencing site roadmap.

---

## Investment Priority (Autonomous / Needs-Learning / Blocked)

### Autonomous — Can execute now, well-specced, non-destructive

These items have specs, task files, or enough signal density to move without human input. Ordered by dependency chain.

1. **Trace propagation** — Wire trace_id through models.py and all 3 MCP servers. Task spec: `tasks/trace-propagation.md`. Dependency: none. Unlocks: everything below.
2. **File tail adapter** — Build the JSONL-to-OTLP bridge. Task spec: `tasks/file-tail-adapter.md`. Dependency: trace propagation. Unlocks: Grafana dashboard.
3. **Grafana dashboard** — Deploy dashboard JSON to Grafana Cloud free tier. Task spec: `tasks/grafana-dashboard.md`. Dependency: file tail adapter + OTel Collector running.
4. **Signal cluster reconciliation** — The 24 signals self-organize into 6 clusters. Emit cluster files to `.intent/` using the cluster template. Dependency: none. Source: signal analysis below.
5. **Product roadmap self-reconciliation** — THIS UPDATE. Reconcile stale claims against actual repo state. Dependency: none.
6. **TASKS.md refresh** — Retire completed items, add newly-specced work, update date. Dependency: this roadmap update.

### Needs-Learning — Direction is clear, but requires validation or human voice

These items need Brien's judgment, external input, or practitioner evidence. They generate disambiguation signals.

7. **Intent Manifesto** — Sharp, opinionated, shareable. Requires Brien's voice and conviction. No spec can substitute for that.
8. **Practitioner interviews (Ari + 4 others)** — External validation of H1-H5. Can't be delegated to agents.
9. **Vocabulary decision (SIG-019)** — "Notice" and "Execute" aren't landing. Candidate replacements exist but this is a naming decision that cascades everywhere.
10. **Signal ID strategy (SIG-022/023)** — Sequential IDs collide in distributed environments. UUID v7, ULID, namespaced, composite, or hierarchical? Architecture decision with long-tail consequences.
11. **Case Study #1** — Brien's own methodology documented. Requires introspection + narrative craft.

### Blocked — Cannot proceed without prerequisite work

12. **Spec-to-agent handoff format** — Depends on vocabulary decision (#9) and at least one spec validation pass.
13. **Signal intelligence (clustering, promotion)** — Depends on signal ID strategy (#10) and trace propagation (#1).
14. **Metrics framework** — Depends on Grafana dashboard (#3) being live with real data flowing through it.

---

## Signal Cluster Analysis (as of 2026-03-30)

The 24 signals self-organize into 6 clusters. This is the input to autonomous signal processing.

### Cluster 1: Infrastructure (SIG-016, 018, 021, 024)
**Theme:** MCP servers exist, deployment options identified, Cowork→Claude Code routing established.
**Status:** Actionable. Servers built, hosting options researched, deployment topology specced.
**Next autonomous action:** Deploy notice.py to FastMCP Cloud as walking skeleton.

### Cluster 2: Observability (SIG-002, 017)
**Theme:** OTel is the right model, deployment is a spectrum not a binary.
**Status:** Fully specced. 27KB observability-stack.md + 3 task specs + OTel config.
**Next autonomous action:** Execute trace-propagation task spec.

### Cluster 3: Signal Capture & Processing (SIG-003, 008, 011, 015)
**Theme:** Multi-surface capture, signal amplification through reference frequency.
**Status:** Notice product operational. Amplification specced but not built.
**Next autonomous action:** Add `referenced_by` field to signal schema.

### Cluster 4: Schemas & Identity (SIG-001, 005, 022, 023)
**Theme:** Work units need formal schemas; signal IDs need distributed-safe strategy.
**Status:** Templates built (13 types). ID strategy needs architecture decision.
**Next autonomous action:** None — blocked on ID strategy decision (SIG-022).

### Cluster 5: Methodology & Adoption (SIG-006, 007, 009, 010, 019, 020)
**Theme:** Founding observations, four-product thesis, vocabulary friction, site IA.
**Status:** Site IA resolved (23 pages, three pillars). Vocabulary friction unresolved.
**Next autonomous action:** None — blocked on vocabulary decision (SIG-019).

### Cluster 6: Autonomous Operations (SIG-012, 013, 014)
**Theme:** Trust-based execution levels, always-on processing, context drift mitigation.
**Status:** Trust framework specced (L0-L4). Deployment topology specced.
**Next autonomous action:** Signal enrichment pipeline that computes trust scores on new signals.

---

## How to Read This Roadmap

This isn't a Gantt chart or a sprint plan. It's a **current-state assessment** of four products, a **signal cluster analysis**, and a **directional investment guide** partitioned by autonomy level — not by time. Items in "Autonomous" can be picked up by agents immediately. Items in "Needs-Learning" generate disambiguation signals when they surface. Items in "Blocked" state their prerequisites explicitly.

The roadmap itself is a living document. As signals come in and intents form, priorities will shift. That's the loop working.

*Last reconciled: 2026-03-30*
