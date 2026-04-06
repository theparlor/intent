---
title: Federated Knowledge Base Architecture
type: spec
maturity: draft
created: 2026-04-05
thought_leaders:
  - stafford-beer
  - christopher-alexander
  - andrej-karpathy
summary: "How Intent's three-layer architecture federates across a Core framework and multiple bounded engagements — inherit down, promote up, never leak sideways."
depth_score: 6
depth_signals:
  file_size_kb: 16.3
  content_chars: 16108
  entity_count: 3
  slide_count: 0
  sheet_count: 0
  topic_count: 0
  has_summary: 1
vocab_density: 0.13
related_entities:
  - {pair: christopher-alexander ↔ andrej-karpathy, count: 2, strength: 1.0}
  - {pair: christopher-alexander ↔ stafford-beer, count: 2, strength: 1.0}
  - {pair: stafford-beer ↔ andrej-karpathy, count: 2, strength: 1.0}
---
# Federated Knowledge Base Architecture

> **Purpose:** How the Core Intent framework and engagement-specific instances form a cascading yet bounded knowledge network — each engagement benefits from Core improvements and contributes generalizable learnings back.
>
> **Version:** 1.0 — 2026-04-05
>
> **Prerequisite:** Read `AGENTS.md` and `spec/operations.md` first.

---

## The Problem

Intent's three-layer architecture (compiled knowledge base + transformation OS + software spec/code) works for a single project. But Brien's practice operates across multiple concurrent engagements (Subaru, ASA, F&G, etc.) plus a Core IP library. The challenge:

1. **Core must continuously grow** — every engagement teaches something generalizable
2. **Each engagement must benefit from Core** — new engagements shouldn't start from zero
3. **Engagement knowledge must stay bounded** — client-specific content never leaks across confidentiality boundaries
4. **The relationship must be cascading** — Core improvements propagate downstream without manual distribution

This is a federation problem. Brien already solves it for glossaries (federated glossary architecture in `memory/glossary.md`). This spec extends that pattern to the full three-layer architecture.

---

## Architecture: Inherit Down, Promote Up, Never Leak Sideways

```
Core/frameworks/intent/           ← THE UNIVERSAL SUBSTRATE
├── raw/                          ← Industry research, methodology sources, public domain
├── knowledge/                         ← Generalized personas, archetypes, pattern library
├── .intent/                      ← Core methodology signals, specs
├── spec/                         ← Core methodology specs
└── AGENTS.md                     ← Core schema (inherited by all engagements)

Work/Consulting/Engagements/Subaru/     ← BOUNDED INSTANCE
├── raw/                          ← Client-specific: interviews, analytics, SOA internal docs
├── knowledge/                         ← Client-specific: SOA personas, SOA journeys, SOA DDRs
│   └── _core_refs.md             ← Links to Core knowledge artifacts this engagement inherits
├── .intent/                      ← Engagement-specific signals, specs
└── AGENTS.md                     ← Engagement-specific extensions (inherits Core schema)

Work/Consulting/Engagements/ASA/        ← ANOTHER BOUNDED INSTANCE
├── raw/                          ← Client-specific: playbook, Miro artifacts, ASA internals
├── knowledge/                         ← Client-specific: ASA personas, ASA journeys, ASA DDRs
│   └── _core_refs.md             ← Links to Core knowledge artifacts this engagement inherits
├── .intent/                      ← Engagement-specific signals, specs
└── AGENTS.md                     ← Engagement-specific extensions
```

### The Three Flows

```
┌─────────────┐        INHERIT ↓         ┌─────────────────────┐
│    CORE      │ ──────────────────────── │   ENGAGEMENT A      │
│  (universal) │                          │   (bounded)         │
│              │ ◄─────────────────────── │                     │
│              │        PROMOTE ↑         │                     │
└─────────────┘                           └─────────────────────┘
                                                    ✕ no sideways
                                          ┌─────────────────────┐
                                          │   ENGAGEMENT B      │
                                          │   (bounded)         │
                                          └─────────────────────┘
```

