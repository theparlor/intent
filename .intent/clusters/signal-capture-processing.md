---
id: CLU-003
name: "signal-capture-processing"
title: "Signal Capture & Processing"
status: active
signals: [SIG-003, SIG-008, SIG-011, SIG-015]
weight: 1.95
formed_date: 2026-03-30
promoted_to: ""
promoted_date:
---
# Cluster: Signal Capture & Processing

## Theme
Multi-surface capture and signal amplification through reference frequency. Conversations should feed the notice layer automatically (SIG-003). Signals die in the gap between where they're noticed and where the system can see them (SIG-008). Capture needs to cover every surface where practitioners work (SIG-011). And signals that get referenced frequently should be amplified — reference frequency is a trust signal in itself (SIG-015). Together these define the Notice product's core challenge: capture signals wherever they occur and use cross-reference patterns to surface the ones that matter most.

## Member Signals

| Signal | Title | Trust | Date |
|--------|-------|-------|------|
| SIG-003 | Conversations should automatically feed the notice layer | 0.35 | 2026-03-28 |
| SIG-008 | Signals die in the gap between where they're noticed and where the system can see them | 0.60 | 2026-03-29 |
| SIG-011 | Signal capture needs to cover every surface where practitioners work — not just the IDE | 0.45 | 2026-03-29 |
| SIG-015 | Signal amplification through reference frequency | 0.55 | 2026-03-29 |

## Promotion Criteria
A cluster is ready for promotion to intent when:
- [x] 3+ signals with independent sources
- [x] Aggregate weight > 1.0 (sum of trust scores)
- [x] At least one signal from the last 14 days (not stale)
- [x] Pattern is actionable (not just an observation)

## Emergence Notes
How did this cluster form? Was it:
- **Human-noticed:** Brien flagged the capture gap pattern across the founding session (SIG-003) and subsequent conversations about signal loss, multi-surface requirements, and amplification. The `signal-capture-surfaces` cluster tag was assigned to SIG-008, SIG-011, and SIG-015 during scoring.

## Open Questions
- What's the minimum viable capture surface set? MCP + CLI + Slack covers most of Brien's flow, but does it generalize?
- How should `referenced_by` be populated — manually, or automatically by scanning signal cross-references?
- What reference frequency threshold should trigger amplification?
