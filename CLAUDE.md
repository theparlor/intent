# Intent — Development Continuity Guide

> This file exists so that any AI agent or human contributor can pick up Intent development without prior session context. Read this first.

## What Is Intent?

Intent is a **team operating model for AI-augmented product teams**. It replaces Agile's ceremony-driven coordination with a continuous loop: **Notice → Spec → Execute → Observe**. When AI collapses implementation from weeks to hours, the bottleneck moves upstream — from delivery to discovery, specification, and observation. Intent is the operating model for that new reality.

Intent is NOT a SaaS tool (yet). It's a methodology that lives in files, tracked in git, observable through events. Teams adopt it by adding a `.intent/` directory to their repos.

**Owner:** Brien (theparlorhq@gmail.com) — solo practitioner, The Parlor
**Repo:** github.com/theparlor/intent (private)
**Status:** Methodology defined, bootstrap kit built, CLI suite operational, validating with real repos.

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

### Three-Layer Repo Pattern
- `.intent/` — Work artifacts (signals, intents, specs, contracts, decisions, events, templates)
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

## CLI Suite

All CLI tools share the same architecture: walk up from `$PWD` to find `.intent/`, generate sequential IDs, write markdown with YAML frontmatter, emit events to `events.jsonl`, optional `--commit` flag.

### intent-signal
```bash
intent-signal "What you noticed"           # Capture a signal
intent-signal "Title" --confidence 0.8     # With confidence score
intent-signal "Title" --source pr-review   # With source attribution
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
├── .intent/                  ← Intent's own dogfood
│   ├── INTENT.md             ← Project manifest
│   ├── decisions.md          ← Decision log (source of truth)
│   ├── signals/              ← 11 founding signals (SIG-001 through SIG-011)
│   ├── intents/              ← Proposed intents
│   ├── specs/                ← Written specs
│   ├── events/               ← Event log (events.jsonl)
│   └── templates/            ← Signal, intent, spec, contract templates
├── .github/
│   └── workflows/
│       └── intent-events.yml ← GitHub Action: emit events on push
├── artifacts/                ← React JSX interactive artifacts
│   ├── intent-event-catalog.jsx
│   ├── intent-flow-diagram.jsx
│   ├── intent-product-roadmap.jsx  ← Interactive roadmap (Products/Priorities views)
│   ├── intent-work-system.jsx
│   └── intent-visual-brief.jsx
├── bin/                      ← CLI tools (add to PATH)
│   ├── intent-signal         ← Capture signals
│   ├── intent-intent         ← Propose/manage intents
│   ├── intent-spec           ← Create/manage specs
│   └── intent-status         ← System status dashboard
├── docs/                     ← GitHub Pages site (source: main, /docs)
│   ├── index.html            ← Product landing page
│   ├── methodology.html
│   ├── concept-brief.html
│   ├── signals.html
│   ├── decisions.html
│   ├── roadmap.html          ← Four-product roadmap page
│   ├── event-catalog.html
│   ├── flow-diagram.html
│   ├── work-system.html
│   ├── native-repos.html
│   ├── visual-brief.html
│   ├── quickstart.md         ← 5-minute getting started guide
│   └── visual-brief-app/     ← Vite-built React app
├── spec/                     ← Markdown source files (source of truth)
│   ├── intent-methodology.md
│   ├── intent-concept-brief.md
│   ├── autonomous-operations-design.md
│   ├── signal-capture-system.md  ← 5-tier capture architecture
│   ├── product-roadmap.md       ← Four-product roadmap
│   ├── signal-stream.md
│   ├── decision-log.md
│   ├── event-catalog.md
│   ├── flow-diagram.md
│   ├── repo-pattern.md
│   └── work-ontology.md
├── tools/
│   └── intent-mcp/           ← MCP server (7 tools)
│       ├── server.py
│       ├── requirements.txt
│       └── README.md
├── notice/                   ← Loop directory: notice phase
├── execute/                  ← Loop directory: execute phase
├── observe/                  ← Loop directory: observe phase
├── reference/                ← Reference materials
├── CLAUDE.md                 ← THIS FILE
├── CHANGELOG.md              ← Timestamp-based version history
├── VERSION                   ← Current: 2026.03.29-0.4.0
├── README.md                 ← Public-facing repo README
└── TASKS.md                  ← Living task list
```

## Design System

