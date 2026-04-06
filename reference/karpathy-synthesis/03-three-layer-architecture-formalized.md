---
title: 03 Three Layer Architecture Formalized
type: framework
maturity: final
confidentiality: shareable
reusability: universal
domains:
  - consulting-operations
created: 2026-04-06
thought_leaders:
  - marty-cagan
  - jeff-patton
  - teresa-torres
  - josh-seiden
  - tim-herbig
  - john-kotter
  - mik-kersten
  - matthew-skelton
  - richard-rumelt
frameworks:
  - transformation-operating-system
depth_score: 6
depth_signals:
  file_size_kb: 12.6
  content_chars: 11595
  entity_count: 10
  slide_count: 0
  sheet_count: 0
  topic_count: 1
  has_summary: 0
vocab_density: 0.60
related_entities:
  - {pair: matthew-skelton ↔ mik-kersten, count: 17840, strength: 0.994}
  - {pair: mik-kersten ↔ john-kotter, count: 17840, strength: 0.993}
  - {pair: matthew-skelton ↔ john-kotter, count: 17839, strength: 0.992}
  - {pair: richard-rumelt ↔ matthew-skelton, count: 17838, strength: 0.997}
  - {pair: richard-rumelt ↔ mik-kersten, count: 17838, strength: 0.997}
---
# Formalized Architecture for the Three-Layer Compiled Knowledge System

## Overview

The three-layer system — a self-organizing domain knowledge base feeding an orchestration loop that produces software specifications — is theoretically overdetermined. Five major product strategy frameworks (Torres, Patton, Cagan, Seiden, Herbig) independently describe the same pattern. Four systems thinking traditions (Beer, Argyris, Boyd, Alexander) provide formal cybernetic theory. Karpathy's LLM Knowledge Base pattern provides the exact technical substrate for Layer 1.

---

## Layer 1: Domain Knowledge Base (Karpathy Pattern Adapted for Product Work)

Karpathy's system uses an LLM as a compiler that reads raw source documents and produces a structured, interlinked wiki of markdown files. His analogy: "raw/ is the source code, the LLM is the compiler, the wiki is the executable, health checks are the test suite, and queries are the runtime."

For Intent's Layer 1, this extends to product domain artifacts:
- `raw/` holds user interview transcripts, analytics exports, competitor analyses, support tickets, stakeholder notes
- `wiki/` compiles these into personas, journey maps, design decision records, domain models, research themes, and a traceability matrix
- All as structured markdown with YAML frontmatter carrying IDs, version numbers, confidence scores, source references, and cross-links

The critical insight: the wiki is a persistent, compounding artifact. Unlike RAG, which re-derives knowledge on every query, this system compiles once and keeps current.

---

## Layer 2: The Transformation Operating System (Intent's Loop)

The notice→spec→execute→observe engine. Domain-agnostic methodology. Orchestrates work through trust-gated agent autonomy (L0–L4).

---

## Layer 3: Software Specification & Code (Generative Output)

Specs, contracts, component designs, and running code. What the system produces.

---

## Five Product Frameworks Mapped

### Teresa Torres — Opportunity Solution Trees
The opportunity space IS the domain wiki. Interview-driven restructuring IS the notice phase. Choosing a target opportunity and generating solutions IS the spec phase. Running assumption tests IS execute. Measuring against desired outcome IS observe. Torres' core insight — the tree self-organizes as new data arrives — maps exactly onto Karpathy's compilation model.

### Jeff Patton — Story Mapping
The story map is a two-dimensional compiled domain artifact: horizontal backbone of user activities (the canonical journey) with vertical ribs of stories ordered by priority. Patton's backbone corresponds to a compiled domain schema. Stories sliced from the map are generated specs. The map evolves as a living artifact through build-learn feedback cycles. His key concept of "shared understanding" maps to the domain wiki as aligned mental models.

