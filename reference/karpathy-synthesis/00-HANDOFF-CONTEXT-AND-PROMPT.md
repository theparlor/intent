---
title: 00 Handoff Context And Prompt
type: framework
maturity: final
confidentiality: shareable
reusability: universal
domains:
  - consulting-operations
created: 2026-04-06
technologies:
  - jira
thought_leaders:
  - marty-cagan
  - jeff-patton
  - teresa-torres
  - josh-seiden
  - tim-herbig
depth_score: 6
depth_signals:
  file_size_kb: 18.4
  content_chars: 17581
  entity_count: 6
  slide_count: 0
  sheet_count: 0
  topic_count: 1
  has_summary: 0
vocab_density: 0.51
related_entities:
  - {pair: consulting-operations ↔ subaru, count: 795, strength: 0.427}
  - {pair: consulting-operations ↔ automotive-manufacturing, count: 770, strength: 0.416}
  - {pair: consulting-operations ↔ engagement-management, count: 498, strength: 0.269}
  - {pair: consulting-operations ↔ turnberry, count: 448, strength: 0.224}
  - {pair: consulting-operations ↔ foot-locker, count: 251, strength: 0.136}
---
# Intent Project — Handoff Context & Agent Prompt

## Agent Instructions

You are continuing work on the **Intent** project (theparlor.github.io/intent, github.com/theparlor/intent). This document contains the full context from a strategic research and architecture session that produced several key decisions about how to evolve Intent's architecture. Read this entire document before taking any action. The owner is an engineer/architect/system designer with deep product strategy expertise who follows Marty Cagan, Jeff Patton, Teresa Torres, Tim Herbig, Josh Seiden, and related thought leaders.

---

## 1. What Intent Is

Intent is an open-source operating model for AI-augmented teams. It replaces Scrum/Jira ceremony stacks with a continuous loop and a two-plane architecture.

**Core thesis:** When AI collapses the cost of implementation, the bottleneck moves from execution to clarity — knowing *what* to build, *why* it matters, and *how to verify* it's done.

**The loop:** Notice → Spec → Execute → Observe (continuous, no batching)

**Two-plane architecture:**
- **Work Stream Plane** (ephemeral flow): Signal → Intent → Atom → Event → Trace
- **Ownership Topology Plane** (persistent structure): Product → Capability → Team
- **Bridging artifacts:** Specs and Contracts persist across both planes

**Technical implementation:** Three MCP servers (intent-notice on port 8001, intent-spec on port 8002, intent-observe on port 8003) with six Claude Code subagents. Trust-gated autonomy (L0–L4) governs agent freedom using the formula:

```
trust = clarity×0.30 + (1/blast_radius)×0.20 + reversibility×0.20 + testability×0.20 + precedent×0.10
```

**Storage:** Markdown files in `.intent/` and `spec/` directories, Git-versioned. Events in JSONL. No database.

**Key URLs:**
- Site: https://theparlor.github.io/intent/
- Pitch: https://theparlor.github.io/intent/pitch.html
- Methodology: https://theparlor.github.io/intent/methodology.html
- Architecture: https://theparlor.github.io/intent/architecture.html
- Concept Brief: https://theparlor.github.io/intent/concept-brief.html
- GitHub: https://github.com/theparlor/intent

---

## 2. What Happened in This Session

### 2.1 Karpathy's LLM Knowledge Bases (April 2, 2026)

We researched Andrej Karpathy's viral tweet (x.com/karpathy/status/2039805659525644595, 25K+ likes) describing a workflow for using LLMs to build personal knowledge bases. Key details:

**His system architecture:**
- `raw/` — Immutable source documents (papers, articles, repos). LLM reads but never modifies.
- `wiki/` — LLM-generated, LLM-maintained markdown: summaries, entity pages, concept pages, cross-references, index. The LLM "owns this layer entirely."
- Schema file (`CLAUDE.md` or `AGENTS.md`) — Co-evolved process definition. Pure methodology, zero domain knowledge.

**Three operations cycle through:**
1. **Ingest** — Human drops source into raw/, LLM reads it, creates summary, updates index, revises relevant concept/entity pages (one source touches 10–15 pages), appends to log.
2. **Query** — Questions answered with citations against the wiki. Good answers get filed back as new pages (compounding feedback loop).
3. **Lint** — Periodic health checks: find contradictions, orphans, stale claims, missing cross-references, suggest next questions.

**His analogy:** "Obsidian is the IDE; the LLM is the programmer; the wiki is the codebase."

**Scale:** ~100 articles, ~400,000 words on a single topic. No vector database needed — LLM navigates via auto-maintained index.md and brief summaries.

**Key resources:**
- GitHub Gist "llm-wiki.md": https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f
- VentureBeat coverage: https://venturebeat.com/data/karpathy-shares-llm-knowledge-base-architecture-that-bypasses-rag-with-an
- Steph Ango (Obsidian CEO) contamination mitigation concept: https://x.com/kepano/status/2039831289533227446

