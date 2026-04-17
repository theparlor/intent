---
decision_id: RETRO-2026-04-08-intent-framework-2
title: Precedent starts at zero — system bootstraps conservatively and earns autonomy
date: 2026-04-05
status: accepted
source: retroactive-extraction
session_date: 2026-04-08
---
# Bootstrap Constraint: Precedent Starts at Zero

## Context
Building the signal scoring model, the precedent dimension (weight 0.15) anchors to the intent journal. With an empty journal, precedent = 0 for all investigation types. This forces the system to start at L0-L1 for autonomous investigation.

## Decision
This is intentional, not a limitation. The bootstrap sequence:
1. **Week 1-2:** Everything L0-L1. System logs signals, enriches silently.
2. **Week 3-4:** First L2 investigations as signal patterns recur.
3. **Month 2:** L3 hypotheses for patterns with 5+ successful L2 priors.
4. **Month 3+:** L4 for patterns with 5+ successful L3 priors where Brien consistently acted.

The timeline isn't calendar-based — it's precedent-accumulation-based. Weekly patterns reach L4 faster than monthly ones.

## Alternatives Considered
- **Start at L3 with manual overrides downward** — faster autonomy but no demonstrated performance. Brien's trust is assumed, not earned.
- **Start at L0 with manual overrides upward** (chosen) — slower but self-correcting. The journal's pattern compiler automatically promotes investigation types that succeed.
- **Configuration-based trust levels** — pre-set trust per investigation type. Rejected: creates a maintenance burden and misses the learning loop.

## Consequences
- The first 10-15 journal entries are critical for earning autonomy
- Brien's approval/dismissal feedback matters more in early weeks (each data point has outsized influence on precedent)
- The system must make it easy for Brien to rate outputs (even a thumbs-up/down captures the signal)
