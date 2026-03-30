# Intent — Development Continuity Guide

> This file exists so that any AI agent or human contributor can pick up Intent development without prior session context. Read this first.

## What Is Intent?

Intent is a **team operating model for AI-augmented product teams**. It replaces Agile's ceremony-driven coordination with a continuous loop: **Notice → Spec → Execute → Observe**. When AI collapses implementation from weeks to hours, the bottleneck moves upstream — from delivery to discovery, specification, and observation. Intent is the operating model for that new reality.

Intent is NOT a SaaS tool (yet). It's a methodology that lives in files, tracked in git, observable through events. Teams adopt it by adding a `.intent/` directory to their repos.

**Owner:** Brien (theparlorhq@gmail.com) — solo practitioner, The Parlor
**Repo:** github.com/theparlor/intent (private)
**Site:** https://theparlor.github.io/intent/
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
├── .intent/                  ← Intent's own dogfood
│   ├── INTENT.md             ← Project manifest
│   ├── decisions.md          ← Decision log (source of truth)
│   ├── signals/              ← 13 founding signals (SIG-001 through SIG-013)
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
├── docs/                     ← GitHub Pages site: https://theparlor.github.io/intent/
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
│   ├── signal-trust-framework.md   ← Trust scoring, autonomy levels, enrichment pipeline
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
├── VERSION                   ← Current: 2026.03.29-0.6.0
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
- Accent amber: `#f59e0b`
- Accent green: `#10b981`
- Accent purple: `#a855f7`
- Accent red: `#dc2626`

### Persona Colors
- Architect (△): `#f59e0b` (amber)
- PM (◇): `#3b82f6` (blue)
- Design/QA (○): `#8b5cf6` (purple)
- Agent (◉): `#10b981` (green)

### Site Information Architecture (IA v2 — Three Pillars)

**IMPORTANT: Read `docs/site-ia.md` for the full IA specification. This section is the summary.**

The site is organized into three pillars. The primary nav has exactly 3 links (plus logo). Each pillar has a hero page and depth pages with a sub-nav.

#### Primary Nav (ALL pages)
```html
<nav class="site-nav">
  <a href="index.html" class="logo"><span>I</span>ntent</a>
  <a href="pitch.html">The Story</a>
  <a href="work-system.html">The System</a>
  <a href="architecture.html">The Build</a>
</nav>
```
One pillar link gets `class="active"` based on which pillar the current page belongs to.

#### Pillar 1 — The Story (pitch.html is hero)
Pages: pitch.html, concept-brief.html, methodology.html, roadmap.html
Primary nav active: "The Story"
```html
<nav class="sub-nav">
  <a href="pitch.html">Overview</a>
  <a href="concept-brief.html">Concept Brief</a>
  <a href="methodology.html">Methodology</a>
  <a href="roadmap.html">Roadmap</a>
</nav>
```

#### Pillar 2 — The System (work-system.html is hero)
Pages: work-system.html, flow-diagram.html, schemas.html, signals.html, dogfood.html, event-catalog.html
Primary nav active: "The System"
```html
<nav class="sub-nav">
  <a href="work-system.html">Overview</a>
  <a href="flow-diagram.html">Flow</a>
  <a href="schemas.html">Schemas</a>
  <a href="signals.html">Signals</a>
  <a href="dogfood.html">Dogfood</a>
  <a href="event-catalog.html">Events</a>
</nav>
```

#### Pillar 3 — The Build (architecture.html is hero)
Pages: architecture.html, agents.html, deployment.html, arb.html, decisions.html, native-repos.html
Primary nav active: "The Build"
```html
<nav class="sub-nav">
  <a href="architecture.html">Overview</a>
  <a href="agents.html">Agents</a>
  <a href="deployment.html">Deployment</a>
  <a href="arb.html">ARB</a>
  <a href="decisions.html">Decisions</a>
  <a href="native-repos.html">Repos</a>
</nav>
```

#### Index Page
**The pitch IS the home page.** `index.html` contains a meta redirect to `pitch.html`. The logo always links to `index.html`. See `docs/site-ia.md` for the redirect HTML.

#### Visual Brief
`visual-brief.html` is NOT a nav destination. It's a CTA link on the pitch page.

Max-width: 900px. Footer with source link to GitHub. All shared CSS lives in `docs/styles.css` — page-specific CSS stays in small inline `<style>` blocks.

### CSS Strategy — CRITICAL RULES

**All pages link `styles.css` for shared foundation (nav, palette, typography, footer, grid, cards) AND keep page-specific CSS in inline `<style>` blocks.**

**Light pages** (methodology, concept-brief, decisions, event-catalog, schemas, flow-diagram, visual-brief)
Small or no `<style>` block. Most styling comes from styles.css.

**Rich pages** (pitch, dogfood, arb, roadmap, signals, architecture, agents, deployment, index, work-system, native-repos)
Extensive `<style>` blocks with page-specific visual components (scroll animations, SVG diagrams, tab interfaces, timelines, stat grids, agent cards, etc.). **Never strip or reduce inline `<style>` blocks from these pages.** The page-specific CSS IS the page's value.

