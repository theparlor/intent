---
type: primary-source
depth_score: 4
depth_signals:
  file_size_kb: 8.9
  content_chars: 8647
  entity_count: 0
  slide_count: 0
  sheet_count: 0
  topic_count: 0
  has_summary: 0
vocab_density: 0.23
source: "https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f"
captured: 2026-04-12
origin: agent
confidence: 0.95
related_signals:
  - SIG-025
  - SIG-032
extraction_depth: high
---
# Karpathy "llm-wiki.md" Gist — Full Extraction

Source: https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f
Stars: 1,388 / Forks: 246 (as of April 5, 2026)

## Critical Finding: No YAML Templates

Karpathy does **not** define any YAML frontmatter templates. The only frontmatter reference is in Tips & Tricks:

> "If your LLM adds YAML frontmatter to wiki pages (tags, dates, source counts), Dataview can generate dynamic tables and lists."

He mentions frontmatter as an option but leaves the schema entirely unspecified and domain-dependent. This is deliberate — see the "idea file" concept below.

## Directory Structure

**No prescribed directory structure.** Karpathy explicitly defers:

> "The exact directory structure, the schema conventions, the page formats, the tooling — all of that will depend on your domain, your preferences, and your LLM of choice."

Only structural artifacts named directly:
- `raw/` — implied location for source documents (immutable, LLM reads but never modifies)
- `raw/assets/` — recommended Obsidian attachment folder path for locally downloaded images
- `index.md` — content-oriented catalog file (wiki-level)
- `log.md` — append-only chronological record (wiki-level)

## Three Operations (Verbatim)

### INGEST

> "You drop a new source into the raw collection and tell the LLM to process it. An example flow: the LLM reads the source, discusses key takeaways with you, writes a summary page in the wiki, updates the index, updates relevant entity and concept pages across the wiki, and appends an entry to the log. A single source might touch 10-15 wiki pages. Personally I prefer to ingest sources one at a time and stay involved — I read the summaries, check the updates, and guide the LLM on what to emphasize. But you could also batch-ingest many sources at once with less supervision. It's up to you to develop the workflow that fits your style and document it in the schema for future sessions."

### QUERY

> "You ask questions against the wiki. The LLM searches for relevant pages, reads them, and synthesizes an answer with citations. Answers can take different forms depending on the question — a markdown page, a comparison table, a slide deck (Marp), a chart (matplotlib), a canvas. The important insight: **good answers can be filed back into the wiki as new pages.** A comparison you asked for, an analysis, a connection you discovered — these are valuable and shouldn't disappear into chat history. This way your explorations compound in the knowledge base just like ingested sources do."

### LINT

> "Periodically, ask the LLM to health-check the wiki. Look for: contradictions between pages, stale claims that newer sources have superseded, orphan pages with no inbound links, important concepts mentioned but lacking their own page, missing cross-references, data gaps that could be filled with a web search. The LLM is good at suggesting new questions to investigate and new sources to look for. This keeps the wiki healthy as it grows."

### INDEX AND LOG

> "**index.md** is content-oriented. It's a catalog of everything in the wiki — each page listed with a link, a one-line summary, and optionally metadata like date or source count. Organized by category (entities, concepts, sources, etc.). The LLM updates it on every ingest. When answering a query, the LLM reads the index first to find relevant pages, then drills into them. This works surprisingly well at moderate scale (~100 sources, ~hundreds of pages) and avoids the need for embedding-based RAG infrastructure."

> "**log.md** is chronological. It's an append-only record of what happened and when — ingests, queries, lint passes. A useful tip: if each entry starts with a consistent prefix (e.g. `## [2026-04-02] ingest | Article Title`), the log becomes parseable with simple unix tools — `grep "^## \[" log.md | tail -5` gives you the last 5 entries. The log gives you a timeline of the wiki's evolution and helps the LLM understand what's been done recently."

## Schema Co-Evolution (Verbatim)

