---
id: SIG-008
timestamp: 2026-03-29T16:00:00Z
source: conversation
confidence: 0.9
author: brien
related_intents: [notice-product, signal-capture]
---
# Signals die in the gap between where they're noticed and where the system can see them

Capturing a signal currently means: open a text editor, write a markdown file with the right frontmatter, save it to .intent/signals/, commit, push. That's 6 steps and a context switch. The signal is gone by step 2.

The capture bar has to be as low as writing a sticky note. One action, no context switch, from wherever you already are. This is why the MCP server and CLI exist — they collapse 6 steps to 1.

Implication: Every surface where a practitioner works (Slack, Claude Code, Cursor, ChatGPT, Copilot) needs its own capture adapter.
