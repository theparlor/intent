---
title: Deployment
type: framework
maturity: final
confidentiality: shareable
reusability: universal
domains:
  - consulting-operations
created: 2026-03-31
depth_score: 2
depth_signals:
  file_size_kb: 4.2
  content_chars: 4002
  entity_count: 0
  slide_count: 0
  sheet_count: 0
  topic_count: 1
  has_summary: 0
vocab_density: 0.00
---
# Deployment: Intent MCP Servers

> **For the 4th server (`intent-knowledge`)**, see [`DEPLOYMENT-INTENT-KNOWLEDGE.md`](DEPLOYMENT-INTENT-KNOWLEDGE.md) — it has the same five-step shape plus the substrate-exposure-specific config (scope tokens, classification.yaml, Phase 1/Phase 2 library-index modes).

## Fastest Path: FastMCP Cloud (Free)

```bash
# 1. Push servers/ to your intent repo
cp -r servers/ /path/to/intent/servers/
cd /path/to/intent && git add servers/ && git push

# 2. Go to fastmcp.cloud, sign in with GitHub
# 3. Create three projects:

#   intent-notice    → entrypoint: servers/notice.py
#   intent-spec      → entrypoint: servers/spec.py
#   intent-observe   → entrypoint: servers/observe.py
#   intent-knowledge → entrypoint: servers/knowledge.py  (see DEPLOYMENT-INTENT-KNOWLEDGE.md)

# Each gets a URL like: https://intent-notice.fastmcp.cloud/mcp
# Auto-redeploys on every push to main.
```

## Connect to Claude Code

Add to `.claude/settings.json` in your intent repo:

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

## Local Development

```bash
pip install fastmcp

# Four terminals (one per server):
fastmcp run servers/notice.py    --transport streamable-http --port 8001
fastmcp run servers/spec.py      --transport streamable-http --port 8002
fastmcp run servers/observe.py   --transport streamable-http --port 8003
fastmcp run servers/knowledge.py --transport streamable-http --port 8004
```

Point Claude Code at `http://localhost:800X/mcp`.

### Port resolution

Running a server directly (`python servers/notice.py`) late-binds its
port: it tries the preferred port, then a fallback range, so a second
instance or an orphaned process does not cause an "address already in
use" boot failure. The server logs the port it actually bound — read
that line rather than assuming the default.

| Variable                         | Default   | Effect                                  |
|----------------------------------|-----------|-----------------------------------------|
| `INTENT_NOTICE_PORT`             | `8001`    | Preferred port for notice               |
| `INTENT_SPEC_PORT`               | `8002`    | Preferred port for spec                 |
| `INTENT_OBSERVE_PORT`            | `8003`    | Preferred port for observe              |
| `INTENT_KNOWLEDGE_PORT`          | `8004`    | Preferred port for knowledge            |
| `INTENT_MCP_HOST`                | `0.0.0.0` | Bind host (all servers)                 |
| `INTENT_MCP_PORT_FALLBACK_COUNT` | `4`       | Extra sequential ports tried after pref |

`fastmcp run ... --port` (above) binds explicitly and bypasses the
resolver — use the direct `python servers/<name>.py` form to get
fallback behavior.

## Alternative Platforms

| Platform        | Free Tier          | Best For                |
|----------------|--------------------|-------------------------|
| FastMCP Cloud  | Unlimited (beta)   | Fastest, zero config    |
| Cloudflare     | 100K req/day       | Edge, stateless         |
| Railway        | $5 free credit     | 24/7, persistent state  |
| Render         | 750 hrs/month      | Containers              |

## Persistence (Phase 4)

Replace in-memory dicts with file I/O to `.intent/` directory:
- Signals: read/write `.intent/signals/*.md` (frontmatter + body)
- Specs: read/write `spec/SPEC-*.md`
- Events: append to `.intent/events/events.jsonl`
- Use GitHub API for remote read/write if servers are cloud-hosted

The servers already generate correct frontmatter format. The
transition is: swap dict operations for file read/write + git commit.
