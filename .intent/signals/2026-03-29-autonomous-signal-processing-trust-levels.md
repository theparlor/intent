---
id: SIG-012
timestamp: 2026-03-29T22:00:00Z
source: conversation
author: brien
confidence: 0.95
trust: 0.3
autonomy_level: L1
status: resolved
cluster: autonomous-infrastructure
parent_signal:
related_intents: [signal-lifecycle, autonomous-execution]
upstream_control_path: ".intent/config/approval-rules.yml; spec/signal-trust-framework.md; trust/autonomy_level/parent_signal frontmatter fields present across the signal corpus"
catch_mechanism: "The trust formula and L0 through L4 ladder are specced and the fields are populated on essentially every signal written since; the approval-rules.yml gate enforces L0 for external actions; CLAUDE.md 'When Stuck' documents the disambiguation-signal pattern"
verification_command: "grep -c '^autonomy_level:' /Users/brien/Workspaces/Core/frameworks/intent/.intent/signals/*.md | grep -vc ':0' "
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

This also surfaces a deployment model question: local CLI install vs. hosted web interface. The interface needs to support both modes via configuration, same tools, different backends. Start with static HTML reading from git (option 1), fast-follow with hosted service (option 2). The signal management interface is the forcing function for this decision.

## Triage, 2026-07-08

Disposition: control exists now. Trust score, autonomy classification, and provenance chain are all live schema fields, not proposals. Builder-configurable thresholds live in .intent/config/approval-rules.yml. The deployment-model question (local vs hosted) is answered in practice: local file-native mode is what actually shipped and runs; hosted mode stays an explicitly documented "planned" option in CLAUDE.md rather than an open gap this signal is still waiting on.
