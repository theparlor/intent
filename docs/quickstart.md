# Quickstart: Intent in 5 Minutes

Get from zero to your first captured signal in under 5 minutes.

## 1. Add the Intent directory to your repo

```bash
mkdir -p .intent/signals .intent/intents .intent/specs .intent/contracts .intent/decisions .intent/events .intent/templates
```

Or clone the template:

```bash
# From within your existing repo:
curl -sL https://raw.githubusercontent.com/theparlor/intent/main/.intent/templates/signal.md \
  > .intent/templates/signal.md
```

## 2. Install the CLI (optional)

```bash
# Copy the script to your PATH
curl -sL https://raw.githubusercontent.com/theparlor/intent/main/bin/intent-signal \
  > /usr/local/bin/intent-signal
chmod +x /usr/local/bin/intent-signal
```

## 3. Capture your first signal

```bash
intent-signal "Teams using AI agents hit a ceremony wall around sprint 3"
```

Or manually — create `.intent/signals/2026-03-29-ceremony-wall.md`:

```yaml
---
id: SIG-001
timestamp: 2026-03-29T14:00:00Z
source: conversation
author: yourname
---
# Teams using AI agents hit a ceremony wall around sprint 3

When AI agents start doing significant portions of the implementation,
the two-week sprint cycle becomes a bottleneck rather than a cadence.
Work completes in hours but waits for the next planning session to
get new specs.
```

## 4. See what you've captured

```bash
ls .intent/signals/
cat .intent/events/events.jsonl
```

## 5. Commit and push

```bash
git add .intent/
git commit -m "signal: first signal captured"
git push
```

That's it. You're running the Notice phase of the Intent loop.

## What's next?

- **Capture more signals** as you work. The bar is one sentence.
- **Review signals weekly** — which ones cluster? Which ones surprise you?
- **When a signal demands action**, write an intent in `.intent/intents/`
- **When an intent is approved**, write a spec in `.intent/specs/`
- **Install the MCP server** to capture signals from Claude Code or Cursor (see `tools/intent-mcp/`)
- **Add the GitHub Action** for automated event emission (see `.github/workflows/intent-events.yml`)

## The Intent Loop

```
NOTICE  →  SPEC  →  EXECUTE  →  OBSERVE  →  (back to NOTICE)
  ↑                                              |
  └──────────────────────────────────────────────┘
```

You just completed your first Notice cycle. The rest follows naturally.
