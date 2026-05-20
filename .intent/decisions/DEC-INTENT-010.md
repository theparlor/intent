---
title: "Compilation over retrieval — knowledge base compiles understanding once"
id: DEC-INTENT-010
type: decision-atom
created: 2026-04-05
date_inferred: false
scope: Core/frameworks/intent — knowledge base access pattern
status: ratified
ratified_at: 2026-04-05
ratified_by: "brien (2026-04-05; 4-gate pass: reversible / local / precedent / no info gap)"
gate_check:
  reversible: pass
  local: pass
  precedent: pass
  info_gap: pass
upstream_control_path: "Core/frameworks/intent/CLAUDE.md §Key Decisions #10; knowledge-engine/spec/; reference/karpathy-synthesis/"
catch_mechanism: "LLM writes knowledge/ artifacts at compile time; LLM reads raw/ as read-only; lint flags orphaned raw/ without knowledge/ counterpart"
pipeline_survival: "Agent permission model (LLM reads raw/, writes knowledge/) enforces at tool-call level"
source: "2026-04-05; Karpathy synthesis research"
---

# Decision: Compilation over retrieval — knowledge base compiles understanding once

> Ratified 2026-04-05. All 4 autonomy-grant gates pass.

## Context

The dominant pattern for LLM knowledge access is RAG (retrieval-augmented generation) — retrieve relevant chunks at query time. An alternative is compilation: agent reads all source material once, compiles synthesized knowledge artifacts, and future agents read the compiled artifacts. Contradictions and cross-references are pre-resolved.

## Decision

The knowledge base compiles understanding once and keeps it current. Not RAG. Agents compile `raw/` → `knowledge/` artifacts. Cross-references are already resolved in the compiled artifacts. Contradictions are already flagged. Future agents read `knowledge/`, not `raw/`.

## Scope

Governs Layer 1 (Compiled Knowledge Base) access pattern. Does not constrain how agents use the compiled artifacts internally.

## Alternatives Not Taken

| Alternative | Why not chosen | Reversibility if revisited |
|-------------|----------------|---------------------------|
| RAG (retrieval on demand) | Cross-references not pre-resolved; contradictions surface at query time; no guarantee of completeness | L2 — architecture change |
| Agent reads raw/ each time | Redundant processing; inconsistent synthesis across sessions | L3 |
| Human-maintained knowledge base | Doesn't scale; brittle to source updates | L2 |

## Reversibility

L2 — switching to RAG would require removing compiled knowledge/ artifacts and adding vector store infrastructure. Significant architecture change.

## Ratification Action

Agent permission model: LLM reads `raw/` (never writes), writes `knowledge/`. `knowledge-engine/AGENTS.md` enforces this boundary. Lint detects orphaned raw/ files without knowledge/ counterparts.
