---
id: SIG-2026-05-26-KNOWLEDGE-SERVER-SUBSTRATE-VERBS
timestamp: 2026-05-26T23:55:00Z
source: code-implementation
author: claude-opus-4-7
confidence: 0.92
trust: 0.85
autonomy_level: L4
status: symptom-repaired, upstream-pending
cluster: substrate-exposure
related_decisions:
  - DEC-010
  - DEC-011
related_signals:
  - 2026-05-26-entire-scope-audit-and-observability-delta
spec_references:
  - spec/substrate-exposure-architecture.md
  - spec/decision-log.md (DEC-010)
upstream_control_path:
  - servers/knowledge.py
  - servers/lib/classification.py
catch_mechanism: servers/test_knowledge.py
pipeline_survival: YES
---

# Knowledge server: substrate-exposure verbs (DEC-010)

## What landed

Five new read verbs on the `intent-knowledge` MCP server (port 8004),
per DEC-010 and substrate-exposure-architecture.md §Phase 1:

| Verb | File | Lines added |
|---|---|---|
| `query(text, scope_token, k)` | `servers/knowledge.py` | ~90 |
| `get(entity_id, scope_token)` | `servers/knowledge.py` | ~80 |
| `list_entities(type, filter, scope_token, limit)` | `servers/knowledge.py` | ~60 |
| `lineage(signal_id, scope_token, depth)` | `servers/knowledge.py` | ~60 |
| `freshness(path, scope_token)` | `servers/knowledge.py` | ~70 |

Supporting modules:

- `servers/lib/classification.py` — load-bearing policy enforcement: `Classification`, `ClassificationResolver`, `in_scope()`, `validate_scope_token()`. Reads `.intent/classification.yaml` walking up from any entity path; per-request cache. Default tier `internal` per DEC-011. Three scope tokens (`public` / `internal` / `engagement:<slug>`) with binary match rules.
- `servers/lib/lineage.py` — backward/forward graph traversal honoring `caused_by` / `parent_signal` / `supersedes` (backward) and `causes` / `related_intents` / `promotes_to` (forward). Bounded depth (default 3, max 5). Truncates at scope boundaries with explicit marker.
- `servers/lib/library_index_client.py` — clean stub interface + `repo_keyword_fallback()` (coarse keyword scoring across every `.intent/{signals,intents,specs,decisions,contracts}/` tree).

## Closure-DoD posture

- **upstream_control_path:** `servers/knowledge.py` + `servers/lib/classification.py` are the implementation. Code is the procedure.
- **catch_mechanism:** `servers/test_knowledge.py` — 33 tests, all passing. Coverage: classification module unit tests (7), all five verbs (24), library-index client behavior (2), server-import smoke (1).
- **pipeline_survival:** YES. The substrate-exposure logic IS code, not a derived artifact. `python servers/knowledge.py` starts the FastMCP server cleanly (validated 2026-05-26 23:52 ET on port 18004).

## Why `symptom-repaired, upstream-pending`

The three Closure-DoD assertions all hold for **the substrate-exposure verbs themselves** — code, tests, server starts. The library-index integration is wired (Phase 1 client per Agent 3's investigation), but BM25+vector ranking still depends on a Port A extension to library-index-mcp:

**Library-index status: Phase 1 wired, Phase 2 deferred.**
- `servers/lib/library_index_client.LibraryIndexClient.query()` now reads `~/Workspaces/CATALOG.json` directly and ranks assets by `word_hits * 0.3 + depth_score * 0.7` — the depth-sorted keyword path documented in `spec/library-index-composition-investigation-2026-05-26.md`. Falls back to `repo_keyword_fallback()` only when CATALOG.json is unreadable.
- Each `query` response carries `library_index_status` describing which path served the request.
- BM25+vector still requires the Port A extension recommended by the investigation (`library_search_ranked` in `Core/products/library-index-mcp/server.py`, half-day effort). When that lands, swap `_search_via_catalog` for the MCP call — no `knowledge.py` change required.

**Upstream gap (named for resolution path):** Port A extension `library_search_ranked` in library-index-mcp. Until then, the `query` verb returns depth+keyword ranking, not true semantic retrieval. This is honest behavior — `library_index_status` exposes it.

**This signal will close to `resolved` when:** `library_search_ranked` is added to `Core/products/library-index-mcp/server.py` and `LibraryIndexClient.query()` is swapped to call it.

## Files (absolute paths)

Created:
- `/Users/brien/Workspaces/Core/frameworks/intent/servers/lib/__init__.py`
- `/Users/brien/Workspaces/Core/frameworks/intent/servers/lib/classification.py`
- `/Users/brien/Workspaces/Core/frameworks/intent/servers/lib/lineage.py`
- `/Users/brien/Workspaces/Core/frameworks/intent/servers/lib/library_index_client.py`
- `/Users/brien/Workspaces/Core/frameworks/intent/servers/test_knowledge.py`
- `/Users/brien/Workspaces/Core/frameworks/intent/servers/README.md`

Modified:
- `/Users/brien/Workspaces/Core/frameworks/intent/servers/knowledge.py` — added 5 verbs + entry point block
- `/Users/brien/Workspaces/Core/frameworks/intent/servers/requirements.txt` — added pyyaml, pytest

## Test results

```
33 passed, 15 warnings in 0.77s
```

Coverage by area:
- Classification module: 7 tests, all pass
- query verb: 4 tests (scope filtering, k bound, invalid token)
- get verb: 6 tests (scope, invalid id, not-found, decision-from-log)
- list_entities verb: 5 tests (scope filtering, type validation, limit cap, substring filter)
- lineage verb: 4 tests (traverse caused_by, scope truncation, out-of-scope root, depth bound)
- freshness verb: 4 tests (mtime, scope, path traversal, not-found)
- library-index: 2 tests (stub raises, fallback works)
- Server-import smoke: 1 test (all verbs present + bare module imports)

## Next-step pointers

1. Agent 3's library-index integration → swap `LibraryIndexClient.query()` body, close this signal to `resolved`.
2. Agent 1's `.intent/classification.yaml` shape ratification → already aligned with the schema this implementation reads.
3. Deploy to FastMCP Cloud as `intent-knowledge.fastmcp.cloud/mcp` (DEC-010 validation criteria #1) — out of scope here; deployment track.
4. Wire scope_token into chat-surface MCP configs (Cowork, Claude.ai, mobile) per substrate-exposure-architecture.md §Phase 1 step 6 — out of scope here; config track.
