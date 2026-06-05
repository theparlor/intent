---
title: Formation Governance Matrix — L0–L4 × λ → model · isolation · privilege · verification
id: SPEC-INTENT-FORMATION-GOVERNANCE-001
type: spec
status: draft
plane: bridge
created: 2026-06-05
updated: 2026-06-05
author: intent framework (formation-flight build)
parent: SPEC-INTENT-FORMATION-FLIGHT-001
sibling: SPEC-INTENT-AUTONOMY-SURFACE-MATRIX-001
ratify_together: true
related:
  - spec/autonomy-gate-surface-matrix-v0-DRAFT.md (sibling — surface × mode floors; cross-human L0 row)
  - spec/autonomy-flight-model-v1-DRAFT.md (λ source, §16; estimate-decide split §4)
  - spec/SPEC-INTENT-COHERENCE-GATE-001.md (verification intensity column → which Stage runs)
  - .intent/config/approval-rules.yml (SPEC-APPROVAL-GATE — output-side L0)
---
# Formation Governance Matrix

> One sentence: a per-sortie governance map — given a seam's autonomy band (L0–L4) and its coefficient of
> bravery (λ), deterministically assign its **model, isolation, privilege, and verification intensity** —
> so the orchestrator (Tower) sets each aircraft's envelope by rule, not by vibe.

**Status:** `draft` · **Sibling of** the surface matrix and the flight model (ratify together).

---

## 1. Intent

### What I noticed
The surface matrix (`autonomy-gate-surface-matrix-v0-DRAFT.md`) answers *where the gate applies*
(surface × mode → floor + hook precondition) for **one** actor. Formation needs the orthogonal axis:
across **many** sorties, how does each seam's `(trust_gate, λ)` translate into concrete dispatch
parameters — which model, how much isolation, what it may do, how hard we verify it?

### Why it matters now
Without this, the orchestrator either over-provisions every sortie (Opus + worktree + adversarial verify
for trivial reads — wasteful) or under-provisions risky ones (no isolation on a high-blast mutate —
dangerous). The flight model's lesson applies: **spend Lift (isolation, verification) to fund Thrust
(autonomy)** — and spend it *proportionally*.

### Desired outcome
A deterministic function `(trust_gate, λ) → {model, isolation, privilege, verification}` the Tower applies
when constructing each Mission Brief.

---

## 2. Shape

### The matrix

| trust_gate | typical λ | model | isolation | privilege (actions) | verification intensity |
|---|---|---|---|---|---|
| **L0** | 0.0 (locked) | human drives / haiku read-only | `readonly` | none — propose only; **quarantine inputs** | human approval (output-side: SPEC-APPROVAL-GATE) |
| **L1** | low (≈1.0) | haiku | `readonly` | read / enrich / annotate | spot-check |
| **L2** | mid (≈1.0–1.3) | sonnet | `worktree` (if mutating) else `readonly` | mutate **within seam**; no commit | coherence-gate **Stage A** |
| **L3** | high (≈1.3–1.5) | sonnet → opus | `worktree` | mutate + commit to **branch** within seam | Stage A + **Stage B** (`audit_chain`) |
| **L4** | high (≥1.5, solo) | opus | `worktree` | full **within seam** (incl. push in solo repos) | Stage A + Stage B + **adversarial verify** (Voices panel) |

### λ modulation (the throttle, not a new axis)
λ shifts a seam *within* and *across* bands (it does not override the deterministic preconditions):
- **High λ** (solo Brien-owned surfaces) pushes a seam toward `worktree` + Opus + adversarial verify — Lift
  funded so Thrust is safe.
- **Low / zero λ** pins a seam to L0 regardless of computed trust. **Cross-human surfaces (Slack, email,
  calendar, PRs-with-reviewers) are λ = 0 → L0, locked** — identical to the surface matrix's cross-human
  row (referenced, not restated). Formation never raises a cross-human seam.

### Quarantine = the L0 input gate
A sortie that **reads untrusted input** (web fetch, third-party doc, external transcript) is governed as
an **input** boundary, distinct from its output band:
- The reading agent runs **low-privilege / `readonly`** and **may not mutate or commit** on the same turn
  it consumed untrusted content.
- A **separate, un-exposed** agent acts on its findings (the clean agent never touched raw untrusted bytes).

This is **taint tracking / privilege separation** (Saltzer & Schroeder, 1975) applied to input provenance
— prompt-injection containment by construction, not by detection. It composes with the output-side L0
(SPEC-APPROVAL-GATE) but is a distinct, input-side control.

### Boundaries
**In:** the `(trust_gate, λ) → params` mapping; λ modulation; the quarantine input-gate rule.
**Out:** the surface × mode floors (owned by the surface matrix — referenced); the gate mechanics (owned by
the coherence-gate spec); the per-product λ values (owned by `lambda-settings-by-product-v1.yaml`).

### Key decisions
- Sibling spec, not an inline edit of the surface matrix (WS-DDR-025; the matrix already declares the
  sibling-ratify pattern). The surface matrix gets a one-line pointer.
- Quarantine is an input-side gate, separate from the output-side approval gate.
- The matrix is the **default**; a brief may carry explicit overrides, recorded with rationale.

### Open questions
- Is λ scalar or vector here? (Inherited open question from flight-model §12 — formation consumes λ; it
  does not need to resolve this. Start scalar.)

---

## 3. Contract

### Done when
- [ ] Every Mission Brief's `(trust_gate, λ)` resolves to a deterministic `{model, isolation, privilege,
      verification}` tuple via this matrix.
- [ ] A cross-human seam (λ=0) is pinned to L0 regardless of computed trust.
- [ ] A quarantine seam (untrusted input) is `readonly`/no-mutate, and a separate agent acts on its output.
- [ ] `verification intensity` per band maps to which coherence-gate stages run (L2→A, L3→A+B, L4→A+B+adv).

### Smoke test
```
python3 - <<'PY'
def govern(trust_gate, lam, untrusted_input=False):
    if untrusted_input: return {"isolation":"readonly","privilege":"no-mutate","note":"quarantine"}
    table = {
      "L0":{"model":"haiku","isolation":"readonly","privilege":"propose","verify":"human"},
      "L1":{"model":"haiku","isolation":"readonly","privilege":"read","verify":"spot"},
      "L2":{"model":"sonnet","isolation":"worktree","privilege":"mutate-in-seam","verify":"A"},
      "L3":{"model":"opus","isolation":"worktree","privilege":"branch-commit","verify":"A+B"},
      "L4":{"model":"opus","isolation":"worktree","privilege":"full-in-seam","verify":"A+B+adv"},
    }
    g = dict(table[trust_gate])
    if lam == 0: g = table["L0"]   # cross-human lock
    return g
assert govern("L4", 1.8)["verify"] == "A+B+adv"
assert govern("L4", 0)["privilege"] == "propose"     # λ=0 pins to L0
assert govern("L2", 1.0, untrusted_input=True)["note"] == "quarantine"
print("governance matrix OK")
PY
```

### Failure modes to watch
- **λ overriding a hard floor** — λ modulates the band; it never lifts a deterministic precondition or the
  cross-human L0 lock.
- **Quarantine skipped** — an agent that both reads untrusted input and commits in one turn breaks privilege
  separation.
- **Over-provisioning** — Opus+worktree+adversarial on trivial reads is waste; respect the band.

### Observability
The Tower records each sortie's resolved governance tuple to Witness alongside its brief; deviations from
the matrix (explicit overrides) are events with rationale.
