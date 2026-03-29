# Intent MCP Server

Capture signals from any MCP-compatible tool: Claude Code, Cowork, Cursor.

## Install

```bash
pip install mcp pydantic
```

## Use with Claude Code

Add to your `.claude/settings.json` or project config:

```json
{
  "mcpServers": {
    "intent": {
      "command": "python",
      "args": ["path/to/intent-mcp/server.py"],
      "transport": "stdio"
    }
  }
}
```

## Use with Cursor

Add to Cursor's MCP settings (Settings → MCP Servers):

```json
{
  "intent": {
    "command": "python",
    "args": ["path/to/intent-mcp/server.py"]
  }
}
```

## Available Tools

### `intent_capture_signal`
Capture an observation as a structured signal.

**Required:** `title` — one-line summary of what was noticed.

**Optional:** `body`, `confidence` (0.0-1.0), `source`, `related_intents`, `author`, `repo_path`

### `intent_list_signals`
List recent signals, most recent first.

**Optional:** `limit` (default 10), `repo_path`

### `intent_get_signal`
Get full content of a specific signal by ID or filename.

**Required:** `signal_id` — e.g., "SIG-001"

## What Happens When You Capture

1. A markdown file is created in `.intent/signals/YYYY-MM-DD-slug.md`
2. A `signal.created` event is appended to `.intent/events/events.jsonl`
3. You get a `git add` command to commit the signal

The signal is local until you commit and push. This is by design — you can review and refine before it enters the shared record.
