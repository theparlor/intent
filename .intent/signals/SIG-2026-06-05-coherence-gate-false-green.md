---
id: SIG-2026-06-05-coherence-gate-false-green
type: signal
status: resolved
severity: design
created: 2026-06-05
target: Formation Flight coherence gate — "wrap audit_chain" is a false-green gate; drift-clean must be delta, not absolute.
discovered_during: "Formation Flight build (DEC-014). Two parallel design reviews flagged it; probing the real audit_chain confirmed it: the intent repo's baseline is color=red (66 unspecced signals, 18 uncontracted specs, 75 orphans) for pre-existing reasons unrelated to any formation."
requested_by: brien
upstream_control_path: "COMPLETE — the delta gate in formation/coherence-gate.workflow.js (Stage B gates on NEW findings vs a pre-fan-out baseline, not absolute color) + formation/formation-flight.workflow.js (captures the baseline before fan-out) + SPEC-INTENT-COHERENCE-GATE-001 §drift-clean, NOW GUARDED by formation/coherence_gate_predicate.test.mjs (built 2026-07-02)."
catch_mechanism: "BUILT 2026-07-02: formation/coherence_gate_predicate.test.mjs (node --test). The Workflow harness forbids sibling imports (meta must be first statement), so the drift-clean predicate stays INLINE in coherence-gate.workflow.js between `coherence-gate:drift-predicate` sentinels; the test EXTRACTS that exact block and executes it against fixtures — real code, no shadow copy. Fixtures: red baseline + zero delta => drift_clean TRUE (the anti-false-green assertion); a NEW finding => FALSE; plus a source guard asserting the predicate never references stageB.color. A revert to absolute-color gating fails both (mutation-verified 2026-07-02). Run: node --test formation/coherence_gate_predicate.test.mjs (7 tests, green)."
pipeline_survival: "The delta logic survives re-runs (it is in the workflow script, not session state); the missing catch-net is the regression guard."
reconsider_when:
  - "any coherence/audit check is added that gates on an ABSOLUTE health score/color rather than a delta from baseline -> it will fire on pre-existing state (zero-violation-start violation); convert to delta."
  - "the gate's delta logic is edited -> add the regression test described in catch_mechanism before merging."
---
# The two findings behind the two-stage / delta gate

## Finding 1 — audit_chain alone is a false-green gate
`audit_chain` (`servers/knowledge.py:1348`) audits **persisted graph topology**: does a signal link
forward, does a spec have a contract, does a contract carry a `verified:` flag, does an entity have
inbound references. It **cannot** see the three semantic-collision types that matter for parallel agents:

1. **Vocabulary drift** — checks links exist, not term consistency across agents. "sortie" vs "mission" → green.
2. **Contract breach** — checks a contract is *referenced and marked* verified; never runs the
   `verification_command`. Breached-but-marked → green.
3. **Non-goal violation** — there is no `non_goals` concept in the persisted graph at all. Invisible.

So a gate that only wraps `audit_chain` certifies semantic collisions as clean — **worse than no gate.**
→ The coherence gate is **two-stage**: Stage A (brief-conformance, in-orchestrator, pre-persistence) +
Stage B (audit_chain topology). Stage A is the load-bearing new behavior.

## Finding 2 — drift-clean must be delta, not absolute (zero-violation-start)
Probing the live tool: the intent repo's baseline is `color=red` (66 unspecced signals, 75 orphans) for
pre-existing reasons. Gating drift-clean on absolute `color == green` would block **every** formation
merge on this repo for reasons unrelated to the formation — exactly the failure the
**zero-violation-start** principle warns against (`feedback_invariant_zero_violation_start`: a new check
must fire zero violations against existing state on day one).

→ Fixed: the harness captures a pre-fan-out `audit_chain` baseline; the gate counts only findings
**absent from that baseline**. Absolute color is reported but not gating. A formation that *resolves*
pre-existing debt is still clean.

This is itself a coherence-engineering datum: **any decision-driving health check needs a baseline/delta
framing, or it indicts pre-existing state as if the current change caused it.**
