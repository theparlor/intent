# Signal Capture System

> Architecture for capturing signals from every surface where practitioners work — Slack, Claude, Cursor, GitHub, ChatGPT, Copilot, and CLI.

## The Problem

Signals die in the gap between where they're noticed and where the system can see them. Right now, capturing a signal means: open a text editor, write a markdown file with the right frontmatter, save it to `.intent/signals/`, commit, push. That's 6 steps and a context switch. The signal is gone by step 2.

The capture bar has to be as low as writing a sticky note. One action, no context switch, from wherever you already are.

## Architecture

```
┌─────────────────────────────────────────────────┐
│              CAPTURE SURFACES                    │
│                                                  │
│  Slack    Claude Code    Cursor    CLI           │
│  Cowork   ChatGPT       Copilot   GitHub        │
│  Codex    365 Copilot   VS Code   Terminal       │
└──────────────────┬──────────────────────────────┘
                   │
                   ▼
┌─────────────────────────────────────────────────┐
│           SIGNAL INGESTION LAYER                 │
│                                                  │
│  Adapter per surface → normalize → validate      │
│                                                  │
│  Output: structured signal file                  │
└──────────────────┬──────────────────────────────┘
                   │
                   ▼
┌─────────────────────────────────────────────────┐
│            LANDING ZONE                          │
│                                                  │
│  .intent/signals/YYYY-MM-DD-slug.md              │
│  committed to repo via PR or direct push         │
└──────────────────┬──────────────────────────────┘
                   │
                   ▼
┌─────────────────────────────────────────────────┐
│            EVENT EMISSION                        │
│                                                  │
│  GitHub Action on merge → signal.created         │
│  → .intent/events/events.jsonl                   │
└─────────────────────────────────────────────────┘
```

## Signal Schema (Minimum Viable)

Every signal, regardless of capture surface, resolves to this:

```yaml
---
id: SIG-XXX
timestamp: 2026-03-29T14:30:00Z
source: slack | claude-code | cowork | cursor | cli | github | chatgpt | copilot | codex
confidence: 0.0-1.0  # optional, defaults to null (unscored)
related_intents: []   # optional, linked later
author: brien         # who noticed
surface_context: ""   # optional, e.g. slack channel, PR number, session ID
---
# Signal title (one line)

Body text: what was noticed and why it might matter.
```

**Minimum required fields:** timestamp, source, author, title, body.
Everything else can be added later by the practitioner or by an automated enrichment step.

## Capture Surfaces — Adapter Strategy

### Tier 1: MCP Server (ships first)

**Covers:** Claude Code, Cowork, Cursor

One MCP server, one `capture_signal` tool. These three tools all support MCP natively, so a single server gives us 3 surfaces immediately.

**How it works:**
- Practitioner says "that's a signal" or explicitly invokes the tool
- MCP tool takes: title (required), body (optional), confidence (optional)
- Server writes the signal file to `.intent/signals/` in the configured repo
- Server can commit directly (local) or push via GitHub API (remote)

**Why this is Tier 1:** MCP is the highest-leverage adapter. One implementation, three surfaces. Claude Code and Cursor are where architects spend their time. Cowork is where strategic thinking happens.

### Tier 2: CLI (ships first, alongside MCP)

**Covers:** Any terminal

A shell script or lightweight Node CLI.

```bash
intent signal "OTel traces show 40% of contracts fail on first pass"
```

**How it works:**
- Takes a quoted string as the signal title
- Optionally: `--body "longer explanation"` `--confidence 0.8`
- Creates the markdown file with timestamp and frontmatter
- Stages for commit (or auto-commits with `--commit`)
- Works entirely local — no API calls, no auth

**Why Tier 2:** Lowest possible implementation cost. Works everywhere. Good fallback when MCP isn't available.

### Tier 3: Slack Integration

**Covers:** Slack (team conversations)

A Slack bot or Workflow Builder automation.

**Option A: Reaction-based capture**
- React to any message with a designated emoji (e.g., 🔵 or `:signal:`)
- Bot captures the message text, channel, author, timestamp
- Bot creates a signal file via GitHub API and opens a PR
- Practitioner reviews/edits the PR to refine the signal

