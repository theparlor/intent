---
title: Formation Flight build plan
type: plan
status: executing
created: 2026-06-05
updated: 2026-06-05
source_spec: spec/SPEC-INTENT-FORMATION-FLIGHT-001.md
related_decision: DEC-014
approved_by: brien
approved_at: 2026-06-05
origin: ~/.claude/plans/tranquil-leaping-barto.md (Claude Code plan-mode artifact; persisted here per spec/plan-artifact-convention.md)
purpose: Build + exercise the Formation Flight layer (coherent non-colliding parallel development).
---

# Plan — Intent: Formation Flight (Coherent Non-Colliding Parallel Development)

## Context

The prior (repo-blind) session produced a build prompt to extend **Intent** for parallel multi-agent
development. Grounding in the real repo (`Core/frameworks/intent/`, its own git repo) corrected its
core assumptions: **most of what it proposed already exists**, and the genuinely new work is the
*semantic-coherence* layer on top.

**The reframe:** Intent already has a single-aircraft **Autonomy Flight Model** (W/T/L/D forces, λ
coefficient of bravery, stall-vs-overspeed crash modes). This build adds **Formation Flight** — the
multi-aircraft layer: many isolated agents flying one intent without colliding. Two collision types:
- **Physical** (file/git): already solved by worktree isolation — `playbooks/idd-build-pattern.md` Shape 2.
- **Semantic** (vocabulary drift / contract breach / non-goal violation across isolated agents):
  *not* solved by isolation — *amplified* by it. **This is the new work.**

**Objective (Brien):** go all the way and build it runnable, so we can **exercise it and find where it
can't stand up.** Every artifact must execute, not just sit as spec.

## Source manifest — what exists vs. what's new (the deltas)

| Build-prompt assumption | Reality (file:line) | Move |
|---|---|---|
| `audit_gaps` tool | **`audit_chain`** BUILT — `servers/knowledge.py:1348`, DEC-012; returns `{color, counts:{unspecced_signals,uncontracted_specs,unverified_contracts,orphans}, findings:[{kind,id,path}]}` | **wrap** + **consume** |
| "brief envelope" | TWO envelopes already exist (flight-envelope `autonomy-flight-model-v1-DRAFT.md §4`; substrate-exposure-envelope `SPEC-substrate-exposure-envelope-extensions-DRAFT.md`). Neither is a dispatch payload. | **new sibling type** (Mission Brief) |
| `interface_contract` | **Contract** = Work-Ontology L4 (`spec/work-ontology.md`) + typed `ContractType.INTERFACE`/`contract_frontmatter()`/`verification_command` (`servers/models.py:60,291`); `contract.verified/failed` events | **reuse** |
| `λ` / L0–L4 trust gates | flight model + `tools/extracted-corpus/lambda-settings-by-product-v1.yaml` + `trust_to_autonomy()` (`models.py:110`) | **reuse by reference** |
| swarm governance matrix | `spec/autonomy-gate-surface-matrix-v0-DRAFT.md` | **extend (sibling spec)** |
| parallel-dev playbook | `playbooks/idd-build-pattern.md` (Shape 2 worktrees; F13 dispatch-injection; Layer-5 hook) | **edit (add Shape 4)** |
| formation lead / telemetry | **Loom**=Tower(lead), **Topography**=Cockpit, **Witness**=recorder/Lift, **Voices**=variance/adversarial-verify (mapped in flight-model spec) | **reuse** |
| lineage | `make_event()` + `TraceContext` (`models.py:178,198`) trace_id/span_id/parent_id | **reuse** |

Strategic anchor: **DEC-013** — "differentiation is the spine + altitude, not the engine." Formation
Flight *is* governed parallel autonomy = that spine. Latest decision DEC-013 → new = **DEC-014**.

## The load-bearing correction (from two parallel design reviews)

Wrapping `audit_chain` **alone is a false-green gate.** `audit_chain` audits *persisted graph topology*
(is the chain wired?) — it structurally cannot see the three semantic-collision types (it checks link
existence not term consistency; checks the `verified:` flag exists but never runs `verification_command`;
has no `non_goals` concept at all). So the coherence gate is **two-stage**:

- **Stage A — brief-conformance** (NEW; runs *in the orchestrator at synthesis time*, pre-persistence,
  per-agent): run each agent's Contract `verification_command`; diff its output against its Mission
  Brief `invariants` / `non_goals`; term-consistency diff against `reference_frame` glossary; preserve
  contradictions as two findings (Voices conservation law, never merge).
- **Stage B — chain audit** (REUSE): wrap `audit_chain` on the merged scope → topology drift +
  the **drift-clean stop predicate** (done = `color==green` AND zero new Stage-A findings across a pass).

**Hard constraint:** `hooks/pre-commit-drag-guard.sh` physically blocks any commit that grows `hooks/`
past baseline (the lexical hook layer measured **95.8% overhead**). → **Stage A is a TEMPLATE / in-orchestrator
check, NOT a new enforced hook.** Everything formation is opt-in, invocation-scoped.

## Naming

**Mission Brief** (grep-clean; your set). "Dispatch"/"Flight"/"Envelope" all overloaded. DEC-014 will
note **"Clearance"** as the precise civil-ATC alternative (Tower→aircraft authorization-with-constraints)
— term is find/replace-cheap pre-ratification.

## Solo zero-overhead — the ON-trigger

Machinery is **invocation-scoped, not session-scoped**: it lives only in the orchestrator script you run
when you deliberately fan out. **ON-trigger = dispatch of ≥2 parallel subagents declaring the same parent
intent id.** N=1 never imports it → literally zero per-turn cost. No "coherence-critical" auto-classifier
(that drift is what killed the lexical layer).

