---
title: "Federated knowledge base — Core is universal substrate, engagements are bounded instances"
id: DEC-INTENT-013
type: decision-atom
created: 2026-04-05
date_inferred: false
scope: Core/frameworks/intent — knowledge base federation model
status: ratified
ratified_at: 2026-04-05
ratified_by: "brien (2026-04-05; 4-gate pass: reversible / local / precedent / no info gap)"
gate_check:
  reversible: pass
  local: pass
  precedent: pass
  info_gap: pass
upstream_control_path: "Core/frameworks/intent/CLAUDE.md §Key Decisions #13; knowledge-engine/spec/federation.md"
catch_mechanism: "federation.md defines inherit-down, promote-up, never-leak-sideways rules; lint detects cross-engagement references"
pipeline_survival: "Directory topology (Core/ vs Work/) mirrors federation; survives reorganizations"
source: "2026-04-05"
---

# Decision: Federated knowledge base — Core is universal substrate, engagements are bounded instances

> Ratified 2026-04-05. All 4 autonomy-grant gates pass.

## Context

Brien's Knowledge Farm spans both universal knowledge (practitioner patterns, methodology theory) and engagement-specific knowledge (client domain models, confidential findings). Mixing them creates contamination and confidentiality risk. The federation model mirrors the existing Workspaces topology.

## Decision

Core knowledge = universal substrate (inheritable by any engagement). Engagement knowledge = bounded instances (inherit down from Core, promote up when generalized, never leak sideways to other engagements). Mirrors Workspaces topology (Core/ vs Work/).

## Scope

Governs knowledge artifact placement and cross-reference rules. Defined in `knowledge-engine/spec/federation.md`. Does not constrain signal flow within a single engagement.

## Alternatives Not Taken

| Alternative | Why not chosen | Reversibility if revisited |
|-------------|----------------|---------------------------|
| Single flat knowledge base | Confidentiality violations; engagement contamination | L2 — structural migration |
| Per-engagement siloed knowledge (no Core) | No shared learning across engagements | L3 |

## Reversibility

L3 — federation topology is encoded in directory structure and in `Workspaces/AGENTS.md` (placement resolver). Migration to a different topology requires coordinated update across placement resolver + federation spec.

## Ratification Action

`knowledge-engine/spec/federation.md` defines the federation rules. Placement resolver (`Workspaces/AGENTS.md`) enforces Core vs engagement boundaries. Three rules: inherit down, promote up, never leak sideways.
