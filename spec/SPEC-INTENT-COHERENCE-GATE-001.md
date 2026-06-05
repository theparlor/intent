---
title: Coherence Gate — the two-stage synthesis barrier
id: SPEC-INTENT-COHERENCE-GATE-001
type: spec
status: draft
plane: bridge
created: 2026-06-05
updated: 2026-06-05
author: intent framework (formation-flight build)
parent: SPEC-INTENT-FORMATION-FLIGHT-001
implements: formation/coherence-gate.workflow.js
related:
  - servers/knowledge.py (audit_chain :1348 — Stage B engine; what it can and cannot see)
  - servers/models.py (Contract.verification_command :291 — Stage A engine)
  - Core/products/voices/ (conservation law — preserve contradictions, never merge)
  - Core/products/witness/ (findings routed via signal_emit/lineage)
  - hooks/pre-commit-drag-guard.sh (why this is a template, not a hook)
---
# Coherence Gate

> One sentence: the synthesis step that closes a formation is a **coherence gate, not a merge** — it
> checks every sortie's output against its Mission Brief and the traceability chain, and only lets
> coherent work through.

**Status:** `draft` · **Created:** 2026-06-05 · **Implementation:** `formation/coherence-gate.workflow.js`

---

## 1. Intent

### What I noticed (the load-bearing finding)
The obvious design — "after the parallel agents finish, run `audit_chain` and merge if green" — is a
**false-green gate.** Verified at `servers/knowledge.py:1402-1430`: `audit_chain` reads only persisted
`.intent` artifacts and checks **graph topology** — does a signal link forward, does a spec have a
contract, does a contract carry a `verified:` flag, does an entity have inbound references. It
**structurally cannot** see the three semantic-collision types:

1. **Vocabulary drift** — it checks that links exist, never that two agents used the same term for the
   same concept. Agent A "sortie" + Agent B "mission" → green.
2. **Contract breach** — it checks a contract is *referenced and marked* verified; it never runs the
   `verification_command` nor compares output to the contract's assertions. A breached-but-marked
   contract → green.
3. **Non-goal violation** — there is no `non_goals` concept in the persisted graph at all. Invisible.

Plus timing: `audit_chain` runs *after* artifacts persist; semantic collision happens *during* isolated
execution, before merge. A gate that only wraps `audit_chain` certifies collisions as clean — **worse
than no gate.**

### Desired outcome
A two-stage barrier: a new **brief-conformance** check (Stage A) catches semantic collision before
persistence; the **existing `audit_chain`** (Stage B) catches topology drift and supplies the stop
predicate.

---

## 2. Shape

### Stage A — brief-conformance (NEW; the load-bearing behavior)
Runs **in the orchestrator at synthesis time**, per sortie, *before* artifacts persist. For each Mission
Report against its Mission Brief:

| Check | How | Catches |
|---|---|---|
| **Verification** | Run the brief's `verification_rubric.verification_command`; require exit 0 (and `report.verification.ran && passed`). | Contract breach (audit_chain never runs this) |
| **Invariants** | Each brief `invariant` vs report `invariants_selfcheck`; corroborate testable ones with the verification result, not the self-report alone. | Broken "don't do X" constraints |
| **Non-goals** | Each brief `non_goal` vs report `non_goals_selfcheck`; cross-check against `touched_paths`. | Scope creep / non-goal violation |
| **Vocabulary** | Report `vocabulary_terms` vs `reference_frame.canonical_terms` / `forbidden_synonyms`. | Vocabulary drift (formation breakup) |
| **Contract freeze** | `report.contract_changed` must be false. | A seam moving its own boundary |
| **Mid-air collision** | Intersect `touched_paths` across sibling reports; flag overlaps outside declared seams. | Physical collision that escaped isolation |

**Conservation law (Voices):** when two sorties produce *contradictory* outputs, Stage A preserves
**both** as two findings — it never silently merges to a false consensus (mirrors Voices `named_dissents`
and Witness append-only). Output: a list of findings `{kind, seam_id, brief_id, detail, severity}`.

Self-report is a signal, not proof. For **high-λ seams** the matrix
(`SPEC-INTENT-FORMATION-GOVERNANCE-001`) escalates invariant/non-goal checks to an **adversarial Voices
panel** rather than trusting the sortie's self-check.

### Stage B — chain audit (REUSE)
After Stage A passes and artifacts persist, call `audit_chain(scope_token)` on the merged scope. Read its
`{color, counts, findings}`. This is the Observe-phase topology read — orphans, unspecced signals,
uncontracted specs, unverified contracts.

