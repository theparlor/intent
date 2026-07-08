---
id: SIG-2026-05-29-friction-02-catch-net-brittleness-bidirectional
created: 2026-05-29
type: road-readiness-friction
status: captured
severity: high
confidence: 0.92
trust: 0.7
friction_class: catch-net-brittleness
road_ready_gate: true
parent_signal: SIG-2026-05-29-friction-00-road-readiness-drag-synthesis
related:
  - feedback_audit_vs_writethrough
  - feedback_closure_dod_literal_terms
  - SIG-2026-05-28-stop-hook-check-6-trailing-observation
  - SIG-2026-05-28-stop-hook-regex-extension-implicit-queue
  - feedback_subagent_claim_vs_execute
---

# Friction-02: catch-nets misfire in BOTH directions and tax the human into regex-conformance

## What pauses / slows me

The string/regex-matching catch-nets fail in three distinct ways, all of which cost time:

### (a) False positives — the net catches legitimate work
- **timestamp-validator misfire**: fired **38 false-positive signals over 21 days**
  because the catch-net's comparator (mtime) was structurally wrong
  (`feedback_audit_vs_writethrough`, 2026-05-27 exemplar). Three weeks of noise from one
  bad comparator.
- **CHECK 4 over-fire**: the autonomy hook's `unless.*prefer` pattern was blocking the
  **required** recommendation-with-reveal form (`"unless you'd prefer B because…"`) —
  i.e., the hook was penalizing the exact decisioning-discipline behavior another rule
  mandates. Caught and patched only as a *"side fix"* discovered during CHECK 6 test
  design (`SIG-2026-05-28-stop-hook-check-6` §"Side fix").

### (b) False negatives — the net misses real drift until a later patch
- The **trailing-observation-after-proposal** drift class slipped past CHECKs 1–5 and
  was only closed by CHECK 6. CHECK 5's signal explicitly logged a **"residual gap"**
  (incident #3) before CHECK 6 existed. The net is always one variant behind.

### (c) Conformance tax — the human must phrase prose to match the regex
- `feedback_closure_dod_literal_terms`: signal frontmatter must use the **literal
  colon-form keys** `upstream_control_path:` / `catch_mechanism:` / `pipeline_survival:`
  or the hook won't recognize a legitimate closure. The *human conforms to the regex*,
  not the regex to the human. That inversion is the smell.

## The principle being violated

`feedback_audit_vs_writethrough`: *"Audit is catch-net, write-through is primary fix."*
A brittle catch-net is worse than none — it manufactures false signal (a), erodes trust
so the real net gets ignored (b), and imposes a phrasing tax that shapes behavior toward
the matcher rather than the goal (c). The 2026-05-27 exemplar's own lesson: *"when an
audit keeps firing despite a working upstream fix, suspect the catch-net before
concluding upstream is incomplete."*

## Why it's a road-readiness blocker

A shippable framework cannot rely on catch-nets that (a) cry wolf for 3 weeks, (b)
silently miss the next variant, and (c) require operators to learn the matcher's literal
vocabulary. Brittle string-matching as a discipline substrate does not survive contact
with a second operator.

## Investigation / operationalization direction

1. **Classify every active catch-net as semantic vs lexical.** Lexical matchers get a
   mandatory FP-rate SLO and a review cadence; ones over budget get rewritten or retired.
2. **Replace conformance-by-literal-string with structured emission.** Closure assertions
   should be a typed field the writer fills (or a tool emits), not prose the human must
   shape to satisfy a grep. (Ties to `feedback_subagent_claim_vs_execute`:
   `verification_command:` as a structured field, not free text.)
3. **Add a "catch-net health" check to friction-00's Drag dashboard**: per-net fire rate,
   FP rate, age-since-last-true-positive. A net with high fire + zero true positives is a
   net to kill.
4. **Make false-positive cost symmetric with false-negative cost** in any future matcher
   design — today only missed drift is penalized, so every net is tuned to over-fire.

## Open

- Which existing nets are already over their FP budget on day one? (timestamp-validator
  was; audit the rest before declaring any net "installed" — see
  `feedback_invariant_zero_violation_start`.)

## Triage, 2026-07-08

Disposition: still pending. Checked the specific operationalization item most likely to have landed, replacing literal-string conformance with a structured field, directly in tools/closure_writeboundary_check.py: REQUIRED_FIELDS is still a literal string list (upstream_control_path:, catch_mechanism:), unchanged from what this signal describes as the conformance-tax smell. No catch-net health check (per-net fire rate, FP rate, age-since-last-true-positive) has been added to the friction-00 Drag dashboard beyond the per-CHECK Stop-hook counts it already tracks. Needed control: the four operationalization items (classify nets semantic vs lexical with an FP-rate SLO, replace literal-string closure fields with structured emission, add catch-net health to the Drag dashboard, make FP cost symmetric with FN cost) remain unbuilt.
