---
title: "Projection Divergence: the differential amplifier for intent"
id: SPEC-INTENT-PROJECTION-DIVERGENCE-001
type: spec
status: terminal
maturity: draft
confidentiality: internal
reusability: universal
created: 2026-09-16
plane: bridge
author: intent framework (host-pickup wave, intake issue 12)
parent: spec/work-ontology.md
lineage:
  - https://github.com/theparlor/intake/issues/12
related:
  - spec/work-ontology.md (the gradient this operator runs on: Signal, Intent, Spec, Contract)
  - spec/typed-evaluation-verdicts.md (criteria_origin, lineage, question_class: the evidence rules)
  - spec/signal-amplification.md (amplification_score and effective_trust: the nudge substrate)
  - spec/closure-discipline-enforcement.md (the one comparator of this family already in production)
  - spec/SPEC-INTENT-SEAM-DECOMPOSITION-001.md (seam as the unit; only the Tower re-cuts a seam)
  - spec/signal-stream.md (closure DoD triad)
  - reference/goal-command-and-eval-prd-analysis.md (verified provenance and mechanism ground truth)
  - Core/products/gauntlet/INTENT.md (cross-line comparator: independent disconfirmation)
  - Core/products/gauge/README.md (below-the-line comparator: cited, deterministic conformance)
  - Core/products/understudy/spec/2026-06-04-v1-fieldbook-slice-design.md (calibration corpus)
  - Core/frameworks/coherence-engineering/README.md (sibling discipline; its drift detector is the producer-side twin of this one)
---
# Projection Divergence

> One sentence: an operator that measures what a spec loses on its way down to a checkable
> contract, rejects the part that survived faithfully, amplifies the part that did not, and
> hands back a higher-fidelity spec instead of a longer one.

**Status:** `draft` (the design is settled; the tolerances are not) · **Created:** 2026-09-16

---

## 0. Plain language first

**What this is.** When you write down what you want, and then write down a test for it, the
test is never the whole of what you wanted. Something always falls out between the two. This
operator is an instrument for measuring exactly what fell out, and for feeding that back into
the thing you wrote down, so the next version says more of what you actually meant.

**Why it matters.** There is a fashionable claim going around that "evals are the new PRD",
meaning the test replaces the document. It is half a sentence. The full sentence is: the test
is the verification half of the document, and the meaning half just got more valuable, not
less. When a machine executes the literal words instead of a colleague interpreting the
intent, the cost of a vague document goes up, not down. The risk did not disappear when
"done" became mechanical. It moved up one floor, from "did we build it right" to "was that
the right line to draw".

**What changes for anyone doing the work.** Three things.

1. You stop treating a finish line as a replacement for the reason. You keep both, and you
   keep a named measurement of the gap between them.
2. You spend your expensive judgment at one specific place: the seam where prose becomes a
   predicate. That is the only seam where a test can be perfectly satisfied while the point
   is entirely missed. Everywhere else, a cheap deterministic check is the right instrument.
3. When the gap gets big enough, it becomes a Signal in the ordinary way, and follows the
   ordinary path. There is no new filing system and no new vocabulary to learn.

**What this is not.** It is not a new product, and it does not get a product name. Naming is
gated by the ecosystem taxonomy and brand program; this is a framework operator inside
Intent, sitting beside seam decomposition and typed evaluation verdicts, and it reuses their
machinery rather than standing up its own.

---

## 1. Intent

### What I noticed

Claude Code shipped `/goal`, which makes "done" mechanical: one model works and prints
evidence into the transcript, and a separate, cheaper model reads only that transcript and
rules on one binary. The vendor documentation is explicit that the evaluator "does not call
tools, so it can only judge what Claude has already surfaced in the conversation"
(verified 2026-09-16; see `reference/goal-command-and-eval-prd-analysis.md`). OpenAI shipped
the same command two weeks earlier and reached the **opposite** default on who declares done:
the model decides, with user evaluators optional.

Two vendors, opposite defaults, within a fortnight. That is not settled wisdom. That is a
live design axis, and it is the same axis Intent already governs with L0 to L4 autonomy
gating and with `criteria_origin` in `spec/typed-evaluation-verdicts.md`.

What I noticed underneath the news: the popular reading of this is **substitution** (the eval
replaces the PRD). The load-bearing reading is **opposition**. A spec and a contract are two
projections of the same intent, one onto the axis of meaning and one onto the axis of
checkability. Neither projection is the whole object, and the difference between them is not
noise. It is the highest-value telemetry in the loop, and nothing currently reads it.

