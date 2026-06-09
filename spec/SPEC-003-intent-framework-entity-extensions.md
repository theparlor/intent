---
title: "Intent Framework Extensions: Entity Lifecycle, INGEST Type, Contribution Contracts, Trust Modifiers"
id: SPEC-003
created: 2026-04-06 18:00:00+00:00
updated: 2026-05-29
depth_score: 4
depth_signals:
  file_size_kb: 17.9
  content_chars: 17613
  entity_count: 0
  slide_count: 0
  sheet_count: 0
  topic_count: 0
  has_summary: 0
vocab_density: 0.06
status: approved
intent: INT-006
ratified_by: WS-DDR-101
ratified_date: 2026-05-29
contracts:
  - CON-008
  - CON-009
  - CON-010
  - CON-011
  - CON-012
  - CON-013
  - CON-014
  - CON-ENTITY-DEDUP
  - CON-ENTITY-ONBOARD
  - CON-ENTITY-DISPOSITION-ORTHOGONALITY
completeness: 0.95
agent_readiness: L2
---
# SPEC-003: Intent Framework Entity Extensions

## Overview

Five extensions to the Intent framework, motivated by the persona system dogfood. Each is independently implementable and backward-compatible with existing signals, intents, and specs.

## Extension 1: Entity Lifecycle Primitive

> **Status: RATIFIED** as a first-class Intent primitive per **WS-DDR-101** (2026-05-29) — a **sibling** of the work-ontology (WS-DDR-025), generalized from Cast's two-axis lifecycle (WS-DDR-071). The original single-axis `lifecycle` enum was amended to the two-axis `pipeline × disposition` shape (the one substantive amendment); the storage model, integration points, and CON-008 are kept and generalized. Cast's live registry is the reference instantiation. Source proposal: `Core/products/cast/.intent/assessments/2026-05-29-intent-entity-lifecycle-primitive-proposal.md`.

### What an entity is

An **entity** is a durable noun the system keeps understanding over time — a persona, an archetype, a dossier, a compiled knowledge artifact. Unlike a work item (promoted toward *done*, then no longer a live concern), an entity is *created*, *accumulates state* across an open-ended life, *persists* (steady state is *existing*, not *being-finished*), and is *superseded/deprecated but usually preserved*, not deleted. That is why it cannot live inside the work-ontology: it is a peer at a different pipeline position, composing with work at the `produces: entity` seam (Extension 2, INGEST).

### Schema Addition

Entities are a first-class concept, sibling to signals/intents/specs/contracts:

```yaml
# .intent/entities/ENT-{ulid}-slug.md frontmatter
# The .intent/ record is a POINTER + lifecycle tracker, NOT a content store.
id: ENT-{ulid}              # ULID per Key Decision #20 (NOT the legacy ENT-NNN
                            #   sequential counter SIG-022 retired)
type: entity
entity_type: string         # persona | archetype | dossier | knowledge-artifact | (extensible)
                            #   The discriminator — declares which value-enums apply.
name: string
canonical_path: string      # Authoritative data location, OUTSIDE .intent/

# --- State: TWO orthogonal axes (the WS-DDR-071 generalization) ---
pipeline: enum              # ADVANCEMENT. "How far through intake/maturation?"
                            #   Monotonic (no regressions), exactly one terminal state.
                            #   VALUES are entity_type-specific (see per-type profiles).
disposition: enum           # EDITORIAL. "How should consumers treat this now?"
                            #   Independent of pipeline; free to move any direction.
                            #   (Cast's `usage` axis, renamed type-neutral.)

# --- Provenance ---
created: datetime
updated: datetime
signals: [SIG-...]          # Signals that created or mutated this entity
specs: [SPEC-...]           # Specs that defined its structure
trace_id: string            # OTel trace — ties entity life into Observe
caused_by: [EVT-...]        # OPTIONAL — Witness lineage, if the event store is wired
```

### Two axes, one machine — per-type profiles

The framework owns the *rules*; each `entity_type` owns the *vocabulary*. A type registers a profile declaring its enum values and transitions:

| `entity_type` | `pipeline` values (advancement) | `disposition` values (editorial) |
|---|---|---|
| **persona** (named-human) | `candidate → stub → draft → ready-for-assess → harvest-complete → assess-complete → active` | `eligible / quote-only / archival / deprecated / restricted` |
| **archetype** | `candidate → synthesizing → synthesis-complete → active` | `eligible / archival / deprecated` |
| **dossier** (company) | `candidate → drafting → active` | `eligible / stale-flagged / archival` |
| **knowledge-artifact** | `candidate → compiled → active` | `current / superseded / archival` |

