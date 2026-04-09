---
id: DEC-20260409-02
title: "Brien's answers to 5 open questions from the post-panel plan"
date: 2026-04-09
status: decided
supersedes: partial-overlay on DEC-20260409-01
author: brien
related_signals: [SIG-042, SIG-043, SIG-049, SIG-048, SIG-053]
related_intents: [INT-008, INT-010, INT-011, INT-012]
---
# DEC-20260409-02: Five open-question answers (commit before week 1)

## Context

DEC-20260409-01 closed with five open questions that Brien needed to answer before the week-1 execution could start. This decision records the answers, ratifies the parts of DEC-20260409-01 that needed explicit confirmation, and opens one new exploration thread.

## Answer 1 — Target user is committed

**Brien:** *"staff+ engineers on teams using Claude Code. I would think the sweet spot is teams of 2-5 but I think it will reach down to 1 and up to 7. Over 7 is an overly large team that doesn't work well in any model."*

**Committed target user:**

> **Intent is for staff+ engineers on teams of 2–7 using Claude Code daily. Sweet spot: teams of 2–5. Reaches down to solo practitioners (team of 1) and up to 7. Teams over 7 are out of scope — Intent is not optimized for large-team coordination, and neither is any other serious methodology.**

**What this means for the subtraction pass (INT-008):**
- Hero copy on pitch.html names this user explicitly
- Every alternative framing gets deleted
- Team size bracket (2–7, sweet spot 2–5) appears in the concept brief and in every discovery conversation
- The "solo reach-down" path is a real path, not an afterthought — there are solo practitioners in this space and they are valid users

**What this means for discovery (INT-010):**
- Participant profile is narrowed to match: staff+ engineers, 2–7 person teams, Claude Code daily
- The team-size question is a first-pass filter in the recruitment outreach

## Answer 2 — Discovery participants seed list

**Brien:** *"do you mean real world humans? I have Chris Markus, Ari Amari, Devin, Zak, and a few others reachable via Slack."*

**Seed participant list (4 named, ~6 TBD):**

| # | Name | Source | Status |
|---|------|--------|--------|
| 1 | Chris Markus | Brien's network | Reach out |
| 2 | Ari Amari | Brien's network (SIG-010 origin) | Reach out |
| 3 | Devin | Brien's network | Reach out (need last name) |
| 4 | Zak | Brien's network | Reach out (need last name) |
| 5-10 | "A few others reachable via Slack" | Brien's network | Brien to identify |
| +3-5 backup | Tier 2/3 referrals | Pending | Generated during the wave |

**Note on Ari Amari:** This is almost certainly the "Ari" from SIG-010, the original external practitioner whose conversation seeded INT-003 ("spec product"). If so, the upcoming interview should treat Ari as a follow-up with a specific charter: "you described something a year ago that turned into a methodology — does that methodology match what you were describing?" This is a valuable validation opportunity AND a risk (confirmation bias — Ari is already primed).

**Action for Brien (week 1):**
- Confirm last names for Devin and Zak
- Identify the remaining 6 candidates from Slack network
- Fill in the participant profile worksheet at `.intent/discovery/wave-1/03-participant-profile.md`

**Protocol reminder:** The interview protocol specifically says to include 2-3 skeptics and 1-2 people outside the assumed target. Brien's seed list is all warm contacts — that's Tier 1. We still need Tier 2 (referrals) and Tier 3 (cold) to hit 10. Relying on 10 warm contacts produces a confirmation-bias echo chamber.

## Answer 3 — Operator persona governance

**Brien:** *"agent proposed with review, and here we can again introduce and use the panel."*

**Governance model for operator personas (updates INT-011):**

1. **Agent-proposed updates.** Any agent can propose an update to an operator persona based on session observations. The proposal is a signal file in `.intent/signals/` with type `operator-persona-update`.

