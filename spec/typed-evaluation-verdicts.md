---
title: Typed Evaluation Verdicts
type: spec
maturity: active
confidentiality: shareable
reusability: universal
created: 2026-06-09
updated: 2026-06-09
purpose: Addendum to event-catalog.md — types every observation.evaluated verdict by criterion provenance so same-frame (self-graded) evaluation is structurally visible and cannot close specs at acceptance authority.
amends: spec/event-catalog.md (LLM-as-Judge Protocol, observation.evaluated)
informed_by:
  - Core/products/parallax/research/2026-06-09-three-vantage-testing-grounding.md
  - Core/products/parallax/research/2026-06-09-test-uat-eval-triad.md
---

# Typed Evaluation Verdicts

> Addendum to `event-catalog.md`. Effective 2026-06-09. Every `observation.evaluated` verdict now carries a type; the type determines what the verdict is allowed to do.

## 1. The flaw this fixes (P0 same-frame evaluation)

The Observe loop's LLM-as-Judge protocol, as originally specified (2026-04-13, 12-factor integration), hands an in-repo judge — same model lineage as the builder, running inside the producing repo — the spec's **own prose criteria** and asks "is the spec satisfied?" The verdict then flows into the closure path: `pass` → "spec marked complete, no further action."

That is the **P0 same-frame failure mode**: a second camera placed at the same coordinate as the first. The judge cannot see author-frame pathologies because it is grading inside the author's frame, against the author's rubric, with the author's lineage. The grounding analysis (`2026-06-09-three-vantage-testing-grounding.md` §headline gap) identified this as the highest-leverage change in the stack — and noted it propagates to **every product that adopts `.intent/`**, not just this repo.

The five-lens triad analysis (`2026-06-09-test-uat-eval-triad.md` §6) sharpened the diagnosis: this is a **TYPING flaw**, not a test/eval/UAT flaw —

> an eval-pattern implementation operating at test-grade displacement (`criteria_origin: self`, same lineage) while its verdicts are consumed at UAT-grade authority.

Three properties were conflated into one event:

