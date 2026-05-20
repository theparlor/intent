---
title: CodeBurn — AI Coding Token Observability
type: reference-analysis
updated: 2026-04-26
depth_score: 4
depth_signals:
  file_size_kb: 14.2
  content_chars: 14014
  entity_count: 0
  slide_count: 0
  sheet_count: 0
  topic_count: 0
  has_summary: 0
vocab_density: 0.21
source: "https://github.com/getagentseal/codeburn"
author: AgentSeal (Germany) — hello@agentseal.org
version_analyzed: 0.9.1
repo_created: 2026-04-13
stars_at_analysis: 3,926 (13 days old)
license: MIT
---
# CodeBurn Analysis: AI Coding Cost Observability for Intent

## What It Is

CodeBurn is a read-only token/cost observability tool for AI coding agents. Think of it as the "billing dashboard you wish your AI provider gave you" — but computed locally from session files already on your disk. No API keys, no proxy, no wrapper. It reads JSONL session transcripts that Claude Code, Codex, Cursor, and others write to disk, then computes cost, classifies activity, and surfaces waste patterns.

The mental model: CodeBurn is to AI agent sessions what `htop` is to processes. It doesn't control anything — it makes the invisible visible.

## How It Works (Architecture)

The architecture is a pipeline with four stages, all running locally:

**1. Session Discovery** — Provider-specific adapters walk known disk locations:
- Claude Code: `~/.claude/projects/<sanitized-path>/<session-id>.jsonl`
- Claude Desktop (Cowork): `~/Library/Application Support/Claude/local-agent-mode-sessions/` (recursive walk, depth 8)
- Codex: `~/.codex/sessions/YYYY/MM/DD/rollout-*.jsonl`
- Cursor: SQLite at `~/Library/Application Support/Cursor/User/globalStorage/state.vscdb`
- Pi/OMP: `~/.pi/agent/sessions/` and `~/.omp/agent/sessions/`
- Copilot: `~/.copilot/session-state/`

**2. JSONL Parsing + Dedup** — Each assistant entry in a session file contains: model name, token usage (input, output, cache_read, cache_write), tool_use blocks, timestamps. Messages are deduped by API message ID (Claude), cumulative token cross-check (Codex), or conversation/timestamp (Cursor). Date-range filtering happens per-entry, not per-file (though files with mtime before range start are skipped entirely for speed).

**3. Turn Classification** — 13 deterministic categories classified from tool usage patterns and user message keywords. No LLM calls. Categories: Coding, Debugging, Feature Dev, Refactoring, Testing, Exploration, Planning, Delegation, Git Ops, Build/Deploy, Brainstorming, Conversation, General. The classifier first checks tool patterns (Edit/Write = Coding, Agent spawn = Delegation, EnterPlanMode = Planning), then refines by keyword regex on the user message.

**4. Cost Calculation** — Pricing fetched from LiteLLM's model_prices_and_context_window.json (auto-cached 24h). Handles input, output, cache write, cache read, web search costs, and fast mode multiplier. Hardcoded fallbacks for all Claude and GPT models prevent fuzzy-match mispricing.

**Output surfaces:**
- Interactive TUI dashboard (Ink/React for terminals) with gradient charts, keyboard navigation
- Native macOS menubar app (Swift/SwiftUI) showing today's spend
- JSON API (`--format json`) for programmatic consumption
- CSV/JSON export for archival
- `optimize` command that scans for waste patterns and suggests fixes
- `compare` command for side-by-side model comparison
- `yield` command (experimental) correlating sessions with git commits

## Critical Finding: Claude Desktop / Cowork Support

**CodeBurn already reads Cowork session data.** The Claude provider's `getDesktopSessionsDir()` function explicitly walks `~/Library/Application Support/Claude/local-agent-mode-sessions/` — which is exactly where Brien's Cowork dispatch sessions live. This means:

- All 20+ parallel persona enrichment dispatch tasks will show up as separate sessions
- Each session's model usage (Opus vs Sonnet vs Haiku) will be individually tracked
- MCP server usage will appear in the MCP breakdown panel
- Agent spawns (dispatch_agent) will be classified as "Delegation" category

**However:** The recursive walk goes to depth 8 looking for `projects/` subdirectories. Cowork's actual session structure (`local-agent-mode-sessions/<uuid>/<uuid>/local_<uuid>/`) may or may not match this pattern. Needs empirical testing.

## Evaluation Against Brien's Use Case

### What Brien Needs vs What CodeBurn Provides

