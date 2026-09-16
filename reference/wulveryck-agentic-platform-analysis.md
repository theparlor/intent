---
title: "Wulveryck, Agentic Platform and Team Topologies, mapped to the Intent and Coherence Engineering stack"
type: reference-analysis
maturity: draft
status: terminal
created: 2026-09-16
confidentiality: internal
reusability: adaptable
lineage:
  - https://github.com/theparlor/intake/issues/23
sources:
  - "Olivier Wulveryck, Vibe Coding at Scale? Engineering Strikes Back, 2026-06-19 (LastMod 2026-07-18), 2224 words / 11 min, https://blog.owulveryck.info/2026/06/19/vibe-coding-at-scale-engineering-strikes-back.html"
  - "Olivier Wulveryck, Who Does What? Team Topologies for the Agentic Platform, 2026-06-24 (LastMod 2026-07-18), 3743 words / 18 min, https://blog.owulveryck.info/2026/06/24/who-does-what-team-topologies-for-the-agentic-platform.html"
  - "Matthew Skelton and Manuel Pais, Team Topologies, IT Revolution, 2019 (the model being adapted)"
  - "Martin Fowler with Don Roberts, Refactoring, 1999 (Rule of Three)"
related:
  - /Users/brien/Workspaces/Core/frameworks/intent/reference/external-patterns-index.md
  - /Users/brien/Workspaces/Core/frameworks/coherence-engineering/positions/agentic-platform-boundary.md
  - /Users/brien/Workspaces/Core/frameworks/coherence-engineering/external/source-pointers/2026-06-24-wulveryck-team-topologies-agentic-platform.md
  - /Users/brien/Workspaces/Core/frameworks/intent/spec/SPEC-INTENT-SEAM-DECOMPOSITION-001.md
  - /Users/brien/Workspaces/Core/frameworks/intent/spec/autonomy-flight-model-v1-DRAFT.md
  - /Users/brien/Workspaces/Core/products/_intake/2026-07-07-three-plane-reconciliation/NOTICE.md
---

# Wulveryck, Agentic Platform and Team Topologies, mapped to our stack

## Plain language first

**What this is.** Two blog posts by Olivier Wulveryck argue that when a company lets AI agents
write its software, the hard problem is no longer writing code. It is that every team invents its
own version of the company's standards, and one person ends up holding all the decisions. His
answer is to build a *platform*: take the organization's own rules, make them executable, and let
the agents ask the platform how to proceed instead of making a human anticipate every question in
advance. The second post uses Team Topologies (a well known 2019 book about how to shape teams) to
say who builds that platform and who consumes it.

**Why it matters to Brien.** This is the same architecture we have been building, described at a
different altitude and in vocabulary clients already recognize. It is not a competitor. Two things
come out of it. First, a borrowed vocabulary: Skelton and Pais give us words a CTO already trusts
for a structure we would otherwise have to introduce from scratch. Second, and more valuable, a
clean boundary. Wulveryck states in his own words that his platform "does not guarantee business
excellence," only "a baseline of safety and standards." That sentence is the edge of his model and
the beginning of ours. His platform checks work against *standards*. Coherence Engineering checks
work against *intent*. Everyone in this space is building the first loop. Almost nobody is building
the second one.

**What changed as a result of this analysis.** Six open questions carried in the intake handoff are
now answered with rulings, recorded below in section 5. One of those rulings corrects the handoff:
the phrase "drive human seam gain toward zero" was wrong as written, because it collapsed two
different quantities into one. One structural gap was found and is recorded as a signal: the
identifier PSAE-001 is cited across the tree as though it were canonical, and no artifact defines
it.

**What someone does differently now.** When framing our work for a client that already knows Team
Topologies, use his four team types and three interaction modes as the entry ramp, then name the
gap his model leaves open. Do not reuse his five platform-maturity criteria as a mapping onto an
engagement's own readiness checklist: section 5 Q5 explains why that rhyme is superficial.

---

## 1. The sources, verified

Both articles were fetched and read on 2026-09-16. The intake handoff was written from a chat
capture in June and carries three citation errors, corrected here.