### Why it matters now

Intent's work ontology already names the exact transition where this happens. Level 3 is
Spec, "narrative plus acceptance criteria". Level 4 is Contract, "the spec's acceptance
criteria extracted and made machine-executable". The ontology has always described that
transition as an extraction. An extraction has a residue, and the residue has never been
measured. Every spec that has passed through this repo has thrown some of itself away at
level 3 to level 4, silently.

Meanwhile the cost of a lossy extraction has changed. When a person read the contract, they
also read the spec, and they interpolated. When an agent reads the contract, the contract is
all there is. The loss that used to be absorbed by a colleague is now shipped.

And there is already one comparator of exactly this family running in production here, which
is the evidence that this shape works: `closure-discipline-signal-check.sh` blocks a signal
claiming `status: resolved` that does not also carry `upstream_control_path` and
`catch_mechanism`. That hook is a fidelity check across a seam. It reads a claim at one
altitude ("this is resolved") and demands the corresponding content at the altitude below
("here is the mechanism that prevents it"), and it fires a discrete event when the two
diverge. It has caught real drift for five months. This spec generalizes it.

### Desired outcome

A spec that survives the trip down to a contract carries a measured, recorded account of what
it lost on the way, and the loss is fed back as amplification on an existing Signal rather
than as a new document. After this lands, a person looking at a finish line can answer, from
the record and without re-deriving it, the question "what did we want that this does not
check".

---

## 2. Shape

### 2.1 The operator, named

**Projection divergence** is a differential amplifier for intent. It takes one intent
expressed at several altitudes, rejects the **common mode** (what every altitude agrees on,
faithfully rendered), and amplifies the **differential** (what one altitude holds and the
next one drops or distorts).

| | |
|---|---|
| **Inputs** | An intent expressed as an ordered stack of existing work-ontology artifacts: Signal(s), Intent, Spec, Contract. Minimum viable input is two adjacent levels. Plus a per-seam tolerance and gain (section 2.6). |
| **Outputs, discrete** | Comparator crossings, emitted as Signals (and, where the divergence is a governance rule rather than an artifact defect, as DDRs). Ordinary `.intent/signals/` files with the ordinary closure triad. |
| **Outputs, continuous** | Nudges: graded contributions to `amplification_score` on an existing Signal, per `spec/signal-amplification.md`. Not artifacts. Not a new type. See the OQ4 ruling. |
| **Output, structural** | A recomposed Contract of higher fidelity and bounded length (section 2.7). |
| **Runs on** | The Spec plane primarily; a deferred instance runs on the Observe plane (section 2.9). |

### 2.2 The gradient is the work ontology, not a document taxonomy

The handoff that seeded this spec described the gradient as BRD, then PRD, then FRD plus TRD.
Those are waterfall document types. In a post-SAFe or LeSS room that vocabulary triggers a
form allergy and the substance gets thrown out with it. It is also a second taxonomy for
something this repo already has.

**Ruling: the gradient is levels 1 to 4 of `spec/work-ontology.md`.** No new layer names are
minted. The legacy labels appear once, here, as a crosswalk for anyone arriving from a
requirements-document world, and nowhere else.

| Ontology level | What it holds | Axis | Legacy label, crosswalk only |
|---|---|---|---|
| 1. Signal | Raw observation. Why anyone is looking at this. | meaning | (raw input, no document equivalent) |
| 2. Intent | The declared change and its business outcome. | meaning | BRD |
| 3. Spec | Product and user intent, narrative plus criteria. | meaning, partly checkable | PRD |
| 4. Contract | Verifiable assertions. The finish line. | checkability | FRD plus TRD |

The gradient is an **axis**, not a filing scheme. A single artifact can sit at two levels at
once; what matters is the projection, not the file.

### 2.3 The checkability line, and why there is exactly one Goodhart seam

There are three seams in a four-level stack, and they are not alike. One line runs through
the stack: the boundary between prose that means something and a predicate a machine can run.
It sits at exactly one place, between Spec and Contract.

| Seam | Question it asks | Class | Instrument |
|---|---|---|---|
| S1 Signal to Intent | Is this still the right thing to want? | **target** | human, or foreign-lineage panel |
| S2 Intent to Spec | Does this shape serve that declared change? | **target** | foreign-lineage judgment |
| S3 Spec to Contract | Does this predicate check what that prose meant? | **fidelity** | foreign-lineage judgment, Gauntlet-class |
| S4 within Contract, and Contract to Capability | Are these assertions mutually consistent and satisfied? | **consistency** | deterministic, cheap, Gauge-class |

