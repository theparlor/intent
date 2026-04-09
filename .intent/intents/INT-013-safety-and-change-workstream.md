---
id: INT-013
title: "Safety + Change workstream — psychological safety contract, change management, infrastructure prerequisites"
status: proposed
proposed_by: "brien + panel-review-2026-04-09"
proposed_date: 2026-04-09T06:30:00Z
accepted_date:
signals: [SIG-049, SIG-053]
specs: []
owner: "brien"
priority: now
product: spec
---
# INT-013: Safety + Change workstream

## Problem

The 2026-04-09 multi-panel review identified two intertwined structural gaps in Intent's methodology:

1. **Psychological safety (SIG-049)** — flagged only by the Org Design panel, but flagged as the biggest latent failure mode in the entire methodology. Trust scoring becomes performance surveillance, signals-with-attribution become dossiers, spec clarity becomes individual critique, accountability diffuses across agent+human boundaries. Edmondson: *"Intent is built by engineers for engineers and treats safety as emergent. It isn't."*

2. **Change management** — flagged broadly by the Org Design panel as "a system design masquerading as a change program." The site is all "new beginning" with no ending, no neutral zone, no power-shift honesty, no Kotter-step-1 urgency translation, no onboarding-into-an-Intent-team story.

Brien's 2026-04-09 session answered three open questions that bear on this workstream:
- Trust scores exist to calibrate agent autonomy without interruptive human-in-the-loop
- The primary technical safeguard is reversibility — "knowing a reversible decision was made and can be reviewed later"
- Brien sensed Edmondson is pointing at "another factor" beyond reversibility — the interpersonal dimension — and explicitly opened the thread for further discussion

Brien also committed a new infrastructure prerequisite (SIG-053): Intent should not be used in environments lacking blue-green deployment, feature flags, automated testing, and visible change reporting.

These three elements — psychological safety, change management, and infrastructure prerequisites — are intertwined. They cannot be solved as separate tracks because each depends on the others. This intent wraps them into a single workstream.

## Desired Outcome

A coherent safety + change layer on Intent that:

1. **Ships the Psychological Safety Contract v1** with 10 enforceable promises covering the four Edmondson dimensions, the infrastructure prerequisites, and the interpersonal accountability norms (Promise 11 pending).

2. **Ships the Change Management Layer** — specific content and mechanisms addressing Bridges' ending/neutral-zone/new-beginning and Kotter's 8 steps, including:
   - An "Ending" page naming what teams release
   - A "Neutral Zone playbook" for weeks 3–8 of adoption
   - A "Who loses power" page with the explicit power-shift table
   - A "Week-by-week adoption playbook" with Kotter-step concretization
   - A "Guiding coalition template" (Kotter Step 2)
   - An "Onboarding a new hire to an Intent team" guide (Kotter Step 8)

3. **Ships the infrastructure prerequisites criterion** — a "When NOT to adopt Intent" page explicitly naming environments where Intent cannot safely operate (missing blue-green, missing automated testing, missing visible measurement, Theory X cultures, performance-review-driven cultures).

4. **Resolves the "Edmondson more" open thread** — either ships Promise 11 (social norms for failure attribution) or documents why the open thread remains unresolved and what the next step is.

5. **Integrates safety + change into Intent's tooling** — the Safety Contract is not just a page; it has enforcement mechanisms:
   - Required `used_for` field on trust score events
   - Required `visibility` field on signal capture
   - Required `failure_type` field on contract.assertion.failed events
   - `disagreement` and `trust-appeal` signal types as first-class primitives
   - Event schema checked for compliance before deploy

## Evidence

- **SIG-049** — Psychological safety never addressed (Org Design panel, critical)
- **SIG-053** — Measurability + visibility as infrastructure prerequisite (Brien, 2026-04-09)
- **Edmondson research** — *The Fearless Organization* (2018), *Right Kind of Wrong* (2023), *Teaming* (2012)
- **Bridges** — *Managing Transitions* (2009) on ending/neutral zone
- **Kotter** — *Leading Change* (1996) on 8 steps, 70% failure rate
- **Org Design panel verdict (2026-04-09)** — "A system design masquerading as a change program"
- **Methodology artifacts already written** — Edmondson four-dimensions analysis, Safety Contract v1, Change management analysis

## Constraints

- **Cannot be solved as three separate tracks.** Psych safety, change management, and infrastructure prerequisites are interdependent. Decoupling them breaks the coherence.
- **Cannot be solved with content alone.** The Safety Contract has enforcement mechanisms that require schema changes to signal/spec/event files. This is a cross-cutting methodology update.
- **Cannot be rushed.** The "Edmondson more" thread specifically requires more exploration with Brien. Promise 11 should not be written until that thread is resolved.
- **Cannot be optional.** Every team adopting Intent must read and sign the Safety Contract. Change management is not a "nice-to-have" for some adopters — it is a prerequisite for adoption in any culture that is not already Teal/self-managing.
- **Must distinguish prerequisites from recommendations.** The infrastructure prerequisites (blue-green, feature flags, automated testing, visible measurement) are HARD constraints. The change management practices are STRONG recommendations with cultural variation.

## Deliverables

### Phase 1 (this week — S0 execution)

