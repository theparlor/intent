---
decision_id: RETRO-2026-04-09-intent-rebuild-2
title: Four-zone progressive depth IA replaces three-pillar IA for intent-site
date: 2026-04-09
status: accepted
source: retroactive-extraction
session_date: 2026-04-09
references:
  - theparlor/intent-site:docs/v2-draft/pitch.html
  - theparlor/intent-site:docs/v2-draft/the-system.html
  - theparlor/intent-site:docs/v2-draft/the-build.html
  - theparlor/intent-site:docs/v2-draft/the-proof.html
---
# Four-zone progressive depth IA replaces three-pillar IA

## Context

The previous intent-site v1.2 used a three-pillar information architecture: The Story (pitch/concept-brief/methodology/walkthrough/roadmap), The System (work-system/flow-diagram/schemas/signals/dogfood/personas/etc.), The Build (architecture/agents/decisions/etc.). Panels flagged that this IA had three problems:

1. No progressive depth guidance — a reader landing on pitch didn't know how to go deeper
2. The Proof of the work was scattered across System and Build instead of having its own zone
3. The first-click experience from pitch dropped readers into shipped-product voice on the next page

Brien's initial instinct was to split the site into two properties (concept site + technical pressure-test site). The panels implicitly rejected this because two sites with two framings compounds the category-confusion problem they had already flagged.

## Decision

The v2-draft intent-site uses a four-zone progressive depth IA:

1. **Zone 1 — The Hypothesis** (pitch, lineage, ending, neutral-zone, who-loses, when-not) — the honest framing
2. **Zone 2 — The System** (how the loop actually runs — methodology, walkthrough, flow diagram, dogfood, signals, personas, events, onramp)
3. **Zone 3 — The Build** (technical substrate — architecture, agents, deployment, observability, ARB, decisions, schemas, hardening backlog)
4. **Zone 4 — The Proof** (evidence ledger — live dogfood, panel review, discovery wave, falsification criteria, disconfirmations)

Each zone has a landing page (pitch.html, the-system.html, the-build.html, the-proof.html) that gates access to the depth with v2 framing. Legacy v1.2 pages remain accessible via the zone landings but show a "v1.2 content" banner indicating their shipped-product voice is one version behind.

The nav across all v2-draft pages is consistent: `The Hypothesis · The System · The Build · The Proof`. The Intent logo links to pitch.html (not the legacy index) so readers never leave the v2 frame by accident.

## Alternatives Considered

1. **Two-site split** (Brien's initial instinct) — Rejected because it compounds F1 (no target user) and F3 (category confusion) by creating two audiences with two framings. The panels' recommendation was subtraction and sharpening, not more surface area. Cancelled unconditionally in DEC-20260409-02.

2. **Keep three-pillar IA and just rewrite content** — Rejected because the three pillars (Story/System/Build) buried the evidence layer. Readers evaluating Intent need a "show me the receipts" destination, which The Proof zone provides.

3. **Immediate full rewrite of all 23 legacy pages** — Rejected because it's 20+ pages of work and the critical path is the HYPOTHESIS framing + discovery interviews, not the technical rewrite. The legacy pages get the banner in S0 and full rewrite in S1+.

4. **Skip the zone landing pages and link directly to legacy** — Rejected. The whole point of the fix is to give readers honest context before they click into v1.2 content. Without zone landings, the narrative whiplash returns.

## Consequences

- 4 new landing pages shipped in v2-draft (pitch + the-system + the-build + the-proof)
- All 23 legacy pages got a v1.2 framing banner (via 5 parallel agent teams in S0)
- Nav structure must remain consistent: 4 zones, same order, on every v2-draft page
- The Proof zone exists as a first-class destination, meaning "evidence ledger" becomes a recurring structural element the site must maintain (not optional)
- Future sites for other products can use this 4-zone pattern as a template
- Legacy pages will be progressively rewritten with v2 framing in S1 and S2 rather than all at once
