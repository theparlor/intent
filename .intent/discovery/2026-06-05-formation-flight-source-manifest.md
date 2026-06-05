---
title: Formation Flight — Source Manifest & Reconciliation
type: analysis
maturity: active
confidentiality: internal
reusability: specific
created: 2026-06-05
updated: 2026-06-05
purpose: Grounding record for the Formation Flight build — what already existed in the Intent repo, the deltas vs the repo-blind build prompt, and how each was reconciled.
related:
  - spec/SPEC-INTENT-FORMATION-FLIGHT-001.md
  - spec/autonomy-flight-model-v1-DRAFT.md
  - spec/autonomy-gate-surface-matrix-v0-DRAFT.md
  - .intent/plans/2026-06-05-formation-flight-plan.md
---

# Formation Flight — Source Manifest

> Grounding for the build. A repo-blind prior session drafted a build prompt assuming several Intent
> primitives existed under invented names. This manifest records what is actually in the repo (with
> citations), the deltas, and the reconciliation. **Extend, never duplicate.**

## What was inventoried (file:line)

| Primitive | Location | Shape |
|---|---|---|
| Autonomy Flight Model (single-aircraft) | `spec/autonomy-flight-model-v1-DRAFT.md` | Forces W/T/L/D; λ "coefficient of bravery" (§2); crash modes stall vs overspeed (§3); estimate-decide split (§4); Cockpit/Tower (§7) |
| Surface matrix | `spec/autonomy-gate-surface-matrix-v0-DRAFT.md` | surface × mode → autonomy floor + deterministic hook precondition; §3 Brien actor overrides; ratifies-together with flight model |
| Trust → autonomy | `servers/models.py:87,110` | `compute_trust()`, `trust_to_autonomy()` (L0<.2, L1<.4, L2<.6, L3<.85, L4≥.85) |
| Contract (the seam) | `spec/work-ontology.md` L4 + `servers/models.py:60,291` | `ContractType.INTERFACE`, `ContractStatus`, `contract_frontmatter()` w/ `verification_command`; `contract.verified`/`contract.failed` events |
| `audit_chain` (graph drift) | `servers/knowledge.py:1348` | Observe-phase verb; returns `{color(green/amber/red), counts:{unspecced_signals,uncontracted_specs,unverified_contracts,orphans}, findings:[{kind,id,path}]}`; DEC-012 |
| `get_core` (standing core) | `servers/knowledge.py:1259` | bounded normative-first context slice |
| Two-plane model | `servers/models.py:5-9` | Ephemeral (Signal→Intent→Atom→Event→Trace) vs Persistent (Spec, Contract = bridge) |
| λ per product | `tools/extracted-corpus/lambda-settings-by-product-v1.yaml` | per-product `default`/`fit_target` fit from closure-rate evidence; per-surface + per-actor overrides |
| Event/lineage | `servers/models.py:178,198` | `make_event()` (trace_id/span_id/parent_id) + `TraceContext` |
| Parallel-dev playbook | `playbooks/idd-build-pattern.md` | Shape 2 (parallel worktrees), F13 (dispatch-prompt injection), Layer-5 hook `autonomy-grant-dispatch-prompt-check.sh` |
| Drag guard | `hooks/pre-commit-drag-guard.sh`, `hooks/lexical-layer-freeze.yaml` | physically blocks commits that grow `hooks/`; lexical layer measured 95.8% overhead |
| Product roles (flight model spec) | flight-model `related:` | Loom=Tower, Topography=Cockpit, Witness=recorder/Lift, Voices=variance/adversarial-verify |

## Deltas vs the build prompt (repo-blind assumptions)

| Prompt assumed | Reality | Reconciliation |
|---|---|---|
| `audit_gaps` FastMCP tool | does NOT exist by that name; **`audit_chain`** is the real, BUILT verb (DEC-012) | coherence gate **wraps** `audit_chain` (Stage B); the name `audit_gaps` appears once, in `SPEC-substrate-exposure-envelope-extensions-DRAFT.md:68`, as the *rejected* generic term mapped TO `audit_chain` |
| "brief envelope" exists | TWO envelopes exist (flight-envelope, substrate-exposure-envelope) — **neither is a dispatch payload** | new **Mission Brief** type, dispatch-direction (orchestrator→agent), sibling to both |
| `interface_contract` is new | **Contract** = Work-Ontology L4, already typed | Mission Brief `interface_contract` **references** a CON id; does not redefine |
| `λ`, L0–L4 are new knobs | both exist | reference by composition (per-product `.intent/INTENT.md` λ; `trust_to_autonomy`) |
| swarm governance is greenfield | `autonomy-gate-surface-matrix-v0-DRAFT.md` exists | governance matrix = **sibling spec** extending it |
| parallel dev is greenfield | `idd-build-pattern.md` Shape 2 already solves physical collision | add **Shape 4: Formation** (semantic layer) — edit, not duplicate |

## The load-bearing finding (the reason this build matters)

**Wrapping `audit_chain` alone is a false-green gate.** Verified at `servers/knowledge.py:1402-1430`:
`audit_chain` reads only persisted `.intent` artifacts and checks *graph topology* — link existence, the
presence of a `verified:` flag, inbound references. It **structurally cannot** see the three
semantic-collision types:

1. **Vocabulary drift** — it checks links exist, never term consistency across two agents' bodies. Agent A
   "sortie" + Agent B "mission" passes green.
2. **Contract breach** — it checks a Contract is *referenced and marked verified*; it never runs the
   `verification_command` nor compares output to the Contract's assertions. A breached-but-marked contract
   passes green.
3. **Non-goal violation** — there is no `non_goals` concept anywhere in the persisted graph. Invisible.

Therefore the coherence gate is **two-stage**: Stage A (brief-conformance, in-orchestrator, pre-persistence:
run `verification_command`; diff output vs `invariants`/`non_goals`/`reference_frame`) + Stage B (wrap
`audit_chain` for topology + the drift-clean stop predicate). Shipping only the wrapper would build a gate
that certifies collisions as clean — worse than no gate.

## Hard constraint that shapes the design

`pre-commit-drag-guard.sh` blocks any commit that grows `hooks/` past baseline. The lexical Stop-hook layer
measured **1,463 runs / 4.17% block rate = 95.8% overhead**. → Stage A runs as an **in-orchestrator template
check, NOT a new enforced hook.** All formation machinery is opt-in and **invocation-scoped** (ON-trigger:
≥2 parallel agents declaring the same parent intent). The solo/N=1 path imports none of it → zero per-turn cost.

## Reviews

Two independent Plan-agent reviews (architecture-coherence, over-engineering/solo-tax) recorded at
`~/.claude/plans/tranquil-leaping-barto*.md`. Convergent verdicts: substrate ~half-built; the false-green
finding above is the critical correction; "Brief Envelope"/"Flight Brief"/"Dispatch" are all overloaded
(→ **Mission Brief**, grep-clean); governance matrix = sibling not inline edit; JSON Schema = single source
of truth to avoid triple-definition drift.
