---
title: Claude
type: framework
maturity: final
confidentiality: shareable
reusability: universal
domains:
  - consulting-operations
created: 2026-03-31
technologies:
  - slack
thought_leaders:
  - marty-cagan
  - jeff-patton
  - teresa-torres
  - josh-seiden
depth_score: 6
depth_signals:
  file_size_kb: 24.1
  content_chars: 19143
  entity_count: 5
  slide_count: 0
  sheet_count: 0
  topic_count: 1
  has_summary: 0
vocab_density: 0.42
related_entities:
  - {pair: consulting-operations ↔ subaru, count: 791, strength: 0.426}
  - {pair: consulting-operations ↔ automotive-manufacturing, count: 769, strength: 0.416}
  - {pair: consulting-operations ↔ engagement-management, count: 498, strength: 0.269}
  - {pair: consulting-operations ↔ turnberry, count: 448, strength: 0.224}
  - {pair: consulting-operations ↔ foot-locker, count: 251, strength: 0.136}
---
# Intent — Development Continuity Guide

> This file exists so that any AI agent or human contributor can pick up Intent development without prior session context. Read this first.

## ⚠ CRITICAL: This Repo Contains Two Products

**Read this first. This is the most common source of session drift.**

This repo contains **two distinct products** that share a repo but have different purposes, different users, and different development paths:

### 1. Intent (Methodology)
An operating model for AI-augmented product teams. **Notice → Spec → Execute → Observe.** Domain-agnostic. Replaces Agile ceremony overhead. Lives in: `spec/`, `.intent/`, `bin/`, `servers/`.

### 2. Knowledge Engine (Product)
A compiled knowledge base system: `raw/` sources → agent-compiled `knowledge/` artifacts → ingest/query/lint operations. Separable from Intent — can be used without the loop. Lives in: `knowledge-engine/` (AGENTS.md, specs, templates).

### 3. Knowledge Farm (Instance — not in this repo)
A specific deployment of the Knowledge Engine for a domain. Brien's Knowledge Farm is his consulting practice first-brain (Subaru, ASA, F&G engagements). It spans `Core/` and `Work/Consulting/Engagements/*/`. Brien's farm feeds Intent ONLY because his domain (product strategy) overlaps with Intent's domain — **this is coincidental, not structural.**

### How to tell which product you're working on

| If you're touching... | You're in... |
|----------------------|-------------|
| The loop, trust scoring, work ontology, signals, intents | **Intent** (methodology) |
| AGENTS.md, ingest/query/lint, federation, enrichment, redaction | **Knowledge Engine** (product) |
| Subaru/ASA/F&G engagement data, Brien's engagement knowledge | **Brien's Knowledge Farm** (instance) |

### Decided Architecture (2026-04-06)

| Decision | Choice |
|----------|--------|
| Knowledge Engine MCP server | New `intent-knowledge` server (port 8004), separate from notice/spec/observe |
| Knowledge Engine CLI | New `intent-knowledge` tool (subcommands: ingest, query, lint) |
| Retroactive enrichment trigger | Suggested-first (lint detects opportunity, surfaces signal), on-demand second |
| Engagement rollout order | Subaru → F&G → ASA → Cargill → Footlocker |
| Redaction enforcement | Tool-level (MCP server applies projection automatically) |

---

## What Is Intent?

Intent is a **team operating model for AI-augmented product teams**. It replaces Agile's ceremony-driven coordination with a continuous loop: **Notice → Spec → Execute → Observe**. When AI collapses implementation from weeks to hours, the bottleneck moves upstream — from delivery to discovery, specification, and observation. Intent is the operating model for that new reality.

Intent is NOT a SaaS tool (yet). It's a methodology that lives in files, tracked in git, observable through events. Teams adopt it by adding a `.intent/` directory to their repos.

### Three-Layer Architecture (v1.0 — 2026-04-05)

Intent's methodology prescribes three layers that work together:

| Layer | Purpose | Directories | Analogy |
|-------|---------|-------------|---------|
| **1. Compiled Knowledge Base** | Everything the system knows about the problem domain | `raw/`, `knowledge/` | The Knowledge Engine product provides this |
| **2. Transformation OS** | The notice→spec→execute→observe engine. Domain-agnostic. | `.intent/`, `spec/` (methodology) | Intent methodology |
| **3. Software Spec & Code** | Specs, contracts, and running code | `spec/` (generated), `src/` | The output |

