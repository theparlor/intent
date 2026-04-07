---
id: SIG-039
timestamp: 2026-04-06T18:00:00Z
source: conversation
confidence: 0.85
trust: 0.6
autonomy_level: L2
status: active
cluster: methodology-adoption
author: brien
related_intents: []
referenced_by: []
parent_signal: SIG-035
---
# Named-human corpus aggregation produces grounded archetypes far richer than store-bought

## Observation

Brien identified that if we ingest 15 real named-human CEOs, we can redact and aggregate their corpus to create archetypes that are statistically grounded rather than stereotypical. The pipeline: corpus → REDACT (PII, proprietary) → TAG (role, industry, themes, stances) → AGGREGATE (cluster by archetype dimensions) → SYNTHESIZE (grounded composite).

A grounded archetype derived from real corpus isn't "a CEO cares about ROI." It's: "Based on 15 Fortune 50 manufacturing CEOs, they spend 40% of public communication on supply chain resilience, use concrete dollar figures 3x more than percentages, and express visible frustration when presented with timeline-free transformation narratives."

This creates a compounding system: each new named-human makes every archetype it contributes to richer. And lensing on top of grounded archetypes isn't fiction — it's emphasis on real signals.

## Implication

The persona system must support:
1. Named humans with stored corpus (raw material, refreshable)
2. Contribution declarations (which archetypes, along which dimensions)
3. Redaction pipeline (PII removal before aggregation)
4. Archetype synthesis (statistical grounding + preserved outlier signal)
5. Lens application (emphasis weighting on real corpus-derived patterns)

Every model at every level must provide standalone value AND contribute upward to the next level.

## Design Constraint

- Redaction must be thorough enough for cross-entity aggregation (no PII leakage between named humans)
- Archetypes must track which named-humans contributed (for provenance and reprocessing)
- Adding a new named-human must be non-destructive to existing archetype content
- Lenses operate on substance, not index — they shift emphasis, not classification
