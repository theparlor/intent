---
id: PER-003
type: persona
subtype: stakeholder
name: "Transformation Sponsor"
slug: transformation-sponsor
confidence: 0.6
origin: agent
sources:
  - Work/Consulting/Engagements/Subaru/reference/Engagement_Context_and_SOW.md
  - Work/Consulting/Engagements/Subaru/ENGAGEMENT_INDEX.md
derived_from: []
exemplifies: []
engagement: Subaru
confidentiality: client-confidential
related_journeys: []
related_decisions: []
related_themes:
  - THM-001
pain_points:
  - "PP-001: No visibility into team capacity, velocity, or predictability — cannot make resource allocation decisions with confidence"
  - "PP-002: Inconsistent JIRA usage across teams makes cross-team reporting impossible — every dashboard is a manual assembly job"
  - "PP-003: Leadership is perceived as the historical barrier to transformation — must demonstrate personal buy-in without losing credibility if the initiative stalls"
  - "PP-004: Business demand for faster delivery outpaces the org's ability to absorb process change — pressure from above and resistance from within"
  - "PP-005: Prior transformation attempts stalled because they lacked executive sponsorship — this time CIO is the catalyst, but the proving ground is Greg's org"
voice_persona: null
created: 2026-04-06
updated: 2026-04-06
---
# Persona: Transformation Sponsor

## Who

VP-level executive sponsoring the Agile transformation within M.A.R.S. and Retail Systems. Greg Giuffrida is the archetype — leads a ~120-person IT organization (50/50 FTE/contractor mix) across 6 teams, reports to a newly promoted CIO (Laura Matey) who is the transformation catalyst.

This person did not initiate the transformation — it was catalyzed from above — but they own the proving ground. Their org (M.A.R.S. Platforms) is where the engagement must demonstrate enough value to justify expansion to the broader IT organization. They carry the political risk: if this fails, it fails visibly in their domain.

They have a director (Gino Guarnere) who is the day-to-day operational lead and who brings prior Scrum experience from Comcast. The sponsor delegates execution but retains accountability for outcomes.

## Behaviors

- Speaks in outcomes: "I want all my teams on the same cadences, using the same tools, with artifacts in JIRA." Operational consistency is the proxy metric for transformation health.
- Evaluates through dashboards, not ceremonies. Wants leader-level views that roll up team-level data without requiring attendance at stand-ups or retrospectives.
- Delegates tactical transformation to Turnberry but stays close enough to course-correct. Expects bi-weekly status reports and platform leader coaching sessions.
- Compares current state against aspirational state ("here and now" framing from discovery sessions). Impatient with process explanations — wants to see the delta.
- Risk-averse on tooling decisions that could disrupt current production work. Wants JIRA standardization to happen without breaking existing team workflows during migration.
- Politically aware: knows the CIO is watching this as a proof point. Will escalate blockers quickly but also buffer the teams from executive pressure.

## Decision Authority

- **Approves:** Expansion scope (which teams come next), budget allocation for Turnberry resources, go/no-go on PI Planning format, escalation to CIO
- **Delegates:** JIRA configuration decisions (to Omar/Gino), training sequencing (to Jason/Dean), coaching cadence (to Dean/Brien)
- **Influenced by:** CIO Laura Matey's transformation vision, Gino's operational feedback, Turnberry's bi-weekly status reports, team scorecard metrics (once established)

## Risk Posture

Conservative-pragmatic. Will invest in the transformation but needs early proof points to sustain commitment. The 20-week engagement timeline creates a forcing function — PI Planning #0 at Week 6 is the first visible checkpoint where the sponsor evaluates whether the investment is tracking.

Key fear: that the transformation becomes a training exercise without behavior change. Wants to see teams actually using the ceremonies and artifacts post-training, not just attending workshops.

Secondary fear: that standardization creates rebellion. Some teams have functional (if inconsistent) JIRA setups. Forcing migration risks the "why fix what works" pushback from team leads.

## Engagement Leverage Points

- **Dashboard-first reporting** — Give this person a leader-level JIRA dashboard that shows velocity, predictability, and cycle time across all 6 teams. This is the single highest-value artifact for sustaining sponsorship.
- **Expansion narrative** — Frame M.A.R.S. success in terms that translate to CRM, ERP, and Data & Analytics teams. The sponsor needs to tell the CIO a story about scalability.
- **Early wins in JIRA consistency** — Even cosmetic standardization (consistent issue types, backlog classification) signals progress. Ship visible changes before deep process changes.
- **Buffer the teams from "transformation theater"** — Help the sponsor distinguish between real adoption signals and performative compliance. Team health metrics matter more than ceremony attendance.

## Needs & Pain Points

- PP-001: No visibility into team capacity, velocity, or predictability — cannot make resource allocation decisions with confidence
- PP-002: Inconsistent JIRA usage across teams makes cross-team reporting impossible — every dashboard is a manual assembly job
- PP-003: Leadership is perceived as the historical barrier to transformation — must demonstrate personal buy-in without losing credibility if the initiative stalls
- PP-004: Business demand for faster delivery outpaces the org's ability to absorb process change — pressure from above and resistance from within
- PP-005: Prior transformation attempts stalled because they lacked executive sponsorship — this time CIO is the catalyst, but the proving ground is Greg's org

## Evidence

- [Engagement Context & SOW](../../Work/Consulting/Engagements/Subaru/reference/Engagement_Context_and_SOW.md) — Discovery session notes document "leadership holding us back" observation and Greg's "here and now" aspiration
- [Engagement Index](../../Work/Consulting/Engagements/Subaru/ENGAGEMENT_INDEX.md) — Org structure, team count, key relationships
- Discovery session 12/11 Focus Forward — Pain points around capacity, predictability, dependencies

## Open Questions

- How does Greg measure success personally vs. what he reports to the CIO? Are they the same metrics?
- What is Greg's appetite for changing team composition (adding business POs) vs. keeping tech POs?
- How does the 50/50 FTE/contractor split affect Greg's willingness to invest in people vs. process? Contractors may not be retained long enough to benefit from transformation.
- What happened in prior transformation attempts that stalled? Was it Greg's org or elsewhere?
