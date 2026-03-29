---
id: SIG-009
timestamp: 2026-03-29T08:30:00Z
source: conversation
author: brien
confidence: 0.85
trust: 0.70
autonomy_level: L2
status: active
cluster: autonomous-infrastructure
parent_signal: SIG-002
related_intents: []
---
# Signal: Ari's team rewired tickets as bot specifications

## Observation

Ari's team (engineering leader) described a shift: their Jira tickets are no longer human task assignments. They're *specifications for autonomous agents*. A ticket says "Validate this contract against our SLA requirements" — the spec is precise enough that a bot can read it, run logic, and report results. Refinement sessions are *design sessions*, not estimation meetings.

## Why It Matters

This is the bridge from Intent (notice→spec→execute→observe) to autonomous operations at L2-L3. Tickets are already written as specs; they just need to be machine-readable. This means:

- Refinement is actually design work (beneficial)
- Execution can be automated (efficiency)
- Observation/results feed back as signals (learning loop)

This is live, working evidence that the spec-driven loop is viable in real teams.

## Trust Factors

- Clarity: High — Ari described it clearly
- Blast radius: High — affects how teams write tickets
- Reversibility: High — teams can revert to human assignments
- Testability: High — bot success rate is directly observable
- Precedent: Medium — not yet mainstream, but growing
