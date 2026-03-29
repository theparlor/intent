---
id: SIG-004
timestamp: 2026-03-28T13:00:00Z
source: cowork-session
author: brien
confidence: 0.8
trust: 0.55
autonomy_level: L1
status: active
cluster: work-ontology-design
parent_signal:
related_intents: []
---
# Signal: OTel spans map naturally to work units (contract, process, tool)

## Observation

During ontology design, Brien noticed that OpenTelemetry spans already model hierarchical work. A contract (customer agreement) spans multiple processes (vendor onboarding, invoice handling), which span tools (Salesforce, Jira, payment system). This is *exactly* the work structure needed for autonomous ops.

## Why It Matters

OTel is already instrumented in production systems. Rather than invent a new telemetry layer, the signal framework can map OTel spans to the work ontology, immediately giving visibility into how work flows and where it breaks. This makes autonomous signal capture possible without added instrumentation burden.

## Trust Factors

- Clarity: High — OTel hierarchy is explicit
- Blast radius: High — changes how we instrument everything
- Reversibility: High — just a mapping layer, non-destructive
- Testability: High — OTel data is queryable
- Precedent: Medium — few projects do this yet
