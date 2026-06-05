---
title: Formation Flight — Coherent Non-Colliding Parallel Development
id: SPEC-INTENT-FORMATION-FLIGHT-001
updated: 2026-06-05
status: draft
scope: framework
plane: bridge
date: 2026-06-05
author: intent framework (formation-flight build, grounded in repo 2026-06-05)
related:
  - spec/autonomy-flight-model-v1-DRAFT.md (parent — the single-aircraft model this extends)
  - spec/autonomy-gate-surface-matrix-v0-DRAFT.md (sibling — surface × mode floors)
  - spec/SPEC-INTENT-MISSION-BRIEF-001.md (mechanism 1 — the dispatch payload)
  - spec/SPEC-INTENT-SEAM-DECOMPOSITION-001.md (mechanism 2 — fan out on seams)
  - spec/SPEC-INTENT-COHERENCE-GATE-001.md (mechanism 3 — two-stage synthesis barrier)
  - spec/SPEC-INTENT-FORMATION-GOVERNANCE-001.md (mechanism 4 — L0–L4 × λ swarm matrix)
  - playbooks/idd-build-pattern.md (Shape 4 — formation; physical-collision substrate)
  - servers/knowledge.py (audit_chain — Stage B engine, :1348)
  - formation/ (runnable kit — schemas + workflow harnesses)
  - Core/products/loom/ (Tower — formation lead), Core/products/topography/ (Cockpit)
  - Core/products/witness/ (recorder/Lift), Core/products/voices/ (variance/adversarial-verify)
sibling_set: [SPEC-INTENT-AUTONOMY-FLIGHT-MODEL-001, SPEC-INTENT-AUTONOMY-SURFACE-MATRIX-001, SPEC-INTENT-FORMATION-FLIGHT-001]
ratify_together: true
source_manifest: .intent/discovery/2026-06-05-formation-flight-source-manifest.md
related_decisions:
  - DEC-014 (formation flight extension — to be written)
  - DEC-013 (differentiation = spine + altitude, not engine — the strategic anchor)
---
# Formation Flight (v1 DRAFT)

> Status: DRAFT. The umbrella spec for coherent, non-colliding parallel multi-agent development.
> It is the **multi-aircraft extension** of `SPEC-INTENT-AUTONOMY-FLIGHT-MODEL-001`. The flight model
> governs one aircraft (one agent, one context). Formation Flight governs many aircraft flying one
> intent at once — built on Claude Code Dynamic Workflows. It ratifies together with the flight model
> and the surface matrix.

## §1 Problem statement

When AI collapses implementation from weeks to hours, the leverage move is to run many agents in
parallel. Claude Code's Dynamic Workflows make this cheap: per-agent context, per-agent worktree,
per-agent model. But that value proposition — **isolation** — is the exact opposite of what Intent
exists to protect: **coherence-to-intent across boundaries**.

So parallelism hands us a sharper problem, not a solution. "Coherent non-colliding parallel
development" is two problems wearing one coat:

| Collision type | What it is | Solved by |
|---|---|---|
| **Physical** | Two agents edit the same file; git conflict; resource contention | **Worktree isolation** — already solved (`idd-build-pattern.md` Shape 2). Free. |
| **Semantic** | Two agents make locally-correct, globally-incoherent decisions: vocabulary drift, silent contract breach, non-goal violation | **Not** solved by isolation — *amplified* by it. Each agent has even less shared context to stay coherent against. **This is the new work.** |

Naive parallelism is just faster incoherence. Isolation severs the coherence channel; each fan-out
agent is, by design, ignorant of the system's intent, vocabulary, and "don't do X" constraints.

## §2 The reframe — formation flight

The flight model describes **one aircraft**: thrust/drag/lift/gravity, λ as coefficient of bravery,
the flight envelope (`L ≥ W` and `T > stall_threshold`), and two crash modes (stall, overspeed).
Parallel development is **formation flight**, which adds three forces the single-aircraft model lacks:

