---
id: SIG-027
timestamp: 2026-04-06T10:00:00Z
source: conversation
confidence: 0.9
trust: 0.7
autonomy_level: L2
status: active
cluster: methodology-adoption
author: brien
related_intents: []
referenced_by: []
parent_signal: SIG-025
---
# Intent, Knowledge Engine, and Knowledge Farm are three distinct things

Brien identified a boundary collapse during Layer 1 implementation: Intent (methodology for how teams build products), the Knowledge Engine (product for compiling domain knowledge), and Brien's Knowledge Farm (a specific instance) were being conflated.

Intent prescribes "you need compiled domain knowledge." The Knowledge Engine provides the pattern for doing it. A Knowledge Farm is a specific deployment. Brien's farm feeds Intent because his domain overlaps — this is coincidental, not structural.

**Resolved by:** Restructured repo with `knowledge-engine/` subdirectory. Spec: `knowledge-engine/spec/boundary.md`. Decision: DDR-005.

## Trust Factors

- Clarity: 0.9 — Three levels clearly defined with explicit boundary
- Blast radius: 0.3 — Additive restructuring, no functionality changed
- Reversibility: 0.9 — Directory structure can be flattened back
- Testability: 0.7 — Validates when KE is used independently of Intent
- Precedent: 0.7 — Mirrors methodology/product/instance pattern common in frameworks
