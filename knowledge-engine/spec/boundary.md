---
title: Knowledge Engine — Product Boundary & Relationship to Intent
type: spec
maturity: draft
created: 2026-04-06
summary: "Defines the boundary between Intent (methodology), the Knowledge Engine (product), and engagement-specific Knowledge Farms (instances). Clarifies what is structural vs coincidental in how they relate."
depth_score: 4
depth_signals:
  file_size_kb: 8.5
  content_chars: 8394
  entity_count: 0
  slide_count: 0
  sheet_count: 0
  topic_count: 0
  has_summary: 1
vocab_density: 0.61
---
# Knowledge Engine — Product Boundary

> **Purpose:** Establish where Intent ends and the Knowledge Engine begins. Define the three-level architecture: methodology → product → instance.
>
> **Version:** 1.0 — 2026-04-06

---

## The Three Levels

### Intent (Methodology)

What it is: An operating model for AI-augmented product teams. Notice → Spec → Execute → Observe. Trust-gated autonomy. Work ontology. Domain-agnostic.

What it prescribes: "You need compiled domain knowledge to write good specs. Layer 1 of your system should be compiled understanding of the problem domain. This feeds the Spec phase and is updated by the Observe phase (double-loop learning)."

What it does NOT prescribe: How to compile that knowledge. What artifact types to use. What the schema looks like. That's the Knowledge Engine's job.

**Location:** `Core/frameworks/intent/` — the methodology specs, loop definition, trust framework, event system, work ontology.

### Knowledge Engine (Product)

What it is: A domain-agnostic product for building compiled knowledge bases. The pattern: raw sources → agent-compiled artifacts → ingest/query/lint operations. Structured markdown, git-versioned, Obsidian-compatible.

What it provides:
- The `raw/` + `knowledge/` directory architecture
- `AGENTS.md` schema and co-evolution model
- Artifact type system (PER, JRN, DDR, THM, DOM, RAT — extensible)
- Three operations (ingest, query, lint)
- Federation model (inherit down, promote up, never leak sideways)
- Confidence scoring, origin tracking, traceability chain
- Retroactive enrichment (recompilation cascade)
- Redaction/projection model for privacy-aware sharing

What it does NOT provide: The loop. Trust scoring for work items. Agent coordination. That's Intent's job.

