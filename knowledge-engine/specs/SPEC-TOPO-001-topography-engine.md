---
title: SPEC-TOPO-001 — Topography Engine (REDIRECT STUB)
id: SPEC-TOPO-001
type: redirect
created: 2026-04-18
updated: 2026-04-18
depth_score: 2
depth_signals:
  file_size_kb: 2.8
  content_chars: 2156
  entity_count: 0
  slide_count: 0
  sheet_count: 0
  topic_count: 0
  has_summary: 0
vocab_density: 0.93
status: moved
canonical_location: Core/products/topography/spec/topography-design.md
moved_reason: "Promoted from Intent/KE specs directory into own product directory per WS-DDR-024 (four-engine naming) and the sibling-composable architecture default (WS-DDR-025). Topography is a sibling at the planning position of Brien's four-engine stack, not a subsystem of the Knowledge Engine."
related_ddrs:
  - WS-DDR-024
  - WS-DDR-025
---
# SPEC-TOPO-001 — Topography Engine (MOVED)

> **This spec has been promoted into its own product directory.**
>
> **Canonical location:** [`Core/products/topography/spec/topography-design.md`](../../../../products/topography/spec/topography-design.md)
>
> **Why the move:** Per WS-DDR-024, Topography is the planning engine of Brien's four-engine stack (Lore / Cast / Forge / Topography), not a subsystem of the Knowledge Engine. Per WS-DDR-025, sibling-composability is the architectural default — Topography composes with Lore, Cast, Forge, Intent, and Loom at declared interface seams rather than being contained by any of them. The canonical spec lives with the product, not under the KE specs directory.

## What lives at the canonical location

- Full spec content (§1 Purpose through §10 Traceability)
- Frontmatter with `architecture: sibling-composable`, `pipeline_position: planning`, `port_interface: topography-planning-port`, `known_siblings: [Loom, Linear, Notion, Jira, Asana, ...]`
- DoR / DoD tables (5 DoR + 5 DoD)
- COMPACT step definition with Loom-composition seam
- Coherence score formula + publication shape
- Handoff protocol with `produced:` / `referenced:` / `siblings_observed:` fields
- Traceability from features to 2026-04-18 pressure-test ledger §8 evidence

## What remains here

Nothing load-bearing. This stub exists only so that inbound links from `session-ledger/LEDGER-20260418-pressure-test.md`, `coherence-engineering/spec/primary-session-2026-04-18.md`, and `.context/DECISIONS.md` WS-DDR-024 continue to resolve to something that points readers to the canonical path.

## Companion artifacts at the canonical product directory

| Artifact | Path |
|----------|------|
| Product manifest | `Core/products/topography/INTENT.md` |
| Canonical spec | `Core/products/topography/spec/topography-design.md` |
| Decision log | `Core/products/topography/.intent/decisions.md` |
| First signal | `Core/products/topography/.intent/signals/SIG-TP-001.md` |
| Directory guide | `Core/products/topography/CONTEXT.md` |
| Product README | `Core/products/topography/README.md` |