| Brien's Need | CodeBurn Provides | Gap? |
|-------------|-------------------|------|
| Token consumption per persona enrichment run | Per-session cost breakdown by model | Need to correlate session IDs to persona names |
| Opus vs Sonnet cost comparison for synthesis vs retrieval | `compare` command + per-model breakdown | Direct fit |
| Cost-per-persona-artifact metric | Per-project breakdown, per-session averages | Need post-processing to map sessions → artifacts |
| Cache hit rate optimization for persona loading | Cache hit % in dashboard, `optimize` detects low cache | Direct fit |
| One-shot success rate for enrichment agents | 1-shot rate per category (edit/test/fix retry detection) | Direct fit for code tasks; less meaningful for knowledge compilation |
| Total burn across model mixing architecture | Multi-model breakdown in single view | Direct fit |
| GLM-5.1/local model cost comparison | LiteLLM pricing covers all models; model alias system for custom names | Need to verify local model session format compatibility |
| Real-time monitoring during parallel dispatch | Auto-refresh every 30s; menubar shows today's spend | Near-real-time, not streaming |

### Model Mixing Architecture Alignment

CodeBurn's model comparison feature (`codeburn compare`) is directly designed for Brien's model mixing question. It compares:
- One-shot rate per model per task category
- Cost per call and cost per edit
- Cache hit rate per model
- Output tokens per call
- Working style differences (delegation rate, planning rate, tools per turn)

This gives Brien empirical data for the Opus-for-synthesis, Sonnet-for-retrieval, Haiku-for-high-volume architecture. He can run a week of mixed-model persona enrichment, then `codeburn compare` to see exactly where each model excels.

### Cowork Plugin Design Relevance

CodeBurn's `optimize` command detects patterns directly relevant to Cowork plugin design:
- **Files re-read across sessions** — Shows if persona context files are being re-parsed instead of cached
- **Low Read:Edit ratio** — Editing without reading leads to retries
- **Unused MCP servers** — Tool-schema overhead for every session
- **Ghost agents/skills** — Defined but never invoked
- **Bloated CLAUDE.md** — With @-import expansion counted
- **Cache creation overhead** — Relevant for persona loading budget

The optimize output includes an A-F setup health grade and tracks improvement over time.

## Who Is AgentSeal?

AgentSeal is a Germany-based organization (created 2026-04-18 on GitHub — 8 days old at time of analysis). Their org description: "Find out what breaks your AI agent before attackers do. 300+ probes. Prompts, MCP, RAG, genome mapping. Open source."

This positions them as an **AI agent security/observability company**, not just an open-source hobby project. CodeBurn (cost observability) is likely their community-building wedge — the free tool that gets adoption before the paid security product. The "300+ probes" and "genome mapping" language suggests a forthcoming agent security testing product.

- **Website:** agentseal.org
- **Email:** hello@agentseal.org
- **Twitter:** @agentseal_org
- **GitHub:** github.com/getagentseal (6 public repos)
- **Location:** Germany
- **Verified org** on GitHub

The codeburn repo hit ~3,900 stars in 13 days — significant traction indicating real demand for this category.

## Mapping to Intent Architecture

### Observe Phase (Flow 5 & 6)

CodeBurn's output maps directly onto Intent's Observe phase. The key architectural question: **should CodeBurn data feed INTO Intent's event system, or run alongside it?**

**Recommendation: Alongside, with a bridge.**

CodeBurn's data model (sessions → turns → API calls → cost) is complementary to Intent's event model (signals → intents → specs → observations). They measure different things:

| CodeBurn Measures | Intent Observes |
|------------------|-----------------|
| Token consumption | Work artifact lifecycle |
| Cost per model/task | Signal-to-spec velocity |
| Retry rates | Trust level accuracy |
| Cache efficiency | Enrichment pipeline throughput |
| Tool usage patterns | Knowledge base freshness |

The bridge: CodeBurn's JSON export (`codeburn report --format json`) can be ingested as an observation into Intent's `observations/metrics/` directory. A scheduled task could:
1. Run `codeburn report -p today --format json > observations/metrics/codeburn-$(date +%Y-%m-%d).json`
2. An enrichment agent reads the JSON and surfaces signals when cost anomalies appear

### Rohit's Principle 9 (Observability) Alignment

Rohit prescribes: "Every agent action should be observable, traceable, and auditable." CodeBurn partially fulfills this:

| Rohit's Observability | CodeBurn | Gap |
|----------------------|----------|-----|
| Token usage per action | Yes — per-turn, per-session, per-model | |
| Cost per session | Yes — with LiteLLM pricing | |
| Model selection impact | Yes — compare command | |
| Tool usage patterns | Yes — core tools, MCP, bash, agent spawns | |
| Retry/failure rates | Yes — one-shot rate, retry detection | |
| Latency/throughput | No — timestamps exist but latency not computed | Missing |
| Traceability (span/trace) | No — sessions are flat, not OTel spans | Structural gap |
| Error classification | No — retries detected but error types not classified | Missing |

