---
id: SIG-2026-05-31-exposed-vocabulary-divergence-principle
type: architectural-principle
status: active
date: 2026-05-31
confidence: 0.88
source: "Brien directive, 2026-05-31 — ratification-gating question on the D1–D4 spec vocabulary"
exposure: public
strategic_value: 0.80
blast_radius: low
irreversibility: 0.0
autonomy_level: L4
related:
  - SIG-2026-05-31-personal-synthesis-layer-commoditizing
  - SIG-2026-05-31-personal-memory-altitude-mismatch
  - SIG-2026-05-31-verbatim-passthrough-differentiator
proposed_edges:   # SURFACED for review — NOT wired
  - "constrains → SPEC-substrate-exposure-envelope-extensions-DRAFT §0 (vocabulary reconciliation)"
  - "candidate principle → coherence-engineering naming/boundary canon (cross-product)"
---

# Exposed-surface vocabulary must intentionally diverge from a validating category

## What I noticed

The first draft of the D1–D4 envelope spec imported the validating category's vocabulary:
`vault` (literally Obsidian's term), `rule`/`fact`/`belief` (the memory category's
knowledge-representation triad), and `brief` / `context_block` / `STM`/`LTM` (memory-product
generics). Brien flagged this **at the ratification gate** — before approving, he asked "are we
using their vocabulary or our own?"

## The principle (reusable)

When a downstream category validates our prior design (see
[[SIG-2026-05-31-personal-synthesis-layer-commoditizing]]), the vocabulary on our
externally-exposed surfaces — MCP verbs, envelope fields, contract names — must be:

1. **Intentionally NOT 100% matched** to the category's terms. Reasons: avoid derivative/IP and
   positioning challenges, and signal that we operate one altitude up (S2), not as a me-too memory
   product.
2. **Anchored in our preexisting patterns + metaphors** — `query`/`get`/`list` verbs, "slice",
   "traceability chain", `chain_audit`, "conservation law", "context supply chain", `tagline`, and
   the Intent ontology (DDR/observation/signal).
3. **Clear on layer and boundary** — each term should name its altitude and its boundary role.

## Why it matters

Vocabulary is positioning. Borrowing the category's words concedes the altitude argument and
invites "you're just an X" challenges. Our words must encode that we sit *above* the engine.

## Where applied

First applied in the D1–D4 reconciliation (`SPEC-substrate-exposure-envelope-extensions-DRAFT` §0):
`brief→sightline`, `injection_policy→supply_policy`, `rule/fact/belief→normative/grounded/provisional`,
`get_context_block→get_core`, `search_vault→query` (existing), `audit_gaps→audit_chain`,
`verbatim-passthrough→preservation_invariant`. Generalizes to every exposed surface (Cast / Voices
/ Forge MCP renderings) and every future category-validation moment.

## Confidence & source

- **Confidence:** 0.88 — a Brien-stated directive, reusable across surfaces.
- **Source:** ratification-gate exchange, 2026-05-31.
