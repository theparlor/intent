---
title: Autonomous Operations Layer
type: spec
maturity: draft
created: 2026-03-27
summary: "Design spec for migrating automated workflows from Cowork sandbox to Claude Code CLI native execution with self-healing, intelligence, and full filesystem authority."
depth_score: 3
depth_signals:
  file_size_kb: 3.3
  content_chars: 3306
  entity_count: 0
  slide_count: 0
  sheet_count: 0
  topic_count: 0
  has_summary: 1
vocab_density: 0.96
---
# Autonomous Operations Layer

> **Purpose**: Turn three operational workflows — Library Index, Digital Declutter, and Workspace Health — into self-healing, intelligent, autonomous agents running natively via Claude Code CLI.
>
> **Design Date**: 2026-03-27
> **Status**: Draft — Designed in Cowork, to be built in Claude Code

---

## The Problem

A sophisticated personal operating system spanning 39,000+ indexed assets, 4 MCP servers, an ML enrichment pipeline, a file organization governance system, and a workspace health fabric. But the automation layer has an execution gap:

**The analogy**: A well-designed factory where every machine is perfectly calibrated, the conveyor belts are aligned, and the quality control specs are written. But the factory only runs when someone physically walks in, flips each breaker, watches for jams, and manually calls the mechanic if something stalls.

| Workflow | Current State | Failure Mode |
|----------|--------------|--------------|
| Library Index nightly refresh | Cowork scheduled task | Sandboxed VM can't write to `.git`, can't clear lock files, can't self-heal |
| Digital Declutter (Downloads intake) | Cowork plugin, manually invoked | Not scheduled. Files accumulate until manually triggered |
| Workspace Health Check | Shell script, manually run | No schedule. Drift accumulates silently |

---

## Design Principles

1. **Native authority, not borrowed permissions.** Full filesystem access. Can clear lock files, write `.git` objects, push to remotes.
2. **Intelligence, not just automation.** Checks preconditions, adapts to unexpected state, decides whether to proceed or pause, explains what it did and why.
3. **Resilience through pre-flight, not retry loops.** Pilot's checklist — verify state before engaging.
4. **Observable by default.** Every run produces a structured log. No silent failures.
5. **The governance chain is the spec.** CLAUDE.md, WORKSPACE_GOVERNANCE.md, and RULES.md are the instructions.

---

## Target Architecture: Three Layers

```
LAYER 3: INTELLIGENCE    Claude Code CLI (native)
                         CLAUDE.md → Pre-flight → Decision → Post-flight
                              │
LAYER 2: ORCHESTRATOR    macOS launchd (native scheduler)
                         Nightly Index @ 2AM | Declutter @ 4hr | Health @ 6AM
                              │
LAYER 1: PIPELINE        Python scripts + shell commands
                         auto_tagger → enrichment → fingerprint → catalog
```

---

## Implementation Phases

- **Phase 0**: Install Entire.io (agent observability)
- **Phase 1**: Library Index Nightly Refresh (pattern-setter)
- **Phase 2**: Workspace Health Check
- **Phase 3**: Digital Declutter Intake

*Full spec with pre-flight checklists, decision logic, and edge case analysis maintained in the canonical source at Core/reference/AUTONOMOUS_OPERATIONS_DESIGN.md*

---

*Designed: 2026-03-27 in Cowork | To be built: Claude Code CLI*
