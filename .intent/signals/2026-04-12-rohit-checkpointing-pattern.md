---
id: SIG-033
title: Checkpointing pattern should be first-class in persona enrichment pipeline, not just a prompt instruction
timestamp: 2026-04-12T01:00:00Z
source: external-article
author: brien
confidence: 0.9
trust: 0.9
autonomy_level: L3
status: active
cluster: bootstrap-tooling
referenced_by:
  - "Rohit @rohit4verse, 'How to Build a Production-Grade AI Agent' (Feb 2026), Principle 8"
  - "SIG-029: Resilient sequential retrieval pattern"
---

# SIG-033: Checkpointing as First-Class Pipeline Capability

## What was noticed

Rohit's Principle 8 (Reliability Mechanics) describes checkpointing: "save the agent state at logical boundaries so you can resume from the last checkpoint rather than restarting a massive task from zero."

We arrived at this same pattern empirically during persona enrichment — the "write to disk after every batch of 10-15 items" approach was a manual workaround for the absence of proper checkpointing. But it's currently encoded as a prompt instruction ("write after every phase"), not as a pipeline capability.

The difference matters: a prompt instruction can be ignored by the agent (and has been, repeatedly). A pipeline capability enforces the checkpoint mechanically — the same way Rohit argues security must exist outside the LLM reasoning loop.

## Evidence

Multiple persona enrichment passes reported "done" without completing all phases. The sequential write-to-disk pattern was adopted after parallel agents stalled twice. But even with the pattern in prompts, agents sometimes accumulated results in memory across phases rather than writing incrementally.

Rohit: "define incredibly explicit completion conditions, such as the task being explicitly completed, the maximum mathematical iterations being reached, timeouts being exceeded, or encountering an unrecoverable system error."

## Implication

The persona enrichment skill (INT-013) should implement checkpointing as code, not as prompt instructions. Each phase writes a checkpoint file. The next phase reads the checkpoint before starting. If a session dies mid-phase, the next session reads the last checkpoint and resumes. This is Dex Horthy's "mechanical enforcement over trust-based collaboration" applied to the retrieval pipeline.