**Goodhart and surrogation can only be caught at S3.** S4 cannot see it: every assertion can
be internally consistent and jointly satisfied while the prose they were extracted from meant
something else entirely. S1 and S2 cannot see it either: they are above the line and never
look at the predicate. S3 is the only seam that spans the meaning axis, and therefore the only
one where "the test is satisfiable while the point is missed" is a detectable state.

This is why routing by seam is the whole economic argument. **Spend on S3.** Everything below
the line is a cheap deterministic consistency check and should be bought at Ollama-class or
Gauge-class cost. Everything above the line is expensive judgment but is asked rarely, at
intent-revision cadence rather than per-turn.

The evidence for why S3 needs a *foreign* instrument, not just a cheaper one: Kohli, "Nine
Judges, Two Effective Votes" (Apple Machine Learning Research, June 2026) finds that nine
frontier judges drawn from seven model families supply about two independent votes' worth of
information, because the models make the same mistakes on the same items. Correlated error
survives across families, not merely within one. Intent's `typed-evaluation-verdicts.md`
already cites Knight and Leveson (1986) for the same phenomenon in N-version programming; the
Apple result is its LLM-era replication. Buying a cheaper same-family judge does not buy a
small discount on the same instrument. It moves you along a curve where, per "Mind the Gap"
(arXiv 2412.02674), the generator-verifier gap widens as the generator gets stronger.

### 2.4 The builder and judge split, applied to the operator itself

The operator has the same split it studies, and must not be exempt from it.

- The **recomposer is a builder**. It writes the next Contract.
- The **comparators are judges**. They read two adjacent projections and rule.
- They may not be the same model instance, and at S3 they may not be the same lineage.
- The recomposer **may not edit a comparator's tolerance or gain**. This is
  `renegotiable_by_generator: no` from `typed-evaluation-verdicts.md`, applied one level up:
  a test the generator can rewrite is not a test, and an amplifier that can turn down its own
  gain is not an amplifier.
- A seam's boundary may not be moved by the agent working inside it. Re-cutting a seam is a
  Tower act, per `SPEC-INTENT-SEAM-DECOMPOSITION-001` clause 3.

### 2.5 Evidence rules

These are binding. They are mostly restatements of `typed-evaluation-verdicts.md` scoped to
this operator, which is the point: no new evidence vocabulary.

- **E1. Name what you read.** A comparator verdict is admissible only if it names the exact
  text spans, on both sides of the seam, that it compared. A verdict without a diff is a null
  verdict, not a pass.
- **E2. Declare the evidence window.** Every comparator declares what it could see. A
  transcript-scoped comparator may not make a claim about anything outside the transcript.
  This is the constraint that makes `/goal` honest and it is inherited here verbatim.
- **E3. Type every verdict.** `criteria_origin`, `lineage`, `question_class` per
  `typed-evaluation-verdicts.md`, and the existing consumption rule applies unchanged: a
  `criteria_origin: self` verdict may route rework and emit nudges, and may not close a seam.
- **E4. S3 requires foreign lineage.** A same-lineage panel is not a substitute for a foreign
  judge; see the Kohli finding in 2.3. `criteria_origin: derived` is required at S3, meaning
  the judge derives its own criteria from the artifact's claims rather than reading the
  builder's rubric.
- **E5. Intention earns nothing.** Inherited from the `/goal` design and from Gauntlet's
  conservation law. A claim that a seam is faithful, unaccompanied by the attempt to show it
  is not, is inadmissible.
- **E6. Nudges are not evidence.** A nudge accumulates; it never supports a conclusion on its
  own. Only a comparator crossing produces a record that anything downstream may cite.

### 2.6 Common mode, defined by round trip

The amplifier is only meaningful if "faithfully rendered" has an operational definition.
Here is one that runs.

**Take the lower projection alone. Re-express it upward without reading the upper text.
Diff the reconstruction against the actual upper text.**

- What **matches** is common mode. Rejected. The intent survived the seam.
- What appears **only in the upper text** is dropped intent. Positive differential. This is
  the loss everyone expects.
- What appears **only in the reconstruction** is invented intent. Negative differential, and
  it is the more dangerous sign, because it means the contract has grown a requirement the
  spec never asked for. Surrogation starts here: the measure has begun to be the construct.

This is the round-trip test from machine translation, and it has the property the operator
needs: it does not require a rubric, so it does not re-inject the author's frame the way a
rubric-driven check does.