**Six bidirectional data flows couple the layers:**
1. Knowledge → Notice: Lint surfaces signals (gaps, contradictions, staleness)
2. Notice → Spec (via knowledge): Spec authoring queries knowledge base for personas, journeys, DDRs
3. Spec → Execute: Trust-gated agents build against specs
4. Execute → Observe: Running code emits events
5. **Observe → Knowledge (double-loop):** Observations update domain models — questioning assumptions, not just optimizing
6. Observe → Spec corpus (single-loop): Spec drift detection, living doc sync

**Knowledge Engine schema:** `knowledge-engine/AGENTS.md`
**Knowledge Engine specs:** `knowledge-engine/spec/` (operations, federation, enrichment, redaction, boundary)
**Research archive:** `reference/karpathy-synthesis/`

**Owner:** Brien (theparlorhq@gmail.com) — solo practitioner, The Parlor
**Repo:** github.com/theparlor/intent (private)
**Site repo:** github.com/theparlor/intent-site → https://theparlor.github.io/intent-site/
**Status:** Methodology defined, CLI suite + MCP server operational, signal dashboard live, trust framework specced, signal management CLI operational (review/dismiss/cluster/promote). All 13 founding signals scored with trust levels.

## Core Concepts

### The Loop
```
NOTICE  →  SPEC  →  EXECUTE  →  OBSERVE  →  (back to NOTICE)
```
No sprint boundaries. No ceremony tax. A continuous loop where the team's energy follows the highest-leverage work.

### Four Products
Intent is four products, not one. Each phase of the loop is a product with its own maturity:
- **Notice** (Operational) — Signal capture from any surface. MCP server, CLI, GitHub Action built.
- **Spec** (Conceptual) — Shaping signals into agent-ready specs. Templates, CLI tools built.
- **Execute** (Defined) — Agent implementation against specs. Event schema defined, no integration yet.
- **Observe** (Schema-Ready) — Dashboard and learning layer. 15 event types defined, no visualization yet.

See `spec/product-roadmap.md` for the full four-product roadmap with investments.

### Work Ontology (7 levels)
Signal → Intent → Spec → Contract → Capability → Feature → Product

Each level has a clear owner, clear transitions, and clear events. This replaces stories, epics, and backlogs.

### Four Personas
- **△ Practitioner-Architect** (amber) — Senior ICs, system thinkers. Primary: Notice, Spec.
- **◇ Product-Minded Leader** (blue) — PMs, business context. Primary: Notice, Observe.
- **○ Design-Quality Advocate** (purple) — Designers/QA, contract quality. Primary: Spec, Observe.
- **◉ AI Agent** (green) — Claude Code, GitHub Actions, Entire.io. Primary: Execute, Observe.

### Event System
15 OTel-compatible events across 6 emission mechanisms. Events stored in `.intent/events/events.jsonl`. Schema: version, event, timestamp, trace_id (=Intent), span_id (=work unit), parent_id (=hierarchy), source, data.

### Three-Layer Repo Pattern (Extended)
- `raw/` — Immutable source material (research, analytics, competitors, support). LLM reads, never writes.
- `knowledge/` — LLM-compiled domain knowledge (personas, journeys, DDRs, themes, domain models, rationale). Agent writes, human reviews.
- `.intent/` — Work artifacts (signals, intents, specs, contracts, decisions, events, templates)
- `observations/` — Runtime feedback (metrics, incidents) that feeds back into knowledge base and specs
- `.claude/` — Agent reasoning (project context, session transcripts)
- `.entire/` — Observability (execution traces from Entire.io)

### Signal Capture System
A 5-tier adapter architecture for capturing signals from every surface where practitioners work:
1. **MCP Server** (Tier 1) — Claude Code, Cowork, Cursor. 7 tools: signal capture/list/get, intent propose, spec create, status.
2. **CLI** (Tier 2) — `bin/intent-signal`, `bin/intent-intent`, `bin/intent-spec`, `bin/intent-status`. Full suite.
3. **Slack** (Tier 3) — Reaction-based or slash command. Specced, not built.
4. **GitHub** (Tier 4) — Issue labels, PR comments. Specced, not built.
5. **AI Plugins** (Tier 5) — ChatGPT, Copilot, Codex. Specced, not built.

