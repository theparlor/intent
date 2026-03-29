---
id: SIG-010
timestamp: 2026-03-29T09:30:00Z
source: cowork-session
author: brien
confidence: 0.9
trust: 0.75
autonomy_level: L1
status: active
cluster: signal-capture-surfaces
parent_signal: SIG-003
related_intents: []
---
# Signal: Signals die when context switches unless captured immediately

## Observation

When a developer notices something (in code, during a conversation with AI, in a meeting, in an email), they often don't *write it down*. They say "Yeah, that's weird" and move on. Minutes later, context switches to another problem, and the observation is forgotten. It becomes noise in Slack, a stale wiki comment, or tribal knowledge.

## Why It Matters

High-value signals are *fleeting*. They exist at the intersection of experience and attention. If not captured within seconds of the observation, they're lost. This means signal capture must be:
- **Immediate** — In the flow of work, not a separate step
- **Low-friction** — One-word observations should be capturable
- **Multimodal** — Slack reaction, voice note, copy-paste, conversation continuation

Without this, the signal framework only captures "big obvious stuff" and misses the nuanced patterns.

## Trust Factors

- Clarity: Very High — developers experience this daily
- Blast radius: High — affects UX/flow design, not core logic
- Reversibility: Very High — can change capture surfaces anytime
- Testability: Medium — hard to measure "missed signals"
- Precedent: Very High — why Slack reactions and Twitter favorites exist
