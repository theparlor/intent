---
title: "Four-product framing — Notice, Spec, Execute, Observe are distinct products"
id: DEC-INTENT-008
type: decision-atom
created: 2026-03-28
date_inferred: false
scope: Core/frameworks/intent — product architecture framing
status: ratified
ratified_at: 2026-03-28
ratified_by: "brien (Cowork session 2026-03-28; 4-gate pass: reversible / local / precedent / no info gap)"
gate_check:
  reversible: pass
  local: pass
  precedent: pass
  info_gap: pass
upstream_control_path: "Core/frameworks/intent/CLAUDE.md §Key Decisions #8; spec/product-roadmap.md four-product roadmap"
catch_mechanism: "Each product has its own maturity state in roadmap; independent development paths visible in status"
pipeline_survival: "Four-product framing encoded in CLAUDE.md, roadmap, and site IA"
source: "Cowork session 2026-03-28"
---

# Decision: Four-product framing — Notice, Spec, Execute, Observe are distinct products

> Ratified 2026-03-28. All 4 autonomy-grant gates pass.

## Context

The Notice → Spec → Execute → Observe loop could be framed as a single monolithic product or as four distinct products with independent maturity. Distinct product framing enables independent roadmaps, clearer maturity assessment, and separate adoption paths.

## Decision

Notice, Spec, Execute, and Observe are four distinct products, each with its own maturity level and roadmap. Current maturity: Notice (Operational), Spec (Conceptual), Execute (Defined), Observe (Schema-Ready).

## Scope

Governs product roadmap structure, maturity reporting, site IA. Does not prevent the four products from sharing infrastructure (CLI suite, MCP server).

## Alternatives Not Taken

| Alternative | Why not chosen | Reversibility if revisited |
|-------------|----------------|---------------------------|
| Single monolithic product | Hides maturity variation; harder to communicate partial adoption | L4 |
| Two products (Notice+Spec vs Execute+Observe) | Arbitrary split; doesn't match natural ownership boundaries | L4 |

## Reversibility

L4 — framing change requires roadmap and site IA update.

## Ratification Action

`spec/product-roadmap.md` has four-product roadmap with distinct maturity states. `intent-status roadmap` renders ASCII four-product maturity view.