| Claim in the handoff | Verified state |
|---|---|
| Article 2 published 2026-06-24, LastMod 2026-06-26 | Published 2026-06-24. **LastMod is 2026-07-18**, not 2026-06-26. Both articles were touched on that date. |
| Article 1 is "Vibe Coding at Scale: Engineering Strikes Back" | Correct title is **"Vibe Coding at Scale? Engineering Strikes Back"** (question mark, no colon), published **2026-06-19**, 2224 words / 11 min. The handoff gave no URL; it is https://blog.owulveryck.info/2026/06/19/vibe-coding-at-scale-engineering-strikes-back.html |
| Article 1 "defines the agentic platform / agentic factory" | It defines **agentic platform** only: "the organization's state of the art made executable and consumable by AI, and governed as a product." It does **not** define "agentic factory"; factory language appears only as a contrast in one diagram. Do not attribute a factory definition to him. |
| 3743 words / 18 min, article 2 | Confirmed. |
| Follow-up promised on A2A communication | Confirmed, still promised, not yet published as of 2026-09-16. |

Everything else the handoff asserted about the article checks out against the text, including the
four team types, the three interaction modes, the four pillars, the five maturity criteria, the
Rule of Three worked example, the Bottleneck Paradox, the three-to-five-team threshold, and the
two sentences that do the most work for us (quoted in section 2).

## 2. What the article actually says

**Four team types**, adapted from Skelton and Pais:

1. **Stream-aligned.** Produce business value, drive the orchestrator, define business intent,
   supply dynamic context. Need not be software engineers: domain specialists, product managers,
   analysts generating applications directly through agents.
2. **Platform.** Builds and runs the engine. Four pillars, all delivered self-service: Global
   Context (system prompts, shared business knowledge, architectural patterns), Deterministic
   Guardrails (security, reliability, brand consistency, coding conventions), Agentic Tooling (MCP
   servers, CI/CD, evaluation frameworks, shared agent skills), Execution Engine (inference).
3. **Enabling.** Environment provisioning, agentic training, and "manual shift-left", enforcing
   practices by hand until the platform hardcodes them. Permanent, not transient.
4. **Complicated Subsystem.** Optional. Deep technical work (hosting open-weights models, inference
   cost, data sovereignty, red-teaming, RAG architecture, fine-tuning, custom evals) that "never
   reaches the stream-aligned product teams directly."

**Three interaction modes.** Facilitating (enabling to stream-aligned, temporary, coaching).
X-as-a-Service (platform to everyone, "the target state and the sole engine of scaling").
Collaboration (complicated subsystem to platform, high bandwidth, meant to mature into
X-as-a-Service).

**Four deviations from Skelton and Pais**, as he states them: stream-aligned teams need not be
technical; stream-aligned autonomy no longer means "you build it, you run it" because the platform
absorbs operational responsibility; enabling teams become permanent because there is a hard ceiling
on upskilling domain experts; and cognitive load must be regulated as throughput over time, not only
distributed as a static quantity.

**Five platform-maturity criteria** that gate the autonomy transfer: hardcoded guardrails (enforced
"deterministically via standard code", explicitly not by "stochastic LLM 'verbal agreement' or
prompt constraint"); measurable reliability against SLAs; a high self-service index; agent-readable
documentation; and decision traceability, an audit trail for every guardrail intervention.

**The sentences that carry the argument for us**, quoted exactly:

- On what the platform will not do: the platform does not guarantee business excellence, only
  "a baseline of safety and standards."
- On guardrail design: "guardrails must be **transparent in their decisions** (providing clear error
  messages and audit trails), even if they remain entirely opaque in their implementation."
- On the boundary he could not clean up: "This 'what/how' boundary is more permeable than it sounds.
  Brand consistency, for example, is a business concern (the _what_), but verifying it can be
  automated by the platform (the _how_)."
- On absorbing the anticipation burden: "telling the agent 'don't worry about security' means it
  will ask the platform how to proceed, and deterministic controls will enforce the outcome
  downstream."
- On governance: "Without governance, agentic production just creates industrialized shadow IT."
- On the Bottleneck Paradox: "If one person must manually arbitrate the flow of needs from dozens of
  agent-driven teams, we recreate the exact cognitive bottleneck this entire model was designed to
  prevent."
- On when to build a platform at all: "Once you reach three to five product teams, the cumulative
  cost of reinvention (recreating context, rewriting guardrails, fixing localized inconsistencies)
  far outweighs the cost of investing in a shared platform."

