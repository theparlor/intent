---
title: "Knowledge Engine as new MCP server — intent-knowledge on port 8004"
id: DEC-INTENT-016
type: decision-atom
created: 2026-04-06
date_inferred: false
scope: Core/frameworks/intent — Knowledge Engine deployment architecture
status: ratified
ratified_at: 2026-04-06
ratified_by: "brien (2026-04-06; 4-gate pass: reversible / local / precedent / no info gap)"
gate_check:
  reversible: pass
  local: pass
  precedent: pass
  info_gap: pass
upstream_control_path: "Core/frameworks/intent/CLAUDE.md §Key Decisions #16; servers/DEPLOYMENT.md port assignments"
catch_mechanism: "Port assignments in DEPLOYMENT.md; servers/knowledge.py is the canonical server file"
pipeline_survival: "Server file and port assignment recorded in deployment config"
source: "2026-04-06"
---

# Decision: Knowledge Engine as new MCP server — intent-knowledge on port 8004

> Ratified 2026-04-06. All 4 autonomy-grant gates pass.

## Context

The Knowledge Engine needed its own MCP server to provide tools for ingest, query, and lint operations. The existing `intent-notice` MCP server is purpose-built for the Notice phase. Bolting Knowledge Engine onto it would violate product boundary (DEC-INTENT-014) and create coupling.

## Decision

Knowledge Engine gets its own MCP server: `intent-knowledge` on port 8004, with CLI subcommands `intent-knowledge ingest/query/lint`. Separate from `intent-notice`. This enforces the two-product boundary and allows independent deployment.

## Scope

Governs Knowledge Engine server deployment. Does not govern the other phase servers (notice, spec, observe) which have their own ports.

## Alternatives Not Taken

| Alternative | Why not chosen | Reversibility if revisited |
|-------------|----------------|---------------------------|
| Bolt KE tools onto intent-notice server | Violates two-product boundary; coupling risk | L3 — server refactor |
| CLI-only (no MCP server) | Blocks Claude Code / Cursor integration | L4 — add server |

## Reversibility

L4 — port assignment is a config. Server file can be renamed/moved.

## Ratification Action

`servers/knowledge.py` is the Knowledge Engine MCP server. Port 8004 assigned in `servers/DEPLOYMENT.md`. CLI `intent-knowledge` with ingest/query/lint subcommands planned.
