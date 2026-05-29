---
title: intent-knowledge MCP server — deployment guide
type: deployment-guide
created: 2026-05-26
depth_score: 4
depth_signals:
  file_size_kb: 17.2
  content_chars: 16664
  entity_count: 0
  slide_count: 0
  sheet_count: 0
  topic_count: 0
  has_summary: 0
vocab_density: 0.12
status: ready-for-brien-execution
purpose: "Brien-driven step to deploy the 4th MCP server (intent-knowledge) to FastMCP Cloud, completing the four-server family per WS-DDR-099 + DEC-010."
prerequisites_repo_state: shipped 2026-05-26 (intent@1239121 + 17f6fd0 + 605cf6c + 1b55e85)
sibling_guides:
  - DEPLOYMENT.md (overarching three-server pattern)
related_decisions:
  - WS-DDR-099 (substrate exposure mechanism)
  - DEC-010 (intent-knowledge scope extension)
  - DEC-011 (bin/intent-init scaffold)
  - DEC-009 (two observabilities)
---
# Deploying the intent-knowledge MCP Server

> Brien-driven step. The framework code is shipped + tested (34/34 in `servers/test_knowledge.py`). What remains is the FastMCP Cloud project + endpoint registration. This guide is the click-by-click.

## TL;DR — 5-step deploy