> "**The schema** — a document (e.g. CLAUDE.md for Claude Code or AGENTS.md for Codex) that tells the LLM how the wiki is structured, what the conventions are, and what workflows to follow when ingesting sources, answering questions, or maintaining the wiki. This is the key configuration file — it's what makes the LLM a disciplined wiki maintainer rather than a generic chatbot. **You and the LLM co-evolve this over time as you figure out what works for your domain.**"

> "It's up to you to develop the workflow that fits your style and **document it in the schema for future sessions.**"

## The "Idea File" Concept (Verbatim)

Opening:
> "This is an **idea file**, it is designed to be copy pasted to your own LLM Agent (e.g. OpenAI Codex, Claude Code, OpenCode / Pi, or etc.). Its goal is to communicate the high level idea, but your agent will build out the specifics in collaboration with you."

Closing:
> "This document is intentionally abstract. It describes the idea, not a specific implementation. The exact directory structure, the schema conventions, the page formats, the tooling — all of that will depend on your domain, your preferences, and your LLM of choice. Everything mentioned above is optional and modular — pick what's useful, ignore what isn't."

> "The right way to use this is to share it with your LLM agent and work together to instantiate a version that fits your needs. The document's only job is to communicate the pattern. Your LLM can figure out the rest."

## Use Cases (Verbatim)

> "This can apply to a lot of different contexts. A few examples:
>
> - **Personal**: tracking your own goals, health, psychology, self-improvement — filing journal entries, articles, podcast notes, and building up a structured picture of yourself over time.
> - **Research**: going deep on a topic over weeks or months — reading papers, articles, reports, and incrementally building a comprehensive wiki with an evolving thesis.
> - **Reading a book**: filing each chapter as you go, building out pages for characters, themes, plot threads, and how they connect. By the end you have a rich companion wiki. Think of fan wikis like Tolkien Gateway — thousands of interlinked pages covering characters, places, events, languages, built by a community of volunteers over years. You could build something like that personally as you read, with the LLM doing all the cross-referencing and maintenance.
> - **Business/team**: an internal wiki maintained by LLMs, fed by Slack threads, meeting transcripts, project documents, customer calls. Possibly with humans in the loop reviewing updates. The wiki stays current because the LLM does the maintenance that no one on the team wants to do.
> - **Competitive analysis, due diligence, trip planning, course notes, hobby deep-dives** — anything where you're accumulating knowledge over time and want it organized rather than scattered."

## Vannevar Bush Memex Connection (Verbatim)

> "The idea is related in spirit to Vannevar Bush's Memex (1945) — a personal, curated knowledge store with associative trails between documents. Bush's vision was closer to this than to what the web became: private, actively curated, with the connections between documents as valuable as the documents themselves. The part he couldn't solve was who does the maintenance. The LLM handles that."

## Gap Analysis for Intent Knowledge Engine

**The gist is intentionally schema-free.** This means there is no artifact-level schema to adopt verbatim. What there IS:

1. **Three-layer architecture** (Raw / Wiki / Schema) — maps directly to KE's Knowledge Farm / Knowledge Engine / schema layer
2. **Three operations** (Ingest / Query / Lint) — maps to KE's ingest → knowledge graph operations
3. **Schema-as-CLAUDE.md** — Karpathy's schema lives in CLAUDE.md/AGENTS.md, exactly how Brien's KE schema works
4. **Log format pattern**: `## [2026-04-02] ingest | Article Title` — parseable prefix convention worth considering for intent journal
5. **"File answers back into wiki"** — query outputs compound the knowledge base. Present in Brien's system but Karpathy's framing is crisper
6. **Memex framing** — Bush's unsolved problem was maintenance cost. LLMs solve maintenance, not retrieval. Directly relevant to Knowledge Farm philosophy.

**What Brien's system has that Karpathy's pattern lacks:** explicit YAML schemas, artifact types, DDRs, signal scoring, autonomy levels, persona layers, freshening schedules, three-ring topology. The Knowledge Engine is a substantial superset. This document is more useful as philosophical validation than schema source.
