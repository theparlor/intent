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
| MCP server (Claude Code, Cowork, Cursor) | ✅ Built | `tools/intent-mcp/server.py` |
| GitHub Action (event emission) | ✅ Built | `.github/workflows/intent-events.yml` |
| Quickstart guide | ✅ Written | `docs/quickstart.md` |
| Signal capture architecture | ✅ Specced | `spec/signal-capture-system.md` |
| 11 founding signals | ✅ Captured | `.intent/signals/` |
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
| Intent template | ⬜ Not built | — |
| Spec template | ⬜ Not built | — |
| Contract template | ⬜ Not built | — |
| Spec validation tooling | ⬜ Not started | — |
| Cross-functional shaping workflow | ✅ Conceptual (flow diagram) | `spec/flow-diagram.md` |
| Spec-to-agent handoff format | ⬜ Not started | — |

### Maturity: **Conceptual**
The Spec product has strong methodology (the ontology, the shaping flow, the persona model) but zero tooling. A practitioner who reads the docs understands *what* a good spec looks like, but there's no template to start from, no validation to check if a spec is agent-ready, and no structured handoff format that an AI agent can consume.

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
| Agent trace capture | ⬜ Not started | — |
| Spec-to-agent handoff | ⬜ Not started | — |
| Contract verification (pre/post execution) | ⬜ Not started | — |
| Execution observability | ⬜ Not started | — |

### Maturity: **Defined**
Execute has the event types defined (contract.verified, agent-trace events) but no actual integration with any agent system. This is intentional — Intent doesn't want to *be* the execution engine. But it does need to know that execution happened, that contracts were checked, and that work output can be traced back to the spec that authorized it.

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
| Event log format (JSONL) | ✅ Defined | `.intent/events/events.jsonl` |
| 15 cataloged event types | ✅ Defined | `spec/event-catalog.md` |
| GitHub Action event emission | ✅ Built | `.github/workflows/intent-events.yml` |
| Dashboard | ⬜ Not started | — |
| Signal clustering view | ⬜ Not started | — |
| Spec-to-outcome traceability | ⬜ Not started | — |
| Weekly digest / report | ⬜ Not started | — |
| Metrics (velocity, signal-to-spec ratio, etc.) | ⬜ Not started | — |

### Maturity: **Schema-Ready**
Observe has the best-defined schema of any product (OTel-compatible events, 15 event types, 6 emission mechanisms) but zero visualization. Events land in a JSONL file that nobody reads. The system is observable in theory but opaque in practice.

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

**GitHub Pages site** — the docs site at `docs/` needs Pages enabled. Brien hasn't flipped the switch yet. Once live, it becomes the canonical reference for the methodology and the starting point for adoption.

**Versioning and release process** — VERSION file and CHANGELOG exist. The next release (0.3.0) captures the bootstrap kit, signal capture system, and four-product roadmap.

**CLAUDE.md continuity** — the continuity guide needs updating with the bootstrap kit, four-product framing, and signal capture system.

---

## Investment Priority (Now / Next / Later)

### Now (this week)
1. **Validate Notice works end-to-end** — Install MCP server on Brien's repos, capture real signals from real work, verify events land in events.jsonl
2. **Build Spec templates** — Intent, Spec, and Contract templates so the Spec product has its first tooling
3. **Enable GitHub Pages** — flip the switch, make the site live

### Next (this month)
4. **Intent dashboard v1** — HTML page in `docs/` that reads events.jsonl and shows signal volume, sources, intent status
5. **Slack signal capture** — reaction-based bot, covers team conversation surface
6. **Spec validation** — CLI tool that checks spec completeness against defined criteria

### Later (after validation)
7. **AI tool plugins** — ChatGPT, Copilot, Codex adapters for signal capture
8. **Agent trace integration** — bridge Entire.io and agent execution into the event stream
9. **Signal intelligence** — automated clustering, pattern detection, promotion suggestions
10. **Metrics framework** — define the Intent-native metrics (signal-to-spec ratio, time-to-shipped, spec quality score)

---

## How to Read This Roadmap

This isn't a Gantt chart or a sprint plan. It's a **current-state assessment** of four products and a **directional investment guide** for where to put energy next. The "Now" items are chosen because they're the constraint — Notice is operational but unvalidated, Spec has no tooling, Observe has no visualization. Execute is intentionally deferred because the agents already work; Intent's job is to make sure they work against good specs.

The roadmap itself is a living document. As signals come in and intents form, priorities will shift. That's the loop working.
