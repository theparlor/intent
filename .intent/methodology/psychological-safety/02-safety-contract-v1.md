# Psychological Safety Contract — v1 (Draft)

**Status:** Draft for review
**Date:** 2026-04-09
**Owner:** Brien
**Derived from:** `01-edmondson-four-dimensions-analysis.md`
**Required reading before team pilot:** YES

## Purpose

Intent's mechanisms (trust scores, signals with attribution, autonomy levels, contract verification, panel review) can either support or destroy psychological safety depending entirely on how they are implemented and what they are used for. This contract codifies the promises Intent makes to the humans whose work touches the system, so that the mechanisms function as learning instruments rather than surveillance.

This is a contract in the technical sense: a set of verifiable assertions about how Intent behaves. It is also a contract in the social sense: the explicit promise a team operating with Intent makes to its members.

**If you cannot sign this contract, do not adopt Intent.** A version of Intent in a culture that cannot honor these promises is a version of Intent that will damage the humans who use it. That is not a better-than-nothing deployment; it is worse than not adopting.

## Scope

This contract applies to any deployment of Intent where humans author signals, review specs, receive trust scores, or are subject to panel-review outputs. That includes:
- Individual practitioners using Intent on their own work
- Teams where Intent is the operating system
- Engagements where Intent is the delivery substrate
- Any org adopting the notice→spec→execute→observe loop

It does NOT apply to purely agent-internal cycles where no human work is being evaluated — e.g., an agent running a panel review on a machine-generated artifact.

## The nine promises

### Promise 1 — Trust scores are about the artifact, not the person

**What we commit to:**
- Trust scores are calculated against specific signals, specs, and contracts — not against authors, reviewers, or teams.
- The trust formula (clarity + blast radius + reversibility + testability + precedent) is a technical assessment of the artifact's readiness for agent execution, not a judgment of the human who produced it.
- Low clarity on a spec means "this spec needs more work" — never "this person thinks unclearly."
- The word "clarity" in the trust formula refers to observable properties of the written artifact: specific acceptance criteria, unambiguous success conditions, testable assertions. It does not refer to the cognitive state of the author.

**What we explicitly do NOT use trust scores for:**
- ❌ Performance reviews
- ❌ Compensation decisions
- ❌ Promotion or demotion
- ❌ Performance improvement plans (PIPs)
- ❌ Firing decisions
- ❌ Public team comparisons
- ❌ Manager-facing dashboards that aggregate trust scores by author
- ❌ Any cross-team "whose scores are higher" benchmarking

**How we enforce this:**
- Trust score events (`signal.trust_scored`, `spec.trust_scored`) carry an explicit `used_for` field. Any consumer that touches these events must declare its purpose. Purposes outside the approved list trigger a warning.
- Author fields on signals, specs, and trust scores are not exposed to manager-facing aggregation tools by default.
- Any new tool that consumes trust scores must be reviewed for compliance with this promise before deployment.

### Promise 2 — Signal capture with scoped visibility

**What we commit to:**
- Every signal has a `visibility` field. Default is `team-only`, not `public`.
- Authors can mark signals as `author-only`, `team-only`, `engagement-only`, or `public`.
- Signals about interpersonal friction (marked with `sensitive: true`) are routed to a private review path and are never visible to the people they mention unless the author explicitly shares them.
- Authors see how their signals flow downstream — who read them, who clustered them, who promoted them to intents — so there is no invisible dossier.

**What we explicitly do NOT do:**
- ❌ Default signals to public visibility
- ❌ Allow managers to search signals by author name as a performance investigation tool
- ❌ Expose sensitive-flagged signals without the author's explicit export action
- ❌ Retain signals for compliance/legal discovery purposes without the author being notified

**How we enforce this:**
- The signal schema requires the visibility field before persistence.
- The signal MCP server filters queries by the caller's visibility scope.
- A "signal provenance" tool lets any author see the downstream path of their signals.

### Promise 3 — The appeal surface

**What we commit to:**
- Any trust score can be appealed by the author. The appeal generates a new signal with type `trust-appeal` and triggers a human-reviewed re-score.
- Any spec-shaping protocol output (the four-persona critique) can be appealed. The author can request an alternate rendering, a different persona rotation, or an explicit rebuttal.
- Any panel-review output on human work can be marked by the author as "not fair," which triggers a check for the known failure modes (confirmation bias, demographic critique pattern, tonal mismatch).
- Appeals are NOT held against the appealing author. An appeal is a design signal, not a complaint.

**How we enforce this:**
- `trust-appeal`, `spec-critique-appeal`, and `panel-review-appeal` are first-class signal types.
- Appeal rates are a health metric for the system, not the appeals' authors. High appeal rates on a particular scorer, panel, or protocol mean something is wrong with the instrument, not with the people using it.

