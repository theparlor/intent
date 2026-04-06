---
title: Agents
type: framework
maturity: final
confidentiality: shareable
reusability: universal
domains:
  - consulting-operations
created: 2026-04-06
thought_leaders:
  - marty-cagan
  - teresa-torres
depth_score: 5
depth_signals:
  file_size_kb: 22.3
  content_chars: 19198
  entity_count: 2
  slide_count: 0
  sheet_count: 0
  topic_count: 1
  has_summary: 0
vocab_density: 0.26
related_entities:
  - {pair: consulting-operations ↔ subaru, count: 795, strength: 0.427}
  - {pair: consulting-operations ↔ automotive-manufacturing, count: 770, strength: 0.416}
  - {pair: consulting-operations ↔ engagement-management, count: 498, strength: 0.269}
  - {pair: consulting-operations ↔ turnberry, count: 448, strength: 0.224}
  - {pair: consulting-operations ↔ foot-locker, count: 251, strength: 0.136}
---
# AGENTS.md — Compiled Knowledge Base Schema & Operations

> The constitution for Intent's Layer 1 domain knowledge base. Human-maintained, co-evolved with the LLM. Defines artifact types, cross-reference conventions, and the three core operations (ingest, query, lint). Under 300 lines.
>
> **Karpathy's analogy applies:** `raw/` is source code. The LLM is the compiler. `knowledge/` is the executable. Lint is the test suite. Queries are the runtime.
>
> **Intent's extension:** The compiled knowledge base doesn't just compile understanding — it feeds a generative loop (Notice → Spec → Execute → Observe) that produces running software. Domain knowledge and software specification are independent layers, bidirectionally coupled.

---

## 1. Directory Contract

```
raw/                    # IMMUTABLE. Human-curated sources. LLM reads, never writes.
  research/             # Interviews, surveys, user research
  analytics/            # Reports, dashboards, usage data
  competitors/          # Market research, competitor analyses
  support/              # Tickets, session recordings, bug reports

knowledge/              # LLM-COMPILED. Agent writes, human reviews.
  _index.md             # Master catalog — LLM reads first on every operation
  log.md                # Append-only chronological activity log
  traceability.md       # Cross-artifact link matrix
  personas/             # PER-NNN files (compiled synthesis)
  journeys/             # JRN-NNN files (compiled synthesis)
  decisions/            # DDR-NNN files (compiled synthesis)
  themes/               # THM-NNN files (compiled synthesis)
  domain-models/        # DOM-NNN files (compiled synthesis)
  design-rationale/     # RAT-NNN files (compiled synthesis)
  dossiers/             # Entity dossiers (structured profiles)
    people/             # DSR-PER-NNN — person dossiers (from individual-research)
    companies/          # DSR-COM-NNN — company dossiers (from company-dossier)
    products/           # DSR-PRD-NNN — product dossiers (from product-analysis)
    services/           # DSR-SVC-NNN — service dossiers
    industries/         # DSR-IND-NNN — industry dossiers (from industry-scan)
    contexts/           # DSR-CTX-NNN — context dossiers (engagement/domain scoping)

observations/           # Runtime feedback from executed specs
  metrics/              # Performance, usage, behavioral data
  incidents/            # Errors, anomalies, unexpected behaviors
```

### Immutability Rules

- `raw/` files are **never modified** after placement. Corrections create new files referencing originals.
- `knowledge/log.md` is **append-only**. Entries are never edited or deleted.
- Signals (`.intent/signals/`) are **immutable once captured**. Status changes and annotations create new linked artifacts, not edits to the original observation text.

---

## 2. Artifact Types & Frontmatter Schema

Every knowledge artifact is a markdown file with YAML frontmatter. All IDs use the prefix format `PREFIX-NNN` (zero-padded to 3 digits). IDs are sequential within their type.

### 2.1 Persona — `knowledge/personas/PER-NNN-slug.md`

Personas have six subtypes. The same schema handles all, with `subtype` determining which sections are primary.

| Subtype | What it represents | Generated from | Example |
|---------|-------------------|----------------|---------|
| `product` | Who uses the thing being built | User research, analytics, interviews | PER-001-practitioner-architect |
| `role` | What hat someone wears in the system | System design, team topology | △◇○◉ loop personas |
| `hero` | Named individual who exemplifies a pattern | individual-research output, public sources | Karpathy, Ari, Torres |
| `stakeholder` | Who has power/interest in the outcome | Engagement context, org analysis | Client VP, Turnberry PM |
| `engagement` | Client-specific user type | Engagement research, client interviews | SOA field engineer, ASA physician |
| `archetype` | Generalized pattern from multiple hero/engagement personas | Synthesis across multiple personas | "The skeptical VP" across 3 clients |

