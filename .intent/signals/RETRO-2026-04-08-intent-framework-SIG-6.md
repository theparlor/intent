---
signal_id: RETRO-2026-04-08-intent-framework-SIG-6
title: Karpathy LLM Knowledge Bases, Intent OS, and Skills Engine independently converge on same compilation patterns
severity: medium
detected: 2026-04-05
status: open
source: retroactive-extraction
trust_score: 0.55
autonomy: L2
---
# Karpathy × Intent × Skills Engine Convergence

## Observation
A parallel session produced a handoff package mapping Karpathy's LLM Knowledge Base pattern (raw/ → wiki/ → schema, with ingest/query/lint) onto the Intent project's three-layer architecture. This session independently arrived at identical patterns for the skills engine: artifact registry (Karpathy's _index.md), lint operations (freshness/contradiction/coverage), and compilation-over-retrieval as core principle.

## Context
Handoff package ingested to Core/frameworks/intent/reference/karpathy-synthesis/ (4 files). The parallels shaped the context resolver, signal detector, and intent journal's pattern compilation.

## Implication
- Three independent systems converge on: compile once → keep current → lint for health → compound queries back into corpus
- Brien's consulting practice IS a domain knowledge base — Workspaces is his wiki, skills engine is his compiler, engagement folders are his raw/
- The Intent project (theparlor.github.io/intent) and Skills Engine share architectural DNA but serve different outputs (software specs vs. consulting intelligence)
- Future integration: Intent's wiki/ pattern could formalize what Workspaces already does informally
