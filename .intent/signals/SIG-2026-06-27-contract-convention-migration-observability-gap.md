---
id: SIG-2026-06-27-contract-convention-migration-observability-gap
product: intent
type: signal
status: open
severity: design
created: 2026-06-27
target: "Intent chain-observability. No mechanism surfaces downstream consumers still bound to an OLD contract/convention when an upstream product migrates it; and no closure rule forces a downstream leaf-fix to emit an upstream-examination signal. Both currently depend on the operator remembering."
discovered_during: "2026-06-27 synthesis-glob consumer-drift remediation (cast 1a501f6c, forge e9612d8, voices 1234b91; symptom record /Users/brien/Workspaces/Core/products/cast/.intent/signals/SIG-2026-06-27-synthesis-glob-consumer-drift.md). A roughly 2-month-old convention split sat undetected and was found by accident."
requested_by: brien
upstream_control_path: "NONE YET. This signal proposes the controls. Candidate homes: (1) /Users/brien/Workspaces/Core/frameworks/intent/tools/convention_migration_invariant.py (new, stdlib, mirroring methodology_coverage_invariant.py and value_term_invariants.py) reading a per-contract bound_consumers + forbidden_legacy_patterns block declared in /Users/brien/Workspaces/Core/products/cast/contracts/*-port.md; (2) a new closure-DoD clause in /Users/brien/Workspaces/Core/frameworks/intent/spec/signal-stream.md plus a detector arm in /Users/brien/Workspaces/Core/frameworks/intent/tools/closure_writeboundary_check.py."
catch_mechanism: "NONE YET, proposed below. Until built, status stays open (not resolved): no automated catch exists that (a) a consumer still references a retired convention after a contract migration, or (b) a downstream leaf-fix closed without an upstream-examination signal."
pipeline_survival: "SAFE to design. Both proposed controls are read-only auditors or write-boundary checks over source-of-truth files (port contracts, signal frontmatter), not pipeline outputs. Must satisfy zero-violation-start (feedback_invariant_zero_violation_start): declare bound_consumers only where it currently holds, so the invariant passes on day one."
blast_radius: medium
exposure: solo
irreversibility: 0.1
strategic_value: 0.7
detection_speed: days
autonomy_level: L3
---

# Contract/convention migration is the blind spot in chain-observability

## The ratified aim this is a counterexample to

The Intent framework's chain-observability claim (Forge/Cast CLAUDE.md, implemented at /Users/brien/Workspaces/Core/frameworks/intent/spec/signal-stream.md) is that the system's own signal stream surfaces incoherence as it forms, not scheduled audits. Signal Stream "How Signals Work" lists "a failed contract assertion" and "a pattern noticed in agent execution traces" as first-class signal sources.

The 2026-06-27 synthesis-glob defect is a direct counterexample. An upstream Cast convention migrated (around 2026-04-17) from opus-synthesis-YYYY-MM-DD.md to synthesis-YYYY-MM-DD-<tier>-<slug>.md. The Cast-to-Voices port contract (/Users/brien/Workspaces/Core/products/cast/contracts/voices-identity-port.md) already names the CURRENT surface (corpus/{slug}/synthesis-*.md). But three classes of downstream consumer stayed bound to the dead opus-synthesis-* glob and degraded silently for roughly 2 months:

- Forge critique skills (panel-critique, panel-critique-v2-balanced, disconfirmation-panel plus cowork copies) emitted a false "synthesis pending" flag on fully-synthesized voices and loaded the thinner registry-substance block instead of the full opus synthesis.
- Forge voices-server tools.py mislabeled synthesis_tier as "sonnet-standard" always, and on same-date opus/sonnet ties loaded the sonnet file over the opus one.
- voices orchestrate.py had a dead lead pattern.

Nothing in the signal stream fired. The split was found only because a 2026-06-26 estimation panel happened to print "synthesis pending" 11 times. Incoherence did NOT surface as it formed; it surfaced by accident, months late.

## The framework-owned gap (two parts)

This is not a Cast bug, a Forge bug, or a Voices bug. Those are the leaves, and they are already fixed. The systemic gap is owned by the Intent framework, which is the layer that asserts chain-observability:

1. **No cross-product migration sensor.** When a named contract or convention changes at its upstream site, nothing enumerates the downstream consumers still bound to the old form. The pipeline scripts (compute-cvrs.py, chain_audit.py, and the rest) used robust *synthesis*.md globs and were fine; the CONSUMER surfaces with the dead glob were exactly the ones with no catch. A convention can split producer from consumer and the system stays green.

2. **No enforcement that a downstream fix emits an upstream signal.** Brien's just-stated discipline, that a downstream leaf-fix must trigger an upstream-examination signal, is today an operator habit. The same shape already exists in memory as feedback_decision_atom_correction_propagation.md (a decision atom with affected files should dispatch a correction pass), but there is no framework mechanism that fires it. Closure-discipline enforcement (spec/closure-discipline-enforcement.md, the Stop + PreToolUse hooks) gates "resolved-without-upstream-control" but does NOT require that a leaf-level fix register an upstream-examination follow-up. A leaf can be patched and committed with no record asking "what convention drifted to allow this, and what else is bound to it?"

## Proposed improvement (mirror existing framework mechanisms; do not over-engineer)

### Control A: contract/convention-migration observability (the migration sensor)

Make the port contracts in /Users/brien/Workspaces/Core/products/cast/contracts/*-port.md the source of truth for what a convention IS and who is bound to it. Add two optional frontmatter blocks to a port contract:

- bound_consumers: the files/globs that read the surface (e.g. the Forge critique skills, voices-server tools.py, orchestrate.py).
- forbidden_legacy_patterns: retired forms that MUST NOT appear in a bound consumer (e.g. opus-synthesis-*).

Then a new stdlib invariant /Users/brien/Workspaces/Core/frameworks/intent/tools/convention_migration_invariant.py, built in the exact shape of methodology_coverage_invariant.py and value_term_invariants.py (pure stdlib, read-only, runnable in the overwatch/nightly suite, with a paired test_convention_migration_invariant.py):

- **INV-MIGRATION-NO-LEGACY (hard):** no bound_consumers file contains any forbidden_legacy_patterns token. This is the assertion that would have fired the day the Forge skills were not migrated.
- **INV-MIGRATION-CONSUMER-RESOLVES (advisory, promotable to hard via --strict):** every declared consumer path exists.

This converts "a failed contract assertion" from an aspiration in Signal Stream prose into an actual mechanism, and it satisfies zero-violation-start because bound_consumers is declared only where it already holds.

### Control B: downstream-fix-implies-upstream-signal as a closure-DoD clause

Add a clause to the Closure Criteria section of /Users/brien/Workspaces/Core/frameworks/intent/spec/signal-stream.md: when a signal records a downstream/leaf fix of an upstream-originated drift (convention, contract, naming, schema), closing it as resolved REQUIRES a triggers_upstream_examination: field pointing at a sibling open signal (or an explicit upstream_examination: not-applicable with one-line rationale). Then extend /Users/brien/Workspaces/Core/frameworks/intent/tools/closure_writeboundary_check.py with a detector arm: if a status: resolved signal's body matches downstream-fix language (e.g. "downstream", "consumer", "leaf-fix", "patched the caller") AND lacks triggers_upstream_examination:, flag it, the same write-boundary catch-net pattern already used there for premature-resolved. This makes the correction-propagation reflex a mechanism rather than a habit.

## Why not over-build

No new infrastructure, no daemon, no graph DB. Both controls reuse patterns the framework already ships: a stdlib invariant in tools/ (Control A) and a write-boundary detector arm (Control B), each declared against existing source-of-truth files (port contracts, signal frontmatter). The Rule-of-Three is satisfied for extraction-grade attention: synthesis-glob (this session) plus the Subaru Story-Points "size" to complexity leaf canon-fix (D-060, same session) plus the prior canon-recovery findings are all the same meta-pattern, a downstream leaf-fix of an upstream convention that drifted with no catch-net.

## Next

Propose-only; nothing built here. If greenlit, build Control A first (it is the sensor whose absence let this form), then Control B. Status stays open until at least Control A's invariant + test land and pass zero-violation against the live tree.