The structural gap matters: CodeBurn is session-centric (flat list of turns), not trace-centric (parent-child spans). Intent's OTel-compatible event system fills this — the two are complementary, not competing.

### Knowledge Engine Integration

For Brien's persona enrichment pipeline specifically, CodeBurn data could answer:
- "How much does it cost to compile one persona from raw interview transcripts?"
- "Is Opus 4.6 worth the 5x cost premium for persona synthesis vs Sonnet 4.6?"
- "What's our cache hit rate when loading the same engagement context across 20 parallel persona runs?"
- "Which MCP tools are eating tokens without producing value?"

These are exactly the metrics Brien needs to make the model mixing decision empirically rather than theoretically.

## Practical Setup

### Installation
```bash
npm install -g codeburn
# or
npx codeburn
```
Requires Node.js 20+.

### First Run
```bash
codeburn                        # Interactive TUI, default 7 days
codeburn today                  # Today's usage
codeburn status                 # One-liner: today + month
codeburn optimize               # Find waste, get fixes
```

### Brien-Specific Configuration
```bash
# Set subscription plan for relative usage tracking
codeburn plan set claude-max    # $200/month plan

# Filter to Intent project only
codeburn report --project intent

# Export for observation pipeline
codeburn report -p today --format json > observations/metrics/codeburn-$(date +%Y-%m-%d).json

# Compare models after a mixed-model enrichment run
codeburn compare -p week

# Check yield (did the work actually ship?)
codeburn yield -p 30days
```

### Menubar App (Always Visible)
```bash
npx codeburn menubar
```
Shows today's spend in macOS menubar. Refreshes every 30s. Click for detailed breakdown.

### JSON Pipeline Integration
```bash
# Cost per project
codeburn report --format json | jq '.projects'

# Today's total cost
codeburn today --format json | jq '.overview.cost'

# Model breakdown
codeburn report --format json | jq '.models'
```

## Risks and Limitations

1. **Read-only, disk-only.** Cannot see API-only usage (no local session files). If Brien moves to hosted mode with always-on processing, those sessions may not produce local JSONL files. CodeBurn would miss them.

2. **No trace correlation.** CodeBurn sessions are flat — it doesn't know that dispatch task #7 was "compile PER-014 from 3 interview transcripts." Brien would need a naming convention or post-processing step to correlate sessions to knowledge artifacts.

3. **Cowork session format untested.** The Claude provider walks `local-agent-mode-sessions/` recursively, but the actual JSONL format of Cowork dispatch sessions may differ from Claude Code's format. Needs empirical validation.

4. **13-day-old project.** Moving fast (0.9.1 already), but the org is 8 days old. Could pivot, abandon, or get acquired. MIT license means the code is forkable regardless.

5. **No API/webhook output.** Data only flows out via CLI/TUI/file export. No event stream, no webhook, no OTel export. Intent's observe phase would need to poll (scheduled export) rather than subscribe.

6. **Classification is heuristic.** The 13-category classifier uses keyword regex, not semantic analysis. "Persona enrichment" work may classify as "Exploration" or "Coding" depending on whether the agent is reading files or writing knowledge artifacts.

## Recommendation

**Install immediately. Run for one week alongside normal work. Then evaluate.**

CodeBurn fills a specific gap in Brien's stack: the empirical cost data needed to make the model mixing decision. It requires zero configuration (reads existing session files), introduces no risk (read-only), and produces exactly the data Brien has been reasoning about theoretically.

The one-week evaluation should answer:
1. Does it correctly discover Cowork dispatch sessions?
2. What's the actual Opus vs Sonnet cost ratio for enrichment work?
3. What's the cache hit rate across parallel persona runs?
4. Does the `optimize` command surface actionable Cowork plugin improvements?

After the evaluation, decide whether to build the JSON-to-observations bridge for ongoing monitoring.

## Signal Candidates

| Signal | Description | Priority |
|--------|-------------|----------|
| Install codeburn, validate Cowork session discovery | Empirical test of tooling gap | HIGH |
| Build codeburn → observations/metrics/ bridge | Scheduled JSON export as observation | MEDIUM |
| Run `codeburn compare` after mixed-model enrichment sprint | Empirical model mixing decision | HIGH |
| Evaluate `codeburn optimize` for Cowork plugin design | Token waste reduction | MEDIUM |
| Monitor AgentSeal's security product launch | Potential observability integration | LOW |