**Rule of Three, worked.** Three teams build data masking independently: E-commerce (shipping
addresses, credit cards), Loyalty Program (customer names, birth dates, three months later), Store
Operations (email addresses). Three distinct teams solving the same shape graduates the guardrail
from local to systemic, as a platform service named "Customer Data Anonymization." The rule is
Fowler and Roberts's Rule of Three from Refactoring (1999), applied to guardrails instead of code.

## 3. The mapping, claim by claim

Reading key for the columns. **Intent stage** is Notice, Spec, Execute, or Observe. **CE** cites a
Coherence Engineering principle or position. **Plane** names which of the three exposure planes the
claim sits on (agent-facing, gateway, system), the decomposition the tree calls PSAE-001; see the
honesty note in section 6. **Autonomy** is the L0 to L4 trust level the claim bears on. **Verdict**
is agree, agree-with-correction, or diverge.

| # | His claim | Intent stage | CE | Plane | Autonomy | Verdict | What we adopt |
|---|---|---|---|---|---|---|---|
| 1 | Cognitive load does not disappear, it becomes an anticipation burden plus a throughput problem, compressed onto one person | Notice | Coordination tax to coordination investment, the founding CE reframe | n/a | Describes why L0 gating cannot scale | Agree | His two-part decomposition of the load is sharper than ours. Adopt "anticipation burden" as vocabulary. |
| 2 | The platform absorbs the anticipation burden by being queryable by the agent | Spec | Artifact composition over ceremony | agent-facing | Raises the ceiling on unattended L | Agree | This is our compiled-artifact thesis stated for an org. Direct validation, nothing to change. |
| 3 | Team Topologies distributes structural load, the platform absorbs dynamic throughput | Notice | Altitude separation | n/a | n/a | Agree | Clean articulation of why an org chart alone cannot answer the question. |
| 4 | Four team types, stream-aligned now possibly non-technical | Spec | Ownership topology, one accountable owner plus contributors | n/a | Sets who may hold which L | Agree | His "specifics with the stream, systemics with the platform" split is our ownership plane with teams as nodes instead of artifacts. Borrow the vocabulary for client framing. |
| 5 | Three interaction modes, with X-as-a-Service as the target state | Spec | Typed seams | gateway | The mode is the current L of the seam | **Agree with correction** | The modes are not three seam types. They are three *states of one seam*, distinguished by who holds the comparator: two humans jointly (Collaboration), a lending team on a decay schedule (Facilitating), or the contract itself (X-as-a-Service). See Q1 and Q2 in section 5. |
| 6 | Platform pillars: Global Context, Deterministic Guardrails, Agentic Tooling, Execution Engine | Execute | Substrate exposure | Global Context and Tooling are agent-facing; Guardrails are the gateway; Execution Engine is the system plane | Guardrail coverage is the gate on L | **Diverge on completeness** | The four pillars are correct and incomplete. There is no pillar holding *declared intent*, which is why his model can only close the conformance loop. See section 4. |
| 7 | Guardrails are transparent in their decisions and opaque in their implementation | Execute, Observe | Descriptive seam outside, constraint seam inside | gateway | The audit trail is what makes a higher L reviewable | Agree, and it earns its keep | This dissolves his own confessed what/how permeability. It is one seam with two faces: a descriptive face the business declares against, and a constraint face the platform enforces. He states the design rule without noticing it solves his problem. |
| 8 | Hardcode guardrails deterministically rather than relying on a stochastic LLM verbal agreement | Execute | Comparator at the seam | gateway | Deterministic enforcement is what lets L rise safely | Agree | A guardrail is a typed comparator: measured output against declared reference, with the "why blocked" message as the error signal. Deterministic means the comparator's response to an error is absolute rather than probabilistic. |
| 9 | Five platform-maturity criteria gate the autonomy transfer | Observe | Closure discipline | all three | Explicitly an L0 to L4 progression on the *business* team, gated by *platform* maturity | Agree | This is the clearest external statement we have that autonomy is a property of the substrate, not of the actor. It is the flight model's Lift term, named in plain English. |
| 10 | Without governance, agentic production is industrialized shadow IT; track active and abandoned apps, trigger automated deprecation | Observe | Coherence debt register | system | Governance is what makes L4 recoverable | Agree | Portfolio deprecation as an Observe-phase obligation is a gap in our own Observe spec, which stops at signal capture and does not mandate retirement of what the loop produced. |
| 11 | Rule of Three: a guardrail duplicated across three distinct teams graduates from specific to systemic | Notice, at platform altitude | Promotion, engagement to Core | gateway | n/a | Agree | We already run this instinct under a different name. The three-count is a detection threshold, not an altitude constant. See Q4. |
| 12 | The Bottleneck Paradox: platform success recreates the bottleneck at the platform PO | Notice | This is coherence debt accumulating at a single seam | n/a | The paradox is a stall, in flight-model terms | **Agree, and this is where we are required** | His instinct ("cognitive automation") is right and unstructured. We supply the structure: instrument the learned seam map, not only the declared one, and decompose the load into coupled forces rather than treating it as scalar throughput. See section 4. |
| 13 | Three to five product teams is the threshold where a shared platform pays | Notice | Altitude transition | n/a | n/a | Agree | Useful, concrete, and citable in client conversation. It is his, not ours; attribute it. |
| 14 | The platform enforces a baseline of safety and standards, it does not guarantee business excellence | (none, he stops here) | **This is the boundary** | n/a | n/a | **Diverge, by his own admission** | The whole wedge. See section 4 and POS-AGENTIC-001. |

