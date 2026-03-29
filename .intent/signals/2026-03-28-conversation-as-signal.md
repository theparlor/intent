---
id: SIG-003
timestamp: 2026-03-28T12:00:00Z
source: cowork-session
author: brien
confidence: 0.9
trust: 0.35
autonomy_level: L1
status: active
cluster: signal-capture-surfaces
parent_signal:
related_intents: []
---
# Signal: Conversations should automatically feed the notice layer

## Observation

During the Cowork session that produced the work ontology and OTel mapping, Brien asked: "Should conversations (developer + AI) be a signal capture surface?" The answer was yes—they should feed the notice layer with observations about design patterns, misunderstandings, and emergent intents that become visible only through conversation.

## Why It Matters

Conversations are a *discovery mechanism* for intents. A developer and AI thinking through a problem surface observations that are not present in code, tickets, or traces. This is where nuance, context switching, and design reasoning live. If not captured, it's lost at context close.

## Trust Factors

- Clarity: High — the pattern is evident once noticed
- Blast radius: Medium — depends on downstream systems using this signal
- Reversibility: High — adding new signal sources is low-cost
- Testability: Medium — "captured signals" are in the repo; hard to test *omission*
- Precedent: High — Slack reactions and PR comments already do this informally
