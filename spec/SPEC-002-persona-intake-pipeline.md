---
title: Persona Intake Pipeline (INGEST skill)
id: SPEC-002
created: 2026-04-06 18:00:00+00:00
depth_score: 4
depth_signals:
  file_size_kb: 6.3
  content_chars: 6123
  entity_count: 0
  slide_count: 0
  sheet_count: 0
  topic_count: 0
  has_summary: 0
vocab_density: 0.65
status: approved
intent: INT-005
contracts:
  - CON-005
  - CON-006
  - CON-007
completeness: 0.85
agent_readiness: L3
---
# SPEC-002: Persona Intake Pipeline

## Overview

A six-stage pipeline that triggers on any phrasing of "ingest this human" and produces a fully registered persona entity with corpus, disambiguation, downstream renderings, and freshening schedule.

## Pipeline Stages

### Stage 1: IDENTIFY
**Input**: Natural language reference to a human (name, URL, description)
**Output**: Identity record in `Core/personas/registry/[slug].yaml`
**Trust level**: L3 (agent executes, human monitors)

1. Parse input for name, URLs, contextual clues
2. If entity already exists in registry → branch to ENRICH (idempotent)
3. Generate disambiguation anchors from available context
4. Search web with anchors to validate identity
5. If ambiguity detected (multiple plausible matches) → pause, surface options to Brien, set `verified: false`
6. Create identity record with: id, type, name, disambiguation, lifecycle: created
7. Set `verified: false` until Brien confirms (or auto-verify if canonical URL matched)

### Stage 2: HARVEST
**Input**: Identity record with channels
**Output**: Populated corpus directory
**Trust level**: L3-L4 (depends on channel accessibility)

1. Register primary channels in identity record
2. For each channel:
   - Substack/blog: Fetch archive, store posts as dated markdown
   - LinkedIn: Attempt fetch (may require fallback to manual or browser tool)
   - Books: Create summary notes from public descriptions and reviews
   - Talks/podcasts: Search for transcripts, store available ones
   - Conferences: Search for talk abstracts and slides
3. Create `sources.yaml` with last-fetched timestamps per channel
4. Create `processing-log.md` with ingestion metadata (date, model, token count)
5. All raw material stored in `corpus/[slug]/` — immutable after initial write

### Stage 3: ASSESS
**Input**: Identity record + populated corpus
**Output**: Enriched identity record with substance, index, originality assessment
**Trust level**: L3

1. Read entire corpus
2. Extract and populate substance block:
   - voice: Synthesize characteristic voice from writing patterns
   - mental_models: Identify 3-7 named mental models with descriptions
   - unique_signal: Capture observations that don't fit structured fields
   - stances: Extract positions on key topics with evidence
   - frustration_triggers: Identify from language patterns
   - vocabulary_fingerprint: Characteristic word choices and patterns
3. Populate index block:
   - roles: From career history
   - industries: From domain focus
   - tier: From company affiliations
4. Set originality_assessment: theorist | practitioner | synthesizer | synthesizer-practitioner
5. Map related_entities against existing registry entries
6. Compute depth_score using library-index methodology
7. Update lifecycle: created → active

### Stage 4: RENDER
**Input**: Enriched identity record + corpus
**Output**: Skills Engine persona file, Knowledge Engine voice reference update
**Trust level**: L3

1. Generate Skills Engine persona file at `Core/products/skills-engine/personas/personalities/[slug].md`
   - Follow exact format of existing personas (frontmatter + epigraph + voice + mental models + shaping + rendering notes)
   - Source all content from registry entity substance block
   - Include rendering notes for platform and role persona combinations
2. Update Knowledge Engine voice references where applicable
   - If entity is relevant to an existing voice (e.g., product.yaml), add to hero_authors
3. Set rendering.skills_engine_persona and rendering.knowledge_engine_voice_ref paths

### Stage 5: CONNECT
**Input**: Fully rendered entity
**Output**: Updated relationship graph, CONTEXT.md updates
**Trust level**: L4

1. Update `Core/personas/CONTEXT.md` with new entity entry
2. Update `Core/products/skills-engine/personas/CONTEXT.md` with new personality entry
3. Map contributes_to declarations based on index dimensions
4. If archetypes don't exist yet, note them as planned in CONTEXT.md
5. Cross-reference with existing entities (update related_entities on both sides)

### Stage 6: SCHEDULE
**Input**: Entity with channels
**Output**: Freshening metadata
**Trust level**: L4

1. Record primary channels with freshening frequency recommendations
2. Add entry to `Core/personas/freshening-schedule.yaml` (or create if first entity)
3. Note: actual automated freshening is future work — this stage records the intent

## Trigger Patterns

The intake skill should activate on any of these natural language patterns:
- "Add [name] as a persona"
- "Ingest [name]"
- "Bring in [name]"
- "Research [name] for our persona library"
- "[URL to someone's profile or content]" (when context implies persona creation)
- "Let's add [name] to our [heroes/personalities/roster]"
- "I want [name]'s voice in our system"

## Contracts

### CON-005: Idempotent Intake
Running the intake pipeline twice on the same entity must not create duplicates. Second run should detect existing entity and branch to enrichment (update corpus, refresh substance, re-render).

**Verification**: Run intake for an existing entity. Registry should have exactly one file. Corpus should be updated, not duplicated. Processing log should show two entries.

### CON-006: Disambiguation Gate
For any entity where `verified: false`, the pipeline must pause at Stage 2 (HARVEST) and surface disambiguation options before proceeding with corpus harvesting. No corpus should be harvested for an unverified identity.

**Verification**: Create an entity with an ambiguous name. Confirm pipeline pauses. Confirm corpus/ directory is empty until verification.

### CON-007: Standalone Value at Every Stage
An entity that has completed Stage 1 (IDENTIFY) only should still be queryable and useful — it has a name, disambiguation anchors, and lifecycle state. An entity that has completed Stage 3 (ASSESS) but not Stage 4 (RENDER) should be fully usable as a persona reference even without downstream renderings.

**Verification**: Query/reference entities at each pipeline stage. Confirm each provides progressively richer but always-usable output.