### 2.2 Structural Parallels Identified

We mapped five deep structural parallels between Karpathy's system and Intent:

| Dimension | Karpathy | Intent |
|-----------|----------|--------|
| Storage | Markdown + Git, no DB | Markdown + Git, no DB |
| Ingestion | Human curates what enters raw/ → LLM compiles | Human notices friction → captures Signal → system promotes |
| Topic centers | Emergent typed pages (concept, entity, comparison) | Coined ontology (Signal, Intent, Spec, Contract, Atom, Event, Trace) |
| Method vs. data | Schema file = process; Wiki = content; Raw = source | Methodology = process; Specs/Contracts = content; Signals = raw observation |
| Feedback loop | Query outputs filed back into wiki | Observe phase feeds back into Notice |

### 2.3 The Critical Distinction the Owner Identified

**Karpathy builds a knowledge artifact — a wiki that gets smarter. The output is understanding.**

**Intent builds a generative engine — a system where a clearly expressed idea moves through a pipeline and becomes running software. The output is working code.**

Karpathy's system compiles knowledge *about* a domain. Intent compiles knowledge *into* a domain — into actual working systems. His loop terminates at understanding. Intent's loop terminates at deployment.

### 2.4 The Architectural Decision: Three-Layer System

The owner's key insight: Karpathy's pattern should be absorbed into Intent not as a replacement but as **Layer 1** of a three-layer architecture where domain knowledge and software specification remain independent but work together through bidirectional coupling.

**Layer 1 — Domain Knowledge Base** (the Karpathy pattern adapted for product work)
A self-organizing wiki that compiles everything the system knows about the problem domain: user research, personas, journey maps, competitive landscape, business rules, design decisions. Grows through ingest and lint. This is the system's *understanding*.

