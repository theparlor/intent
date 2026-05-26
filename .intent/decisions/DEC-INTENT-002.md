---
title: "Methodology first, tool second"
id: DEC-INTENT-002
type: decision-atom
created: 2026-03-28
date_inferred: false
scope: Core/frameworks/intent — GTM and build strategy
status: ratified
ratified_at: 2026-03-28
ratified_by: "brien (Cowork session 2026-03-28; 4-gate pass: reversible / local / precedent / no info gap)"
gate_check:
  reversible: pass
  local: pass
  precedent: pass
  info_gap: pass
upstream_control_path: "Core/frameworks/intent/CLAUDE.md §Key Decisions #2; spec/product-roadmap.md"
catch_mechanism: "Staged GTM framing in roadmap prevents premature tooling investment; interview gate before tooling"
pipeline_survival: "Encoded in product-roadmap.md phase sequence; survives session cycles"
source: "Cowork session 2026-03-28"
---

# Decision: Methodology first, tool second

> Ratified 2026-03-28. All 4 autonomy-grant gates pass.

## Context

Early development risked building tooling before validating the methodology. Brien is a solo practitioner — highest-leverage move is content and interviews, not code. Needed a clear sequencing principle.

## Decision

Validate with practitioners before building software. Stage the GTM: thought leadership (manifesto + case studies) → methodology product (playbook + workshops) → tooling (conditional on validation).

## Scope

Governs sequencing of all Intent development phases. Does not govern the Knowledge Engine product separately.

## Alternatives Not Taken

| Alternative | Why not chosen | Reversibility if revisited |
|-------------|----------------|---------------------------|
| Tooling first | Premature investment without methodology validation | L3 — sunk tooling cost |
| Simultaneous methodology + tooling | Dilutes focus, risks building wrong tool | L3 |

## Reversibility

L3 — if 5 in-depth interviews reveal strong tooling demand before methodology is validated, pivot is possible but requires re-scoping the roadmap. GTM timeline may be optimistic for solo practitioner.

## Ratification Action

Established three-stage GTM order in product roadmap. Interview gate (5 teams) is the mandatory unlock for tooling investment.
