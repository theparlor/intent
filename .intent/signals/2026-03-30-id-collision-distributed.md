---
id: SIG-022
title: Sequential signal IDs will collide in distributed multi-agent environments
type: friction
source: conversation
source_context: IDs SIG-006 through SIG-011 collided with existing site signals during Cowork session
date: 2026-03-30
status: active
cluster: schemas
autonomy_level: L1
tags: [ids, distributed, collision, schema, infrastructure]
---

# SIG-022: Sequential signal IDs will collide in distributed multi-agent environments

## Observation

During this session, new signals were created with IDs SIG-006 through SIG-011 in the local `.intent/signals/` directory. Those IDs were already in use on the live signals.html dashboard (SIG-001 through SIG-015). This happened because:

1. Two surfaces (local files, live site) maintain independent ID sequences
2. No coordination mechanism exists between them
3. Sequential counters assume a single writer

This is a preview of a much larger problem: when multiple agents (signal-capture running on Haiku, enrichment running on Sonnet, a CLI capture, a Slack integration) all generate signals concurrently, sequential IDs guaranteed to collide.

## Current ID Scheme

`SIG-NNN` — zero-padded sequential integer, scoped to nothing. No namespace, no origin, no timestamp component.

## Failure Modes

- **Concurrent agents**: Two signal-capture agents both read "next ID = 016", both write SIG-016
- **Multi-surface**: Local `.intent/signals/`, live site, MCP server in-memory store all have independent counters
- **Cross-team**: Team A's SIG-042 means something completely different from Team B's SIG-042
- **Merge conflicts**: Git-backed storage with multiple writers creates frontmatter ID collisions

## Design Considerations

- IDs should be **globally unique without coordination** (no central counter)
- IDs should carry **provenance** (who/what generated this)
- IDs should be **human-readable** enough for conversation ("that signal Brien captured yesterday about the API")
- IDs should sort **temporally** (newest signals findable by ID ordering)
- The scheme should work for ALL entity types (SIG, INT, SPEC, CON, ATOM), not just signals

## Candidate Approaches

1. **UUID v7** — Timestamp-ordered, globally unique, but opaque (`019506a1-...`)
2. **ULID** — Like UUID v7 but base32-encoded, sortable, more readable (`01H5A3...`)
3. **Namespaced sequential** — `{team}.SIG-{NNN}` (e.g., `parlor.SIG-042`) — still needs per-team coordination
4. **Composite** — `{team}-{date}-{short-hash}` (e.g., `parlor-20260330-a7f3`) — unique enough, human-readable
5. **Hierarchical** — `{intent}.{signal}` (e.g., `INT-003.SIG-042`) — ties signal to intent but breaks for unattached signals

## Implication

The schema spec for all entity types needs an ID strategy decision before multi-agent deployment. This blocks SIG-016 (multi-agent MCP architecture) at Phase 3+.

## Relates To

- SIG-016 (multi-agent architecture — multiple writers)
- SIG-018 (cloud hosting — stateless servers need coordination-free IDs)
