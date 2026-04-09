---
id: INT-010
title: "Run 10 external discovery interviews — close the N=1 gap"
status: proposed
proposed_by: "panel-review-2026-04-09"
proposed_date: 2026-04-09T05:02:00Z
accepted_date:
signals: [SIG-043]
specs: []
owner: "brien"
priority: now
product: notice
---
# Run 10 external discovery interviews — close the N=1 gap

## Problem

The site claims "continuous discovery" via 43 signals, 19 specs, 19 decisions — but every signal prior to this review was internal. SIG-010 ("Ari") is the single external practitioner voice. Four panels (Product Strategy, Strategy/Systems, Discovery/UX, Org Design) independently flagged this as the critical credibility gap.

No amount of honest hypothesis framing, better copy, or architectural hardening compensates for zero external evidence. This is the Torres/Cagan/Blank/Fitzpatrick unanimous call: 10 interviews before any content redesign.

## Desired Outcome

10 structured discovery interviews with senior ICs and PMs using Claude Code (or equivalent AI dev tools) daily. Each interview:

- Follows the Mom Test protocol (no leading questions, observe current behavior, avoid "would you use...")
- Focuses on current pain points in spec-to-execution flow with AI tools
- Captures verbatim quotes (not paraphrased)
- Produces a signal file in `.intent/signals/external/` (new subdirectory)
- Feeds an opportunity tree synthesis

### Deliverables

- 10 signal files: `2026-04-XX-interview-[participant-slug].md` in `.intent/signals/external/`
- One synthesis document: `knowledge/themes/THM-external-discovery-wave-1.md`
- One opportunity tree: `knowledge/domain-models/DOM-spec-pain-OST.md`
- One new site page: `external-signals.html` showing these alongside internal dogfooding (once site subtraction is complete)

### Interview target profile

- Senior IC or PM (5+ years experience)
- Uses Claude Code, Cursor, Copilot, or equivalent daily for 3+ months
- Ships code or specs in a team context (not solo hobby)
- Mix of: engineering leads, staff engineers, senior PMs, principal PMs
- Geographic spread not required; domain spread is (not all SaaS)

## Evidence

- **SIG-043:** Discovery theater — 42 internal signals, 1 external voice
- **SIG-042:** No target user — interviews will surface the target user profile
- Panel consensus: Product/Strategy/Discovery/Org Design all independently called for this

## Constraints

- Cannot be auto-executed — requires Brien to schedule and conduct
- Cannot be faked with agent-generated personas — must be real humans
- Must follow Mom Test to avoid confirmation bias (no leading questions)
- Interviews published with participant consent; anonymized if preferred
- Target completion: 2 weeks from today (2026-04-23)

## Open Questions

- Who are the 10? Need to draft a candidate list from Brien's network
- Remote-only or mix in-person? Remote likely — faster to schedule
- 30-min or 60-min? Recommend 45-min (enough for 3-4 pain stories, not so long people cancel)
- Incentive? Offer to share synthesis privately with participants as thank-you

## Relationship to panel-review primitive (INT-007)

Once 10 external signals exist, they become input to panel reviews. "Given these 10 real practitioner pain points, how should the pitch be rewritten?" becomes a panel call with real evidence instead of internal assumptions.

## Out of Scope

- Quantitative survey (different tool, different skill)
- Public-facing case studies (those come after engagement, not discovery)
- Recruiting participants for pilot use (discovery first, pilot second)
