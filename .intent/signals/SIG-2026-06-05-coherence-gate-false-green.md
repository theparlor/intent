---
id: SIG-2026-06-05-coherence-gate-false-green
type: signal
status: open
severity: design
created: 2026-06-05
target: Formation Flight coherence gate — "wrap audit_chain" is a false-green gate; drift-clean must be delta, not absolute.
discovered_during: "Formation Flight build (DEC-014). Two parallel design reviews flagged it; probing the real audit_chain confirmed it: the intent repo's baseline is color=red (66 unspecced signals, 18 uncontracted specs, 75 orphans) for pre-existing reasons unrelated to any formation."
requested_by: brien
upstream_control_path: "PARTIAL — fixed in formation/coherence-gate.workflow.js (Stage B now gates on NEW findings vs a pre-fan-out baseline, not absolute color) + formation/formation-flight.workflow.js (captures the baseline before fan-out) + SPEC-INTENT-COHERENCE-GATE-001 §drift-clean. PENDING upstream control: a test asserting the gate gates on delta (so a future edit cannot silently revert to absolute-green)."
catch_mechanism: "PENDING — no automated catch yet that a future change re-introduces absolute-green gating. Candidate: a unit test over coherence-gate that feeds a red baseline + a clean formation and asserts drift_clean=true; and the inverse (a new finding) asserts false."
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
