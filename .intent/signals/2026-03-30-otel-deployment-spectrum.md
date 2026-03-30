---
id: SIG-017
title: OTel deployment is a spectrum, not a binary choice
type: insight
source: conversation
source_context: Claude mobile session — OTel vs Kafka vs MQTT clarification
date: 2026-03-30
status: active
cluster: observability
autonomy_level: L2
tags: [otel, observability, events, infrastructure, grafana]
---

# SIG-017: OTel deployment is a spectrum, not a binary choice

## Observation

Brien asked how OTel relates to Kafka, MQTT, and Confluent — revealing a common conflation of three distinct architectural layers. The clarification surfaced a clean deployment progression for Intent's event system.

## Three Layers (Not Competing Choices)

| Layer | What It Does | Examples |
|-------|-------------|----------|
| **Format** | Defines the event envelope | OpenTelemetry (traces, spans, metrics, logs) |
| **Transport** | Moves events from producers to consumers | Kafka, MQTT, Confluent, HTTP |
| **Reader** | Ingests, stores, queries, visualizes | Datadog, Grafana, Jaeger, Honeycomb |

OTel is the **format**, not the pipe or the dashboard. You instrument once with OTel, then send to whatever backend.

## Intent's Deployment Spectrum

| Stage | Infrastructure | When |
|-------|---------------|------|
| **Phase 0** | `events.jsonl` — append-only file in git | Now (solo practitioner) |
| **Phase 1** | OTel Collector → Grafana Cloud free tier (50GB traces/month) | When you want dashboards |
| **Phase 2** | OTel Collector → Grafana + alerting | When teams need monitoring |
| **Phase 3** | Kafka for high-volume multi-consumer fan-out | Teams-of-teams scale |

## Key Insight

Intent's existing event schema (JSONL with OTel-compatible envelope) means upgrading from Phase 0 to Phase 1 is a **configuration change, not a rewrite**. The schema already carries the right shape.

## Validates

- SIG-002 on site / SIG-002 in local signals (OTel is the right observability model)
- The decision to use JSONL as Phase 0 storage was architecturally sound

## Implication

The work-system page and schemas page should present this as a progressive deployment story, not "you need OTel infrastructure to start." Intent works with a flat file and scales to distributed tracing.