### Promise 4 — Distinguished failure types

**What we commit to:**
- The `contract.assertion.failed` event carries a `failure_type` field: {basic, complex, intelligent}.
- **Basic failures** — deviations from known processes in predictable domains. These are preventable and are addressed through process improvement, not individual blame.
- **Complex failures** — novel combinations of factors in complex systems. These are unavoidable but manageable through early detection. They are addressed through better signal capture and pattern recognition, not individual blame.
- **Intelligent failures** — deliberate experiments at the frontier of knowledge, where outcome uncertainty is high and failure generates information. These are celebrated, not corrected.
- L3 and L4 autonomy exists specifically to enable intelligent failures on agent work. Failures at those levels are expected and valuable.

**Source:** Edmondson, *Right Kind of Wrong* (2023).

**How we enforce this:**
- The event schema requires failure_type classification.
- Dashboards show failure type distribution, not raw failure counts. A team with 80% intelligent failures is healthier than a team with 20% basic failures.
- "Celebrate the failure" is a first-class ritual for intelligent failures on L3/L4 work — not theater, an actual artifact-generating moment.

### Promise 5 — Explicit accountability routing

**What we commit to:**
- When a contract fails, the event captures four roles explicitly:
  1. **Spec author** — the human who wrote the spec being verified
  2. **Spec reviewer** — the human who approved the spec
  3. **Autonomy authorizer** — the human who set the autonomy level (L0–L4)
  4. **Executing agent** — the agent (or human) that executed the contract
- Accountability is distributed, not diffused. Each role has a specific responsibility and a specific learning loop.
- "The agent did what the spec said but the outcome was wrong" is not a mysterious failure. It is a spec problem (the spec didn't anticipate the condition) OR an autonomy problem (the authorizer escalated too quickly) OR a verification problem (the contract didn't test the right thing). The `root_cause` field on the failure event must identify which.
- No role is ever scapegoated for a failure that belongs to another role.

**How we enforce this:**
- The event schema requires all four role fields.
- Root-cause analysis is a required follow-up to any contract failure at L3/L4 autonomy, and is done in a structured format (not a blame meeting).

### Promise 6 — Disagreement is protected

**What we commit to:**
- Any human can challenge any spec, any trust score, any agent output, any panel-review finding, at any time, without prejudice.
- The "disambiguation signal" pattern — generate a new signal when stuck — is Intent's institutional permission to ask questions and express doubt. It is not a sign of failure; it is a sign of engagement.
- "I disagree" is a valid input to the loop. It does not require a superior to ratify it.
- Challenge-the-Intent passes (premise-level critique) are welcomed and structured, not suppressed.

**How we enforce this:**
- The `disagreement` signal type is a first-class primitive.
- Disagreement signals are not used in trust score calculation as negative evidence.
- Panel reviews include explicit prompts for disagreement in the output format.

### Promise 7 — No capability stigma on autonomy levels

**What we commit to:**
- Autonomy levels (L0–L4) describe the technical readiness of a signal/spec for agent execution. They do not describe the capability of the humans involved.
- A team whose signals cluster at L1–L2 is not "less capable" than a team whose signals cluster at L3–L4. They may be working on harder problems, newer domains, or higher-stakes systems.
- Autonomy level distributions are NOT published as team comparison metrics.
- Individual managers do not see "their direct reports' average autonomy level" as a performance indicator.

**How we enforce this:**
- Dashboards do not aggregate autonomy levels by team or individual for public comparison.
- The phrase "autonomy level" is never used in performance conversations. It is a system classification, not a human rating.

### Promise 8 — Inclusion in voice and vocabulary

**What we commit to:**
- The panel-review voice library actively grows to include voices historically underrepresented in tech and product. Signal diversity is signal quality.
- Intent's vocabulary has a plain-language translation layer. Every term ("signal," "trust score," "contract," "autonomy level," "atom") has a one-line gloss for non-engineering practitioners.
- Non-git onramps for Notice capture exist. PMs, designers, research leads, and customer-facing roles can contribute signals without touching a terminal.
- The "practitioner-architect" target user framing is named explicitly in all content. Intent does not pretend to be universal.

**How we enforce this:**
- Persona library expansion is a tracked workstream with explicit demographic diversity goals.
- Glossary pages are required for all public Intent content.
- At least one non-git Notice onramp is supported in every deployment mode (MCP tool is the first example).

### Promise 10 — Infrastructure prerequisites for safe trust-scored autonomy

**What we commit to:**

