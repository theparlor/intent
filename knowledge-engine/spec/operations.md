---
title: Domain Knowledge Base Operations
type: spec
maturity: draft
created: 2026-04-05
thought_leaders:
  - andrej-karpathy
  - christopher-alexander
  - chris-argyris
  - stafford-beer
summary: "Specification for the three core operations (ingest, query, lint) that maintain Intent's Layer 1 domain knowledge base. Adapted from Karpathy's LLM Knowledge Base pattern for product-domain artifacts."
depth_score: 6
depth_signals:
  file_size_kb: 8.7
  content_chars: 8292
  entity_count: 4
  slide_count: 0
  sheet_count: 0
  topic_count: 0
  has_summary: 1
vocab_density: 0.37
related_entities:
  - {pair: stafford-beer ↔ andrej-karpathy, count: 2, strength: 1.0}
  - {pair: stafford-beer ↔ christopher-alexander, count: 2, strength: 1.0}
  - {pair: andrej-karpathy ↔ christopher-alexander, count: 2, strength: 1.0}
---
# Domain Knowledge Base Operations

> **Purpose:** How the compiled knowledge base (Layer 1) stays alive, grows, and self-audits.
>
> **Version:** 1.0 — 2026-04-05
>
> **Schema:** See `AGENTS.md` for artifact types, frontmatter schemas, and cross-reference conventions.
>
> **Origin:** Andrej Karpathy's LLM Knowledge Base pattern (April 2026), adapted for Intent's three-layer architecture.

---

## Overview

The compiled knowledge base is maintained through three operations that cycle continuously:

```
         ┌──────────┐
         │  INGEST  │ ← New source material enters raw/
         └────┬─────┘
              │ compiles into knowledge artifacts
              ▼
         ┌──────────┐
         │  QUERY   │ ← Questions answered against compiled knowledge
         └────┬─────┘
              │ good answers filed back as new pages
              ▼
         ┌──────────┐
         │   LINT   │ ← Health checks: contradictions, gaps, staleness
         └────┬─────┘
              │ findings become signals for Notice phase
              └──────────→ back to INGEST (or to Intent loop)
```

These operations are independent of the Intent loop (Notice→Spec→Execute→Observe) but coupled to it through Flows 1, 2, and 5.

---

## Ingest

### Trigger

A new file appears in `raw/` (any subdirectory).

### Prerequisites

- `knowledge/_index.md` exists and is readable
- `AGENTS.md` schema is loaded (artifact templates, frontmatter conventions)

### Process

1. **Read the source.** Read the new file in `raw/` completely. Note its type (interview, analytics report, competitor analysis, etc.) and key content.

2. **Read the index.** Read `knowledge/_index.md` to understand the current state of all knowledge artifacts.

3. **Identify affected knowledge artifacts.** For each persona, journey, theme, decision, domain model, or rationale mentioned or implied by the source:
   - Does a relevant artifact already exist? → plan an update
   - Does the source introduce a new entity? → plan a creation

4. **Create new artifacts.** For each new artifact:
   - Use the template from `knowledge-engine/templates/`
   - Assign the next sequential ID (e.g., PER-003, THM-004)
   - Set `origin: agent` (unless human is doing the ingest interactively)
   - Set initial `confidence` based on evidence strength:
     - Single source mention: 0.3
     - Corroborated by 2+ sources: 0.5
     - Corroborated + observation-validated: 0.7+
     - Human-confirmed: 0.9
   - Add `sources:` referencing the raw/ file path
   - Add `[[wikilinks]]` to all related artifacts

5. **Update existing artifacts.** For each existing artifact touched by this source:
   - Add the new source to `sources:` list
   - Update relevant sections with new evidence
   - Adjust `confidence` if evidence strengthens or contradicts
   - Add new `[[wikilinks]]` for new cross-references
   - Update `updated:` date

6. **Update navigation files.**
   - `knowledge/_index.md`: Add new knowledge artifacts, update summaries, recalculate coverage table
   - `knowledge/traceability.md`: Add or extend traceability chains
   - `knowledge/log.md`: Append `[INGEST]` entry with source path, created list, updated list

7. **Verify cross-reference integrity.** Every `[[wikilink]]` in new/updated files should point to an artifact that exists. Flag any broken links.

### Output

