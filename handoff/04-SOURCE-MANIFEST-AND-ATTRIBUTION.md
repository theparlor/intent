---
title: 04 Source Manifest And Attribution
type: framework
maturity: final
confidentiality: shareable
reusability: universal
domains:
  - consulting-operations
created: 2026-04-13
thought_leaders:
  - marty-cagan
  - jeff-patton
  - teresa-torres
  - josh-seiden
  - tim-herbig
frameworks:
  - product-operating-model
  - continuous-discovery-habits
  - outcomes-over-output
  - double-loop-learning
depth_score: 6
depth_signals:
  file_size_kb: 23.8
  content_chars: 19076
  entity_count: 9
  slide_count: 0
  sheet_count: 0
  topic_count: 1
  has_summary: 0
vocab_density: 0.47
related_entities:
  - {pair: marty-cagan ↔ teresa-torres, count: 223, strength: 0.4}
  - {pair: jeff-patton ↔ marty-cagan, count: 136, strength: 0.273}
  - {pair: jeff-patton ↔ teresa-torres, count: 133, strength: 0.311}
  - {pair: marty-cagan ↔ product-engineering-coaching, count: 104, strength: 0.092}
  - {pair: josh-seiden ↔ marty-cagan, count: 101, strength: 0.204}
---
# Source Manifest & Attribution Index

## Purpose

This document catalogs every source surfaced during the research session that produced the Intent three-layer architecture. It serves as the provenance layer — ensuring that future agents or humans can trace any claim back to its origin, re-access source material for deeper extraction, and avoid re-discovering previously found material.

**Session date:** April 5, 2026
**Research passes:** 3 (Karpathy tweet capture, structural parallels, three-layer architecture formalization)

---

## How to Use This Document

- Every source has a **category**, **URL**, **what it contributed**, and **retrieval status** (fetched = full content was read; searched = appeared in search results with snippets; referenced = cited by other sources but not directly accessed)
- Sources marked "HIGH EXTRACTION POTENTIAL" contain significant material that was only partially used — future passes should prioritize these
- Sources are grouped by topic cluster for navigability
- If re-running research, start with the "Not Yet Accessed" section at the bottom

---

## A. Karpathy Primary Sources

### A1. The Original Tweet
- **URL:** https://x.com/karpathy/status/2039805659525644595
- **Status:** Fetched (via xcancel.com mirror)
- **What it contributed:** Full tweet text, core concept of LLM Knowledge Bases, three operations (ingest/query/lint), the Obsidian workflow, scale metrics (100 articles, 400K words), the compilation-over-retrieval thesis
- **Extraction completeness:** HIGH — primary content fully captured
- **Note:** Tweet thread replies were partially captured via mirrors; direct X API access was not available

### A2. The GitHub Gist ("llm-wiki.md")
- **URL:** https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f
- **Status:** Fetched (full content read)
- **What it contributed:** Formalized architecture, directory structure, YAML frontmatter templates, all three operation workflows with step-by-step instructions, use cases (personal/research/book/business/team), Vannevar Bush Memex connection, the "idea file" concept, schema co-evolution notes
- **Extraction completeness:** HIGH — fully captured
- **Stars/forks at time of access:** 1,388 stars / 246 forks
- **HIGH EXTRACTION POTENTIAL:** The Gist contains detailed YAML frontmatter templates and workflow specifications that were summarized but not reproduced verbatim. Future passes should extract these templates for direct adaptation into Intent's wiki/ schema.

