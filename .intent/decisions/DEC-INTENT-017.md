---
title: "Retroactive enrichment is suggested, not automatic cascade"
id: DEC-INTENT-017
type: decision-atom
created: 2026-04-06
date_inferred: false
scope: Core/frameworks/intent — knowledge enrichment trigger model
status: ratified
ratified_at: 2026-04-06
ratified_by: "brien (2026-04-06; 4-gate pass: reversible / local / precedent / no info gap)"
gate_check:
  reversible: pass
  local: pass
  precedent: pass
  info_gap: pass
upstream_control_path: "Core/frameworks/intent/CLAUDE.md §Key Decisions #17; knowledge-engine/spec/"
catch_mechanism: "Lint detects enrichment opportunities and surfaces as signals; no auto-cascade code path exists"
pipeline_survival: "Signal-based enrichment pattern is the only wired path; cascade would require new code"
source: "2026-04-06"
---

# Decision: Retroactive enrichment is suggested, not automatic cascade

> Ratified 2026-04-06. All 4 autonomy-grant gates pass.

## Context

When new knowledge is compiled, it may make existing compiled artifacts stale or enrichable. The question was whether to automatically recompile affected artifacts (cascade) or to surface the opportunity as a signal for human review and on-demand execution.

## Decision

Lint detects recompilation opportunities and surfaces them as signals. Enrichment is on-demand — Brien or an agent decides when to execute. No automatic cascades. This prevents runaway recompilation chains and maintains human oversight on what gets refreshed.

## Scope

Governs the Knowledge Engine enrichment trigger model. Does not constrain how frequently Brien manually triggers enrichment.

## Alternatives Not Taken

| Alternative | Why not chosen | Reversibility if revisited |
|-------------|----------------|---------------------------|
| Automatic cascade on any knowledge update | Runaway recompilation; blast radius unknown; defeats signal-based governance | L3 — wire cascade code |
| No lint detection (fully manual) | Enrichment opportunities silently missed; staleness accumulates | L4 — add lint |

## Reversibility

L4 — can add automatic cascade as an optional mode without removing signal-based path. Suggested-first is the default; cascade could be opt-in.

## Ratification Action

Lint tool detects enrichment opportunities and writes signals to `.intent/signals/`. No automatic cascade code path. On-demand execution is the only wired path.
