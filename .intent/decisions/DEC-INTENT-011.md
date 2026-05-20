---
title: "Double-loop learning — Observe updates domain understanding, not just execution"
id: DEC-INTENT-011
type: decision-atom
created: 2026-04-05
date_inferred: false
scope: Core/frameworks/intent — observe phase feedback architecture
status: ratified
ratified_at: 2026-04-05
ratified_by: "brien (2026-04-05; 4-gate pass: reversible / local / precedent / no info gap)"
gate_check:
  reversible: pass
  local: pass
  precedent: pass
  info_gap: pass
upstream_control_path: "Core/frameworks/intent/CLAUDE.md §Key Decisions #11; CLAUDE.md §Six bidirectional data flows (flows 5 and 6)"
catch_mechanism: "Observe phase event catalog includes domain-model-update events (Flow 5); observations/ directory feeds both Layer 1 and Layer 3"
pipeline_survival: "observations/ directory + Flow 5/6 data flow definitions persist in CLAUDE.md architecture"
source: "2026-04-05; Chris Argyris double-loop learning"
---

# Decision: Double-loop learning — Observe updates domain understanding, not just execution

> Ratified 2026-04-05. All 4 autonomy-grant gates pass.

## Context

Single-loop learning optimizes within existing assumptions (execution gets better at doing the same thing). Double-loop learning (Argyris) questions the assumptions themselves. An observe layer that only feeds back into spec/code quality (single-loop) can never detect when the underlying domain model is wrong.

## Decision

The Observe phase updates Layer 1 (domain understanding / Compiled Knowledge Base) via Flow 5, not just Layer 3 (execution) via Flow 6. Without double-loop, the system can only optimize, never question. Observations directory (`observations/`) feeds both flows.

## Scope

Governs the two feedback flows from Observe: Flow 5 (Observe → Knowledge, double-loop) and Flow 6 (Observe → Spec corpus, single-loop). Both flows are required for a complete observe phase.

## Alternatives Not Taken

| Alternative | Why not chosen | Reversibility if revisited |
|-------------|----------------|---------------------------|
| Single-loop only (Observe → Spec) | Can optimize wrong assumptions indefinitely | L3 — requires retroactive observations/ re-classification |
| No observe phase | No learning; system degrades over time | L2 |

## Reversibility

L3 — if double-loop update mechanism proves too expensive in practice, can defer Flow 5 to batch cycles. Single-loop still exists and is functional.

## Ratification Action

Flow 5 (Observe → Knowledge) and Flow 6 (Observe → Spec) defined in CLAUDE.md architecture. `observations/` directory created with `metrics/` and `incidents/` subdirectories. Argyris cited as intellectual foundation.
