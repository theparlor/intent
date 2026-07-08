---
id: SIG-044
title: Parallel AI session orchestration UX is an unsolved L1 problem — solutions are appearing but may only reveal the challenge rather than solve it
timestamp: 2026-04-12T23:00:00Z
source: community-observation
author: brien
confidence: 0.8
trust: 0.7
autonomy_level: L2
status: active
cluster: productivity-os-layers
referenced_by:
  - "Lanes.sh — multi-session workspace for AI coding agents"
  - "Brien's Cowork dispatch experience — 60+ parallel tasks, lost overview"
  - "SPEC-productivity-os-layers (L1 Personal OS)"
  - "Dex Horthy, harness engineering"
---

# SIG-044: Parallel Session Orchestration UX — The L1 Cockpit Problem

## What was noticed

A developer built Lanes (lanes.sh) specifically because managing multiple Claude Code and Codex sessions in parallel was overwhelming — "agents were working against each other," "kept losing track," "tried worktrees but lost overview." He went from quarterly planning → monthly → weekly → intra-daily and hit the orchestration ceiling.

This is the same problem Brien experienced in this Cowork session: 60+ dispatch tasks spawned, no real-time visibility into which were running vs. stalled vs. completed, no coordination to prevent conflicting writes, and the dashboard/transcript reading loop was manual and fragile.

## Why solutions may only reveal the challenge

The risk with tools like Lanes is that they provide a better cockpit for watching parallel sessions but don't address the underlying architectural problem: without trust levels, completion criteria, dashboard-driven queues, and checkpointing, more visibility just means you can watch things fail faster.

The pattern: someone builds a UI layer over the existing chaos (parallel sessions with no governance) and it feels valuable initially because you can finally SEE what's happening. But visibility without governance is monitoring without remediation — Splunk's 73% alert suppression stat applies here. You can see the alerts but you can't act on them all.

## What's actually needed at L1

The function/space that needs to be addressed combines three layers:

1. **Cockpit (what Lanes provides)**: Real-time visibility into what each session is doing, resource consumption, conflicts, progress. This IS needed but it's the display layer, not the control layer.

2. **Governance (what Intent provides)**: Trust levels that determine what sessions can do autonomously, completion criteria that prevent premature "done" declarations, the cortège pattern that ensures items are worked to exhaustion not comfort, and the enrichment dashboard that drives the queue.

3. **Coordination (what neither fully provides yet)**: Agent-to-agent awareness. Session A knows Session B is modifying the same file. Conflict detection before it happens, not after. Lock management for shared resources. The Confluent event-driven patterns (Orchestrator-Worker, Blackboard) are the architectural answer, but no product implements them for AI coding sessions yet.

## Implications for Intent

Intent's Productivity Stack has a cell at L1/Tool Access that says "4 MCP servers + plugin." The parallel session orchestration UX belongs in that cell or adjacent to it. Brien doesn't need to build the cockpit (Lanes or similar tools will handle the display layer), but Intent needs to provide the governance and coordination layers that make the cockpit useful.

The Cowork plugin design should account for this: when Brien dispatches 22 tasks from his phone, the plugin should provide the governance layer (which tasks have authority to write where, what completion looks like, how conflicts are detected) regardless of what cockpit UI is showing the progress.

## Who to watch

- **Lanes.sh** — cockpit UI for parallel AI sessions. Learn from the UX patterns.
- **Anthropic Cowork** — dispatch is their answer but governance is thin.
- **Dex Horthy / HumanLayer** — harness engineering addresses the governance layer.
- **Confluent** — event-driven coordination patterns are the architectural foundation.
- **The community at large** — this is a hot problem space and solutions will proliferate.

## Triage, 2026-07-08

Disposition: still pending on the specific gap named (agent-to-agent conflict detection, file lock management for parallel sessions). The governance layer this signal calls for has grown substantially since (the full autonomy-grant/closure-discipline hook stack), but that layer governs individual-session behavior, not cross-session coordination or conflict detection between simultaneously-running agents. Core/frameworks/intent/reference/lanes-session-orchestration.md exists as a reference note on the Lanes tool, not as an implemented coordination layer.
