---
id: RETRO-2026-04-13-approval-gradient-SIG-2
type: signal
category: architecture-gap
severity: medium
source: session-analysis
detected: 2026-04-13
topic: approval-gradient
related:
  - RETRO-2026-04-13-approval-gradient-DEC-3
  - SPEC-APPROVAL-GATE
status: open
---

# Payload Similarity Computation Is an Unstated Dependency

## Signal

The Phase 2 contextual action trust model relies on two factors that require payload comparison:
- **Precedent** (weight 0.35): "Brien approved N similar actions with similar payload"
- **Novelty** (weight 0.20): "Payload divergence from previously approved payloads"

"Similar payload" requires a similarity metric. For text payloads (Slack messages, emails), this could be:
- String edit distance (Levenshtein) — cheap but brittle
- TF-IDF cosine similarity — moderate, no external deps
- Embedding similarity — accurate but requires embedding model

None of these are designed yet. The trust model assumes similarity is computable, but the computation method is unspecified.

## Evidence

- SPEC-APPROVAL-GATE Phase 2 section references "similar payload" and "payload divergence" without defining the metric
- DEC-3 (4-factor model) assigns 0.55 combined weight to factors that depend on payload comparison
- No existing payload comparison infrastructure in Intent or Skills Engine

## Implication

Phase 2 can't ship without a payload similarity decision. This is the primary technical risk in the gradient model. The decision should be made during Phase 1 (while collecting data), not deferred until Phase 2 implementation.

## Recommended Action

Add to Phase 2 pre-work: design payload similarity metric. Start simple (TF-IDF or structural template matching per action type), validate against Phase 1 data, upgrade to embeddings only if simple approaches fail. Capture as a spec-level decision before Phase 2 implementation begins.
