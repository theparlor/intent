---
id: SIG-011
timestamp: 2026-03-29T19:00:00Z
source: conversation
author: brien
confidence: 0.85
trust: 0.45
autonomy_level: L2
status: active
cluster: signal-capture-surfaces
parent_signal:
related_intents: [notice-product, signal-capture]
---
# Signal capture needs to cover every surface where practitioners work — not just the IDE

Slack, Claude Code, Cowork, Cursor, ChatGPT, GitHub Copilot, Microsoft 365 Copilot, Codex — practitioners work across all of these. A signal capture system that only works in the terminal misses where most insights actually happen: conversations, code reviews, strategic thinking sessions.

The 5-tier adapter strategy (MCP, CLI, Slack, GitHub, AI Plugins) prioritizes by leverage: MCP covers 3 surfaces with one implementation. CLI works everywhere as a fallback. Slack captures team conversations. GitHub captures structured observations. AI plugins are last because each requires platform-specific development.

## Triage, 2026-07-08

Disposition: still pending, partial. Tier 1 (MCP) and Tier 2 (CLI) are built and live. Tiers 3 through 5 (Slack, GitHub issue/PR capture, AI plugins) remain specced-only, per CLAUDE.md's own status table in this exact section (spec/signal-capture-system.md). Needed control: build the Slack reaction-based capture adapter (Tier 3) as the next-highest-leverage surface, since Brien already has the native Slack connector wired for other work, or explicitly deprioritize this in the spec if solo-practitioner usage no longer needs multi-surface coverage beyond MCP and CLI.
