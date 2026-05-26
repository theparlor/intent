---
title: "Two products, not one — Intent (methodology) and Knowledge Engine (product) are distinct"
id: DEC-INTENT-014
type: decision-atom
created: 2026-04-06
date_inferred: false
scope: Core/frameworks/intent — product boundary definition
status: ratified
ratified_at: 2026-04-06
ratified_by: "brien (2026-04-06, DDR-005; 4-gate pass: reversible / local / precedent / no info gap)"
gate_check:
  reversible: pass
  local: pass
  precedent: pass
  info_gap: pass
upstream_control_path: "Core/frameworks/intent/CLAUDE.md §CRITICAL Two Products section; knowledge/decisions/DDR-005"
catch_mechanism: "CLAUDE.md has CRITICAL warning at top; session drift pattern is documented; agent handoff instructions check this first"
pipeline_survival: "CLAUDE.md §CRITICAL section is the first thing agents read; warning is prominent"
source: "2026-04-06, DDR-005"
---

# Decision: Two products, not one — Intent (methodology) and Knowledge Engine (product) are distinct

> Ratified 2026-04-06. All 4 autonomy-grant gates pass. See DDR-005.

## Context

The Knowledge Engine (compiled knowledge base system) was initially developed inside the Intent repo because Brien's domain knowledge overlaps with Intent's domain. This created confusion: agents worked on the Knowledge Engine when they meant to work on Intent methodology, and vice versa. The domain overlap is coincidental, not structural.

## Decision

Intent (methodology: Notice→Spec→Execute→Observe loop) and Knowledge Engine (product: raw/→knowledge/ compilation) are two distinct products. The Knowledge Engine is separable from Intent — can be used without Intent. Brien's Knowledge Farm is an instance of the Knowledge Engine, not a part of Intent. The domain overlap is coincidental.

## Scope

Governs all development work in theparlor/intent repo. The CRITICAL warning section at the top of CLAUDE.md is the enforcement surface for this decision.

## Alternatives Not Taken

| Alternative | Why not chosen | Reversibility if revisited |
|-------------|----------------|---------------------------|
| Single product (KE folded into Intent) | Creates architectural coupling; KE would be non-separable | L2 — KE extraction |
| Separate repos immediately | Premature; KE is still maturing; shared repo until clear boundary | L3 — repo split |

## Reversibility

L3 — if the Knowledge Engine reaches sufficient maturity, a repo split to `theparlor/knowledge-engine` is the natural next step. Current decision is to keep in shared repo with clear documentation.

## Ratification Action

CLAUDE.md §CRITICAL section added at the top of the file as the first thing agents read. DDR-005 recorded in `knowledge/decisions/`. Boundary table (which directory = which product) in CLAUDE.md. Engagement Farm is Brien's instance — not part of either product.
