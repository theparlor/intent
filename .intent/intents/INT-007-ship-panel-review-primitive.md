---
id: INT-007
title: "Ship panel-review as a first-class skill (the async feedback primitive)"
status: proposed
proposed_by: "brien"
proposed_date: 2026-04-09T04:55:00Z
updated: 2026-04-09T06:45:00Z
accepted_date:
signals: [SIG-041, SIG-048, SIG-050, SIG-053]
related_decisions: [DEC-20260409-01, DEC-20260409-02]
specs: []
owner: "brien"
priority: now
product: notice
---

# v2 UPDATE (2026-04-09 session, after Brien's answers)

Per DEC-20260409-02 and the persona updates (Dunford/Gilad promoted to foundational, Aakash Gupta added as primary), the panel-review primitive now has a concrete default panel rotation:

## The foundational panel (always available, default to subset)

These 26 foundational voices form the standard pool for panel-review calls. The skill accepts a `panels` parameter that specifies which subset of foundational voices to dispatch, with named clusters as presets:

**Preset: `full-foundational`** — all 26 foundational voices in 8 panel clusters (the 2026-04-09 review pattern).

**Preset: `content-review`** — Dunford + Raskin + Miller + Godin (positioning); Cagan + Perri + Wille + Gilad + Aakash Gupta (product strategy); Torres + Patton + Blank + Fitzpatrick (discovery). Used for any content or site review.

**Preset: `architecture-review`** — Fowler + Majors + Kim + Forsgren + Skelton + Ford + Hohpe + Wardley. Used for architectural decisions and ADRs.

**Preset: `safety-review`** — Edmondson + Argyris + Schein + Kotter + Bridges + Smart. Used for any work touching psychological safety, change management, or adoption. Edmondson is ALWAYS the dominant voice.

**Preset: `decision-review`** — Kahneman + Tversky + Duke + Ariely + Thaler + Gilad + Rumelt + Martin. Used for any decision that involves trust scoring, evidence weighting, or cognitive bias.

**Preset: `operator-review`** — brien-operator + the operator's chosen complement panel. Used when the review is specifically about self-directed development cycles.

**Custom:** Any ad-hoc list of entity IDs from the persona registry.

## Always-on voices (cannot be excluded)

Three voices are ALWAYS in every panel call regardless of preset:
1. **Edmondson** — safety check on every recommendation
2. **Dunford** — category clarity check on every positioning or content move
3. **Kahneman** — cognitive bias check on every decision

These three are the minimum bar. If a panel-review call filters them out, the skill adds them back with a warning.

## New primary voices to integrate

From DEC-20260409-02:
- **Aakash Gupta** — included in content-review preset for contemporary practitioner-educator voice on AI-era PM craft
- **Itamar Gilad (promoted to foundational)** — included in content-review AND decision-review presets for evidence-based decision framework

## Safety-contract integration

Per INT-013, the panel-review skill MUST run a safety-contract-check pass on any output that evaluates human work:
- Does the output attribute failures to artifacts rather than humans?
- Does it protect disagreement as a valid input?
- Does it respect visibility scoping?
- Does it distinguish basic/complex/intelligent failures?

A panel review that fails the safety-contract-check cannot be published without explicit operator override, and the override itself is a signal.

---

# Original intent (v1)

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
