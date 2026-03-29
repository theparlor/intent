---
id: SIG-008
timestamp: 2026-03-29T08:00:00Z
source: cowork-session
author: brien
confidence: 0.75
trust: 0.35
autonomy_level: L0
status: active
cluster: autonomous-infrastructure
parent_signal:
related_intents: []
---
# Signal: "Ceremony wall" — agile ceremonies are becoming expensive overhead

## Observation

During autonomy level discussions, a team lead mentioned: "We spend 3-4 hours per sprint on ceremonies (standups, planning, retro). With faster autonomous execution, that's now a bottleneck. We're either cutting ceremonies or moving to async specs." This is happening across multiple teams.

## Why It Matters

As autonomy increases (L2+), team synchronization overhead becomes the constraint. Ceremonies were designed for human-paced work. If agents execute in minutes, humans waiting for the next standup is inefficient. This signals a shift: from ceremony-driven coordination to spec-driven automation.

## Trust Factors

- Clarity: Medium — anecdotal but consistent
- Blast radius: Medium — affects team structure and process, not code
- Reversibility: Very High — can revert to ceremonies anytime
- Testability: Medium — hard to measure ceremony cost in isolation
- Precedent: High — similar shifts in CI/CD, infrastructure automation
