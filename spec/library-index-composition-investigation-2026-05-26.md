---
title: library-index ↔ intent-knowledge composition investigation
type: investigation-report
created: 2026-05-26
related: DEC-010, WS-DDR-099, WS-DDR-080, WS-DDR-083, WS-DDR-084
depth_score: 4
depth_signals:
  file_size_kb: 9.7
  content_chars: 9586
  entity_count: 0
  slide_count: 0
  sheet_count: 0
  topic_count: 0
  has_summary: 0
vocab_density: 0.10
author: claude-sonnet (substrate-exposure track research)
---
# library-index ↔ intent-knowledge composition investigation

## TL;DR

library-index does **not** have a BM25+vector retrieval API today — its query surface is faceted keyword search over CATALOG.json metadata (depth-sorted substring matching), not ranked chunk retrieval over file content. The `intent-knowledge` server currently uses the same keyword-only approach in `knowledge_query()`. Composing the two for a true BM25+vector `query(text, k=10)` verb requires an API exposure sub-milestone: either adding a ranked-retrieval endpoint to library-index-mcp (Port A extension, half-day cost), or wiring `qmd` (the BM25+vector tool referenced in the cowork handoffs) as the retrieval backend called by intent-knowledge directly (full-day, new dependency).

---

## library-index surface inventory

### What exists today

**`Core/products/library-index/` — data store + enrichment pipeline (no server)**

The product has no HTTP server and no Python module exposing a `query()` function. It is a batch pipeline (`auto_tagger.py`, `enrichment_passes.py`, `concept_fingerprint_pass.py`, `layer0_enhancements.py`, `catalog_generator.py`) that writes to flat files consumed by its sibling:

- `~/Workspaces/CATALOG.json` — asset index with `facet_index`, depth scores, topics, entities
- `~/Workspaces/Core/reference/RELATIONSHIPS.json` — entity co-occurrence graph
- `~/Workspaces/Core/reference/VOCABULARY.yml`, `ACRONYM_DICTIONARY.yml`, etc.

The pipeline has `chromadb==1.5.5` and `sentence-transformers` in requirements.txt (via accelerate/torch/einops chain), but **no code in any pipeline script calls `chromadb` for query or any vector store for retrieval**. chromadb is present in the venv as a dependency-of-a-dependency (docling chain), not as an active retrieval backend. There is no `.chroma/` or `chroma.sqlite3` data directory.

**`Core/products/library-index-mcp/server.py` — the live query surface (Port A: 9 tools)**

This is the real access layer. It exposes Port A (`library_*`) read tools over CATALOG.json and sidecars:

| Tool | What it does | Search type |
|---|---|---|
| `library_search_catalog` | Filter by facet+value | Exact facet lookup |
| `library_compound_search` | Intersect multiple facets | Set intersection |
| `library_search_content` | Keyword in path/topics/entities | Substring match, depth-sorted |
| `library_get_asset` | Full asset metadata by path | Direct lookup |
| `library_read_sidecar` | `.meta.yml` file for any path | Direct lookup |
| `library_get_keystones` | Top-depth assets | Score threshold filter |
| `library_get_relationships` | Entity co-occurrence graph | Exact entity lookup |
| `library_entity_lookup` | NER entity details + file sample | Substring match |
| `library_stats` | Coverage summary | Aggregate |

**`Core/frameworks/intent/servers/knowledge.py` — current intent-knowledge server**

`knowledge_query(question)` does exactly the same thing as `library_search_content`: keyword split → substring match → sort by `score` (word-hit count). No ranking beyond word-frequency. No BM25, no vector comparison. The two products share the same primitive retrieval strategy today.

### What does NOT exist

- No `library_index.query` Python-importable function
- No `/query` HTTP endpoint in library-index or library-index-mcp
- No BM25 index (rank_bm25, Whoosh, Tantivy, or equivalent)
- No vector store with queryable embeddings (`chromadb` is in the venv but unused for retrieval)
- No `qmd` installation or integration (referenced in cowork handoffs as the planned BM25+vector layer — it is not yet wired)

---

## Composition path recommendation

**Recommended: Add a `library_search_ranked` tool to library-index-mcp (Port A extension).**

This is the half-day path. The existing `library_search_content` tool does substring matching over CATALOG.json metadata (path + topics + entity strings). A ranked variant can reuse this same in-memory CATALOG.json load and apply BM25 scoring over the `content_excerpt` field in each asset's sidecar `.meta.yml` file.

The retrieval chain for intent-knowledge becomes:

1. `intent-knowledge.knowledge_query(question)` calls `library_search_ranked(query, k)` via a thin HTTP or subprocess call to library-index-mcp
2. library-index-mcp loads sidecars for the top-N CATALOG.json hits, scores them with BM25 over `content_excerpt` + `summary` fields, returns ranked results
3. intent-knowledge wraps results in citation pointers and returns to caller