Framework-owned invariants (the shared machine):
- **`pipeline` is monotonic** — advancement only, no regressions.
- **`pipeline` has exactly one terminal state** (conventionally `active`). Steady-state existence is `active`, not "done."
- **`disposition` moves freely** — editorial judgment is reversible; demote and re-promote at will.
- **Demotion never regresses `pipeline`** — an editorially-retired entity stays `pipeline: active`; retirement is expressed on `disposition` (`archival`/`deprecated`). See CON-ENTITY-DISPOSITION-ORTHOGONALITY.
- **Provenance is required** — every entity carries `signals`, `specs`, `trace_id`.

### The `candidate` entry state + admission hooks

`candidate` is the canonical first `pipeline` state for every `entity_type` — the single front door — distinct from Cast's `proposed`/`stub` (which describe *scaffold readiness*, not *citizenship readiness*). A candidate is a nominee not yet admitted, which might duplicate an existing entity. Two contract-backed hooks govern the door:

```
candidate ──(dedup passes + onboarding complete)──▶ <first post-admission state> ──▶ … ──▶ active
    │
    └──(dedup finds an existing entity)──▶ MERGE-INTENT against the incumbent
                                            (never a silent second entity)
```

- **CON-ENTITY-DEDUP** — on `candidate` creation, check for an existing entity of the same `entity_type` with a matching identity key (name + alias-normalized form). On match, the candidate does NOT advance; it raises a merge-intent. (CON-009 / INGEST `idempotent: true` pulled forward to the entry gate — write-through dedup; the chain_audit dedup sweep is the catch-net.)
- **CON-ENTITY-ONBOARD** — a `candidate` advances only when its profile's minimum-admission criteria are met (persona: identity block + ≥1 source; archetype: ≥2 `source_humans`). The entry-gate analogue of a DoR.

### Lifecycle Transitions

```
(work-ontology INGEST emits)              → candidate
candidate → <first post-admission state>    # CON-ENTITY-DEDUP + CON-ENTITY-ONBOARD pass
… → active                                  # advancement complete (terminal pipeline state)
active, disposition: eligible ⇄ archival ⇄ deprecated …   # editorial; never regresses pipeline
candidate → MERGE-INTENT                    # dedup found an incumbent
```

### Integration Points

- **Notice**: entity staleness (derived from `last_freshened` vs. channel cadence) and dedup collisions emit signals.
- **Spec**: entity creation/mutation is driven by specs (persona-intake, archetype-synthesis).
- **Execute**: agents create/advance/enrich entities per specs; advancement is a contract-gated state transition.
- **Observe**: every transition emits an OTel event (`entity.candidate`, `entity.admitted`, `entity.advanced`, `entity.enriched`, `entity.demoted`, `entity.superseded`).

### Storage

Entity metadata lives in `.intent/entities/`. The entity's actual content lives at `canonical_path` (e.g., `Core/products/cast/farm/registry/pawel-huryn.yaml`). The `.intent/` record is a pointer + lifecycle tracker, not a content store.

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

## Extension 5: Execution Checkpoint Primitive

### Schema Addition

Checkpoints are serialized execution state, enabling pause/resume across agent invocations. They attach to the entity lifecycle as a transient artifact — checkpoints are consumed on resume, not stored permanently.

```yaml
# Checkpoint schema (embedded in execution.paused event data)
checkpoint:
  spec_id: SPEC-NNN
  contract_id: CON-NNN
  step_index: integer          # Which step in the execution plan
  context_snapshot: string     # Reference to serialized context (file path or base64)
  tools_completed: [string]    # Tool calls already executed
  tools_remaining: [string]    # Tool calls still pending
  next_action: string          # Human-readable description of resume action
  created: datetime
  ttl_seconds: integer         # How long the checkpoint remains valid (default: 86400)

resume_trigger:
  type: enum                   # webhook | human_response | timer | signal | dependency
  endpoint: string             # URL for webhook triggers
  signal_id: SIG-NNN           # For signal-based triggers (e.g., human_input.received)
  timeout_seconds: integer     # Max wait before fallback
  fallback: enum               # escalate_to_human | retry | abandon | degrade_trust
```

### Lifecycle Integration

Checkpoints interact with the entity lifecycle from Extension 1:

```
Entity: active → (agent executing) → PAUSED (checkpoint written) → RESUMED (checkpoint consumed) → enriched
```

When an entity's processing is paused:
- The entity remains in its current lifecycle state (does not transition)
- The checkpoint records where processing stopped
- On resume, processing continues from checkpoint — the entity transitions only when processing completes

### Trust Model Integration

