---
id: SIG-007
timestamp: 2026-03-29T07:30:00Z
source: cowork-session
author: brien
confidence: 0.9
trust: 0.80
autonomy_level: L1
status: active
cluster: signal-capture-surfaces
parent_signal: SIG-003
related_intents: []
---
# Signal: Signals must be captured from multiple surfaces: conversation, OTel, Slack, PRs, agent traces

## Observation

During signal framework design, it became clear that no single source captures all observations. Signals come from:
- **Conversation** — human→AI discussion, reasoning aloud
- **OTel spans** — system behavior, bottlenecks, errors
- **Slack** — team observations, incident discussions
- **PR reviews** — design decisions, technical debt comments
- **Agent traces** — what agents noticed while executing

Each surface has different latency, noise, and trust profile. Cowork/IDE is high-trust/low-latency. Slack is medium-trust/medium-latency. OTel is automated/always-on but noisy.

## Why It Matters

Signals from a single source miss blind spots. A contract issue might show up in OTel (slow responses) but only get *named* in conversation. A process bottleneck might live in Slack discussion for weeks before a PR comment makes it actionable. The framework must ingest *all* surfaces and synthesize them.

## Trust Factors

- Clarity: Very High — multiple surfaces are observable
- Blast radius: High — affects architecture of signal ingestion
- Reversibility: High — can add/remove surfaces without breaking core logic
- Testability: High — each surface has auditable input
- Precedent: Very High — modern observability tools do this (Datadog, New Relic, etc.)