See `spec/signal-capture-system.md` for the full architecture.

### Signal Trust & Autonomous Execution

Signals are not just captured — they are enriched, scored, classified, and routed through an autonomous processing pipeline. The goal: work every signal as far along as it can go, with humans intervening only when something is unsafe or too ambiguous.

**Trust Model:** Every signal gets two scores:
- **Confidence** (0-1): How likely is this signal real and worth acting on?
- **Trust** (0-1): How confidently can an agent resolve this without human input?

Trust = clarity × 0.30 + (1/blast_radius) × 0.20 + reversibility × 0.20 + testability × 0.20 + precedent × 0.10

**Autonomy Levels:**
- L0 (trust < 0.2): Human drives — strategic, ambiguous
- L1 (0.2–0.4): Agent assists — enriches, human decides
- L2 (0.4–0.6): Agent decides, human approves — drafts intent+spec
- L3 (0.6–0.85): Agent executes, human monitors — full loop, observe after
- L4 (≥ 0.85): Full autonomy — circuit breakers only

**Enrichment Pipeline:** Source Adapter → Dedup Agent → Context Agent → Trust Scorer → Classifier → Router

**Disambiguation Loop:** When an agent hits ambiguity, it generates a new signal asking a better question. The system never dead-ends.

See `spec/signal-trust-framework.md` for the full architecture.

### Deployment Topology

Intent supports a config-driven deployment model. The same tools work in two modes:

**Local mode:** `.intent/` in git is the source of truth. CLI tools read/write files. MCP server reads/writes files. Signal dashboard reads from git. Best for solo practitioners and teams that want full git control.

