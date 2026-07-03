---
id: SIG-037
timestamp: 2026-05-16T00:00:00Z
source: knowledge-ingest
confidence: 0.7
trust: 0.35
autonomy_level: L1
status: resolved
resolved_date: 2026-07-03
disposition: |
  DECIDED by Brien 2026-07-03 (direct, in-session): GitHub Actions is the always-on substrate
  now (least change, already deep in git), with an explicit trajectory to cloud (MCP space,
  cloud data space, multi-dev access) and named migration triggers. Promoted to DDR-009 per
  this signal's own proposed action 1.
upstream_control_path: /Users/brien/Workspaces/Core/frameworks/intent/knowledge/decisions/DDR-009-always-on-hosting-substrate.md
catch_mechanism: DDR-009 validation criteria (14-day migrated-stage reliability run + NDA log spot-audit); migration triggers named in DDR-009 section 3 fire a fresh substrate DDR
pipeline_survival: DDR-009 is a committed knowledge/decisions artifact; survives independently of this signal
cluster: deployment-topology
author: agent
related_intents: []
referenced_by:
  - THM-005
parent_signal: null
---

# "Laptop is not a strategy" — always-on hosting is the unresolved load-bearing decision

## Summary

The Rahul playbook (THM-005) independently states the exact failure Intent already names in its deployment-topology section: the processing pipeline must run somewhere always-on; "cron stops at 4am... nobody notices until Monday." Intent's CLAUDE.md explicitly flags this ("Brien's laptop goes offline during travel") and lists "Hosted deployment mode — always-on processing" as an open item. External corroboration raises the priority: every autonomous-execution claim Intent makes (L3/L4, autonomous pipeline) is undeliverable until this is resolved.

## Signal Value

This is not new information — it is *pressure on an existing unresolved decision*. The enrichment pipeline (Source → Dedup → Context → Trust Scorer → Classifier → Router) and any L3/L4 loop are vapor without a 24/7 substrate. The local-vs-always-on partition heuristic from the playbook (which stages run on-demand vs. must be always-on) is a usable organizing axis for the hosted-mode spec.

## Proposed Actions

1. Promote hosted-mode from open-item to a decision needing a DDR: GitHub Actions vs. cloud service vs. dedicated machine (options already enumerated in CLAUDE.md).
2. Use the local/always-on partition as the structuring axis: classify each pipeline stage by whether it can be on-demand.
3. Do NOT adopt the playbook's vendor-adjacent hosting recommendation or its cost math without independent sourcing.
</content>