### Marty Cagan — Product Model
Discovery (deciding what to build) = Layer 1. Delivery (building it) = Layer 3. Cagan insists the same empowered team does both — they are continuous, interleaved activities. His trust-gated autonomy concept (teams earning independence through demonstrated competence) maps directly to Intent's trust-gated agent model. His "Direction" layer (vision + strategy) sits above the loop, determining which problems the cycle should address.

### Josh Seiden — Outcomes Over Output
An outcome is a change in human behavior that drives business results. This gives the observe phase specific meaning — you're observing behavioral change, not system metrics. His logic model (Impact ← Outcomes ← Outputs ← Activities) gives the domain wiki a causal structure: not just facts but a theory of how behavior connects to value, validated every cycle.

### Tim Herbig — Impact Mapping
WHY/impact → WHO/actors → HOW/outcomes → WHAT/outputs → WHETHER/experiments. Creates explicit traceability chains from strategic goals through personas through outcomes to specs. Every output traces back to strategic justification. Supplies the traceability schema the domain wiki needs.

### Synthesis
Layer 1 contains: goal hierarchy (Seiden + Herbig), actor/persona maps (Herbig + Patton), opportunity trees (Torres), user journey maps (Patton), causal behavior-to-impact chains (Seiden + Herbig). It self-organizes as research feeds in. Each framework treats domain understanding as a continuously compiled artifact that generates actionable work.

---

## Four Cybernetic Traditions

### Stafford Beer — Viable System Model
- Layer 1 = System 4+5 (intelligence + identity)
- Layer 2 = System 2+3 (coordination + management)
- Layer 3 = System 1 (operations)
- The **3-4 Homeostat** (bidirectional coupling between ops and intelligence) is the most important interface. If S3 dominates → operationally efficient but strategically blind. If S4 dominates → plans disconnected from capability.

### Chris Argyris — Double-Loop Learning
- Single-loop: corrects errors within existing assumptions (optimizing execution)
- Double-loop: questions the governing variables themselves (the domain model)
- Flow 5 (observe → domain wiki) enables double-loop learning
- Without it, the system can refine how it builds but never question whether it's building the right thing
- Risk: defensive routines that suppress disconfirming signals instead of surfacing them

### Boyd — OODA Loop
- Notice→spec→execute→observe maps to Observe→Orient→Decide→Act
- But Boyd's full diagram has 5+ simultaneous feedback paths with Orient at center
- Orient shapes what you Observe (domain model determines what you notice)
- **Implicit Guidance & Control** lets compiled patterns bypass explicit spec creation for familiar situations
- Design for **shared orientation** — agents sharing the same domain wiki can act autonomously with less coordination

### Christopher Alexander — Pattern Languages / Systems Generating Systems
- Core axiom: to make things that function as wholes, design the generating system, not individual outputs
- The domain wiki should be a pattern language — interconnected patterns with rules for combination that GENERATE software
- **Accretive growth**: "several acts of building, each one done to repair and magnify the product of the previous acts, will slowly generate a larger and more complex whole than any single act can generate"

---

## The Traceability Chain

Every link is bidirectional and navigable through [[wikilinks]] and YAML frontmatter:

```
Raw Research (interview P14, analytics segment, 12 support tickets)
  → synthesized into →
Persona (wiki/personas/power-user-sarah.md)
  + Journey Map (wiki/journeys/onboarding-power-user.md#first-use)
  → identifies →
Pain Point (PP-001: cannot skip onboarding)
  → addressed by →
Design Decision (wiki/decisions/DDR-012-skip-onboarding.md)
  → specified in →
Spec (spec/SPEC-045-onboarding-flow.md)
  → verified by →
Contract (spec/contracts/CON-045-onboarding.md)
  → implemented in →
Code (src/features/skip-onboarding/)
  → observed via →
Metrics (observations/metrics/onboarding-completion-rates.md)
  → feeds back into →
Persona confidence scores, journey map accuracy, design decision validation
```

---

## Six Bidirectional Data Flows

