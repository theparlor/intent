---
title: Redaction & Privacy Projection Model
type: spec
maturity: draft
created: 2026-04-06
summary: "How Brien's Knowledge Farm maintains full-fidelity named context for solo work while generating redacted projections for sharing, proposals, and cross-engagement reasoning."
depth_score: 4
depth_signals:
  file_size_kb: 6.2
  content_chars: 6378
  entity_count: 0
  slide_count: 0
  sheet_count: 0
  topic_count: 0
  has_summary: 1
vocab_density: 0.00
---
# Redaction & Privacy Projection Model

> **Purpose:** Brien's Knowledge Farm needs full named context for his own work, but must generate privacy-safe projections when sharing, generating proposals for new clients, or reasoning across engagement boundaries.
>
> **Version:** 1.0 — 2026-04-06

---

## The Problem

Brien works solo. When he's reasoning about an engagement, he needs full fidelity: real client names, real people, real metrics, real org charts. Abstraction would slow him down and lose signal.

But when he:
- Generates a proposal for a new client based on patterns from prior clients
- Shares a framework or methodology insight externally
- Uses cross-engagement patterns to inform a current engagement
- Creates case studies or thought leadership content

...he needs to redact client-identifying details while preserving the insight.

This is not a one-time sanitization. It's a **projection model** — the same underlying knowledge, viewed through different lenses depending on the audience.

---

## Confidentiality Tiers

Every knowledge artifact and raw source carries a `confidentiality:` field:

| Tier | Meaning | Who Sees Full Fidelity | Redacted For |
|------|---------|----------------------|--------------|
| `public` | Can be shared externally as-is | Everyone | Nobody |
| `internal` | Brien's eyes only, no client sensitivity | Brien | External audiences |
| `client-confidential` | Contains client-identifying details | Brien | Other clients, external |
| `nda` | Explicitly covered by NDA terms | Brien | Everyone except the client |

---

## Projection Types

### Full Fidelity (Brien's Working View)

The default. All names, metrics, details visible. This is how Brien works day-to-day.

No transformation needed — this is the raw knowledge base state.

### Client-Safe Projection (Cross-Engagement Reasoning)

When Brien uses insights from Engagement A to inform Engagement B:

| Original | Projected |
|----------|-----------|
| "Subaru's VP of Engineering resisted the coaching model" | "A VP of Engineering at an automotive OEM resisted the coaching model" |
| "SOA's JIRA instance had 14,000 stale tickets" | "The client's project management tool had thousands of stale tickets" |
| "The $125/hr rate was 55% below market" | Omitted (Brien's own financial details, not relevant to the pattern) |
| "The transformation playbook we used at Subaru" | "A transformation playbook used at a prior automotive engagement" |

**Rules:**
- Client name → industry + company type ("an automotive OEM", "a healthcare association")
- Named individuals → role only ("the VP of Engineering", "the product owner")
- Specific metrics → ranges or qualitative descriptions ("thousands of", "significantly below market")
- Engagement-specific tooling → generic equivalents ("their project management tool")
- Preserve the PATTERN, strip the IDENTITY

### External Projection (Thought Leadership, Proposals)

When Brien shares insights publicly or in proposals:

Everything in Client-Safe, plus:
- Engagement timing abstracted ("in a recent engagement" vs specific dates)
- Brien's specific financial arrangements omitted entirely
- Framework names preserved (these are Brien's IP)
- Multiple engagements synthesized into composite examples where needed

### Archive Projection (Historical Engagements)

When an engagement ends:
- Full fidelity version preserved in the engagement folder (for Brien's reference)
- Promoted Core artifacts are already sanitized (federation model handles this)
- No active confidentiality obligations change — NDA terms govern retention

---

## Implementation

### At the Artifact Level

Every knowledge artifact already has `confidentiality:` in its frontmatter (or inherits from the engagement's `confidentiality_default` in AGENTS.md).

The redaction model adds a `projection` operation:

```
project(artifact, tier) → redacted copy

where:
  project(PER-001, "client-safe") → same structure, names replaced, metrics abstracted
  project(DDR-007, "external") → decision preserved, context generalized, client stripped
```

### At the Query Level

When querying across engagements:
1. Determine the projection tier needed for the current context
2. Read artifacts at full fidelity
3. Apply projection before synthesizing the answer
4. Cite projected artifacts, not originals

### At the Generation Level

When generating proposals, case studies, or cross-engagement analyses:
1. Gather relevant artifacts from all engagement knowledge bases
2. Apply the appropriate projection to each
3. Synthesize from the projected artifacts
4. The output inherits the HIGHEST confidentiality tier of any input
   - If any source is `nda`, the synthesis must be `nda`
   - If sources are `client-confidential` from different clients, the synthesis is `internal` (no single client's details visible)

---

## Relationship to Federation

The federation model says "never leak sideways." The redaction model makes that safe:

- Full fidelity stays in the engagement folder
- Cross-engagement reasoning goes through projection
- Core promotion goes through sanitization (already defined in federation spec)
- Projections are generated on demand, never persisted as separate copies (to avoid stale redacted copies drifting from the source)

---

## Brien's Modes of Operation

| Mode | Projection Tier | Context |
|------|----------------|---------|
| Working on Subaru engagement | Full fidelity (Subaru) | Brien is inside the engagement boundary |
| Using Subaru pattern for ASA proposal | Client-safe | Brien needs the pattern, not Subaru's identity |
| Writing a blog post about transformation patterns | External | Brien is creating public content |
| Reasoning about his own consulting practice | Internal | Brien is thinking about his business, not a client |
| Generating a company dossier for a new prospect | Internal + external sources | No prior engagement data unless projection-safe |

---

*Redaction & Privacy Projection Model v1.0 — 2026-04-06*
