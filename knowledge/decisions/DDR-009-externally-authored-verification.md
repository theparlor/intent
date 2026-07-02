---
title: Externally-Authored Verification — Provider/Model Separation for Coherence Checks
id: DDR-009
type: decision
created: 2026-07-02
updated: 2026-07-02
depth_score: 4
depth_signals:
  file_size_kb: 0
  content_chars: 0
  entity_count: 0
  slide_count: 0
  sheet_count: 0
  topic_count: 0
  has_summary: 0
vocab_density: 0.20
status: proposed
confidence: 0.55
origin: human
amends: spec/SPEC-INTENT-COHERENCE-GATE-001.md (§2 — Stage A / adversarial-Voices escalation)
related:
  - spec/SPEC-INTENT-COHERENCE-GATE-001.md
  - spec/SPEC-INTENT-FORMATION-FLIGHT-001.md
  - spec/SPEC-INTENT-FORMATION-GOVERNANCE-001.md (L0–L4 × λ matrix — the tier this DDR extends)
  - .intent/signals/external/SIG-2026-07-02-mobai-team-pilot-convergence.md (action A — origin of this DDR)
  - knowledge/decisions/DDR-006-12-factor-agent-patterns.md (LLM-as-judge; CON-014)
  - DEC-013 (differentiation = spine + altitude, not engine)
frameworks:
  - separation-of-duties
  - double-loop-learning
---
# DDR-009: Externally-Authored Verification (Provider/Model Separation)

## Context

Intent's whole reason to exist is **coherence** — keeping parallel work true to one shared intent. The
coherence gate (`SPEC-INTENT-COHERENCE-GATE-001`) is the mechanism: at synthesis time it checks each
sortie's output against its Mission Brief. That spec already states the right instinct —
*"Self-report is a signal, not proof"* — and for high-λ seams it escalates from trusting the sortie's
self-check to an **adversarial Voices panel**.

But there is a hole the current spec does not close: **it never constrains what model runs the
verification.** If the same model family both builds the work and judges it — even in a separate context,
even framed as "adversarial" — the judge inherits the builder's training priors, its vocabulary, and its
notion of what "success" looks like. It grades its own homework. Worse than a student marking their own
exam: a student marking it while holding the answer key. The "adversary" and the builder share a brain,
so they share blind spots, and the check certifies exactly the incoherence it was meant to catch — a
higher-order **false-green**.

The sharper generative principle (credited to **Markus**): *always author red/green tests in a different
provider and model from the code, or the test is corrupted by the agent already knowing what success
looks like.* Generalized to Intent: a verification is only trustworthy to the degree it is **independent
of the thing it verifies** — and the strongest available independence is not sharing weights at all.

This is also the operational form of the **two-tension design**: intent↔coherence is only a real tension
if the coherence pole is authored *externally* to the builder. Otherwise the "tension" collapses into
self-consistency theater. Origin: `SIG-2026-07-02-mobai-team-pilot-convergence` action A.

## Decision

Amend the coherence gate so that verification independence is an **explicit, λ-graded requirement**, not
left to chance. Introduce an **independence ladder (I0–I3)** and bind the required rung to the seam's λ /
autonomy / blast-radius via the formation-governance matrix.

### The independence ladder

| Tier | What it is | Independence from builder |
|---|---|---|
| **I0** | Same model, same context — the sortie self-checks. | None. **Forbidden as the sole gate** (this is the existing false-green bug). |
| **I1** | Same model family, **isolated context, blind to the implementation** (sees the Mission Brief, not the reasoning/diff beyond what a check needs). | Context-level only. Shares model priors on "what good looks like." |
| **I2** | **Different model**, possibly same provider. | Architectural — different weights, likely different failure modes. |
| **I3** | **Different provider AND model family**, blind to the implementation. "Vacuum-insulated interrogation." | Strongest available. Two systems that don't share weights, training, or success-priors can't collude. |

### Binding rung to risk (extends `SPEC-INTENT-FORMATION-GOVERNANCE-001`)

- **Low-λ, reversible, local:** I1 is acceptable. Cheap context-separation is proportionate.
- **Mid-λ / design-changing:** I2 minimum.
- **High-λ, low-reversibility, external-surface, or L0-adjacent:** **I3 required.** No drift-clean
  certification without an I3 verifier attached.

### Load-bearing properties

1. **Blindness, not just difference.** The verifier is fed the Mission Brief (intent, invariants,
   `non_goals`, canonical terms, verification rubric) — the shared reference frame — but **not** the
   builder's implementation reasoning or full diff beyond what running the checks requires. Independence
   without blindness leaks the answer key.
