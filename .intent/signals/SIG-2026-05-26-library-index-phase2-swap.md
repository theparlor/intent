---
id: SIG-2026-05-26-LIBRARY-INDEX-PHASE2-SWAP
timestamp: 2026-05-27T00:00:00Z
source: code-implementation
author: claude-sonnet-4-6
confidence: 0.95
trust: 0.90
autonomy_level: L4
status: resolved
cluster: substrate-exposure
related_decisions:
  - DEC-010
  - DEC-011
related_signals:
  - SIG-2026-05-26-KNOWLEDGE-SERVER-SUBSTRATE-VERBS
spec_references:
  - spec/library-index-composition-investigation-2026-05-26.md
  - spec/substrate-exposure-architecture.md
upstream_control_path:
  - servers/lib/library_index_client.py
  - Core/products/library-index-mcp/server.py (_build_bm25_index surface)
catch_mechanism: servers/test_knowledge.py (36/36 passing — includes 2 new BM25 tests)
pipeline_survival: YES
supersedes: SIG-2026-05-26-KNOWLEDGE-SERVER-SUBSTRATE-VERBS (upstream-pending gap closed)
---

# Library-index Phase 2 swap: BM25 via direct Python import

## What landed

`servers/lib/library_index_client.py` Phase 1 body (`_search_via_catalog`) replaced
with a Phase 2 BM25 path that calls `library-index-mcp`'s `_build_bm25_index` +
inline `BM25Okapi` directly via `importlib.util.spec_from_file_location`.

## Transport choice: Option A (direct Python import)

Option B (in-process MCP stdio client, spawn subprocess from inside MCP server) was
rejected — known pain point in this codebase. Option C (HTTP dial-in) requires
`--transport http` launch of library-index-mcp, which is not guaranteed. Option A
reuses the exact same BM25 ranking logic without a subprocess, preserves the
architectural "MCP composition" commitment at the user-side (both servers still run
independently), and uses `importlib.util.spec_from_file_location` so no circular
package installs are needed.

Import path resolved via `LIBRARY_INDEX_MCP_ROOT` env var (override for tests) or
hardcoded default `~/Workspaces/Core/products/library-index-mcp/server.py`.

## Fallback chain

```
1. BM25 via library-index-mcp import (Phase 2 — primary)
   └─ _build_bm25_index has its own stdlib BM25Okapi fallback (no rank_bm25 required)
2. Word-hit * 0.3 + depth_score * 0.7 (Phase 1 — when import fails)
3. NotImplementedError raised → caller (knowledge.py query verb) falls back
   to repo_keyword_fallback() (substrate .intent/ file walk)
```

The server never goes dark: defensive except blocks at each transition.

## Files modified

- `/Users/brien/Workspaces/Core/frameworks/intent/servers/lib/library_index_client.py`
  — Phase 2 implementation (BM25 primary path + Phase 1 word-hit fallback + `status()` method)
- `/Users/brien/Workspaces/Core/frameworks/intent/servers/knowledge.py`
  — `li_status` now calls `client.status()` instead of hardcoded string
- `/Users/brien/Workspaces/Core/frameworks/intent/servers/test_knowledge.py`
  — 2 new tests: `test_library_index_client_bm25_returns_hits` +
    `test_library_index_client_bm25_fallback_when_import_fails`

## Test results

36/36 passed (34 existing + 2 new BM25 path + fallback tests). No regressions.

## No requirements.txt change needed

`_build_bm25_index` in library-index-mcp contains a full stdlib `BM25Okapi`
fallback — `rank_bm25` is optional there and not needed here. `pyyaml` was already
in `servers/requirements.txt`; the sidecar-loading path uses it.

## Closure-DoD assertions

- **upstream_control_path:** `servers/lib/library_index_client.py` is the swap
  target. `Core/products/library-index-mcp/server.py` provides `_build_bm25_index`
  — the ranking surface. Both are code; code is the procedure.
- **catch_mechanism:** `servers/test_knowledge.py` 36/36. Covers BM25 primary path
  (synthetic `server.py` with inline BM25Okapi), import-failure fallback to Phase 1
  word-hit scorer, absent-catalog path (NotImplementedError), and all 34 pre-existing
  substrate-exposure verb tests.
- **pipeline_survival:** YES — `python servers/knowledge.py` imports cleanly
  (validated by `test_server_imports_clean`).

All three assertions hold → status: **resolved**.

This closes the upstream-pending gap from SIG-2026-05-26-KNOWLEDGE-SERVER-SUBSTRATE-VERBS.
