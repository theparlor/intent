---
id: INT-002
title: "Build signal amplification pipeline with reference tracking"
status: proposed
proposed_by: "system"
proposed_date: 2026-03-30T22:00:00Z
accepted_date:
signals: [SIG-003, SIG-008, SIG-011, SIG-015]
specs: []
owner: ""
priority: now
product: notice
---
# Build signal amplification pipeline with reference tracking

## Problem
Signals are static after capture. Their trust scores don't evolve as evidence accumulates. When a signal gets referenced repeatedly — in conversations, commits, other signals, specs — that frequency is information, but the system doesn't track it. High-value signals look identical to noise until a human manually reviews them. The signal capture cluster (4 signals, weight 1.95) consistently identifies this gap: capture is operational, but enrichment is missing.

## Desired Outcome
Every signal tracks who and what references it. Reference frequency feeds into an amplification score that adjusts effective trust over time (7-day half-life decay). Signals that keep getting referenced naturally rise in priority. Signals that go unreferenced naturally decay. The enrichment pipeline computes this automatically — no human triage required for the mechanical part.

## Evidence
- **SIG-003:** Conversations should auto-feed the notice layer — every reference in a conversation is a signal about signal importance
- **SIG-008:** Signals die in context switches — multi-surface capture means the same observation gets referenced from different tools
- **SIG-011:** Multi-surface capture requirement — 5 tiers of capture, each producing references to existing signals
- **SIG-015:** Signal amplification through reference frequency — the spec for this exact mechanism (reference weights, time decay, co-reference clustering)

## Constraints
- Must be backwards-compatible with existing 24 signals (add `referenced_by: []` field, don't break parsing)
- Amplification formula from spec/signal-amplification.md: `amplification = Σ weight(ref) × decay(age)`
- Reference weights: signal=0.15, conversation=0.10, commit=0.05, intent/spec=0.20
- Half-life: 7 days (configurable in .intent/config.yml when it exists)
- Must work in local mode (file-based) — no database required
- Autonomy level crossing (e.g., L1→L2) should emit a signal.updated event with boundary_crossed flag

## Open Questions
- Should the enrichment agent run as a scheduled job (cron/launchd) or on-demand when new signals arrive?
- How do we detect references in conversations? (Cowork transcripts aren't in .intent/ yet)
- Should co-reference clustering (signals referenced together) auto-suggest merges?
