---
title: Cowork Phase 1 Deliverables — Substrate Exposure + Witness/Entire Composition
created: 2026-05-26
updated: 2026-05-26
depth_score: 4
depth_signals:
  file_size_kb: 6.1
  content_chars: 5589
  entity_count: 0
  slide_count: 0
  sheet_count: 0
  topic_count: 0
  has_summary: 0
vocab_density: 0.36
session_origin: Cowork
session_target: Claude Code (Phase 2 filing)
owner: brien
status: ready-for-phase-2-filing
brien_closes_recorded: 2026-05-26 (4 explicit + D4 default-publish)
brien_overrides: "D5-refined (tier-aware Day 1, redaction-map authoring deferred — third option beyond the original D5 binary)"
parent_handoff: ../2026-05-26-substrate-exposure-and-witness-entire-composition.md
parent_audit_signal: ../../.intent/signals/2026-05-26-entire-scope-audit-and-observability-delta.md
ratifies: DEC-009
phase_2_dispatch_brief: 07-phase-2-code-dispatch-brief.md
---
# Cowork Phase 1 — Staged Deliverables

This directory contains the Phase 1 (thinking) output of the 2026-05-26 substrate-exposure + Witness/Entire-composition handoff. Phase 2 (Code, Claude Code session) will file these into framework canon per the routing notes below.

## What's here

| File | Track | What it is | Phase 2 destination (proposed) |
|---|---|---|---|
| `01-track-a-substrate-exposure-architecture.md` | A | Architecture brief: how chat surfaces reach the substrate when the desktop is offline or unreachable | `Core/frameworks/intent/spec/substrate-exposure-architecture.md` (new) + index entry in `ARCHITECTURE.md` |
| `02-track-b-spawn-a-product-runbook.md` | B | Composition runbook: how any new product climbs Tier 0 → 1 → 2 → 3 | `Core/frameworks/intent/playbooks/spawn-a-product.md` (new; `playbooks/` already exists) |
| `03-WS-DDR-099-substrate-exposure-mcp-front-repo-as-truth.md` | A | Workspaces-level DDR (placement + governance scope; substrate sibling-composes across surfaces) | append to `/Users/brien/Workspaces/.context/DECISIONS.md` with index row, status `proposed` |
| `04-DEC-010-intent-knowledge-mcp-scope-extension.md` | A | Intent-framework-local decision (intent-knowledge MCP server scope explicitly covers `.intent/` + `wiki/` substrate exposure) | append to `Core/frameworks/intent/spec/decision-log.md` |
| `05-DEC-011-intent-init-scaffold-script.md` | B | Intent-framework-local decision (the `bin/intent-init` scaffold) | append to `Core/frameworks/intent/spec/decision-log.md` |
| `06-open-decisions-for-brien.md` | both | The five open decisions, with recommendations, ready for Brien's close | not a filed artifact — read by Brien, then close-out edits land per his rulings |

## Routing rationale (WS-level vs. Intent-framework-local)

Per §3 of the handoff: WS-level DDR if it touches placement/governance; Intent-framework-local DEC if it's a framework architecture call.

- **WS-DDR-099** is WS-level because it commits the workspace to a sibling-composition pattern across surfaces (per WS-DDR-025) — that is placement and governance, applies to *all* products in the portfolio, not just the Intent framework.
- **DEC-010 and DEC-011** are Intent-framework-local because they extend the existing MCP server family and add a new scaffold script — framework architecture inside `Core/frameworks/intent/`.

## Brien's closes (2026-05-26)

- **D1 Hosting:** Cloud (FastMCP / Cloudflare Workers) — matches recommendation.
- **D2 R/W scope:** Read-only first — matches recommendation.
- **D3 Witness adapter timing:** Ship runbook now, Tier 2 conditional — matches recommendation.
- **D4 Publish two-observabilities post:** Defaults to YES via 7-day rule.
- **D5 Scope of "any product":** **OVERRIDE + REFINEMENT — D5-refined.** Brien picked a third option beyond the original D5 binary: design the substrate-exposure architecture tier-aware from Day 1 (classification schema, scope-token mechanism, binary enforcement at the MCP server) but ship only internal-tier query Day 1. Engagement substrate is scaffolded with full classification metadata but federation to Witness and chat-surface query are deferred until Phase 2 / on-demand (when per-engagement redaction-maps are authored). The structural commitment is honored without paying the redaction-authoring cost upfront. Phase 1 target: ~2.5-3 weeks.

All staged deliverables (01, 02, 03, 05, 06) have been re-threaded for D5-refined. The Phase 2 dispatch brief (`07-phase-2-code-dispatch-brief.md`) carries the full filing instruction set for Code, including the D5-refined paragraph.

## What Phase 2 should NOT do

- Do not flip the WIT-004 #5 (`engine/adapters/entire-io.py`) stub to "implemented" — Track B's runbook explicitly marks Tier 2 federation as "live when stub lands" so the dependency is honored.
- Do not modify the rendered Observe-leg surface (`observe.html`, `observe/README.md`) — Phase 1 audit already confirmed those are correct.
- Do not weaken the tier-aware architecture into a future-add — Brien's D5-refined close commits to building classification schema + scope-token mechanism + binary policy enforcement Day 1. That is the load-bearing commitment. What IS deferred (per-engagement redaction-maps, shaped-view code, engagement-tier Witness federation) is configuration and content work, not architectural code.

## Two-observabilities continuity

Both deliverables preserve the DEC-009 frame:

- **Authoring path** (Entire, session-traces, prompt→commit provenance) is what Track B scaffolds at Tier 0.
- **Running-system path** (OTel/Grafana/Tempo/Mimir/Loki via `observe/`) is what Track B climbs to at Tier 3.

Substrate exposure (Track A) is *neither* of these — it is the **reachability layer** for the canonical records the two observability paths feed and produce. The substrate (`.intent/` + `wiki/`) is the place both paths' outputs live; exposing it across surfaces is what makes chat-surface Claude not-a-stranger.

## Reading order

For Brien:
1. `06-open-decisions-for-brien.md` — the five questions you need to close.
2. `01-track-a-substrate-exposure-architecture.md` — the architecture brief.
3. `02-track-b-spawn-a-product-runbook.md` — the composition runbook.
4. The three DDRs only if you want to inspect the load-bearing decision form.

For the Phase 2 Code agent:
1. Read this README first.
2. Wait for Brien's closes on `06-open-decisions-for-brien.md`.
3. File per the routing table above, in dependency order: DDRs → architecture brief → runbook.
