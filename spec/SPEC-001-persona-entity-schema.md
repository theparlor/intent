---
title: Unified Persona Entity Schema
id: SPEC-001
created: 2026-04-06 18:00:00+00:00
depth_score: 4
depth_signals:
  file_size_kb: 11.7
  content_chars: 9981
  entity_count: 0
  slide_count: 0
  sheet_count: 0
  topic_count: 0
  has_summary: 0
vocab_density: 0.30
status: approved
intent: INT-005
contracts:
  - CON-001
  - CON-002
  - CON-003
  - CON-004
completeness: 0.90
agent_readiness: L3
---
# SPEC-001: Unified Persona Entity Schema

## Overview

Define the canonical schema for all persona entities in `Core/personas/registry/`. The schema must support three entity types (named-human, archetype, class) with parallel structured index and open-world substance blocks.

## Directory Structure

```
Core/personas/
├── CONTEXT.md                    # Index and architecture guide
├── registry/                     # Identity records (one YAML per entity)
│   ├── _schema.yaml              # The canonical schema definition
│   ├── pawel-huryn.yaml          # named-human
│   ├── teresa-torres.yaml        # named-human (migrated)
│   ├── marty-cagan.yaml          # named-human (migrated)
│   ├── april-dunford.yaml        # named-human (migrated)
│   ├── jeff-patton.yaml          # named-human (migrated)
│   ├── ryan-singer.yaml          # named-human (migrated)
│   ├── fortune-50-ceo-mfg.yaml   # archetype
│   └── skeptical-exec.yaml       # class
├── corpus/                       # Raw material (per named-human)
│   ├── pawel-huryn/
│   │   ├── sources.yaml          # Channel registry + last-fetched
│   │   ├── posts/                # Scraped/saved content, dated
│   │   ├── books/                # Summaries or notes
│   │   ├── talks/                # Transcripts, notes
│   │   └── processing-log.md     # What was ingested, when, model version
│   └── teresa-torres/            # (etc. for each named-human)
├── taxonomies/                   # Standard reference taxonomies
│   ├── roles.yaml                # O*NET-derived role/function/level
│   ├── industries.yaml           # NAICS-derived industry codes
│   └── tiers.yaml                # Revenue/size bands
├── archetypes/                   # Synthesis outputs from corpus aggregation
│   └── fortune-50-ceo-mfg/
│       ├── synthesis.md          # The grounded archetype
│       ├── evidence.md           # Redacted aggregate evidence
│       └── source-humans.yaml    # Which named-humans contributed
└── .intent/                      # Intent artifacts for this project
    ├── INTENT.md
    ├── signals/
    └── decisions.md
```

## Entity Schema (registry/*.yaml)