### Content Preservation Rules

1. **Never reduce a page's file size by more than 20%** without explicit human approval. A dramatic size reduction means content loss.
2. **Never replace a page with a skeleton/placeholder.** If a page has interactive content (tabs, diagrams, grids, timelines), that content must be preserved.
3. **Visual components are content.** Tech radar grids, SVG loop diagrams, comparison strips, timeline visualizations, stat box layouts — these are not decoration. They are the page's value.
4. **When resolving merge conflicts on HTML files, prefer the LARGER version.** The smaller version is almost certainly content-stripped.

### Footer (ALL pages)
```html
<footer>
  <p>Source: <a href="https://github.com/theparlor/intent">github.com/theparlor/intent</a> &middot; Built with the Intent methodology</p>
</footer>
```
Footer may be wrapped in `<div class="container">` on content pages.

### Site Contracts and Spec
See `docs/site-spec.md` for the canonical page inventory with CSS strategy, nav tier, file size baselines, and status.
See `docs/site-contracts.md` for verifiable assertions. **Run contract checks after ANY change to docs/.**

### Site IA Implementation Notes
The site uses a three-pillar IA (see "Site Information Architecture" above). The pitch page replaces the old index as the primary landing experience. See `docs/site-ia.md` for the full specification, `docs/site-contracts.md` for verifiable assertions, and `docs/site-spec.md` for the page inventory.

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
GitHub Pages is **live** at https://theparlor.github.io/intent/. Source: main branch, /docs folder. Enabled 2026-03-29.

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

1. **Read these files first, every time:**
   - `CLAUDE.md` (this file) — project context, design system, CSS rules
   - `docs/site-ia.md` — three-pillar IA structure, nav templates, page assignments
   - `docs/site-spec.md` — canonical page inventory, file size baselines, visual components
   - `docs/site-contracts.md` — verifiable assertions (run after ANY change)
   - Any task-specific spec in `docs/tasks/` if referenced

2. **Load context before acting.** Read all referenced specs upfront. Do not start modifying files until you understand the full picture. Misunderstanding the CSS strategy or nav structure causes cascading damage.

3. **Check `docs/tasks/` for pending task specs.** These are handoff instructions from Cowork (the architect surface). Each task spec includes requirements, verification checks, and commit instructions.

### Execution Model

**Parallelize aggressively.** When a task involves multiple independent files or pages, use subagents to work on them concurrently. For example:
- Updating nav on 18 pages → spawn subagents per page or per pillar group
- Running contract checks → run all 10 contracts in parallel
- Building independent page sections → parallelize section creation

**Seek permissions and context upfront.** Don't discover mid-task that you need a file you haven't read. Front-load all reads, then execute.

**Verify before AND after.** Run relevant contracts from `site-contracts.md` before starting (to know the baseline state) and after finishing (to verify nothing broke). Diff the before/after contract results.

### Verification Checklist (run after EVERY change to docs/)

```bash
cd ~/Workspaces/Core/frameworks/intent/docs

# Quick smoke test — run these at minimum
for f in *.html; do
  SIZE=$(wc -c < "$f")
  echo "$SIZE $f"
done | sort -rn

# Then run full contracts from site-contracts.md
# CON-SITE-001 through CON-SITE-010
```

**If a contract fails:** Fix the failure before committing. Do not commit with known contract violations. If fixing requires a design decision, stop and generate a disambiguation signal.

### Linting and Cleanup

When touching HTML files, also check for:
- **Inconsistent indentation** — use 2-space indent for HTML, match surrounding code
- **Missing alt text on images** — add descriptive alt attributes
- **Unclosed tags** — validate HTML structure
- **Orphaned CSS** — if a visual component is removed, remove its CSS too
- **Stale content** — if a page references a spec file, verify the spec still exists and content matches

### Content Freshness

The site makes claims about the product (trust formula, CLI commands, agent counts, etc.). Before rebuilding or editing a page, verify its claims against the source of truth:
- CLI tools → check `bin/` for actual scripts
- Trust formula → check `spec/signal-trust-framework.md`
- Event types → check `spec/event-catalog.md`
- Agent definitions → check `frameworks/intent/servers/` (if present)

If a page's content contradicts the source of truth, update the page content to match reality.

### Signal Generation from Conversations
Brien may generate signals from Cowork sessions, Claude desktop app (iOS/web/desktop), or regular chat. These signals will be formatted as `.intent/signals/` files and committed to the repo. Claude Code agents should monitor for new signals and begin processing them through the enrichment pipeline.

### When Stuck
**Generate a disambiguation signal** — don't dead-end. Capture what's ambiguous as a new signal for Brien to review. Write it to `.intent/signals/` with `status: blocked` and `trust: 0.1`.

### Priority of Work
1. Task specs in `docs/tasks/` — explicit handoffs from Cowork
2. Contract violations — fix any failing contracts
3. Signals with trust ≥ 0.6 that can be auto-executed (L3/L4)
4. Signals that need enrichment (add context, compute trust)
5. Specs that are approved and ready for execution
6. Infrastructure work (tooling, pipeline, config)
