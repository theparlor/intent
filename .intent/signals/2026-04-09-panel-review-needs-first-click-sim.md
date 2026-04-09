---
id: SIG-054
timestamp: 2026-04-09T08:15:00Z
source: conversation
confidence: 0.9
trust: 0.85
autonomy_level: L4
status: captured
cluster: panel-primitive
author: brien
related_intents: [INT-007]
referenced_by: []
parent_signal: SIG-041
---
# Panel-review needs a "first-click simulation" pass to catch nav-gap failures

Brien noticed the v2-draft site rebuild had a structural gap: the new story pages (pitch, lineage, ending, etc.) linked to `../architecture.html` for "The Build" — dropping readers back into the old v1.2 multi-framing site one click in. The panels that reviewed the v2-draft pitch content couldn't catch this because they were reading page content, not clicking through navigation.

**The meta-learning:** panel-review calls on content pages miss structural gaps that only appear when you actually follow the nav. A panel reading a single page as text will miss nav holes entirely because the next destination doesn't exist in their reading context.

## The new capability

The `panel-review` skill (INT-007) needs a new pass called `first-click-simulation`:

1. Take the target artifact (page or page set)
2. Parse all outbound links from the nav, sub-nav, and body
3. For each link, verify:
   a. Destination exists
   b. Destination belongs to the same "version" of the content (e.g., same IA, same voice, same maturity framing)
   c. Destination doesn't drop the reader into a conceptually different universe
4. Flag any link that fails (b) or (c) as a "narrative whiplash" finding
5. Include this pass in the `full-foundational` preset by default

The implementation can be lightweight: a sub-agent reads the target page, extracts links, follows each one, and asks "does this next page belong to the same site?" A page with v2 hypothesis framing linking to a page with v1 shipped-product framing is a fail.

## Why this is the panel-primitive's job, not a linter's job

A static linter could check link validity (404s). It cannot check *narrative consistency* — whether the destination page matches the voice and framing of the origin page. That requires reading both pages and making a judgment. That judgment is exactly what panel-review is for.

Specifically, the cold-visitor simulation (the 8th panel in the 2026-04-09 review) is the voice most likely to catch this. Cold visitors follow their curiosity through the nav and notice friction when the next page "feels different." A cold-visitor pass that explicitly clicks through the top 3-5 nav destinations on the target page would catch narrative whiplash reliably.

## Implication for panel-review skill spec

Update INT-007 to add `first-click-simulation` as a new preset or as a mandatory sub-pass of `content-review` and `full-foundational`. The sub-pass:

- **Input:** same as parent panel review
- **Execution:** dispatches a cold-visitor sub-agent that navigates the site
- **Output:** list of nav transitions with a voice-consistency score (0-1) and narrative-whiplash findings
- **Integration:** whiplash findings are promoted to the cross-cutting synthesis

## Trust Factors

- Clarity: 0.9 (specific failure mode, reproducible from this session)
- Blast radius: 0.2 (narrow enhancement to existing skill)
- Reversibility: 1.0
- Testability: 0.9 (can A/B on this specific rebuild — run panel before/after adding first-click-sim and see if it catches the nav gap)
- Precedent: 0.85 (Nielsen heuristic evaluation, Norman user journey mapping)

## Session context

Brien pointed this out after I shipped S0 batch 2. The v2-draft pages had:
- New 4-zone IA (Hypothesis / System / Build / Proof) — only The Hypothesis had pages
- Nav linking to `../architecture.html` because I hadn't built The System/Build/Proof landings yet
- First-click gap: reader goes pitch → clicks "The Build" → lands in v1.2 site with different voice

A panel reading pitch.html alone would have scored the page highly (clear user, honest framing, named lineage). A panel that *followed the nav* would have flagged F1a: "narrative breaks at first click." That second panel capability is what this signal asks for.

Confirmed by Brien in the same session: *"I have reviewed the first pages. the build is unchanged and links back to the old site. is that intentional?"*

Not intentional. Caught on the first click. Exactly the kind of thing first-click-simulation would have caught before shipping.
