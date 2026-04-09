---
id: INT-011
title: "Add operator persona type + brien-operator first instance"
status: proposed
proposed_by: "brien"
proposed_date: 2026-04-09T05:04:00Z
accepted_date:
signals: [SIG-048, SIG-052]
specs: []
owner: "brien"
priority: next
product: notice
---
# Add operator persona type + brien-operator first instance

## Problem

The unified persona system at `Core/personas/` has 178 entities across three types: named-human (Torres, Cagan), archetype (Practitioner-Architect), and class (planned). There is NO persona type capturing the operator themselves — Brien's own flow patterns, decision postures, known failure modes, and corrective self-prompts as a reusable persona for self-directed agent cycles.

During self-directed development cycles (agents working without Brien present), there's no way to self-prompt "what would the operator do here?" because the operator isn't in the registry. Agents fall back to generic senior-engineer behavior instead of matching operator-specific preferences, lineage, and anti-patterns.

This was identified during the 2026-04-09 session as a concrete gap, with immediate use case in the panel-review primitive (INT-007).

## Desired Outcome

### New persona type: `operator`

Added to `Core/personas/registry/_schema.yaml`. Distinct from named-human (public thought leaders) and archetype (composite voices).

**Schema fields:**
- `flow_patterns`: typical cycle behaviors ("parallel by default", "discovery before implementation")
- `decision_postures`: how decisions are made at L1/L2/L3/L4 ("runs 4-gate reversibility check", "defaults to action")
- `tool_preferences`: canonical toolchain signatures
- `communication_style`: "visual analogies, system-design metaphors, first-principles > best-practices"
- `lineage`: named methodology ancestors the operator follows (Cagan, Torres, Patton, Petra, Seiden...)
- `known_failure_modes`: recurring pattern failures (e.g., "build-more reflex when panels say subtract-more", SIG-052)
- `corrective_prompts`: self-prompts that trigger when a failure mode is detected
- `escalation_signals`: when to pause and request human input (if not already present)
- `anti_patterns`: behaviors explicitly NOT wanted

### First instance: `brien-operator`

Derived from:
- `~/.claude/CLAUDE.md` (user profile, execution posture, behavioral rules)
- `memory/` (feedback entries about preferences)
- Session journals (cross-session patterns)
- This session (SIG-052: build-more reflex)

### Usage

- Referenced by panel-review primitive (INT-007) as one of the voices
- Loaded at session start for self-prompt calibration during self-directed cycles
- Used by Overwatch for alignment checks ("is this session aligned with operator patterns?")

## Evidence

- **SIG-048:** Team/operator self-persona gap (explicit Brien request)
- **SIG-052:** Subtract-before-build reflex — example of a pattern to capture
- Existing 178-persona library covers thought leaders but not self-operators

## Constraints

- New schema fields must not break existing named-human/archetype personas
- Operator personas are engagement-scoped OR core-scoped (federation rules apply)
- First instance (brien-operator) is core-scoped (not tied to any engagement)
- Must be versionable — operator personas evolve as the operator learns

## Governance model (COMMITTED per DEC-20260409-02 answer 3)

**Brien's decision:** "agent proposed with review, and here we can again introduce and use the panel."

### How operator persona updates work

1. **Agent proposes.** Any agent, observing the operator in a session, can propose an update to the operator persona. The proposal is a signal file in `.intent/signals/` with type `operator-persona-update`.

2. **Panel reviews.** Before acceptance, the update goes through a panel-review call (INT-007). Required voices:
   - **The operator in question** (self-persona voice — checks the update against its own known patterns)
   - **Org Design panel member** (Edmondson, always-on per INT-007 rules) — checks against psychological safety dimensions
   - **Relevant foundational voices** depending on what's being updated (e.g., if the update is about communication style, pull in Carmine Gallo + Nancy Duarte; if it's about decision patterns, pull in Kahneman + Rumelt)

3. **Operator ratifies.** After panel review, Brien (for brien-operator) either accepts, revises, or rejects the update. Rejections are logged as signals about what doesn't fit — these become learning data for the system.

4. **Versioned history.** Operator personas are versioned with a changelog. Old versions are preserved, never deleted. This documents the operator's evolution and creates a learning corpus.

### Why this is the first recursive use of panel-review

The panel-review primitive reviews Intent's own artifacts. Now it also reviews updates to the personas the panel uses. This is double-loop learning at the registry level: the system that scores trust is itself trust-scored by the system that scores trust.

### Operator persona lives at Core/personas/operators/

New subdirectory: `Core/personas/operators/` — distinct from `Core/personas/registry/` which holds named-humans, archetypes, and classes. The operator type has different governance (agent-proposed with panel review), different update cadence (after-session reflection), and different use cases (self-prompting during self-directed cycles). It deserves structural separation.

Brien-operator lives at `Core/personas/operators/brien.yaml` with versioned history at `Core/personas/operators/brien/versions/` if needed.

## Open Questions

- Is there a class-level operator persona that generalizes across operators (e.g., "practitioner-architect-operator") vs. individual files (`brien.yaml`)?
- How does the existing Practitioner-Architect archetype in Skills Engine relate? (Answer: the archetype describes an IDEAL practitioner pattern derived from thought leaders; the operator persona describes an ACTUAL operator's observable behavior. Complementary, not duplicative.)
- Post-v1: what does operator persona evolution look like over a year? Monthly updates? Quarterly? Only when triggered by specific patterns?

## Out of Scope

- Operator personas for other humans (wait until brien-operator proves out)
- Automated derivation from session data (manual authoring for v1)
- Integration with overwatch (comes after v1 exists)