Tolerance is per seam and is compared against the summed magnitude of the differential.
**The tolerances and the gain function are not set in this spec** (see OQ6, parked with a
named unblocking condition).

### 2.7 Recompose, and the damping that keeps it from eating itself

Decompose and recompose are not inverses. Comparators and the amplifier fire in between, so
recompose yields a higher-fidelity Contract than decompose consumed. That gain is the point.

An amplifier with gain and no negative feedback saturates or oscillates. Without a settling
criterion, every divergence recomposes a richer Contract, and the ten-page PRD regrows through
the operator's own loop. Four damping terms, all of which must hold:

1. **Fixpoint.** Settle when a full decompose-and-compare pass produces zero comparator
   crossings and the summed differential at every seam is inside tolerance.
2. **Monotonic decrease.** Each pass must strictly reduce the total differential. A pass that
   does not is oscillation, not convergence: abort and escalate to a human. Gain without
   negative feedback is a feedback squeal.
3. **Depth cap.** Passes are capped at the number of seams. Past that the operator is
   implicitly re-cutting seams, which it is not allowed to do (2.4).
4. **No unattributed growth.** The recomposed Contract may not add an assertion that does not
   carry the id of the comparator crossing that produced it. Every new line traces to a
   measured loss or it does not land. This is the direct, mechanical answer to spec
   reinflation.

Prior art, verified rather than asserted: Claude Code's own `/goal` loop ships two of these.
It stops when the agent keeps answering the evaluator "without making progress (no tool use
for several turns in a row)", which is a progress predicate, and it backs off check-ins by
doubling up to four times the first interval. It also carries a third verdict the June
capture missed: **impossible**. An evaluator that can rule a finish line unreachable, clear
the goal and record a failure is an evaluator with a small amount of upward critique already
in it. That verdict is the seed of S3 inside the vendor's own loop, and it is the strongest
available evidence that the two-projection architecture is incomplete without it.

### 2.8 Reuse map: nothing new gets built

| Operator part | Existing implement | Why it fits |
|---|---|---|
| S4 consistency comparator | **Gauge** (`Core/products/gauge/`) | Citation-or-no-finding, Class A invariant rules, determinism as a per-class promise. Exactly a below-the-line deterministic check. |
| S3 fidelity comparator | **Gauntlet** (`Core/products/gauntlet/`) | Conservation law: a verdict without a genuine disconfirmation attempt is invalid. Independence ladder. Derive-own-criteria. This is the Vantage-C instrument and the only one that earns `criteria_origin: derived`. Its published disconfirmation-contract is the shape an S3 comparator input takes. |
| S1 and S2 target comparators | **Voices** panel, or a human | Target selection is a validation question; per `typed-evaluation-verdicts.md` only validation questions carry UAT-grade authority. |
| Tolerance calibration corpus | **Understudy** (`Core/products/understudy/`) | Golden data with a conservation law of the same family (no identifier crosses the boundary; every join survives it). This is what OQ6 needs and does not yet have. |
| Nudge accumulation and promotion | **`spec/signal-amplification.md`** | `amplification_score`, `effective_trust`, and an existing autonomy-boundary-crossing trigger table. The analog-to-digital promotion path is already specified. |
| Discrete output | **`.intent/signals/`** plus the closure triad | No new artifact type. |
| Verdict typing | **`spec/typed-evaluation-verdicts.md`** | No new evidence vocabulary. |
| Seam ownership and freeze | **`SPEC-INTENT-SEAM-DECOMPOSITION-001`** | Seams already exist as a first-class unit with an owner. |

### 2.9 Where it sits in Notice, Spec, Execute, Observe

- **Notice.** Consumes Signals as the qualitative end of the gradient. Emits Signals as
  comparator output. Net: Notice is both the operator's floor and its sink.
- **Spec.** The primary seat. The operator runs between the Spec and Contract levels of the
  work ontology, before Execute begins. This is the double loop made physical, in Argyris's
  sense: the single loop hits the finish line, and this pass asks whether the finish line
  encoded the right intent.
- **Execute.** Does not run. Execute consumes a recomposed Contract and nothing else. An
  operator that ran during Execute would be re-cutting a frozen seam.
- **Observe.** A **deferred instance** runs here, on the outcome lag (see the OQ2 ruling).
  Observe is also the telemetry sink: comparator verdicts land as `observation.evaluated`
  events carrying the three required fields from `typed-evaluation-verdicts.md`.

### 2.10 Relation to the closure-discipline DoD triad

