---
title: 03 Ws Ddr 099 Substrate Exposure Mcp Front Repo As Truth
type: framework
maturity: final
confidentiality: internal
reusability: adaptable
created: 2026-05-27
depth_score: 4
depth_signals:
  file_size_kb: 10.0
  content_chars: 10111
  entity_count: 0
  slide_count: 0
  sheet_count: 0
  topic_count: 0
  has_summary: 0
vocab_density: 0.30
---
# WS-DDR-099 — Substrate exposure via MCP-front + repo-as-truth composition

> **Routing note for Phase 2 (Code):** When filing, copy this DDR body into `/Users/brien/Workspaces/.context/DECISIONS.md` after WS-DDR-098, and add the index row:
> `| WS-DDR-099 | Substrate exposure via MCP-front + repo-as-truth composition | proposed | 2026-05-26 | 0.88 |`

```yaml
id: WS-DDR-099
type: decision
created: 2026-05-26
status: accepted
accepted_by: brien
accepted_at: 2026-05-26
confidence: 0.90
origin: human
related_closes:
  - D1: cloud (FastMCP/Workers) — matches recommendation
  - D2: read-only first — matches recommendation
  - D5-refined: tier-aware architecture Day 1, redaction-map authoring deferred to actual need (third option beyond the original D5 binary)
refinement_pattern: |
  Architecture commits to tier-aware substrate exposure on Day 1 — classification schema,
  scope-token mechanism, binary policy enforcement at the MCP server. Internal-tier
  substrate is queryable Day 1; engagement-tier substrate stays scope-locked until
  per-engagement redaction-maps are authored on demand (~30 min one-time per engagement).
  No future refactor needed; the deferred work is configuration, not code.
phase_1_shipping_target: ~2.5-3 weeks
related:
  - WS-DDR-025 (sibling-over-parent-child)
  - WS-DDR-079 (Conduit↔Witness OTel composition seam)
  - DEC-009 (Entire scoped as authoring provenance — supersedes DEC-007)
  - DEC-004 (file-native, git-tracked, OTel-compatible)
  - DEC-010 (intent-knowledge MCP scope extension — Intent-framework-local)
thread_hooks:
  - vt_id: VT-001
    relationship: serves
    rationale: "A coordination-discipline operating model at AI speed requires the canonical substrate to be reachable from any working surface, not bound to one machine. Substrate-as-sibling encodes the structural commitment at the reachability layer."
    declared_at: 2026-05-26
```

## Context

As of 2026-05-26, the canonical substrate of Brien's coherence stack (`.intent/` + `wiki/` + linked knowledge graph held in `library-index`) is reachable only when the desktop is online and the chat surface is at the desktop. When Brien is traveling, the chat surface has memory-fragments of the work, never the work itself — the substrate is structurally bound to one machine.

This collapses three distinct concerns into one:

- **Identity** (canonical state at time T)
- **Reachability** (who can read, from where)
- **Liveness** (is the source-of-truth process online?)

WS-DDR-025 (sibling-over-parent-child) commits the workspace to separating these concerns when separable mechanisms are available. The substrate-exposure question is the WS-DDR-025 principle applied at the surface-of-truth layer.

The 2026-05-26 audit (SIG-ENTIRE-SCOPE-2026-05-26 → DEC-009) sharpened a related distinction — authoring observability vs. running-system observability — and named the substrate as the place both observability paths' records land. Making the substrate reachable across surfaces is the load-bearing reachability commitment downstream of DEC-009.

## Decision

The substrate is exposed across surfaces via **MCP-front + repo-as-truth composition**:

- **Identity layer:** The repo (`theparlor/intent` + per-product repos containing `.intent/` directories) is the canonical source of truth. Git commit hashes are the identity. This is unchanged from DEC-004; the DDR commits to *not* reintroducing a sidecar database, even when adding a query surface.
- **Reachability layer:** The `intent-knowledge` MCP server (port 8004, today specced/CLI-pending per `ARCHITECTURE.md`) is the sibling of `intent-notice` / `intent-spec` / `intent-observe`, exposing query verbs over the substrate. Hosted on FastMCP Cloud / Cloudflare Workers at $0/mo, same infra family as the other three.
- **Liveness layer:** Decoupled from any single machine. The repo is durable via git's distributed model. The MCP server is stateless and serverless (Cloudflare Workers cold-start). Substrate is reachable whether or not any single machine is online.
- **Relevance + token-bound slicing:** `library-index` (BM25 + vector retrieval over 39k+ files) composes with the `intent-knowledge` MCP server as the relevance filter. Chat surfaces ask for slices; the MCP server returns top-N relevant chunks. The chat surface never sees the substrate raw.
- **Phase 1 = read-only.** Phase 2 adds write-back via MCP verbs that emit pull requests against the repo (PR-as-arbiter), not direct commits.

The **desktop demotes** from source-of-truth-and-single-point-of-failure to (a) primary authoring surface and (b) one reader of N.

## Alternatives considered

