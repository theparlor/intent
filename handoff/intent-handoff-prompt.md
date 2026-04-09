---
title: Intent Handoff Prompt
type: framework
maturity: final
confidentiality: shareable
reusability: universal
domains:
  - consulting-operations
created: 2026-04-08
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
  file_size_kb: 16.5
  content_chars: 15582
  entity_count: 10
  slide_count: 0
  sheet_count: 0
  topic_count: 1
  has_summary: 0
vocab_density: 0.45
related_entities:
  - {pair: mik-kersten ↔ matthew-skelton, count: 17865, strength: 0.993}
  - {pair: mik-kersten ↔ john-kotter, count: 17862, strength: 0.991}
  - {pair: richard-rumelt ↔ mik-kersten, count: 17857, strength: 0.995}
  - {pair: john-kotter ↔ matthew-skelton, count: 17857, strength: 0.99}
  - {pair: richard-rumelt ↔ matthew-skelton, count: 17856, strength: 0.995}
---
# Intent Project: Handoff Context & Prompt

## PROMPT FOR CLAUDE CODE / COWORK

You are continuing work on **Intent**, an open-source operating model for AI-augmented teams. The project lives at `theparlor.github.io/intent` with source at `github.com/theparlor/intent`.

This session produced a major architectural evolution: **integrating Karpathy's LLM Knowledge Base pattern as a self-organizing domain wiki layer that feeds Intent's notice→spec→execute→observe loop, enabling the system to compile raw research into personas, journey maps, and design decisions that generate software specifications.** The domain wiki and software spec layers remain independent but are fully bidirectionally coupled through the Intent loop.

Your job is to help formalize and implement this three-layer architecture within the Intent project.

---

## COMPLETE CONVERSATION CONTEXT

### What happened in this session (in order)

1. **Karpathy tweet research.** We did deep research on Andrej Karpathy's April 2, 2026 tweet about "LLM Knowledge Bases" (x.com/karpathy/status/2039805659525644595). Produced a comprehensive document capturing the full tweet, thread commentary, community discourse, linked resources, and strategic analysis. Key sources: the tweet itself, his GitHub Gist "llm-wiki" (gist.github.com/karpathy/442a6bf555914893e9891c11519de94f), VentureBeat coverage, Extended_Brain Substack's Zettelkasten comparison, Glen Rhodes analysis, DAIR.AI coverage, Antigravity.codes implementation guide.

2. **Structural parallels identified.** We mapped Karpathy's system against Intent across five dimensions: storage mechanism, ingestion/curation, topic-centering, method-vs-content separation, and compounding feedback loops. Produced a formal Word document (`Karpathy-x-Intent-Structural-Parallels.docx`) with side-by-side architecture table and eight specific recommendations for what Intent can absorb.

3. **The critical distinction clarified.** The user identified the most significant difference: **Intent angles toward self-managed code generation for any idea, not self-organizing wikis.** Karpathy builds a knowledge artifact (output = understanding). Intent builds a generative engine (output = running software). Karpathy's loop terminates at understanding. Intent's loop terminates at deployment.

4. **The three-layer synthesis.** The user's key architectural insight: Karpathy's pattern can improve the processes and skills within Intent so the system can **build its own wiki around the thing to be built** — compiling personas, journeys, and designs from raw research — and then use Intent's transformation operating system to generate software specs from that compiled understanding. Domain knowledge and software specification remain independent layers but work together through the Intent loop.

5. **Bidirectional coupling confirmed.** The user specified:
   - Layer 1 (domain wiki) should compile from BOTH raw research inputs AND synthetic generation from specs/signals already in the system
   - All three layers are fully bidirectionally coupled: wiki feeds Notice, Spec queries the wiki, Observe updates BOTH the wiki and the spec corpus simultaneously

6. **Formalized architecture produced.** Deep research mapped the three-layer system against five product strategy frameworks (Torres, Patton, Cagan, Seiden, Herbig) and four systems thinking traditions (Beer's VSM, Argyris' double-loop learning, Boyd's OODA, Alexander's pattern languages). Produced a comprehensive architecture document with file system layout, six bidirectional data flows, the full traceability chain (raw research → persona → journey step → design decision → spec → code), and technical stack recommendations.

---

## THE THREE-LAYER ARCHITECTURE

### Layer 1: Domain Knowledge Base (Karpathy pattern)
A self-organizing wiki that compiles everything the system knows about the problem domain. Uses Karpathy's ingest/query/lint operations adapted for product artifacts.

**Contains:** Personas, journey maps, design decision records (DDRs), research themes, domain models, design rationale, traceability matrix, master index, activity log.

**Fed by:** Raw research (interviews, analytics, competitor docs, support tickets) AND synthetic generation from specs/signals already in the system.

**Self-organizes through:** Ingestion (new source → LLM compiles into wiki pages, touches 10-15 pages per source), query (answers filed back as new wiki pages), lint (contradictions, orphans, stale claims, missing cross-refs, coverage gaps).

### Layer 2: Transformation Operating System (Intent's loop)
The notice→spec→execute→observe engine. Domain-agnostic methodology. Orchestrates the handoff between understanding and action.

