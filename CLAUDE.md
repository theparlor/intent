# Intent — Development Continuity Guide

> This file exists so that any AI agent or human contributor can pick up Intent development without prior session context. Read this first.

## What Is Intent?

Intent is a **team operating model for AI-augmented product teams**. It replaces Agile's ceremony-driven coordination with a continuous loop: **Notice → Spec → Execute → Observe**. When AI collapses implementation from weeks to hours, the bottleneck moves upstream — from delivery to discovery, specification, and observation. Intent is the operating model for that new reality.

Intent is NOT a SaaS tool (yet). It's a methodology that lives in files, tracked in git, observable through events. Teams adopt it by adding a `.intent/` directory to their repos.

**Owner:** Brien (theparlorhq@gmail.com) — solo practitioner, The Parlor
**Repo:** github.com/theparlor/intent (private)
**Status:** Idea → ready for validation. Thought leadership first, methodology product second, tooling conditional on validation.

## Core Concepts

### The Loop
```
NOTICE  →  SPEC  →  EXECUTE  →  OBSERVE  →  (back to NOTICE)
```
No sprint boundaries. No ceremony tax. A continuous loop where the team's energy follows the highest-leverage work.

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
- `.intent/` — Work artifacts (signals, intents, specs, contracts, decisions, events)
- `.claude/` — Agent reasoning (project context, session transcripts)
- `.entire/` — Observability (execution traces from Entire.io)

## Repo Structure

```
intent/
├── .intent/                  ← Intent's own dogfood
│   ├── INTENT.md             ← Project manifest
│   ├── decisions.md          ← Decision log (source of truth)
│   └── signals/              ← 5 founding signals (SIG-001 through SIG-005)
├── artifacts/                ← React JSX interactive artifacts
│   ├── intent-event-catalog.jsx    ← Event catalog (~750 lines)
│   ├── intent-flow-diagram.jsx     ← Flow diagram (~880 lines)
│   ├── intent-work-system.jsx      ← Work ontology explorer
│   └── intent-visual-brief.jsx     ← Product visual brief
├── docs/                     ← GitHub Pages site (source: main, /docs)
│   ├── index.html            ← Product landing page (~22KB)
│   ├── methodology.html      ← Full long-form rendering of methodology spec
│   ├── concept-brief.html    ← Full long-form rendering of concept brief
│   ├── signals.html          ← Signal stream
│   ├── decisions.html        ← Decision log
│   ├── event-catalog.html    ← Event catalog overview + link to artifact
│   ├── flow-diagram.html     ← Flow diagram overview + link to artifact
│   ├── work-system.html      ← Work ontology overview + link to artifact
│   ├── native-repos.html     ← Repo pattern guide
│   ├── visual-brief.html     ← Embeds visual-brief-app via iframe
│   └── visual-brief-app/     ← Vite-built React app for visual brief
├── spec/                     ← Markdown source files (source of truth for content)
│   ├── README.md             ← Spec directory overview
│   ├── intent-methodology.md ← Full methodology (9KB) — source for methodology.html
│   ├── intent-concept-brief.md ← Full concept brief (6KB) — source for concept-brief.html
│   ├── autonomous-operations-design.md ← Three-layer ops design
│   ├── signal-stream.md      ← Source for signals.html
│   ├── decision-log.md       ← Source for decisions.html
│   ├── event-catalog.md      ← Source for event-catalog.html
│   ├── flow-diagram.md       ← Source for flow-diagram.html
│   ├── repo-pattern.md       ← Source for native-repos.html
│   └── work-ontology.md      ← Source for work-system.html
├── notice/                   ← Loop directory: notice phase artifacts
├── execute/                  ← Loop directory: execute phase artifacts
├── observe/                  ← Loop directory: observe phase artifacts
├── reference/                ← Reference materials
├── CLAUDE.md                 ← THIS FILE — continuity guide
├── CHANGELOG.md              ← Timestamp-based version history
├── VERSION                   ← Current version (YYYY.MM.DD-MAJOR.MINOR.PATCH)
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

### Editing existing content
1. Edit the markdown source in `spec/` first
2. Then update the HTML in `docs/` to match
3. For methodology and concept-brief, the HTML is a full rendering of the markdown — every section, table, code block

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

## Intellectual Foundations

Intent draws from: Marty Cagan (product operating model), Jeff Patton (story mapping → spec mapping), Teresa Torres (continuous discovery → continuous observation), Josh Seiden (outcomes over outputs), OpenTelemetry (observability conventions). Primary empirical evidence: Brien's conversation with engineer Ari, whose team independently discovered the Intent pattern.

## What's Not Yet Done

- [ ] GitHub Pages not yet enabled by Brien
- [ ] Install .intent/ scaffolds into Brien's 4 repos (script exists at ~/Workspaces/Core/install-intent-scaffolds.sh)
- [ ] 5 in-depth interviews with teams experiencing AI + Agile friction
- [ ] Tier 3 observe-cycle agent (automated health check → signal generation)
- [ ] Phase 2 health check scheduling (launchd plist)
- [ ] Message to Ari about Intent (draft exists)
- [ ] Deeper positioning and vision work (Brien flagged for when he has time)
- [ ] OTel collector integration for production teams (Phase 6 of event implementation)
