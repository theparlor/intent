---
id: INT-015
title: "Define the Productivity OS Layer Model — L1 through L6"
status: proposed
proposed_by: brien
proposed_date: 2026-04-12T10:30:00Z
signals: [SIG-035]
specs: [SPEC-productivity-os-layers]
owner: brien
priority: now
product: cross-cutting
---
# Define the Productivity OS Layer Model — L1 through L6

## Problem

Intent's three-layer architecture (Knowledge Base → Transformation OS → Software) is layer-agnostic. It doesn't prescribe how the architecture changes across organizational scales. Brien is building L1 tools (personas, Knowledge Farm, Cowork plugin) and L6 tools (Intent methodology, site, consulting deliverables) but the layers between are implicit.

This creates three concrete problems:

1. **Fragmented product narrative.** The persona library, Knowledge Farm, Cowork plugin, and auto-memory are all L1 personal productivity tools. The Intent methodology, four-persona spec shaping, and signal trust framework are L3-L4 team tools. The Transformation Operating System and Intent site are L6 enterprise tools. These are the same architecture at different altitudes, but nothing connects them into a coherent story.

2. **Invisible gaps at L2 and L5.** Independent builders (freelancers, open source maintainers, solo consultants who collaborate) don't have a model. Department-level product organizations don't have a model. These are real buyer segments with no explicit Intent offering.

3. **Undefined cross-layer mechanics.** How does a personal observation (L1) become a team signal (L3)? How does enterprise governance (L6) constrain team autonomy (L3)? How does knowledge flow laterally between teams (L3→L4→L3)? The federation spec addresses some of this, but only for knowledge — not for signals, governance, or observability.

## Desired Outcome

Brien has a comprehensive, consulting-deliverable specification that:

1. Defines six distinct layers (L1 Personal through L6 Enterprise) with clear scope, knowledge architecture, loop cadence, trust model, persona usage, observability, and tooling for each
2. Maps cross-layer data flows: signals UP, governance DOWN, knowledge LATERALLY
3. Shows how Intent's existing architecture (three-layer, loop, trust, federation, Knowledge Engine) manifests at every layer
4. Identifies L2 and L5 as explicit gaps with enough definition to begin designing for them
5. Connects Brien's personal productivity work (L1) to the enterprise transformation story (L6) through a continuous, coherent model
6. Serves as a consulting asset — clients can see themselves at a specific layer and understand the path to adjacent layers

## Evidence

- SIG-035: Observation that Intent addresses L1 and L3-L6 but lacks a formal model connecting them
- SIG-030: Cowork plugin work is building L1 tooling without acknowledging the layer
- INT-005: Unified persona system operates primarily at L1 (personal invocation) and L3 (team spec shaping) — the layering model explains why
- Federation spec: Already addresses L4 knowledge flows but not the full altitude model
- Team Topologies (Pais/Skelton): Provides the organizational precedent for altitude-aware operating models
- Dex Horthy's harness engineering: External validation of L1-L2 as a real and growing market

## Constraints

- Must be consistent with existing three-layer architecture (KB → TOS → Software)
- Must be consistent with existing trust/autonomy model (L0-L4 autonomy levels)
- Must be consistent with federation spec (inherit down, promote up, never leak sideways)
- Must not introduce new concepts where existing ones (loop, trust, personas, Knowledge Engine) already apply — the model should show how existing concepts vary by altitude, not replace them
- Must be usable as a consulting deliverable — professional, visual, client-ready
- The six layers are a framework, not a rigid hierarchy — some organizations will skip layers, merge layers, or operate primarily at one altitude
