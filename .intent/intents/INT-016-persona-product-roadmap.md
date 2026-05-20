---
id: INT-016
title: "Define the Persona System Product Roadmap — five capabilities from discovery through evals"
status: proposed
proposed_by: brien
proposed_date: 2026-04-12T16:00:00Z
signals: [SIG-036, SIG-037, SIG-038, SIG-039]
specs: [SPEC-001, SPEC-002, SPEC-persona-product-system]
owner: brien
priority: now
product: cross-cutting
---

# Define the Persona System Product Roadmap

## Problem

The persona system is being built as disconnected enrichment tasks — a fetch script here, a synthesis prompt there, a manual review when Brien has time. Four signals (SIG-036 through SIG-039) establish that this is actually a product with five distinct capability areas, each with its own maturity curve and quality model. Without treating it as a product, the interactions between capabilities are accidental and the system can accumulate content but never systematically improve quality.

The existing specs (SPEC-001 entity schema, SPEC-002 intake pipeline) cover the schema and the initial linear pipeline. They are necessary but insufficient. They don't account for:

- How new personas are discovered (beyond Brien saying "add this person")
- How sourcing prioritizes unguarded voice over polished content
- How synthesis separates mechanical fetching from subjective interpretation
- How different pipeline configurations are compared and optimized
- How quality is measured independently of the agent that produced the work

## Desired Outcome

Brien can:

1. **Discovery**: The persona system actively suggests new people worth ingesting, based on citation graphs, dissent patterns, and tangential domain exploration — not just Brien's direct knowledge of who exists.

2. **Sourcing**: Content acquisition follows the "unguarded voice" hierarchy, with new channels (podcast transcription, YouTube captions, academic papers, community content) expanding the source surface beyond web fetch.

3. **Synthesis**: The pipeline separates cheap/mechanical work (fetching, markdown conversion) from expensive/subjective work (voice extraction, reasoning chain identification). Raw markdown is always preserved for re-interpretation.

4. **Bandit Testing**: Pipeline configurations are systematically compared. Different persona types converge on different optimal configurations. The system gets cheaper without getting worse (or gets better at the same cost).

5. **Evals**: Three layers of evaluation (structural, content, fidelity) gate depth score advancement. The system can detect its own failure modes — sycophantic voice synthesis, confabulated reasoning chains, vocabulary contamination, depth score inflation.

## Evidence

- SIG-036: Multi-model adversarial synthesis eliminates sycophancy — the quality hypothesis
- SIG-037: Five capabilities identified as product framing — the architectural hypothesis
- SIG-038: Eval-driven development is the missing governance layer — the quality gate hypothesis
- SIG-039: Bandit testing optimizes pipeline configurations — the optimization hypothesis

## Constraints

- Must build on existing SPEC-001 (entity schema) and SPEC-002 (intake pipeline) — not replace them
- Must work with file-native storage in `Core/personas/` (no database dependency)
- Must support the three-layer architecture (knowledge base / transformation OS / software)
- Eval infrastructure must produce machine-readable reports that feed bandit reward signals
- Discovery autonomy must follow the L0→L3 progression in the trust framework
- Bandit testing involves real API cost — explore/exploit tradeoffs need Brien's cost ceiling input
