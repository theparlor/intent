---
title: Hermes/Obsidian Three-Tier Memory System — Analysis and Intent Framework Mapping
type: reference
depth_score: 3
depth_signals:
  file_size_kb: 5.1
  content_chars: 4758
  entity_count: 0
  slide_count: 0
  sheet_count: 0
  topic_count: 0
  has_summary: 0
vocab_density: 0.84
source: Community post on AI assistant long-term memory using Obsidian
analyzed: 2026-04-12
relevance: "medium-high — validates Intent architecture decisions, surfaces implementable patterns for scheduled automation and memory hygiene"
---
# Hermes/Obsidian Memory System — Analysis

A solo practitioner built a personal AI assistant (Hermes) using Obsidian as a structured knowledge base the assistant can read from and write to autonomously. The system uses a three-tier memory architecture with scheduled automation pipelines.

## The Three-Tier Memory System

### Tier 1 — Hot Memory (~9K chars, per-session)
Injected every conversation turn. Covers communication preferences, active projects, recent corrections, procedural quirks. 67% capacity trigger promotes stable entries to Tier 2.

### Tier 2 — Vault Living Files (stable reference, on-demand)
Markdown files in Obsidian vault: context.md (operations overview), preferences.md (communication style), environment.md (hardware, services, known issues). Read on-demand when deeper context needed.

### Tier 3 — Daily Notes (searchable timeline)
Dated YYYY-MM-DD.md notes with Tasks, Schedule, Log, Wins, Context sections. Append-only. Backlinks to People, Decisions, Files. Creates searchable decision history.

## Mapping to Intent Architecture

| Hermes/Obsidian | Intent Framework | Gap |
|-----------------|-----------------|-----|
| Hot Memory (Tier 1) | CLAUDE.md + auto-memory | Intent's auto-memory lacks size-aware promotion trigger |
| Vault Living Files (Tier 2) | Knowledge Engine compiled artifacts | Intent compiles; Hermes just files. Intent is architecturally ahead. |
| Daily Notes (Tier 3) | events.jsonl + .intent/signals/ | Intent has structured events with OTel compatibility; Hermes has timestamped prose. Intent is ahead. |
| Content routing rules | Signal routing + trust scoring | Intent adds trust scoring and autonomy levels. Hermes is binary (do/don't). |
| Morning briefing pipeline | Not implemented | **Gap: Intent specs this but hasn't built it.** |
| 67% capacity trigger | Not implemented | **Gap: Auto-memory has no size-aware promotion mechanism.** |
| Vault hygiene (orphan detection) | Not implemented | **Gap: Enrichment dashboard tracks persona gaps but not memory hygiene.** |
| USER.md / MEMORY.md split | Mixed in single MEMORY.md | **Gap: Brien's auto-memory mixes user facts, project context, and feedback.** |

## What Intent Should Steal

### 1. Morning Briefing Pipeline
A scheduled task (cron or Cowork scheduled task) that:
- Collects from Google Calendar, Harvest, Slack, Gmail
- Creates a daily note in a standard location
- Delivers formatted summary to Brien's phone or Slack
This is the "always-on" processing Intent specs in the deployment topology but hasn't implemented. The Cowork `schedule` skill could do this today.

### 2. 67% Capacity Trigger for Memory Promotion
When MEMORY.md exceeds a threshold (~4000 chars), automatically scan for entries that are stable enough to promote to a vault file or compiled knowledge artifact. Currently Brien has to manually decide what to promote. This heuristic automates it.

### 3. USER.md / MEMORY.md Separation
Split auto-memory into:
- USER.md: who Brien is, preferences, timezone, workspace map (stable, rarely changes)
- MEMORY.md: what the system has learned this session/week (dynamic, changes frequently)
Reduces index bloat and makes the stable profile available without loading dynamic entries.

### 4. Vault Hygiene as Dashboard Section
Add to the enrichment dashboard: orphaned notes (persona files with no incoming references), stale memory entries (not referenced in 30+ days), oversized memory files. Automated weekly check.

## What Intent Already Does Better

### Compilation over Filing
Hermes writes raw observations to vault files. Intent's Knowledge Engine compiles raw material into structured artifacts with cross-references resolved and contradictions flagged. A filing cabinet vs. a compiled knowledge base.

### Trust Scoring and Autonomy
Hermes does what you say or doesn't. Intent evaluates every signal's trust score and routes to the appropriate autonomy level. This is the governance layer Hermes lacks entirely.

### 170 Expert Personas
Hermes has preferences.md (how the user likes things). Intent has 170 expert personas with voice profiles, reasoning chains, and intellectual genealogies. Different order of magnitude.

### Federation Boundaries
Hermes has Work/ and Personal/ folders. Intent has engagement-level federation with redaction at the tool level. The difference between folder-based separation and cryptographic projection.

## Cross-References
- Dex Horthy's 40% context rule relates to Tier 1 hot memory capacity management
- Rohit's Principle 7 (Memory as Architecture) describes the same tiered approach at enterprise scale
- Intent signals: SIG-029 (resilient retrieval pattern), SIG-033 (checkpointing)