## 4. The divergence, stated once and precisely

Everything above is agreement or refinement. There is exactly one real divergence, and he names it
himself.

His platform closes the loop between **what was produced** and **what the standards require**. That
is a conformance loop, and it is a genuine achievement: he makes it deterministic, auditable, and
self-service. Call it eval against standards.

He then hands back the harder loop with no mechanism. Business excellence, the question of whether
the thing produced actually serves what someone intended, is explicitly outside his platform's
guarantee. Call that eval against intent. Coherence Engineering is the discipline that closes it.

The structural reason his platform cannot close it is visible in his own pillar list. He has four
pillars: Global Context, Deterministic Guardrails, Agentic Tooling, Execution Engine. Context is
shared knowledge. Guardrails are constraints. Tooling and Execution are mechanism. **Nothing in the
pillar set holds a declared reference for the outcome.** A comparator needs two inputs, a measured
value and a reference. He built the measured side and the constraint side. The declared-intent side
lives in the stream-aligned team's head and in a prompt, which is precisely the stochastic verbal
agreement he refuses everywhere else.

So the honest statement of the relationship is not "two frameworks in the same space." It is: his
model is the layer below ours, it is well built, and it terminates one loop short. Our framework is
the continuation of his, not a parallel to it.

**The Bottleneck Paradox is the proof.** It is the strongest passage in the piece and the place
where his model runs out. In flight-model terms (SPEC-INTENT-AUTONOMY-FLIGHT-MODEL-001 draft,
/Users/brien/Workspaces/Core/frameworks/intent/spec/autonomy-flight-model-v1-DRAFT.md): thrust, the
business teams producing, rose; lift, the platform's absorption capacity, did not rise with it;
gravity, governance debt, pulled the whole thing toward shadow IT. His enabling team is *temporary
lift*, humans manually holding a trust gate that the platform has not yet earned. The maturity arc
is the swap of temporary lift for structural lift. His own sentence, that the platform must provide
structural compensation, is exactly that swap, and he has no model that says when it is safe.

We do. Lambda, the coefficient of bravery, is how aggressively business teams deploy unsupervised,
and it can only be raised once lift exceeds gravity. Treating cognitive load as a scalar throughput
number, as he does, can name the paradox. The coupled force decomposition explains it.

The second structure we supply is the declared-versus-learned seam map. His org chart is a purely
*declared* map: here are the teams, here are the sanctioned interaction modes. The Rule-of-Three
signal, three teams independently building the same guardrail, is telemetry from the *learned* map,
evidence of where the real seams are rather than where they were drawn. His paradox is what happens
when an organization instruments the declared map and never the learned one: the graduation
candidates have to be collected by hand, by one person, which is the bottleneck. The fix is not
generic "cognitive automation." It is closing the loop between the declared map and the learned map,
so the platform PO arbitrates data instead of collecting it. He says he wants that outcome; he does
not have the pair of maps that produces it.

