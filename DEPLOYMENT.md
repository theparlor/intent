---
title: Deployment
type: framework
maturity: final
confidentiality: shareable
reusability: universal
domains:
  - consulting-operations
created: 2026-04-02
depth_score: 2
depth_signals:
  file_size_kb: 2.5
  content_chars: 2194
  entity_count: 0
  slide_count: 0
  sheet_count: 0
  topic_count: 1
  has_summary: 0
vocab_density: 0.00
---
# Deployment: Intent MCP Servers

## Fastest Path: FastMCP Cloud (Free)

```bash
# 1. Push servers/ to your intent repo
cp -r servers/ /path/to/intent/servers/
cd /path/to/intent && git add servers/ && git push

# 2. Go to fastmcp.cloud, sign in with GitHub
# 3. Create three projects:

#   intent-notice  → entrypoint: servers/notice.py
#   intent-spec    → entrypoint: servers/spec.py
#   intent-observe → entrypoint: servers/observe.py

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
    }
  }
}
```

## Local Development

```bash
pip install fastmcp

# Three terminals:
fastmcp run servers/notice.py --transport streamable-http --port 8001
fastmcp run servers/spec.py --transport streamable-http --port 8002
fastmcp run servers/observe.py --transport streamable-http --port 8003
```

Point Claude Code at `http://localhost:800X/mcp`.

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