2. **Panel review mandatory.** Before an operator persona update is accepted, it goes through a panel-review call. Required panel members:
   - **Operator in question** (self-persona voice — reads the update against its own known patterns)
   - **Org Design panel member** (Edmondson or similar) — checks the update against psych safety dimensions
   - **Relevant foundational voices** depending on what's being updated

3. **Brien ratifies.** After panel review, Brien either accepts, revises, or rejects the update. Rejections are logged — they become signals about what doesn't fit.

4. **Versioning.** Operator personas are versioned. Each update produces a new version with a changelog. Old versions are not deleted — they document the operator's evolution.

**This is the first recursive use of the panel-review primitive:** the panel that reviews Intent's own artifacts now also reviews updates to the personas the panel uses. This is double-loop at the registry level.

**Implication for INT-011:** The governance section of INT-011 is now concrete. It was "open question" in v1; it is "agent-proposed with panel review" in v2.

## Answer 4 — Two-site split is cancelled

**Brien:** *"cancel the split, i accept the feedback. i misunderstood the problem the panel raised."*

**Ratified:** DEC-20260409-01's rejection of the two-site split is now unconditional. No exit criterion needed because the decision is not reversible from this side — the reason to split (serving two audiences) was identified as the wrong frame. There is one audience (staff+ engineers on 2–7 person teams using Claude Code) and it gets one site with progressive depth.

**What this means operationally:**
- No new repos are created for the "technical pressure-test site" concept
- All content consolidation happens in `theparlor/intent-site`
- The archive folder (`docs/archive/v1.2-multi-framing/`) is the ONLY site content archival — no second-site archive is needed
- Week 1 subtraction pass proceeds as planned with renewed clarity

## Answer 5 — Trust scores: Brien's stance + blue-green prerequisite + measurability principle

**Brien:** *"the trust scores are designed for us to consider the current maturity of our agents and identify the risk of tasks we face and use those to calibrate our trust for decision making without interuptive human in the loop. knowing a reversible decision was made and can be reviewed later is my measure but i feel like edmondson is teasing at another factor. so we should talk more."*

Plus: *"we should explicitly pursue blue green environments and feature flag change management so that the code can advance but humans are still required to accept the result of a potential multitude of impactful changes. we will also need significant automated testing and change reporting. if your development and your product isn't measurable and the measures visible it shouldn't be using our approach. it lacks the ability to generate and rely on valid signals."*

**This answer contains four distinct decisions:**

### 5a. The explicit purpose of trust scores (committed)

Trust scores are for:
1. Considering the current maturity of our agents
2. Identifying the risk of tasks we face
3. Calibrating our trust for decision-making without interruptive human-in-the-loop

Trust scores are NOT for (per the Psychological Safety Contract Promise 1):
- Performance reviews, compensation, promotion, PIPs, firing decisions, team comparison, manager dashboards.

### 5b. Reversibility as the primary safeguard (committed)

Brien's stated measure: "knowing a reversible decision was made and can be reviewed later."

This becomes a first-class design criterion. If a decision cannot be reversed or reviewed later, it should NOT be in the L3/L4 autonomy bracket regardless of trust score. This is a hard constraint on the trust formula that is currently implicit.

### 5c. The "Edmondson more" factor (open — needs exploration)

Brien senses correctly that Edmondson is pointing at something beyond reversibility. My read of what she's pointing at, for discussion:

**Reversibility is a rational safety concern. Edmondson's safety is an interpersonal safety concern.** Even a fully reversible decision can be socially punishing for the person who made it. A team can have perfect blue-green / feature-flag infrastructure and still be psychologically unsafe if the person who authorized an L4 action gets shamed when it goes sideways.

The "more" factor is the human reputational cost of having been associated with a failed decision — which is independent of the decision's technical reversibility. Edmondson's research specifically shows that teams with high safety report MORE errors not because errors are reversible, but because the humans who made them aren't punished socially.

