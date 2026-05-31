---
id: SIG-2026-05-31-verbatim-passthrough-differentiator
type: differentiator-reaffirmation
status: active
date: 2026-05-31
confidence: 0.90
source: "category architecture analysis (2026-05-31 session) read against Voices' conservation law (voices/INTENT.md, spec/SPEC-001-voices-dissent-preservation.md, INV-1..INV-11)"
exposure: public
strategic_value: 0.88
blast_radius: low
irreversibility: 0.0
autonomy_level: L4
provenance_note: >
  Reaffirms a PRIOR architectural commitment. Voices' dissent-preservation conservation law
  predates this scan (VC-004, 2026-04-22; conservation law stated in voices/INTENT.md). This
  signal records that the commoditizing synthesis category structurally CANNOT offer it — it
  is validation that the existing constraint is a moat, not a new idea.
related:
  - SIG-2026-05-31-personal-synthesis-layer-commoditizing
  - SIG-2026-05-31-personal-memory-altitude-mismatch
  - SIG-2026-05-31-exposed-vocabulary-divergence-principle
proposed_edges:   # SURFACED for review — NOT wired into any decision log (see session response)
  - "reaffirms → Core/products/voices/INTENT.md 'The Conservation Law' + SPEC-001-voices-dissent-preservation (INV-1..INV-11) + VC-004"
  - "feeds → SPEC-substrate-exposure-envelope-extensions-DRAFT (preservation_invariant on the MCP envelope)"
  - "candidate DDR → 'a preservation_invariant is REQUIRED on the substrate-exposure MCP surface'"
---

# Verbatim persona passthrough is architecturally hostile to the synthesis category — protect it

> **Framing.** This is a reaffirmation of a constraint we already hold, not a new design.
> Voices' conservation law is on disk and dated earlier. The signal's value is recognizing
> that the commoditizing category *cannot copy it* — so the constraint is a differentiator,
> and should be protected and exposed deliberately.

## What I noticed

Synthesis layers **rewrite by definition.** Their core operation is compression: take many
sources, produce a digest. That operation is *lossy by design* — it paraphrases, merges, and
smooths. The whole personal-synthesis category ([[SIG-2026-05-31-personal-synthesis-layer-commoditizing]])
is built on this.

**Verbatim persona passthrough is architecturally hostile to that.** You cannot have a
synthesis broker that also guarantees verbatim, attributed, per-source preservation — the
defining operation of the first destroys the guarantee of the second. A memory layer that
merges two contradictory claims into one "fact" has, by construction, deleted the dissent.

## Why it matters now

This reaffirms **Voices' conservation law** as a category-level differentiator:

> *Dissent is conserved across every transformation … iteration loops may optimize against
> `machine_assertions` freely, but must pass a PRESERVATION CHECK on `named_dissents`*
> (`voices/INTENT.md`; enforced by INV-1..INV-11 in `spec/SPEC-001-voices-dissent-preservation.md`).

Where the synthesis category aggregates to consensus, Voices preserves the full disagreement
surface verbatim, per persona slug. **No synthesis broker offers this** — not as a feature gap,
but as an architectural impossibility within their model. (Conservation law as moat — the same
shape as Witness's append-only "no merge verb" law: two contradictory writers produce two
records, never one merged record.)

## Implication (protect + expose)

The substrate-exposure MCP surface should carry a **REQUIRED `preservation_invariant`** — the
contract the category structurally lacks. Concretely:

- At the exposure layer (`servers/knowledge.py` envelope), `grounded` and `provisional` items
  with named provenance MUST be returned **verbatim with source preserved** — no synthesis-rewrite
  at the exposure boundary. (Pairs with D2 supply-policy typing — see SPEC-DRAFT.)
- This is the envelope-level analog of Voices' `named_dissents` preservation check: dropping or
  paraphrasing a sourced item at the exposure layer is a regression, not "cleanup."

This is a moat at the judgment/critique altitude. It is cheap to hold (it is a *refusal*, not a
build) and impossible for a synthesis-first competitor to match.

## Confidence & source

- **Confidence:** 0.90 — near-definitional. Synthesis = rewrite; verbatim = no-rewrite; the two
  cannot co-exist in one engine. Highest-conviction of the three signals.
- **Source:** category architecture analysis this session against Voices' conservation law.
- **Related intents:** `preservation_invariant` envelope contract (SPEC-DRAFT); positioning DDR.