```yaml
# ═══════════════════════════════════════════
# IDENTITY — who/what this is
# ═══════════════════════════════════════════
id: string                        # URL-safe slug (e.g., pawel-huryn)
type: enum                        # named-human | archetype | class
name: string                      # Display name
created: datetime                 # When this entity was created
updated: datetime                 # Last modification
lifecycle: enum                   # created | active | enriched | stale | deprecated | archived

# ═══════════════════════════════════════════
# STRUCTURED INDEX — standards-backed, rollup-capable
# Multiple entries per dimension allowed.
# These are access paths, not definitions.
# ═══════════════════════════════════════════
index:
  roles:                          # O*NET-backed
    - title: string               # Job title
      level: enum                 # C-suite | VP | Director | Manager | IC | Board
      function: string            # O*NET broad function
      onet: string                # O*NET code (optional)
      org: string                 # Organization (optional, named-human only)
  industries:                     # NAICS-backed
    - naics: string               # NAICS code
      label: string               # Human-readable label
      relationship: enum          # primary | parent | adjacent (default: primary)
  tier:                           # Company size/type (optional)
    revenue_band: string          # Fortune 50 | Fortune 500 | Enterprise | Mid-market | SMB
    employee_range: string        # 50000+ | 10000-50000 | 1000-10000 | 100-1000 | <100
    ownership: enum               # public | private | nonprofit | government
    geography: string             # US-domestic | global | EMEA | APAC | etc.

# ═══════════════════════════════════════════
# SUBSTANCE — open-world, never truncated to fit a field
# This is what actually gets used in rendering.
# ═══════════════════════════════════════════
substance:
  voice: string                   # Freeform voice description (multiline)
  mental_models:                  # Named mental models with descriptions
    - name: string
      description: string         # Freeform, multiline, Opus-quality
  unique_signal:                  # Observations that don't fit any field
    - string                      # First-class content, not overflow
  stances:                        # Positions on topics
    - topic: string
      position: string
      confidence: enum            # high | medium | low
      evidence: string            # What supports this stance
  frustration_triggers:           # What irritates or alienates this entity
    - string
  decision_patterns:              # How they make decisions (optional)
    - string
  vocabulary_fingerprint:         # Characteristic language patterns (optional)
    - string

# ═══════════════════════════════════════════
# CONTRIBUTION — how this entity enriches composites
# Named-human and archetype types only.
# ═══════════════════════════════════════════
contributes_to:
  archetypes:                     # (named-human → archetype)
    - id: string                  # Archetype entity ID
      contribution_dimensions:    # Which substance fields flow upward
        - enum                    # voice | mental_models | stances | unique_signal | frustration_triggers | decision_patterns | vocabulary_fingerprint
  classes:                        # (named-human or archetype → class)
    - id: string
      contribution_dimensions:
        - enum

# ═══════════════════════════════════════════
# DISAMBIGUATION — identity anchors for research
# Named-human type only. Required.
# ═══════════════════════════════════════════
disambiguation:
  anchors:                        # Facts that uniquely identify (AND logic)
    - string
  anti_anchors:                   # Common false matches (NOT logic)
    - string
  canonical_urls:                 # Ground-truth pages, verified
    - string
  verified: boolean               # Human-confirmed identity graph

# ═══════════════════════════════════════════
# CHANNELS — where they publish (named-human only)
# Used for freshening schedule.
# ═══════════════════════════════════════════
channels:
  - platform: string              # substack | linkedin | twitter | conference | earnings-call | podcast | blog | youtube
    url: string                   # Direct URL (optional)
    handle: string                # Platform handle (optional)
    frequency: string             # daily | weekly | monthly | quarterly | annual
    richness: enum                # high | medium | low (how much signal per post)

# ═══════════════════════════════════════════
# SOURCING — provenance and attribution
# ═══════════════════════════════════════════
source: enum                      # public | mixed | private
sourced_from:                     # Attribution list
  - string                        # "Book: Title (year)" | "Blog: description" | etc.
originality_assessment: enum      # theorist | practitioner | synthesizer | synthesizer-practitioner
corpus_path: string               # Relative path to corpus directory (named-human only)

# ═══════════════════════════════════════════
# RENDERING METADATA — for Skills Engine / Knowledge Engine consumers
# ═══════════════════════════════════════════
rendering:
  skills_engine_persona: string   # Path to generated persona .md (or null)
  knowledge_engine_voice_ref: string  # Voice YAML that references this entity (or null)
  frameworks:                     # Key frameworks this entity is known for
    - string
  depth_score: integer            # 1-10, from library-index scoring
  related_entities:               # Entity relationship graph
    - id: string
      relationship: enum          # extends | complements | contradicts | mentors | peers_with
      strength: float             # 0.0-1.0
```

## Contracts

### CON-001: Schema Validation
Every file in `registry/` must validate against `_schema.yaml`. Required fields by type:
- **All types**: id, type, name, created, lifecycle, substance.voice, source
- **named-human additionally**: disambiguation (with verified field), channels (at least one), corpus_path, sourced_from
- **archetype additionally**: at least one entry in index.roles or index.industries
- **class additionally**: substance.voice (behavioral description is the definition)

**Verification**: Parse every YAML file in registry/, check required fields by type, report violations.

### CON-002: Open-World Guarantee
No entity may be rejected or flagged as invalid because substance fields contain content that doesn't map to any index field. The index block may be empty or minimal; the substance block must always be accepted as-is.

**Verification**: Attempt to validate entities with empty index blocks but populated substance blocks. Must pass.

### CON-003: Lossless Migration
After migrating existing Skills Engine personas (Torres, Cagan, Patton, Dunford, Singer), every piece of content in the original persona files must be recoverable from the new registry entity + corpus. Diff the original persona rendering against a re-rendering from the new entity; delta must be zero for substantive content.

**Verification**: For each migrated entity, generate the Skills Engine persona format from the registry entity. Diff against original. Semantic diff (ignoring whitespace/formatting) must be empty.

### CON-004: Contribution Integrity
When a named-human declares `contributes_to` an archetype, the declared dimensions must exist in the entity's substance block. You cannot declare contribution of `mental_models` if the entity has no mental_models.

**Verification**: For each contributes_to entry, check that every declared dimension has non-empty content in the entity's substance block.
