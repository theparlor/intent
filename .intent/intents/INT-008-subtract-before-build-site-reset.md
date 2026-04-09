---
id: INT-008
title: "Ruthless subtraction pass on intent-site before any new content"
status: proposed
proposed_by: "panel-review-2026-04-09"
proposed_date: 2026-04-09T04:58:00Z
accepted_date:
signals: [SIG-042, SIG-044, SIG-045, SIG-052]
specs: []
owner: "brien"
priority: now
product: spec
---
# Ruthless subtraction pass on intent-site before any new content

## Problem

Six of eight panels flagged "no target user" and "six category framings." Brien's reflex is to build new material in new repos. The panels said the opposite: subtract and sharpen before adding surface area.

Both moves are valid, but the sequence matters. Building before subtracting compounds the category confusion — two sites serving two audiences is worse than one site serving no one because the math gets exponentially worse.

## Desired Outcome

Current intent-site undergoes a one-week subtraction pass BEFORE any new content or new repos are built.

### Deletions

1. **Five of six category framings deleted from every page.** Keep ONE. Candidate: "Specification-driven operating loop for AI-native engineering teams."
2. **Every "Intent does..." rewritten as "you will..."** — reader becomes the hero.
3. **All multi-product framing deleted from the hero.** The four-products / three-layers / eight-products framings move to /depth pages or get archived entirely.
4. **Decisions pages reframed** — remove claims about production readiness, multi-tenant deployment, etc. Label what's tablestakes vs evolutionary vs open question.
5. **Products.html archived as-is** — the flat catalog tries to sell 8 products at once, which is the category confusion factory. Keep it accessible via /archive/ for honesty but remove from main nav.

### Archival

- Move current intent-site content to `/archive/v1.2-multi-framing/` subfolder on main branch
- Preserve review-2026-04-09.html in main (it's the artifact that drove this reset)
- Keep walkthrough.html, dogfood.html, getting-started.html, methodology.html (panels praised these) but subject them to the "delete 5 framings" pass
- Archive: pitch.html, concept-brief.html, roadmap.html, work-system.html, products.html (current versions)

### Replacement

One new pitch.html, one new concept-brief.html — built from the hypothesis framing (SIG-047) and the lineage acknowledgment (SIG-046). Everything else waits.

## Evidence

- **SIG-042:** No target user — 6/8 panels flagged
- **SIG-044:** Category confusion — 6 framings across 6 pages
- **SIG-045:** Reader is never the hero
- **SIG-052:** Brien's "build more" reflex vs. panels' "subtract more" recommendation

## Constraints

- Must NOT build the new content until the subtraction is complete
- Must preserve all archived content in git history (for accountability)
- Must retain the review document (review-2026-04-09.html) as the forcing function
- Must NOT split into two sites — one site, layered depth, progressive disclosure
- Target: 30% reduction in total site content by end of week

## Open Questions

- Does Brien accept the one-site instinct, or does he want to proceed with two-site split against this advice?
- Who is the named target user? "Practitioner-architect" is close but needs sharpening.
- What's the single category claim? Draft candidates in the spec.

## Out of Scope

- New material (blocked until after subtraction)
- Engineering hardening (separate track, INT-009)
- Discovery interviews (separate track, INT-010)
