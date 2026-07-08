---
id: SIG-021
title: Working MCP server code exists for all three loop phases
type: opportunity
source: conversation
source_context: Claude mobile session produced deployable FastMCP servers
date: 2026-03-30
status: resolved
cluster: infrastructure
autonomy_level: L2
tags: [mcp, servers, code, fastmcp, deployment]
upstream_control_path: "tools/intent-mcp/server.py (the CLAUDE.md-documented stable production MCP surface)"
catch_mechanism: "Overtaken by events: verified servers/notice.py still holds signals in an in-memory _signals dict (checked 2026-07-08), so the Phase 4 git-backed persistence this signal called out as the next step never landed on that code path. Instead a separately built, file-native server (tools/intent-mcp/server.py, walks up to .intent/, writes real markdown) became the actual production MCP surface. The mobile-session prototype was superseded rather than completed"
verification_command: "grep -n '_signals\\[' /Users/brien/Workspaces/Core/frameworks/intent/servers/notice.py"
---

# SIG-021: Working MCP server code exists for all three loop phases

## Observation

The mobile session produced not just architecture diagrams but actual deployable Python code:

- `notice.py` — 15KB, 8 tools (create_signal, score_trust, cluster_signals, promote_to_intent, add_reference, dismiss_signal, list_signals, get_events)
- `spec.py` — 12KB, 5 tools (create_spec, create_contract, verify_contract, assess_agent_readiness, list_specs)
- `observe.py` — 10KB, 5 tools (ingest_event, detect_spec_delta, detect_trust_drift, system_health, suggest_signals_from_events)
- `models.py` — 6KB, shared data models with trust computation, amplification, event generation
- `intent-architecture.jsx` — Interactive React diagram with 4 views (Loop, MCP Servers, Subagents, Trust)

Plus 6 Claude Code subagent definitions (signal-capture, signal-enricher, spec-writer, contract-verifier, observer, coordinator) with model routing (Haiku for capture, Sonnet for reasoning).

## Current State

In-memory stores — Phase 4 replaces with Git-backed file I/O to `.intent/` directories. The servers already generate correct frontmatter format, so the transition is swapping dict operations for file read/write + git commit.

## Location

All files copied to `frameworks/intent/servers/` and `frameworks/intent/artifacts/`.

## Next Steps

1. Deploy notice.py to FastMCP Cloud as walking skeleton
2. Test signal capture → trust scoring → clustering flow
3. Add Git-backed persistence (Phase 4)

## Relates To

- SIG-016 (multi-agent architecture)
- SIG-018 (free cloud hosting)

## Triage, 2026-07-08

Disposition: overtaken by events. Checked directly: servers/notice.py at line 131 still does `_signals[sig_id] = signal`, an in-memory dict, so "Next Steps" item 3 (git-backed persistence) never happened on this code. What actually shipped as the real MCP server, per CLAUDE.md, is tools/intent-mcp/server.py, a different implementation using the base mcp library that was file-backed from the start. The prototype documented here was set aside in favor of that separately-built surface, not finished.
