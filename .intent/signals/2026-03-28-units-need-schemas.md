---
id: SIG-006
timestamp: 2026-03-28T15:00:00Z
source: cowork-session
author: brien
confidence: 0.75
trust: 0.45
autonomy_level: L1
status: active
cluster: work-ontology-design
parent_signal:
related_intents: []
---
# Signal: Work units (contract, process, tool) need structured schemas

## Observation

The work ontology defines what *exists* (contracts, processes, tools), but not how to *describe* them. A contract needs fields like `vendor`, `term`, `renewal_date`, `status`. A process needs `owner`, `steps`, `handoff_points`, `sla`. Without schemas, signals about work units are free text—hard to query, integrate, or score for trust.

## Why It Matters

Schemas are the boundary between human-readable signals and machine-actionable intents. With schemas, a signal like "Contract with Acme expires in 30 days" can be parsed into structured metadata, matched against risks, and escalated automatically. Without them, signals are just comments.

## Trust Factors

- Clarity: High — the need is obvious once stated
- Blast radius: Very High — schemas define downstream automation
- Reversibility: Medium — schema changes require migration
- Testability: High — schema validation is testable
- Precedent: Very High — every data system uses schemas
