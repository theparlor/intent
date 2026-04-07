---
id: INT-006
title: "Extend Intent framework: entity lifecycle, INGEST type, contribution contracts, trust modifiers"
status: accepted
proposed_by: brien
proposed_date: 2026-04-06T18:00:00Z
accepted_date: 2026-04-06T18:00:00Z
signals: [SIG-032, SIG-033, SIG-034, SIG-035]
specs: [SPEC-003]
owner: brien
priority: now
product: intent-methodology
---
# Extend Intent Framework: Entity Lifecycle, INGEST Type, Contribution Contracts, Trust Modifiers

## Problem

The persona system design exposed four gaps in the Intent framework:
1. No entity lifecycle primitive — durable entities that accumulate state have no home in the work ontology
2. No INGEST intent type — acquiring and registering new entities isn't covered by the eight existing types
3. No contribution contract type — verifying that entity composition enriches without degrading has no contract pattern
4. Trust scoring ignores development infrastructure — worktree/blue-green patterns should modify reversibility and blast radius scores

## Desired Outcome

1. The work ontology includes an entity primitive with lifecycle states (created → active → enriched → stale → deprecated → archived)
2. INGEST joins the intent taxonomy as the ninth type, with a default skill chain for entity acquisition
3. CONTRIBUTION joins the contract types as the fifth type, verifiable through before/after diff
4. The trust scoring formula includes a deployment context modifier that accounts for worktree isolation, branch strategy, and blue/green patterns

## Evidence

- SIG-032: Brien identified that worktree development should raise trust scores — blast radius mitigation through infrastructure
- SIG-033: Persona design revealed no home for durable entities in the work ontology
- SIG-034: "Ingest this human" had no matching intent type in the taxonomy
- SIG-035: Archetype enrichment requires a new contract type to verify composition quality

## Constraints

- Entity lifecycle must be orthogonal to work ontology — entities and work items coexist
- INGEST must be idempotent and handle disambiguation as a required substep
- Contribution contracts must be direction-aware (upward only)
- Trust modifier must be verifiable (actually in a worktree, not just claimed)
- All changes must be backward-compatible with existing 31 signals and 4 intents