**Implication for the Safety Contract:** Promise 4 (distinguished failure types) and Promise 5 (explicit accountability routing) already start to address this. But there may be a missing Promise — something about **social accountability norms**, not just technical accountability fields. Tag for further exploration with Brien.

### 5d. Blue-green + feature flags + automated testing as infrastructure prerequisites (NEW — becomes a design constraint)

**This is a significant new decision.** Intent now has explicit infrastructure prerequisites for safe adoption:

1. **Blue-green deployment or equivalent reversibility infrastructure** — the code can advance but the result must be accepted by humans before rollout
2. **Feature flag change management** — impactful changes are gated behind flags that humans control
3. **Significant automated testing** — signals about outcomes depend on tests that actually run and report
4. **Change reporting** — the measures must be visible, not hidden in dashboards nobody checks

**The load-bearing principle:**

> **If your development and your product isn't measurable and the measures aren't visible, it shouldn't be using our approach. It lacks the ability to generate and rely on valid signals.**

This is a new first-class criterion. It becomes:

- A filter on discovery interviews (is the participant's environment measurable?)
- A filter on pilot adoption (does the adopting team have the infrastructure?)
- A new section on the site (when NOT to adopt Intent)
- A new design constraint on the trust formula (reversibility is only meaningful if the infrastructure supports it)

**New signal:** SIG-053 — "Intent requires measurability + visibility as infrastructure prerequisite."

### 5e. "So we should talk more" (not closed)

Brien explicitly flagged that the Edmondson "more" factor needs more discussion. This is a DEFERRED decision — it is not closed today, and the open thread is tracked.

**Thread for next session:** What is the interpersonal/social dimension of the Safety Contract that reversibility alone doesn't cover? How do we design for it explicitly without being preachy?

## Consequences

### Positive

- The target user is now a specific, committable sentence. Week 1 subtraction can execute without ambiguity.
- The operator persona governance model closes a major gap in INT-011.
- The blue-green prerequisite + measurability principle gives Intent a clean "when NOT to adopt" statement, which is itself a positioning advantage (per Dunford, naming who you're not for is category clarity).
- The two-site question is closed. No second-guessing.

### Negative

- The target user commit may be wrong. If discovery interviews reveal a different natural user, we'll need to reopen. That's a feature of discovery, not a bug.
- The blue-green prerequisite narrows the addressable market. Teams without modern deployment infrastructure cannot adopt Intent safely, which is a large exclusion. This is the right call — unsafe adoption is worse than no adoption — but it has business consequences that should be named.
- The "Edmondson more" thread is open. Until we work through it, the Safety Contract v1 is provisionally incomplete on Dimension 3 and Dimension 4.

## Next actions (updates to existing plan)

1. **DEC-20260409-01 updated** — target user committed, two-site split unconditionally cancelled.
2. **INT-008 (subtraction)** — hero copy target sentence locked in.
3. **INT-010 (discovery)** — seed participant list captured; target user filter updated.
4. **INT-011 (operator persona)** — governance model committed: agent-proposed with panel review, Brien ratifies.
5. **INT-012 (content rebuild)** — add "when NOT to adopt" section as prerequisite; add measurability principle as structural criterion.
6. **Safety Contract v1** — add Brien's stance on trust score purpose (5a); add Promise 10 for infrastructure prerequisites; flag the "Edmondson more" open thread for next session.
7. **SIG-053 (new)** — "Intent requires measurability + visibility as infrastructure prerequisite"
8. **Discovery protocol** — add cultural/infrastructure readiness questions to the interview protocol.

## Lineage

- DEC-20260409-01 — parent decision
- Amy Edmondson — the "interpersonal safety beyond reversibility" thread
- Jez Humble / Dave Farley — blue-green and feature flag practices (Continuous Delivery)
- Nicole Forsgren — Accelerate, DORA metrics, measurability as prerequisite for improvement
- Richard Rumelt — "name who you're not for" as strategic clarity