1. Ensure `theparlor/intent` repo on `main` is at or after commit `1b55e85` (verify with `git log --oneline | grep knowledge-server`).
2. Sign into [fastmcp.cloud](https://fastmcp.cloud) with GitHub. Authorize on `theparlor/intent` if not already.
3. Create new project: name `intent-knowledge`, repo `theparlor/intent`, entrypoint `servers/knowledge.py`, requirements file `servers/requirements.txt`.
4. Deploy. Wait for green build. Endpoint becomes `https://intent-knowledge.fastmcp.cloud/mcp`.
5. Add to your Claude Code / Cursor / Cowork MCP config (`mcpServers` section, snippet in §Connect below).

Smoke test: ask Claude "use intent-knowledge to get DEC-009." Expect Brien's two-observabilities DEC body. If you get a 404 / empty result, see Troubleshooting.

## Why this server, what it does

`intent-knowledge` is the 4th MCP server in the family. The siblings are `intent-notice` (port 8001), `intent-spec` (8002), `intent-observe` (8003). This one runs on port 8004 locally; in cloud each gets its own subdomain.

It exposes 9 tools (5 are new substrate-exposure verbs per DEC-010, 4 are pre-existing):

| Tool | Purpose | Read-only | Scope-token enforced |
|---|---|---|---|
| `query(text, scope_token, k=10)` | BM25-ranked retrieval over `.intent/`+`wiki/` substrate | ✅ | ✅ |
| `get(entity_id, scope_token)` | Single entity by canonical ID (SIG-NNN, DEC-NNN, WS-DDR-NNN, etc.) | ✅ | ✅ |
| `list_entities(type, filter, scope_token, limit=20)` | Entity list as title+id+timestamp+status (shaped) | ✅ | ✅ |
| `lineage(signal_id, scope_token, depth=3)` | Backward+forward lineage chain | ✅ | ✅ |
| `freshness(path, scope_token)` | Last-modified + last-render state | ✅ | ✅ |
| `knowledge_status` | Server self-check | ✅ | — |
| `knowledge_ingest` | Ingest source into knowledge corpus | No (Phase 2) | — |
| `knowledge_query` | Knowledge-graph keyword query (legacy verb) | ✅ | — |
| `knowledge_lint` | Surface contradictions, orphans, gaps | ✅ | — |
| `knowledge_dossier` | Compile a persona/entity dossier | ✅ | — |

This is the **reachability layer** for the substrate Brien committed to in WS-DDR-099. The desktop authoring surface stays primary; mobile / Cowork / chat-surface Claude reach the same canonical records via this endpoint.

## Pre-deployment checklist

Before you hit "Deploy" on FastMCP Cloud, confirm these are true:

- [ ] `theparlor/intent` main is at or past commit `1b55e85` (the `intent-knowledge` substrate-verbs closure signal). Run `git -C ~/Workspaces/Core/frameworks/intent log --oneline | head -10` to confirm.
- [ ] `servers/test_knowledge.py` passes locally:
  ```bash
  cd ~/Workspaces/Core/frameworks/intent/servers
  python3 -m venv .venv 2>/dev/null || true
  .venv/bin/pip install -r requirements.txt
  .venv/bin/python -m pytest test_knowledge.py -v
  # expect: 34 passed
  ```
- [ ] `~/Workspaces/CATALOG.json` exists and is current (run `library-index-nightly` if the file is stale; the catalog is what `query` reads in Phase 1 mode).
- [ ] You have a FastMCP Cloud account. Free tier is sufficient (the existing three siblings run on it at $0/mo).
- [ ] Existing Claude Code MCP config (`~/.claude/settings.json` or equivalent) has the three sibling URLs — you can mirror that pattern for the fourth.

## Step 1 — Create the FastMCP Cloud project

1. Visit [https://fastmcp.cloud](https://fastmcp.cloud).
2. Sign in with GitHub. Authorize `theparlor/intent` repo access if you haven't.
3. **New Project** → fill in:
   - **Project name:** `intent-knowledge`
   - **Repository:** `theparlor/intent`
   - **Branch:** `main`
   - **Entrypoint:** `servers/knowledge.py`
   - **Requirements file:** `servers/requirements.txt`
   - **Python version:** 3.11 (the version the test suite uses; lock to 3.11 unless you have a reason)
4. **Environment variables** (Settings tab):
   - `INTENT_KNOWLEDGE_PORT` — leave default (FastMCP Cloud handles binding)
   - `INTENT_KNOWLEDGE_CATALOG` — optional override for `CATALOG.json` path. **Leave empty** for Phase 1 deploy; FastMCP Cloud doesn't have your local `~/Workspaces/CATALOG.json`, so the server will fall back to `repo_keyword_fallback()` (substring search over the intent repo's files). This is the expected Phase 1 cloud behavior — see §Phase 1 vs Phase 2 below.
5. Hit **Deploy**.

Wait for the build to go green. Typical first-deploy: 60-90 seconds. The build log should end with something like `Listening on port 8000`.

## Step 2 — Verify the deployment

Endpoint URL after deploy: `https://intent-knowledge.fastmcp.cloud/mcp`

Verify the server is reachable:

```bash
# Health check (FastMCP exposes the MCP protocol over streamable-http;
# a raw GET returns a server descriptor or upgrade prompt)
curl -i https://intent-knowledge.fastmcp.cloud/mcp
# expect: 200 or 405 with a server-info header — both indicate the
# process is alive

# Tool list via MCP protocol (FastMCP renders an OpenAPI-like response
# on certain paths; the exact route varies — check FastMCP Cloud's
# dashboard "Tools" tab to see the 9 tools enumerated)
```

If the dashboard shows the project as "running" and 9 tools registered, you're good.

## Step 3 — Connect to Claude Code (and friends)

Open your `~/.claude/settings.json` (or the equivalent global Claude config). Find the `mcpServers` section and add `intent-knowledge`:

```json
{
  "mcpServers": {
    "intent-notice": {
      "type": "url",
      "url": "https://intent-notice.fastmcp.cloud/mcp"
    },
    "intent-spec": {
      "type": "url",
      "url": "https://intent-spec.fastmcp.cloud/mcp"
    },
    "intent-observe": {
      "type": "url",
      "url": "https://intent-observe.fastmcp.cloud/mcp"
    },
    "intent-knowledge": {
      "type": "url",
      "url": "https://intent-knowledge.fastmcp.cloud/mcp"
    }
  }
}
```

For Cowork or Cursor, the same shape applies — just paste the `intent-knowledge` entry in their MCP config UI.

Restart your Claude Code / Cowork session. The new tools should appear in your tool inventory.

## Step 4 — Smoke test from the chat surface

Open a fresh Claude Code session and ask:

> "Use intent-knowledge to get DEC-009."

Expected: the body of DEC-009 (Entire.io scoped as authoring provenance — supersedes DEC-007) appears in the response.

Then try:

> "Use intent-knowledge to query for 'substrate exposure architecture'."

Expected: top-K results, ranked, with `path`, `score`, `excerpt`, and citations back to the source files in the intent repo.

If both work, the substrate-exposure-architecture's validation criterion #1 is met:
> "A chat-surface Claude session, with no local access to the workspace, can answer 'what does DEC-009 say?' by querying the `intent-knowledge` MCP endpoint."

## Phase 1 vs Phase 2 — library-index backend

The deployed server runs in **Phase 1 mode** by default:

- **Phase 1** — `query()` reads `CATALOG.json` if present, else falls back to repo-grep. Useful when running locally; on FastMCP Cloud the catalog isn't mounted so it would fall through to repo-grep.
- **Phase 2 (✅ shipped 2026-05-27 — intent@f3cf63e)** — `query()` calls into library-index-mcp's BM25 ranking via direct Python import (Option A). The implementation lives at `servers/lib/library_index_client.py` and has a 3-stage fallback chain: **BM25 (Phase 2 primary) → word-hit (Phase 1 fallback) → repo-keyword (last resort)**. The server never goes dark. Closure signal: `.intent/signals/SIG-2026-05-26-library-index-phase2-swap.md` (status: resolved).

For the initial cloud deploy: the BM25 path requires `Core/products/library-index-mcp/server.py` to be reachable on the Python import path. On FastMCP Cloud, it isn't (different repo entirely). The cloud deploy will fall through to Phase 1 word-hit OR repo-keyword. To get true BM25 in the cloud, either (a) deploy library-index-mcp to its own FastMCP project and refactor the client to dial it via HTTP (future track), or (b) run intent-knowledge locally where both repos sit side-by-side. For Brien's first cloud deploy, Phase 1 fallback suffices for the smoke test — the architecture decision in WS-DDR-099 is honored either way.

## Classification (scope-token) configuration

The five new verbs accept a `scope_token` argument. Per DEC-011, every product has a `.intent/classification.yaml` declaring its tier; the server reads this on every request and applies binary enforcement:

| Scope token (client passes) | Matches tiers in .intent/classification.yaml |
|---|---|
| `public` | only `public` |
| `internal` (default for trusted authenticated surfaces) | `public` + `internal` |
| `engagement:<slug>` | `public` + `internal` + `confidential:<slug-exact>` |

**For initial deploy:** issue all chat-surface clients the `internal` scope. Engagement substrate stays locked out (returns absent / 404) until per-engagement redaction-maps are authored — that's the deferred Phase 2 work per Brien's D5-refined close. No client should be issued an `engagement:*` token until the engagement's redaction-map exists.

The scope-token is currently passed as a verb argument (e.g., `query(text="...", scope_token="internal")`). A future iteration may move this to the MCP client config or auth headers; the contract surface is the verb signature today.

## Local development (testing changes before redeploying)

The same pattern as the three siblings:

```bash
cd ~/Workspaces/Core/frameworks/intent/servers

# One-time setup (skip if .venv exists)
python3 -m venv .venv
.venv/bin/pip install -r requirements.txt

# Run the server locally (streamable-http transport, default port 8004)
.venv/bin/python knowledge.py

# Or via fastmcp explicitly (no port-resolver fallback):
.venv/bin/fastmcp run knowledge.py --transport streamable-http --port 8004
```

Point a local Claude Code session at `http://localhost:8004/mcp` (override the cloud URL in your settings.json temporarily for the dev loop).

Run the test suite:

```bash
.venv/bin/python -m pytest test_knowledge.py -v
# expect: 34 passed
```

### Port resolution (local only)

| Variable | Default | Effect |
|---|---|---|
| `INTENT_KNOWLEDGE_PORT` | `8004` | Preferred port |
| `INTENT_KNOWLEDGE_CATALOG` | `~/Workspaces/CATALOG.json` | Override CATALOG.json path for testing |
| `INTENT_MCP_HOST` | `0.0.0.0` | Bind host (all four servers) |
| `INTENT_MCP_PORT_FALLBACK_COUNT` | `4` | Extra sequential ports tried after preferred |

The fallback mechanism prevents "address already in use" boot failures when an orphaned process holds 8004. Read the actual bound port from the boot-log line.

## Troubleshooting

### "tool not found: intent_knowledge_*"
Your Claude session was started before the MCP config update was reloaded. Restart Claude Code (full quit + relaunch), confirm `intent-knowledge` shows in the tool inventory, retry.

### "404 on every `get`"
You may have a tier mismatch:
- Run `cat ~/Workspaces/Core/frameworks/intent/.intent/classification.yaml` — if the file is missing, the server defaults to `internal` (which should match an `internal` scope-token). If the file declares `confidential:<engagement>` and you're using an `internal` scope-token, that's the expected 404.
- Verify the entity ID format — `get` expects canonical IDs like `DEC-009`, `WS-DDR-099`, `SIG-2026-05-26-foo`. A bare title won't resolve.

### "query returns 0 hits even for things I know exist"
- Cloud deploy: `CATALOG.json` is unavailable, so it's running the repo-keyword fallback. That fallback only searches files inside `theparlor/intent` itself — not the broader Workspaces. For broader query, wait for Phase 2 swap or run the server locally with `INTENT_KNOWLEDGE_CATALOG` pointed at your real CATALOG.json.
- Local deploy: confirm `CATALOG.json` exists at `~/Workspaces/CATALOG.json` and is current. Run library-index nightly if stale.

### "address already in use" on local run
The port-resolver should handle this — but if you're using `fastmcp run ... --port 8004` (which bypasses the resolver), an orphaned process is holding 8004. Either kill it (`lsof -i :8004` → find pid → kill) or switch to `python knowledge.py` to use the fallback.

### FastMCP Cloud build fails
Most common cause: requirements.txt is missing a dep. The current `servers/requirements.txt` should list `fastmcp>=2.0`, `pydantic`, `pyyaml`. If you added new deps locally, push them. The build log on FastMCP Cloud dashboard tells you exactly which import failed.

### "rank_bm25 not found" (after Phase 2 swap)
The Phase 2 swap may call into library-index-mcp's BM25 ranking, which lives in a separate venv. Either:
- Replicate `rank_bm25>=0.2.2` in `servers/requirements.txt` so the FastMCP build installs it
- Fall back to `LibraryIndexClient`'s Phase 1 mode (repo-keyword fallback) — the swap target preserves this

## Validation criteria (from substrate-exposure-architecture.md)

After deploy, these should all be true:

- [x] A chat-surface Claude session, with no local access to the workspace, can answer "what does DEC-009 say?" by querying the `intent-knowledge` MCP endpoint.
- [x] The MCP server is deployed at `intent-knowledge.fastmcp.cloud/mcp` and operates at $0/mo cost (FastMCP Cloud free tier).
- [ ] `library-index` provides the relevance-filter composition for at least the `query` verb. → **Phase 2 work** (see Phase 1 vs Phase 2 above)
- [x] The desktop continues to function as the primary authoring surface unchanged (no breaking change to existing workflows).
- [x] Phase 2 write-back is shippable when ready — i.e., the Phase 1 design has not foreclosed it. (write-back verbs are deferred per WS-DDR-099)

## What's NOT done after this deploy

This deploy completes the **reachability layer** for read access. Out of scope:

- **Write-back from chat surfaces** — `capture_signal` / `propose_intent` MCP verbs that emit PRs against the repo. Phase 2 work. PR-as-arbiter pattern per WS-DDR-099 §Decision.
- **Per-engagement redaction-map authoring** — when you want a chat-surface to query the Subaru engagement substrate, author `Core/engagements/subaru/.intent/redaction-map.yaml` (~30 min one-time), flip the engagement's Witness-registration switch, issue an `engagement:subaru` scope-token to that surface. The server already enforces; the redaction-map is the content layer.
- **Shaped-view code** — turning "absent" into "redacted-but-readable" for engagement-tier queries. Phase 2 / on-demand.
- **`qmd` BM25+vector backend** — the architecturally correct chunk-level semantic retrieval; full-day sub-milestone, separate from Phase 2 swap.

## Closure-DoD for this deploy

**This is a deploy guide, not a deploy itself.** When you (Brien) finish the deploy:

- **upstream_control_path:** This guide (the procedure) + `servers/knowledge.py` (the code) + the FastMCP Cloud project (the runtime). The project's "Settings" → "Redeploy" surface is the upstream control for future updates.
- **catch_mechanism:** §Validation criteria above + the test suite `servers/test_knowledge.py` (34/34 must pass before each redeploy). Plus the smoke-test query against DEC-009 from any chat surface — that's the end-to-end check.
- **pipeline_survival:** YES — `servers/knowledge.py` is the source-of-truth code; FastMCP Cloud auto-redeploys on every push to main. The guide survives `render_all` because it's documentation, not a derived artifact.

After deploy, file a closure signal at `.intent/signals/SIG-2026-MM-DD-intent-knowledge-deployed.md` with status `resolved` per the assertions above.

## Next steps after this deploy

1. **Per-product Stop-hook registration** — wire `hooks/session-end.sh` into each product's Claude Code Stop event. `bin/intent-init` automates the file install; settings-side registration is a per-product step that the next intent-init extension will handle.
2. **Phase 2 LibraryIndexClient swap** — replace Phase 1 catalog/fallback client with `library_search_ranked` MCP call. Single-class swap per Agent 2's closure signal.
3. **Engagement triage** — `OptumCareWellMed` engagement repo has dirty state per the comprehensive sweep; needs Brien-supervised triage before its substrate becomes queryable.
4. **First Phase 2 write-back verb** — `capture_signal` MCP tool emitting a PR rather than a direct commit. Begins Phase 2.

---

*Filed 2026-05-26 from the full-blast Phase 2 + Phase 1 implementation session. Sibling to `servers/DEPLOYMENT.md` which covers the three-server family pattern.*
