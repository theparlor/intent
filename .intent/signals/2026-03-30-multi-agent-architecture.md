---
id: SIG-016
title: Intent needs a multi-agent MCP architecture
type: opportunity
source: conversation
source_context: Claude mobile session during airport transit
date: 2026-03-30
status: resolved
cluster: infrastructure
autonomy_level: L1
tags: [agents, mcp, architecture, deployment]
upstream_control_path: "Claude Code native Agent/Task subagent system; agent-teams plugin; servers/notice.py, spec.py, observe.py, knowledge.py"
catch_mechanism: "Overtaken by events: Claude Code's own Agent tool and agent-teams plugin (specialization, model routing, parallel dispatch) superseded the bespoke seven-server mesh this signal proposed; the four core phases got their own server files without needing dedicated hosted FastMCP/Cloudflare deployments"
verification_command: "ls /Users/brien/Workspaces/Core/frameworks/intent/servers/*.py"
---

# SIG-016: Intent needs a multi-agent MCP architecture

## Observation

Brien explored the architecture for running multiple specialized coding agents, each with bounded context and specific skills, always available via URL. The conversation identified a clear service-mesh pattern for Intent's agent layer.

## Key Insights

- **Specialization beats generalism**: Three focused agents consistently outperform one generalist working three times as long (Addy Osmani finding)
- **Claude Code native subagents** now support this — markdown-defined agents with custom system prompts, tool access, and model routing (Haiku for simple tasks)
- **Agent Teams / Swarms mode** allows a lead agent to spawn and manage parallel specialists on a shared codebase
- **oh-my-claudecode** runs up to 5 concurrent workers in isolated Git worktrees with shared task lists (3-5x speedup)

## Proposed Agent Roster for Intent

| Agent | Domain | MCP Server |
|-------|--------|-----------|
| Signal Capture | Creating and ingesting signals from conversations, logs, observations | `signal-capture-server` |
| Signal Enrichment | Trust scoring, clustering, pattern detection, amplification | `signal-enrichment-server` |
| Spec Writer | Deriving specs from promoted signals/intents | `spec-server` |
| Contract Generator | Creating verifiable assertions from specs | `contract-server` |
| Test Automation | Generating automated testing scripts from contracts | `test-server` |
| Code Reviewer | Reviewing execution output against specs and contracts | `review-server` |
| Observe/Emit | Event emission, trace generation, JSONL append | `observe-server` |

## Deployment Pattern

1. Each MCP server as a focused FastMCP Python file
2. Deploy to FastMCP Cloud (free, auto-redeploys on push to main) or Cloudflare Workers (100K req/day free)
3. StreamableHTTP transport with `/mcp` endpoint
4. Claude Code subagents connect to relevant servers via URL
5. Coordinator subagent or Agent Teams orchestrates

## Implication

This is the operational backbone that makes Intent's autonomy levels real. Without specialized agents, L3/L4 autonomy is theoretical. With them, the trust-scored pipeline can actually execute.

## Promotion Candidate

-> INT-??? (Multi-Agent Infrastructure Intent)
-> SPEC-??? (MCP Server Architecture Spec)

## Triage, 2026-07-08

Disposition: overtaken by events. This never got promoted to its own intent or spec, and it didn't need to be: Claude Code shipped native Agent Teams, a Task tool, and per-agent model routing directly into the harness Brien already runs sessions in, which is a better answer to "specialization beats generalism" than a bespoke seven-server mesh would have been. The four core loop phases (notice, spec, observe, knowledge) each got a server file; the other three roles in the proposed roster (contract generator, test automation, code reviewer) never shipped as separate servers because Claude Code's built-in subagent types cover the same ground on demand.