**Contains:** The methodology itself, trust scoring formula, autonomy levels (L0-L4), MCP server architecture (intent-notice, intent-spec, intent-observe), signal lifecycle, event stream.

**Key role:** Bidirectional coupling mechanism between Layer 1 and Layer 3. The loop doesn't just produce specs — it updates domain understanding based on what happens when specs are executed.

### Layer 3: Software Specification & Code
The actual specs, contracts, component designs, and running code.

**Contains:** Feature specs (SDD-style), API contracts, component specs, BDD/Gherkin tests (living documentation), design tokens, source code.

**Fed by:** Specs generated against compiled domain knowledge (Layer 1) through the Intent loop (Layer 2).

### The six bidirectional data flows

1. **Domain wiki → Notice:** Wiki lint surfaces signals (pain points without DDRs, decayed confidence, contradictions)
2. **Notice → Spec with wiki queries:** During spec authoring, LLM queries wiki for relevant personas, journeys, existing DDRs
3. **Spec → Execute:** Trust-gated agents generate code from specs (maker-checker pattern)
4. **Execute → Observe:** Running code emits events (test results, metrics, user behavior)
5. **Observe → Domain wiki (double-loop):** Observations update personas, journey maps, DDRs — questioning assumptions, not just optimizing execution
6. **Observe → Spec corpus (single-loop):** Spec drift detection, status updates, living doc sync

### Proposed file system

```
intent-project/
├── raw/                          # Immutable source material
│   ├── research/                 # Interview transcripts, surveys
│   ├── analytics/                # Exported reports, dashboards
│   ├── competitors/              # Competitor analyses
│   └── support/                  # Ticket exports, session recordings
├── wiki/                         # LLM-compiled domain knowledge (Layer 1)
│   ├── _index.md                 # Master catalog (LLM-maintained)
│   ├── personas/                 # Generated persona files
│   ├── journeys/                 # Generated journey maps
│   ├── decisions/                # Design Decision Records
│   ├── themes/                   # Research themes and insights
│   ├── domain-models/            # Glossary, bounded contexts
│   ├── design-rationale/         # Why-level documentation
│   ├── traceability.md           # Cross-artifact link matrix
│   └── log.md                    # Chronological activity log
├── specs/                        # Generated specifications (Layer 3)
│   ├── features/                 # Feature specs (SDD-style)
│   ├── api/                      # API contracts
│   ├── components/               # Component specs + design tokens
│   └── tests/                    # BDD/Gherkin living docs
├── src/                          # Running code
├── observations/                 # Runtime feedback
│   ├── metrics/                  # Performance, usage analytics
│   └── incidents/                # Error reports, anomalies
├── .intent/                      # Intent system state
│   ├── signals/                  # SIG-NNN markdown files
│   ├── intents/                  # INT-NNN markdown files
│   └── events/                   # events.jsonl
├── spec/                         # Intent specs and contracts
│   ├── SPEC-NNN-*.md
│   └── contracts/CON-NNN.md
└── AGENTS.md                     # Schema: conventions, workflows, templates
```

### The traceability chain

Raw Research → Persona → Journey Step → Pain Point → Design Decision Record → Spec → Contract → Code

Every link is navigable in both directions through `[[wikilinks]]` and YAML frontmatter cross-references. Lint enforces coverage: every persona must be referenced by at least one journey, every DDR must link to a persona and journey stage, every spec must link to a DDR, orphans are flagged.

---

## KEY DESIGN PRINCIPLES (from the research)

1. **Compilation over retrieval.** The domain wiki compiles understanding once and keeps it current. Not RAG. The cross-references are already there. The contradictions are already flagged.

2. **Files as the universal interface.** Plain markdown, git-versioned. No database, no vector store, no proprietary format. Maximally legible to humans, LLMs, and unix tools.

3. **Schema file co-evolution.** AGENTS.md is the constitution — human-maintained, under 300 lines, defining conventions, templates, and workflows. Co-evolved between human and LLM.

4. **Immutable raw/ directory.** Sources are never modified. Signals are immutable once captured. This preserves the audit trail.

5. **Trust-gated autonomy.** `trust = clarity×0.30 + (1/blast_radius)×0.20 + reversibility×0.20 + testability×0.20 + precedent×0.10`. L0-L4 levels.

6. **Double-loop learning.** Observe phase must update Layer 1 (domain understanding), not just Layer 3 (execution). Without this, the system can only optimize execution, never question whether it's building the right thing.

7. **Implicit Guidance & Control.** As the wiki grows richer, well-established patterns should flow from notice to execute without full spec creation. Compiled domain patterns enabling speed.

8. **The human contribution is intent.** Humans source, curate, ask the right questions, and set strategic direction. Everything else is compilation.

---

## FRAMEWORKS MAPPED TO THIS ARCHITECTURE