**Layer 2 — The Transformation Operating System** (Intent's loop)
The notice→spec→execute→observe engine. Domain-agnostic methodology. This is the system's *process*.

**Layer 3 — Software Specification & Code** (the generative output)
Specs, contracts, component designs, and running code. This is what the system *produces*.

### 2.5 Coupling Model: Full Bidirectional

The owner chose full bidirectional coupling — all three layers feed and are fed by each other:

**Flow 1: Domain wiki → Notice.** Compiled wiki surfaces signals (pain points from lint passes, decayed confidence scores, coverage gaps). Beer's System 4 function.

**Flow 2: Notice → Spec with domain wiki queries.** During spec authoring, agents query the domain wiki for relevant personas, journey stages, existing design decisions. Specs reference and link back to domain artifacts.

**Flow 3: Spec → Execute.** Trust-gated agents generate code from specs. Maker-checker pattern.

**Flow 4: Execute → Observe.** Running code emits events: test results, deployment metrics, user behavior, errors.

**Flow 5: Observe → Domain wiki (double-loop learning / Argyris).** Observations update personas, journey maps, and design decisions when reality diverges from models. This is the critical path — the system questions its own assumptions, not just optimizes execution.

**Flow 6: Observe → Spec corpus (single-loop learning).** Spec drift detection, status updates, BDD living docs.

### 2.6 Domain Wiki Content: Both Raw Research and Synthetic Generation

The domain wiki should:
- **Compile from raw research inputs** (interviews, analytics, competitor docs) the way Karpathy compiles from papers
- **Generate synthetic artifacts** (personas, journey maps, design rationale) from signals and specs already in the system
- Both simultaneously — raw research in, synthetic generation across

### 2.7 Product Frameworks Mapped to the Architecture

Five product strategy frameworks independently describe the same compilation pattern:

- **Torres (Opportunity Solution Trees):** The opportunity space IS the domain wiki. Interview-driven restructuring IS the notice phase.
- **Patton (Story Mapping):** The story map backbone IS the compiled domain schema. Stories sliced from the map ARE generated specs.
- **Cagan (Product Model):** Discovery = Layer 1. Delivery = Layer 3. Same empowered team does both. Trust-gated autonomy maps to his team empowerment model.
- **Seiden (Outcomes Over Output):** The observe phase measures behavioral change, not system metrics. The domain wiki contains a causal theory of behavior→impact validated every cycle.
- **Herbig (Impact Mapping):** WHY→WHO→HOW→WHAT→WHETHER provides the traceability schema linking strategic goals through personas through outcomes to specs.

### 2.8 Systems Thinking Grounding

Four cybernetic traditions explain WHY the architecture works:

- **Beer (Viable System Model):** Layer 1 = System 4+5 (intelligence + identity). Layer 2 = System 2+3 (coordination + management). Layer 3 = System 1 (operations). The 3-4 Homeostat (bidirectional coupling between ops and intelligence) is the most important interface.
- **Argyris (Double-Loop Learning):** Flow 5 (observe → domain wiki) enables the system to question its governing variables, not just optimize execution. Without this, only single-loop learning is possible.
- **Boyd (OODA Loop):** Notice→spec→execute→observe maps to Observe→Orient→Decide→Act but with crucial additions: Orient (the domain wiki) shapes what you observe, and Implicit Guidance & Control lets compiled patterns bypass explicit spec creation for familiar situations.
- **Alexander (Pattern Languages / Systems Generating Systems):** The domain wiki should be structured as a generating system — a pattern language that GENERATES software through rules of combination, not merely describes requirements.

---

## 3. Proposed File System Architecture

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

## 4. Traceability Chain

Every link is bidirectional and navigable through `[[wikilinks]]` and YAML frontmatter:

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

## 5. Documents Produced in This Session

Three documents were created and are available for reference:

1. **Karpathy's LLM Knowledge Bases: The Full Picture** — Complete capture of the tweet, thread, community discourse, resources, and strategic analysis. (~5,000 words)

2. **Structural Parallels: Karpathy × Intent** — Word document (.docx) with side-by-side architecture mapping, five deep parallels, and eight specific recommendations for what Intent should incorporate. Includes callout boxes, comparison tables, and source index.

3. **Formalized Architecture for the Three-Layer Compiled Knowledge System** — The full technical architecture grounding the three-layer system in product frameworks (Torres, Patton, Cagan, Seiden, Herbig) and cybernetic theory (Beer, Argyris, Boyd, Alexander). Includes the complete file system architecture, six bidirectional data flows, the traceability chain, and the technical stack. (~6,000 words)

---

## 6. Eight Specific Recommendations from the Session

These were identified as concrete next steps for Intent:

1. **Add a lint pass to the Observe phase** — A `lint_specs` tool on intent-observe that scans all active specs/contracts for contradictions, orphans, unverified contracts, uncovered signal clusters, and stale specs.

2. **Adopt the index.md + log.md navigation pattern** — Generate and maintain an `_index.md` in `.intent/` listing every active signal, intent, spec, and contract with one-line summaries. Generate a `log.md` appending every event with parseable prefixes.

3. **Introduce the compilation metaphor for spec evolution** — When a capability accumulates enough specs, the LLM generates a compiled overview page synthesizing what the capability does, what's verified, what's outstanding, and how it connects to adjacent capabilities.

4. **Formalize raw/ immutability** — Signals become immutable once captured. Original observation text is never edited. Changes create new signals referencing old ones.

5. **Support ephemeral knowledge bases for complex specs** — When a Spec scores below L3 trust due to low clarity, spawn a temporary research context that compiles relevant signals/specs/decisions into a temporary wiki, uses it to generate a better spec, then discards the scaffolding.

6. **Adopt contamination mitigation** — Add an `origin` field to all artifacts (human | agent | system). Weight human-originated signals differently from agent-originated ones in trust computation.

7. **Build the Obsidian bridge** — Ensure all Intent markdown files are Obsidian-compatible with YAML frontmatter, [[wikilinks]], and typed fields. Publish an Obsidian vault template.

8. **Position Intent as the team-scale version of Karpathy's personal pattern** — His system has one human + one LLM. Intent has multiple humans (teams), multiple agents (subagents), and formal governance (trust scoring, contracts, ARB). Frame explicitly: "Karpathy showed what one person can do with a compiled knowledge base. Intent shows what a team can do with a compiled operating model."

---

## 7. Key Conceptual Vocabulary

| Term | Meaning in This Context |
|------|------------------------|
| Compilation | Transforming raw material into a structured, interlinked, self-auditing artifact (vs. retrieval/RAG which re-derives on every query) |
| Generating system | Alexander's concept: a kit of parts with rules for combination that *produces* things, not the things themselves |
| Double-loop learning | Argyris: questioning governing variables (domain models), not just optimizing within them |
| Single-loop learning | Optimizing execution within existing assumptions |
| 3-4 Homeostat | Beer: the bidirectional coupling between operations and intelligence that keeps a system viable |
| IG&C | Boyd: Implicit Guidance & Control — compiled orientation enabling fast action without explicit decision |
| Contamination | Ango: mixing agent-generated content with human-curated content without tracking provenance |
| Ephemeral wiki | Karpathy: temporary, task-specific knowledge bases spun up for complex questions then dissolved |

---

## 8. What to Do Next

The immediate priorities, in order:

1. **Read the existing Intent codebase** at github.com/theparlor/intent to understand current state
2. **Design the `wiki/` directory schema** — YAML frontmatter templates for personas, journeys, DDRs, themes, domain models
3. **Design the AGENTS.md schema** that will govern the domain wiki's ingest/query/lint operations
4. **Implement the `raw/` → `wiki/` compilation pipeline** as a new capability in the intent-notice or a new intent-wiki MCP server
5. **Add index.md + log.md generation** to the existing MCP servers
6. **Add the lint pass** to intent-observe
7. **Wire the bidirectional flows** — especially Flow 5 (observe → domain wiki, double-loop learning)
8. **Test with a real domain** — use Intent's own dogfooding data as the first raw/ corpus

The owner will provide domain-specific raw material. The system should be ready to ingest it and begin self-organizing the wiki.
