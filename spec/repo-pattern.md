# Repo Pattern

> The three-layer structure every Intent-native repo follows: .intent/, .claude/, .entire/ — with file schemas and directory conventions.

## Why a Repo Pattern?

Intent is file-native and git-tracked. That means adopting Intent isn't installing software — it's adding a directory structure to your repo. The pattern is deliberate: three layers, each with a clear purpose, each observable, each composable with whatever else is already in the repo.

This is the minimum viable adoption. A team can add `.intent/` to an existing repo and start capturing signals today. No backend, no SaaS, no migration.

## Directory Structure

```
your-repo/
├── .intent/                  ← Layer 1: Intent work artifacts
│   ├── signals/              ← Observations from work
│   ├── intents/              ← What we want to change
│   ├── specs/                ← How we'll change it
│   ├── contracts/            ← Verifiable assertions
│   ├── decisions/            ← Significant choices with rationale
│   └── events/               ← Structured event stream (JSONL)
│       └── events.jsonl
├── .claude/                  ← Layer 2: Agent reasoning
│   ├── projects/             ← Project-level context for agents
│   └── sessions/             ← Session transcripts and reasoning
├── .entire/                  ← Layer 3: Observability
│   └── traces/               ← End-to-end execution traces
├── src/                      ← Your code (unchanged)
├── docs/                     ← Your docs (unchanged)
└── ...
```

## Layer 1: Intent (.intent/)

The Intent layer stores all work artifacts in structured files, versioned in git. This is the team's shared working memory — the durable record of what was noticed, what was decided, what was specified, and what happened.

### signals/
Observations from work, research, conversation. Each signal has a source, confidence score, timestamp, and related intents. Markdown files with YAML frontmatter, named by date and slug.

**Naming:** `YYYY-MM-DD-slug.md`

**Example:**
```yaml
---
id: SIG-001
confidence: 0.92
source: internal-research
related_intents: [positioning]
---
# Work needs a formal ontology
Teams who've tried AI-augmented workflows report that ticket-based coordination breaks down...
```

### intents/
What we want to change. Declarative statements: "Users should be able to X." Each intent links signals to specs. YAML with title, description, related signals, assigned to.

**Naming:** `YYYY-MM-DD-slug.yml`

### specs/
How we'll change it. Narrative + acceptance criteria (contracts). Markdown with frontmatter. Human-readable but machine-parseable. The spec is the primary handoff artifact between humans and agents.

**Naming:** `YYYY-MM-DD-slug.md`

### contracts/
Verifiable assertions extracted from specs. JSON schema defining inputs, outputs, and assertions. Executable by agents. A contract is "done" when all assertions pass.

**Naming:** `contract-spec-slug.json`

### decisions/
Significant architectural and strategic decisions. Context, alternatives considered, rationale, decision date. Markdown with frontmatter. The organizational memory of why things are the way they are.

**Naming:** `YYYY-MM-DD-slug.md`

### events/
Structured events from execution. OpenTelemetry-compatible format. JSONL (newline-delimited JSON). One file per day or one rolling file — team's choice.

**Naming:** `events.jsonl` or `events-YYYYMMDD.jsonl`

## Layer 2: Claude (.claude/)

Agent reasoning and session artifacts. Where Claude Code (or other AI agents) store project context and reasoning traces. This layer makes agent cognition observable — teams can see what the agent was thinking, what decisions it made, and where it got stuck.

### projects/
High-level project metadata. Vision, architecture, key decisions, dependencies. Used by agents to bootstrap context when starting a new session.

### sessions/
Session transcripts and reasoning logs. Agents log their thinking, decisions made, and blockers encountered. Enables post-execution review of agent reasoning.

## Layer 3: Entire (.entire/)

Observability layer. End-to-end execution traces and system health metrics. This is where Entire.io (or equivalent tooling) captures the full picture of what happened during execution.

### traces/
Complete execution traces. Spans, logs, metrics. Ingested from GitHub Actions, agent sessions, test runs. Used by the observe phase for pattern recognition and learning.

## File Naming Conventions

| Artifact | Pattern | Example |
|----------|---------|--------|
| Signal | `YYYY-MM-DD-slug.md` | `2026-03-28-work-ontology.md` |
| Intent | `YYYY-MM-DD-slug.yml` | `2026-03-28-event-system.yml` |
| Spec | `YYYY-MM-DD-slug.md` | `2026-03-28-event-catalog.md` |
| Contract | `contract-spec-slug.json` | `contract-event-catalog.json` |
| Decision | `YYYY-MM-DD-slug.md` | `2026-03-28-naming.md` |
| Events | `events.jsonl` | `events.jsonl` |

## Adoption Tiers

Teams don't have to adopt everything at once. Intent supports three tiers:

### Tier 1: Observe Only
Add `.intent/signals/` and `.intent/decisions/`. Start capturing what you notice and what you decide. No tooling required. This alone replaces informal "we should write that down" habits.

### Tier 2: Spec-Driven
Add `.intent/specs/` and `.intent/contracts/`. Start writing specs with verifiable assertions. Agents can now execute against them. This is where the loop starts closing.

### Tier 3: Full Observability
Add `.intent/events/`, `.claude/`, and `.entire/`. Full event emission, agent reasoning capture, and end-to-end trace aggregation. The system becomes self-observing.

## Where This Lives

- **Interactive artifact:** [Work System (React)](../artifacts/intent-work-system.jsx)
- **Site page:** [native-repos.html](../docs/native-repos.html)
