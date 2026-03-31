---
id: CLU-001
name: "infrastructure"
title: "Infrastructure"
status: active
signals: [SIG-016, SIG-018, SIG-021, SIG-024]
weight: 2.0
formed_date: 2026-03-30
promoted_to: ""
promoted_date:
---
# Cluster: Infrastructure

## Theme
MCP servers exist, deployment options identified, Cowork-to-Claude Code routing established. This cluster represents the foundational infrastructure layer that makes Intent's agent architecture real: multi-agent MCP architecture (SIG-016), free-tier cloud hosting viability (SIG-018), working server code across all three loop phases (SIG-021), and the friction that forced the Cowork→Claude Code CLI routing path (SIG-024). Together they form the deployment topology that everything else runs on.

## Member Signals

| Signal | Title | Trust | Date |
|--------|-------|-------|------|
| SIG-016 | Intent needs a multi-agent MCP architecture | 0.50 | 2026-03-30 |
| SIG-018 | Free-tier cloud MCP hosting is viable for Intent's agent layer | 0.50 | 2026-03-30 |
| SIG-021 | Working MCP server code exists for all three loop phases | 0.50 | 2026-03-30 |
| SIG-024 | Cowork sandbox cannot reliably sync to GitHub — needs Claude Code CLI path | 0.50 | 2026-03-30 |

## Promotion Criteria
A cluster is ready for promotion to intent when:
- [x] 3+ signals with independent sources
- [x] Aggregate weight > 1.0 (sum of trust scores)
- [x] At least one signal from the last 14 days (not stale)
- [x] Pattern is actionable (not just an observation)

## Emergence Notes
How did this cluster form? Was it:
- **Human-noticed:** Brien identified the infrastructure pattern across signals captured during airport transit and Cowork sessions. All four signals share the `infrastructure` cluster tag and relate to the MCP deployment topology.

## Open Questions
- Which cloud hosting option (FastMCP Cloud, Cloudflare Workers, Railway) should be the first walking skeleton target?
- Does the Cowork→Claude Code routing path need formalization, or is the current manual handoff sufficient?
- How do the three MCP servers (notice, spec, observe) coordinate in a multi-agent architecture?
