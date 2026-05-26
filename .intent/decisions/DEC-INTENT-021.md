---
title: "12-factor agent pattern integration — 5 gaps resolved, event catalog expanded"
id: DEC-INTENT-021
type: decision-atom
created: 2026-04-13
date_inferred: false
scope: Core/frameworks/intent — agent execution patterns and event catalog
status: ratified
ratified_at: 2026-04-13
ratified_by: "brien (2026-04-13; 4-gate pass: reversible / local / precedent / no info gap)"
gate_check:
  reversible: pass
  local: pass
  precedent: pass
  info_gap: pass
upstream_control_path: "Core/frameworks/intent/CLAUDE.md §Key Decisions #21; knowledge/decisions/DDR-006; event schema"
catch_mechanism: "DDR-006 in knowledge/decisions/; event catalog updated from 15→22 events; checkpoint protocol in execution layer"
pipeline_survival: "Event catalog is the wired artifact; checkpoint protocol survives session cycles"
source: "2026-04-13; HumanLayer 12-factor-agents manifesto; DDR-006"
---

# Decision: 12-factor agent pattern integration — 5 gaps resolved, event catalog expanded

> Ratified 2026-04-13. All 4 autonomy-grant gates pass. See DDR-006.

## Context

HumanLayer published a 12-factor-agents manifesto identifying patterns for reliable agent systems. Reviewing it against Intent's architecture identified 5 gaps that needed resolution to make Intent's agent execution patterns production-grade.

## Decision

Adopt 5 gap resolutions from the 12-factor-agents analysis: (1) pause/resume protocol — execution checkpoints via `execution.paused`/`execution.resumed` events; (2) human-contact-as-capability — distinct from governance gates; (3) LLM-as-judge — semantic evaluation in the Observe phase; (4) error-retry-escalate — platform-level standard; (5) state philosophy — stateful system / stateless invocations. Event catalog expanded from 15→22 events. DDR-006 records the full analysis.

## Scope

Governs the Execute phase patterns and event catalog. The 5 gap resolutions are now first-class primitives in Intent's execution model.

## Alternatives Not Taken

| Alternative | Why not chosen | Reversibility if revisited |
|-------------|----------------|---------------------------|
| Ignore 12-factor-agents (no integration) | Leaves known production-grade patterns unimplemented | L4 — can remove any individual pattern |
| Full adoption of all 12 factors (not just 5) | 7 remaining factors did not identify gaps in Intent's existing architecture | L4 |

## Reversibility

L4 — each of the 5 patterns is independently revertible. Event catalog is append-only (additions don't break existing consumers).

## Ratification Action

DDR-006 in `knowledge/decisions/`. Event catalog expanded to 22 events. Checkpoint protocol (`execution.paused`/`execution.resumed`) in execution layer. `methodology/meta/approval-gate.md` defines the human-contact-as-capability boundary.
