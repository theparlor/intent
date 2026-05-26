---
type: implementation-analysis
depth_score: 4
depth_signals:
  file_size_kb: 9.1
  content_chars: 8836
  entity_count: 0
  slide_count: 0
  sheet_count: 0
  topic_count: 0
  has_summary: 0
vocab_density: 0.34
source: "https://github.com/rvk7895/llm-knowledge-bases"
captured: 2026-04-12
origin: agent
confidence: 0.85
related_signals:
  - SIG-032
extraction_depth: high
---
# rvk7895/llm-knowledge-bases — Full Architecture Extraction

**Repo:** github.com/rvk7895/llm-knowledge-bases
**Version:** 1.3.0 (MIT)
**Published:** 2026-04-03
**Attribution at root:** Karpathy's original vision; research subskills from Weizhena/Deep-Research-skills

## 1. Architecture

Pure Claude Code **skills-only** implementation — no MCP server, no Python backend, no vector store. Every operation is a SKILL.md prompt that Claude executes using its native tool access (Bash, Glob, Read, Write, WebSearch, Task/subagents).

**Two-skill core:**
- `kb-init` — one-time vault scaffold + config generation
- `kb` — four operating workflows: compile, query, lint, evolve

**Five attached research subskills** (attributed to Weizhena):
- `research` — structured outline generation
- `research-deep` — parallel subagent execution per outline item
- `research-add-fields` — append field definitions to outline
- `research-add-items` — append subjects to outline
- `research-report` — Python-generated markdown report from JSON results

**Orchestration model — explicitly tiered by model cost:**

| Task | Executor | Verifier |
|---|---|---|
| Index scanning, link checking, file diffing | haiku subagents | none |
| Summarizing individual sources | haiku subagents | opus spot-checks |
| Wiki article writing | sonnet subagents | opus reviews before commit |
| Deep research | sonnet subagents | opus orchestrates + verifies |
| Research synthesis / final reports | opus | none |
| Lint issue detection | sonnet subagents | opus prioritizes + filters |
| Query answering | opus | none |
| Consistency checks | sonnet subagents | opus final judgment |

## 2. YAML Frontmatter Template

```markdown
---
title: "Concept Name"
aliases: [alternate name, abbreviation]
tags: [domain, topic]
sources:
  - "[[raw/articles/source-file.md]]"
created: 2026-04-03
updated: 2026-04-03
---

# Concept Name

Core explanation of the concept.

## Details

Detailed information extracted from sources.

## Relationships

- Related to [[Other Concept]] because...
- Contradicts [[Conflicting Idea]] on the point of...
- Builds on [[Foundation Concept]]

## Sources

- [[raw/articles/source-file.md]] -- key claims extracted from this source
```

Key points: `sources` field stores `[[wikilinks]]` to raw files, not bare paths. The `created`/`updated` date pair supports staleness detection in lint. The `aliases` field resolves alternate names to the same article.

## 3. Directory Structure (kb-init)

```
<vault-root>/
  kb.yaml                  # Config (paths, output formats, obsidian settings)
  CLAUDE.md                # Project-level Claude instructions
  README.md
  raw/
    articles/              # Web articles (from Obsidian Web Clipper)
    papers/                # Academic PDFs
    repos/                 # Cloned/snapshotted GitHub repos
    notes/                 # Local markdown/text
    images/                # Images and diagrams
    transcripts/           # YouTube transcripts
    datasets/              # CSVs, JSON datasets
  wiki/                    # Compiled Obsidian vault content
    _index.md              # Master article list with one-line summaries + compiled-from hashes
    _sources.md            # raw source → wiki article contribution mapping
    _categories.md         # auto-maintained category tree
    _evolution.md          # append-only log of auto-evolve actions
    [category-folders]/    # auto-categorized by Claude as wiki grows
  output/                  # Query results, lint reports, slides, charts
  .obsidian/               # Obsidian vault config
```

**kb.yaml config:**
```yaml
name: "My Knowledge Base"
paths:
  raw: raw/
  wiki: wiki/
  output: output/
output_formats:
  - markdown
  - marp
obsidian:
  wikilinks: true
  recommended_plugins:
    - obsidian-web-clipper
    - obsidian-marp-slides
    - dataview
integrations:
  smaug:
    path: null   # auto-set when Smaug is installed (X/Twitter ingestion)
```

## 4. Cross-References and Index Maintenance

**Three index files maintained after every compile:**

