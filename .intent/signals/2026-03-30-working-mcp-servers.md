---
id: SIG-021
title: Working MCP server code exists for all three loop phases
type: opportunity
source: conversation
source_context: Claude mobile session produced deployable FastMCP servers
date: 2026-03-30
status: active
cluster: infrastructure
autonomy_level: L2
tags: [mcp, servers, code, fastmcp, deployment]
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
