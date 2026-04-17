---
id: SIG-033
timestamp: 2026-04-13T01:30:00Z
source: research-synthesis
confidence: 0.9
trust: 0.8
autonomy_level: L3
status: resolved
cluster: knowledge-engine
author: agent
related_intents: []
referenced_by:
  - SIG-032
parent_signal: SIG-032
---
# intent-knowledge MCP server must have architectural write-back from queries

The Rotifer Protocol article ("Compile Your Knowledge, Don't Search It") and rvk7895's auto-evolve pattern both surface the same finding: **a knowledge MCP that only reads and never writes is architecturally incomplete.** The distinction between "archival" and "evolutionary" knowledge is the feedback loop — query outputs filed back as new artifacts.

rvk7895 implements this as a background opus subagent that fires after every query, silently creating/updating wiki articles when the answer contained new knowledge. The Rotifer article frames it as a fundamental architectural property: "reading and writing are the same operation."

**For intent-knowledge MCP (port 8004):** The current design (DDR-005, Key Decision 16) specifies ingest/query/lint subcommands. The query operation must couple to a write pathway at design time. This is not a feature to add later — it determines the MCP's tool surface, the event schema, and the trust model for autonomous knowledge enrichment.

**Decision required:** DDR-007 — should intent-knowledge query always write back (with constraints), write back conditionally (confidence threshold), or offer write-back as an explicit post-query operation?

**Grounded in:** rvk7895 auto-evolve pattern, Rotifer Protocol query-as-contribution, Karpathy "file answers back into the wiki."
