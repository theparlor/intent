# Intent Site Specification

> Canonical inventory of the Intent product site. Any agent modifying files in `docs/` MUST read this spec first and verify against `site-contracts.md` after.

## Page Inventory

### Primary Nav Pages (storytelling tier)

| Page | File | CSS Strategy | Nav Active | Min Size | Status |
|------|------|-------------|------------|----------|--------|
| Home | index.html | A (styles.css + inline) | none (logo only) | 7KB | Live |
| Pitch | pitch.html | **B (fully inline)** | Pitch | 26KB | Live |
| Methodology | methodology.html | A (styles.css + inline) | Methodology | 12KB | Live |
| Concept Brief | concept-brief.html | A (styles.css + inline) | Concept Brief | 10KB | Live |
| Work System | work-system.html | A (styles.css + inline) | Work System | 48KB | Live |
| Flow | flow-diagram.html | A (styles.css + inline) | Flow | 1.5KB | **NEEDS REBUILD — content stripped** |
| Schemas | schemas.html | A (styles.css + inline) | Schemas | 8KB | Live |
| ARB | arb.html | **B (fully inline)** | ARB | 32KB | Live — verify tab interface intact |
| Dogfood | dogfood.html | **B (fully inline)** | Dogfood | 20KB | Live |
| Roadmap | roadmap.html | **B (fully inline)** | Roadmap | 15KB | Live |

### Technical Depth Pages (sub-nav tier)

| Page | File | CSS Strategy | Sub-Nav Active | Min Size | Status |
|------|------|-------------|----------------|----------|--------|
| Architecture | architecture.html | A (styles.css + inline) | Architecture | 15KB | New — 2026-03-30 |
| Agents | agents.html | A (styles.css + inline) | Agents | 15KB | New — 2026-03-30 |
| Deployment | deployment.html | A (styles.css + inline) | Deployment | 12KB | New — 2026-03-30 |
| Signals | signals.html | **B (fully inline)** | Signals | 48KB | Live — verify 15 signals intact |
| Dogfood | dogfood.html | **B (fully inline)** | Dogfood | 20KB | Live (dual nav: primary + sub) |

### Supporting Pages (no nav active state)

| Page | File | CSS Strategy | Min Size | Status |
|------|------|-------------|----------|--------|
| Decisions | decisions.html | A (styles.css + inline) | 10KB | Live |
| Event Catalog | event-catalog.html | A (styles.css + inline) | 10KB | Live |
| Native Repos | native-repos.html | A (styles.css + inline) | 13KB | Live |
| Visual Brief | visual-brief.html | A (styles.css + inline) | 1KB | Live (launches visual-brief-app/) |

## CSS Strategy Definitions

### Strategy A: External + Inline
```html
<link rel="stylesheet" href="styles.css">
<style>
  /* Page-specific component CSS only */
  .my-page-component { ... }
</style>
```
The shared `styles.css` provides: reset, body, nav, hero, cards, grids, badges, scroll animations, sub-nav, footer, responsive breakpoints. Page-specific `<style>` blocks provide component CSS unique to that page (e.g., server cards on architecture.html, agent cards on agents.html).

### Strategy B: Fully Self-Contained
```html
<style>
  /* ALL CSS for the page — reset, body, nav, hero, everything */
  * { margin: 0; padding: 0; box-sizing: border-box; }
  body { background: #0f172a; ... }
  .site-nav { ... }
  /* Plus all page-specific components */
</style>
```
No `<link>` to styles.css. The page is a single self-contained HTML document. This strategy is used for pages with complex interactive visuals that have extensive custom CSS.

**CONVERSION RULE: Never convert between strategies. Strategy B pages will break if converted to A (loss of nav/body CSS). Strategy A pages may break if converted to B (duplication/conflicts with styles.css patterns).**

## Navigation Patterns

### Primary Nav (9 links + logo)
Present on ALL 18 pages. Exactly one link has `class="active"` matching the current page. Pages not in the nav (decisions, event-catalog, native-repos, visual-brief, architecture, agents, deployment, signals) have NO active link on the primary nav.

### Technical Sub-Nav (5 links)
Present on: architecture.html, agents.html, deployment.html, signals.html, dogfood.html. Sits below primary nav. Exactly one link has `class="active"`.

## Visual Components Inventory

These are HIGH-VALUE visual elements. Their loss constitutes a critical defect.

| Page | Component | Description |
|------|-----------|-------------|
| pitch.html | Fracture grid | 2-column broken/intact comparison cards |
| pitch.html | Timeline | Gradient-line era timeline (waterfalls → agile → AI → intent) |
| pitch.html | Comparison strip | 3-column old/divider/new |
| pitch.html | SVG loop diagram | Notice → Spec → Execute → Observe circular |
| pitch.html | Two-plane diagram | Work stream + ownership topology rows |
| pitch.html | Stat boxes | 3-column grid (10×, 0×, ∞) |
| arb.html | Tab interface | 4 tabs: Tech Radar, Architectural Stack, ARB Panel, Atomized Roadmap |
| arb.html | Tech radar grid | Quadrant cards: Adopt, Trial, Assess, Hold |
| arb.html | Stack layers | Tiered architecture cards |
| signals.html | Signal cards | 15 signal cards with trust scores, status badges |
| signals.html | Cluster views | Signal grouping visualization |
| signals.html | Source flow | Signal source → pipeline flow |
| signals.html | Pattern timeline | Emergent pattern visualization |
| work-system.html | Full work system | Comprehensive operational dashboard replacement |
| dogfood.html | Dogfood dashboard | Self-referential metrics and status |
| roadmap.html | Product roadmap | Interactive phase cards with investment sizing |

## File Size Baselines

File sizes serve as a canary. A page dropping significantly below its baseline means content was lost.

```
pitch.html        ~26KB (Strategy B — complex visuals)
work-system.html  ~48KB (Strategy A — largest page)
signals.html      ~48KB (Strategy B — 15 signal cards)
arb.html          ~32KB (Strategy B — tab interface + radar)
dogfood.html      ~20KB (Strategy B — dogfood dashboard)
roadmap.html      ~15KB (Strategy B — roadmap cards)
native-repos.html ~13KB
methodology.html  ~12KB
concept-brief.html ~10KB
decisions.html    ~10KB
event-catalog.html ~10KB
schemas.html      ~8KB
index.html        ~8KB
architecture.html ~15KB (Strategy A — server cards, trust table)
agents.html       ~15KB (Strategy A — agent cards, routing table)
deployment.html   ~12KB (Strategy A — step cards, platform table)
flow-diagram.html ~1.5KB ⚠️ NEEDS REBUILD (was stripped to skeleton)
visual-brief.html ~1KB (launcher page)
```