**Option B: Slash command**
- `/signal OTel traces show 40% of contracts fail on first pass`
- Bot creates the file, opens PR
- Optionally posts back to channel with a link to the signal

**Option C: Workflow Builder (no-code)**
- Slack Workflow triggered by emoji reaction or form submission
- Sends webhook to a lightweight endpoint (Cloudflare Worker, Vercel function)
- Endpoint creates file via GitHub API

**Why Tier 3:** Slack is where cross-functional conversations happen. The Ari conversation that started Intent happened in a conversation. But Slack integration requires auth, a bot, and possibly hosting — more infrastructure than Tier 1-2.

### Tier 4: GitHub Native

**Covers:** GitHub (PRs, issues, discussions)

**Option A: Issue label**
- Label an issue with `signal` → GitHub Action extracts title and first comment → creates signal file

**Option B: PR comment**
- Comment `/signal` on a PR → Action captures the context (PR title, diff summary, comment thread) → creates signal file

**Option C: Discussion integration**
- GitHub Discussions category for signals → Action watches for new posts → creates signal files

**Why Tier 4:** GitHub is already the landing zone, so this is the shortest path. But signals from GitHub tend to be more structured (they're already written down) — the real value is in capturing the *unstructured* observations from conversations and work sessions.

### Tier 5: AI Tool Plugins (later)

**Covers:** ChatGPT, GitHub Copilot, Microsoft 365 Copilot, Codex

Each of these has its own plugin/extension model:

- **ChatGPT:** Custom GPT with an Action that calls GitHub API
- **GitHub Copilot Extensions:** Copilot agent that responds to `@intent signal ...`
- **Microsoft 365 Copilot:** Copilot plugin (declarative or API-based)
- **Codex:** Agent hook that emits signals during autonomous execution
- **VS Code Extension:** Command palette action `Intent: Capture Signal`

These all follow the same pattern: capture text → normalize to schema → push to `.intent/signals/` via GitHub API. The variability is in each platform's plugin model.

**Why Tier 5:** Each requires platform-specific development. Worth doing once there's validation that the signal capture loop works at all (from Tiers 1-3).

## Implementation Plan

### Phase 1: Bootstrap Kit (build now)

1. **Signal template** — `.intent/templates/signal.md` with frontmatter schema
2. **CLI tool** — `bin/intent-signal` shell script
3. **MCP server** — `tools/intent-mcp/` with `capture_signal`, `list_signals`, `get_signal` tools
4. **GitHub Action** — `.github/workflows/intent-events.yml` that emits `signal.created` on merge
5. **Quickstart README** — `docs/quickstart.md` with 5-minute setup guide

### Phase 2: Team Capture (build after validation)

6. **Slack bot** — reaction-based signal capture
7. **GitHub Action** — issue/PR label-based signal capture

### Phase 3: Ecosystem Plugins (build on demand)

8. **ChatGPT Custom GPT** with signal capture action
9. **VS Code extension** with command palette integration
10. **GitHub Copilot extension**
11. **Microsoft 365 Copilot plugin**

## Design Principles

1. **One action to capture.** If it takes more than one step, it's too many.
2. **Capture first, refine later.** The initial signal can be a single sentence. Confidence scores, related intents, and enrichment happen after the fact.
3. **No new accounts.** Every adapter uses infrastructure the team already has (GitHub, Slack, their existing AI tool).
4. **File-native landing.** Every signal, regardless of source, becomes a markdown file in `.intent/signals/`. The file is the source of truth, not a database row.
5. **Observable by default.** Every signal.created event goes to `events.jsonl`. The system knows what's being noticed, from where, by whom.

## Open Questions

- **Auto-slug generation:** How do we generate a meaningful filename slug from a one-line signal? Timestamp + first-3-words? AI-generated slug?
- **Deduplication:** If the same observation is captured from Slack and from a CLI, how do we detect and merge?
- **Confidence scoring:** Should confidence be human-assigned at capture time, or should there be an enrichment step that scores based on signal frequency and source diversity?
- **Repo targeting:** For teams with multiple repos, which repo does the signal land in? Central intent repo? The repo most related to the signal?
- **PR vs direct commit:** Signals from external surfaces (Slack, ChatGPT) should probably open PRs for review. Signals from the CLI in a local repo can commit directly. Where's the boundary?