```yaml
---
id: PER-NNN
type: persona
subtype: product | role | hero | stakeholder | engagement | archetype
name: "Display Name"
slug: slug-name
confidence: 0.0-1.0        # How well-evidenced is this persona?
origin: human | agent | synthetic
sources: []                 # Paths to raw/ files, signal IDs, or individual-research outputs
derived_from: []            # PER-NNN IDs (for archetypes synthesized from multiple personas)
exemplifies: []             # PER-NNN archetype IDs this persona is an instance of
engagement: null            # Engagement name (for engagement subtypes, confidentiality scoping)
related_journeys: []        # JRN-NNN IDs
related_decisions: []       # DDR-NNN IDs
related_themes: []          # THM-NNN IDs
pain_points: []             # Free-text list, each linked to DDRs when addressed
voice_persona: null         # Skills Engine persona reference (e.g., "personalities/teresa-torres")
created: YYYY-MM-DD
updated: YYYY-MM-DD
---
```

**Body structure (all subtypes):**
- `## Who` — Demographics, role, context, goals
- `## Behaviors` — Observable patterns, habits, workflows
- `## Needs & Pain Points` — What they need, what frustrates them (each as `- PP-NNN: description`)
- `## Evidence` — Source references with [[wikilinks]] to raw/ files
- `## Open Questions` — What we don't yet know about this persona

**Additional sections by subtype:**

| Subtype | Additional sections |
|---------|-------------------|
| `hero` | `## Professional Trajectory`, `## Communication Profile`, `## Influence Map`, `## Frameworks & Methodology` |
| `stakeholder` | `## Decision Authority`, `## Engagement Leverage Points`, `## Risk Posture` |
| `archetype` | `## Exemplars` (list of hero/engagement personas this generalizes), `## Pattern` (what they share) |
| `engagement` | `## Client Context`, `## Relationship to Engagement Scope` |

**Generation paths:**

```
Name of a person ──→ individual-research skill ──→ raw/ profile ──→ ingest ──→ hero persona
Role description ──→ direct generation ──→ role persona
User research ──→ ingest (standard) ──→ product persona
Multiple heroes ──→ synthesis ──→ archetype persona
Engagement context ──→ engagement-scoped generation ──→ engagement persona
```

### 2.1b Entity Dossiers — `knowledge/dossiers/{type}/DSR-{TYPE}-NNN-slug.md`

Entity dossiers are structured profiles of real-world entities. They sit between raw sources and compiled synthesis — richer than raw research, not yet abstracted into personas/journeys/decisions. Dossiers are the intermediate compilation step.

**Six dossier types:**

| Type | Prefix | Generated by (Skills Engine) | Feeds (compiled synthesis) |
|------|--------|------------------------------|---------------------------|
| Person | DSR-PER | `individual-research` | Hero personas (PER), stakeholder personas |
| Company | DSR-COM | `company-dossier` | Domain models (DOM), themes (THM), engagement context |
| Product | DSR-PRD | `product-analysis` | Journeys (JRN), decisions (DDR), competitive themes |
| Service | DSR-SVC | (manual or new skill) | Journeys (JRN), decisions (DDR), capabilities |
| Industry | DSR-IND | `industry-scan` | Themes (THM), design rationale (RAT), market context |
| Context | DSR-CTX | (composite) | Engagement scoping — pulls from other dossier types |

**Shared frontmatter (all dossier types):**

```yaml
---
id: DSR-{TYPE}-NNN
type: dossier
subtype: person | company | product | service | industry | context
name: "Entity Name"
slug: slug-name
confidence: 0.0-1.0
origin: human | agent | synthetic
sources: []               # Raw sources, URLs, skill outputs
related_personas: []       # PER-NNN IDs this feeds
related_themes: []         # THM-NNN IDs this informs
engagement: null           # Engagement scope (null = Core)
confidentiality: public | internal | client-confidential | nda
last_researched: YYYY-MM-DD
created: YYYY-MM-DD
updated: YYYY-MM-DD
---
```

**Body structure by subtype:**

**Person** (`DSR-PER`): `## Headline` (3-sentence compression), `## Professional Trajectory`, `## Communication Profile`, `## Influence Map`, `## Current Priorities`, `## Engagement Strategy`, `## Frameworks & Methodology`

**Company** (`DSR-COM`): `## Overview` (what they do, scale, market position), `## Strategic Position` (competitive landscape, recent moves), `## Organizational Signals` (hiring patterns, tech stack, culture indicators), `## Industry Context`, `## Engagement Relevance`