Intent's trust formula (clarity + 1/blast_radius + reversibility + testability + precedent) only produces valid calibration if the deployment environment actually supports the properties being scored. A trust score of 0.85 on "reversibility" is meaningless if the environment has no rollback capability. A "testability" score of 0.9 is meaningless if no automated tests exist. Intent commits to naming these infrastructure prerequisites explicitly so that teams can assess whether they can safely use trust-scored autonomy at all.

**The four required infrastructure capabilities:**

1. **Blue-green deployment or equivalent reversibility infrastructure.** The code can advance but the result must be accepted by humans before rollout. Without this, "reversibility" in the trust formula is fictional and L3/L4 autonomy is unsafe regardless of score.

2. **Feature flag change management.** Impactful changes are gated behind flags that humans control. Intent's L3/L4 autonomy brackets assume the ability to ship code that is still "off" until a human turns it on. Without this, the "blast radius" factor is unknowable at commit time.

3. **Significant automated testing.** Signals about outcomes depend on tests that actually run and report. Without automated testing, contract verification becomes manual authorship (slow, biased) or absent (silent failure). Either path destroys the signal quality the trust formula depends on.

4. **Change reporting that is visible.** The measures must be visible, not hidden in dashboards nobody checks. Forsgren's DORA research (*Accelerate*, 2018) is unambiguous: measurement without visibility is cargo-cult measurement. Intent cannot generate valid signals from invisible measures.

**The load-bearing principle (Brien, 2026-04-09):**

> If your development and your product isn't measurable, and the measures aren't visible, it shouldn't be using our approach. It lacks the ability to generate and rely on valid signals.

**What we explicitly do NOT do:**
- ❌ Pretend trust scores are meaningful in environments that don't support the properties being scored
- ❌ Recommend L3/L4 autonomy for teams without rollback infrastructure
- ❌ Claim "observability-first" methodology and then deploy into environments where observability doesn't exist
- ❌ Treat infrastructure gaps as "can be addressed later" — they are prerequisites, not roadmap items

**How we enforce this:**
- The discovery interview protocol includes infrastructure readiness questions
- The site has an explicit "when NOT to adopt Intent" section naming infrastructure gaps
- Pilot engagement intake includes a reversibility/testability/visibility checklist
- The trust formula should emit a warning signal when the environment's actual rollback/test infrastructure doesn't match the scored value

**The connection to Promise 4 (distinguished failure types):**

Promise 4 commits to distinguishing basic, complex, and intelligent failures. But distinguishing failure types requires knowing what happened. Knowing what happened requires measurability and visibility. Therefore: Promise 4 cannot be honored without Promise 10. The two are technically distinct but operationally co-dependent.

A team can honor Promise 10 (have great infrastructure) without honoring Promise 4 (treat all failures as equal). A team cannot honor Promise 4 (celebrate intelligent failures) without also honoring Promise 10 (actually see the failures). The infrastructure prerequisites are a necessary but not sufficient condition for psychological safety around agent execution.

### Promise 9 — Cultures where Intent cannot honor this contract must not adopt it

**What we commit to:**
- Intent explicitly lists cultures and contexts where it should not be adopted:
  - Theory X organizations where trust is low and surveillance is normalized
  - Performance-review-driven cultures where any new metric becomes a compensation input
  - Environments where psychological safety is not already valued at the leadership level
  - Contexts where the "distinguished failure types" promise cannot be honored because all failures are punished equally
- When Brien or any Intent practitioner engages with a potential adopter, this list is part of the intake conversation.
- Saying "no, Intent is not for you" is a legitimate outcome of discovery. It protects both the potential adopter and Intent's reputation.

**How we enforce this:**
- The discovery interview protocol (INT-010) includes cultural readiness questions.
- The site includes an honest "who should not adopt Intent" section.
- Engagement intake has a safety-culture checklist.

## What happens if the contract is violated

This is a trust-based contract, not a legally enforceable one. It is honored through:

1. **Design-time enforcement** — the schemas, events, and tools are built to make violations technically difficult (e.g., required visibility field, accountability roles, appeal surfaces).

2. **Review-time enforcement** — every new Intent capability is reviewed against this contract before shipping. Panel-review calls should include a "safety contract check" pass for new mechanisms.

3. **Operational enforcement** — if a deployment is using Intent's mechanisms in ways that violate this contract, the correct response is to reach out to the deployment owner and either fix the usage or help them migrate off.

4. **Public enforcement** — this contract is published alongside Intent. Anyone evaluating Intent can read it and hold the project accountable.

## What this contract is NOT

- **It is not a legal document.** It has no force of law and does not create liability.
- **It is not a complete methodology.** It addresses psychological safety specifically, not every ethical consideration in agent-human collaboration.
- **It is not permanent.** It will evolve. Version 1 is a starting position, not a final answer.
- **It is not sufficient alone.** It needs to be paired with change management practices (see `03-change-management-analysis.md`), training, and explicit culture work in any adopting team.

