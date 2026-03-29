---
id: SIG-002
timestamp: 2026-03-28T11:00:00Z
source: cowork-session
author: brien
confidence: 0.95
trust: 0.75
autonomy_level: L1
status: active
cluster: work-ontology-design
parent_signal:
related_intents: []
---
# Signal: Work is organized into three nested units: contract, process, tool

## Observation

Across multiple customer engagements (Subaru, Ari's team, internal), the same pattern appears:

1. **Contracts** — Agreements with vendors/customers (SLAs, scope, renewal cycles)
2. **Processes** — Business workflows running within or across contracts (e.g., vendor onboarding, invoice cycle, PR review)
3. **Tools** — Systems executing processes (Salesforce, Jira, payment platforms, code repos)

These nest: a contract spans multiple processes, a process uses multiple tools. This is the "unit structure" that autonomous systems need to reason about.

## Why It Matters

Autonomous operations (L2-L4) cannot work at the level of individual API calls or tickets. They need to understand *business context*. The work ontology provides it: where business drivers (contracts) create obligations, which decompose into processes, which require tools. A signal about an SLA breach means nothing without knowing the contract. A monitoring alert is just noise without knowing the process it's in.

## Trust Factors

- Clarity: Very High — this structure is observable across all engagements
- Blast radius: High — this structure defines how everything else is organized
- Reversibility: High — it's a naming convention, not a code/infra change
- Testability: High — can check that work units map cleanly to existing systems
- Precedent: Very High — same pattern in ITIL, work breakdown structures, product management
