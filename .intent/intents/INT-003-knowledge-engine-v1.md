---
id: INT-003
title: "Ship Knowledge Engine v1: ingest/query/lint operations against Brien's Knowledge Farm"
status: proposed
proposed_by: brien
proposed_date: 2026-04-06T10:00:00Z
accepted_date:
signals: [SIG-025, SIG-026, SIG-027, SIG-028, SIG-029, SIG-030]
specs: []
owner: brien
priority: now
product: cross-cutting
---
# Ship Knowledge Engine v1: ingest/query/lint against Brien's Knowledge Farm

## Problem

The Knowledge Engine has a complete schema (AGENTS.md), artifact templates, federation model, retroactive enrichment spec, and redaction spec — but no executable operations. The first ingest was performed manually (agent writing files by hand). There's no CLI tool, no MCP server, no automated pipeline. Brien can't drop a source into `raw/` and have the system compile it.

Six signals (SIG-025 through SIG-030) produced the architecture. Now the architecture needs to produce working software.

## Desired Outcome

Brien can:
1. Drop a source file into `raw/` and run `intent-knowledge ingest` — the system reads the source, reads the knowledge index, creates/updates knowledge artifacts, updates cross-references, appends to log
2. Ask a question via `intent-knowledge query "question"` — the system reads the index, synthesizes an answer with citations, offers to file new artifacts
3. Run `intent-knowledge lint` — the system scans for contradictions, orphans, staleness, coverage gaps, and outputs suggested signals
4. These operations work against Brien's Knowledge Farm (Subaru, ASA, F&G engagement data), not just Intent's own dogfood
5. The MCP server exposes these as tools for Claude Code/Desktop

## Evidence

- SIG-025: Karpathy pattern validated at ~100 articles / ~400K words with no vector DB
- SIG-027: Boundary between Intent/KE/Farm clarified — KE is a separable product
- SIG-028: Retroactive enrichment requires working ingest to recompile prior knowledge
- SIG-029: Redaction requires working query that can apply projections
- SIG-030: Naming corrected — this is a compiled knowledge base, not a wiki
- First manual ingest (2026-04-05) produced 16 knowledge artifacts from 3 sources — proof the compilation model works

## Constraints

- Must work as both CLI and MCP server (consistent with Intent's existing dual-interface pattern)
- Must follow AGENTS.md schema exactly — templates, frontmatter, cross-reference conventions
- Must support federation (engagement AGENTS.md extending Core) from day one
- Ingest must be idempotent — running it twice on the same source should not create duplicates
- Operations must emit events to `.intent/events/events.jsonl` (consistent with Intent's event system)

## Open Questions

- Should this be a new MCP server (`intent-knowledge` on port 8004) or extend `intent-notice` (since knowledge lint feeds the Notice phase)?
- Should the CLI be `intent-knowledge` (new tool) or subcommands on existing tools?
- How does ingest handle non-markdown sources (PDFs, images, CSVs) in raw/?
- What's the right batch size for retroactive enrichment — one engagement at a time, or all at once?
- How does the redaction projection work at the MCP tool level — separate tools or a `--projection` flag?
