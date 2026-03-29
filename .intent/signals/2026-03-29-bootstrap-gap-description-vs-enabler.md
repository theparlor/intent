---
id: SIG-006
timestamp: 2026-03-29T18:00:00Z
source: conversation
author: brien
confidence: 0.95
trust: 0.55
autonomy_level: L2
status: active
cluster: bootstrap-tooling
parent_signal:
related_intents: [notice-product, adoption]
---
# Intent is a description, not an enabler — practitioners can understand it but can’t install and test it Monday morning

Ari could read everything we’ve built and reconstruct Intent from scratch, but he couldn’t enable his existing dev work with a plugin and test it out Monday morning on real code. The gap between "I understand the methodology" and "I’m running it on my repo" is the entire bootstrap kit problem.

This is the difference between a whitepaper and a product. The methodology docs are the whitepaper. The MCP server + CLI + GitHub Action are the product.

Evidence: Every prior artifact was a spec, decision, or explanation. Zero artifacts were installable tools. The quickstart guide didn’t exist until this signal was noticed.
