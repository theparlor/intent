---
id: SIG-048
timestamp: 2026-04-09T04:44:00Z
source: conversation
confidence: 0.9
trust: 0.8
autonomy_level: L3
status: captured
cluster: panel-primitive
author: brien
related_intents: []
referenced_by: []
parent_signal:
---
# Team/operator self-persona missing from unified persona system

Brien's explicit request during 2026-04-09 session: *"we should add a signal that we need to develop team personas like for myself so that my behavior is converted to a usable player persona during self-directed development."*

The unified persona system (Core/personas/) has 178 entities across three types: named-human (thought leaders like Torres, Cagan), archetype (composites like Practitioner-Architect), and class (planned but not instantiated). There is NO persona type that captures the operator themselves — Brien's own flow patterns, decision postures, tool preferences, and behavioral signatures as a reusable persona for self-directed agent cycles.

## Why this matters

- During self-directed development cycles (agent working alone), there's no way to self-prompt "what would Brien do here?" because Brien isn't in the registry
- The gap means agents default to generic "senior engineer" behavior instead of matching operator-specific preferences (e.g., "visual thinker, storytelling-driven, product-first, Cagan/Torres/Patton/Petra lineage")
- Cross-session continuity suffers — agents can't reference a canonical operator persona, they have to reconstruct from CLAUDE.md on each session
- This is a new persona TYPE, not just a new entity in the existing types

## Required outcome

- New persona type: `operator` (distinct from named-human, archetype, class)
- Schema: flow patterns, decision postures, tool preferences, communication style, lineage, anti-patterns, escalation signals
- First instance: `brien-operator` derived from CLAUDE.md, memory/, session journal data
- Schema fields include: typical cycle behaviors, "how I think when X", known failure modes, recovery patterns
- Used for self-prompting during self-directed development cycles (complement to the 178 thought-leader personas used for spec-shaping)

## Relationship to Panel-as-a-service primitive (SIG-041)

The operator persona becomes one of the voices the panel can call. When an agent runs a panel review, one voice is "brien-operator" — used to check "would the operator accept this output, or would they push back?" This is a different use case than thought-leader critique.

## Trust Factors

- Clarity: 0.9 (explicit Brien request + clear gap identified)
- Blast radius: 0.2 (new schema + new instances, no existing flow breaks)
- Reversibility: 1.0
- Testability: 0.7 (can compare agent output with/without operator persona)
- Precedent: 0.8 (Cooper's personas done right, but applied to self)