1. **`wiki/_index.md`** — master list: article name, one-line summary, compiled-from hash. This is what Query reads first. The hash enables incremental detection — on next compile, Claude diffs `raw/` against this to find new/changed/deleted files.

2. **`wiki/_sources.md`** — bidirectional map: raw source → which wiki articles it contributed to. Supports the lint check "orphan sources."

3. **`wiki/_categories.md`** — auto-maintained category tree reflecting current folder structure.

4. **`wiki/_evolution.md`** — append-only log format: `YYYY-MM-DD | trigger | action | articles affected`. Written by auto-evolve after every query.

**Cross-reference mechanism:** Pure `[[wikilinks]]`. No markdown-style links allowed for internal references. Enforced in both CLAUDE.md and SKILL.md. Aliases in YAML frontmatter resolve alternate names. Lint check 6 ("missing backlinks") finds references that should be bidirectional but aren't.

**Incremental compile flow:**
1. Read `wiki/_index.md` to get last-compiled hash per source
2. `Glob raw/` recursively
3. Diff → identify new, changed, deleted
4. Only dispatch subagents for what changed
5. Update all four index files after each compile run

## 5. Claude Code Integration (No MCP)

Plugin installation via Claude Code marketplace. Uses standard `.claude-plugin/marketplace.json` and `plugin.json` descriptors.

Maintenance uses Claude Code's native `/loop` and `/schedule` skills for automated lint cadence. No custom scheduler.

Obsidian setup handled by bundled Bash script (`setup.sh`) — downloads community plugins from GitHub releases, writes config JSON. Idempotent.

## 6. Compilation vs. Retrieval

**It is NOT RAG.** No embeddings, no vector store, no semantic search.

**It is LLM-as-compiler** in Karpathy's original sense:
- Claude reads raw source material and writes wiki articles — synthesized, structured, cross-linked
- The wiki IS the compiled artifact, not an index into raw data
- Query discovery uses `_index.md` as primary navigation layer
- Quick queries: indexes + articles only
- Standard queries: supplement with WebSearch when wiki coverage insufficient
- Deep queries: invoke research pipeline (parallel subagents)

**Auto-evolve after query** is key: after every query, a background opus subagent checks whether the answer contained new knowledge not in the wiki. If yes, creates/updates articles silently. Constraint: never creates stubs under 100 words.

## 7. Design Decisions of Note

1. **CLAUDE.md as persistent session memory.** kb-init generates project-level CLAUDE.md so future sessions know they're in a KB project.

2. **LLM owns the wiki, not the human.** "Never manually edit wiki articles outside of the kb skill workflows." Human feeds raw data, LLM maintains compiled artifact.

3. **Hash-based incremental detection.** `_index.md` stores compiled-from hashes, not timestamps. Makes compile genuinely incremental.

4. **Background auto-evolve subagent.** After every query, a `run_in_background: true` opus subagent fires silently. Autonomous knowledge graph maintenance with tight constraints: no deleting, no stubs, re-read before modifying.

5. **Smaug integration for X/Twitter.** Uses npm `@steipete/bird` + Smaug for X ingestion via session cookies. Fallback chain: Smaug → manual paste → Thread Reader App → X data export.

6. **Prompt pinning in research-deep.** "Hard Constraint: The following prompt must be strictly reproduced, only replacing variables in {xxx}, no rewriting of structure or wording allowed." Prevents subagent drift across model updates.

7. **Lint runs fully parallel.** Seven lint check categories as parallel sonnet subagents, collated and false-positive-filtered by opus. Output to `output/lint-YYYY-MM-DD.md`.

8. **No MCP server.** Pure Claude Code skills. Zero external infrastructure.

## Relevance to Intent Knowledge Engine

**Solved same way as KE:**
- Three-tier model hierarchy (haiku/sonnet/opus ≈ KE mechanical/synthesis/orchestration)
- Index-as-navigation-layer rather than RAG
- YAML frontmatter as schema carrier
- Append-only evolution logs (`_evolution.md` ≈ intent journal)

**What they formalized that KE hasn't:**
- Background auto-evolve subagent after every query (autonomous KB enrichment loop)
- Hash-based incremental compile detection
- Explicit lint workflow with 7 parallel check categories
- Smaug integration for X/Twitter ingestion
- Field schema validation via Python
- `_sources.md` bidirectional source→article mapping

**Where KE is more sophisticated:**
- Federated persona registry (no persona layer in rvk7895)
- Attribution chain and lineage tracking
- Intent framework (Notice → Spec → Execute → Observe)
- Engagement-scoped vs. reusable IP separation
- Three-ring topology (no multi-instance concept)
