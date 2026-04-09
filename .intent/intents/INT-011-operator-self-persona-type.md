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

## Open Questions

- Where does brien-operator live in the registry? `Core/personas/operators/brien/` vs `Core/personas/registry/brien-operator.yaml`?
- How are updates triggered? After-session reflection? Manual curation? Agent-proposed changes?
- Is there a class-level operator persona that generalizes (e.g., "practitioner-architect-operator") vs individual (`brien-operator`)?
- How does this relate to the existing Practitioner-Architect archetype in Skills Engine?

## Out of Scope

- Operator personas for other humans (wait until brien-operator proves out)
- Automated derivation from session data (manual authoring for v1)
- Integration with overwatch (comes after v1 exists)