## Build (full, pipeline-sequenced)

**New specs** (`spec/`, follow `SPEC_TEMPLATE.md` Intent→Shape→Contract, id `SPEC-INTENT-<TOPIC>-NNN`):
1. `spec/SPEC-INTENT-FORMATION-FLIGHT-001.md` — umbrella: two collision types, multi-aircraft extension
   of the flight model, new crash modes (mid-air-collision, formation-breakup), Cockpit/Tower/Witness/Voices
   mapping, ON-trigger, sibling set, provenance. Declares the ratify-together set.
2. `spec/SPEC-INTENT-MISSION-BRIEF-001.md` — typed dispatch payload. **New fields** (no existing carrier):
   `reference_frame` (glossary), `invariants`, `non_goals`, `drift_markers`. **Reference fields** (compose,
   don't copy): `interface_contract`→CON id, `lambda`/`trust_gate`→product `.intent/INTENT.md` λ,
   `verification_rubric`→Contract `verification_command`, `lineage`→`make_event`/`TraceContext`.
3. `spec/SPEC-INTENT-SEAM-DECOMPOSITION-001.md` — fan out on Contract seams not files (~30% new + pointer
   to idd Shape 2 + federation "never leak sideways" = separation minima). Cite Beer VSM / Alexander.
4. `spec/SPEC-INTENT-COHERENCE-GATE-001.md` — the two-stage barrier above; explicitly template/in-orchestrator;
   routes findings through Witness.
5. `spec/SPEC-INTENT-FORMATION-GOVERNANCE-001.md` — **sibling** to surface-matrix (WS-DDR-025): L0–L4 × λ →
   (model, isolation, privilege, verification intensity). Quarantine = L0 input gate (cite Saltzer–Schroeder
   1975); reference the matrix's existing cross-human L0 row, don't restate.

**Runnable kit** (`formation/` — new dir; the exercisable core):
6. `formation/mission-brief.schema.json` — **JSON Schema = single source of truth**, usable directly as
   Workflow `agent(prompt, {schema})`.
7. `formation/coherence-gate.workflow.js` — two-stage gate as Workflow-DSL JS (Stage A `parallel` of
   verification-command + brief-conformance agents; Stage B `audit_chain` wrap + drift-clean predicate).
8. `formation/formation-flight.workflow.js` — full reference harness: fan-out-on-seams → coherence-gate →
   loop-until-drift-clean. Marked TEMPLATE. **This is what we run to exercise.**
9. `formation/formation.py` + test — thin `MissionBrief` dataclass (house style, `models.py` idiom) **validated
   against the JSON Schema by a test** (avoids triple-definition drift). Run via `servers/.venv`.
10. `formation/README.md` — how to run the harness + the ON-trigger.

**Edits** (extend, not duplicate):
11. `playbooks/idd-build-pattern.md` — add **Shape 4: Formation** (under Composition Shapes), an Anti-Pattern
    "semantic drift across isolated agents" (mitigation = coherence gate, noting it's a synthesis-time check
    not a hook), and a Hook-Registry note.
12. `spec/autonomy-gate-surface-matrix-v0-DRAFT.md` + `spec/autonomy-flight-model-v1-DRAFT.md` — one-line
    pointers adding formation specs to the ratify-together sibling set.

**Records / dogfood** (lean):
13. `spec/decision-log.md` — **DEC-014** (extension; two-stage/false-green finding; Mission Brief as dispatch-plane
    type; naming + Clearance note; template-not-hook constraint; sibling set; provenance).
14. `.intent/discovery/2026-06-05-formation-flight-source-manifest.md` (persist the manifest above) +
    `.intent/signals/` Notice signal + a reusable signal capturing the **false-green** insight.
15. `.intent/plans/2026-06-05-formation-flight-plan.md` — persist this plan (plan-artifact-convention).

## Provenance (cited as prior art, never claimed)

MapReduce (fan-out/synthesize) · Argyris double-loop + separation-of-duties (adversarial verify; already
RAT-002) · fixpoint iteration (loop-until-drift-clean) · Elo/pairwise (tournament) · Saltzer–Schroeder 1975
taint/privilege-separation (quarantine) · Beer VSM + Alexander bounded centers (seam decomposition). **Intent's
defensible contribution = the governance layer**: the typed Mission Brief that survives isolation + the two-stage
coherence gate that closes the Observe loop.

## Verification / exercise (the point)

- **Static:** `node --check` each `.workflow.js`; validate `mission-brief.schema.json` (ajv/jsonschema);
  `servers/.venv/bin/python -m pytest formation/` for the dataclass↔schema conformance test.
- **Stage B live:** call `audit_chain` against real `.intent/` and confirm the gate reads its `{color,findings}`.
- **EXERCISE (find where it breaks):** run `formation/formation-flight.workflow.js` via the Workflow tool on a
  real 2–3-seam parallel task; observe Stage A (brief-conformance) and Stage B firing; deliberately seed a
  vocabulary-drift / non-goal violation in one agent and confirm the gate catches it (and that audit_chain alone
  would NOT). Capture every failure mode as a signal → this is the "see where it can't stand up" close.
- **Drag guard:** confirm `pre-commit-drag-guard.sh` passes (no new hooks) before the specific-file commit.

## Guardrails

- Extend-not-duplicate (edits to idd/matrix/flight-model, not parallel structures).
- Template/in-orchestrator, never a new enforced hook (drag-guard).
- JSON Schema is source of truth; dataclass test-pinned to it.
- Solo path zero-overhead (invocation-scoped ON-trigger).
- Formation-flight vocabulary preserved as Intent's owned framing.