---

## Flow 1: Inherit Down (Core → Engagement)

When an engagement starts, it inherits from Core:

### What Inherits

| Artifact | How It Inherits | Example |
|----------|----------------|---------|
| **AGENTS.md schema** | Engagement AGENTS.md starts with `inherits: Core/frameworks/intent/AGENTS.md` and adds engagement-specific extensions | Core defines PER/JRN/DDR templates; Subaru adds SOA-specific frontmatter fields |
| **Templates** | Core `.intent/templates/` are the base. Engagement can override or extend. | Core persona template; Subaru adds `business_unit:` and `platform:` fields |
| **Core knowledge archetypes** | `knowledge/_core_refs.md` links to generalized archetypes in Core that apply to this engagement | Core has PER-001 (Practitioner-Architect); Subaru knowledge base references it when describing SOA's senior engineers |
| **Methodology specs** | Core `spec/` is the canonical methodology. Engagements don't fork it — they apply it. | `spec/intent-methodology.md` governs all engagements |
| **Themes and rationale** | Core themes (THM-001 Compilation Over Retrieval, THM-002 Bottleneck Shift) are universal truths available to every engagement | Engagement knowledge base can reference `Core:THM-002` when justifying a decision |
| **Trust framework** | The trust scoring formula and autonomy levels are Core methodology | Same L0-L4 levels everywhere |

### How Inheritance Works

1. **Schema inheritance.** Engagement `AGENTS.md` declares `inherits: ../../Core/frameworks/intent/AGENTS.md`. All Core conventions apply unless explicitly overridden. Override = engagement adds fields; never removes Core fields.

2. **Template inheritance.** Engagement uses Core templates by default. Can extend with additional YAML frontmatter fields relevant to the client context. Never modifies Core template files.

3. **Reference, not copy.** Engagement knowledge bases reference Core artifacts via `Core:PER-001` notation. They don't copy Core content into the engagement knowledge base. This means Core updates automatically propagate.

4. **The `_core_refs.md` file.** Each engagement knowledge base contains `_core_refs.md` listing which Core knowledge artifacts are relevant to this engagement and why. This is the "inheritance manifest."

---

## Flow 2: Promote Up (Engagement → Core)

When an engagement produces a generalizable insight, it gets promoted to Core.

### What Gets Promoted

| Artifact Type | Promotion Criteria | Sanitization |
|---------------|-------------------|--------------|
| **Theme** | Pattern observed in 2+ engagements, or single engagement with strong evidence that it's universal | Strip client name, project details, internal metrics. Keep the insight. |
| **Design Rationale** | Reasoning that applies to any product team, not just this client | Strip engagement context. Generalize the argument. |
| **Persona archetype** | A persona pattern seen across multiple engagements (e.g., "the skeptical VP") | Abstract from specific person/org to archetype. New PER-NNN in Core. |
| **Journey pattern** | A journey stage sequence that repeats across engagements | Abstract from client-specific touchpoints to universal stages. |
| **Methodology improvement** | The engagement revealed a gap or improvement in Intent's core methodology | Update Core spec/ directly. This IS the double-loop. |
| **Template evolution** | Engagement needed a frontmatter field that every future engagement would benefit from | Add to Core template. |

### How Promotion Works