### Unified Slate Palette
All site pages and artifacts use this palette:
- Background: `#0f172a`
- Surface: `#1e293b`
- Border: `#334155`
- Text: `#f1f5f9`
- Muted text: `#94a3b8`
- Dim text: `#64748b`
- Accent blue: `#3b82f6`

### Persona Colors
- Architect (△): `#f59e0b` (amber)
- PM (◇): `#3b82f6` (blue)
- Design/QA (○): `#8b5cf6` (purple)
- Agent (◉): `#10b981` (green)

### Site Nav Pattern
Every page in `docs/` has this nav:
```html
<nav class="site-nav">
  <a href="index.html" class="logo"><span>I</span>ntent</a>
  <a href="index.html">Home</a>
  <a href="methodology.html">Methodology</a>
  <a href="concept-brief.html">Concept Brief</a>
  <a href="signals.html">Signals</a>
  <a href="decisions.html">Decisions</a>
  <a href="roadmap.html">Roadmap</a>
</nav>
```
The current page gets `class="active"`. Max-width: 900px. Footer with source link to GitHub.

### Site Information Architecture
The index page follows five sections that mirror the loop:
1. **Understand** (blue) — 4 feature cards: Visual Brief, Methodology, Concept Brief, Work Ontology
2. **The Shift** (amber) — 6 from/to cards showing what changes
3. **Implement** (green) — 3 cards: Repo Pattern, Event Catalog, Flow Diagram
4. **Open Development** (purple) — 2 cards: Signal Stream, Decision Log
5. **Engage** (pink) — 3 persona columns + GitHub CTA

## How to Continue Development

### Adding a new page
1. Write the markdown source in `spec/` — this is the source of truth
2. Create the HTML rendering in `docs/` — match the existing nav, palette, and typography
3. If it's a primary nav item, add it to the nav in ALL pages
4. If it has an interactive artifact, create the JSX in `artifacts/`
5. Link from `docs/index.html` in the appropriate section
6. Update CHANGELOG.md

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
1. Edit the markdown source in `spec/` first
2. Then update the HTML in `docs/` to match
3. For methodology and concept-brief, the HTML is a full rendering of the markdown

### Pushing changes
The sandbox environment cannot `git commit` directly (no git config). Use the GitHub MCP tool `push_files` to push:
```
mcp__github__push_files(owner: "theparlor", repo: "intent", branch: "main", files: [...], message: "...")
```

### Versioning
- Edit `VERSION` with new version string: `YYYY.MM.DD-MAJOR.MINOR.PATCH`
- Add entry to top of `CHANGELOG.md`
- Major = breaking change to ontology/schema/pattern. Minor = new capability/scope. Patch = fix/clarify.

### GitHub Pages
Brien needs to enable GitHub Pages: Settings → Pages → Source: Deploy from branch → Branch: main, /docs. NOT YET ENABLED as of 2026-03-29.

## Key Decisions (for context)

1. **Named "Intent"** — not "Dev OS", Frame, Premise, or Lucid. The name IS the thing.
2. **Methodology first, tool second** — validate with practitioners before building software.
3. **Open development** — signals, decisions, architecture all public. Dogfood the observe layer.
4. **File-native, git-tracked, OTel-compatible** — no lock-in, no proprietary formats.
5. **Target practitioner-architects first** — senior ICs who feel the gap and have org influence.
6. **Specs as contracts, not stories** — agents need verifiable assertions, not prose.
7. **Staged GTM** — thought leadership → methodology product → tooling (conditional).
8. **Four-product framing** — Notice, Spec, Execute, Observe are distinct products with own roadmaps.

## Intellectual Foundations

Intent draws from: Marty Cagan (product operating model), Jeff Patton (story mapping → spec mapping), Teresa Torres (continuous discovery → continuous observation), Josh Seiden (outcomes over outputs), OpenTelemetry (observability conventions). Primary empirical evidence: Brien's conversation with engineer Ari, whose team independently discovered the Intent pattern.

## What's Not Yet Done

- [ ] GitHub Pages not yet enabled by Brien
- [ ] Install MCP server on Brien's repos and validate end-to-end signal capture
- [ ] Install .intent/ scaffolds into Brien's 4 repos
- [ ] Intent dashboard v1 (Observe product)
- [ ] Slack signal capture bot (Notice product, Tier 3)
- [ ] Spec validation CLI — check completeness against criteria
- [ ] 5 in-depth interviews with teams experiencing AI + Agile friction
- [ ] Message to Ari about Intent (draft exists)
- [ ] Deeper positioning and vision work