`spec/signal-stream.md` requires that a signal claiming `status: resolved` carry
`upstream_control_path` and `catch_mechanism`, and this repo's wave convention adds
`verification_command`. Two things follow, and the second is the load-bearing one.

**First, this operator's own signals obey the triad like any other.** No exemption.

**Second, the triad is itself a three-level projection stack of exactly this shape**, and the
closure hook is already a comparator running at S3 in production:

| Triad key | Projection level | Axis |
|---|---|---|
| `upstream_control_path` | why this cannot recur | meaning |
| `catch_mechanism` | what detects a regression | functional |
| `verification_command` | the predicate that proves the state | checkability |

`closure-discipline-signal-check.sh` blocks a `resolved` claim that has the top of that stack
without the bottom. That is a fidelity comparator with a tolerance of zero and a binary gain,
firing a discrete event at a seam. It has been in production since May 2026 and it works. The
operator in this spec is that hook generalized from one hard-coded seam to the whole stack,
with a graded output added alongside the binary one.

That is the argument for placing this in Intent rather than anywhere else: the mechanism is
already here, running, in a special case.

### 2.11 Boundaries

**In:** the gradient definition on the existing work ontology; the seam classification and the
checkability line; the comparator and amplifier split; the evidence rules; common mode by
round trip; the damping terms; the reuse map; the placement in the loop.

**Out:**
- Tolerance values and the gain function (OQ6). Parked with a named unblocking condition.
- Any new artifact type, filing location, vocabulary, or product name.
- The implementation. This spec routes every part to an existing implement; a build spec, if
  one is ever written, is a separate document.
- **Producer-side drift.** Coherence engineering owns the question of whether the outputs of
  several independent producers compose. That is a different axis and its drift detector,
  named as not-yet-built in that framework's README, remains distinct from this one. This
  operator scans one intent across altitudes; that one scans many producers across a surface.
  They are siblings, they are not the same instrument, and neither is a parent of the other.

### 2.12 Key decisions

1. **Owning framework: Intent.** The operator's inputs are work-ontology levels 1 to 4, its
   discrete outputs are Signals and DDRs, its evidence rules are Intent's typed verdicts, its
   nudge substrate is Intent's amplification model, and its production ancestor is an Intent
   hook. Coherence engineering is the discipline within which Intent operates and is
   cross-referenced, not the home.
2. **No new taxonomy.** The BRD, PRD, FRD, TRD stack is dropped in favour of the existing
   ontology. The crosswalk in 2.2 exists so the idea is legible to people arriving from a
   requirements-document world, and appears nowhere else.
3. **No new artifact type for nudges.** See the OQ4 ruling.
4. **No product name.** Gated by the ecosystem taxonomy and brand program.
5. **One Goodhart seam.** S3 is the only seam that spans the meaning axis, so it is the only
   place cross-seam spend is justified and the only place surrogation is detectable.
6. **The reframe is adopted as canon.** "Evals are the new PRD" is half a sentence. The full
   sentence: **evals are the PRD's verification half, and the intent half got more valuable,
   not less.**

### 2.13 Prior art, cited and not claimed

- **Chris Argyris, double-loop learning.** The decompose, compare, reconcile, recompose cycle
  is the double loop made physical. The single loop hits the finish line; the double loop asks
  whether the finish line was right.
- **Stafford Beer, VSM.** Variety attenuators and amplifiers; recursion bounded by a governing
  system. The damping terms in 2.7 are the negative feedback a viable system requires.
- **Willie Choi, Gary Hecht, William B. Tayler**, on surrogation (The Accounting Review 2012;
  Journal of Accounting Research 2013). Surrogation is strongest under a **single** measure and
  is mitigated by involvement in choosing the strategy. This is experimental evidence, not
  analogy, and it drives the OQ8 ruling.
- **Goodhart (1975), Strathern (1997).** The measure-becomes-target formulation.
- **Guneet Kohli**, "Nine Judges, Two Effective Votes", Apple ML Research, June 2026
  (arXiv 2605.29800); **"Mind the Gap"**, arXiv 2412.02674; **Knight and Leveson (1986)**.
  The correlated-error case against same-lineage judging.
- **Round-trip translation** as a rubric-free fidelity test.
- **Claude Code `/goal`** and **Codex CLI `/goal`**, as two opposed industrial answers to the
  who-declares-done question, verified in
  `reference/goal-command-and-eval-prd-analysis.md`.
