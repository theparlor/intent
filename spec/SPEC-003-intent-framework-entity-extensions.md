---
title: "Intent Framework Extensions: Entity Lifecycle, INGEST Type, Contribution Contracts, Trust Modifiers"
id: SPEC-003
created: 2026-04-06 18:00:00+00:00
depth_score: 4
depth_signals:
  file_size_kb: 7.6
  content_chars: 7392
  entity_count: 0
  slide_count: 0
  sheet_count: 0
  topic_count: 0
  has_summary: 0
vocab_density: 0.14
status: approved
intent: INT-006
contracts:
  - CON-008
  - CON-009
  - CON-010
  - CON-011
completeness: 0.80
agent_readiness: L2
---
# SPEC-003: Intent Framework Entity Extensions

## Overview

Four extensions to the Intent framework, motivated by the persona system dogfood. Each is independently implementable and backward-compatible with existing signals, intents, and specs.

## Extension 1: Entity Lifecycle Primitive

### Schema Addition

Entities are a new first-class concept in the work ontology, alongside signals/intents/specs/contracts:

```yaml
# .intent/entities/ENT-NNN-slug.md frontmatter
id: ENT-NNN
type: entity
entity_type: string         # persona | knowledge-artifact | dossier | archetype | (extensible)
name: string
lifecycle: enum             # created | active | enriched | stale | deprecated | archived
created: datetime
updated: datetime
canonical_path: string      # Where this entity's authoritative data lives (outside .intent/)
signals: [SIG-NNN]          # Signals that created or modified this entity
specs: [SPEC-NNN]           # Specs that defined this entity's structure
trace_id: string            # OTel trace for provenance
```

### Lifecycle Transitions

```
created → active       # After initial population (substance exists)
active → enriched      # After corpus expansion or re-assessment
enriched → enriched    # Repeated enrichment (most common steady state)
active|enriched → stale  # Freshening overdue (lint-detected)
stale → active|enriched  # After freshening
any → deprecated       # Entity replaced or no longer relevant
deprecated → archived  # Removed from active rendering
```

### Integration Points

- **Notice**: Entity staleness detected by lint → emits signal
- **Spec**: Entity creation/modification driven by specs
- **Execute**: Agents create/enrich entities per specs
- **Observe**: Entity state changes emit events (`entity.created`, `entity.enriched`, `entity.stale`)

### Storage

Entity metadata lives in `.intent/entities/`. The entity's actual content lives at `canonical_path` (e.g., `Core/personas/registry/pawel-huryn.yaml`). The `.intent/` record is a pointer + lifecycle tracker, not a content store.

## Extension 2: INGEST Intent Type

### Taxonomy Addition

Add to `spec/intent-taxonomy.md`:

```yaml
INGEST:
  description: "Acquire raw material → transform to structured knowledge → register durable entity"
  default_chain:
    - identify          # Parse input, disambiguate, create identity record
    - harvest           # Fetch from primary channels, store in corpus
    - assess            # Extract substance, populate index, score originality
    - render            # Generate downstream renderings (persona files, voice configs)
    - connect           # Update relationship graph, cross-references
    - schedule          # Register freshening channels
  target_types:
    Person: persona-intake
    Company: company-dossier + entity-register
    Domain: knowledge-compilation
    Source: corpus-ingestion
  produces: entity      # KEY DIFFERENCE from other types: produces durable entity, not report
  idempotent: true      # Re-ingesting updates, never duplicates
```

### Compound Intents

- INGEST+EVALUATE: Ingest a source AND assess whether it's worth subscribing to (the Huryn use case)
- INGEST+RESEARCH: Ingest an entity AND produce a research report about it
- INGEST+POSITION: Ingest a competitor AND position against them

## Extension 3: CONTRIBUTION Contract Type

### Contract Schema Addition

Add to `spec/contracts.md`:

```yaml
contribution:
  description: "Verifies that adding entity A to composite B enriches B along declared dimensions without degrading existing content"
  fields:
    source_entity: string       # Entity contributing (e.g., mary-barra)
    target_composite: string    # Entity being enriched (e.g., fortune-50-ceo-mfg)
    dimensions: [string]        # Which substance fields should be enriched
    non_regression: [string]    # Which fields must not degrade (default: all existing)
  verification:
    method: before_after_diff
    steps:
      1: Snapshot target composite substance block (BEFORE)
      2: Execute contribution (add source entity's content)
      3: Snapshot target composite substance block (AFTER)
      4: For each declared dimension: AFTER must contain new content not in BEFORE
      5: For each non_regression field: AFTER content must be superset of BEFORE content
    pass_condition: "All declared dimensions enriched AND no non-regression fields degraded"
```

## Extension 4: Trust Scoring Deployment Context Modifier

### Formula Modification

Current: `trust = clarity × 0.30 + (1/blast_radius) × 0.20 + reversibility × 0.20 + testability × 0.20 + precedent × 0.10`

Extended: Same formula, but `reversibility` and `blast_radius` accept a deployment context modifier before scoring:

```yaml
deployment_context:
  type: enum                # in_place | branch | worktree | blue_green
  modifiers:
    in_place:
      reversibility_bonus: 0.0
      blast_radius_multiplier: 1.0
    branch:
      reversibility_bonus: 0.1
      blast_radius_multiplier: 0.5
    worktree:
      reversibility_bonus: 0.2
      blast_radius_multiplier: 0.25
    blue_green:
      reversibility_floor: 0.95
      blast_radius_multiplier: 0.1
```

Applied: `effective_reversibility = min(1.0, base_reversibility + deployment_bonus)` and `effective_blast_radius = base_blast_radius × deployment_multiplier`.

### Verification

The deployment context must be **verifiable**, not claimed:
- `branch`: `git branch --show-current` ≠ main/master
- `worktree`: working directory is inside a git worktree (`git rev-parse --show-toplevel` differs from main repo)
- `blue_green`: defined by project config (`.intent/config.yml`) — must reference a parallel environment with its own test suite

## Contracts

### CON-008: Entity Lifecycle Consistency
An entity's lifecycle state must be consistent with its content:
- `created`: has identity, may lack substance
- `active`: has substance.voice at minimum
- `enriched`: has corpus_path with content newer than last assessment
- `stale`: freshening overdue per channel frequency
- `deprecated`: must have deprecation reason in metadata

**Verification**: For each entity, check lifecycle state against content presence. Report inconsistencies.

### CON-009: INGEST Idempotency
Running INGEST twice on the same entity must produce exactly one registry entry, one corpus directory, and two processing-log entries. The second run enriches; it does not duplicate.

**Verification**: INGEST entity, count files. INGEST same entity again, count files. Registry count unchanged. Corpus has updated content. Processing log has two entries.

### CON-010: Contribution Non-Regression
After executing a contribution contract, no existing content in the target composite may be removed or reduced. New content may be added; existing content must be preserved or expanded.

**Verification**: Snapshot before/after. Set diff (BEFORE - AFTER) must be empty for all non-regression dimensions.

### CON-011: Trust Modifier Verification
A deployment context modifier may only be applied when the context is machine-verifiable. If `git rev-parse` cannot confirm worktree isolation, the modifier must not be applied (falls back to `in_place` baseline).

**Verification**: Apply worktree modifier from non-worktree context. Must fail gracefully and use baseline scores.
