---
id: SIG-030
title: Cowork plugin should bundle persona MCP access + critique skills for mobile and dispatch use
timestamp: 2026-04-11T20:00:00Z
source: cowork-session
author: brien
confidence: 0.85
trust: 0.6
autonomy_level: L2
status: active
cluster: bootstrap-tooling
---

# SIG-030: Cowork Plugin for Persona Access

## What was noticed

Brien wants to make his four Intent MCP servers and persona-based critique skills available from Cowork dispatch sessions and mobile Claude chat. The three-layer plugin design:

1. **MCP Servers** — intent-notice (8001), intent-spec (8002), intent-observe (8003), intent-knowledge (8004)
2. **Persona Skills** — four Intent personas (△◇○◉) as invokable skills for structured review
3. **Expert Critique / ARB Review** — composite skill running multi-perspective assessment

## Additional insight from this session

The persona library itself should be queryable via MCP — not just the four Intent personas, but the thought leader personas (Tune, Torres, Patton, Cagan, etc.) as invokable advisors. "What would Teresa say about this discovery approach?" should be a tool call, not a prompt engineering exercise.

This requires the Knowledge Engine MCP server (intent-knowledge) to serve persona artifacts as queryable entities, with the depth scale informing confidence levels in responses.

## Deployment consideration

For mobile access, the MCP server needs to be hosted (not localhost). Brien's preferred topology: self-hosted VPS (~$10/month), bearer token auth, federation boundaries for engagement data, audit logging via Intent observe layer.

## Triage, 2026-07-08

Disposition: still pending, partially actioned by a different route than proposed. The specific ask (personas queryable via the intent-knowledge MCP server, hosted for mobile/dispatch access on a self-hosted VPS with bearer-token auth) was not built as specified: tools/intent-mcp/server.py has no persona-related tools, and no hosted deployment exists. A substrate-exposure-architecture.md spec and a 2026-05-26 Cowork handoff track discuss hosted MCP access at a more general architectural level, but that work is still at the open-decisions-for-Brien stage, not deployed. Separately, library-index-mcp now provides queryable entity lookup over the Cast registry, which functionally covers part of the "query personas by name" ask through a different server than the one this signal named.
