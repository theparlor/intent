---
id: SIG-037
timestamp: 2026-05-16T00:00:00Z
source: knowledge-ingest
confidence: 0.7
trust: 0.35
autonomy_level: L1
status: captured
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