1. **Identify the candidate.** During engagement work, notice something generalizable. This can happen during:
   - Knowledge lint (a theme appears that's clearly not client-specific)
   - Engagement review / retrospective
   - Cross-engagement pattern recognition

2. **Capture a promotion signal.** In the engagement's `.intent/signals/`, capture a signal with `promotion_candidate: true` and `target: core`. Include the artifact path and a brief case for why it's generalizable.

3. **Sanitize.** Strip all client-identifying information:
   - Client name → "the client" or omit
   - Internal metrics → "metrics showed X" without specific numbers
   - Named individuals → roles only
   - Internal tools/platforms → generic equivalents
   - Anything that would violate NDA if read by another client

4. **File in Core.** Create the new artifact in Core knowledge base with:
   - `origin: promoted`
   - `promoted_from: [engagement name]` (engagement name is OK; details are not)
   - `promoted_date: YYYY-MM-DD`
   - A sanitized version of the evidence

5. **Back-link.** The engagement artifact gets an `promoted_to: Core:[ID]` field. The Core artifact gets a `promoted_from_engagements: [list]` field.

### Promotion Frequency

- **After each engagement milestone** (phase completion, deliverable hand-off): review knowledge base for promotion candidates
- **During cross-engagement lint:** compare themes across active engagements for shared patterns
- **At engagement close:** final promotion sweep

---

## Flow 3: Never Leak Sideways (Engagement ↛ Engagement)

This is the hard boundary. Client-specific content never flows directly from one engagement to another.

### What Never Crosses

- `raw/` content (interviews, analytics, internal documents)
- Client-specific personas with real names/details
- Client-specific journey maps with internal tool references
- Financial data, org charts, strategic plans
- Any content marked `confidentiality: client-internal` or `confidentiality: nda`

### The Laundering Path

If Engagement A produces an insight that would help Engagement B, it must flow through Core:

```
Engagement A → (promote, sanitize) → Core → (inherit) → Engagement B
```

This is not bureaucracy. It's the same pattern Brien already uses for glossaries — org-specific terms live in each engagement's `glossary.md`, never centralized. The promotion path through Core is the sanitization layer.

### Enforcement

- YAML frontmatter `confidentiality:` field on every artifact. Values: `public`, `internal`, `client-internal`, `nda`
- `client-internal` and `nda` artifacts can never be copied to Core or another engagement
- Lint check: any Core knowledge artifact referencing an engagement-specific `raw/` file is a violation
- Lint check: any cross-engagement `[[wikilink]]` is a violation

---

## Schema Extension Model

### Core AGENTS.md (universal)

Defines:
- All artifact types (PER, JRN, DDR, THM, DOM, RAT)
- All frontmatter fields that every engagement must have
- All three operations (ingest, query, lint)
- Cross-reference conventions
- Naming conventions (prefix-NNN-slug.md)
- Confidentiality rules

### Engagement AGENTS.md (extends Core)

```yaml
# Engagement AGENTS.md header
inherits: ../../Core/frameworks/intent/AGENTS.md
engagement: Subaru
confidentiality_default: client-internal
```

Can add:
- Engagement-specific frontmatter fields (e.g., `business_unit:`, `platform:`, `jira_epic:`)
- Engagement-specific artifact subtypes (e.g., a Subaru-specific "transformation readiness assessment" template)
- Engagement-specific lint rules (e.g., "every DDR must reference a JIRA epic")
- Engagement-specific raw/ subdirectories (e.g., `raw/jira-exports/`, `raw/miro-boards/`)

Cannot override:
- Core artifact types
- Core frontmatter fields (can only add, never remove)
- Core naming conventions
- Core operation definitions (ingest/query/lint)
- Cross-reference conventions
- Confidentiality enforcement rules

---

## ID Namespacing

To prevent ID collisions between Core and engagements:

| Scope | Pattern | Example |
|-------|---------|---------|
| Core | `PER-NNN` | `PER-001-practitioner-architect` |
| Engagement | `[ENG]:PER-NNN` | `SOA:PER-001-field-engineer` |

When referencing across scopes:
- Core → Engagement: not needed (Core doesn't know about engagements)
- Engagement → Core: `Core:PER-001` or `Core:THM-002`
- Engagement → Engagement: **forbidden**

In practice, engagement artifacts use plain `PER-NNN` within their own knowledge base (context is implicit). The namespace prefix is only needed in cross-scope references.

---

## The Cascade Effect

Here's what "cascading yet bound" looks like in practice:

### Core grows a new theme

Brien notices across Subaru and ASA that both clients struggle with the same pattern. He promotes it:

```
Core/knowledge/themes/THM-004-transformation-theater.md
  origin: promoted
  promoted_from: [Subaru, ASA]
  confidence: 0.6 (two engagements, consistent pattern)
```

Every future engagement's `_core_refs.md` can reference `Core:THM-004` during their first ingest. The insight compounds across the practice.

### Core improves a template

Working with Subaru reveals that every persona should have a `decision_authority:` field. Brien adds it to the Core template:

```
knowledge-engine/templates/persona.md
  + decision_authority: sponsor | approver | influencer | user | none
```

Next time any engagement runs ingest, the template is available. Existing engagements can adopt it at their own pace.

### Core methodology evolves

The Subaru engagement reveals that the lint operation needs a new check: "personas referenced by a DDR that have no journey map." Brien adds it to `knowledge-engine/spec/operations.md` (the Core spec). All engagements benefit.

### An engagement inherits a Core archetype

ASA starts a new engagement phase. During knowledge base setup, the agent reads `Core:PER-001-practitioner-architect` and creates `ASA:PER-001-product-champion` with a note: "Based on Core:PER-001 archetype. ASA-specific: this persona is a physician with part-time product responsibilities."

---

## Lifecycle: Engagement Knowledge Base Setup

When a new engagement starts, the agent should:

1. **Read Core AGENTS.md** to understand the universal schema
2. **Create engagement directories:** `raw/`, `knowledge/`, `.intent/` within the engagement folder
3. **Create engagement AGENTS.md** extending Core with engagement-specific conventions
4. **Create `knowledge/_core_refs.md`** listing which Core knowledge artifacts are relevant
5. **Seed `raw/`** with engagement-specific source material
6. **Run first ingest** — this creates the engagement's knowledge base, referencing Core archetypes where applicable
7. **Capture setup signal** in engagement `.intent/signals/`

---

## Beer's VSM Mapping (Why This Architecture Works)

| VSM Component | Maps To |
|---------------|---------|
| **System 5 (Identity)** | Core methodology and values — what Intent IS across all engagements |
| **System 4 (Intelligence)** | Core knowledge base — generalized domain knowledge, pattern recognition across engagements |
| **System 3 (Management)** | Core AGENTS.md + trust framework — governance that applies everywhere |
| **System 2 (Coordination)** | The promote/inherit flows — how engagements stay aligned without being coupled |
| **System 1 (Operations)** | Each engagement — autonomous, bounded, doing the actual work |
| **3-4 Homeostat** | The bidirectional coupling between engagement-level learning and Core-level knowledge |

The federation is a viable system: each engagement is operationally autonomous (System 1), but coordinated through shared methodology (System 2+3), informed by accumulated intelligence (System 4), and aligned to a shared identity (System 5).

---

## Anti-Patterns

| Anti-Pattern | Why It's Wrong | What To Do Instead |
|-------------|---------------|-------------------|
| Forking Core methodology into engagement | Creates drift, loses the cascade benefit | Always inherit Core; extend only in engagement AGENTS.md |
| Copying Core knowledge artifacts into engagement | Creates stale copies that diverge | Reference Core artifacts via `Core:ID` notation |
| Promoting without sanitizing | NDA violation, client trust breach | Always strip client-identifying details during promotion |
| Direct engagement-to-engagement reference | Violates confidentiality boundary | Promote to Core first, then the other engagement inherits |
| Engagement overriding Core conventions | Fragments the methodology | Engagement can only ADD to Core schema, never remove or change |
| Skipping the `_core_refs.md` manifest | Engagement loses track of what it inherits | Always create and maintain the inheritance manifest |

---

*Federated Knowledge Base Architecture v1.0 — 2026-04-05*
*Design decision: Mirrors Brien's existing Workspaces topology (Core = reusable IP, Work = applied IP) extended to the three-layer architecture.*
