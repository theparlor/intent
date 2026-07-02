---
title: value_term_audit status enum was OPEN - unknown statuses escaped all enforcement (INV-5 added)
type: signal
maturity: active
created: 2026-07-02
signal_id: SIG-INTENT-STATUS-ENUM-2026-07-02
detected: 2026-07-02
status: resolved
severity: medium
scope: "value_term_audit.py status-keyed enforcement. Every invariant (INV-1 defect-exemption, INV-2, INV-3, INV-4) keys off the status field, but status membership was never checked - any string outside {defect, capped, healthy} carried zero obligations and passed silently."
source: "loom priming-usefulness measure redesign 2026-07-02 (SIG-LOOM-USEFULNESS-SEAM-2026-07-02): the author had to deliberately keep status: defect with a phase: annotation because a natural intermediate status ('instrumented-pending-data') would have dropped loom-score-thread out of INV-3 enforcement entirely. The escape hatch existed; only author discipline kept it shut."
autonomy: L4
upstream_control_path: "Core/frameworks/intent/tools/value_term_audit.py::_audit_entry INV-5 + KNOWN_STATUSES - status is now a closed enum {healthy, fixed, capped, defect}; anything else (including empty) FAILs with exit 2 and no other invariant is evaluated for that entry (its obligations are undefined). This is in-pipeline, not a one-shot: every consumer path inherits it - --registry single-product audits, --all ecosystem sweeps, and value_term_invariants.py INV-VALUE-TERM-CLEAN (delegates to _audit_registry), which runs in the nightly/overwatch invariant suite."
catch_mechanism: "Core/frameworks/intent/tools/test_value_term_audit.py::TestINV5StatusClosedEnum - 5 fixture tests written RED-first (unknown status FAILs even with full remediation; empty status FAILs; 'fixed' recognized; defect + phase: annotation stays PASS; --all fails the ecosystem on one sneaky status). Plus the nightly INV-VALUE-TERM-CLEAN invariant now fires a SIG-VALUE-TERM-CLEAN-VIOLATION signal if any registry grows an out-of-enum status."
verification_command: "cd /Users/brien/Workspaces/Core/frameworks/intent/tools && python3 -m unittest test_value_term_audit test_value_term_invariants  =>  Ran 44 tests, OK  ;  python3 value_term_audit.py --all  =>  ECOSYSTEM: 0 FAIL across 12 registries, exit 0  ;  python3 value_term_invariants.py  =>  both invariants PASS, exit 0"
pipeline_survival: "yes: the enum check lives inside _audit_entry in the auditor engine itself, so every audit mode and the chain-audit invariant class evaluate it on every run; registries are declarative data no render pipeline rewrites. Regression to open-enum behavior is caught by the RED-first fixture tests."
---

# SIG-INTENT-STATUS-ENUM-2026-07-02

## The gap

`value_term_audit.py` enforced INV-3 (remediation required) only for
`status in {defect, capped}` and INV-1/2/4 only for `healthy`. Status
membership itself was never validated. Any other status string - an
intermediate lifecycle label like `instrumented-pending-data`, a typo, or an
empty field - carried NO invariant obligations and passed silently. The
registry vocabulary was documented as closed (`healthy | fixed | capped |
defect` in value-term-registry-README.md and in the loom registry header) but
the auditor treated it as open.

This is the catch-net's own version of the anti-pattern it polices: the audit
claimed coverage ("every declared score/gate checked") while a whole degree of
freedom (status) was unmeasured.

## How it surfaced

During the 2026-07-02 loom priming-usefulness redesign, the honest label for
`loom-score-thread` was "defect, but instrumented, pending data". A custom
status would have silently removed the entry from INV-3 enforcement, so the
author kept `status: defect` and added a `phase:` annotation - and noted the
silent-pass hazard inline in the registry. That inline note was the detection.

## The fix (decision: closed enum, annotation fields for lifecycle)

Between the two options in the task (closed enum vs per-status obligation
definitions), both were done in one move:

- **INV-5**: `status` must be in `{healthy, fixed, capped, defect}`; unknown or
  empty status FAILs loudly and short-circuits the entry (obligations
  undefined). Checked first.
- **Obligations matrix** documented at `KNOWN_STATUSES` in the module, the
  docstring, and the README: healthy -> INV-1/2/4 · fixed -> INV-1 ·
  defect/capped -> INV-3.
- Intermediate lifecycle state is recorded via annotation fields (`phase:`)
  on top of one of the four statuses - the loom pattern is now the sanctioned
  and test-protected precedent (`test_defect_with_phase_annotation_passes`).

## Sweep result

All 12 discovered registries (10 under `Core/products/*/`, intent's own, plus
the vendored copy under `products/forge/outputs/dist/voices-panel/`) audit
clean under the new enum: every live status is already one of the four.
Zero-violation start holds (feedback_invariant_zero_violation_start).

Observation (out of scope, flagged separately): the forge `outputs/dist/`
vendored registry copy is discovered by `--all` despite the "never audit
vendored copies" intent of `_EXCLUDE_DIR_PARTS` - it double-audits the voices
entries.

## Related

- SIG-LOOM-USEFULNESS-SEAM-2026-07-02 (the near-miss that surfaced this)
- Core/products/loom/value-term-registry.yaml header note (updated to reflect
  INV-5 enforcement)
- value-term-registry-README.md (schema + invariants updated)