| Property | What the Observe judge actually is | What its verdict was treated as |
|----------|-----------------------------------|--------------------------------|
| Mechanism | eval (LLM judge, sampled, semantic) | eval |
| Displacement | test-grade (builder's own criteria, same lineage, same repo) | — (invisible) |
| Consumption authority | — (unstated) | UAT-grade (closes the spec) |

The fix is **not** to delete the judge. A same-frame fuzzy judge is *legitimate* as a cheap inner-loop instrument — a fuzzy test that catches semantic regressions before anything expensive runs — once it is **labeled as the fuzzy test it is**. The fix is to make the displacement label honest and structurally load-bearing: type the verdict, and let the type gate what the verdict may be consumed for.

## 2. The verdict type tuple

Displacement is a property of the **criterion's provenance** (who authored the expected values), not of the oracle's mechanism. Every verdict carries a type (triad §1; this generalizes Gauntlet's `(verdict, independence_level, disconfirmation_attempt)` triple):

```
verdict := {
  criteria_origin:  self | distilled | derived     # the load-bearing field
  lineage:          same-model | foreign
  repeatability:    deterministic | sampled | episodic
  renegotiable_by_generator: yes | no
  stakes:           advisory | gate | constitution
  question_class:   verification ("thing right") | validation ("right thing")
}
```

Field semantics:

- **`criteria_origin`** — who authored the expected values the judge graded against.
  - `self`: the spec's own prose criteria; the builder grading the builder's work against the builder's rubric. Zero displacement regardless of architecture diagram.
  - `distilled`: criteria compiled by the builder from external evidence (UAT incidents, judge-calibration labels, user reports). Partial displacement — every distillation step re-injects builder interpretation (the conveyor's displacement-laundering problem, triad §3.3), so `distilled` is *not* sufficient for closure.
  - `derived`: an exterior judge derived its own criteria from the artifact's claims without reading the builder's rubric (the Gauntlet derive-own-criteria pattern). This is the only origin that detects author-frame pathologies.
- **`lineage`** — whether the judge shares model lineage with the generator. Same-lineage error correlation is empirical, never zero (Knight–Leveson).
- **`repeatability`** — deterministic predicate, sampled LLM verdict, or episodic human encounter. Governs how the verdict may be cached and re-spent.
- **`renegotiable_by_generator`** — whether the agent being judged can edit the criteria that constrain it. A test the generator can rewrite is not a test.
- **`stakes`** — advisory (routes attention), gate (blocks progress), constitution (conservation law; ablatable only by deliberate human act).
- **`question_class`** — verification (built the thing right) vs validation (built the right thing). UAT-type authority attaches to validation questions only.

**Event-catalog binding (the REQUIRED subset).** Three fields are required on every `observation.evaluated` event: `criteria_origin`, `evaluator_model`, `evaluator_repo`. (`evaluator_repo: same-repo|external` is the event-level projection of `lineage` + frame; the full tuple is the analytical model, the three required fields are the minimum that makes same-frame grading structurally visible and rejectable.) An event missing any required field is schema-invalid and its verdict carries no authority.

## 3. The consumption rule (normative)

> A verdict with `criteria_origin: self` **MUST NOT** close a spec at acceptance authority. It may serve as an inner-loop instrument only. Closure on the basis of an `observation.evaluated` verdict requires `criteria_origin: derived`, OR an explicitly recorded Brien override (a `decision.recorded` event referencing the verdict and stating the override).

Consumption authority by origin:

| `criteria_origin` | May do | May NOT do |
|---|---|---|
| `self` | Route rework, gate cheap inner-loop iteration, emit gap signals to Notice | Close a spec; mark complete-with-caveats; satisfy any acceptance criterion |
| `distilled` | Everything `self` may, plus serve as gate-stakes evidence inside the loop | Close a spec on its own authority |
| `derived` | Close a spec at acceptance authority (subject to the spec's own gates) | — |
| any + recorded Brien override | Close a spec (the override, not the verdict, carries the authority; the `decision.recorded` event is the record) | — |

This is GA-006 generalized (triad §6): uncalibrated semantic judges must not occupy gate positions. Self-graded judges are routed to triage queues and recorded deltas — never to closure.

## 4. Migration

**Grandfathering, not deletion.** Every `observation.evaluated` event emitted before 2026-06-09 lacks the required fields. These events are **grandfathered as `criteria_origin: self`** (the honest default — they were all in-repo judges grading builder-authored criteria with builder lineage) and are thereby **visibly demoted, not deleted**:

- Historical events remain in `.intent/events/events.jsonl` untouched (append-only; no rewriting history).
- Any consumer reading a pre-amendment `observation.evaluated` event MUST treat it as `criteria_origin: self` / `evaluator_repo: same-repo` and apply the consumption rule accordingly: its verdict is inner-loop information, not acceptance evidence.
- Specs previously marked complete on the strength of a self-graded `pass` are **not** reopened by this amendment. Their closure record now visibly rests on a demoted verdict type — which is the correct, honest state. Reopening (if warranted) is a per-spec judgment surfaced through normal signal flow, not a mechanical cascade.
- New emitters MUST populate all three required fields from 2026-06-09 forward. The manual-emission escape hatch (event-catalog §Emission Mechanisms 7) is not exempt.

This is the demote-don't-flatten pattern: the historical record keeps its full content, gains an honest type label, and loses only the authority it never legitimately had.

## 5. Enforcement path (the catch-net)

Write-through control is primary; the audit is the safety net (`feedback_audit_vs_writethrough` discipline).

**Primary (write-through):** the LLM-as-Judge protocol itself, as amended in `event-catalog.md` — emitters populate the required fields at emission time, and the Observe-loop integration steps refuse closure on a `self` pass.

**Catch-net (BUILT 2026-07-02):** `INV-INTENT-NO-SELF-GRADED-CLOSURE` — implemented at `tools/typed_verdict_invariants.py` with RED-first suite `tools/test_typed_verdict_invariants.py` (15 tests, green). It uses the **repo-local route**: the portfolio-level audit (`Core/products/library-index/chain_audit_portfolio.py`, `INV-LI-*` pattern) is not present in this checkout, so the invariant is stood up local to `frameworks/intent` per the alternative named here. Run `python3 tools/typed_verdict_invariants.py` (exit 0 = clean). The invariant asserts:

> For every spec whose status transitions to closed/complete on or after 2026-06-09 with an `observation.evaluated` event in its trace: the closing verdict has `criteria_origin: derived`, OR a `decision.recorded` event exists referencing that verdict as a Brien override. Additionally, every `observation.evaluated` event emitted on or after 2026-06-09 carries all three required fields.

**Zero-violation-start discipline applies** (`feedback_invariant_zero_violation_start`): the invariant must fire zero violations against existing state on day one before the catch-net counts as installed. It does so by construction — the date predicate scopes it to post-amendment closures and post-amendment emissions; grandfathered events are typed `self` by rule but are attached to pre-amendment closures, which the invariant does not judge. If a day-one run fires on existing state, the invariant's comparator is wrong, not the corpus.

**Why the existing hook family does not already catch this:** the closure-discipline hooks (`hooks/closure-discipline-check.sh`, `closure-discipline-signal-check.sh`, `closure-discipline-stop-check.sh`; spec `closure-discipline-enforcement.md`) match literal frontmatter keys on *signal* files (`upstream_control_path:`, `catch_mechanism:`, `pipeline_survival:`). They enforce that closures name their upstream control — they do not inspect `observation.evaluated` event payloads or verdict types in `events.jsonl`. The nearest existing control is therefore adjacent, not covering; the chain_audit invariant is the genuine catch-net and is named here so its absence is a tracked gap, not a silent one.

## 6. Scope of propagation

This amendment is defined in Intent's event catalog and therefore applies to every repo that adopts the `.intent/` scaffold and emits `observation.evaluated`. Products with their own judge implementations (Gauntlet adjudication, Voices panel verdicts) already carry stronger typing (`independence_level`, named dissents) and are unaffected except insofar as they emit into an `.intent/` event stream — in which case the three required fields apply at the emission boundary.

## 7. Traceability

- Amends: `spec/event-catalog.md` §LLM-as-Judge Protocol (dated note in the catalog header blockquote, 2026-06-09)
- Diagnosis: `Core/products/parallax/research/2026-06-09-test-uat-eval-triad.md` §1 (verdict type tuple), §6 (typing-flaw restatement)
- Grounding: `Core/products/parallax/research/2026-06-09-three-vantage-testing-grounding.md` (headline gap; required-fields fix)
- Signal: `.intent/signals/SIG-2026-06-09-typed-evaluation-verdicts.md`
- Catch-net (built 2026-07-02): `INV-INTENT-NO-SELF-GRADED-CLOSURE` → `tools/typed_verdict_invariants.py` (+ `tools/test_typed_verdict_invariants.py`), repo-local route, zero-violation on day one


## 8. Composing several verdicts over one artifact (candidate, added 2026-09-16)

Sections 1 to 7 type a **single** verdict and govern what that one verdict may be consumed
for. They say nothing about what happens when several verdicts land on the same artifact.
Every live aggregation in the tree today is strict AND: the CON-COH contract family runs five
machine-assertable contracts over one corpus and the run record reads "FAIL, 1 violation"
even when four of five passed everywhere
(`/Users/brien/Workspaces/Core/frameworks/coherence-engineering/contracts/runs/CON-COH-005-first-run-2026-06-10.md`).
That gives the corpus one bit and no way to say which of two failing documents is closer to
good, which is the question a repair pass actually needs.

**Candidate rule.** Given `M` binary verdicts `v[1..M]` over one artifact from judges sharing
a `criteria_origin`, aggregate as the mean of the verdicts raised to the power of the check
count:

```
r = ( (1/M) * sum_m v[m] ) ^ M
```

With `M = 5`: five of five gives 1.000, four of five gives 0.328, three of five gives 0.078,
zero of five gives 0.000.

Two properties are why this is preferred to a minimum or a plain mean.

1. **It stays positive until every check fails**, so imperfect candidates remain orderable.
   Strict AND returns zero for four-of-five and three-of-five alike and destroys the ranking,
   which is fatal wherever the comparator's job includes ranking the imperfect.
2. **Strictness is derived, not tuned.** The exponent is the number of checks, so widening
   the audit tightens the aggregate automatically. There is no tolerance knob to argue over,
   because tolerance is a consequence of how broadly you decided to audit.

**Consumption authority of a composed verdict.** A composed `r` inherits the **lowest**
`criteria_origin` among its inputs. Five `self` checks compose to a `self` number and are
still barred by section 3 from closing a spec. Composition changes resolution, never
authority.

**Status: candidate, not normative.** It becomes normative only after this falsification
test passes: score the CON-COH corpus run three ways (strict AND, plain mean, power-mean),
hand-label a sample of 30 files by how much repair each actually needs, and check whether the
power-mean ordering correlates better with the labels than the plain mean without collapsing
into strict AND's one-bit partition. If it does not, this section is withdrawn.

**Provenance.** Borrowed from the CLR (Claim-Level Reliability Assessment) stage of
VibeThinker-3B, arXiv 2606.16140v1, where `M = 5` claims are extracted per trajectory and
reliability-weighted clustering over `K = 32` trajectories buys 2.7 to 6.1 benchmark points
with zero added parameters. Source record:
`raw/research/2026-09-16-vibethinker-3b-verifiable-reasoning.md`. Mapping, rejected
alternatives, and the rest of the disposition:
`knowledge/design-rationale/RAT-004-verifier-at-the-seam.md`. Captured via intake issue
https://github.com/theparlor/intake/issues/18.
