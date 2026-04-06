---
title: 2026 04 02 Karpathy Llm Knowledge Bases
type: framework
maturity: final
confidentiality: shareable
reusability: universal
domains:
  - consulting-operations
created: 2026-04-06
depth_score: 4
depth_signals:
  file_size_kb: 9.5
  content_chars: 9316
  entity_count: 0
  slide_count: 0
  sheet_count: 0
  topic_count: 1
  has_summary: 0
vocab_density: 0.11
---
# Karpathy's LLM Knowledge Bases: The Full Picture

**Andrej Karpathy revealed the most consequential shift in how elite practitioners use LLMs — from generating code to compiling knowledge.** On April 2, 2026, the former Director of AI at Tesla and OpenAI co-founder posted a detailed workflow on X describing how he now spends more tokens manipulating structured knowledge than writing code. The post generated 25,000+ likes, a VentureBeat feature, a formalized GitHub Gist, an open-source implementation, a DAIR.AI virtual event, and a wave of blog analysis.

---

## The Core Concept: LLMs as Knowledge Compilers

Karpathy's post, titled "LLM Knowledge Bases," opens with the key insight: a large fraction of his recent token throughput goes less into manipulating code and more into manipulating knowledge stored as markdown and images. Most people treat LLMs as transactional — ask a question, get an answer, close the tab. Karpathy describes a fundamentally different pattern where LLMs build persistent, compounding knowledge artifacts.

### Three-Layer Architecture

1. **Raw sources** (`raw/`) — An immutable directory of articles, papers, repos, datasets, and images that serve as the source of truth. The LLM reads but NEVER modifies these.
2. **The wiki** (`wiki/`) — A growing collection of LLM-generated markdown files with summaries, entity pages, concept articles, backlinks, and cross-references. The LLM owns this layer entirely; Karpathy rarely touches it directly.
3. **The schema** (`CLAUDE.md` or `AGENTS.md`) — A configuration file that tells the LLM how the wiki is structured and what workflows to follow. This schema co-evolves between human and LLM over time.

### Three Core Operations

**Ingest:** Drop a new source into `raw/`, and the LLM reads it, discusses key takeaways, writes a summary, updates the index, revises relevant entity and concept pages across the wiki, and appends an entry to a chronological log. A single source might touch 10–15 wiki pages.

**Query:** Ask questions against the wiki, with answers rendered as markdown files, Marp slide decks, matplotlib charts, or dynamic HTML. Critically, good answers get filed back into the wiki as new pages, creating a compounding feedback loop.

**Lint:** Periodic health checks where the LLM scans for contradictions, stale claims, orphan pages, missing cross-references, and data gaps that could be filled with a web search.

At the time of posting, Karpathy's research wiki on a single topic had grown to ~100 articles and ~400,000 words. He expected to need complex RAG pipelines but found the LLM's ability to navigate via auto-maintained index files and brief document summaries was more than sufficient at this scale.

---

## The Toolchain

- **Obsidian** — The "IDE frontend." Karpathy has the LLM agent on one side and Obsidian on the other, browsing results in real time. His analogy: "Obsidian is the IDE; the LLM is the programmer; the wiki is the codebase."
- **Obsidian Web Clipper** — Browser extension converting web articles to clean markdown files
- **Custom hotkey (Ctrl+Shift+D)** — Downloads all images from a clipped article to local storage for LLM vision access
- **Marp** — Markdown-based slide deck format with Obsidian plugin
- **Matplotlib** — Inline data visualizations
- **Dataview** — Obsidian plugin running queries over page frontmatter YAML
- **qmd** — Local search engine for markdown files with hybrid BM25/vector search and LLM re-ranking (CLI and MCP server)
- **Git** — Version history and collaboration

### Two Special Navigation Files

- **index.md** — Content catalog: every page listed with link, one-line summary, metadata, organized by category. LLM reads it first when answering queries.
- **log.md** — Chronological, append-only record of ingests, queries, and lint passes with consistent prefixes parseable with unix tools.

---

## The GitHub Gist: "llm-wiki"

Two days after the tweet, Karpathy published a formal GitHub Gist (gist.github.com/karpathy/442a6bf555914893e9891c11519de94f) — a complete "idea file" designed to be copy-pasted into any LLM agent. Includes the full architecture, all three operations, use cases (personal, research, reading a book, business/team), and the philosophical note that the pattern realizes Vannevar Bush's 1945 Memex vision. Karpathy writes: "Bush's vision was closer to this than to what the web became. The part he couldn't solve was who does the maintenance. The LLM handles that."

---

## Thread Highlights from Karpathy

