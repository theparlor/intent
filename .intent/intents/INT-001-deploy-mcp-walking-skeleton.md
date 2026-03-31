---
id: INT-001
title: "Deploy MCP walking skeleton to FastMCP Cloud"
status: proposed
proposed_by: "system"
proposed_date: 2026-03-30T22:00:00Z
accepted_date:
signals: [SIG-016, SIG-018, SIG-021, SIG-024]
specs: []
owner: ""
priority: now
product: notice
---
# Deploy MCP walking skeleton to FastMCP Cloud

## Problem
Three MCP servers exist as Python code (notice.py, spec.py, observe.py) but run only locally. The signal capture pipeline dies when Brien's laptop closes. Free-tier cloud hosting is viable (FastMCP Cloud, Cloudflare Workers) but no deployment has been attempted. The infrastructure cluster (4 signals, weight 2.0) consistently points to the same gap: the servers need to be reachable from any surface, not just localhost.

## Desired Outcome
At least one MCP server (notice.py — the signal capture entry point) is deployed to FastMCP Cloud and accessible via a stable URL. Claude Code, Cowork, and Cursor can connect to it remotely. Signal capture works when the laptop is offline. The deployment is reproducible — a second person could follow the same steps.

## Evidence
- **SIG-016:** Multi-agent MCP architecture designed — 3 servers, 18 tools, model routing
- **SIG-018:** Free-tier cloud hosting is viable — FastMCP Cloud (unlimited beta), Cloudflare Workers (100K/day)
- **SIG-021:** Working MCP server code exists — notice.py (15KB, 8 tools), spec.py (12KB, 5 tools), observe.py (10KB, 5 tools)
- **SIG-024:** Cowork sandbox cannot sync to GitHub — needs always-on infrastructure path

## Constraints
- Must use free tier (no paid infrastructure at this stage)
- Must not require Docker or Kubernetes — binary/script deployment only
- Must be reproducible from `servers/` directory + `requirements.txt`
- Should not break existing local development workflow
- Brien's Grafana Cloud credentials are needed for the OTel exporter config (Phase 2 — not blocking this intent)

## Open Questions
- Does FastMCP Cloud support the current FastMCP version in servers/?
- What's the cold start latency on free tier? Acceptable for interactive use?
- Should all 3 servers deploy together or notice.py first as a walking skeleton?
