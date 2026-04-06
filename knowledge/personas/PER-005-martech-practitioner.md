---
id: PER-005
type: persona
subtype: engagement
name: "M.A.R.S. Practitioner"
slug: martech-practitioner
confidence: 0.6
origin: agent
sources:
  - Work/Consulting/Engagements/Subaru/reference/Engagement_Context_and_SOW.md
  - Work/Consulting/Engagements/Subaru/ENGAGEMENT_INDEX.md
  - Work/Consulting/Engagements/Subaru/glossary.md
derived_from: []
exemplifies: []
engagement: Subaru
confidentiality: client-confidential
related_journeys: []
related_decisions: []
related_themes: []
pain_points:
  - "PP-001: JIRA is a reporting tool imposed on them, not a work management tool that helps them — they maintain it because they're told to, not because it makes their job easier"
  - "PP-002: Unclear how to write user stories for marketing technology work that doesn't map neatly to 'as a user I want' — the training examples feel disconnected from their reality"
  - "PP-003: Capacity is invisible — no one knows how much work they can actually take on, leading to over-commitment and reactive firefighting"
  - "PP-004: Dependencies across teams (e.g., Subaru.com depends on TechShare, Martech depends on QA) are managed through hallway conversations, not artifacts"
  - "PP-005: The 50/50 FTE/contractor split means half the team may not be around long enough to benefit from the transformation — knowledge leaves when contractors roll off"
voice_persona: null
created: 2026-04-06
updated: 2026-04-06
---
# Persona: M.A.R.S. Practitioner

## Who

Developer, engineer, QA analyst, or DevOps practitioner on one of the 6 in-scope M.A.R.S. teams. Approximately 156 staff mapped across the org (per the org chart extraction), working in teams of 4-6 people per stream. They execute the digital marketing campaigns, build and maintain Subaru.com and Subaru.net, manage shared services (TechShare), and provide QA and DevOps support.

This person is the individual contributor who shows up to standup, writes the code, files the JIRA tickets, and sits through the training sessions. The discovery session explicitly noted: **"Individual contributors are excited about the transformation."** That excitement is real but fragile — it survives only as long as the transformation makes their daily work better, not just more structured.

They are 99% onsite in Camden, NJ. Their work is a mix of project work (campaigns, feature builds) and keep-the-lights-on maintenance. They have a tech PO (not a business PO) — meaning product direction comes from within IT, not from marketing business partners.

## Behaviors

- Uses JIRA daily but in team-specific ways. Some teams use Kanban boards, others use custom workflows, some barely use it beyond ticket creation. The "no tooling consistency" finding from discovery is their lived experience.
- Excited about structure because they feel the pain of its absence. Dependencies surprise them. Capacity is a guess. Priorities shift without explanation. They want predictability — not for management's sake, but for their own sanity.
- Attends training sessions with mixed engagement. Topics that connect to their daily work (User Stories, Achieving Flow) land well. Abstract topics (Product Mindset, Challenging Assumptions) feel like they're for someone else — leadership, not ICs.
- Views consultants with cautious optimism. They've seen initiatives come and go. Turnberry is the latest. If the consultants help them solve real problems (dependency management, backlog hygiene), trust builds. If the consultants create more meetings, trust erodes.
- Works across the FTE/contractor boundary daily. Contractors do the same work but have different incentives (project-scoped, not transformation-scoped). This creates a two-speed team dynamic that no training curriculum addresses.
- Measures their own productivity in "things shipped," not velocity points or cycle time. The metrics the engagement introduces may feel like surveillance unless framed as team-level health indicators.

## Needs & Pain Points

- PP-001: JIRA is a reporting tool imposed on them, not a work management tool that helps them — they maintain it because they're told to, not because it makes their job easier
- PP-002: Unclear how to write user stories for marketing technology work that doesn't map neatly to "as a user I want" — the training examples feel disconnected from their reality
- PP-003: Capacity is invisible — no one knows how much work they can actually take on, leading to over-commitment and reactive firefighting
- PP-004: Dependencies across teams (e.g., Subaru.com depends on TechShare, Martech depends on QA) are managed through hallway conversations, not artifacts
- PP-005: The 50/50 FTE/contractor split means half the team may not be around long enough to benefit from the transformation — knowledge leaves when contractors roll off

## What They Need from the Engagement

- **JIRA that is their tool, not management's telescope.** The backlog classification scheme (keep-the-lights-on, enhancements, maintenance, defects, innovation) is useful IF it helps them protect capacity for innovation work instead of drowning in maintenance. If it just generates better reports for Greg, they'll fill it in mechanically.
- **Stories and examples from their domain.** "User stories for a digital marketing campaign deployment" is more useful than "user stories for an e-commerce checkout." The Agile Academy content needs martech-specific adaptation.
- **Dependency visibility without dependency ceremonies.** A cross-team dependency board in JIRA, maintained as part of natural workflow, is better than a weekly dependency standup that adds 30 minutes to the calendar.
- **Respect for the work that already works.** Some teams have functional processes. Acknowledging "you're already doing this well, here's how the standard approach formalizes what you've built" is more effective than "here's the right way."
- **Contractor inclusion.** If half the team isn't invited to transformation activities (or doesn't see the point), the transformation has a 50% ceiling.

## Evidence

- [Engagement Context & SOW](../../Work/Consulting/Engagements/Subaru/reference/Engagement_Context_and_SOW.md) — "Individual contributors are excited"; "no tooling consistency"; "managing capacity, predictability, dependencies" as key pain points; "POs will all be tech POs"; team composition (4-6 per stream)
- [Engagement Index](../../Work/Consulting/Engagements/Subaru/ENGAGEMENT_INDEX.md) — 157 staff mapped in org chart; 6 teams in scope; JIRA backlog classification categories
- [Subaru Glossary](../../Work/Consulting/Engagements/Subaru/glossary.md) — M.A.R.S. = Marketing Automation Retail Solutions; Martech = specific team within M.A.R.S.

## Open Questions

- How do ICs currently prioritize their own work? Is it lead-assigned, self-selected, or queue-based?
- What is the support model burden? How much time goes to production support vs. project work? This ratio determines how much sprint capacity is actually plannable.
- Do contractors attend training and coaching sessions? If so, do they see value or view it as overhead?
- Which teams have the most functional existing processes? These are adoption leaders, not remediation targets.
- Are any ICs already practicing Agile informally (e.g., personal Kanban, pair programming) without org support?
