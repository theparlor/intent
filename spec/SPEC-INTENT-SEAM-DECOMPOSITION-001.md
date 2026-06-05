---
title: Seam Decomposition — fan out on Contracts, not files
id: SPEC-INTENT-SEAM-DECOMPOSITION-001
type: spec
status: draft
plane: bridge
created: 2026-06-05
updated: 2026-06-05
author: intent framework (formation-flight build)
parent: SPEC-INTENT-FORMATION-FLIGHT-001
related:
  - playbooks/idd-build-pattern.md (Shape 2 physical isolation; Shape 4 formation — this is the semantic half)
  - spec/work-ontology.md (Contract = level 4, the seam unit)
  - servers/models.py (ContractType.INTERFACE, contract_frontmatter, verification_command)
  - knowledge-engine/spec/federation.md (inherit down / promote up / never leak sideways = separation minima)
---
# Seam Decomposition

> One sentence: decompose parallel work on **interface boundaries (Contracts)**, not on files — so that
> collisions become impossible by construction rather than something the merge step has to clean up.

**Status:** `draft` · **Created:** 2026-06-05

---

## 1. Intent

### What I noticed
Most collision is a **decomposition failure**, not an execution failure. When agents are fanned out by
file ("you take these files, you take those"), they share assumptions silently and edit across each
other's mental boundaries. When they are fanned out by **seam** — each owning one frozen interface — two
agents *cannot* collide on that interface, because neither may change it unilaterally.

### Why it matters now
Intent already has the seam primitive: **Contract** is level 4 of the Work Ontology
(Signal→Intent→Spec→**Contract**→Capability→Feature→Product) and a typed model
(`ContractType.INTERFACE`, `contract_frontmatter()` with `verification_command`). And `idd-build-pattern.md`
Shape 2 already gives **physical** isolation (parallel worktrees). What's missing is the rule that ties
the fan-out unit to the Contract — the **semantic** separation minima.

### Desired outcome
A decomposition rule: given an intent, produce N sorties where each owns exactly one frozen Contract
(seam), no two share a seam, and each seam carries its own `verification_command`. Physical collision is
handled by worktrees (Shape 2); semantic collision is handled by the frozen Contract + the coherence gate.

---

## 2. Shape

### Approach (the rule)
1. **Find the seams.** From the parent intent, enumerate the interface boundaries — the Contracts. If the
   Contracts don't exist yet, the decomposition step **mints them first** (Spec → Contract per the work
   ontology) and then freezes them. You cannot fan out until the seams are named.
2. **One seam per sortie.** Each Mission Brief carries exactly one `interface_contract` (CON id) and a
   unique `seam_id`. **No two briefs share a `seam_id`** — separation minima. This is Decision 13's
   *"never leak sideways"* applied to agent topology.
3. **Freeze the Contract.** An agent may build freely *behind* its Contract (produce Capabilities), but it
   **may not change the Contract itself**. A `contract_changed: true` in the Mission Report is a breach the
   coherence gate escalates — a seam cannot move its own boundary unilaterally; that requires the Tower.
4. **Each seam is independently verifiable.** The Contract's `verification_command` is the per-seam test.
   The coherence gate Stage A runs it (the existing `audit_chain` only checks that a `verified:` flag
   exists — it never runs the command).
5. **Physical containment per λ.** High-λ mutating seams get `isolation: worktree` (Shape 2). Read-only or
   exploratory seams get `readonly`. This is the Lift investment that buys parallel autonomy.

### Why Contracts make collision impossible (the structural argument)
A Contract is a *frozen interface*. If agent A and agent B each own a distinct frozen interface, then:
- Neither can change the other's boundary (semantic separation).
- Their worktrees keep their file mutations apart (physical separation).
- Their outputs are checkable independently (`verification_command` per seam).
So the only remaining coupling is *through the contracts themselves* — which are frozen and owned by the
Tower. Collision is designed out, not merged out.

### Prior art (cited, not claimed)
- **Beer's VSM recursion** — each seam is a viable subsystem operating autonomously behind its interface,
  recursively governed. The Tower is System 3/5 to each sortie's System 1.
- **Alexander's bounded centers** — a seam is a center with a clear boundary; coherence comes from
  well-formed boundaries between centers, not from a master plan.
- **Parnas information hiding / interface segregation** — the contract is the public interface; the
  implementation behind it is hidden and independently replaceable.

### Boundaries
**In:** the decomposition rule; the Contract-freeze mechanism; the seam-uniqueness invariant.
**Out:** worktree mechanics (owned by `idd-build-pattern.md` Shape 2 — this spec *points* to it, does not
restate it); the gate that checks conformance (owned by `SPEC-INTENT-COHERENCE-GATE-001`).

### Key decisions
- Fan-out unit = Contract (CON), not file. Reuse the existing typed Contract; do not invent a new seam type.
- Contracts are frozen for the duration of the sortie; only the Tower re-cuts seams.
- This spec is thin by design: ~70% pointer to Shape 2 + work-ontology, ~30% new (Contract-as-fan-out-unit).

### Open questions
- Granularity heuristic: too-coarse seams overlap (agents step on each other); too-fine seams add merge
  overhead. Initial guidance: one seam per `ContractType.INTERFACE` boundary; revisit after the exercise.

---

## 3. Contract

### Done when
- [ ] Every sortie in a formation has exactly one `seam_id` and one `interface_contract` (CON id).
- [ ] No `seam_id` is shared across briefs in the same formation (separation minima holds).
- [ ] Each seam's Contract has a `verification_command`.
- [ ] At merge, the intersection of sibling `touched_paths` is empty outside each seam's declared scope
      (no mid-air collision).

### Smoke test
```
# given a formation's briefs: assert seam_ids are unique and each has a CON + verification_command
python3 - <<'PY'
briefs = [...]  # list of mission briefs for one formation
seams = [b["seam_id"] for b in briefs]
assert len(seams) == len(set(seams)), "seam collision"
assert all(b["interface_contract"] and b["verification_rubric"]["verification_command"] for b in briefs)
print("seam decomposition OK")
PY
```

### Failure modes to watch
- **Seams too coarse** → agents overlap → mid-air collision (caught by `touched_paths` intersection, but
  better avoided at decomposition).
- **Contract not actually frozen** → an agent "fixes" the interface another depends on → silent breach
  (caught by `contract_changed`, but it means the decomposition leaked).
- **Seams minted but not verifiable** → a Contract with no `verification_command` → Stage A has nothing
  to run.

### Observability
The Tower records the seam map (briefs) to Witness at fan-out; the coherence gate reports any seam-overlap
or contract-breach finding against `seam_id`.
