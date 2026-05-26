---
title: "Spec shaping is self-prompting through four personas"
id: DEC-INTENT-019
type: decision-atom
created: 2026-04-06
date_inferred: false
scope: Core/frameworks/intent — spec shaping protocol
status: ratified
ratified_at: 2026-04-06
ratified_by: "brien (2026-04-06; 4-gate pass: reversible / local / precedent / no info gap)"
gate_check:
  reversible: pass
  local: pass
  precedent: pass
  info_gap: pass
upstream_control_path: "Core/frameworks/intent/CLAUDE.md §Key Decisions #19; spec/spec-shaping-protocol.md"
catch_mechanism: "spec-shaping-protocol.md is the canonical execution surface; four-persona interrogation is required before spec is moved to approved"
pipeline_survival: "Protocol file survives session cycles; spec template includes shaping checklist"
source: "2026-04-06"
---

# Decision: Spec shaping is self-prompting through four personas

> Ratified 2026-04-06. All 4 autonomy-grant gates pass.

## Context

Turning an intent into a contract-quality spec requires interrogating the intent from multiple angles: shape, outcome, contract quality, and agent readiness. Doing this manually is slow and inconsistent. The system should be able to self-prompt through each persona's lens using the knowledge base.

## Decision

Intents become specs through four-persona interrogation: △ Shape (Practitioner-Architect), ◇ Outcome (Product-Minded Leader), ○ Contract (Design-Quality Advocate), ◉ Readiness (AI Agent). Each persona queries the knowledge base. Brien reviews the resulting spec, not the intermediate execution. See `spec/spec-shaping-protocol.md`.

## Scope

Governs the Notice→Spec phase transition. Does not govern Execute phase (which works from approved specs).

## Alternatives Not Taken

| Alternative | Why not chosen | Reversibility if revisited |
|-------------|----------------|---------------------------|
| Single-perspective spec authoring | Misses contract quality, outcome clarity, or agent readiness | L4 |
| Brien-only spec writing | Doesn't scale; Brien is the bottleneck | L3 |
| Template-only (no persona interrogation) | Templates without interrogation produce boilerplate | L4 |

## Reversibility

L4 — protocol is a document + CLI behavior. Can revise persona set or interrogation sequence without structural change.

## Ratification Action

`spec/spec-shaping-protocol.md` defines the four-persona interrogation sequence. Each persona queries the knowledge base. Brien reviews final spec output.