**On ephemeral wikis:** "You could imagine that every question to a frontier-grade LLM spawns a team of LLMs to automate the whole thing: iteratively construct an entire ephemeral wiki, lint it, loop a few times, then write a full report. Way beyond a `.decode()`."

**On the current workflow:** "At the moment it's not a fully autonomous process. I add every source manually, one by one and I am in the loop, especially in early stages. After a while, the LLM 'gets' the pattern and the marginal document is a lot easier."

**On the product gap:** "I think there is room here for an incredible new product instead of a hacky collection of scripts."

**On future direction:** Using the wiki to generate synthetic training data and fine-tune an LLM so it "knows" the data in its weights — turning a personal knowledge base into a personalized model.

---

## Community Discourse

### Validation from Heavyweights

**Lex Fridman:** Uses a similar setup, adds dynamic visualization: "I often have it generate dynamic HTML with JavaScript that allows me to sort/filter data." Novel use case: generating a temporary mini-knowledge-base loaded into an LLM for voice-mode interaction on 7–10 mile runs.

**Steph Ango (CEO of Obsidian):** Introduced "contamination mitigation" — keeping a high-signal personal vault with known content origins separate from a "messy vault" for agent-generated content. "The knowledge management equivalent of separating production from staging."

### Business Opportunity Recognition

**Vamshi Reddy:** "Every business has a raw/ directory. Nobody's ever compiled it. That's the product." Karpathy agreed.

**Eugen Alpeza (CEO of Edra):** "The jump from personal research wiki to enterprise operations is where it gets brutal. Thousands of employees, millions of records, tribal knowledge that contradicts itself across teams."

**Ole Lehmann:** "Whoever packages this for normal people is sitting on something massive."

### The Simplicity Faction

**Jason Paul Michaels:** "No vector database. No embeddings... Just markdown, FTS5, and grep. Every bug fix gets indexed. The knowledge compounds."

### Thoughtful Pushback

**Extended_Brain (Substack):** Compared Karpathy's system to Niklas Luhmann's Zettelkasten. Core argument: "Luhmann's Zettelkasten is the exercise. Karpathy's wiki is the report from the trainer." When you manually rewrite and categorize knowledge, the cognitive work produces understanding. Conclusion: "Use the machine to build the map, then insist on walking the territory yourself."

**Glen Rhodes:** Identified the accessibility barrier: "It requires you to be Andrej Karpathy to set it up."

**Hallucination compounding risk:** Multiple commenters noted that if the LLM hallucinates a connection during compilation, it persists and potentially gets reinforced through subsequent operations.

---

## Karpathy's Intellectual Arc

This tweet is the culmination of a clear trajectory:

- **Feb 2025: "Vibe coding"** — Code becomes cheap and disposable. If code generation is free, what becomes the scarce resource?
- **Apr 2025: "Power to the People"** — LLMs uniquely benefit individuals more than corporations — a reversal of every prior technology diffusion pattern.
- **Dec 2025: "Never felt this behind as a programmer"** — A new programmable layer of abstraction involving agents, subagents, prompts, contexts, memory, modes, tools, plugins, MCP, workflows.
- **Feb 2026: "Bespoke software"** — Vibe-coded a custom cardio tracking dashboard in one hour. "The 'app store' of discrete apps is an increasingly outdated concept."
- **Mar 2026: Autoresearch** — GitHub repo (65K+ stars) running LLM agents in autonomous ML research loops.
- **Apr 2026: LLM Knowledge Bases** — The synthesis: once code generation is "solved enough," the frontier moves to knowledge orchestration.

---

## Complete Resource Index

### Primary Sources from Karpathy
- Original tweet (April 2, 2026): x.com/karpathy/status/2039805659525644595
- GitHub Gist "llm-wiki.md" (April 4, 2026): gist.github.com/karpathy/442a6bf555914893e9891c11519de94f
- Bear Blog: karpathy.bearblog.dev/blog/
- Autoresearch repo: github.com/karpathy/autoresearch

### Major Coverage
- VentureBeat: "Karpathy shares 'LLM Knowledge Base' architecture that bypasses RAG" (April 4, 2026)
- Extended_Brain Substack: "The Wiki That Writes Itself"
- Glen Rhodes: "The Personal Computing Shift Nobody's Talking About"
- DAIR.AI Academy: Interactive architecture diagram + virtual event (April 29)
- Antigravity.codes: "The Post-Code AI Workflow"

### Tools
- Obsidian, Obsidian Web Clipper, Marp, Dataview, qmd, matplotlib

### Open-Source Implementation
- rvk7895/llm-knowledge-bases — Claude Code plugin implementing /kb-init, /kb compile, /kb query, /kb lint
