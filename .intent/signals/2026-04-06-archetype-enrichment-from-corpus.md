---
id: SIG-039
timestamp: 2026-04-06T18:00:00Z
source: conversation
confidence: 0.85
trust: 0.6
autonomy_level: L2
status: resolved
upstream_control_path: "Core/frameworks/intent/spec/SPEC-003-intent-framework-entity-extensions.md CON-010 + Core/products/cast/farm/archetypes/*/source-humans.yaml"
catch_mechanism: "contribution non-regression contract (before/after diff, set-empty verification) governs archetype enrichment; the REDACT step this signal proposed is superseded by the no-preemptive-redaction policy, not built"
verification_command: "grep -n CON-010 /Users/brien/Workspaces/Core/frameworks/intent/spec/SPEC-003-intent-framework-entity-extensions.md"
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

## Triage, 2026-07-08

Disposition: control exists now, mostly, with one piece overtaken by later policy. The contribution-declaration and archetype-synthesis architecture this signal proposed is built: Cast's farm/archetypes/[slug]/source-humans.yaml tracks named-human contributors, and SPEC-003's CON-010 (Contribution Non-Regression) formalizes the non-destructive-merge contract this signal asked for. The one piece not built as proposed is the explicit REDACT (PII-removal) pipeline stage: that premise is superseded by memory/feedback_no_preemptive_redaction.md (ratified 2026-06-10), which rejects automated redaction pipelines in favor of a per-recipient human decision at share time. Same overtaking logic as this pass's disposition on SIG-029 below.
