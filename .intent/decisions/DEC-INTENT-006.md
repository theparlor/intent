---
title: "Specs as contracts, not stories"
id: DEC-INTENT-006
type: decision-atom
created: 2026-03-28
date_inferred: false
scope: Core/frameworks/intent — spec format and agent-readiness requirement
status: ratified
ratified_at: 2026-03-28
ratified_by: "brien (Cowork session 2026-03-28; 4-gate pass: reversible / local / precedent / no info gap)"
gate_check:
  reversible: pass
  local: pass
  precedent: pass
  info_gap: pass
upstream_control_path: "Core/frameworks/intent/CLAUDE.md §Key Decisions #6; spec/spec-shaping-protocol.md; knowledge-engine/spec/contracts.md"
catch_mechanism: "Spec template enforces verifiable assertions; contracts.md lists 10 structural constraints; lint detects prose-only specs"
pipeline_survival: "Spec template is the artifact surface; contracts enforced in every session"
source: "Cowork session 2026-03-28"
---

# Decision: Specs as contracts, not stories

> Ratified 2026-03-28. All 4 autonomy-grant gates pass.

## Context

Traditional Agile stories are prose descriptions of desired outcomes written for human interpretation. AI agents need verifiable assertions — boolean-checkable acceptance criteria, not narrative. The spec is the handoff surface between human intent and agent execution.

## Decision

Specs are contracts with verifiable assertions, not prose user stories. Agents need boolean-checkable criteria. The spec-shaping protocol uses four-persona interrogation to produce contract-quality specs before any agent executes.

## Scope

Governs all spec artifacts in `.intent/specs/`. Does not govern signal files (which are intentionally lightweight prose) or intent files (which are intermediate).

## Alternatives Not Taken

| Alternative | Why not chosen | Reversibility if revisited |
|-------------|----------------|---------------------------|
| Prose user stories | Not agent-readable without additional interpretation step | L4 |
| BDD / Gherkin | Overly rigid syntax; good for test automation, not system design | L4 |
| Free-form markdown | No verifiability; agents fabricate completion | L3 |

## Reversibility

L4 — format change is a template update + migration of existing specs.

## Ratification Action

Spec template enforces verifiable assertions. `knowledge-engine/spec/contracts.md` defines 10 structural contracts. Spec-shaping protocol (`spec/spec-shaping-protocol.md`) uses four-persona self-prompting to produce contract-quality specs.