### A3. Karpathy's Bear Blog
- **URL:** https://karpathy.bearblog.dev/blog/
- **Status:** Referenced (not fetched directly)
- **What it contributed:** Context for intellectual arc — "Power to the People" essay, "2025 LLM Year in Review"
- **HIGH EXTRACTION POTENTIAL:** The "Power to the People" essay (https://karpathy.bearblog.dev/power-to-the-people/) was referenced but not fully read. Contains arguments about LLMs benefiting individuals over institutions that are relevant to Intent's positioning.

### A4. "2025 LLM Year in Review"
- **URL:** https://karpathy.bearblog.dev/year-in-review-2025/
- **Status:** Referenced
- **What it contributed:** Context for Karpathy's broader thesis about LLM evolution
- **HIGH EXTRACTION POTENTIAL:** Not read in this session.

### A5. Vibe Coding Tweet
- **URL:** https://x.com/karpathy/status/1886192184808149383
- **Status:** Referenced
- **What it contributed:** Origin of "vibe coding" concept, Phase 1 of Karpathy's thesis (code becomes cheap)

### A6. "Never Felt This Behind" Tweet
- **URL:** https://x.com/karpathy/status/2004607146781278521
- **Status:** Referenced
- **What it contributed:** Description of new programmable abstraction layer, 14M views

### A7. Bespoke Software Tweet
- **URL:** https://x.com/karpathy/status/2024583544157458452
- **Status:** Referenced
- **What it contributed:** Custom cardio dashboard example, "app store is outdated concept"

### A8. Autoresearch Repo
- **URL:** https://github.com/karpathy/autoresearch
- **Also:** https://github.com/karpathy/autoresearch/blob/master/README.md
- **Status:** Referenced
- **What it contributed:** Context for autonomous ML research loops, 65K+ stars

### A9. LLM Council Repo
- **URL:** https://github.com/karpathy/llm-council
- **Status:** Referenced
- **What it contributed:** Context for multi-LLM evaluation patterns

---

## B. Major Coverage & Analysis of Karpathy's Post

### B1. VentureBeat
- **URL:** https://venturebeat.com/data/karpathy-shares-llm-knowledge-base-architecture-that-bypasses-rag-with-an
- **Status:** Fetched (multiple passages read)
- **What it contributed:** "Direct challenge to SaaS-heavy models like Notion or Google Docs" framing, enterprise implications analysis, comparison to RAG approaches, community reaction synthesis
- **Extraction completeness:** MEDIUM — key passages captured but article contains additional enterprise analysis

### B2. Extended_Brain Substack ("The Wiki That Writes Itself")
- **URL:** https://extendedbrain.substack.com/p/the-wiki-that-writes-itself
- **Status:** Fetched (full content read)
- **What it contributed:** Deep Zettelkasten comparison, "structural cognition" concept, the tension between AI-maintained knowledge and human understanding, the critique that outsourcing filing/cross-referencing may weaken deep understanding
- **Extraction completeness:** HIGH — core argument fully captured
- **HIGH EXTRACTION POTENTIAL:** Contains detailed comparison of Luhmann's 90,000-card system with Karpathy's approach. The epistemological argument about "cognitive work of formulation" is directly relevant to Intent's philosophy of human-in-the-loop.

### B3. Antigravity.codes ("The Post-Code AI Workflow")
- **URL:** https://antigravity.codes/blog/karpathy-llm-knowledge-bases
- **Status:** Fetched
- **What it contributed:** "Once code generation is solved, the conversation must shift to knowledge orchestration" framing, implementation guide perspective, the "post-code" framing
- **Extraction completeness:** MEDIUM

### B4. Antigravity.codes ("The Complete Guide to His Idea File")
- **URL:** https://antigravity.codes/blog/karpathy-llm-wiki-idea-file
- **Status:** Searched (snippets read)
- **What it contributed:** Detailed walkthrough of the GitHub Gist structure
- **HIGH EXTRACTION POTENTIAL:** Contains implementation details not captured in our session.

### B5. Glen Rhodes
- **URL:** https://glenrhodes.com/andrej-karpathys-llm-powered-personal-knowledge-base-workflow-using-markdown-wikis-and-obsidian/
- **Status:** Fetched (multiple passages)
- **What it contributed:** Accessibility critique ("requires you to be Andrej Karpathy"), practical workflow walkthrough, scale limitations analysis, hallucination compounding risk
- **Extraction completeness:** MEDIUM

### B6. DAIR.AI Academy
- **URL:** https://academy.dair.ai/blog/llm-knowledge-bases-karpathy
- **Status:** Searched (snippets read)
- **What it contributed:** Interactive architecture diagram mention, virtual event (April 29) announcement
- **HIGH EXTRACTION POTENTIAL:** Contains an interactive architecture diagram that was not extracted.

### B7. HowAIWorks.ai ("The Karpathy Method")
- **URL:** https://howaiworks.ai/blog/andrej-karpathy-llm-knowledge-bases
- **Status:** Searched (snippets read)
- **What it contributed:** "Building Personal Knowledge Bases with LLMs" framing, method comparison
- **HIGH EXTRACTION POTENTIAL:** Not deeply read.

### B8. Technology Data Bank (dataworldbank.net)
- **URL:** https://www.dataworldbank.net/2026/04/04/karpathy-shares-llm-knowledge-base-architecture-that-bypasses-rag-with-an-evolving-markdown-library-maintained-by-ai/
- **Status:** Searched (snippets read)
- **What it contributed:** Additional coverage perspective, enterprise framing

### B9. a2a-mcp.org
- **URL:** https://a2a-mcp.org/blog/andrej-karpathy-llm-knowledge-bases-obsidian-wiki
- **Status:** Searched (snippets read)
- **What it contributed:** 2026 implementation guide perspective, Obsidian-specific walkthrough

### B10. DEV Community
- **URL:** https://dev.to/rotiferdev/compile-your-knowledge-dont-search-it-what-llm-knowledge-bases-reveal-about-agent-memory-32pg
- **Status:** Searched
- **What it contributed:** "Compile Your Knowledge, Don't Search It" — agent memory implications
- **HIGH EXTRACTION POTENTIAL:** Focuses on agent memory architecture, directly relevant to Intent's MCP server design. Not read in this session.

### B11. Vuink (DAIR.AI mirror)
- **URL:** https://vuink.com/post/npnqrzl-d-dqnve-d-dnv/blog/llm-knowledge-bases-karpathy
- **Status:** Searched
- **What it contributed:** Mirror of DAIR.AI content

### B12. Futurum Group
- **URL:** https://futurumgroup.com/insights/karpathys-thread-signals-ai-driven-development-breakpoint/
- **Status:** Searched
- **What it contributed:** "AI-Driven Development Breakpoint" industry analyst framing
- **HIGH EXTRACTION POTENTIAL:** Industry analyst perspective not captured in this session.

### B13. 36Kr
- **URL:** https://eu.36kr.com/en/p/3638410115976320
- **Status:** Searched
- **What it contributed:** "Karpathy's Tweet Triggers a Magnitude-9 Earthquake Among Developers" — Asian tech media perspective

---

## C. Community Voices in the Thread

### C1. Steph Ango (Obsidian CEO) — Contamination Mitigation
- **URL:** https://x.com/kepano/status/2039831289533227446
- **Status:** Referenced (snippets via coverage articles)
- **What it contributed:** "Keep your personal vault clean and create a messy vault for your agents" — contamination mitigation concept, production/staging metaphor for knowledge management
- **HIGH EXTRACTION POTENTIAL:** Full tweet thread not read. May contain additional Obsidian-specific implementation advice.

### C2. Lex Fridman
- **Status:** Referenced via coverage articles (no direct URL captured)
- **What it contributed:** Dynamic HTML visualization use case, voice-mode interaction on runs use case

### C3. Vamshi Reddy
- **Status:** Referenced via coverage articles
- **What it contributed:** "Every business has a raw/ directory. Nobody's ever compiled it. That's the product."

### C4. Eugen Alpeza (CEO of Edra)
- **Status:** Referenced via coverage articles
- **What it contributed:** Enterprise scaling challenge — thousands of employees, millions of records, contradicting tribal knowledge

### C5. Ole Lehmann
- **Status:** Referenced via coverage articles
- **What it contributed:** Consumer packaging opportunity

### C6. Jason Paul Michaels
- **Status:** Referenced via coverage articles
- **What it contributed:** Anti-complexity case — markdown, FTS5, grep, no vector DB

---

## D. Open-Source Implementations

### D1. rvk7895/llm-knowledge-bases
- **URL:** https://github.com/rvk7895/llm-knowledge-bases
- **Status:** Searched (description read)
- **What it contributed:** Claude Code plugin implementing full /kb-init, /kb compile, /kb query, /kb lint workflow
- **HIGH EXTRACTION POTENTIAL:** This is a working implementation of Karpathy's pattern. Should be deeply studied for Intent's Layer 1 implementation. Not read in this session beyond the README description.

---

## E. Product Strategy Framework Sources

### E1. Teresa Torres — Opportunity Solution Trees
- **URL:** https://www.producttalk.org/opportunity-solution-trees/
- **Status:** Fetched
- **What it contributed:** Full OST framework description, continuous discovery model, tree-structured opportunity mapping, weekly interview cadence, assumption testing
- **Extraction completeness:** HIGH

### E2. Product School — OST Guide
- **URL:** https://productschool.com/blog/product-fundamentals/opportunity-solution-tree
- **Status:** Searched
- **What it contributed:** Additional OST explanation and examples

### E3. Andrew Clark — Continuous Discovery Habits Summary
- **URL:** https://andrewclark.co.uk/product-book-summaries/continuous-discovery-habits
- **Status:** Searched
- **What it contributed:** Torres book summary, core habits framework

### E4. Jeff Patton — Story Mapping (via multiple sources)
- **URLs:**
  - https://productmindset.substack.com/p/2336-a-guide-to-effective-user-stories
  - https://mpug.com/the-big-picture-with-story-map-in-agile-development
  - https://www.avion.io/what-is-user-story-mapping/
  - https://storiesonboard.com/blog/jeff-patton-user-story-mapping
  - https://jeffgothelf.com/blog/okr-and-user-story-mapping/
- **Status:** Searched (snippets from multiple sources)
- **What it contributed:** Story mapping methodology, backbone/rib structure, release slicing, shared understanding concept, Gothelf OKR integration

### E5. Marty Cagan — SVPG
- **URLs:**
  - https://www.svpg.com/discovery-delivery/
  - https://www.svpg.com/the-product-operating-model-an-introduction/
- **Status:** Searched
- **What it contributed:** Discovery-delivery dual track, product operating model, empowered teams, trust-based autonomy

### E6. Agile Academy — Product Operating Model
- **URL:** https://www.agile-academy.com/en/agile-leader/product-operating-model-innovation-agility/
- **Status:** Searched
- **What it contributed:** Cagan's product operating model explained for agile leaders

### E7. Josh Seiden — Outcomes Over Output (via Intercom)
- **URL:** https://www.intercom.com/blog/podcasts/josh-seiden-on-why-product-teams-should-focus-on-outcome-vs-output/
- **Status:** Searched
- **What it contributed:** Outcomes = changes in human behavior that drive business results, logic model (Impact ← Outcomes ← Outputs ← Activities)

### E8. Tim Herbig — Impact Mapping
- **URLs:**
  - https://herbig.co/impact-mapping-product-discovery/
  - https://www.mindtheproduct.com/impact-mapping-tim-herbig-the-product-experience/
- **Status:** Searched
- **What it contributed:** WHY→WHO→HOW→WHAT→WHETHER framework, traceability from goals through personas to features

---

## F. Systems Thinking & Cybernetics Sources

### F1. Stafford Beer — Viable System Model
- **URLs:**
  - https://metaphorum.org/staffords-work/viable-system-model
  - https://www.systemspractice.org/resources/attachment/43a8a71a-31ad-4165-9ba1-a5815b5719f2 (VSM Guide v1.3)
  - https://umbrex.com/resources/frameworks/organization-frameworks/viable-system-model-stafford-beer/
- **Status:** Searched
- **What it contributed:** Five-system model mapping, 3-4 Homeostat concept, Law of Requisite Variety, variety attenuators/amplifiers

### F2. Chris Argyris — Double-Loop Learning
- **URLs:**
  - https://infed.org/dir/welcome/chris-argyris-theories-of-action-double-loop-learning-and-organizational-learning/
  - https://en.wikipedia.org/wiki/Double-loop_learning
  - https://onlinelibrary.wiley.com/doi/10.1111/emre.12615
- **Status:** Searched
- **What it contributed:** Single vs. double-loop learning distinction, governing variables concept, defensive routines, espoused theory vs. theory-in-use gap

### F3. John Boyd — OODA Loop
- **URLs:**
  - https://thedecisionlab.com/reference-guide/computer-science/the-ooda-loop
  - https://strategyu.co/ooda-loop/
  - https://ooda.de/media/chet_richards_-_boyds_ooda_loop.pdf
  - https://www.artofmanliness.com/character/behavior/ooda-loop/
- **Status:** Searched
- **What it contributed:** Full OODA diagram with multiple feedback paths, Orient as central hub, Implicit Guidance & Control concept, Auftragstaktik (mission-type orders), shared orientation enabling distributed action
- **HIGH EXTRACTION POTENTIAL:** Chet Richards' peer-reviewed article on Boyd's OODA Loop (PDF at ooda.de) was not read. Contains the detailed multi-path feedback diagram that maps precisely to Intent's bidirectional flows.

### F4. Christopher Alexander — Pattern Languages / Systems Generating Systems
- **URLs:**
  - https://coevolving.com/blogs/index.php/archive/systems-generating-systems-architectural-design-theory-by-christopher-alexander-1968/
- **Status:** Fetched
- **What it contributed:** "Systems generating systems" concept, the axiom that to make wholes you must design the generating system, accretive growth principle, Quality Without a Name (QWAN)
- **Extraction completeness:** HIGH

---

## G. Technical Architecture Sources

### G1. Martin Fowler — Spec-Driven Development
- **URL:** https://martinfowler.com/articles/exploring-gen-ai/sdd-3-tools.html
- **Status:** Searched
- **What it contributed:** SDD tools survey (Kiro, spec-kit, Tessl), spec-driven development patterns
- **HIGH EXTRACTION POTENTIAL:** Directly relevant to Intent's spec authoring approach. Not deeply read in this session.

### G2. AGENTS.md Specification
- **URL:** https://agents.md/
- **Status:** Searched
- **What it contributed:** AGENTS.md as a standard for LLM agent context files, conventions and structure

### G3. Augment Code — How to Build AGENTS.md
- **URL:** https://www.augmentcode.com/guides/how-to-build-agents-md
- **Status:** Searched
- **What it contributed:** Best practices for agent context files, 300-line limit guidance, human-curated vs. LLM-generated performance difference

### G4. AWS — ADR Process
- **URL:** https://docs.aws.amazon.com/prescriptive-guidance/latest/architectural-decision-records/adr-process.html
- **Status:** Searched
- **What it contributed:** Architectural Decision Record template and process, relevant to DDR design

### G5. CHI 2024 — LLM-Generated Personas
- **URL:** https://dl.acm.org/doi/10.1145/3613905.3650860
- **Status:** Searched
- **What it contributed:** Research confirming LLM-generated personas are indistinguishable from human-written ones in blind evaluation
- **HIGH EXTRACTION POTENTIAL:** Academic paper with methodology details relevant to Intent's persona generation pipeline. Not read beyond abstract.

### G6. Obsidian Linking Guide
- **URL:** https://www.obsibrain.com/blog/obsidian-linking-the-complete-guide-to-connecting-your-notes
- **Status:** Searched
- **What it contributed:** Obsidian [[wikilink]] conventions and best practices

### G7. Event-Driven Architecture
- **URL:** https://insights.daffodilsw.com/blog/event-driven-architecture-explained-with-real-world-examples
- **Status:** Searched
- **What it contributed:** Event-driven architecture patterns relevant to Intent's event bus design

---

## H. Intent Project Sources (Direct Reads)

### H1. Intent Pitch
- **URL:** https://theparlor.github.io/intent/pitch.html
- **Status:** Fetched (full content read)
- **Extraction completeness:** COMPLETE

### H2. Intent Methodology
- **URL:** https://theparlor.github.io/intent/methodology.html
- **Status:** Fetched (full content read)
- **Extraction completeness:** COMPLETE

### H3. Intent Architecture
- **URL:** https://theparlor.github.io/intent/architecture.html
- **Status:** Fetched (full content read)
- **Extraction completeness:** COMPLETE

### H4. Intent Concept Brief
- **URL:** https://theparlor.github.io/intent/concept-brief.html
- **Status:** Fetched (full content read)
- **Extraction completeness:** COMPLETE

### H5. Intent GitHub Repo
- **URL:** https://github.com/theparlor/intent
- **Status:** Referenced (not crawled beyond site pages)
- **HIGH EXTRACTION POTENTIAL:** Repo structure, actual code, issues, and existing .intent/ directory not examined in this session.

---

## I. Sources Referenced But Not Accessed

These appeared in search results or were cited by other sources but were not directly fetched. They represent the next frontier for deeper extraction.

1. **Karpathy "Power to the People" essay** — https://karpathy.bearblog.dev/power-to-the-people/
2. **Karpathy "2025 LLM Year in Review"** — https://karpathy.bearblog.dev/year-in-review-2025/
3. **Chet Richards OODA Loop paper (PDF)** — https://ooda.de/media/chet_richards_-_boyds_ooda_loop.pdf
4. **CHI 2024 LLM Personas paper** — https://dl.acm.org/doi/10.1145/3613905.3650860
5. **Martin Fowler SDD tools survey** — https://martinfowler.com/articles/exploring-gen-ai/sdd-3-tools.html
6. **rvk7895/llm-knowledge-bases repo (full code)** — https://github.com/rvk7895/llm-knowledge-bases
7. **DEV Community agent memory article** — https://dev.to/rotiferdev/compile-your-knowledge-dont-search-it-what-llm-knowledge-bases-reveal-about-agent-memory-32pg
8. **Futurum Group analyst piece** — https://futurumgroup.com/insights/karpathys-thread-signals-ai-driven-development-breakpoint/
9. **DAIR.AI interactive architecture diagram** — https://academy.dair.ai/blog/llm-knowledge-bases-karpathy
10. **Antigravity idea file guide** — https://antigravity.codes/blog/karpathy-llm-wiki-idea-file
11. **Steph Ango full tweet thread** — https://x.com/kepano/status/2039831289533227446
12. **Karpathy autoresearch README** — https://github.com/karpathy/autoresearch/blob/master/README.md
13. **Data Science Dojo autoresearch explainer** — https://datasciencedojo.com/blog/karpathy-autoresearch-explained/
14. **Wiley double-loop learning review paper** — https://onlinelibrary.wiley.com/doi/10.1111/emre.12615
15. **VSM Guide v1.3 (PDF)** — https://www.systemspractice.org/resources/attachment/43a8a71a-31ad-4165-9ba1-a5815b5719f2
16. **Wind4Change Cagan analysis** — https://wind4change.com/product-management-discovery-delivery-inspired-empowered-marty-cagan/
17. **LogRocket dual-track agile** — https://blog.logrocket.com/product-management/dual-track-agile-continuous-discovery/
18. **GitHub pmbod (PM body of knowledge)** — https://github.com/ikostas/pmbod
19. **GoPractice PM reading list** — https://gopractice.io/library/what-product-managers-should-read-and-listen-to-in-2023/
20. **Open Repo Guide (Autoresearch)** — https://openrepoguide.com/
21. **Nanochat explainer** — https://emelia.io/hub/nanochat-karpathy

---

## Summary Statistics

| Category | Sources Found | Sources Fetched (full read) | Sources Searched (snippets) | Referenced Only |
|----------|--------------|---------------------------|---------------------------|----------------|
| Karpathy primary | 9 | 2 | 0 | 7 |
| Coverage & analysis | 13 | 4 | 9 | 0 |
| Community voices | 6 | 0 | 0 | 6 |
| Open-source implementations | 1 | 0 | 1 | 0 |
| Product strategy frameworks | 8+ | 1 | 7+ | 0 |
| Systems thinking & cybernetics | 4 clusters (12+ URLs) | 1 | 11+ | 0 |
| Technical architecture | 7 | 0 | 7 | 0 |
| Intent project | 5 | 4 | 0 | 1 |
| Not yet accessed | 21 | 0 | 0 | 21 |
| **TOTALS** | **~82 distinct sources** | **~12** | **~35** | **~35** |

**Note on "430 sources" claim:** The research tool processes many search results internally across multiple queries. The 82 distinct sources cataloged here represent the deduplicated, unique URLs that contributed material to our analysis. The higher count reflects individual search result entries (many URLs appeared across multiple queries) plus internal processing steps.

---

## Extraction Priority for Next Session

If continuing research, prioritize in this order:

1. **rvk7895/llm-knowledge-bases** (working implementation to study)
2. **Karpathy GitHub Gist YAML templates** (extract verbatim for Intent wiki schema)
3. **Martin Fowler SDD tools** (spec-driven development patterns)
4. **Chet Richards OODA paper** (detailed feedback path diagrams)
5. **CHI 2024 LLM Personas** (methodology for persona generation pipeline)
6. **DEV Community agent memory article** (MCP server design implications)
7. **Intent GitHub repo actual code** (understand current implementation state)
8. **Steph Ango full thread** (Obsidian-specific implementation advice)