## 5. The six open questions, ruled

The handoff left six questions open. All six are answered here. Rulings are L4 local and reversible;
each one names its evidence.

**Q1. Formalize interaction-mode-as-typed-seam into the topology spec, or keep it as an
interpretive lens?**

Ruling: **keep it as an interpretive lens, add no new seam type, write no DDR.** The evidence is a
ratified key decision in our own spec. SPEC-INTENT-SEAM-DECOMPOSITION-001, section 2, Key decisions,
states: "Fan-out unit = Contract (CON), not file. Reuse the existing typed Contract; do not invent a
new seam type." Minting an "interaction mode" seam type in parallel with the Contract would fork the
seam primitive, which is the exact move that clause forbids. The three modes are better expressed as
an attribute on the existing Contract, a `mediation:` field with values `joint`, `lent`, or
`contract`, describing who currently holds the comparator at that seam. No spec changes, so no DDR
is required. The vocabulary is recorded in section 7 as a small adoption.

**Q2. Is "drive human-seam gain toward zero at maturity" the right gain semantics?**

Ruling: **no, and the handoff phrasing is corrected here.** It conflates two independent quantities.

- *Gain* is how strongly a comparator converts an error signal into corrective action. A
  deterministic guardrail is **maximum** gain: any error produces an absolute block.
- *Human mediation* is how much of the seam's traffic has to pass through a person in real time.

Maturity moves both, in opposite directions. It drives human mediation at the seam toward zero, and
it drives comparator gain **up**, to deterministic. "Drive human-seam gain toward zero" reads as
though maturity means weaker correction, which is the opposite of what his maturity arc does.

The corrected statement, which is the one to reuse: **maturity converts a human-mediated seam into a
contract-held seam, driving human mediation toward zero while raising comparator gain to
deterministic.** Coupling and loop speed are then separable, which is what the handoff's question was
reaching for: on the declared map we want low coupling, and on the learned map we want a fast loop.
Those are not in tension once gain and mediation are no longer collapsed into one word.

**Q3. Where does eval-against-intent get instrumented in his target state, without breaking
self-service?**

Ruling: **as a fifth pillar, Declared Intent, queryable on the same self-service terms as the
guardrails.** His self-service constraint is that nothing may require a ticket or a human handoff.
An intent artifact satisfies that constraint as long as it is published to the platform and readable
by the agent: a typed record carrying the declared outcome and a verification command, sitting beside
Global Context rather than inside it. Global Context holds what is *true of the organization*.
Declared Intent holds what *this piece of work is for*. Keeping them in one pillar is what lets the
reference side of the comparator stay in a prompt. Separating them is the whole fix, and it costs
his architecture nothing.

**Q4. Do our altitudes imply different graduation thresholds than his three teams?**

Ruling: **the number does not move, the confirmation lag does.** Fowler and Roberts's Rule of Three
counts *occurrences of a duplication*, not teams as such. At different altitudes the unit of
duplication changes (three teams at org altitude, three products at portfolio altitude, three
sorties at formation altitude), but three remains the detection threshold at every altitude, because
three is where a coincidence becomes a pattern regardless of what is being counted. What is genuinely
altitude-dependent is the cost of graduating too early: promoting a guardrail into a shared contract
freezes it for every downstream consumer, and the number of consumers grows with altitude. So higher
altitudes need a longer confirmation lag between detection and graduation, not a higher count. Keep
three as the trigger; add lag as the altitude-sensitive knob.

**Q5. Does his five-criteria dependency chain map onto a live engagement's five data-integrity
prerequisites, or is the rhyme superficial?**

Ruling: **superficial at the item level, real at the pattern level. Do not reuse the five-versus-five
table in any client-facing material.**

The pressure test was run against the actual five-item chain in the live engagement (engagement
scoped, not reproduced here: NDA, and this is a Core artifact). Item-for-item pairing fails, and
fails in a way that would embarrass anyone who presented it. His five describe the *producer*: can it
enforce, can it be measured, can it be consumed with no human in the loop, can an agent read it, can
you audit what it did. The engagement's five describe the *instrument*: does a denominator exist, do
counts resolve to the right unit, do counts agree across views, is the underlying record correct, has
a human validated it. Forced pairings produce false friends. His decision traceability, a machine
audit trail, is not the engagement's validation step, which is human acceptance, and reading them as
equivalents would mislead a client about what is already done.

