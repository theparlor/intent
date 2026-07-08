---
id: SIG-008
timestamp: 2026-03-29T16:00:00Z
source: conversation
author: brien
confidence: 0.9
trust: 0.6
autonomy_level: L2
status: resolved
cluster: signal-capture-surfaces
parent_signal:
related_intents: [notice-product, signal-capture]
upstream_control_path: "bin/intent-signal; tools/intent-mcp/server.py (intent_capture_signal)"
catch_mechanism: "The one-call capture path this signal describes as the fix is exactly what shipped; the remaining per-surface adapter ask is tracked separately under SIG-011 (multi-surface-capture-requirement), left still-pending there rather than duplicated here"
verification_command: "ls /Users/brien/Workspaces/Core/frameworks/intent/bin/intent-signal"
---
# Signals die in the gap between where they’re noticed and where the system can see them

Capturing a signal currently means: open a text editor, write a markdown file with the right frontmatter, save it to .intent/signals/, commit, push. That’s 6 steps and a context switch. The signal is gone by step 2.

The capture bar has to be as low as writing a sticky note. One action, no context switch, from wherever you already are. This is why the MCP server and CLI exist — they collapse 6 steps to 1.

Implication: Every surface where a practitioner works (Slack, Claude Code, Cursor, ChatGPT, Copilot) needs its own capture adapter.

## Triage, 2026-07-08

Disposition: control exists now. The core complaint here, 6 manual steps to capture a thought, is resolved by the CLI and MCP tool. The broader "needs its own capture adapter per surface" implication is the same open item as SIG-011 and is tracked there, not duplicated on this file.