**Product** (`DSR-PRD`): `## What It Does`, `## Target Users`, `## Competitive Position`, `## Strengths & Weaknesses`, `## Technical Architecture` (if known), `## Market Signals`

**Service** (`DSR-SVC`): `## What It Provides`, `## Delivery Model`, `## Target Clients`, `## Competitive Position`, `## Differentiation`, `## Integration Points`

**Industry** (`DSR-IND`): `## Landscape` (market size, key players, growth trajectory), `## Trends` (technology, regulatory, behavioral), `## Forces` (Porter's or equivalent), `## Implications for Engagement`

**Context** (`DSR-CTX`): `## Scope` (what this context covers), `## Key Entities` (links to other dossiers), `## Constraints`, `## Assumptions`, `## Strategic Questions`

**The ingest/extract/expound cycle:**

```
INGEST:  Skills Engine research skill runs → output lands in raw/
EXTRACT: Knowledge Engine ingests raw output → creates DSR-* dossier
EXPOUND: Dossier feeds persona/journey/theme generation → compiled knowledge grows
         Compiled knowledge reveals gaps → triggers new research → cycle repeats
```

### 2.2 Journey Map — `knowledge/journeys/JRN-NNN-slug.md`

```yaml
---
id: JRN-NNN
type: journey
name: "Journey Name"
persona: PER-NNN
confidence: 0.0-1.0
origin: human | agent | synthetic
sources: []
related_decisions: []
related_specs: []           # SPEC-NNN IDs
created: YYYY-MM-DD
updated: YYYY-MM-DD
---
```

**Body structure:**
- `## Overview` — What this journey covers, start/end conditions
- `## Stages` — Ordered H3 sections, each stage containing:
  - `### Stage: Name` with substeps, emotions, pain points, touchpoints
  - Pain points cross-referenced to persona pain points (`PP-NNN`)
  - Touchpoints linked to domain models where applicable
- `## Moments of Truth` — Critical decision points or high-emotion moments
- `## Evidence` — Source references

### 2.3 Design Decision Record — `knowledge/decisions/DDR-NNN-slug.md`

```yaml
---
id: DDR-NNN
type: decision
title: "Decision Title"
status: proposed | accepted | superseded | validated | invalidated
confidence: 0.0-1.0
origin: human | agent | synthetic
addresses: []               # PP-NNN pain point IDs
persona: PER-NNN
journey_stage: "JRN-NNN#stage-name"
sources: []
related_specs: []           # SPEC-NNN IDs
superseded_by: null         # DDR-NNN if superseded
validated_by: []            # Observation file paths
created: YYYY-MM-DD
updated: YYYY-MM-DD
---
```

**Body structure:**
- `## Context` — Why this decision is needed now
- `## Decision` — What was decided
- `## Alternatives Considered` — What else was evaluated and why it was rejected
- `## Consequences` — Expected outcomes (positive and negative)
- `## Validation Criteria` — How we'll know if this decision was right (observable, measurable)

### 2.4 Theme — `knowledge/themes/THM-NNN-slug.md`

```yaml
---
id: THM-NNN
type: theme
name: "Theme Name"
confidence: 0.0-1.0
origin: human | agent | synthetic
sources: []
related_personas: []        # PER-NNN IDs
related_journeys: []        # JRN-NNN IDs
related_decisions: []       # DDR-NNN IDs
signals: []                 # SIG-NNN IDs from .intent/
created: YYYY-MM-DD
updated: YYYY-MM-DD
---
```

**Body structure:**
- `## Insight` — The core finding in 1-2 sentences
- `## Evidence` — Supporting data points with source references
- `## Implications` — What this means for the product/system
- `## Open Questions` — What remains unclear

### 2.5 Domain Model — `knowledge/domain-models/DOM-NNN-slug.md`

```yaml
---
id: DOM-NNN
type: domain-model
name: "Model Name"
scope: glossary | bounded-context | entity-relationship | state-machine
confidence: 0.0-1.0
origin: human | agent | synthetic
sources: []
related_specs: []
created: YYYY-MM-DD
updated: YYYY-MM-DD
---
```

**Body structure:**
- `## Definition` — What this model represents
- `## Elements` — Key terms, entities, or states with definitions
- `## Relationships` — How elements relate to each other
- `## Boundaries` — What's in scope and what's not (bounded context)

### 2.6 Design Rationale — `knowledge/design-rationale/RAT-NNN-slug.md`

```yaml
---
id: RAT-NNN
type: rationale
name: "Rationale Name"
confidence: 0.0-1.0
origin: human | agent | synthetic
sources: []
related_decisions: []       # DDR-NNN IDs this rationale supports
related_themes: []
frameworks: []              # Named frameworks applied (Torres, Cagan, etc.)
created: YYYY-MM-DD
updated: YYYY-MM-DD
---
```

**Body structure:**
- `## Argument` — The reasoning chain
- `## Framework Application` — Which product/systems framework applies and how
- `## Evidence` — Supporting data
- `## Risks` — What could make this rationale wrong

---

## 3. Cross-Reference Conventions

### Wikilinks

Use `[[target]]` syntax for all cross-references within knowledge/:

```markdown
This persona's primary journey is [[JRN-001-onboarding]].
The pain point is addressed by [[DDR-012-skip-onboarding]].
See [[PER-003-power-user]] for the affected persona.
```

### Source References

Reference raw/ files with relative paths:

```markdown
Source: [Interview P14](../raw/research/2026-04-01-user-interview-p14.md)
```

### Signal Links

Reference .intent/ signals with ID only (agents resolve the path):

```markdown
Related signal: SIG-014
```

### Spec Links

Reference specs with ID:

```markdown
Specified in: SPEC-045
Verified by: CON-045
```

### Pain Point IDs

Pain points are namespaced to their persona: `PER-NNN/PP-NNN`. They originate in persona files and are referenced by DDRs, journeys, and specs.

---

## 4. Three Core Operations

### 4.1 Ingest

**Trigger:** A new file appears in `raw/`.

**Process:**
1. Read the source file completely
2. Read `knowledge/_index.md` to understand current knowledge base state
3. Create a summary of the source (filed under the appropriate knowledge subdirectory)
4. For each persona, journey, theme, decision, or domain model mentioned:
   - If the artifact exists → update it with new evidence, adjust confidence
   - If the artifact doesn't exist → create it with initial confidence based on evidence strength
5. Update cross-references: add [[wikilinks]] in all affected files
6. Update `knowledge/traceability.md` with new source-to-artifact chains
7. Update `knowledge/_index.md` with new/modified artifacts
8. Append to `knowledge/log.md`: `[INGEST] YYYY-MM-DD source-filename → created: [list], updated: [list]`

**One source typically touches 10-15 knowledge artifacts.**

**Confidence scoring on ingest:**
- Single source mention: confidence 0.3
- Corroborated by 2+ sources: confidence 0.5
- Corroborated + validated by observation: confidence 0.7+
- Direct human confirmation: confidence 0.9

### 4.2 Query

**Trigger:** A human or agent asks a question about the domain.

**Process:**
1. Read `knowledge/_index.md` to identify relevant artifacts
2. Read identified artifacts
3. Synthesize answer with [[citations]] to knowledge artifacts and raw/ sources
4. If the answer reveals a significant new insight → offer to file it as a new knowledge artifact (theme or design-rationale)
5. If the answer reveals a gap → note it for the next lint pass
6. Append to `knowledge/log.md`: `[QUERY] YYYY-MM-DD "question" → referenced: [list], new artifacts: [list]`

**Query answers that become knowledge artifacts create a compounding feedback loop.** This is the mechanism by which the knowledge base grows richer through use, not just through ingestion.

### 4.3 Lint

**Trigger:** Periodic (after every 5 ingests, or on demand).

**Checks:**
1. **Contradictions** — Two artifacts assert incompatible claims. Flag both with specific text.
2. **Orphans** — Artifacts with no inbound [[wikilinks]]. Why does this exist if nothing references it?
3. **Stale claims** — Confidence scores that haven't been updated in 30+ days with no new evidence.
4. **Missing cross-refs** — Persona mentions a pain point addressed by no DDR. Journey references a persona that doesn't exist. DDR links to no spec.
5. **Coverage gaps** — Personas with no journey maps. Journey stages with no pain points identified. Pain points with no DDR. DDRs with no spec.
6. **Provenance drift** — Agent-generated artifacts (`origin: agent | synthetic`) that haven't been human-reviewed.

**Output:** Each finding becomes a suggested signal for the Notice phase. Lint doesn't fix — it surfaces.

**Append to `knowledge/log.md`:** `[LINT] YYYY-MM-DD findings: N contradictions, N orphans, N stale, N gaps → signals suggested: [SIG-NNN list]`

---

## 5. Bidirectional Data Flows

These six flows couple the three layers. The first two are knowledge-base-specific; the rest involve the full Intent loop.

| Flow | From → To | Mechanism | Learning Type |
|------|-----------|-----------|---------------|
| 1 | Knowledge → Notice | Lint surfaces signals (gaps, contradictions, staleness) | System 4 intelligence |
| 2 | Notice → Spec (via knowledge) | Spec authoring queries knowledge base for personas, journeys, DDRs | Informed specification |
| 3 | Spec → Execute | Trust-gated agents build against specs | Maker-checker |
| 4 | Execute → Observe | Running code emits events | Empirical feedback |
| 5 | Observe → Knowledge | Observations update personas, journeys, DDRs | **Double-loop** (Argyris) |
| 6 | Observe → Spec corpus | Spec drift detection, living doc sync | Single-loop |

**Flow 5 is the most important.** Without it, the system can refine how it builds but never question whether it's building the right thing.

---

## 6. Origin Tracking (Contamination Mitigation)

Every knowledge artifact carries an `origin` field:

| Value | Meaning |
|-------|---------|
| `human` | Created or substantively edited by a human |
| `agent` | Generated by an LLM agent during ingest/query/lint |
| `synthetic` | Derived entirely from other knowledge artifacts, no raw source |

**Rules:**
- Agent-generated artifacts start at confidence ≤ 0.5 unless corroborated
- Human review of an agent-generated artifact changes origin to `human` and allows confidence > 0.7
- Synthetic artifacts are flagged in knowledge lint if they lack raw source backing
- Trust scoring can weight human-originated signals differently (see signal-trust-framework.md)

---

## 7. Implicit Guidance & Control (Boyd)

As the knowledge base grows, well-established patterns should enable speed:

- **Familiar pattern detected:** If a new signal matches an existing persona pain point with an accepted DDR and a validated spec, the system can route directly from Notice → Execute without full spec creation. The knowledge base provides the implicit guidance.
- **Threshold:** DDR status = `validated`, persona confidence ≥ 0.7, journey confidence ≥ 0.7
- **Audit trail:** Even IG&C-accelerated work emits events and updates log.md

---

## 8. Naming Conventions

| Artifact | Prefix | File Pattern | Example |
|----------|--------|-------------|---------|
| Persona | PER | `PER-NNN-slug.md` | `PER-001-power-user.md` |
| Journey | JRN | `JRN-NNN-slug.md` | `JRN-001-onboarding.md` |
| Decision | DDR | `DDR-NNN-slug.md` | `DDR-001-skip-onboarding.md` |
| Theme | THM | `THM-NNN-slug.md` | `THM-001-speed-over-ceremony.md` |
| Domain Model | DOM | `DOM-NNN-slug.md` | `DOM-001-work-ontology.md` |
| Rationale | RAT | `RAT-NNN-slug.md` | `RAT-001-compilation-over-rag.md` |
| Pain Point | PP | `PER-NNN/PP-NNN` | `PER-001/PP-003` (namespaced to persona) |

---

## 9. Federation Model

Intent federates across a Core framework and multiple bounded engagements. See `spec/federation.md` for the full spec.

### The Rule

**Inherit down. Promote up. Never leak sideways.**

- Core knowledge base = generalized archetypes, universal themes, methodology
- Engagement knowledge base = client-specific personas, journeys, DDRs
- Engagement inherits Core schema and references Core knowledge artifacts via `Core:ID` notation
- Generalizable insights are promoted from engagement → Core after sanitization
- Client-specific content NEVER flows between engagements

### Engagement AGENTS.md

Each engagement creates its own AGENTS.md that extends Core:

```yaml
inherits: ../../Core/frameworks/intent/AGENTS.md
engagement: ClientName
confidentiality_default: client-internal
```

Engagement can ADD frontmatter fields and artifact subtypes. Cannot REMOVE or OVERRIDE Core conventions.

### Cross-Scope References

| Direction | Notation | Example |
|-----------|----------|---------|
| Engagement → Core | `Core:PER-001` | "Based on Core:PER-001 archetype" |
| Core → Engagement | Not needed | Core doesn't know about engagements |
| Engagement → Engagement | **Forbidden** | Use promote → Core → inherit path |

### Confidentiality

Every knowledge artifact carries a `confidentiality:` field: `public`, `internal`, `client-internal`, `nda`. Lint flags any `client-internal` or `nda` artifact referenced from Core or another engagement.

### Promotion

Engagement → Core promotion requires sanitization: strip client names, specific metrics, named individuals, internal tools. Keep the insight. See `spec/federation.md` §Flow 2 for the full protocol.

---

_AGENTS.md v1.1 — 2026-04-05_
_Co-evolved: Brien (architecture) + Claude (formalization)_
_Sources: reference/karpathy-synthesis/03-three-layer-architecture-formalized.md, spec/federation.md_