- **Aakash Gupta** as amplifier and framer of the PM-facing version of this discourse. The
  "evals are the new PRD" phrase is the title of his interview with Ankur Goyal of Braintrust;
  the welding of that phrase to the `/goal` mechanism was done in the June capture session,
  not by Aakash, and is attributed accordingly.

---

## 3. Contract

### Done when

- [x] The operator's inputs, outputs, seams, comparator classes, evidence rules, builder and
      judge split, damping terms, and loop placement are stated in one document.
- [x] Every part of the operator routes to an implement that already exists, or is explicitly
      parked with its unblocking condition. Zero new artifact types.
- [x] Every open question from the seeding handoff carries a ruling or an honest park with a
      named unblocking condition (section 4).
- [x] Both academic load-bearers carry named citations, and all four truncated source links
      are resolved or marked, in `reference/goal-command-and-eval-prd-analysis.md`.
- [x] The artifact is reachable from the framework's registration surfaces (`spec/README.md`,
      `reference/external-patterns-index.md`, `reference/corpus/aakash-gupta/README.md`).
- [ ] **Not done, and honestly so:** tolerances and gain are uncalibrated, so the operator is
      specified and not yet runnable. See OQ6.

### Smoke test

The operator's first runnable instance already exists as a special case, and this command
proves the ancestor is live:

```bash
grep -n "upstream_control_path\|catch_mechanism" \
  /Users/brien/Workspaces/Core/frameworks/intent/hooks/closure-discipline-signal-check.sh
```

Non-zero output means the production S3-with-tolerance-zero comparator described in 2.10 is
on disk. Reachability of this spec itself:

```bash
grep -rn "SPEC-INTENT-PROJECTION-DIVERGENCE-001" \
  /Users/brien/Workspaces/Core/frameworks/intent/spec/README.md \
  /Users/brien/Workspaces/Core/frameworks/intent/reference/external-patterns-index.md
```

### Failure modes to watch

- **Amplifier squeal.** Recompose grows the Contract every pass and the ten-page PRD regrows.
  Caught by damping terms 2 and 4 in 2.7.
- **Cheap judge at S3.** Somebody routes the fidelity comparator to a same-family small model
  because it is faster. The result is a comparator that catches "did not do what was said" and
  structurally cannot catch "what was said was wrong". Caught by E4.
- **Surrogation of the operator itself.** The differential magnitude becomes a number people
  optimise, and a spec gets written to minimise measured divergence rather than to say what is
  meant. This is the operator Goodharting itself, and it is the failure mode with no mechanical
  catch. It is why 2.7 term 4 requires every new assertion to trace to a crossing: you cannot
  drive the number down by adding text.
- **Taxonomy regrowth.** Somebody reintroduces BRD, PRD, FRD, TRD as directories. Caught by
  reading 2.2 and 2.12 decision 2.
- **Silent seam re-cutting.** The recomposer changes which levels it compares to make the
  numbers settle. Caught by 2.4 and by seam-decomposition clause 3.

### Observability

Comparator verdicts land as `observation.evaluated` events in `.intent/events/events.jsonl`
carrying the three required fields (`criteria_origin`, `evaluator_model`, `evaluator_repo`)
from `typed-evaluation-verdicts.md`. Nudges land as `amplification_score` deltas on existing
signals per `signal-amplification.md`, which already emits `signal.referenced` and
`signal.co_referenced`. No new event type is defined by this spec.

---

## 4. Rulings on the seeding handoff's open questions

Twelve questions arrived with the handoff. Eight are ruled here, one was already resolved,
three are parked with named unblocking conditions. None is dropped.

### OQ1 (was RESOLVED; the sub-question is now ruled)

The divergence detector is an operator, a differential amplifier for intent. **Sub-question:
is it the same primitive as the previously-flagged periodic-retrospective operator, or a
sibling? Ruling: sibling.** They scan the same corpus on orthogonal axes. The retrospective
operator (`reckoning`) reads the signal and decision stream as a **time-ordered sequence** and
surfaces reversals, oscillation and repeat mistakes. This operator reads one intent as an
**altitude-ordered stack** at a single point in time. Same substrate, perpendicular scans,
different failure modes caught. Merging them would produce an instrument that is
under-specified on both axes.

### OQ2 (was PARTIAL; now RULED)

*Can evals ever check outcomes, or are they permanently output-confined? If confined, what
carries outcome verification in Intent, the Observe plane alone?*

**Ruling: evals are not permanently output-confined. They are permanently confined to
admissible evidence, and an outcome becomes admissible only after a lag during which
attribution decays.** The output versus outcome framing is the wrong cut. The real cut is
**same-turn evidence versus deferred evidence**. Three parts:

1. A **transcript-scoped** evaluator, the `/goal` shape, IS structurally output-confined, and
   permanently so. Its evidence window is one session transcript, and no outcome exists inside
   a session. This is not a limitation to be engineered away; it is what makes the instrument
   honest and cheap. Verified from the vendor documentation: it "does not call tools".
2. A **tool-enabled evaluator with a widened evidence window** can check an outcome, but only
   one whose measurement has already landed in a readable substrate: an analytics table, a
   ledger, a ticket count. It is then checking an outcome **proxy at a later timestamp**. Same
   mechanism, different clock. There is no new instrument here, only a deferred one.
3. The cost of deferral is **attribution**, and attribution is a judgment, not a predicate. A
   cheap evaluator cannot make it. So an outcome verdict is a `question_class: validation`
   verdict, and the existing consumption rule in `typed-evaluation-verdicts.md` already
   forbids closing on it with `criteria_origin: self`. The rule needed already exists.

**What carries outcome verification in Intent: not Observe alone, but a three-way split.**
The **Contract** carries the output check, which is the eval. The **Observe plane** carries the
deferred outcome check, and it does so through a second instance of the same contract with a
later `evaluated_at`, not through a different mechanism. The **Intent** level carries the
attribution argument, because the Intent is the artifact that named the outcome in the first
place, and only it records which outcome this change was supposed to move. An outcome claim
that cannot point at an Intent has no attribution and is inadmissible.

### OQ3 (RESOLVED, carried)

Operator design specified. This document is that specification, with the layer taxonomy
replaced by the work ontology and the routing rule restated in terms of one checkability line.

### OQ4 (was OPEN; now RULED)

*Definition of "nudges": telemetry, choice-architecture steering, or an actuator?*

**Ruling: a nudge is not a new artifact type, and the amplifier is telemetry, not an actuator.
A nudge is the amplification contribution of one divergence observation to an existing
Signal's `amplification_score`, exactly as specified in `spec/signal-amplification.md`.**

Intent already has the whole analog half. `signal-amplification.md` defines
`amplification_score`, `effective_trust = min(1.0, base_trust + amplification_score)`,
time-decayed reference weights, and a re-evaluation trigger table keyed to autonomy-boundary
crossings. That IS a continuous, accumulating, low-magnitude directional bias with a
promotion path into discrete action. The handoff's working definition of a nudge and that
model's `amplification_score` are the same object described twice.

So the analog-to-digital promotion path is not something to design; it is the existing table:
L0 to L1 notifies, L1 to L2 auto-enriches, L2 to L3 drafts an intent and spec, L3 to L4 flags
for autonomous execution. A divergence observation adds a weighted, decayed increment. When
the accumulation crosses a boundary, the crossing fires and a discrete record is produced.
**The amplifier never acts on a human directly.** Its output is a number on a signal. The
actuator is whatever the autonomy-crossing trigger already invokes.

Consequence worth stating: the divergence observation is a new **reference source class** in
that model's weight table, alongside signal-to-signal, conversation, commit, and intent/spec
references. Its weight is uncalibrated and belongs to OQ6.

### OQ5 (was OPEN, flagged chain-blocking; now RULED)

*The damping or settling criterion that bounds the decompose-to-recompose recursion.*

**Ruling: four conjunctive terms, stated in full in section 2.7.** Fixpoint (zero crossings,
all seams inside tolerance), monotonic decrease (a pass that does not strictly reduce the total
differential is oscillation and escalates to a human), depth cap (passes bounded by seam
count, because going past it means re-cutting seams), and no unattributed growth (every new
assertion carries the id of the crossing that produced it). Term 4 is the specific answer to
"the spec reinflates": you cannot grow the Contract without a measured loss to point at.

Grounded rather than asserted: Claude Code's `/goal` loop ships a progress predicate and an
exponential check-in backoff, and carries an **impossible** verdict that terminates an
unreachable loop. Verified in `reference/goal-command-and-eval-prd-analysis.md`.

### OQ6 (OPEN, parked with an unblocking condition)

*Comparator tolerance calibration per seam, and the amplifier gain function.*

**Parked, honestly.** These are empirical, and setting them from an armchair would be the
worst kind of false precision. **Unblocking condition: a corpus of at least ten real
Spec-to-Contract pairs from this tree with known outcomes, run through the round-trip test of
2.6, so a tolerance can be fitted rather than invented.** `Core/products/understudy/` is the
implement that produces such a corpus, and this is a concrete first non-Fieldbook slice for it.
Until then the operator is specified and not runnable, which section 3 states plainly.

