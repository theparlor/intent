---
title: Lanes Session Orchestration
type: framework
maturity: final
confidentiality: internal
reusability: adaptable
created: 2026-04-27
depth_score: 4
depth_signals:
  file_size_kb: 7.4
  content_chars: 7257
  entity_count: 0
  slide_count: 0
  sheet_count: 0
  topic_count: 0
  has_summary: 0
vocab_density: 0.14
---
# Lanes.sh — Parallel AI Session Orchestration

> Reference material for SIG-044. Awareness-level research on cockpit UX patterns for parallel AI coding sessions.

**Last updated:** 2026-04-26
**Source:** https://lanes.sh, blog post "Introducing Lanes" (2026-03-15)

## What Lanes Is

Lanes is a native macOS app that wraps AI coding CLIs (Claude Code, Codex, etc.) in a kanban-style issue board. Each issue card gets its own real PTY terminal session, its own git worktree, and real-time status tracking. The tagline: "AI coding CLIs got powerful. The workflow around them didn't. Lanes is the missing layer."

Published March 15, 2026. Early access via Discord. No public GitHub repo for the app itself (org: github.com/lanes-sh).

## The Problem They're Solving

From their intro post — this is almost word-for-word Brien's Cowork experience:

"We were running three Claude Code sessions across eight terminal tabs. One had finished ten minutes ago. One was waiting for input we didn't notice. Two were editing the same file."

Three gaps identified: no single view (you ARE the dashboard), no structure (tasks live in your head), no isolation (agents share working directory, cause conflicts).

## Feature Set

**Issue Board.** Kanban columns: Planning → Implementation → Review → Done. Multi-select, context menus, collapsible columns, board tabs per project. Each issue is a card with a prompt, an agent session, and a worktree.

**Live Terminals.** Real PTY sessions — your shell, your dotfiles, your aliases. Not a wrapper or abstraction. Claude Code runs exactly as it would in your terminal. Real-time status indicators: busy, awaiting input, stopped, error. Sessions resume across app restarts with full conversation history.

**Worktree Management.** Auto-creates a git worktree per issue with a generated branch name. Each session works on its own branch. Status bar shows uncommitted/unmerged state. Auto-cleanup on issue completion.

**Git Changes.** Two modes: working tree changes and commit history. Monaco inline diff viewer with auto branch detection from the active worktree.

**File Browser + Editor.** Sidebar file tree, Monaco editor, tabbed editing, dirty tracking, syntax highlighting.

**Dependencies.** Link issues as dependencies. Cycle detection. Blocked issues stay blocked until prerequisites reach Done.

**Labels + Filtering.** 13 label colors. Filter by label, directory, or workflow step.

**Quick Commands.** Cmd+Alt+1-9 for preset/custom commands. Two types: CLI commands injected into the AI session, and shell commands run directly.

## Architecture

Lanes is a **display and isolation layer**, not a coordination layer. It:

- Wraps existing CLI agents (doesn't replace them)
- Uses git worktrees for isolation (well-understood, reliable)
- Provides kanban status tracking (card state, not agent reasoning state)
- Offers real PTY sessions (no abstraction penalty)

What it does NOT do: trust scoring, completion criteria enforcement, agent-to-agent awareness, conflict detection before it happens, governance over what agents can modify, or queue-driven dispatch.

## Who Built It

The team publishes through lanes.sh with a Discord community for early access. Their blog has a second post: "The IDE Is Dead. Long Live the ADE." (April 2, 2026) — arguing the IDE → ADE (Agent Development Environment) transition. This framing aligns with the broader "agentic coding" wave of early 2026.

## Competitive Landscape (as of April 2026)

Lanes is one of several tools attacking the parallel session problem:

**Superset (superset.sh)** — Open-source (GitHub: superset-sh/superset). Agent-agnostic orchestrator. Creates worktree per task, handles session management with persistent daemons, diff review, editor integration. Claims 10+ parallel agents. More CLI-oriented than Lanes' GUI approach.

**Agent-Deck (GitHub: asheshgoplani/agent-deck)** — TUI (terminal UI) session manager. One interface for Claude, Gemini, OpenCode, Codex.

**Agent Orchestrator (GitHub: ComposioHQ/agent-orchestrator)** — Plans tasks, spawns agents, handles CI fixes, merge conflicts, code reviews autonomously.

**Claude Squad / Conductor / Verdent Deck** — Various community tools. By February 2026, every major tool shipped multi-agent capabilities.

The common pattern across all of them: worktree-based isolation + some form of status dashboard. None implement governance or trust-based coordination.

## UX Patterns Worth Learning From

1. **Card = Session = Worktree.** The 1:1:1 mapping is clean. Each card IS the unit of work, the terminal, and the branch. No indirection.

2. **Status as first-class UI.** Real-time indicators (busy / awaiting input / stopped / error) solve the "which tab needs me?" problem. This is the minimum viable cockpit.

3. **Kanban over list.** Columns give spatial meaning to lifecycle stage. You can SEE what's in progress vs. review vs. done without reading status labels.

4. **Dependencies as issue links.** Blocking/blocked relationships with cycle detection. Simple but prevents the "agent starts before prerequisite is done" problem.

5. **Resume across restarts.** Session persistence means you don't lose context when the app or machine restarts. Critical for long-running agent work.

6. **Quick commands as muscle memory.** Cmd+Alt+N for common actions. The power user wants keyboard-driven dispatch, not mouse-driven.

## What Intent's Governance Layer Adds on Top

| Capability | Lanes (Cockpit) | Intent (Governance) |
|---|---|---|
| **Visibility** | Real-time status per card | Same, but enriched with trust scores and completion % |
| **Isolation** | Git worktree per issue | Same mechanism, plus write-authority constraints (which files this agent can touch) |
| **Lifecycle** | Kanban drag (manual) | Trust-gated transitions (auto-promote when criteria met, block when unsafe) |
| **Completion** | Human drags to Done | Completion criteria defined in spec — agent declares done, system verifies |
| **Conflict prevention** | Worktree isolation (no shared writes) | Pre-dispatch conflict detection (don't assign overlapping file scopes) |
| **Dispatch** | Manual (create card, write prompt) | Queue-driven from enrichment dashboard; phone-dispatchable |
| **Prioritization** | Manual card ordering | Trust-scored queue with autonomy levels determining agent authority |
| **Quality** | Human reviews in Review column | Cortege pattern — work items to exhaustion, not comfort |
| **Agent awareness** | None (agents are independent) | Event-driven coordination (Orchestrator-Worker pattern) |
| **Learning** | None | Observe loop feeds back into knowledge base and future dispatch decisions |

The key insight: Lanes solves the **display problem** (I can't see what's happening) but not the **governance problem** (I can't control what happens) or the **coordination problem** (agents can't see each other). Intent doesn't need to build the cockpit — tools like Lanes will keep improving that layer. Intent needs to provide the governance and coordination APIs that any cockpit can consume.

## Sources

- https://lanes.sh/
- https://lanes.sh/blog/introducing-lanes
- https://github.com/lanes-sh
- https://superset.sh
- https://github.com/superset-sh/superset
