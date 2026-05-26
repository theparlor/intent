---
title: "Three-layer architecture — compiled knowledge base + transformation OS + spec/code"
id: DEC-INTENT-009
type: decision-atom
created: 2026-04-05
date_inferred: false
scope: Core/frameworks/intent — core architectural model
status: ratified
ratified_at: 2026-04-05
ratified_by: "brien (2026-04-05; 4-gate pass: reversible / local / precedent / no info gap)"
gate_check:
  reversible: pass
  local: pass
  precedent: pass
  info_gap: pass
upstream_control_path: "Core/frameworks/intent/CLAUDE.md §Key Decisions #9; CLAUDE.md §Three-Layer Architecture; reference/karpathy-synthesis/"
catch_mechanism: "Architecture diagram in CLAUDE.md; six bidirectional data flows coupling layers; Knowledge Engine spec enforces layer 1 contracts"
pipeline_survival: "Directory structure (raw/, knowledge/, .intent/) mirrors the three layers; survives all refactors"
source: "2026-04-05"
---

# Decision: Three-layer architecture — compiled knowledge base + transformation OS + spec/code

> Ratified 2026-04-05. All 4 autonomy-grant gates pass.

## Context

Intent needed a clear architectural model to avoid conflating the knowledge substrate (what we know about the domain) with the methodology loop (how we work) with the code output. The Karpathy pattern (compiled knowledge base) provided the Layer 1 model.

## Decision

Intent prescribes three independent but bidirectionally coupled layers: (1) Compiled Knowledge Base — `raw/` sources → `knowledge/` artifacts; (2) Transformation OS — the notice→spec→execute→observe engine in `.intent/`, `spec/`; (3) Software Spec and Code — generated specs, contracts, running code. Six bidirectional data flows couple the layers.

## Scope

Governs directory structure, agent read/write permissions per layer, six data flow definitions. Does not govern Knowledge Engine as a separate product (see DEC-INTENT-014).

## Alternatives Not Taken

| Alternative | Why not chosen | Reversibility if revisited |
|-------------|----------------|---------------------------|
| Two layers (knowledge + loop) | Loses distinction between methodology and output | L3 |
| Single-layer (all in .intent/) | Collapses compiled knowledge into work artifacts; contamination risk | L2 |
| RAG-based knowledge retrieval | Retrieval on demand vs compiled understanding; see DEC-INTENT-010 | L2 |

## Reversibility

L3 — directory structure is baked into CLI tools and agent instructions. Migration possible but requires coordinated update.

## Ratification Action

Directory structure (`raw/`, `knowledge/`, `.intent/`) mirrors the three layers. `knowledge-engine/AGENTS.md` defines Layer 1 contracts. Six data flows documented in CLAUDE.md.