### OQ7 (was OPEN; now RULED)

*Common-mode definition: how to define "faithfully rendered".*

**Ruling: common mode is what survives a round trip.** Full definition in 2.6. Re-express the
lower projection upward without reading the upper text, diff the reconstruction against the
actual upper text, reject the match, amplify the two asymmetric residues. Dropped intent
(upper only) is the expected loss. **Invented intent (reconstruction only) is the more
dangerous residue**, because a contract that has grown a requirement the spec never asked for
is surrogation already in progress. The round trip is chosen specifically because it needs no
rubric, and therefore does not re-inject the author's frame the way a rubric-driven comparison
does.

### OQ8 (was OPEN; now RULED)

*Does introducing eval-style finish lines into a low-maturity org create a more credible way
to look done without being done?*

**Ruling: yes, and the mitigation is structural, not a footnote.** This is no longer a hunch;
it is a finding. Choi, Hecht and Tayler show experimentally that surrogation is **strongest
when a single measure stands in for the construct**, and is mitigated when people are involved
in choosing the strategy the measure represents. A single binary finish line standing in for a
product intent is precisely the experimental condition under which surrogation was strongest.
Adding production values to that (a clean verdict, a transcript, a green check) makes the
surrogate more convincing, not less.

Two mitigations follow directly from the evidence, and neither is "add a caveat":

1. **Never one finish line.** At least two non-redundant measures per seam. The Choi result is
   specifically about single-measure conditions.
2. **The team that will be judged writes the finish line.** Involvement in choosing the
   construct is the intervention with experimental support.

"Confirmation with a footnote" is the weakest of the three and should not be relied on. A
footnote does not survive the screenshot.

### OQ9 (was OPEN; now RESOLVED)

Source manifest complete. All four Aakash links identified, three verified and one probable,
in `reference/goal-command-and-eval-prd-analysis.md` section 2. The LinkedIn post body itself
remains unreadable and the two claims that depend on it are marked UNRESOLVED there rather
than carried as facts.

### OQ10 (was OPEN; now RESOLVED)

Both academic load-bearers grounded in named work. See `reference/...` section 5: Kohli 2026
plus "Mind the Gap" plus Knight and Leveson for correlated error; Choi, Hecht and Tayler plus
Goodhart and Strathern for surrogation.

### OQ11 (was OPEN; now RULED, medium confidence)

*At what altitude does collapsing PRD and eval stop being acceptable and start being
dangerous?*

**Ruling: the threshold is not org size. It is whether the author of the intent and the author
of the contract are the same mind holding the same context.** Collapse is free when one person
writes both within one working memory. It becomes load-bearing at the first of two crossings,
whichever comes first: **a person boundary** (the one who wanted it is not the one who wrote
the finish line) or **a time boundary** (the same person, far enough apart that the why is no
longer in working memory). The second crossing is the one people miss, and it is the one an
agent forces constantly, because an agent resuming a session has no working memory of the why
at all.

Confidence: medium. **What would falsify it:** a case where intent and contract were authored
by one person in one sitting and the collapse still produced a confidently wrong "done". If
that shows up, the threshold is about the artifact's lifespan rather than its authorship, and
this ruling is wrong.

### OQ12 (OPEN, parked with an unblocking condition)

*How does the three-floor model reconcile with the BRD, FRD, TRD lineage once a real
requirements artifact is available?*

**Partly dissolved, partly parked.** Dissolved: 2.2 replaces the document lineage with the
work ontology, so there is no second taxonomy left to reconcile, only a crosswalk to read.
What remains parked is the empirical half, and it is the same one as OQ6. **Unblocking
condition: a real, externally authored requirements document (a client BRD or FRD, synthetic
or genuine) run through the crosswalk, to test whether the four legacy document types actually
land on four distinct ontology levels or collapse onto two.** The seeding handoff's decision
to park this pending a real artifact stands, and it is not a Subaru task: that engagement
closes 2026-09-18 and nothing client-specific may enter Core.

---

## 5. Provenance

Seeded by a chat session of 2026-06-16 captured to
https://github.com/theparlor/intake/issues/12, itself triggered by a LinkedIn post carrying a
`/goal` cheat sheet. That capture's findings F1 through F11 are absorbed into sections 1 and 2
above. Its sourcing was completed, and five of its factual claims corrected, on 2026-09-16;
the verified record and the corrections are in
`reference/goal-command-and-eval-prd-analysis.md`.