2. **The `verification_command` stays king where it exists.** An objective, executable check is already
   model-agnostic and is the strongest signal. This DDR governs the layers where *a model is in the loop*:
   **authoring** the evals/tests and rendering **adversarial judgment**. Open question below on whether
   the `verification_command` itself must be authored cross-provider.
3. **The Mission Brief becomes even more load-bearing** — for a blind external verifier it is the *only*
   channel of intent. An incomplete Brief now surfaces as verifier false-flags, which is a feature: it
   pressures Brief completeness.
4. **Conservation law preserved.** When builder and external verifier disagree, both outputs are kept as
   two findings (Voices `named_dissents`), never silently merged.

### Recorded, not implied

Every gate run records the independence tier actually used (`I0–I3`) and the verifier's provider/model,
emitted to Witness alongside the drift-clean decision. The tier is auditable after the fact.

## Alternatives Considered

| Alternative | Pros | Cons | Why Rejected |
|---|---|---|---|
| **Keep current spec** (self-report + `verification_command` + same-family adversarial panel) | Simplest; one provider; cheapest | If the builder authored the tests, the tests encode the builder's misunderstanding; same-family "adversary" shares blind spots | This is the exact hole — a higher-order false-green |
| **Single-provider context-separation only (I1 everywhere)** | Cheap; one set of credentials; no cross-provider plumbing | Shares model priors on "success"; misses builder-shared blind spots | Kept for **low-λ only**; insufficient for high-λ |
| **Human-only verification of high-λ** | Maximum independence | Doesn't scale; defeats the point of an autonomous coherence gate; Brien becomes the bottleneck the whole system exists to remove | Rejected as the mechanism (humans stay the *gate* via approval, not the *checker*) |
| **Full I3 on everything** | Maximum rigor | Cost, latency, and cross-provider ops on trivial reversible work | Disproportionate; the λ ladder exists to spend rigor where it pays |

## Consequences

**Positive:**
- Verification becomes genuinely independent — catches blind spots the builder's own model shares.
- The intent↔coherence tension becomes a real opposition instead of self-consistency theater.
- Strengthens DEC-013 positioning: the defensible layer is the *governance/coherence contract*, and
  "we verify across independent models" is a claim commodity single-model tooling cannot make.

**Negative:**
- Cost and latency of a second provider on high-λ paths.
- Operational surface: cross-provider orchestration, second set of secrets, and **Mission Brief prompt
  portability** across model families.
- A blind external verifier with an incomplete Brief will false-flag (mitigated by treating that as Brief-
  completeness pressure, but it is real friction early).
- Provider diversity is itself a governance surface (versioning, availability, drift between providers).

**Neutral:**
- Makes the Mission Brief the single most load-bearing artifact in the system.
- Adds `independence_tier` + verifier identity to the gate's event payload.

## Validation Criteria

- [ ] **Proof exercise (mirrors the coherence-gate seeded-drift exercise):** seed a defect that the
      builder's own model *reliably misses* (a shared blind spot). Confirm an **I3** verifier catches it
      while an **I1** self-check passes it green. This is the DDR's ratifying test — it is accepted by
      being *run*, not by being written.
- [ ] Each gate run emits `independence_tier` + verifier provider/model to Witness.
- [ ] A high-λ seam refuses to certify drift-clean when only an I0/I1 verifier is attached.
- [ ] Mission Brief validated as portable to a second provider (a non-Claude model can consume it and run
      the checks without Claude-specific assumptions).

## Open Questions (for readers to pressure-test)

1. **Thresholds.** Exact λ / autonomy / blast-radius cutoffs for I1→I2→I3. Is there a clean λ number, or
   is it surface-dependent (external-comms surfaces jump straight to I3 regardless of λ)?
2. **Which second provider**, and how portable is the Mission Brief across families (OpenAI/Codex is the
   obvious first candidate given single-provider-landscape availability)?
3. **Does the `verification_command` itself** need cross-provider authorship, or only the eval-generation
   and judgment layers? (I.e., is a builder-written objective test still trustworthy because it's
   executable and inspectable, or does authorship contaminate even that?)
4. **Cost ceiling / graceful degradation** — when an I3 provider is unavailable or over budget, does the
   gate block (fail-closed) or downgrade to I2 with a recorded caveat?

## Status & next step

`proposed`. Circulating for read. On acceptance this amends `SPEC-INTENT-COHERENCE-GATE-001` §2 (the
Stage A / high-λ escalation clause gains the independence-ladder requirement) and extends the
`SPEC-INTENT-FORMATION-GOVERNANCE-001` matrix with an `independence_tier` column. Not a restructure DDR
(no N>3 file change authorized yet) — the propagation manifest is deferred to the amendment PR.
</content>
