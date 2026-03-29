---
id: SIG-011
timestamp: 2026-03-29T10:00:00Z
source: cowork-session
author: brien
confidence: 0.8
trust: 0.50
autonomy_level: L1
status: active
cluster: bootstrap-tooling
parent_signal:
related_intents: []
---
# Signal: Bootstrap gap is "description-as-enabler" — we need to describe systems to automate them

## Observation

The gap between Intent (concept) and autonomous ops (running system) is not code. It's *specification infrastructure*. Before a system can be autonomous, it needs to be *described*: contracts, processes, policies, schemas. Right now, that description lives in spreadsheets, wikis, tribal knowledge. It's scattered.

## Why It Matters

Autonomous agents cannot run against undocumented systems. They need:
- What is the contract? (SLA, scope, vendor details)
- What is the process? (steps, rules, exceptions)
- What are the schemas? (valid states, transitions, edge cases)

This isn't "nice to have" documentation. It's the *specification layer* that makes autonomy possible. The bootstrap gap is: *how do we build this description layer fast enough for the three-year roadmap?*

## Trust Factors

- Clarity: High — the problem is concrete
- Blast radius: Very High — solution affects entire architecture
- Reversibility: Medium — description infrastructure is sticky once in place
- Testability: High — can measure description completeness
- Precedent: High — similar to "infrastructure-as-code" pattern
