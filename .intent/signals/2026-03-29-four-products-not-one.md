---
id: SIG-013
timestamp: 2026-03-29T11:30:00Z
source: cowork-session
author: brien
confidence: 0.80
trust: 0.65
autonomy_level: L1
status: active
cluster: bootstrap-tooling
parent_signal:
related_intents: []
---
# Signal: Intent has four product shapes, not one

## Observation

During product roadmap planning, it became clear that Intent isn't a single product. It's four products at different layers:

1. **Developer OS** — Notice/spec loop inside IDE/Cowork (personal layer)
2. **Team Foundation** — Shared spec library, signal feed, trust dashboard (team layer)
3. **Autonomous Platform** — Multi-agent orchestration, L2-L4 execution (infrastructure layer)
4. **Commercial Service** — SaaS for customers managing complex work (commercial layer)

Each has different UI, pricing, security model. Conflating them causes confusion and poor roadmap prioritization.

## Why It Matters

A roadmap that tries to be "all things to all users" ships nothing. Clarity on which product solves which problem lets teams move in parallel and use different tooling. It also clarifies go-to-market: the OS is Bootstrap, the Platform is Enterprise, the Service is SaaS.

## Trust Factors

- Clarity: High — the four shapes are distinct once named
- Blast radius: Very High — affects positioning, roadmap, teams, and go-to-market
- Reversibility: Medium — product direction is hard to reverse
- Testability: High — can validate with customer interviews
- Precedent: Very High — successful platforms (Kubernetes, Vercel, AWS) all have layered products
