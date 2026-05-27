---
title: Readme
type: framework
maturity: final
confidentiality: internal
reusability: adaptable
created: 2026-05-27
depth_score: 2
depth_signals:
  file_size_kb: 4.2
  content_chars: 4165
  entity_count: 0
  slide_count: 0
  sheet_count: 0
  topic_count: 0
  has_summary: 0
vocab_density: 0.24
---
# Intent MCP Servers

FastMCP-based servers, one per phase of the Intent loop:

| Server | Port (default) | Phase | Status |
|---|---|---|---|
| `notice.py` | 8001 | Notice | Operational |
| `spec.py` | 8002 | Spec | Operational |
| `observe.py` | 8003 | Execute + Observe | Operational |
| `knowledge.py` | 8004 | Cross-cutting (knowledge + substrate exposure) | Operational |

See `ARCHITECTURE.md` for the per-server agent contract and
`AGENT_DEFINITIONS.md` for the role/responsibility split.

## Setup

```bash
cd /Users/brien/Workspaces/Core/frameworks/intent/servers
python3 -m venv .venv
.venv/bin/pip install -r requirements.txt
```

Dependencies: `fastmcp>=2.0`, `pyyaml>=6.0` (substrate exposure), `pytest>=8.0` (tests).

## Run a server

```bash
# Knowledge / substrate exposure
.venv/bin/python knowledge.py

# Notice
.venv/bin/python notice.py

# Spec
.venv/bin/python spec.py

# Observe
.venv/bin/python observe.py
```

Each server uses `port_resolver.py` — preferred port + fallback range.
Override with the per-server env var:

| Server | Env var |
|---|---|
| `notice` | `INTENT_NOTICE_PORT` |
| `spec` | `INTENT_SPEC_PORT` |
| `observe` | `INTENT_OBSERVE_PORT` |
| `knowledge` | `INTENT_KNOWLEDGE_PORT` |

Common: `INTENT_MCP_HOST` (default `0.0.0.0`), `INTENT_MCP_PORT_FALLBACK_COUNT` (default 4).

## Run tests

```bash
.venv/bin/python -m pytest test_knowledge.py -v
```

The test suite covers:
- Classification module (default tier, walk-up resolution, scope matching, malformed YAML)
- All five substrate-exposure verbs (`query`, `get`, `list_entities`, `lineage`, `freshness`)
- library-index stub + repo-keyword fallback path
- Server import smoke test (`python servers/knowledge.py` imports cleanly)

## Knowledge server: substrate exposure (DEC-010)

Per DEC-010 (2026-05-26), `knowledge.py` exposes five additional read verbs
for cross-surface substrate exposure on top of the existing knowledge-engine
verbs:

| Verb | Returns | Bound |
|---|---|---|
| `query(text, scope_token, k=10)` | Top-K relevance-ranked chunks | k default 10, max 25 |
| `get(entity_id, scope_token)` | Single entity body | One entity per call |
| `list_entities(type, filter, scope_token, limit=20)` | Shaped summaries | Default 20, max 50 |
| `lineage(signal_id, scope_token, depth=3)` | Backward + forward chain | Default depth 3, max 5 |
| `freshness(path, scope_token)` | mtime + size + tier + last_event | Single path |

Every verb takes a `scope_token` argument enforced binarily against each
entity's `.intent/classification.yaml`:

```yaml
tier: internal       # public | internal | confidential:<engagement-slug>
declared_at: 2026-05-26
declared_by: brien
notes: ""
```

Scope match rules:

| scope_token | Matches tier(s) |
|---|---|
| `public` | `public` |
| `internal` | `public`, `internal` |
| `engagement:<slug>` | `public`, `internal`, `confidential:<slug>` (exact) |

Out-of-scope behavior per verb:
- `query`: omit hit from results (with `omitted_out_of_scope` counter)
- `get`: `{"error": "out_of_scope", ...}`
- `list_entities`: omit from list
- `lineage`: truncate at boundary, emit `"lineage continues outside your scope"` marker
- `freshness`: `{"error": "out_of_scope", ...}`

Default tier when `classification.yaml` absent: `internal` (per DEC-011).

## library-index composition

The `query` verb composes with library-index (BM25 + vector retrieval over
the 39k+ file knowledge graph) per substrate-exposure-architecture.md §Q4.

**Phase 1 status:** `servers/lib/library_index_client.py` is a stub. It
raises `NotImplementedError` on `.query()`; the MCP server catches this
and falls back to `repo_keyword_fallback()` (coarse keyword scoring across
every `.intent/{signals,intents,specs,decisions,contracts}/` tree under
the repo). Each response includes `fallback_used` and `library_index_status`
so callers can see which path served them.

**Phase 1 → Phase 2 wire-up:** when the library-index integration path is
resolved (see `spec/library-index-composition-investigation-2026-05-26.md`),
replace `LibraryIndexClient.query()` with the real call. No knowledge.py
change is needed — the client is the sole composition seam.
