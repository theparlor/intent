# Intent Site Specification

> Canonical inventory of the Intent product site. Any agent modifying files in `docs/` MUST read this spec first and verify against `site-contracts.md` after.

## Page Inventory

### Primary Nav Pages (storytelling tier)

| Page | File | Page Type | Nav Active | Min Size | Status |
|------|------|-----------|------------|----------|--------|
| Home | index.html | Rich | none (logo only) | 7KB | Live |
| Pitch | pitch.html | Rich | Pitch | 26KB | Live |
| Methodology | methodology.html | Light | Methodology | 12KB | Live |
| Concept Brief | concept-brief.html | Light | Concept Brief | 10KB | Live |
| Work System | work-system.html | Rich | Work System | 48KB | Live |
| Flow | flow-diagram.html | Light | Flow | 1.5KB | **NEEDS REBUILD — content stripped** |
| Schemas | schemas.html | Light | Schemas | 8KB | Live |
| ARB | arb.html | Rich | ARB | 32KB | Live — verify tab interface intact |
| Dogfood | dogfood.html | Rich | Dogfood | 20KB | Live |
| Roadmap | roadmap.html | Rich | Roadmap | 15KB | Live |

### Technical Depth Pages (sub-nav tier)

| Page | File | Page Type | Sub-Nav Active | Min Size | Status |
|------|------|-----------|----------------|----------|--------|
| Architecture | architecture.html | Rich | Architecture | 15KB | New — 2026-03-30 |
| Agents | agents.html | Rich | Agents | 15KB | New — 2026-03-30 |
| Deployment | deployment.html | Rich | Deployment | 12KB | New — 2026-03-30 |
| Signals | signals.html | Rich | Signals | 48KB | Live — verify 15 signals intact |
| Dogfood | dogfood.html | Rich | Dogfood | 20KB | Live (dual nav: primary + sub) |

### Supporting Pages (no nav active state)

| Page | File | Page Type | Min Size | Status |
|------|------|-----------|----------|--------|
| Decisions | decisions.html | Light | 4KB | Live — candidate for content expansion |
| Event Catalog | event-catalog.html | Light | 2KB | Live — candidate for content expansion |
| Native Repos | native-repos.html | Rich | 13KB | Live |
| Visual Brief | visual-brief.html | Light | 1KB | Live (launches visual-brief-app/) |

## CSS Strategy

**All pages use the same architecture:** link `styles.css` for shared foundation + page-specific `<style>` blocks for unique components.

```html
<link rel="stylesheet" href="styles.css">
<style>
  /* Page-specific component CSS only */
  .my-page-component { ... }
</style>
```

The shared `styles.css` provides: reset, variables, body, nav, sub-nav, hero, content, cards, grids, badges, scroll animations, callouts, code blocks, footer, responsive breakpoints. Page-specific `<style>` blocks provide component CSS unique to that page.

### Page Types

**Light pages** have small or no `<style>` blocks. Most styling comes from styles.css.

**Rich pages** have extensive `<style>` blocks (50-300+ lines) with complex visual components. **Never strip or reduce `<style>` blocks from rich pages.** The page-specific CSS IS the page's value. The protection against content loss is CON-SITE-006 (file size canary) and CON-SITE-008 (visual components check).

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
pitch.html        ~26KB (Rich — scroll animations, SVG, fracture grid, timeline, comparison strip)
work-system.html  ~48KB (Rich — full React work system dashboard)
signals.html      ~48KB (Rich — 15 signal cards, cluster views, trust scoring)
arb.html          ~32KB (Rich — tab interface, tech radar, stack, ARB panel, roadmap)
dogfood.html      ~20KB (Rich — dogfood dashboard, event stream, signal list)
roadmap.html      ~15KB (Rich — product phase cards, investment sizing, CLI grid)
architecture.html ~15KB (Rich — server cards, trust table, ASCII diagrams, phase cards)
agents.html       ~15KB (Rich — agent cards, model routing table, tool pills)
native-repos.html ~13KB (Rich — React tabbed interface)
deployment.html   ~12KB (Rich — step cards, platform table, code blocks)
methodology.html  ~12KB (Light)
concept-brief.html ~10KB (Light)
decisions.html    ~4KB (Light — candidate for expansion with actual decision entries)
event-catalog.html ~2KB (Light — candidate for expansion with 15 event type details)
schemas.html      ~8KB (Light)
index.html        ~8KB (Rich — loop strip, card grid, section layout)
flow-diagram.html ~1.5KB ⚠️ NEEDS REBUILD (was stripped to skeleton)
visual-brief.html ~1KB (Light — iframe launcher)
```