The pattern underneath is real and reusable: both are **forced-order precondition chains gating an
autonomy step**, ordered by dependency rather than by priority, and both contain an item whose
position number understates its blast radius. That is the transferable observation. It is also
consistent with the standing distinction between priority and sequence already recorded in memory
(`feedback_priority_vs_sequence_conflation`). Carry the pattern forward, leave the table behind.

**Q6. Is there a positioning artifact worth producing?**

Ruling: **yes, and it exists as of this session.**
/Users/brien/Workspaces/Core/frameworks/coherence-engineering/positions/agentic-platform-boundary.md,
POS-AGENTIC-001.

## 6. Honesty notes

**PSAE-001 has no canonical artifact.** The identifier is cited across the tree as though it were a
ratified spec. A full-tree search on 2026-09-16 found it in exactly two files, both inside
/Users/brien/Workspaces/Core/products/_intake/2026-07-07-three-plane-reconciliation/, and in neither
case is it defined. The three-plane content attributed to it (agent-facing plane, gateway plane,
system plane) is used consistently in the intake handoff and in the Plane column of section 3 above,
and it is coherent, but it currently rests on a dangling identifier. This analysis uses the plane
decomposition on its merits and does not treat PSAE-001 as a citation. The gap is recorded as
SIG-COH-EXT-009.

**Depth of the Rule-of-Three example.** The article's worked example was verified at the level of
three named teams, the fields each masked, the three-month gap between the first two, and the name of
the graduated service. Finer detail in the intake handoff (for example a GDPR and CCPA configurable
posture on the graduated service) was not independently re-verified at that granularity and is not
repeated here as fact.

**Coverage.** Both articles were fetched directly. No web search was used, so no search-quota
narrowing applies. The promised third article on A2A communication had not appeared as of
2026-09-16; it is worth watching, because it will show whether he closes the intent loop or extends
the conformance one.

## 7. Adoptions made, with citations

Small, local, reversible adoptions executed in this session:

1. **Vocabulary, "anticipation burden."** Adopted as the name for the load a human carries when they
   must foresee every question an agent will fail to ask. Recorded in
   /Users/brien/.claude/projects/-Users-brien-Workspaces/memory/glossary.md, attributed to
   Wulveryck.
2. **Seam mediation vocabulary.** `joint` / `lent` / `contract` as the three states of a seam,
   describing who holds the comparator. Recorded in glossary and in this analysis, Q1. Not yet an
   attribute in the Contract model; adding it to `servers/models.py` is a larger change than this
   issue's scope and is queued rather than executed.
3. **Index registration.** This analysis is entry 8 in
   /Users/brien/Workspaces/Core/frameworks/intent/reference/external-patterns-index.md, with action
   rows.
4. **Position artifact.** POS-AGENTIC-001 in the Coherence Engineering repo, plus a source pointer in
   that repo's external/source-pointers/ index.

Queued rather than executed, because each is a scoped build rather than a side effect of filing
this analysis:

| Queue id | What |
|---|---|
| QMT-01M2P83PJMP08Q6J06HNDHGRKG | Define PSAE-001 with a real artifact, or retire the identifier from the two files that cite it |
| QMT-01M2P844R2JTD5EN79YB78T982 | Build a CON-COH identifier-resolution contract, the upstream control that closes SIG-COH-EXT-009 |
| QMT-01M2P846EKGKEA16E6FCPBTM39 | Add the `mediation` attribute (joint / lent / contract) to the Contract seam model |
| QMT-01M2P84M9FK8MEGZG1EAVR93DT | Add portfolio deprecation to the Observe phase spec, composed with retire-never-delete |
| QMT-01M2P84Q2EGMB3KVY7H687GNGS | Check for his promised third article after 2026-11-01 and revisit POS-AGENTIC-001 |

Deliberately **not** adopted:

- His five maturity criteria as a readiness checklist for any engagement. See Q5.
- A new seam type in the topology spec. See Q1.
- "Agentic factory" as a term. He does not define it; attributing a definition to him would be
  wrong.