**Flow 1: Domain wiki → Notice.** Compiled wiki surfaces signals: pain points from lint passes, decayed confidence scores, contradictions, coverage gaps (persona pain points without DDRs). Beer's System 4 function.

**Flow 2: Notice → Spec with domain wiki queries.** During spec authoring, agents query the domain wiki for relevant personas, journey stages, existing DDRs, design rationale. Specs reference and link back to all queried domain artifacts.

**Flow 3: Spec → Execute.** Trust-gated agents generate code from specs. Maker-checker pattern: one agent generates, another evaluates against acceptance criteria.

**Flow 4: Execute → Observe.** Running code emits events: test results, deployment metrics, user behavior, errors.

**Flow 5: Observe → Domain wiki (double-loop learning).** Observation agents update domain wiki with learnings. If users behave differently than persona predicted → confidence decreases. If journey map diverges from observed behavior → flagged for revision. If design decision's predicted outcome doesn't materialize → DDR marked for supersession.

**Flow 6: Observe → Spec corpus (single-loop learning).** Spec drift detection, status updates. BDD/Gherkin specs function as living documentation — simultaneously specs, docs, and tests.

---

## Complete File System Architecture

```
intent-project/
├── raw/                          # Immutable source material (Layer 1 input)
│   ├── research/                 # Interview transcripts, surveys
│   ├── analytics/                # Exported reports, dashboards
│   ├── competitors/              # Competitor analyses
│   └── support/                  # Ticket exports, session recordings
├── wiki/                         # LLM-compiled knowledge (Layer 1)
│   ├── _index.md                 # Master index (LLM-maintained)
│   ├── personas/                 # LLM-generated persona files
│   ├── journeys/                 # LLM-generated journey maps
│   ├── decisions/                # Design Decision Records (DDRs)
│   ├── themes/                   # Research themes and insights
│   ├── domain-models/            # Glossary, bounded contexts
│   ├── design-rationale/         # Why-level documentation
│   ├── traceability.md           # Cross-artifact link matrix
│   └── log.md                    # Chronological activity log
├── .intent/                      # Intent system artifacts (Layer 2)
│   ├── signals/                  # SIG-NNN files
│   ├── intents/                  # INT-NNN files
│   └── events/                   # events.jsonl
├── spec/                         # Generated specifications (Layer 3)
│   ├── SPEC-NNN-*.md             # Feature specs
│   ├── contracts/                # CON-NNN contract files
│   ├── api/                      # API contracts
│   ├── components/               # Component specs + design tokens
│   └── tests/                    # BDD/Gherkin living docs
├── src/                          # Running code (Layer 3 output)
├── observations/                 # Runtime feedback
│   ├── metrics/                  # Performance, usage analytics
│   └── incidents/                # Error reports, anomalies
└── AGENTS.md                     # Schema: conventions, templates, workflows
```

---

## Technology Stack

- **Obsidian** — Wiki viewer (graph view, backlinks, YAML rendering via Dataview)
- **Git** — Versioning (every LLM operation produces a commit with meaningful message)
- **Claude Code or OpenAI Codex** — LLM agent layer with filesystem access
- **LangGraph or Temporal** — Orchestration state management
- **Gherkin/Cucumber** — Living documentation in Layer 3
- **Style Dictionary** — Design tokens as code (→ CSS variables → components → Storybook)
- **qmd** — Local hybrid search (BM25 + vector) over markdown files at scale

---

## Key Design Principles

1. **Compilation over retrieval.** Compile understanding once and keep it current. The domain wiki is not a search index — it's a compiled artifact that grows richer with every cycle.

2. **The 3-4 Homeostat is the most important interface.** The coupling between the orchestration loop and the domain knowledge base must be balanced and continuous.

3. **Implicit Guidance & Control is the reward for compilation.** As the domain wiki grows richer, familiar patterns can flow from notice to execute without full spec creation. Compiled domain patterns enable speed.