1. **A shared reference frame** every aircraft navigates against. Without a common datum, "straight and
   level" means something different to each pilot. → carried by the Mission Brief `reference_frame`
   (glossary + canonical terms). Sourced cheaply from the substrate-exposure `get_core` standing core.
2. **Separation minima** — no two aircraft may occupy the same airspace (the same **seam**). → enforced
   by seam-based decomposition: each agent owns one frozen **Contract**; two briefs never share a
   `seam_id`. This is Decision 13's *"inherit down, promote up, never leak sideways"* made operational.
3. **A lead whose job is formation integrity, not the mission.** The orchestrator does not fly the
   mission; it holds the formation. → mapped to the **Tower** altitude (§4).

## §3 Two new crash modes

The flight model models stall (too cautious) and overspeed (acts past recovery capacity) — both
single-aircraft. Formation adds two more, *on top* of those:

| Crash | Mechanism | Detector |
|---|---|---|
| **Mid-air collision** | Two aircraft occupy the same airspace — same file (physical) or same contract (semantic). | worktree isolation (physical) + `touched_paths` intersection + `contract_changed` (semantic), coherence-gate Stage A |
| **Formation breakup** | The formation loses its shared frame — agents drift apart in vocabulary, assumptions, scope. Each is locally airworthy; the formation is incoherent. | coherence-gate Stage A (invariants / non_goals / glossary diff) |

Formation breakup is the dangerous one, because it is invisible to every single-aircraft instrument.
Each agent reports "airworthy"; the formation has already broken up.

## §4 Component mapping (reuse, don't rebuild)

Formation Flight is mostly **composition of primitives that already exist**. The flight model already
named the products; this spec assigns them formation roles:

| Formation role | Product / primitive | Job |
|---|---|---|
| **Tower** (lead — holds formation) | Loom (cross-session port) | Orchestrator altitude. Owns formation integrity, λ per slice, the merge. Does NOT fly the mission. |
| **Cockpit** (per-sortie tactical) | Topography (scoring/active/handoff) | One agent flying one seam, fast and local. |
| **Recorder / Lift** | Witness (mandatory recorder, WS-DDR-098) | Logs every sortie's inputs/outputs; the telemetry that makes the formation observable and λ calibratable (shadow-autonomy §9 of the flight model). |
| **Variance / adversarial verify** | Voices (panel, conservation law) | High-λ seams get an adversarial verifier panel; contradictions preserved as two findings, never merged. |
| **Coherence-gate engine (Stage B)** | `audit_chain` (`servers/knowledge.py:1348`) | The Observe-phase read on substrate health: graph topology drift. |
| **Lineage / event fabric** | `make_event` + `TraceContext` (`servers/models.py`) | trace_id = formation, span_id = sortie, parent_id = hierarchy. |

## §5 The five mechanisms (this spec family)

1. **Mission Brief** (`SPEC-INTENT-MISSION-BRIEF-001`, `formation/mission-brief.schema.json`) — the typed
   dispatch payload every spawned agent receives. The structural fix for formation breakup: the
   intent, glossary, invariants, non_goals, frozen Contract, λ/trust-gate, verification rubric, and
   lineage travel WITH the agent into isolation.
2. **Seam decomposition** (`SPEC-INTENT-SEAM-DECOMPOSITION-001`) — fan out on Contract seams, not files.
   Collisions become impossible by construction. Extends `idd-build-pattern.md` Shape 2 (physical) with
   the Contract-as-fan-out-unit (semantic).