### The drift-clean stop predicate (delta, not absolute)
For coherence work, **"done" = drift-clean across a full pass** (fixpoint iteration). Stage B gates on
the **delta**, never absolute topology — `audit_chain` may be amber/red for PRE-EXISTING repo debt
unrelated to this formation (verified on this repo 2026-06-05: baseline `color=red`, 66 unspecced
signals, 75 orphans). Gating on absolute green would fire against existing state, violating the
**zero-violation-start** principle (`feedback_invariant_zero_violation_start`: a new check must fire
zero violations on day one). So:

```
drift_clean ⇔ stageA_findings == []
              AND  no NEW audit_chain findings vs the pre-fan-out baseline
              (absolute audit_chain.color is reported but NOT gating)
```

The harness captures a baseline `audit_chain` **before** fan-out and passes its finding set to the gate;
the gate counts only findings absent from that baseline (a formation that *resolves* pre-existing debt is
still clean). The loop: while not `drift_clean`, feed findings back as bounded corrective sorties (each a
new Mission Brief scoped to the finding), re-run the gate. Bound the loop (max passes + `/goal`).
K consecutive drift-clean passes ⇒ converged.

### Where it runs (and why not a hook)
The gate is a **synthesis-time function inside the orchestrator** (`formation/coherence-gate.workflow.js`),
invoked only on the formation path. It is **not** a global hook: `hooks/pre-commit-drag-guard.sh` blocks
new hooks, and the lexical Stop-hook layer measured **95.8% overhead**. Enforcement-by-hook is earned
only later, by measured collision data, and would debit the Drag budget per the freeze rule. Findings
route to **Witness** (`signal_emit`/`lineage`) so the formation is observable and λ stays calibratable.

### Boundaries
**In:** Stage A checks; the `audit_chain` wrap; the stop predicate; the corrective-loop shape.
**Out:** a new datastore; a new hook; re-implementing `audit_chain` (wrap, don't fork).

### Key decisions
- Two stages, not one. Stage A is mandatory — shipping only the `audit_chain` wrap is the false-green bug.
- Self-report corroborated by verification + (for high-λ) adversarial verify.
- Template/in-orchestrator, never a hook.

### Open questions
- Vocabulary-drift detection precision: exact-term diff (cheap, brittle) vs. a cheap-tier semantic check
  (Ollama) — start with exact `forbidden_synonyms` + canonical-term presence; escalate only if noisy.

---

## 3. Contract

### Done when
- [ ] Given a set of Mission Reports + Briefs, Stage A returns findings for: a failed `verification_command`,
      a violated `non_goal`, a forbidden-synonym vocabulary drift, a `contract_changed`, and a
      `touched_paths` overlap.
- [ ] Stage B calls real `audit_chain` and reads `{color, findings}`.
- [ ] `drift_clean` is true only when Stage A is empty AND this formation introduced NO NEW `audit_chain`
      findings vs the pre-fan-out baseline (absolute color is informational, not gating).
- [x] **Proof of the finding (2026-06-05):** the exercise (`formation/exercise-gate.workflow.js`) ran the
      real gate on a clean + a seeded-drift sortie — Stage A flagged the drift with 7 findings (verification,
      invariant, ×2 non-goal, ×2 vocabulary, contract breach) and exonerated the clean sortie, while
      `audit_chain` (Stage B) returned identical pre-existing red for both → audit_chain alone is false-green.
      See `.intent/signals/SIG-2026-06-05-formation-flight-build.md` (Exercise result).
- [x] **Gate fails closed (2026-06-05):** empty/mis-invoked `sorties` returns `drift_clean:false` + a
      `no_sorties` finding, never a false-green (surfaced by the exercise's first attempt).

### Smoke test
```
# in formation/: run the gate over a fixture formation with one seeded drift
node coherence-gate.workflow.js --selftest   # or run via the Workflow tool on the fixture
# expect: Stage A flags the seeded drift; audit_chain alone returns green on the same fixture
```

### Failure modes to watch
- **Skipping Stage A** → false-green gate (the whole reason this spec exists).
- **Trusting self-report** → a lying/optimistic sortie passes; mitigate with verification + adversarial
  verify for high-λ.
- **Unbounded corrective loop** → cap passes + `/goal`.
- **Becoming a hook** → forbidden; stays in the orchestrator.

### Observability
Every gate run emits findings to Witness with `seam_id`/`brief_id`/`trace_id`; the drift-clean decision is
itself an event. The gate's output IS the Observe-phase read on a formation.
