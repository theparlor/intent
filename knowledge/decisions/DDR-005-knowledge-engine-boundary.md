---
title: Separate Intent (methodology) from Knowledge Engine (product) from Knowledge Farm (instance)
id: DDR-005
type: decision
created: 2026-04-06
updated: 2026-04-06
depth_score: 2
depth_signals:
  file_size_kb: 2.3
  content_chars: 2116
  entity_count: 0
  slide_count: 0
  sheet_count: 0
  topic_count: 0
  has_summary: 0
vocab_density: 1.42
status: accepted
confidence: 0.90
origin: human
persona: PER-001
journey_stage: JRN-001#compile-understanding
---
# DDR: Intent / Knowledge Engine / Knowledge Farm Boundary

## Context

During the schema-first implementation of Layer 1, Brien identified that the implementation had collapsed three distinct things:
1. Intent (the methodology — how teams build products)
2. The Knowledge Engine (the product — the compiled knowledge base pattern)
3. Brien's Knowledge Farm (a specific instance — Brien's consulting practice knowledge)

The conflation manifested as: Knowledge Engine specs living in Intent's spec/ directory, Intent's own raw/+knowledge/ directories being treated as part of the methodology rather than dogfooding of a separate product.

Additional insight: Brien's Knowledge Farm feeds Intent not because of the architecture but because his knowledge domain (product strategy, consulting) overlaps with Intent's domain. This is coincidental, not structural.

## Decision

Establish three clear levels with explicit boundaries:

- **Intent** prescribes "you need compiled domain knowledge" (the what)
- **Knowledge Engine** provides the pattern for compiling it (the how)
- **Knowledge Farm** is a specific deployment for a specific domain (the where)

The Knowledge Engine is a separable product that can be used with or without Intent. Intent benefits from but does not require the Knowledge Engine.

## Consequences

**Positive:**
- Clear separation enables the Knowledge Engine to serve non-Intent use cases
- Brien's Knowledge Farm can grow without being constrained by Intent's scope
- The coincidence clause is explicit — Brien's farm feeds Intent by domain overlap, not architecture

**Negative:**
- More conceptual complexity to maintain
- File layout needs to reflect the boundary (or at least document it clearly)

## Validation Criteria

- [ ] Someone could use the Knowledge Engine without adopting Intent's methodology
- [ ] Someone could use Intent's methodology without the Knowledge Engine
- [ ] Brien's Knowledge Farm about product strategy feeds Intent; a hypothetical farm about manufacturing does not
