---
title: "Open development — signals, decisions, architecture all public"
id: DEC-INTENT-003
type: decision-atom
created: 2026-03-28
date_inferred: false
scope: Core/frameworks/intent — development transparency
status: ratified
ratified_at: 2026-03-28
ratified_by: "brien (Cowork session 2026-03-28; 4-gate pass: reversible / local / precedent / no info gap)"
gate_check:
  reversible: pass
  local: pass
  precedent: pass
  info_gap: pass
upstream_control_path: "Core/frameworks/intent/CLAUDE.md §Key Decisions #3; public GitHub repo theparlor/intent"
catch_mechanism: "Repo is public; any private/confidential drift would require explicit access change"
pipeline_survival: "GitHub repo visibility setting; .intent/ directory committed publicly"
source: "Cowork session 2026-03-28"
---

# Decision: Open development — signals, decisions, architecture all public

> Ratified 2026-03-28. All 4 autonomy-grant gates pass.

## Context

Intent is its own best dogfood case. The observe layer needs to be observable. Keeping development private would contradict the methodology's core principle and miss the thought leadership opportunity of transparent practice.

## Decision

Develop Intent in the open. Signals, decisions, architecture, and the `.intent/` directory are all public. Dogfood the observe layer by making Intent's own development observable.

## Scope

Governs the Intent framework repo (theparlor/intent). Does not govern engagement-specific client work in Work/ directories.

## Alternatives Not Taken

| Alternative | Why not chosen | Reversibility if revisited |
|-------------|----------------|---------------------------|
| Private repo | Contradicts transparency principle; loses GTM leverage | L4 — change repo visibility |
| Partial public (methodology only, not signals) | Inconsistent with dogfooding; weaker thought leadership | L4 |

## Reversibility

L4 — repo visibility is a GitHub setting. Any public commit history cannot be fully retracted, so this is irreversible for existing commits in practice.

## Ratification Action

Repo theparlor/intent is public. `.intent/` directory committed and visible. All signal files use public-safe content (no client confidentials).