The `fallback` field respects the trust model:
- `escalate_to_human`: Always valid. Creates a `request_human_input` signal.
- `retry`: Valid at L3+. Re-enters the execution loop from checkpoint.
- `abandon`: Valid at L4 only. Marks execution as incomplete, emits signal.
- `degrade_trust`: Lowers the effective trust level for this spec by one tier and re-routes.

## Contracts

### CON-008: Entity Lifecycle Consistency
An entity's state must be consistent with its content *per the `entity_type` profile* (Extension 1):
- `pipeline: candidate`: has an identity key; may lack substance; has not yet cleared dedup.
- `pipeline: active`: satisfies the type's admission + completeness floor (persona ⇒ `substance.voice`; archetype ⇒ ≥2 `source_humans`; etc.).
- `disposition: deprecated`: must carry a deprecation reason in metadata.
- `pipeline: active` + `disposition: archival` is a VALID combination (advancement-complete, editorially-retired) and must NOT be flagged inconsistent.

**Verification**: For each entity, check both axes against content presence per its profile. Report inconsistencies. A demoted-but-active entity is consistent, not a violation.

### CON-009: INGEST Idempotency
Running INGEST twice on the same entity must produce exactly one registry entry, one corpus directory, and two processing-log entries. The second run enriches; it does not duplicate.

**Verification**: INGEST entity, count files. INGEST same entity again, count files. Registry count unchanged. Corpus has updated content. Processing log has two entries.

### CON-010: Contribution Non-Regression
After executing a contribution contract, no existing content in the target composite may be removed or reduced. New content may be added; existing content must be preserved or expanded.

**Verification**: Snapshot before/after. Set diff (BEFORE - AFTER) must be empty for all non-regression dimensions.

### CON-011: Trust Modifier Verification
A deployment context modifier may only be applied when the context is machine-verifiable. If `git rev-parse` cannot confirm worktree isolation, the modifier must not be applied (falls back to `in_place` baseline).

**Verification**: Apply worktree modifier from non-worktree context. Must fail gracefully and use baseline scores.

### CON-012: Checkpoint Validity
A checkpoint must be consumed within its TTL. Expired checkpoints must not be resumed — they trigger the fallback action instead. A resumed checkpoint must produce an `execution.resumed` event that references the original `execution.paused` event's span_id.

**Verification**: Create a checkpoint with TTL=1 second. Wait 2 seconds. Attempt resume. Must trigger fallback, not resume. Create a checkpoint with TTL=3600. Resume immediately. Must emit `execution.resumed` with matching span_id.

### CON-013: Human Input Request Independence
A `request_human_input` signal must be emittable at any trust level (L0-L4). The signal must not be blocked by governance gates. When urgency is `blocking`, it must produce an `execution.paused` event. When urgency is `informational`, execution must continue without pausing.

**Verification**: Emit `request_human_input` from an L4 context. Must succeed. Emit with urgency=blocking. Must produce `execution.paused`. Emit with urgency=informational. Must NOT produce `execution.paused`.

### CON-014: LLM-as-Judge Semantic Gap Detection
When `observation.evaluated` produces a verdict of `fail` or `conditional_pass`, the system must emit a new signal describing the semantic gap. This signal must reference the original spec_id and include the evaluator's evidence.

**Verification**: Trigger evaluation where contracts pass but LLM scores below threshold. Must emit new signal with `type: semantic_gap` referencing the spec. Trigger evaluation where LLM scores above threshold. Must NOT emit signal.

### CON-ENTITY-DEDUP: Candidate Dedup Gate
*(Added per WS-DDR-101.)* A `candidate` with an identity-key match (type + alias-normalized name) against an existing entity MUST NOT advance; it MUST raise a merge-intent against the incumbent. This is CON-009 idempotency pulled forward to the entry gate — write-through dedup; the chain_audit dedup sweep is the catch-net, not the primary fix.

**Verification**: Create a candidate matching an incumbent → assert no second entity created AND a merge-intent emitted. Create a candidate with no match → assert it advances normally.

### CON-ENTITY-ONBOARD: Admission DoR
*(Added per WS-DDR-101.)* A `candidate` may advance out of `candidate` only when its `entity_type` profile's minimum-admission criteria are met.

**Verification**: An under-specified candidate cannot leave `candidate`; a complete candidate can.

### CON-ENTITY-DISPOSITION-ORTHOGONALITY: Disposition Never Regresses Pipeline
*(Added per WS-DDR-101.)* Setting `disposition` to a retired value (`archival`/`deprecated`) MUST NOT regress `pipeline`. Advancement and editorial disposition are orthogonal axes (generalized WS-DDR-071 rule).

**Verification**: Demote an `active` entity → assert `pipeline` is still `active`; re-promote `disposition` → assert no pipeline change.
