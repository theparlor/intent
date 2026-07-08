---
signal_id: RETRO-2026-04-08-intent-framework-SIG-8
title: Methodology volume risk — 8 new files in methodology/meta/ may create approachability barrier
severity: low
detected: 2026-04-05
status: open
source: retroactive-extraction
trust_score: 0.35
autonomy: L1
---
# Methodology Volume Risk

## Observation
This session produced 8 files in methodology/meta/ (intent-taxonomy, skill-graph, context-resolver, attribution-chain, intent-journal, signal-scoring, autonomous-investigation, plus the existing skill-authoring-patterns). The methodology layer is internally consistent but dense. A new session inheriting this needs to read ~50KB of methodology before operating — most of which it won't need for any single execution.

## Context
Echoes SIG-026 (system complexity approachability). The methodology is sound but the volume creates a loading problem for sessions with tight context windows.

## Implication
- The intent-orchestrator SKILL.md is the entry point — it should be sufficient for most executions without reading all 8 methodology files
- Consider a "methodology summary" file that compresses the key concepts into a 1-page reference
- The skill graph compositions contain the operational decisions; the rest is rationale/governance
- This is manageable today (Opus 4.6 1M context) but becomes a real constraint on Copilot or system-prompt platforms

## Triage, 2026-07-08

Disposition: still pending, low urgency (trust_score 0.35, this signal's own self-assessment). No methodology-summary or 1-page reference file exists that compresses the meta/ layer for fast session loading. Given the methodology directory has grown substantially since this signal (not shrunk), the approachability concern this signal raised has not been addressed, only outgrown its original scope.
