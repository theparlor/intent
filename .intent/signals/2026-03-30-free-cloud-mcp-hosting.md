---
id: SIG-018
title: Free-tier cloud MCP hosting is viable for Intent's agent layer
type: opportunity
source: conversation
source_context: Claude mobile session — cloud deployment research
date: 2026-03-30
status: active
cluster: infrastructure
autonomy_level: L2
tags: [mcp, deployment, cloud, fastmcp, cloudflare]
---

# SIG-018: Free-tier cloud MCP hosting is viable for Intent's agent layer

## Observation

Research during mobile session identified multiple free/cheap hosting paths for always-on MCP servers. This removes the infrastructure cost barrier from Intent's multi-agent architecture.

## Hosting Options Identified

| Platform | Free Tier | Characteristics |
|----------|-----------|----------------|
| **FastMCP Cloud** | Free personal tier (indefinite) | Sign in with GitHub, point at repo, auto-deploys on push to main |
| **Cloudflare Workers** | 100K requests/day free | Edge-deployed, cold start ~0ms, StreamableHTTP transport |
| **mcphosting.io** | Free indefinite | Purpose-built for MCP servers |
| **Railway** | $5/month free credit | 24/7 uptime, no cold starts, good for stateful servers |
| **Render** | 750 free hours/month | Spins down after 15min inactivity |

## Technical Requirements

- MCP servers must use **StreamableHTTP transport** (not stdio)
- Expose a `/mcp` endpoint
- FastMCP Python framework is the fastest path to deployment

## Implication

Intent's deployment topology decision (config-driven local vs hosted) now has a concrete answer for the hosted path. FastMCP Cloud + GitHub repo = zero-cost always-on agent infrastructure.

## Relates To

- SIG-016 (multi-agent architecture)
- Project memory: Intent Deployment Topology (config-driven local vs hosted)