**Hosted mode (planned):** A service is the source of truth. CLI and MCP become API clients. Dashboard reads from the service. `.intent/` in git becomes an optional sync target. Required for always-on agent processing (Brien's laptop goes offline during travel).

Configuration lives in `.intent/config.yml` (schema in `spec/signal-trust-framework.md`). The same CLI commands, MCP tools, and dashboard work in both modes — only the backend changes.

The processing pipeline (enrichment agents, routing, execution) must run somewhere always-on. Options under evaluation: GitHub Actions (simplest), cloud service (most capable), dedicated machine (interim).

## CLI Suite

All CLI tools share the same architecture: walk up from `$PWD` to find `.intent/`, generate sequential IDs, write markdown with YAML frontmatter, emit events to `events.jsonl`, optional `--commit` flag.

### intent-signal
```bash
# Capture
intent-signal "What you noticed"                    # Capture a signal
intent-signal "Title" --confidence 0.8 --trust 0.6  # With scores (auto-computes autonomy level)
intent-signal "Title" --source pr-review             # With source attribution

# Triage
intent-signal review                                 # Show all signals awaiting triage
intent-signal review SIG-003                         # Review a specific signal

# Lifecycle
intent-signal dismiss SIG-003 --reason "Duplicate"   # Dismiss a signal
intent-signal cluster SIG-001,SIG-003 --name "Group" # Group related signals
intent-signal promote SIG-003                        # Promote signal → intent

# Query
intent-signal list                                   # List active signals
intent-signal list --status captured                 # Filter by status
intent-signal list --all                             # Include dismissed
intent-signal show SIG-003                           # Show full signal file
```

### intent-intent
```bash
intent-intent "What needs to change"                          # Propose an intent
intent-intent "Title" --signals SIG-006,SIG-008 --priority now # Link to signals
intent-intent list                                            # List all intents
intent-intent show INT-003                                    # Show details
intent-intent accept INT-003                                  # Accept for shaping
```

### intent-spec
```bash
intent-spec "What to build" --intent INT-003    # Create a spec linked to intent
intent-spec list                                # List all specs
intent-spec show SPEC-001                       # Show details
intent-spec approve SPEC-001                    # Move to approved
```

### intent-status
```bash
intent-status              # Full overview: counts + pipeline
intent-status signals      # Signal table (ID, Source, Conf, Title)
intent-status intents      # Intent pipeline with status breakdown
intent-status specs        # Spec pipeline with status breakdown
intent-status events       # Last 15 events from events.jsonl
intent-status roadmap      # ASCII four-product maturity view
```

## MCP Server (7 tools)

The MCP server at `tools/intent-mcp/server.py` provides 7 tools accessible from Claude Code, Cowork, and Cursor:

| Tool | Action | Read-only |
|------|--------|-----------|
| `intent_capture_signal` | Capture a signal | No |
| `intent_list_signals` | List recent signals | Yes |
| `intent_get_signal` | Get signal details | Yes |
| `intent_propose_intent` | Propose an intent | No |
| `intent_create_spec` | Create a spec | No |
| `intent_status` | System status overview | Yes |

Install: `pip install mcp pydantic` then configure in Claude Code or Cursor settings.

## Repo Structure

```
intent/
├── raw/                      ← LAYER 1 INPUT: Immutable source material
│   ├── research/             ← Interview transcripts, surveys
│   ├── analytics/            ← Exported reports, dashboards
│   ├── competitors/          ← Market research
│   └── support/              ← Ticket exports, session recordings
├── knowledge/                ← LAYER 1 OUTPUT: LLM-compiled domain knowledge
│   ├── _index.md             ← Master catalog (LLM-maintained, read first)
│   ├── log.md                ← Append-only activity log
│   ├── traceability.md       ← Cross-artifact link matrix
│   ├── personas/             ← PER-NNN files
│   ├── journeys/             ← JRN-NNN files
│   ├── decisions/            ← DDR-NNN design decision records
│   ├── themes/               ← THM-NNN research themes
│   ├── domain-models/        ← DOM-NNN bounded contexts, glossaries
│   └── design-rationale/     ← RAT-NNN why-level documentation
├── .intent/                  ← LAYER 2: Intent's own dogfood
│   ├── INTENT.md             ← Project manifest
│   ├── decisions.md          ← Decision log (source of truth)
│   ├── signals/              ← 24+ signals (SIG-001 through SIG-025+)
│   ├── intents/              ← Proposed intents
│   ├── specs/                ← Written specs
│   ├── clusters/             ← 6 signal clusters
│   ├── events/               ← Event log (events.jsonl)
│   └── templates/            ← Signal, intent, spec, contract (knowledge artifact templates moved to knowledge-engine/templates/)
├── observations/             ← RUNTIME FEEDBACK (feeds Flows 5 & 6)
│   ├── metrics/              ← Performance, usage, behavioral data
│   └── incidents/            ← Error reports, anomalies
├── .github/
│   └── workflows/
│       └── intent-events.yml ← GitHub Action: emit events on push
├── artifacts/                ← React JSX interactive artifacts
├── bin/                      ← CLI tools (add to PATH)
│   ├── intent-signal         ← Capture signals
│   ├── intent-intent         ← Propose/manage intents
│   ├── intent-spec           ← Create/manage specs
│   └── intent-status         ← System status dashboard
├── spec/                     ← Methodology source files (source of truth)
├── servers/                  ← MCP servers (notice, spec, observe)
├── tools/
│   └── intent-mcp/           ← MCP server (7 tools)
├── reference/                ← Reference materials
│   └── karpathy-synthesis/   ← Three-layer architecture research & decisions
├── notice/                   ← Loop directory: notice phase
├── execute/                  ← Loop directory: execute phase
├── observe/                  ← Loop directory: observe phase
├── knowledge-engine/         ← Knowledge Engine product (AGENTS.md, specs, templates)
├── CLAUDE.md                 ← THIS FILE
├── CHANGELOG.md              ← Timestamp-based version history
├── VERSION                   ← Current: 2026.03.30-0.9.0
├── README.md                 ← Public-facing repo README
└── TASKS.md                  ← Living task list
```

## Design System

### Persona Colors
- Architect (△): `#f59e0b` (amber)
- PM (◇): `#3b82f6` (blue)
- Design/QA (○): `#8b5cf6` (purple)
- Agent (◉): `#10b981` (green)

> For the full site design system (slate palette, CSS strategy, IA), see `theparlor/intent-site`.

### Marketing & Documentation Site

The site has been moved to its own repo: **`theparlor/intent-site`**
- Live at: https://theparlor.github.io/intent-site/
- Three-pillar IA: The Story, The System, The Build
- All site governance (IA spec, contracts, content map) lives in that repo
- See `content-map.md` in the site repo for how site claims trace back to specs here

## How to Continue Development

### Adding a new CLI tool
1. Create the script in `bin/` — follow the existing pattern:
   - `find_intent_root()` to locate `.intent/`
   - Sequential ID generation (`PREFIX-XXX`)
   - Markdown with YAML frontmatter output
   - Event emission to `events.jsonl`
   - Optional `--commit` flag
2. Add corresponding MCP tool in `tools/intent-mcp/server.py` with Pydantic input model
3. Update this file's CLI section
4. Update `docs/roadmap.html` CLI grid if relevant

### Editing existing content
1. Edit the markdown source in `spec/` — this is the source of truth
2. If the content affects the site, note it — the site repo (`theparlor/intent-site`) has a `content-map.md` that traces site claims back to specs here

### Versioning
- Edit `VERSION` with new version string: `YYYY.MM.DD-MAJOR.MINOR.PATCH`
- Add entry to top of `CHANGELOG.md`
- Major = breaking change to ontology/schema/pattern. Minor = new capability/scope. Patch = fix/clarify.

### Site
The marketing site lives in `theparlor/intent-site` and deploys to https://theparlor.github.io/intent-site/. This repo has no `docs/` folder.

## Traceability Chain

Every link is bidirectional and navigable through `[[wikilinks]]` and YAML frontmatter:

```
Raw Research → Persona → Journey Step → Pain Point → DDR → Spec → Contract → Code
                                                                              ↓
Observations ← ← ← ← ← ← ← ← ← ← ← ← ← ← ← ← ← ← ← ← ← ← ← ← ← ← ←
  ↓                         (Flow 6: single-loop → spec updates)
  └→ Knowledge Base updates  (Flow 5: double-loop → assumption questioning)
```

Lint enforces coverage: every persona must be referenced by at least one journey, every DDR must link to a persona and journey stage, every spec must link to a DDR, orphans are flagged.

## Key Decisions (for context)

1. **Named "Intent"** — not "Dev OS", Frame, Premise, or Lucid. The name IS the thing.
2. **Methodology first, tool second** — validate with practitioners before building software.
3. **Open development** — signals, decisions, architecture all public. Dogfood the observe layer.
4. **File-native, git-tracked, OTel-compatible** — no lock-in, no proprietary formats.
5. **Target practitioner-architects first** — senior ICs who feel the gap and have org influence.
6. **Specs as contracts, not stories** — agents need verifiable assertions, not prose.
7. **Staged GTM** — thought leadership → methodology product → tooling (conditional).
8. **Four-product framing** — Notice, Spec, Execute, Observe are distinct products with own roadmaps.
9. **Three-layer architecture** — Compiled knowledge base (Karpathy pattern) + Transformation OS (Intent loop) + Software Spec/Code. Independent layers, bidirectionally coupled. (2026-04-05)
10. **Compilation over retrieval** — The knowledge base compiles understanding once and keeps it current. Not RAG. Cross-references already there. Contradictions already flagged.
11. **Double-loop learning** — Observe updates Layer 1 (domain understanding), not just Layer 3 (execution). Without this, system can only optimize, never question. (Argyris)
12. **Origin tracking** — Every knowledge artifact carries `origin: human | agent | synthetic` for contamination mitigation. (Ango)
13. **Federated knowledge base architecture** — Core = universal substrate, engagements = bounded instances. Inherit down, promote up, never leak sideways. Mirrors Workspaces topology. (2026-04-05)
14. **Two products, not one** — Intent (methodology) and Knowledge Engine (product) are distinct. KE is separable — can be used without Intent. Brien's Knowledge Farm is an instance. The domain overlap is coincidental. (2026-04-06, DDR-005)
15. **Engagement rollout order** — Subaru → F&G → ASA → Cargill → Footlocker. Subaru first (most data, highest learning). (2026-04-06)
16. **Knowledge Engine as new MCP server** — `intent-knowledge` on port 8004 with CLI `intent-knowledge` (ingest/query/lint subcommands). Not bolted onto intent-notice. (2026-04-06)
17. **Retroactive enrichment = suggested** — Lint detects recompilation opportunities, surfaces as signals. On-demand execution. Not automatic cascades. (2026-04-06)
18. **Redaction at tool level** — MCP server applies confidentiality projection automatically based on engagement context. Not a flag Brien has to remember. (2026-04-06)

## Intellectual Foundations

Intent draws from: Marty Cagan (product operating model), Jeff Patton (story mapping → spec mapping), Teresa Torres (continuous discovery → continuous observation), Josh Seiden (outcomes over outputs), OpenTelemetry (observability conventions). Primary empirical evidence: Brien's conversation with engineer Ari, whose team independently discovered the Intent pattern.

## What's Not Yet Done

- [x] ~~GitHub Pages enabled~~ — live at https://theparlor.github.io/intent/ (2026-03-29)
- [x] ~~Signal management dashboard~~ — signals.html with lifecycle, clustering, trust levels (2026-03-29)
- [x] ~~Signal trust framework spec~~ — spec/signal-trust-framework.md (2026-03-29)
- [x] ~~Add trust/autonomy_level/status fields to signal schema and template~~ (2026-03-29, v0.6.0)
- [x] ~~Signal management CLI commands: review, dismiss, cluster, promote~~ (2026-03-29, v0.6.0)
- [ ] Trust scoring agent (first enrichment agent)
- [ ] .intent/config.yml schema for builder-configurable thresholds
- [ ] Install MCP server on Brien's repos and validate end-to-end signal capture
- [ ] Install .intent/ scaffolds into Brien's 4 repos
- [ ] Intent dashboard v1 (Observe product)
- [ ] Slack signal capture bot (Notice product, Tier 3)
- [ ] Spec validation CLI — check completeness against criteria
- [ ] Hosted deployment mode — always-on processing for travel/multi-machine
- [ ] Multi-machine file sync via GitHub for library organizational skills
- [ ] 5 in-depth interviews with teams experiencing AI + Agile friction
- [ ] Message to Ari about Intent (draft exists)

## Agent Handoff Protocol

Intent is designed to be developed by AI agents (Claude Code) working from this file.

### Before Starting ANY Task

1. **Read these files first, IN THIS ORDER:**
   - `CLAUDE.md` (this file) — project context, architecture, tooling
   - `knowledge-engine/AGENTS.md` — compiled knowledge base schema, operations, cross-reference conventions
   - `tasks/ROADMAP.md` — **master execution plan with phase status, verification scripts, and contracts**
   - `TASKS.md` — living backlog partitioned by autonomy level
   - Any relevant spec in `spec/` for the domain you're working in

2. **Follow the ROADMAP.** It tells you which phase is current, what to execute next, and how to verify. Do NOT skip phases. Do NOT parallelize across phases (except Phase 4, which is explicitly parallelizable).

3. **Load context before acting.** Read all referenced specs upfront. Do not start modifying files until you understand the full picture.

### Execution Model

**Parallelize aggressively.** When a task involves multiple independent files or pages, use subagents to work on them concurrently. For example:
- Updating nav on 18 pages → spawn subagents per page or per pillar group
- Running contract checks → run all 10 contracts in parallel
- Building independent page sections → parallelize section creation

**Seek permissions and context upfront.** Don't discover mid-task that you need a file you haven't read. Front-load all reads, then execute.

**Verify before AND after.** Run relevant contracts from `site-contracts.md` before starting (to know the baseline state) and after finishing (to verify nothing broke). Diff the before/after contract results.

### Verification

Before committing, verify your changes don't break existing functionality:
- CLI tools: run `intent-status` to confirm the tool suite works
- Signal files: validate YAML frontmatter format
- Event log: check `events.jsonl` for valid JSON lines

**If something breaks:** Fix before committing. If fixing requires a design decision, generate a disambiguation signal.

### Signal Generation from Conversations
Brien may generate signals from Cowork sessions, Claude desktop app (iOS/web/desktop), or regular chat. These signals will be formatted as `.intent/signals/` files and committed to the repo. Claude Code agents should monitor for new signals and begin processing them through the enrichment pipeline.

### When Stuck
**Generate a disambiguation signal** — don't dead-end. Capture what's ambiguous as a new signal for Brien to review. Write it to `.intent/signals/` with `status: blocked` and `trust: 0.1`.

### Priority of Work
1. **Site roadmap** — read `../intent-site/tasks/ROADMAP.md` for the master execution plan. It has phased work with verification scripts. Execute the current phase before moving to product repo tasks.
2. Task specs in `docs/tasks/` — explicit handoffs from Cowork
3. Contract violations — fix any failing contracts
4. Signals with trust ≥ 0.6 that can be auto-executed (L3/L4)
5. Signals that need enrichment (add context, compute trust)
6. Specs that are approved and ready for execution
7. Infrastructure work (tooling, pipeline, config)
