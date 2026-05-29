---
title: 04 Dec 010 Intent Knowledge Mcp Scope Extension
type: framework
maturity: final
confidentiality: internal
reusability: adaptable
created: 2026-05-27
depth_score: 4
depth_signals:
  file_size_kb: 6.1
  content_chars: 5923
  entity_count: 0
  slide_count: 0
  sheet_count: 0
  topic_count: 0
  has_summary: 0
vocab_density: 0.34
---
# DEC-010 — intent-knowledge MCP scope extended to substrate exposure

> **Routing note for Phase 2 (Code):** When filing, append this decision to `Core/frameworks/intent/spec/decision-log.md` immediately after DEC-009.

## Decided

2026-05-26

## Context

`Core/frameworks/intent/ARCHITECTURE.md` (line 107) defines `intent-knowledge` (port 8004) with verbs `ingest`, `query`, `lint` — per SPEC-001 and DDR-005. The CLI implementation is pending per Gap 7.1 / track E3 in `.intent/specs/2026-05-20-upgrade-plan.md`.

The 2026-05-26 Cowork Phase 1 brief on substrate exposure (`handoff/cowork-phase1-2026-05-26/01-track-a-substrate-exposure-architecture.md`) identifies `intent-knowledge` as the natural host for cross-surface substrate exposure verbs. Two options exist:

- **(a)** Build a new MCP server (intent-substrate, port 8005) dedicated to substrate exposure.
- **(b)** Extend `intent-knowledge`'s scope to cover substrate exposure, treating substrate query as a specialization of knowledge query.

This decision picks (b).

## Decision

`intent-knowledge` MCP server's scope is extended to explicitly include **cross-surface substrate exposure**. The verb set is broadened beyond `ingest`/`query`/`lint` to cover:

| Verb | Purpose | Bound |
|---|---|---|
| `query(text)` | Top-K relevant chunks via BM25+vector (library-index composition) | K configurable, default 10, max 25 |
| `get(entity_id)` | Single entity by canonical ID (SIG-NNN, INT-NNN, SPEC-NNN, DEC-NNN, WS-DDR-NNN) | One entity per call |
| `list(type, filter)` | Entity list shaped as title+id+timestamp+status (not full body) | Default 20, max 50 |
| `lineage(signal_id)` | Backward + forward lineage chain (depth 3) | Bounded by graph traversal |
| `freshness(path)` | Last-modified + last-render state | Single path |
| `ingest` (existing) | Per SPEC-001 / DDR-005 | unchanged |
| `lint` (existing) | Per SPEC-001 / DDR-005 | unchanged |

The server composes with `library-index` for the `query` verb's BM25+vector ranking. `get`/`list`/`lineage`/`freshness` read directly from the repo file tree.

**Phase 1 (this DEC's scope):** read-only verbs only. Write-back verbs (`capture_signal`, `propose_intent`) are deferred to a Phase 2 decision once auth + redaction + conflict design lands.

**Deployment:** `intent-knowledge.fastmcp.cloud/mcp` on FastMCP Cloud free tier or Cloudflare Workers, completing the four-server family alongside intent-notice / intent-spec / intent-observe (per ARCHITECTURE.md lines 303-307).

## Alternatives considered

- **(a) New dedicated `intent-substrate` server (port 8005).** Rejected. Creates two servers whose verbs would significantly overlap (a `query` on knowledge is structurally a `query` on substrate; the substrate *is* the knowledge corpus). Splitting violates the principle that the four-server family maps to the four loop phases plus knowledge — a fifth server breaks the elegance of the four-phase model.
- **(c) Defer the entire question; ship intent-knowledge with only `ingest`/`query`/`lint`, leave substrate exposure as a future track.** Rejected. The substrate-exposure problem is the load-bearing reason to prioritize the intent-knowledge CLI implementation in the first place (it is the forcing function). Deferring loses the motivating use case.

## Rationale

- **`intent-knowledge` already owns the knowledge-graph cross-cutting layer** (ARCHITECTURE.md line 108: "Cross-cutting (Layer 1)"). Substrate query is the natural specialization of knowledge query — the substrate *is* a knowledge corpus with extra structure (canonical IDs, lineage, freshness state).
- **The four-server family stays clean.** Notice / Spec / Observe / Knowledge maps to Notice / Spec / Execute+Observe / cross-cutting. Adding substrate exposure to Knowledge maintains the symmetry.
- **library-index composition is identical** whether substrate exposure is on intent-knowledge or a sibling server. Picking intent-knowledge avoids duplicating the composition seam.
- **Phase 1 scope is tight** — five new read verbs + library-index composition. Phase 2 write-back is gated separately on Brien's close of the read/write-scope open decision.

## Consequences

- **Positive.** Substrate exposure is delivered via the existing four-server architecture, not a new product. Operational surface area unchanged.
- **Positive.** The intent-knowledge MCP server's "specced; CLI pending" status (ARCHITECTURE.md line 111) gets a concrete shipping target with a clear motivating use case.
- **Manageable cost.** Five new verbs vs. three originally specced — moderate increase in server surface. All five are read-only; complexity is bounded.
- **Risk.** library-index API exposure to intent-knowledge is the one structural unknown. If library-index does not currently expose a usable Python/HTTP API, that exposure becomes a sub-milestone. Falls inside the E3 track already.

## Validation criteria

This decision is validated when:

1. `intent-knowledge` MCP server is deployed at `intent-knowledge.fastmcp.cloud/mcp`.
2. The five read verbs are callable from a chat-surface client.
3. The `query` verb composes correctly with library-index's relevance filter.
4. Token-context burn stays bounded — no single call returns more than one entity body or > N shaped summaries.
5. The four-server family at $0/mo is preserved (no new hosting bill).

## Related

- WS-DDR-099 (substrate exposure mechanism — Workspaces-level placement & governance)
- DEC-009 (Entire scoped as authoring provenance)
- DEC-004 (file-native, git-tracked, OTel-compatible)
- ARCHITECTURE.md lines 107-111, 303-307
- `.intent/specs/2026-05-20-upgrade-plan.md` Gap 7.1 / track E3
- SPEC-001 (intent-knowledge spec, per ARCHITECTURE.md reference)

## Supporting evidence

`/Users/brien/Workspaces/Core/frameworks/intent/handoff/cowork-phase1-2026-05-26/01-track-a-substrate-exposure-architecture.md`
