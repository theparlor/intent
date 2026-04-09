---
id: INT-007
title: "Ship panel-review as a first-class skill (the async feedback primitive)"
status: v1.0-shipped
proposed_by: "brien"
proposed_date: 2026-04-09T04:55:00Z
updated: 2026-04-09T22:00:00Z
accepted_date: 2026-04-09T06:45:00Z
v1_shipped_date: 2026-04-09T22:00:00Z
signals: [SIG-041, SIG-048, SIG-050, SIG-053]
related_decisions: [DEC-20260409-01, DEC-20260409-02]
specs: []
shipping_artifacts:
  - Core/products/skills-engine/platforms/claude-code/meta/panel-review/SKILL.md
  - Core/products/skills-engine/platforms/claude-code/meta/panel-review/panel-presets.yaml
  - Core/products/skills-engine/platforms/claude-code/meta/panel-review/panel-voice-template.md
  - Core/products/skills-engine/platforms/claude-code/meta/panel-review/SHIP-NOTES-v1.md
owner: "brien"
priority: now
product: notice
---

# v3 UPDATE (2026-04-09 later session — v1.0 SHIPPED)

Panel-review skill v1.0 operational and committed to theparlor/skills-engine.
The v0.1 scaffold (same-day morning) has been fully rewritten and joined by
two new sibling files (panel-presets.yaml, panel-voice-template.md) plus a
SHIP-NOTES doc capturing the v1.1 deferred backlog.

## What shipped (v1.0)

1. **6 operational presets** in `panel-presets.yaml` with verified voices —
   full-foundational (8 panels), content-review (3), architecture-review (2),
   safety-review, decision-review, operator-review. Every entity_id verified
   against `Core/personas/registry/` before commit. Four voices referenced
   in the v0.1 scaffold (Raskin, Miller, Farley) were not in the registry
   and were substituted with adjacent voices (Duarte, Humble) rather than
   stubbing new registry entries on the fly.

2. **Concrete Agent dispatch pattern** — each panel launches as a Task
   sub-agent in parallel. Voices are INLINED into the sub-agent prompt
   (not loaded by file read inside the sub-agent) to avoid file-read
   failures and focus context. Default model is Opus per voice fidelity
   concerns (Sonnet over-accepts critique framing per
   memory/feedback_model_selection.md).

3. **Phase 0 preflight** with always-on voice injection (Edmondson,
   Dunford, Kahneman), voice diversity heuristic warning, registry
   validation, safety contract file loading with fallback.

4. **Phase 2 synthesis** with semantic dedup (keyword clustering for v1.0;
   embedding-based replacement deferred to v1.1), severity classification
   (critical / structural / gap / single-panel / disagreement), agreement
   ranking, consensus strength extraction.

5. **Phase 3 safety contract check** as a HARD GATE. Four yes/no questions
   against the synthesis: Promise 1 (attribution to artifacts, not humans),
   Promise 6 (disagreement protected), Promise 8 (voice diversity),
   generative mode (every weakness paired with strengthening). 1-2 fails
   = block and require override; 3+ fails = unconditional block + re-run.

6. **Candidate signal byproducts** — one signal per cross-cutting finding,
   written to target's `.intent/signals/` at `trust: 0.2`.

7. **Error handling table** — 10 failure modes mapped to responses
   including partial-review flagging, missing voice graceful degrade,
   malformed return detection, unreachable target hard fail.

8. **Budget guidance table** — cost estimates per preset (tokens + wall
   clock) with scheduling advice.

9. **Caller contract locked at v1.0** — Brien-only via `/panel-review`.
   Intent-orchestrator auto-invoke explicitly deferred to v1.1.

## Persona critique applied before ship

Spec passed through three voices inline before writing code:

- **Torres:** "Who calls this in v1.0? You said 'Brien + orchestrator'.
  Orchestrator integration is unspecified." → Correction: v1.0 caller
  locked to Brien-only. Orchestrator deferred to v1.1.
- **Dunford:** "'Async feedback primitive' is still vague — lead with
  the concrete value prop." → Correction: frontmatter description
  sharpened to name the concrete job (1-8 parallel panels, 2-5 min wall
  clock, structured findings + synthesis + signals, substitute-when-
  human-unavailable not replace-human).
- **brien-operator (self):** "Safety check placed where it actually
  protects?" → Correction: voice diversity heuristic moved to Phase 0
  preflight (warn early), safety contract check stays in Phase 3
  (block late). Gate-level check earlier than previously drafted.

## Validation criteria for v1.0

Per DEC-20260409-01, the ship is validated when:
- [ ] `panel-review full-foundational thorough` runs end-to-end on
  `intent-site/docs/v2-draft/pitch.html` without manual intervention
- [ ] Re-run panel review produces agreement scores that can be compared
  to the 2026-04-09 baseline (F1 no target user, F3 category confusion,
  F4 reader-not-hero, F10 psych safety)
- [ ] F1 drops from 6/8 → ≤1/8 panels
- [ ] F3 drops from 5/8 → ≤1/8 panels
- [ ] F10 drops from 1/8 → 0/8 panels (psych safety explicitly addressed
  in v2-draft with safety-contract page)
- [ ] Safety contract check passes on synthesis output (zero Promise 1
  violations, Promise 6 disagreements visible, ≥3 role functions,
  100% weakness-recommendation pairing)

If validation criteria fail, reconvene and double-loop per DEC-20260409-01
consequences section.

## What's NOT shipped in v1.0 (deferred backlog)

See `SHIP-NOTES-v1.md` in the skill directory for the full v1.1 backlog.
Highest-priority deferred items:

1. **Visual HTML output format** — requires design-system-exact renderer
   matching `intent-site/docs/review-2026-04-09.html`
2. **Intent-orchestrator auto-invoke** — requires orchestrator-side changes
3. **Operator-persona-update recursive governance** — panel-review is
   supposed to gate operator persona updates per DEC-20260409-02 answer 3,
   but the recursive governance wiring is not in v1.0
4. **Embedding-based semantic dedup** — replaces v1.0 keyword clustering
   for cross-cutting finding identification
5. **Challenge-the-Intent preset** — per SIG-050, questions the premise
   not the execution

## Lineage and attribution

- Marty Cagan (product critique as discipline)
- Teresa Torres (confirmation bias check, evidence-before-opinion)
- April Dunford (category clarity as always-on review dimension)
- Amy Edmondson (safety-first posture as always-on)
- Daniel Kahneman (cognitive bias check as always-on)
- Richard Rumelt (diagnosis before prescription)
- Architecture Review Board pattern (enterprise IT field practice)
- Multi-persona prompting (LLM agent community field practice)
- Brien (the architecture, the operator integration, the "panel IS the
  product" 2026-04-09 insight)

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
