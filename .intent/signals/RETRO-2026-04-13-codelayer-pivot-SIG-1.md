---
id: RETRO-2026-04-13-codelayer-pivot-SIG-1
type: signal
category: pattern-opportunity
severity: medium
source: competitive-analysis
detected: 2026-04-13
topic: codelayer-pivot
related:
  - RETRO-2026-04-12-humanlayer-approval-SIG-1
  - SPEC-APPROVAL-GATE
---

# Staged Human Review Gates: Review Earlier, Not Later

## Signal

HumanLayer's pivot to CodeLayer (hlyr.dev/code) introduced a "Research → Plan → Implement" workflow where human review gates fire at the research and plan stages — NOT at the code stage. This inverts traditional code review to maximize human leverage at the highest-leverage points in the pipeline.

## Evidence

- CodeLayer's workflow: Research (human reviews) → Plan (human reviews) → Implement (agent executes)
- Their "Advanced Context Engineering" blog post positions this as the primary quality lever
- Their sub-agent isolation pattern (fresh context for search/discovery) prevents context pollution in parent sessions
- HumanLayer *abandoned* per-tool-call approval in favor of per-phase-gate review — the pivot itself is evidence that tool-level gates are less valuable than phase-level gates

## Connection to Intent

This is structurally isomorphic to Intent's loop:
- **Notice** (research) → human reviews signals → **Spec** (plan) → human reviews spec → **Execute** (implement) → agent runs
- Intent already places the spec-shaping protocol (4-persona interrogation) as the high-leverage gate
- The L0 approval gate we just built covers *external actions* within Execute — a different axis

## Implication

Two complementary gate systems:
1. **Phase gates** (already in Intent): Human reviews at Notice→Spec and Spec→Execute transitions. Spec-shaping protocol. Trust scoring.
2. **Action gates** (just built): L0 approval entities for external communication during Execute. The gate skill.

These are not redundant — they gate different things. Phase gates prevent building the wrong thing. Action gates prevent saying the wrong thing. CodeLayer's pivot validates that phase gates are higher leverage, but action gates remain necessary for irreversible external actions.

## Recommended Action

No immediate action — this validates our existing architecture. Intent already prioritizes phase gates (spec-shaping) over action gates (L0 approval). The L0 gate is a safety net, not the primary quality mechanism. Document this distinction in the gate skill's SKILL.md rationale section.

## Upstream Status

HumanLayer (the approval SDK) is effectively dead. CodeLayer (the IDE) is the company's new product. Apache 2 licensed, private beta, targeting 50-100 engineer enterprise teams. The approval entity patterns we extracted remain architecturally valid but will not receive upstream improvements.
