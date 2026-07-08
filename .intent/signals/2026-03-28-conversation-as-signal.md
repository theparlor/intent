---
id: SIG-003
date: 2026-03-28
source: cowork-session
confidence: high
related_intents: []
status: resolved
upstream_control_path: "bin/intent-signal; tools/intent-mcp/server.py (intent_capture_signal); session-signal and session-extract Claude Code skills; .github/workflows/intent-events.yml"
catch_mechanism: "Mechanism 1 (during-session capture) is the CLI/MCP one-call path; mechanism 2 (post-session extraction) is the session-signal / session-extract skill pair, which read a session and propose signal files"
verification_command: "ls /Users/brien/Workspaces/Core/frameworks/intent/bin/intent-signal"
---

# Signal: Conversations should automatically feed the notice layer

## Observation

During the Cowork session that produced the work ontology and OTel mapping, Brien asked: "how do we take this thread here between us and turn it into consideration and part of the intent ideation and notice layer as we talk?"

## Implication

If Intent is a system for surfacing and acting on insights, then the insights generated during Cowork/Claude sessions are primary signal sources. They should flow into `.intent/signals/` with minimal friction — ideally automatically.

## Proposed Mechanism

1. **During session**: Human or Claude identifies key insights and writes signal files to `.intent/signals/` in real time (what we're doing right now)
2. **Post-session**: An extract-signals agent reads the conversation transcript (available via Cowork session API or Entire.io capture) and proposes signal files
3. **On schedule**: The observe-cycle agent reads accumulated Entire.io traces and extracts signals automatically

## Design Constraint

Signal extraction must be high-precision, low-volume. The notice layer should contain 3-5 high-quality signals per session, not 50 low-quality ones. The agent should surface what's surprising or non-obvious, not summarize everything.

## Dogfooding Note

This signal file was itself generated during the conversation it describes, demonstrating the pattern in action.

## Triage, 2026-07-08

Disposition: control exists now. Both mechanisms this signal asked for are built: the CLI/MCP path collapses capture to one action from inside a session, and the session-signal / session-extract skill pair does the post-session extraction this signal called mechanism 2. Mechanism 3 (an always-on observe-cycle agent tailing Entire.io traces on a schedule) was not built as a separate always-on process; the GitHub Action plus the two skills cover the same need without requiring a standing daemon.
