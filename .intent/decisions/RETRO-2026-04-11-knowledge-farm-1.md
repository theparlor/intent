---
decision_id: RETRO-2026-04-11-knowledge-farm-1
title: "Knowledge Farm Deployment Topology for Mobile-Accessible MCP"
date: 2026-04-11
status: accepted
source: retroactive-extraction
---

## Context

The Knowledge Farm (compiled persona knowledge, engagement data, research artifacts) needs to be accessible from both desktop Cowork sessions and mobile Claude chat. Desktop access is solved by local MCP servers, but mobile requires a network-accessible endpoint.

## Decision

Defined deployment topology:

- **Self-hosted VPS** (~$10/month) running the intent-knowledge MCP server
- **Bearer token authentication** for API access
- **Federation boundaries** for engagement data — engagement data stays within its originating context and is not promoted to the shared knowledge layer without explicit approval
- **Audit logging via observe layer** — all queries and responses logged for signal extraction
- **Same server** serves both Cowork dispatch (desktop) and mobile Claude chat

## Consequences

- Knowledge Farm becomes accessible from any Claude interface (desktop, mobile, API)
- $10/month operating cost is sustainable for a solo operator
- Bearer token auth is simple but sufficient for a single-user system
- Federation boundaries prevent accidental data leakage between engagement contexts
- Audit logging creates a secondary signal stream from usage patterns
