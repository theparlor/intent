---
id: SIG-2026-06-05-formation-flight-build
type: signal
status: open
severity: build
created: 2026-06-05
target: Formation Flight — coherent non-colliding parallel development built + ready to exercise.
discovered_during: "Brien handed a repo-blind build prompt to execute in-repo: 'go all the way ... our objective is to be able to exercise this and see where it can't stand up.'"
requested_by: brien
upstream_control_path: "Built artifacts under Core/frameworks/intent/: 5 specs (SPEC-INTENT-FORMATION-FLIGHT-001 + MISSION-BRIEF/SEAM-DECOMPOSITION/COHERENCE-GATE/FORMATION-GOVERNANCE-001), runnable kit formation/ (2 schemas + 2 workflow harnesses + dataclasses + test + README), idd-build-pattern Shape 4 + anti-pattern, DEC-014, source manifest. Static-verified: node --check x2 green, dataclass<->schema 6/6, audit_chain probe live."
catch_mechanism: "Specs are draft; ratify-together gate (flight model + surface matrix) is the catch. The EXERCISE (run formation-flight.workflow.js on a real >=2-seam task, seed a drift, confirm Stage A catches what audit_chain alone misses) is the demonstrable-function close — pending."
pipeline_survival: "Runnable kit survives (node-checked, test-pinned). The exercise will surface where it cannot stand up -> new signals."
reconsider_when:
  - "the exercise run is executed -> capture failure modes as signals; promote the spec family from draft toward accepted per the ratify-together set."
  - "a second real formation run is done -> re-fit whether the Mission Brief field set is right (drop/add fields by evidence) and whether governance bands hold."
---
# Formation Flight — build record (Notice/Observe)

Built the formation layer for coherent non-colliding parallel development as the **multi-aircraft
extension of the Autonomy Flight Model**, grounded in the real repo (manifest:
`.intent/discovery/2026-06-05-formation-flight-source-manifest.md`). Decisions: DEC-014.

**What's new (thin):** the typed **Mission Brief** (dispatch payload), the **two-stage coherence gate**
(Stage A brief-conformance + Stage B audit_chain, delta-gated), seam-as-frozen-Contract decomposition,
and the L0–L4 × λ governance matrix. **What's reused:** audit_chain, Contract, λ/trust bands, Witness,
Voices, Loom (Tower), Topography (Cockpit), the event/lineage fabric, idd Shape 2.

**Next (the point):** fly it. Run `formation/formation-flight.workflow.js` on a real 2–3-seam task,
seed a vocabulary-drift / non-goal violation, and confirm the gate catches what `audit_chain` alone
passes green. Every stall / over-block / false-green is a signal.

## Exercise result — 2026-06-05 (PROOF OBTAINED)

Ran the REAL gate via the Workflow tool (`formation/exercise-gate.workflow.js` → `coherence-gate.workflow.js`)
on a CLEAN sortie (`seam-schema`) + a SEEDED-DRIFT sortie (`seam-gate`). 3 agents, ~150s, ~234k tokens.

**Verdict: `drift_clean=false` — driven entirely by Stage A.**
- **Stage A caught the drift sortie with 7 findings; the clean sortie got 0 (exonerated):**
  `verification_failed` (the agent ran `false` via Bash → exit 1, did NOT trust the report's self-claim),
  `invariant_violated` (hooks/ touch vs template-only), `non_goal_violated` ×2 (servers/models.py + hooks/ —
  preserved separately, Voices conservation law), `vocabulary_drift` ×2 ("Brief Envelope" present + "Mission
  Brief" absent — preserved separately), `contract_breach` (contract_changed=true).
- **Stage B (`audit_chain`): red — 68 unspecced / 18 uncontracted / 77 orphans, ALL pre-existing repo debt,
  NONE referencing either sortie.** Identical regardless of which sortie ran.

**False-green proof:** `audit_chain` is blind to the drift (its findings are unchanged by it); with delta-gating
and NO Stage A, the drift would pass `drift_clean=true`. **Stage A is load-bearing.** DEC-014 validation
criterion #1 satisfied.

**Findings from the exercise (where it bent):**
1. **FIXED — gate must fail closed.** The first attempt (top-level Workflow `args` arrive stringified →
   `args.sorties` empty) made the gate early-return `drift_clean:true` (0 agents, 4ms). A gate that reports
   clean when handed nothing IS a false-green. Fixed: `coherence-gate.workflow.js` now FAIL-CLOSED on empty
   sorties (`drift_clean:false` + a `no_sorties` finding). Lesson: invoke via a self-contained harness that
   builds sorties internally, never via stringified tool args.
2. **Calibration — Stage-A over-attribution.** One finding said `servers/models.py` was "modified on disk
   (9431 bytes)"; the file exists but was not actually modified (the fixture only *claimed* the touch). The
   finding is correct (non-goal violated per the report) but the embellishment shows Stage-A agents can
   over-read disk state. Watch for it; prefer claims grounded in the report + a run, not inferred disk deltas.
