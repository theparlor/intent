---
id: INT-007
title: "Ship panel-review as a first-class skill (the async feedback primitive)"
status: proposed
proposed_by: "brien"
proposed_date: 2026-04-09T04:55:00Z
accepted_date:
signals: [SIG-041, SIG-048, SIG-050]
specs: []
owner: "brien"
priority: now
product: notice
---
# Ship panel-review as a first-class skill — the async feedback primitive

## Problem

During the 2026-04-09 site review exercise, 8 independent persona panels (48 voices) produced structured, high-quality critique in parallel in roughly 2 minutes. Brien's observation after reading the output: **this IS the product**. The panel dispatch pattern is more concrete, more shippable, and more immediately valuable than the Notice→Spec→Execute→Observe loop itself.

None of the 8 panels caught this insight — because they were busy being the panel. The meta-finding had to come from Brien reviewing the synthesis. This is a significant advance that was hiding inside the exercise.

Currently the pattern exists only as an ad-hoc prompt template. It needs to become a first-class skill callable by any agent in any cycle.

## Desired Outcome

A new skill `panel-review` lives at `Core/products/skills-engine/skills/claude-code/meta/panel-review/` with:

1. **Input contract:**
   - `target`: URL, file path, or spec ID to review
   - `panels`: one of
     - `all` (8 default panels)
     - `subset` (named panel list)
     - `custom` (ad-hoc cluster)
   - `depth`: `quick` (1500 words/panel) | `thorough` (3000 words/panel)
   - `output_format`: `raw` (8 critique docs) | `synthesis` (cross-cutting findings) | `visual` (HTML review doc like review-2026-04-09.html)

2. **Execution:**
   - Dispatches panel agents in parallel (one per panel) using the Agent tool
   - Each panel agent embodies its persona cluster and returns structured critique
   - Output writer synthesizes cross-cutting findings using the agreement heatmap pattern

3. **Byproducts:**
   - Every panel critique becomes one or more signal files in `.intent/signals/`
   - Cross-cutting findings become candidate intents
   - Agreement heatmap is stored as a reusable asset

4. **Callability:**
   - Any agent can call it during any cycle
   - Specifically: after spec-shaping, after execution, after content drafts, before major decisions
   - Makes Intent's loop genuinely asynchronous — agents get real external feedback without waiting for human availability

## Evidence

- **SIG-041:** Panel-as-async-feedback-loop is the genuine breakthrough from this exercise
- **SIG-048:** Operator persona (brien-operator) becomes one of the voices callable by the panel
- **SIG-050:** Double-loop learning is single-loop in practice — the "Challenge the Intent" pass is a specialized panel call
- Session proof: the 2026-04-09 review produced 8 parallel critiques + visual synthesis in ~2 minutes

## Constraints

- Must use the skills-engine platform (claude-code renderer)
- Must produce signal files as output (integrates with Intent's event stream)
- Must not require new infrastructure — uses existing Agent tool + persona library
- Must be composable: called inside other skills (spec-shaping, overwatch, etc.)
- Input schema must support both "canned panels" (the 8 we just used) and "build your own panel"

## Open Questions

- Should the panel catalog be stored in `Core/personas/panels/` as a new entity type?
- How does the operator persona (SIG-048) integrate — is it always included, or opt-in?
- Should the skill auto-generate signal files, or return them as structured data for the calling agent to write?
- Panel review of a panel review: does that converge or diverge?

## Out of Scope (for v1)

- Automated triggering (no cron, no hooks — explicit invocation only in v1)
- Novel panel generation (use the 8 we have first; expand later)
- Voice synthesis across panels (synthesis is LLM-generated, not algorithmic)

## Cross-references

- `Core/products/skills-engine/` — where the new skill lives
- `Core/personas/` — voice library the panels draw from
- `docs/review-2026-04-09.html` — reference implementation and output format