3. **Two-stage coherence gate** (`SPEC-INTENT-COHERENCE-GATE-001`) — the synthesis barrier is a coherence
   gate, not a merge. Stage A (brief-conformance, in-orchestrator) catches semantic collision; Stage B
   (wrap `audit_chain`) catches topology drift and provides the stop predicate. **Wrapping audit_chain
   alone is a false-green gate** (see that spec's §1) — Stage A is the load-bearing new behavior.
4. **Drift-clean loop** (defined in the coherence-gate spec) — for coherence work, "done" = no new drift
   findings across a full pass (fixpoint iteration). The convergence detector for loop-until-done.
5. **Formation governance matrix** (`SPEC-INTENT-FORMATION-GOVERNANCE-001`) — maps L0–L4 × λ →
   (model, isolation, privilege, verification intensity). High-λ → worktree + Opus + adversarial verify;
   low-λ exploration → Haiku + read-only. Quarantine = an L0 input gate.

Runnable realizations live in `formation/`: the two schemas, `coherence-gate.workflow.js`, and the
reference harness `formation-flight.workflow.js`.

## §6 The ON-trigger — solo stays zero-overhead

Formation Flight applies **only** when work is BOTH parallel AND coherence-critical. A single coherent
feature needs none of it. The machinery is **invocation-scoped, not session-scoped**: it lives in the
orchestrator harness you run only when you deliberately fan out.

> **ON-trigger:** the dispatch of **≥2 parallel agents declaring the same parent `intent` id.**

Clean because it keys off explicit existing artifacts (the dispatch + the intent id) — no detector, no
"coherence-critical" classifier (that drift is what killed the lexical Stop-hook layer). At N=1 the
solo path imports nothing → literally zero per-turn cost. The discipline is knowing when to fly solo.

## §7 What this is NOT (and the Drag constraint)

- **Not replacing the flight model.** The single-aircraft forces, λ, and crash modes still govern each
  sortie. Formation adds the multi-aircraft layer above them.
- **Not a new hook.** `hooks/pre-commit-drag-guard.sh` blocks commits that grow `hooks/`; the lexical
  Stop-hook layer measured **95.8% overhead**. Every formation check runs **in the orchestrator at
  synthesis time** (data-level) — a **template, never an enforced global hook.** Enforcement is only
  earned later, by measured collision data, and debits the Drag budget per the freeze rule.
- **Not relaxing closure-discipline.** Resolved still requires `upstream_control_path:` +
  `catch_mechanism:`. Formation adds coordinated parallel autonomy, not looser standards.

## §8 Provenance — borrowed mechanics, owned governance

The orchestration mechanics are not new and are not claimed:

| Mechanism | Prior art |
|---|---|
| Fan-out + synthesize | MapReduce (Dean & Ghemawat, 2004) |
| Adversarial verification | Argyris double-loop (already RAT-002) + separation of duties |
| Loop-until-done (drift-clean) | Fixpoint iteration |
| Tournament / generate-and-filter | Elo / pairwise preference (RLHF machinery) |
| Quarantine (untrusted input → low privilege) | Taint tracking / privilege separation (Saltzer & Schroeder, 1975) |
| Seam decomposition | Beer VSM recursion; Alexander bounded centers |

**Intent's defensible contribution is the governance layer**, consistent with DEC-013 (differentiation
= the spine + altitude, not the engine): *the typed Mission Brief that survives isolation, and the
two-stage coherence gate that closes the Observe loop over isolated parallel work.* The chassis is
commodity; the coherence contract that rides it is not. Position Intent as the flight computer, not the
engine.

## §9 Ratification dependencies (status → accepted)

Ratifies together with the flight model and surface matrix (the sibling set). Additional:

1. One real exercise run (≥2-seam formation) with captured failure modes (the "see where it can't stand
   up" close) — recorded as signals.
2. The coherence-gate Stage A proven to catch a seeded vocabulary-drift / non-goal violation that
   `audit_chain` alone passes green.
3. Witness routing for formation findings (reuses §11.2 mandatory-recorder).
4. DEC-014 written.

## §10 Exercise (the point)

This spec is not ratified by being written; it is ratified by being **flown**. The reference harness
(`formation/formation-flight.workflow.js`) is run on a real 2–3-seam parallel task. We deliberately
seed a drift in one sortie and confirm the gate catches what `audit_chain` alone misses. Every place it
stalls, over-blocks, or false-greens becomes a signal and feeds the next pass. Formation Flight earns
its place by closing a loop on real data with a trace — not by existing.