## Signing

If you are adopting Intent in a team or organizational context, you sign this contract by:

1. Reading it in full (not just the summary)
2. Discussing it with your team — especially the people most likely to be affected (junior engineers, cross-functional partners, people new to the org)
3. Identifying the specific mechanisms you will use and the specific promises they invoke
4. Writing down any promises you cannot honor, and either adjusting your use of Intent to avoid those mechanisms OR deciding not to adopt
5. Publishing your signed version to your team (not a signature requirement — a transparency requirement)

## The "Edmondson more" open thread

Brien's position on trust scores (DEC-20260409-02, answer 5):

> "the trust scores are designed for us to consider the current maturity of our agents and identify the risk of tasks we face and use those to calibrate our trust for decision making without interuptive human in the loop. knowing a reversible decision was made and can be reviewed later is my measure but I feel like Edmondson is teasing at another factor. so we should talk more."

Brien is sensing correctly that Edmondson is pointing at something beyond reversibility. Reversibility is a rational safety concern (we can undo this). Edmondson's safety is an **interpersonal** safety concern (we will not punish you for having been associated with this).

**The gap, as best we can name it today:**

Even a fully reversible decision can be socially costly for the human who made it. A team can have perfect blue-green and feature flag infrastructure (Promise 10) and still be psychologically unsafe if the person who authorized an L4 action gets shamed when it goes sideways. Edmondson's research specifically shows that teams with high safety report MORE errors not because the errors are reversible, but because the humans who made them aren't punished socially for having been present when they occurred.

**What might be missing from the Safety Contract:**

Promises 4 (distinguished failure types) and 5 (explicit accountability routing) start to address this, but they address the *technical* shape of accountability. The missing piece may be a promise about the *social norms* of accountability — specifically, what the team commits to NOT doing when a failure attributed to an identifiable role goes public.

Candidate language (UNCOMMITTED, needs exploration):

> **Promise 11 (draft):** Social norms for failure attribution. When a contract.assertion.failed event identifies a spec author, a reviewer, an autonomy authorizer, and an executing agent, the team commits to responding to all four roles as contributors to a learning moment, not as targets for blame. No standup retrospective, no 1:1, no 360 review references the failure in a way that diminishes the human who held the role. Intelligent and complex failures are treated as shared learning events; basic failures are addressed through process fix, not individual correction.

This is marked as open for exploration because the wording and enforcement mechanism are not yet clear. Brien and I will work on this in a follow-up session.

**What is clear:** The gap exists, it is not covered by Promise 10 (infrastructure) or by the existing 9 promises alone, and it is worth explicit design work.

## Open questions and uncertainties

This is v1. We do not have all the answers. Known open questions:

- **Promise 1 (`used_for` field):** How do we technically prevent a downstream tool from claiming a valid `used_for` but actually using scores for something else? This is the classic policy-vs-enforcement gap.
- **Promise 2 (sensitive visibility):** The signal's `sensitive: true` flag relies on the author's judgment. Some authors will under-use it; others will over-use it. How do we help authors calibrate?
- **Promise 4 (failure type classification):** Who classifies a failure as basic/complex/intelligent? Self-attribution has an incentive to mark everything as intelligent. Third-party attribution risks becoming performance review.
- **Promise 6 (disagreement protection):** How do we distinguish protected disagreement from unproductive objection? Is there a limit?
- **Promise 9 (cultural readiness):** How do we objectively assess cultural readiness without being preachy or gatekeeping? We need a checklist, not a vibes test.

## Related artifacts

- `01-edmondson-four-dimensions-analysis.md` — the research foundation
- `03-change-management-analysis.md` — Bridges + Kotter applied to Intent adoption (also required reading)
- `.intent/intents/INT-013-safety-and-change-workstream.md` — the intent that governs this work
- `.intent/signals/2026-04-09-psychological-safety-never-addressed.md` — SIG-049, the origin signal
- DEC-20260409-01 — the decision record from the post-panel review

## Lineage and attribution

- **Amy Edmondson** — *The Fearless Organization* (2018), *Right Kind of Wrong* (2023), *Teaming* (2012). Every promise in this contract traces back to her research.
- **Chris Argyris** — theory-in-use vs. espoused theory (used in Promise 6 on protected disagreement).
- **Edgar Schein** — humble inquiry (informing the appeal surface and disagreement norms).
- **Liz Wiseman** — *Multipliers* (used in Promise 3 on help-seeking and in critique of diminisher patterns).
- **Douglas McGregor** — Theory X/Y (used in Promise 9 on cultural readiness).
- **Intent panel review 2026-04-09** — Org Design panel, dominant voice Edmondson, critical finding F10.
