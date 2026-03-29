---
id: SIG-012
timestamp: 2026-03-29T10:30:00Z
source: cowork-session
author: brien
confidence: 0.85
trust: 0.70
autonomy_level: L1
status: active
cluster: autonomous-infrastructure
parent_signal:
related_intents: []
---
# Signal: Multi-machine requirement means cloud processing must be always-on

## Observation

When developers work offline or switch devices, intent signals must still flow. Processing cannot block on the laptop. This means:
- Signals must sync to cloud (async)
- Cloud agents process and store results
- When laptop comes online, it syncs back results
- Trust scoring and autonomous actions run in cloud, not locally

This is different from "cloud-enabled" tools. It requires *persistent cloud infrastructure* running at all times, not just when the user is active.

## Why It Matters

The bootstrap roadmap assumes L3-L4 autonomous ops running 24/7. This requires always-on cloud processing. A hosted SaaS is not optional; it's architectural. This also affects security/compliance: cloud processing handles customer data, so compliance review is early-path work.

## Trust Factors

- Clarity: High — the requirement is technical and clear
- Blast radius: Very High — affects deployment, security, and business model
- Reversibility: Low — architectural decisions are hard to reverse
- Testability: High — can test sync and cloud execution independently
- Precedent: Very High — similar to Slack, GitHub, Figma architectures
