---
signal_id: RETRO-2026-04-09-intent-rebuild-SIG-2
title: First-click nav integrity needs a navigation-following simulation pass in panel-review
severity: medium
detected: 2026-04-09
status: open
source: retroactive-extraction
trust_score: 0.9
autonomy: L3
related_signals: [theparlor/intent:.intent/signals/2026-04-09-panel-review-needs-first-click-sim.md]
---
# First-click nav integrity needs a simulation pass in panel-review

## Observation

After the v2-draft intent-site rebuild shipped in S0, Brien reviewed the pitch.html page and immediately caught a structural gap: the Intent logo and "The Build" nav link both pointed to `../architecture.html` (the legacy v1.2 site) instead of staying within v2-draft. One click from pitch.html dropped the reader into a completely different voice and framing.

The 2026-04-09 panel review had run on the LEGACY site and produced 10 findings, all text-level critiques of individual pages. No panel flagged the nav consistency issue for the v2-draft rebuild because:
1. The v2-draft didn't exist when the review ran
2. Panels reading single page contents don't follow nav links
3. "Narrative consistency across nav transitions" is a structural property that emerges from clicking through multiple pages, not reading one

Brien caught it in ~10 seconds with his eyes. The panel-review primitive couldn't catch it because it has no navigation-following capability.

## Context

This is a specific instance of a general pattern: panels reading individual artifacts miss structural gaps that only appear when you follow the nav from page to page. A page can be perfect in isolation and still break the site-wide narrative the moment a reader clicks the wrong link.

The 2026-04-09 intent-site rebuild had multiple such transitions:
- Pitch → The Build: broken (pointed to legacy)
- Pitch → The System: broken (pointed to legacy)
- Pitch logo click: broken (pointed to legacy index)
- Every v2-draft page's logo click: broken

All fixed via explicit Edit operations after Brien flagged the first one. But the panel-review primitive had no way to catch this automatically.

## Implication

1. **Panel-review needs a `first-click-simulation` sub-pass** that:
   - Takes the target artifact(s) as input
   - Parses all outbound links from nav, sub-nav, and body
   - Follows each link and reads the destination page
   - Compares the destination's voice/framing/version to the origin's
   - Flags any transition where the destination "feels like a different site"
   - Reports these as "narrative whiplash" findings in the synthesis

2. **This capability uses the cold-visitor persona** which already exists in the 8-panel preset. Cold visitors are the voices most likely to notice narrative transitions because they're the only voice type that actually navigates a site as a user rather than reading pages as critics.

3. **The primitive needs to be added to `full-foundational` and `content-review` presets** as a mandatory sub-pass, not optional. Content review without nav integrity check is incomplete.

4. **This is one of several "structural integrity" passes** that panel-review should eventually support. Others include:
   - Cross-link validity (do internal links point to existing anchors?)
   - Image/asset loading (do referenced images exist?)
   - Accessibility audit (alt text, aria labels, tab order)
   - Visual hierarchy consistency (do similar pages use similar component weights?)

## Recommended follow-up

1. Add `first-click-simulation` to the panel-review skill spec (INT-007) as a mandatory sub-pass for content-review and full-foundational presets
2. Implement as a sub-agent that uses the cold-visitor persona with navigation-following prompts
3. Write the sub-pass to emit individual "narrative whiplash" findings that promote to cross-cutting synthesis
4. Test the sub-pass by running it against the 2026-04-09 v2-draft state (before the logo fix) and verifying it catches the nav gap Brien caught manually
5. This is the first "integrity pass" type — future passes (link validity, accessibility, visual hierarchy) follow the same pattern

Related: `theparlor/intent:.intent/signals/2026-04-09-panel-review-needs-first-click-sim.md` already captured this in the Intent product repo as SIG-054. This signal is the ODT-level echo, focused on the session-extraction perspective of catching structural gaps that text-reading panels miss.

## Triage, 2026-07-08

Disposition: still pending. Grepped Forge's panel-review outputs for a first-click-simulation or navigation-following sub-pass; none exists. This signal's own text confirms the intent-repo original (theparlor/intent SIG-054) as the primary record; this ODT-level echo remains open on the same unbuilt capability.