| Framework | Maps to |
|---|---|
| Torres' Opportunity Solution Trees | Layer 1 self-organizing structure: interviews → opportunity tree → solutions → experiments |
| Patton's Story Mapping | Layer 1 artifact structure: horizontal backbone (journey) + vertical ribs (stories) = compiled domain schema |
| Cagan's Discovery/Delivery | Layer 1 = discovery, Layer 3 = delivery, same team does both, trust-gated autonomy |
| Seiden's Outcomes Over Output | Observe phase semantics: measuring behavioral change, not just system metrics |
| Herbig's Impact Mapping | Traceability architecture: WHY → WHO → HOW → WHAT → WHETHER |
| Beer's Viable System Model | Layer 1 = System 4+5 (intelligence+identity), Layer 2 = System 2+3 (coordination+management), Layer 3 = System 1 (operations) |
| Argyris' Double-Loop Learning | Flow 5: observe updates domain wiki (governing variables), not just specs (execution strategy) |
| Boyd's OODA Loop | Notice→Spec→Execute→Observe is Boyd's loop; wiki is shared Orientation enabling distributed autonomous action |
| Alexander's Pattern Languages | Layer 1 is a generating system (pattern language), not just documentation. It generates specs through rules of combination. |

---

## EIGHT SPECIFIC RECOMMENDATIONS FROM THE PARALLELS ANALYSIS

1. **Add a lint pass to the Observe phase.** A `lint_specs` tool on intent-observe: scan for contradictions between specs, orphan specs, unverified contracts, clustered signals lacking a unifying spec, stale specs superseded by decisions. Output = suggested signals back to Notice.

2. **Adopt the index.md + log.md pattern.** Generate `_index.md` in .intent/ listing every active signal, intent, spec, contract with one-line summary and status. Generate `log.md` appending every event with parseable prefixes. Primary entry point for any LLM agent.

3. **Introduce compilation for spec evolution.** When a capability accumulates enough specs, LLM generates a compiled overview page synthesizing what the capability does, what's verified, what's outstanding, how it connects to adjacent capabilities.

4. **Formalize raw/ immutability.** Declare signals immutable once captured. Can be dismissed, promoted, annotated — but original text never edited. New understanding = new signal referencing old.

5. **Support ephemeral knowledge bases for complex specs.** When a spec scores below L3 trust due to low clarity, spawn a temporary research context, compile relevant signals/specs/decisions, use it to produce a better spec, then discard the scaffolding.

6. **Adopt contamination mitigation.** Every artifact carries an `origin` field (human | agent | system). Agent-generated specs tagged accordingly. Trust formula can weight human-originated signals differently.

7. **Build the Obsidian bridge.** Ensure all markdown files are Obsidian-compatible with YAML frontmatter and `[[wikilinks]]`. Publish an Obsidian vault template. Every Intent project becomes a browsable, queryable, graph-visualizable knowledge base.

8. **Position Intent as the team-scale Karpathy.** His system = one human curator + one LLM agent. Intent = multiple human curators (teams) + multiple agent roles (subagents) + formal governance (trust scoring, contracts, ARB).

---

## WHAT TO BUILD NEXT

The immediate implementation priority is **a working prototype of Layer 1 (the domain wiki) integrated with Intent's existing MCP servers.** This means:

1. Define the AGENTS.md schema for the wiki/ directory — artifact templates, YAML frontmatter conventions, cross-reference rules, ingest/query/lint workflows.

2. Implement the `ingest` operation: drop a source in raw/, LLM reads it, creates/updates summary + relevant persona/journey/theme/decision pages, updates _index.md, appends to log.md.

3. Implement the `query` operation: ask a question, LLM reads _index.md to find relevant pages, synthesizes answer with [[citations]], offers to file answer as new wiki page.

4. Implement the `lint` operation: scan wiki for contradictions, orphans, missing cross-refs, coverage gaps, staleness. Output = suggested signals for the Notice phase.

5. Wire Flow 2: during spec authoring in the intent-spec MCP server, the LLM queries the wiki for relevant personas, journeys, and DDRs before writing the spec.

6. Wire Flow 5: in the intent-observe MCP server, add a `update_domain_wiki` tool that takes observation events and proposes updates to Layer 1 artifacts.

---

## PROJECT LINKS

- **Project site:** https://theparlor.github.io/intent
- **GitHub repo:** https://github.com/theparlor/intent
- **Pitch:** https://theparlor.github.io/intent/pitch.html
- **Methodology:** https://theparlor.github.io/intent/methodology.html
- **Architecture:** https://theparlor.github.io/intent/architecture.html
- **Concept Brief:** https://theparlor.github.io/intent/concept-brief.html
- **Karpathy's tweet:** https://x.com/karpathy/status/2039805659525644595
- **Karpathy's Gist (llm-wiki.md):** https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f

---

## USER CONTEXT

The person building Intent is an engineer/architect/system designer focused on product first principles, design thinking, and strategic business alignment. They follow Marty Cagan, Jeff Patton, Tim Herbig, Teresa Torres, Josh Seiden, Jeff Gothelf, and related thought leaders. They are a highly visual thinker who connects with storytelling and analogies. Frame technical decisions in terms of the product strategy implications, not just implementation details.
