---
id: SIG-033
timestamp: 2026-04-13T01:30:00Z
source: research-synthesis
confidence: 0.9
trust: 0.8
autonomy_level: L3
status: symptom-repaired, upstream-pending
cluster: knowledge-engine
upstream_control_path: knowledge/decisions/DDR-007-ke-mcp-query-write-back.md (accepted 2026-04-13; decides conditional write-back with confidence gating and a 5-tool surface including intent_knowledge_enrich)
catch_mechanism: "NONE TODAY: no lint or test asserts a write-back pathway exists in servers/knowledge.py; DDR-007's five validation criteria remain unchecked"
pipeline_survival: "NONE TODAY: nothing blocks read-only growth of the MCP tool surface; query/get/list_entities/lineage/freshness/get_core all shipped without the write pathway"
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

## Remediation note (2026-07-03)

Status downgraded from resolved to symptom-repaired, upstream-pending. The decision this signal demanded did land: DDR-007 (knowledge/decisions/DDR-007-ke-mcp-query-write-back.md, accepted 2026-04-13) chose conditional auto-enrichment with confidence gating and a 5-tool surface including intent_knowledge_enrich. But the implementation never followed: servers/knowledge.py has no enrich tool, knowledge_query has no write pathway, knowledge/log.md contains zero [ENRICH] entries, and all five DDR-007 validation criteria are unchecked. The tool surface has since grown read-only (query, get, list_entities, lineage, freshness, get_core), which is the exact retrofit-cost scenario this signal warned about. Open work: implement the write-back pathway per DDR-007 and add a catch mechanism (lint or test) that asserts it stays present.

Checker note: the flagged phrase "architecturally incomplete" in the body above quotes the research finding about read-only knowledge MCPs generally; it is not a self-referential admission. The line is left as written.

## Triage, 2026-07-08

Disposition: still pending, confirmed unchanged. Re-checked directly: servers/knowledge.py still has no enrich tool, and knowledge/log.md still has zero ENRICH entries five days after the 2026-07-03 note. Needed control: implement the DDR-007 write-back pathway (intent_knowledge_enrich) plus a lint/test that fails if the tool surface grows read-only-only again.