**Relationship to Intent:** Intent says "you need Layer 1." The Knowledge Engine IS Layer 1. Intent is used to build and improve the Knowledge Engine (dogfooding). But the Knowledge Engine is a separable product — a team could use it without Intent, and a team could use Intent without the Knowledge Engine (though they'd be worse at specification).

**Location:** Initially spec'd in `Core/frameworks/intent/spec/` (because it was conceived as part of Intent), but architecturally separable. Could eventually live at `Core/knowledge-engine/` if it grows beyond Intent's scope.

### Knowledge Farm (Instance)

What it is: A specific deployment of the Knowledge Engine for a particular domain. Brien's Knowledge Farm is about product strategy, consulting methodology, transformation patterns, and engagement learnings. Someone else's Knowledge Farm might be about manufacturing, healthcare, or astrophysics.

What it contains:
- `raw/` — Domain-specific source material (named clients, specific people, real metrics)
- `knowledge/` — Compiled artifacts specific to this domain and practitioner
- Engagement-scoped sub-farms (Subaru, ASA, F&G) with full named context
- Core knowledge that's domain-general within the farm's scope

**Relationship to Intent:** Brien's Knowledge Farm happens to feed Intent because Brien's domain (product strategy, consulting, software methodology) overlaps with Intent's domain. This is **coincidental, not structural.** If Brien built a Knowledge Farm about Victorian renovation, it wouldn't help Intent at all — but it would still be a valid Knowledge Farm using the same Knowledge Engine, and Brien might use Intent's methodology to build it.

**Location:** Brien's instance spans `Core/` (reusable IP) and `Work/Consulting/Engagements/*/` (engagement-scoped knowledge). The Knowledge Farm IS Brien's Workspaces system, viewed through the compiled knowledge base lens.

---

## What Lives Where

| Artifact | Lives In | Why |
|----------|----------|-----|
| Notice → Spec → Execute → Observe loop definition | Intent | Methodology |
| Trust scoring formula, autonomy levels | Intent | Methodology |
| Work ontology (Signal → Intent → Spec → Contract → ...) | Intent | Methodology |
| MCP servers (intent-notice, intent-spec, intent-observe) | Intent | Methodology tooling |
| "Layer 1 should be compiled domain knowledge" statement | Intent | Methodology prescription |
| AGENTS.md schema, artifact types, frontmatter conventions | Knowledge Engine | Product |
| Ingest/Query/Lint operation definitions | Knowledge Engine | Product |
| Federation model (inherit/promote/isolate) | Knowledge Engine | Product |
| Retroactive enrichment, recompilation cascade | Knowledge Engine | Product |
| Redaction/projection model | Knowledge Engine | Product |
| Artifact templates (PER, JRN, DDR, THM, DOM, RAT) | Knowledge Engine | Product |
| Brien's consulting personas, engagement journeys, client DDRs | Brien's Knowledge Farm | Instance |
| Subaru-specific raw material and compiled knowledge | Subaru engagement sub-farm | Instance (bounded) |
| "Compilation over retrieval" as a theme | Brien's Knowledge Farm | Instance (but promotable to Knowledge Engine as a design principle) |

---

## The Coincidence Clause

Brien's Knowledge Farm is about building great products, services, and software. Intent is a methodology for building great products, services, and software. This overlap means Brien's Knowledge Farm is uniquely useful to Intent — compiled insights about product strategy directly inform how Intent's methodology should evolve.

**This is a feature of Brien's specific situation, not a feature of the architecture.**

The architecture must support:
1. Knowledge Farms that ARE relevant to the methodology they're built with (Brien's case)
2. Knowledge Farms that are NOT relevant (a manufacturing Knowledge Farm built with Intent)
3. Both cases using the exact same Knowledge Engine product

When Brien's Knowledge Farm produces an insight that improves Intent's methodology, the promotion path is:
```
Brien's Knowledge Farm (insight observed)
  → promoted to Knowledge Engine (if it's about the compilation pattern itself)
  → OR promoted to Intent (if it's about the methodology loop)
  → based on WHAT the insight is about, not WHERE it came from
```

---

## Implications for File Layout

### Previous (conflated)
```
Core/frameworks/intent/           # Everything mixed together
├── AGENTS.md                     # Knowledge Engine schema (was at root)
├── raw/                          # Intent's own Knowledge Farm (in Intent repo)
├── knowledge/                    # Intent's own Knowledge Farm (in Intent repo)
├── spec/domain-wiki-operations.md    # Knowledge Engine spec (was in spec/)
├── spec/federated-wiki-architecture.md  # Knowledge Engine spec (was in spec/)
└── spec/intent-methodology.md    # Actual Intent methodology
```

### Current (same repo, clear boundary)
```
Core/frameworks/intent/
├── spec/                         # INTENT METHODOLOGY
│   ├── intent-methodology.md     # The loop
│   ├── signal-trust-framework.md # Trust scoring
│   ├── work-ontology.md          # Signal → Intent → Spec → ...
│   └── ...
├── knowledge-engine/             # KNOWLEDGE ENGINE PRODUCT
│   ├── AGENTS.md                 # Schema & operations
│   ├── spec/                     # KE-specific specs
│   │   ├── operations.md         # Ingest/query/lint
│   │   ├── federation.md         # Inherit/promote/isolate
│   │   ├── enrichment.md         # Retroactive recompilation
│   │   └── redaction.md          # Privacy projections
│   └── templates/                # Artifact templates
├── raw/                          # INTENT'S OWN KNOWLEDGE FARM (dogfooding)
├── knowledge/                    # INTENT'S OWN KNOWLEDGE FARM
└── .intent/                      # Intent's own dogfood
```

This keeps everything in one repo but makes the boundary legible. The Knowledge Engine specs could be extracted to their own repo later if needed.

---

*Knowledge Engine Boundary v1.0 — 2026-04-06*
*Decision rationale: Brien identified boundary collapse between methodology and product during schema-first implementation.*
