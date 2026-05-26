---
title: "Engagement rollout order — Subaru → F&G → ASA → Cargill → Footlocker"
id: DEC-INTENT-015
type: decision-atom
created: 2026-04-06
date_inferred: false
scope: Core/frameworks/intent — Knowledge Farm deployment sequence
status: ratified
ratified_at: 2026-04-06
ratified_by: "brien (2026-04-06; 4-gate pass: reversible / local / precedent / no info gap)"
gate_check:
  reversible: pass
  local: pass
  precedent: pass
  info_gap: pass
upstream_control_path: "Core/frameworks/intent/CLAUDE.md §Key Decisions #15; CLAUDE.md §Decided Architecture table"
catch_mechanism: "[unknown — prose did not record a catch mechanism for rollout order drift]"
pipeline_survival: "Rollout order recorded in decisions.md and CLAUDE.md"
source: "2026-04-06"
---

# Decision: Engagement rollout order — Subaru → F&G → ASA → Cargill → Footlocker

> Ratified 2026-04-06. All 4 autonomy-grant gates pass.

## Context

Brien's Knowledge Farm spans multiple active consulting engagements. Installing `.intent/` scaffolds and knowledge compilation across all at once would scatter focus. A rollout order was needed to prioritize where to start.

## Decision

Rollout the Knowledge Engine to Brien's engagements in this order: Subaru first (most data, highest learning opportunity), then F&G, ASA, Cargill, Footlocker.

## Scope

Governs the order of `.intent/` scaffold installation and knowledge compilation for Brien's consulting engagements. Does not govern timeline (which is demand-driven).

## Alternatives Not Taken

| Alternative | Why not chosen | Reversibility if revisited |
|-------------|----------------|---------------------------|
| ASA first | Less data volume than Subaru | L4 — reorder |
| Simultaneous all-engagement rollout | Scatter-focus; harder to learn from first installation | L4 |

## Reversibility

L4 — rollout order is a sequencing preference. Can reorder at any point.

## Ratification Action

Rollout order recorded in CLAUDE.md §Decided Architecture table. Subaru is the first install target.
