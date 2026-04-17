---
decision_id: RETRO-2026-04-09-intent-rebuild-3
title: Inline SVG beats raster for web hero visuals in Brien's portfolio
date: 2026-04-09
status: accepted
source: retroactive-extraction
session_date: 2026-04-09
references:
  - RETRO-2026-04-09-image-gen-1 (parallel decision on DALL-E for raster)
  - theparlor/intent-site:docs/v2-draft/pitch.html (reference implementation)
---
# Inline SVG beats raster for web hero visuals in Brien's portfolio

## Context

The intent-site needed a hero visual for pitch.html (the v2-draft landing page) showing the Notice→Spec→Execute→Observe loop. Four image tools were tested (Midjourney, Gemini, DALL-E 3, Ideogram) — DALL-E 3 won the raster competition, but after seeing the winning raster output, Brien chose to ship a hand-crafted inline SVG instead.

The SVG went through three iterations in-session:
1. Initial 960×540 circular loop
2. Full-width 1600×540 elliptical layout (flatter, wider)
3. Label overlap fix + matching INTENT ellipse with pulsing animation

## Decision

For any web hero visual on Brien's portfolio sites (intent-site, rate card site, future sites), inline SVG is the default over raster image files. Use raster tools (DALL-E 3 preferred per parallel decision) for social/OG images, presentation slides, printable documents, and static use cases only.

The specific advantages that tilted this decision:

1. **Scales perfectly** — no resolution loss at any viewport size, no @2x/@3x variants needed
2. **Animates** — CSS/SMIL animations for pulsing, flowing arrows, hover effects without external libraries
3. **Exact design-system fidelity** — hex colors, spacing, typography all match the site's CSS variables rather than approximating the design system
4. **Accessible** — role="img" + aria-label + meaningful text elements are natively supported
5. **Zero external dependencies** — no CDN calls, no image asset loading, no preload hints needed
6. **Editable** — Brien or any future agent can directly modify element positions, colors, animations via Edit tool; raster images require regeneration
7. **Lightweight** — a detailed SVG hero is typically 3-8KB; a high-res raster is 200-800KB

## Alternatives Considered

1. **Use the DALL-E 3 raster as the hero** — Rejected because SVG advantages compound over time (every design system change would require regeneration). DALL-E output moves to OG image / social share role instead.

2. **SVG generated from raster via vectorization tools** — Rejected because auto-vectorized SVGs are typically bloated (thousands of paths) and don't respect design-system semantics. Hand-crafted SVG is smaller, more readable, and more maintainable.

3. **Figma export to SVG** — Valid alternative for cases where visual design is happening in Figma anyway. Not the case here (the visual was designed by direct SVG authoring). Future work that starts in Figma should still export as SVG, not PNG.

4. **HTML Canvas rendering** — Rejected for hero visuals because it doesn't degrade gracefully on crawlers/printers and loses accessibility.

## Consequences

- The intent-site pitch.html v2-draft hero is an inline SVG (full-width elliptical loop with pulsing INTENT center and animated flow arcs)
- Future heroes for other sites default to inline SVG unless there's a specific reason to use raster
- The SVG-authoring skill/pattern becomes a known Brien-portfolio pattern — other agents should follow it
- Raster outputs from DALL-E 3 are still valued but scoped to: og:image, twitter:image, presentation slides, printable docs, screenshot replacements
- Design-system fidelity becomes easier to maintain because hex values in the SVG live in the same file as the CSS variables
- Animation is a first-class feature of hero visuals, not an afterthought