- [x] `methodology/psychological-safety/01-edmondson-four-dimensions-analysis.md` — research foundation (DONE)
- [x] `methodology/psychological-safety/02-safety-contract-v1.md` — 10 promises, Promise 11 flagged as open (DONE)
- [x] `methodology/psychological-safety/03-change-management-analysis.md` — Bridges + Kotter applied (DONE)
- [ ] `site: new Ending page` — "What Intent asks you to release" (S0 deliverable)
- [ ] `site: new Neutral Zone playbook page` — weeks 3–8 of adoption (S0 deliverable)
- [ ] `site: new Who Loses page` — power-shift table with honest consequences (S0 deliverable)
- [ ] `site: new When NOT to Adopt page` — cultural + infrastructure exclusion criteria (S0 deliverable)

### Phase 2 (next week — S1)

- [ ] Trust score event schema updated with `used_for` field
- [ ] Signal schema updated with `visibility` field
- [ ] Contract assertion event schema updated with `failure_type` field
- [ ] `disagreement` and `trust-appeal` signal types added to template library
- [ ] Discovery interview protocol updated with cultural/infrastructure readiness questions (DONE)
- [ ] Pilot engagement intake checklist with safety + infrastructure assessment

### Phase 3 (week after — S2)

- [ ] Resolve "Edmondson more" thread with Brien → either Promise 11 draft or documented deferral
- [ ] Safety Contract v2 with full 11 promises
- [ ] Kotter 8-step adoption playbook with week-by-week milestones
- [ ] Guiding coalition template
- [ ] "Onboarding a new hire to an Intent team" guide
- [ ] Celebrate-intelligent-failure ritual spec

## Dependencies

- **Blocks:** Any team pilot invitation. Intent cannot be adopted by a team until at minimum the Safety Contract v1 is published and the Who Loses + When NOT to Adopt pages exist.
- **Blocked by:** Nothing. This work can proceed in parallel with INT-008 (subtraction), INT-012 (content rebuild), and INT-010 (discovery). In fact, it MUST proceed in parallel because the safety work informs the content rebuild.
- **Depends on:** INT-007 (panel-review primitive) for the "Edmondson is always in the panel" promise.

## Open questions

1. **How is "Promise 11" (social norms for failure attribution) designed?** Open thread with Brien. Needs a follow-up session specifically on the interpersonal dimension of safety beyond reversibility.

2. **How do we technically enforce `used_for` on trust score events?** The field requires downstream tools to declare purpose, but there's no runtime enforcement mechanism. This is the policy-vs-enforcement gap from Safety Contract Promise 1.

3. **Who validates that an adopting team meets the infrastructure prerequisites?** Self-assessment is vulnerable to optimism bias. Third-party assessment is expensive. What's the middle path?

4. **How do we surface signal silence as a safety signal?** The Safety Contract says silence is a leading indicator of unsafety, but we need a concrete mechanism — probably a monitored signal rate with alerts.

5. **What's the onboarding story for new hires into an already-Intent team?** Kotter Step 8 is a real gap — someone joining an Intent team walks into vocabulary and rituals that aren't in any standard PM or engineering onboarding.

## Relationship to other intents

- **INT-007 (panel-review primitive):** Safety Contract relies on the panel-review primitive to run safety-contract-check passes on new Intent capabilities. Bidirectional dependency.
- **INT-008 (subtraction pass):** Subtraction removes the multi-framing problem; INT-013 adds the honest "what you're releasing" framing. Complementary.
- **INT-010 (discovery interviews):** Discovery protocol was updated with cultural readiness questions from INT-013. Uses INT-013 outputs.
- **INT-011 (operator persona):** Operator persona includes safety-related known failure modes. Operator persona governance is agent-proposed-with-panel-review, which uses Safety Contract promises about disagreement protection.
- **INT-012 (content rebuild):** Content rebuild must include Safety Contract, Change Management pages, and When-NOT-to-Adopt section. INT-013 produces the content that INT-012 publishes.
- **INT-009 (architecture hardening):** P0/P1/P2 engineering work is necessary but not sufficient for safe adoption. Infrastructure prerequisites (SIG-053) depend on the adopter having equivalent infrastructure.

## Acceptance criteria

This intent is complete when:

1. Safety Contract v1 is published on the Intent site (not as a subpage — as a primary nav destination).
2. Ending, Neutral Zone, Who Loses, and When-NOT-to-Adopt pages exist on the site.
3. At least one external discovery interview (from INT-010) includes explicit psychological safety and infrastructure readiness questions, and the findings are incorporated into Safety Contract v2.
4. Trust score and signal event schemas include the required safety fields (used_for, visibility, failure_type).
5. The "Edmondson more" thread is either resolved (Promise 11 shipped) or explicitly deferred with a documented next step.
6. Brien has signed the Safety Contract v1 as the operator adopting Intent for their own work.

## Out of scope

- Full Kotter 8-step playbook customization for every adopter (we ship one standard version, adopters fork it)
- Automated safety contract compliance checking (manual review for v1, automation later)
- Cultural transformation consulting (Intent is not a change consultancy; we document, we don't facilitate)
- Individual psychological safety coaching (Intent is not therapy; we create conditions, we don't treat)
