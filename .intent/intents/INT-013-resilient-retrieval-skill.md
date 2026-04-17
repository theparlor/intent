---
id: INT-013
title: Build a resilient sequential retrieval skill for persona enrichment
timestamp: 2026-04-11T22:00:00Z
signals:
  - SIG-029
  - SIG-026
priority: now
status: proposed
---

# INT-013: Resilient Sequential Retrieval Skill

## Problem

Parallel sub-agent retrieval consistently stalls on large web sweeps. Agents self-report completion without actually finishing. No incremental save mechanism exists in the current ad-hoc approach.

## Intent

Create a persona enrichment skill that encodes the proven sequential pattern: phased source-type sweeps, batch sizes of 10-15, disk writes after each batch, explicit progress tracking with completion percentages (not just structural completeness), and continuation protocols for multi-session sweeps.

## Acceptance criteria

- Skill template exists in the skills engine
- Batched retrieval with numbered file output
- Progress tracking: X of Y posts fetched, not "depth score N"
- Continuation protocol: new session can pick up where previous left off by reading inventory file
- Works in both Claude Code and Cowork dispatch contexts
