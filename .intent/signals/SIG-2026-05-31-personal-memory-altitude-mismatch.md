---
id: SIG-2026-05-31-personal-memory-altitude-mismatch
type: architectural-positioning
status: active
date: 2026-05-31
confidence: 0.86
source: "category analysis (2026-05-31 session) read against Brien's altitude framework (coherence-engineering/DEFINITION.md, 4 altitudes) and the prompt→context→intent progression"
exposure: public
strategic_value: 0.84
blast_radius: low
irreversibility: 0.0
autonomy_level: L4
provenance_note: >
  Reaffirms a PRIOR analytical pattern. The "altitude mismatch" frame was already run once
  against Glean (coherence-engineering/handoff/2026-04-16-glean-vs-intent-phase1/). This
  signal applies the same validated lens to the personal-memory category — a repeat of an
  existing analysis, not a new thesis.
related:
  - SIG-2026-05-31-personal-synthesis-layer-commoditizing
  - SIG-2026-05-31-verbatim-passthrough-differentiator
proposed_edges:   # SURFACED for review — NOT wired into any decision log (see session response)
  - "extends → coherence-engineering/DEFINITION.md (four-altitude framework)"
  - "extends → coherence-engineering/handoff/2026-04-16-glean-vs-intent-phase1/ (the original altitude-mismatch analysis — 'Glean redux')"
  - "validates → DEC-009 (two observabilities) + Intent KE Decision #14 (two products: methodology vs engine)"
  - "validates → project_intent_engineering_positioning (prompt→context→intent; L2 = Coherence, L3 = Intent)"
  - "candidate decision atom → DEC-CE / DDR placing personal-memory layers one altitude below Intent"
---

# Personal memory layers sit one altitude below Intent (Glean redux)

> **Framing.** Same analytical lens we already pointed at Glean in April, pointed now at the
> personal-memory category. The conclusion is the same shape, which is why confidence is high:
> this is a **repeat of a validated analysis**, not a fresh claim.

## What I noticed

The commoditizing personal-synthesis category ([[SIG-2026-05-31-personal-synthesis-layer-commoditizing]])
operates at the **memory-layer altitude**. Measured against our own altitude framework, the
category is structurally missing everything that lives above Layer 1:

| Capability | Personal memory layer (LYKN / Mem0 / Supermemory / Zep) | Intent |
|---|---|---|
| Spec/Contract coupling **across teams** | — none | core (7-level work ontology) |
| Two-plane separation (ingest vs distribute as governed planes) | — none | substrate-exposure Phase 1/Phase 2 |
| Trust-gated autonomy (L0–L4) | — none | signal-trust-framework + flight model |
| Decision records (DDRs) as first-class state | — none | `.intent/decisions/` + WS-DDR chain |

They are a **memory layer**, not an **operating model**.

## Why this is "Glean redux"

In April we ran exactly this analysis against Glean (enterprise search) and concluded Glean
sits one altitude below Intent — it answers "what do we know" but never "what do we do about
it, who decides, and how does the decision bind across teams." (`coherence-engineering/handoff/2026-04-16-glean-vs-intent-phase1/`.)

The personal-memory category is the **personal-scale instance of the same mismatch.** Glean
was the enterprise-search version; LYKN/Mem0/Supermemory are the personal-context version.
The altitude gap is identical. That a second, independent category lands at the same altitude
gap *raises* confidence in the placement — it is now corroborated across two scales.

## Why it matters now

This is the structural complement to S1's strategic payload. S1 says "the memory engine is
commoditizing." This signal says **why that is safe for us**: we do not compete at the memory
altitude. The prompt→context→intent progression places the category at Layer 1–2 (context),
while Coherence Engineering (L2) and Intent (L3) operate above it.

**The altitude gap IS the moat.** A memory layer can be cloned in a quarter (S1 proves it). An
operating model — loop + ontology + trust-gated autonomy + binding decision records — is the
thing the category structurally does not reach for.

## What needs to happen (proposed, not executed)

- Record the altitude placement as a citable decision (CE decision atom or DDR) so external
  articulation can lean on it without re-deriving.
- When the spine's interface (the `intent-knowledge` envelope) is refined, do it at the
  *operating-model* altitude — typed supply policy, governed planes — not as a better
  key-value store. (See [[SIG-2026-05-31-personal-synthesis-layer-commoditizing]] → SPEC-DRAFT.)

## Confidence & source

- **Confidence:** 0.86 — an analytical-judgment claim, corroborated by the second independent
  instance (Glean → personal-memory) landing at the same altitude.
- **Source:** category analysis this session against `coherence-engineering/DEFINITION.md`
  (four altitudes) and the prompt→context→intent positioning.
- **Related intents:** positioning DDR (altitude placement); spine-interface refinement at the
  operating-model altitude.
