# Participant Profile — Discovery Wave 1

## The target

We are looking for 10 people who match this profile:

### Must have

1. **Role level:** Senior IC or higher. Specifically:
   - Senior Engineer (5+ years) OR
   - Staff / Principal Engineer OR
   - Senior Product Manager (5+ years) OR
   - Principal / Group Product Manager OR
   - Engineering Manager of a 5–15 person team

2. **AI tool usage:** Daily use of Claude Code, Cursor, Copilot, or equivalent for at least 3 months. "Daily" means they touched the tool on most working days, not "I tried it once and it was cool."

3. **Ships work in a team context:** Not a solo hobbyist. Code/specs/decisions go through review, merge, deploy — there's a team rhythm around their work.

4. **Opinionated:** They've already formed opinions about what's working and what isn't. (Proxy: they've complained on record at least once, or shipped a tool/hack to solve a problem.)

### Nice to have

- Mix of domains: 3 SaaS, 2 platform/infra, 2 consumer, 2 B2B, 1 regulated (fintech/health)
- Mix of company stages: 2 startup (<30 eng), 4 scaleup (30-300), 3 mid-enterprise (300-3000), 1 large enterprise (3000+)
- Mix of tenure: 2 new-in-role (<12mo), 6 established (1-5yr), 2 long-tenured (5yr+)
- Mix of geo (at least: North America, EU, non-US/EU representation)
- Mix of post-Jira status: some still using Jira, some moved to Linear/Shortcut, some using nothing structured

### Must NOT be

- Friends who will tell us what we want to hear (polite lies destroy discovery)
- People we've pitched Intent to already (their responses are contaminated)
- People who report to us or are dependent on us in any way (power asymmetry kills candor)
- Vendors with competing products (conflict of interest)
- AI thought-leader influencers (they give performative answers, not behavioral ones)

## The recruitment funnel

Expect to contact ~25 people to land 10 interviews.

- **Tier 1 (direct ask, warm):** People Brien has worked with, respects, and can ask directly. Target: 8 contacts → 5 interviews.
- **Tier 2 (network referral, 1 hop):** Asked of Tier 1 participants "who else should I be talking to?" — plus direct ask through Brien's broader network. Target: 10 contacts → 4 interviews.
- **Tier 3 (cold outreach):** LinkedIn / Slack communities / direct message to people matching the profile who don't know Brien. Target: 7 contacts → 1 interview.

Tier 3 is intentional — it surfaces the voice of people Brien doesn't already hear from. That voice is often the most valuable.

## Candidate list worksheet

**Committed target user (per DEC-20260409-02):** Staff+ engineers on teams of 2–7 using Claude Code daily. Sweet spot teams of 2–5. Reaches solo practitioners (team of 1) and up to 7. Teams over 7 are out of scope.

Seed list from Brien (2026-04-09):

| # | Name | Role | Company | Tier | AI tool | Contact method | Known friction? | Risk of polite lies? | Status |
|---|------|------|---------|------|---------|----------------|-----------------|---------------------|--------|
| 1 | Chris Markus | TBD | TBD | 1 | Claude Code | Direct | TBD | MEDIUM — warm | Reach out |
| 2 | Ari Amari | TBD | TBD | 1 | Claude Code | Direct | YES (SIG-010 origin — independently described the Intent pattern) | **HIGH — already primed** | Reach out, see note below |
| 3 | Devin [last name TBD] | TBD | TBD | 1 | TBD | Slack | TBD | MEDIUM — warm | Brien: confirm last name |
| 4 | Zak [last name TBD] | TBD | TBD | 1 | TBD | Slack | TBD | MEDIUM — warm | Brien: confirm last name |
| 5–10 | "A few others reachable via Slack" | TBD | TBD | 1/2 | TBD | Slack | TBD | TBD | Brien: identify before week 2 start |
| +3-5 backup | Tier 2 referrals | TBD | — | 2 | — | Referred by Tier 1 | — | LOW | Generated during the wave |
| +cold | Tier 3 cold outreach | TBD | — | 3 | — | LinkedIn/cold DM | — | LOW | Required to hit 10 — Brien should NOT skip this tier |

### IMPORTANT note on Ari Amari

Ari is the original external voice from SIG-010 — the conversation that seeded INT-003 and served as the single cited external practitioner for the entire Intent methodology until this discovery wave. There are two issues:

1. **Ari is already primed.** Ari has heard about the hypothesis, has been cited back to themselves, and has social reason to confirm the framing. This is classic confirmation bias risk.
2. **Ari may have moved on.** What Ari said a year ago may not match what Ari would say today about their actual current experience.

**Recommendation:** Include Ari as a *follow-up* interview with a specific charter: "you described something a year ago that turned into a methodology — does that methodology match what you were describing? What would you say differently today?" Treat Ari's interview as *validation with known bias*, not as a fresh signal. Do not weight Ari's confirmation signals highly in the synthesis.

### Gap analysis on Brien's seed list

Brien's current seed list is **all Tier 1 warm contacts**. This is good for getting started, but the protocol requires:

- **Tier 1 (warm, direct ask):** 8 contacts → 5 interviews. Brien has 4–5 named, need 3–4 more.
- **Tier 2 (referrals):** 10 contacts → 4 interviews. Generated from Tier 1 asks — not pre-populated.
- **Tier 3 (cold):** 7 contacts → 1 interview. **Brien has NOT listed any Tier 3 candidates.** This is a gap.

**Required action for Brien before week 2:**
1. Confirm Devin's and Zak's last names + contact method
2. Identify 4–6 additional Tier 1 warm contacts from Slack network
3. Identify at least 5 Tier 3 cold outreach candidates — people Brien does NOT already know. LinkedIn search for "staff engineer" + "Claude Code daily" or similar.

**Why Tier 3 matters:** The single highest-value signal in discovery is often from someone who has no social reason to agree with you. If the entire wave is Brien's network, the wave is an echo chamber with a dashboard.

### Infrastructure readiness filter

Per DEC-20260409-02 (answer 5), Intent has infrastructure prerequisites: blue-green/feature flags, automated testing, measurable and visible metrics. Add this filter to candidate screening:

- Does the candidate's team have deploy rollback capability?
- Does their team have automated testing as a real practice (not aspirational)?
- Are their product/engineering outcomes measurable and visible?

Candidates whose teams lack this infrastructure are STILL valuable interviews — they represent the "when NOT to adopt" population, and their pain is important to hear. But they should not be the majority of the sample. Target: 7 of 10 from infrastructure-ready teams, 3 of 10 from infrastructure-gap teams (to validate the exclusion criterion).

## Selection tradeoffs

The temptation is to pick the 10 people most likely to confirm the hypothesis. Resist it. Specifically:

- **Include 2-3 skeptics.** People you suspect will say "I don't have that problem, my process works fine." If they surprise you, great. If they confirm, also great — it means the hypothesis fails in their world and we learn the boundary.
- **Include 1-2 people outside the assumed target.** An SRE, a designer, a data engineer. They will tell you if the "spec clarity" bottleneck generalizes or is engineering-specific.
- **Exclude the 2-3 most enthusiastic Intent allies.** They'll confirm everything and teach us nothing.

## Disqualifying signals during outreach

If a candidate:
- Responds with "I love this idea, tell me more!" — deprioritize (they're primed)
- Asks for a demo before the interview — hard no (contaminates the data)
- Is a recruiter or sales rep — no (not an end user)
- Hasn't actually used AI tools daily in 3+ months — politely defer
- Is in an NDA context that would block them from discussing workflow — respect it, move on