**Alternative: Wire `qmd` as the retrieval backend (full-day, new dependency)**

The cowork handoffs (`handoff/2026-05-26-substrate-exposure-and-witness-entire-composition.md`, `handoff/01-karpathy-llm-knowledge-bases-full-picture.md`) reference `qmd` — a local hybrid BM25+vector search engine for markdown files with an MCP server. This is the architecturally correct answer for true semantic retrieval but requires: (a) qmd installation + index build over `~/Workspaces/`, (b) deciding whether qmd runs as a sibling MCP server or as a library called by intent-knowledge, (c) managing a persistent index that needs incremental updates as the nightly pipeline runs. This is correct but is a multi-step sub-milestone, not a half-day drop-in.

---

## The client interface intent-knowledge should implement

```python
import json
import subprocess
from pathlib import Path
from typing import Optional

class LibraryIndexClient:
    """
    Thin adapter from intent-knowledge to library-index-mcp.

    Today: calls library_search_content via subprocess to library-index-mcp
    (or directly imports CATALOG.json as a fallback).

    Phase 2: replace _search_via_catalog with a ranked BM25+vector call
    to library_search_ranked once that Port A tool is added to
    Core/products/library-index-mcp/server.py.
    """

    CATALOG_PATH = Path.home() / "Workspaces" / "CATALOG.json"

    def __init__(self):
        self._catalog: Optional[dict] = None

    def _load_catalog(self) -> dict:
        if self._catalog is None:
            with open(self.CATALOG_PATH) as f:
                self._catalog = json.load(f)
        return self._catalog

    def query(self, text: str, k: int = 10) -> list[dict]:
        """
        Returns top-k ranked chunks relevant to text.

        Current implementation: depth-sorted keyword match over CATALOG.json.
        Future: BM25+vector via library_search_ranked (Port A extension).

        Each result: {path, chunk, score, entity_id (optional)}
        """
        catalog = self._load_catalog()
        query_lower = text.lower()
        results = []

        for asset in catalog.get("assets", []):
            searchable = " ".join([
                asset.get("path", ""),
                " ".join(asset.get("topics", [])),
                " ".join(str(e) for e in asset.get("entities", [])),
            ]).lower()
            word_hits = sum(1 for w in query_lower.split() if len(w) > 3 and w in searchable)
            if word_hits > 0:
                results.append({
                    "path": asset["path"],
                    "chunk": asset.get("summary", asset.get("path", "")),
                    "score": word_hits * 0.3 + asset.get("depth_score", 0) * 0.7,
                    "entity_id": asset.get("entities", [None])[0],
                })

        results.sort(key=lambda x: x["score"], reverse=True)
        return results[:k]
```

**How this maps to library-index's actual surface:**

The `_load_catalog()` call reads `~/Workspaces/CATALOG.json` directly — same file that library-index-mcp loads. intent-knowledge can import this as a Python library (direct import path: none today, would need packaging) or replicate the CATALOG.json load pattern above. The simpler path is the direct file read shown above, which avoids the MCP protocol hop.

For the Port A extension, intent-knowledge would change to:

```python
# Phase 2 client — calls library_search_ranked once it exists in server.py
result = await call_mcp_tool("library_search_ranked", {"query": text, "k": k})
# returns SPEC-001-enveloped list of {path, score, excerpt, entity_ids}
```

---

## Open questions

1. **Does the BM25+vector layer need to live in library-index-mcp (Port A) or should intent-knowledge own it?** The cleanest answer is Port A — library-index-mcp is the query surface for the knowledge graph, and all consumers (including intent-knowledge) get ranked retrieval for free. But it adds a chromadb/rank_bm25 dependency to the lightweight MCP venv (`requirements.txt` today: only `mcp`, `pydantic`, `pyyaml`). Brien's stated preference (CLAUDE.md) is to keep library-index-mcp lightweight. Slot the question for DEC-010 resolution.

2. **Is `qmd` the right retrieval backend, or is in-process BM25 over sidecar excerpts sufficient?** The `content_excerpt` field in `.meta.yml` sidecars is a 500-char preview, not a full chunk. True chunk retrieval requires either the full file or a chunked index (what qmd builds). If intent-knowledge needs to return actual text chunks (not just file pointers), qmd is required. If returning file paths + excerpts is sufficient, in-process BM25 over sidecars works and avoids the qmd dependency entirely.

3. **WS-DDR-080/083/084 schema-version handshake:** these three DDRs define the `schema_version` + `bundle_min_compatible_version` envelope that all Port A tool responses carry. Any new `library_search_ranked` tool added to library-index-mcp must emit the same SPEC-001 §2 envelope. No new handshake machinery is needed — it inherits from the existing Port A pattern. No conflict.
