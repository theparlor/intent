---
id: SPEC-MCP-MIGRATION-2026-05-20
title: MCP Server Migration — tools/intent-mcp → servers/ (FastMCP)
type: spec
status: shaped
date: '2026-05-20'
upstream_control_path: .intent/specs/SPEC-MCP-MIGRATION-2026-05-20.md (this file) — tracks dual-implementation until resolved
catch_mechanism: this spec is the disambiguation artifact; once a direction is committed, CLAUDE.md invocation section is updated and the deprecated path is marked
pipeline_survival: git-tracked; future agents read CLAUDE.md + this spec before touching either server implementation
---

# MCP Server Migration — Disambiguation Spec

## Problem Statement

Two MCP server implementations co-exist in this repo with no documented relationship:

| Implementation | File | Library | Status |
|---|---|---|---|
| Legacy stable | `tools/intent-mcp/server.py` | `mcp` (base) | Documented in CLAUDE.md "MCP Server" section. 6 tools. Actively configured in users' Claude Code / Cursor settings. |
| FastMCP architecture-forward | `servers/notice.py`, `servers/spec.py`, `servers/observe.py`, `servers/knowledge.py` | `fastmcp>=2.0` | Documented in CLAUDE.md "Invocation" section. 4 servers, phase-aligned. Not yet widely configured. |

CLAUDE.md describes both as "current" without indicating a migration direction or sunset timeline. This creates maintenance ambiguity — when a feature is added, which surface gets it?

## Decision Options

### Option A — Legacy is primary; FastMCP is experimental
`tools/intent-mcp/server.py` remains the single MCP surface for external consumers. The `servers/` FastMCP implementation is a design exploration / future migration candidate but is NOT authoritative.

**Tradeoffs:** Least disruption to existing configurations. Does not use FastMCP's cleaner per-phase architecture. Tech debt stays.

### Option B — FastMCP is primary; legacy is deprecated
`servers/` becomes the authoritative MCP surface. `tools/intent-mcp/server.py` gets a deprecation notice and a sunset date. Agents update their config to point at the appropriate phase server.

**Tradeoffs:** Cleaner architecture (Notice/Spec/Observe/Knowledge each has its own server). Requires consumers to reconfigure. FastMCP is newer — less battle-tested at Brien's scale.

### Option C — Merge: FastMCP replaces legacy one-to-one
Implement the 6 existing tools from `tools/intent-mcp/server.py` into the `servers/` phase architecture, then retire the legacy file. Single implementation, FastMCP-based.

**Tradeoffs:** Best long-term hygiene. Most implementation work. Clean boundary: migrate once, not continuously.

## Recommended Direction

**Option C** (merge + retire) is the long-term goal, but it requires an IDD Execute loop to migrate the 6 tools.

**Interim posture (until Execute loop completes):**
- `tools/intent-mcp/server.py` = authoritative stable surface for Brien's Claude Code config
- `servers/` = active development surface; new features land here first, then backported if needed
- CLAUDE.md should clarify this relationship explicitly (currently silent)

## CLAUDE.md Update Needed

Add to the `tools/intent-mcp/` invocation section:

> **Migration note (2026-05-20):** `tools/intent-mcp/server.py` is the current stable surface and Brien's active config points here. The `servers/` directory (FastMCP) is the architecture-forward implementation. Migration plan: implement the 6 legacy tools in `servers/` (per-phase), then retire `tools/intent-mcp/server.py`. Track via `SPEC-MCP-MIGRATION-2026-05-20.md`.

## Trigger Signal for Execute Loop
When Brien chooses a direction (A/B/C), emit `SIG-MCP-MIGRATION-DIRECTION-*.md` and open an IDD Execute loop for the implementation.

## Acceptance Criteria
- [ ] Direction chosen (A, B, or C)
- [ ] CLAUDE.md updated with migration note
- [ ] If C: IDD loop opened with DoR + DoD for tool migration
- [ ] Legacy server either retired (C/B) or explicitly declared long-term (A)