A single ingest typically touches **10-15 knowledge artifacts** (Karpathy's empirical observation). The result is a more complete, more interlinked knowledge base with updated confidence scores.

### Confidence Scoring Rules

| Evidence Pattern | Confidence |
|-----------------|------------|
| Single source, single mention | 0.3 |
| Single source, detailed treatment | 0.4 |
| Two sources, corroborating | 0.5 |
| Three+ sources, consistent pattern | 0.6 |
| Corroborated + observation data | 0.7 |
| Corroborated + validated by experiment | 0.8 |
| Human-confirmed with direct evidence | 0.9 |
| Axiomatic / definitional | 1.0 |

---

## Query

### Trigger

A human or agent asks a question about the domain.

### Process

1. **Read the index.** Read `knowledge/_index.md` to identify which artifacts are relevant to the question.

2. **Read relevant artifacts.** Read the identified knowledge artifacts. Follow `[[wikilinks]]` one level deep if the answer requires synthesis across artifacts.

3. **Synthesize answer.** Answer the question with explicit citations:
   - `[[wikilinks]]` to knowledge artifacts used
   - Source references to `raw/` files where applicable
   - Confidence assessment based on the cited artifacts' confidence scores

4. **Offer to file.** If the answer reveals a significant new insight (a theme, a rationale, a cross-cutting pattern), offer to file it as a new knowledge artifact.

5. **Note gaps.** If the answer reveals a gap (question can't be fully answered from compiled knowledge), note it for the next lint pass.

6. **Log.** Append to `knowledge/log.md`: `[QUERY] date "question" → referenced: [artifact list], new: [if any]`

### Compounding Feedback Loop

Query answers that become knowledge artifacts are the mechanism by which the knowledge base grows richer through use, not just through ingestion. This is the runtime of the compilation model.

---

## Lint

### Trigger

Run after every 5 ingests, or on demand.

### Checks

| Check | What to Look For | Severity |
|-------|-----------------|----------|
| **Contradictions** | Two artifacts assert incompatible claims | High |
| **Orphans** | Artifacts with no inbound `[[wikilinks]]` | Medium |
| **Stale claims** | Confidence unchanged for 30+ days, no new evidence | Medium |
| **Missing cross-refs** | Persona pain points with no DDR. DDR with no spec. Journey referencing non-existent persona. | High |
| **Coverage gaps** | Personas with no journey. Journey stages with no pain points. Pain points with no DDR. DDRs with no spec. | Medium |
| **Provenance drift** | `origin: agent` or `origin: synthetic` artifacts never human-reviewed | Low |
| **Broken wikilinks** | `[[target]]` where target file doesn't exist | High |

### Process

1. **Read all knowledge artifacts.** Read `knowledge/_index.md`, then read every artifact file.
2. **Run all checks.** Each check produces a list of findings.
3. **Generate signals.** Each finding becomes a suggested signal for the Notice phase (`.intent/signals/`).
4. **Log.** Append to `knowledge/log.md`: `[LINT] date findings: N contradictions, N orphans, N stale, N gaps → signals: [SIG-NNN list]`

### Important

Lint **does not fix**. Lint **surfaces**. Findings become signals. The Intent loop (Notice→Spec→Execute→Observe) decides what to do about them. This preserves the separation between Layer 1 (knowledge) and Layer 2 (methodology).

---

## Integration with Intent Loop

### Flow 1: Lint → Notice

Lint findings are filed as signals with `source: knowledge-lint`. They enter the normal signal pipeline: trust scoring, clustering, promotion to intents.

### Flow 2: Spec Authoring → Knowledge Query

When an agent authors a spec (in the intent-spec MCP server or manually), it should:
1. Read `knowledge/_index.md`
2. Identify relevant personas, journeys, and DDRs
3. Reference them in the spec's YAML frontmatter
4. Include `[[wikilinks]]` in the spec body

### Flow 5: Observe → Knowledge Update

When the observe phase detects that reality diverges from a domain model prediction:
- If user behavior differs from persona prediction → decrease persona confidence
- If journey map doesn't match observed user flow → flag journey for revision
- If DDR's validation criteria fail → change DDR status to `invalidated`
- If DDR's validation criteria pass → change DDR status to `validated`

All updates logged to `knowledge/log.md` with `[UPDATE]` prefix.

---

*Domain Knowledge Base Operations v1.0 — 2026-04-05*
*Source: reference/karpathy-synthesis/, AGENTS.md*
