---
id: CLU-002
name: "observability"
title: "Observability"
status: active
signals: [SIG-002, SIG-017]
weight: 0.7
formed_date: 2026-03-30
promoted_to: ""
promoted_date:
---
# Cluster: Observability

## Theme
OTel is the right observability model for Intent, and deployment is a spectrum not a binary. SIG-002 established that distributed tracing maps directly onto Intent's work hierarchy — the same architecture designed for multi-service systems applies to multi-agent work systems. SIG-017 clarified that OTel deployment doesn't require a full-stack commitment; teams can start with file-based JSONL and progressively adopt the Collector, Grafana, and dashboards as needs grow. Together these signals define the observability philosophy: start simple, grow into OTel's full model.

## Member Signals

| Signal | Title | Trust | Date |
|--------|-------|-------|------|
| SIG-002 | Distributed tracing is the right observability model for Intent work | 0.50 | 2026-03-28 |
| SIG-017 | OTel deployment is a spectrum, not a binary choice | 0.50 | 2026-03-30 |

## Promotion Criteria
A cluster is ready for promotion to intent when:
- [ ] 3+ signals with independent sources
- [ ] Aggregate weight > 1.0 (sum of trust scores)
- [x] At least one signal from the last 14 days (not stale)
- [x] Pattern is actionable (not just an observation)

## Emergence Notes
How did this cluster form? Was it:
- **Human-noticed:** Brien identified the OTel-as-model pattern in the founding Cowork session (SIG-002) and refined the deployment stance during the mobile session (SIG-017). Both signals share the observability domain.

## Open Questions
- Is the 27KB observability-stack.md spec still accurate after the four-product reframing?
- When does the file-based JSONL approach hit its ceiling? At what team size or event volume?
- Does this cluster need a third signal (e.g., from practitioner feedback) to reach promotion weight?
