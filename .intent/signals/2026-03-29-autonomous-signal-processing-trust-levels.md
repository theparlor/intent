---
id: SIG-012
timestamp: 2026-03-29T22:00:00Z
source: conversation
author: brien
confidence: 0.95
trust: 0.3
autonomy_level: L1
status: active
cluster: autonomous-infrastructure
parent_signal:
related_intents: [signal-lifecycle, autonomous-execution]
---
# Autonomous signal processing with trust-based execution levels

During interface design discussion, Brien articulated a fundamental shift in how signals should flow through the system. Rather than all signals requiring human triage and action, signals should be **worked as far along as they can go** with agent autonomy, and humans should only intervene when:

1. Something is deemed **unsafe** (high blast radius, security implications, irreversible)
2. The original intent is **too ambiguous** for agents to take confident action

When human intervention IS required, the system should not dead-end — it should **generate a new disambiguation signal** that re-enters the loop with enriched context.

## Autonomy Levels

- **L0 — Human drives:** Signal → human triages → human specs → human executes
- **L1 — Agent assists:** Agent enriches signal, human decides
- **L2 — Agent decides, human approves:** Agent drafts intent+spec, human rubber-stamps
- **L3 — Agent executes, human monitors:** Full loop for trusted signals, human sees results in Observe
- **L4 — Full autonomy with circuit breakers:** Agent runs full loop including deploy, generates disambiguation signals when stuck

## New Signal Properties Required

- **Trust score:** Confidence that an agent can resolve this without human input
- **Autonomy classification:** Recommended level based on trust, blast radius, contract testability
- **Provenance chain:** Links to parent signals for disambiguation trees
- **Builder-configurable thresholds:** "Anything above 0.8 trust with blast radius < 3 files can auto-execute"

## Deployment Topology Implication

This also surfaces a deployment model question: local CLI install vs. hosted web interface. The interface needs to support both modes via configuration — same tools, different backends. Start with static HTML reading from git (option 1), fast-follow with hosted service (option 2). The signal management interface is the forcing function for this decision.