1. **Single mechanism — MCP server with a sidecar database.** Rejected. Decouples the queryable surface from the file-native, git-tracked truth, reintroducing the lock-in DEC-004 explicitly rejects. Adds a new state-management problem (sidecar vs. repo drift).
2. **Single mechanism — committed repo + hosted projection (GitHub Pages / Cloudflare Worker static).** Rejected as the *sole* mechanism. Static projection cannot do BM25+vector ranking, cannot do lineage traversal, cannot do shaped queries. Would still need an MCP server in front for chat-surface usability. Equivalent to choosing MCP+repo but at higher token-context cost.
3. **Sync per surface (mirror substrate locally to each consumer).** Rejected. Duplicates the staleness problem the substrate-exposure question was raised to solve. Reintroduces drift between surfaces. Stateful per-surface caches are themselves a distributed-state problem.
4. **Desktop-resident MCP server (no hosting upgrade).** Rejected. Fails the original problem statement — substrate unreachable when desktop offline. Acceptable as a fallback if the hosting question goes the other way (see Open Decision #1 in the Cowork handoff), but does not satisfy the load-bearing requirement that chat surfaces work while traveling.

## Rationale

- **Sibling-composition (WS-DDR-025).** The substrate is a sibling of the surfaces, not a child of any machine. Identity (repo), reachability (MCP), liveness (decoupled) become separately optimized layers. Each can be replaced or upgraded without touching the others.
- **Composes with existing infra.** The MCP server family already runs on FastMCP Cloud / Cloudflare Workers at $0/mo (`ARCHITECTURE.md` lines 303-307). Adding `intent-knowledge` completes the four-server family. No new hosting decision.
- **Composes with existing knowledge graph.** `library-index` already serves the BM25+vector role for the 39k+ file graph. Token-context burn is bounded at the server, not at the client.
- **Constraint-compatible.** FastMCP-Cloud-hosted MCP servers consumed via Anthropic's official MCP transport are user-owned endpoints, not third-party API routing — compatible with the Max-subscription / April-2026 routing-restriction constraint.
- **PR-as-arbiter for Phase 2 write-back** preserves DEC-003 (build in the open) and gives Brien a review surface for cross-surface writes.

## Consequences

- **Positive.** Chat surfaces stop being strangers when Brien travels. Substrate becomes addressable from any surface that can reach an MCP endpoint. The desktop's role becomes legible (authoring + one reader, not source-of-truth).
- **Positive.** Cross-product queries become possible at the same surface as per-product queries — "show me every decision across the portfolio about sibling-composition" is a single MCP call.
- **Positive.** Phase 2 write-back through PR opens a clean path for capture-from-anywhere without losing the authoring-trace discipline.
- **Negative (manageable).** Adds one more MCP server to the family's operational surface (deployment, health, monitoring). Mitigation: the infra is identical to the existing three; nothing structurally new.
- **Negative (managed by composition).** Latency introduced — chat surface → MCP → repo + library-index. Expected ~1s end-to-end, acceptable for human-pace queries. Aggressive caching at library-index handles the common case.
- **Risk.** If `library-index`'s API surface is not currently exposed in a form `intent-knowledge` can consume, that exposure becomes a sub-milestone of Phase 1. Falls inside the existing E3 track in `.intent/specs/2026-05-20-upgrade-plan.md`.
- **Phase 1 dependency (per D5-refined close).** Tier-aware architecture: classification schema (`.intent/classification.yaml`), scope-token mechanism in MCP client configs, and binary policy enforcement at every verb response (return absent if no scope match). This is what gets built Day 1 so engagement-tier light-up later is config-only.
- **Phase 2 / on-demand (deferred per D5-refined close).** Per-engagement redaction-map authoring, shaped-view substitution code, engagement event federation to Witness, inbound redaction. None of these requires re-architecting Day-1 code — they slot into the tier-aware enforcement point that already exists.

## Validation criteria

The decision is validated when:

1. A chat-surface Claude session, with no local access to the workspace, can answer "what does DEC-009 say?" by querying the `intent-knowledge` MCP endpoint.
2. The MCP server is deployed at `intent-knowledge.fastmcp.cloud/mcp` and operates at $0/mo cost.
3. `library-index` provides the relevance-filter composition for at least the `query` verb.
4. The desktop continues to function as the primary authoring surface unchanged (no breaking change to existing workflows).
5. Phase 2 write-back is shippable when ready — i.e., the Phase 1 design has not foreclosed it.

## Related decisions to file alongside

- `DEC-010` (Intent-framework-local) — extends intent-knowledge MCP scope to include substrate-query verbs.
- `DEC-011` (Intent-framework-local) — bin/intent-init scaffold (Track B sibling).

## Supersession / lineage

Does not supersede prior DDRs. Builds on WS-DDR-025 (the sibling-composition principle) and WS-DDR-079 (the existing example of "lock the composition seam before building"). Companion to DEC-009 (the two-observabilities frame that ratified upstream).
