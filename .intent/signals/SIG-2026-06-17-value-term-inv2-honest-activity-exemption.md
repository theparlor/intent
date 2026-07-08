---
id: SIG-2026-06-17-value-term-inv2-honest-activity-exemption
date: 2026-06-17
type: comparator-recalibration
status: resolved
severity: medium
upstream_control_path: "Core/frameworks/intent/tools/value_term_audit.py _audit_entry() INV-2, the comparator now exempts an activity-measuring dimension from the healthy+activity FAIL when it honestly declares observability-only status via outcome_signal beginning \"n/a by design, <outcome-close>\". This is the producer of the verdict consumed by value_term_invariants.py INV-VALUE-TERM-CLEAN (nightly/overwatch suite)."
catch_mechanism: "INV-VALUE-TERM-CLEAN remains armed and unchanged in scope. The exemption is additive, it can only convert a FAIL to PASS for entries matching the documented honest-disclosure convention; it cannot newly-pass a SILENT activity term (no outcome_signal) nor one that CLAIMS an outcome_signal while measuring activity (those still FAIL). Zero-violation-start verified: full cross-product registry run exits 0 on 2026-06-17 (INV-VALUE-TERM-CLEAN PASS, INV-VALUE-TERM-COVERAGE PASS)."
pipeline_survival: "The change lives in the audit engine (value_term_audit.py) that value_term_invariants.py imports; it is exercised on every nightly/overwatch invariant run. Verified PASS this session against the live registry set (cast, gauge, topography, pulse, intent, voices, loom, forge, cortege, org-design-tooling). Survives the next portfolio audit run."
summary: "INV-VALUE-TERM-CLEAN FAILed on gauge-audit + gauge-ensemble-pass (status=healthy + measures=activity). Both are honestly-labeled observability-only terms with outcome_signal \"n/a by design, the outcome is gauge-findings / the merged majority core\" and an explicit outcome-close pointer, the GOOD pattern the discipline prescribes, not the anti-pattern. The comparator penalized the disclosure. Fixed at the comparator (feedback_audit_vs_writethrough: when the data is correct but the audit keeps firing, suspect the comparator), not by relabeling gauge's honest data."
surfaced_by: "SCOUT global lens=health sweep 2026-06-17 (where-next #2; dissent: data-dirty vs comparator-misfire, resolved here in favor of comparator-misfire)"
---

# INV-2 honest-activity exemption — value-term comparator recalibration

## What fired and why it was a false positive

`value_term_invariants.py / INV-VALUE-TERM-CLEAN` failed on two Gauge entries:

```
[INV-2] gauge-audit: status=healthy but measures='activity'
[INV-2] gauge-ensemble-pass: status=healthy but measures='activity'
```

INV-2 (in `value_term_audit.py _audit_entry`) was a flat rule:
`status == "healthy" and measures == "activity" → FAIL`.

But both Gauge entries are the discipline's **intended honest pattern**:

- `gauge-audit` — `measures: activity`, `outcome_signal: "n/a by design — the
  outcome is gauge-findings…"`, with `activity_proxy_risk` text explicitly naming
  the proxy risk it guards and `notes: "Correctly labeled activity."`
- `gauge-ensemble-pass` — `measures: activity`, `outcome_signal: "n/a by design —
  the outcome is the merged majority core (gauge-determinism-consensus)…"`.

The value-term discipline exists to stop a score from measuring its own ACTIVITY
while being *read as* delivered value. The honest move it prescribes is exactly
what Gauge did: label observability-only counts `measures: activity` so "N audits
run" can never be mistaken for outcome, and point to the sibling dimension that
closes the outcome. The flat INV-2 penalized that disclosure — it would force an
honest observability term to carry `defect`/`capped` (which then demands a
remediation for a thing that is not broken). That violates
`feedback_invariant_zero_violation_start` for any honest activity term.

## The fix (comparator, not data)

`Core/frameworks/intent/tools/value_term_audit.py` — INV-2 now FAILs
`healthy + activity` **only when** the entry does NOT declare itself
observability-only. Detection keys on the documented convention:
`outcome_signal` beginning with `"n/a by design"`. An honest term that names
its outcome-close passes; a SILENT activity term, or one CLAIMING an
outcome_signal while measuring activity, still FAILs.

Blast radius is one-directional and safe: the exemption can only relax the
current FAIL for convention-matching entries. No other registry currently has a
`healthy + activity` entry, so nothing is newly passed or failed elsewhere.

## Verification

`python3 value_term_invariants.py` (root Core/) → **exit 0**:
`INV-VALUE-TERM-CLEAN PASS · INV-VALUE-TERM-COVERAGE PASS`. Confirmed against the
live registry set this session.

## Related

- `feedback_audit_vs_writethrough` — write-through/data is primary; a fix that's
  correct while the audit keeps firing means suspect the comparator.
- `feedback_invariant_zero_violation_start` — a new/updated invariant must hold
  zero violations on honest data day one.
- `SIG-2026-06-09-signal-staleness-recalibration` (library-index) — same shape:
  a decision-driving check firing on a legitimate pattern was recalibrated at the
  comparator, not worked around.
- Gauge registry: `Core/products/gauge/value-term-registry.yaml`.
