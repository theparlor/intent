# Intent Site — Information Architecture v2

> This document defines the navigation structure, page hierarchy, and content placement for the Intent product site. Any agent modifying navigation or page structure MUST read this spec first.

## Design Principle

The site tells a story in three acts. Each act has a **hero page** (the entry point) and **depth pages** (the detail). The primary nav shows only the three acts. Each act's hero page includes a sub-nav to its depth pages. Cross-links connect related content across acts.

Think of it like a building with three wings. You enter through the lobby (home/pitch), and from there you choose a wing. Inside each wing, a corridor (sub-nav) connects the rooms.

---

## The Three Pillars

### Pillar 1 — "The Story" (What & Why)

**Purpose:** Convince. Create the visceral "something is broken, here's what's different" reaction. Then let people go deeper into the formal framing.

| Role | Page | File | Notes |
|------|------|------|-------|
| **Hero** | Pitch | pitch.html | Becomes the site index. Fracture grid, loop SVG, stat boxes, timeline, comparison strip, two-plane diagram. The full emotional + intellectual hook. |
| Depth | Concept Brief | concept-brief.html | Formal product framing — problem, solution, differentiation, audience. |
| Depth | Methodology | methodology.html | The Intent loop explained — Notice→Spec→Execute→Observe with depth on each phase. |
| Depth | Roadmap | roadmap.html | Where Intent is headed. Vision-forward, not implementation-detail. |

**Sub-nav label order:** Concept Brief · Methodology · Roadmap

**Why this grouping:** These pages answer "what is Intent?" from different angles — emotional (pitch), formal (brief), procedural (methodology), temporal (roadmap). A visitor convinced by the pitch naturally wants to understand the concept, then the method, then what's coming.

---

### Pillar 2 — "The System" (How It Works)

**Purpose:** Show. The operational centerpiece — how Intent actually functions as a working system. Proof over promise.

| Role | Page | File | Notes |
|------|------|------|-------|
| **Hero** | Work System | work-system.html | The Jira-replacement dashboard. Signal stream, spec lifecycle, execution state, the full operational picture. |
| Depth | Flow | flow-diagram.html | The loop visualized — interactive/animated Notice→Spec→Execute→Observe diagram. **Currently a 1.5KB skeleton — needs full rebuild.** |
| Depth | Schemas | schemas.html | Data contracts — signal schema, spec schema, execution record schema. The type system behind the system. |
| Depth | Signals | signals.html | Live signal stream — 15 signal cards, trust scores, clustering, pattern detection. |
| Depth | Dogfood | dogfood.html | Intent building Intent. Self-referential proof — the system's own signal stream, specs, and event log. |
| Depth | Event Catalog | event-catalog.html | Catalog of event types in the system. **Currently thin — candidate for expansion.** |

**Sub-nav label order:** Flow · Schemas · Signals · Dogfood · Events

**Why this grouping:** These pages answer "how does it actually work?" from different angles — operational (work system), visual (flow), structural (schemas), live data (signals), proof (dogfood), and reference (events). A visitor who understands the concept naturally wants to see it in action.

---

### Pillar 3 — "The Build" (How It's Constructed)

**Purpose:** Explain. The technical architecture, governance, and engineering decisions. For builders and evaluators.

| Role | Page | File | Notes |
|------|------|------|-------|
| **Hero** | Architecture | architecture.html | MCP server topology, trust model, loop diagram, phased rollout. The technical overview. |
| Depth | Agents | agents.html | 6 subagent definitions, model routing, tool access, coordinator pattern. |
| Depth | Deployment | deployment.html | FastMCP Cloud, local dev, platform comparison, configuration. |
| Depth | ARB / Tech Radar | arb.html | SVG radar visual, architectural stack, governance panel, atomized roadmap. |
| Depth | Decisions | decisions.html | Architecture decision records. **Currently thin — candidate for expansion with full ADR entries.** |
| Depth | Native Repos | native-repos.html | Repository structure, code organization, integration points. |

**Sub-nav label order:** Agents · Deployment · ARB · Decisions · Repos

**Why this grouping:** These pages answer "how is it built?" from different angles — topology (architecture), agents (who does what), operations (deployment), governance (ARB/decisions), and code (repos). A visitor evaluating the technical depth naturally wants to understand the architecture, then drill into specifics.

---

## Navigation Structure

### Primary Nav (3 links + logo)

```html
<nav class="site-nav">
  <a href="index.html" class="logo"><span>I</span>ntent</a>
  <a href="pitch.html">The Story</a>
  <a href="work-system.html">The System</a>
  <a href="architecture.html">The Build</a>
</nav>
```

**Active states:**
- Pitch and all Pillar 1 depth pages → "The Story" active
- Work System and all Pillar 2 depth pages → "The System" active
- Architecture and all Pillar 3 depth pages → "The Build" active

### Sub-Nav (per pillar)

Each pillar's hero page AND depth pages show the same sub-nav below the primary nav. The hero page name appears first, then depth pages.

**Pillar 1 sub-nav:**
```html
<nav class="sub-nav">
  <a href="pitch.html">Overview</a>
  <a href="concept-brief.html">Concept Brief</a>
  <a href="methodology.html">Methodology</a>
  <a href="roadmap.html">Roadmap</a>
</nav>
```

**Pillar 2 sub-nav:**
```html
<nav class="sub-nav">
  <a href="work-system.html">Overview</a>
  <a href="flow-diagram.html">Flow</a>
  <a href="schemas.html">Schemas</a>
  <a href="signals.html">Signals</a>
  <a href="dogfood.html">Dogfood</a>
  <a href="event-catalog.html">Events</a>
</nav>
```

**Pillar 3 sub-nav:**
```html
<nav class="sub-nav">
  <a href="architecture.html">Overview</a>
  <a href="agents.html">Agents</a>
  <a href="deployment.html">Deployment</a>
  <a href="arb.html">ARB</a>
  <a href="decisions.html">Decisions</a>
  <a href="native-repos.html">Repos</a>
</nav>
```

### Index Page

`index.html` becomes a landing/redirect to `pitch.html`, or pitch.html content replaces index.html directly. The logo link always points to `index.html`.

### Visual Brief

`visual-brief.html` is not a nav destination. It becomes a CTA button or link on the Pitch page ("Launch Visual Brief →") rather than a standalone page in the navigation.

---

## Cross-Links

Cross-links connect related content across pillars. These are inline contextual links within page content, not nav elements.

| From | To | Context |
|------|----|---------|
| Methodology (Pillar 1) → | Schemas (Pillar 2) | "See the data contracts behind each loop phase" |
| Methodology (Pillar 1) → | Flow (Pillar 2) | "See the loop visualized" |
| Concept Brief (Pillar 1) → | Work System (Pillar 2) | "See the system in action" |
| Roadmap (Pillar 1) → | ARB (Pillar 3) | "See the technology decisions behind the roadmap" |
| Signals (Pillar 2) → | Architecture (Pillar 3) | "How signals are ingested — MCP server topology" |
| Dogfood (Pillar 2) → | Methodology (Pillar 1) | "The methodology this system follows" |
| Schemas (Pillar 2) → | Decisions (Pillar 3) | "Why these schema shapes were chosen" |
| Work System (Pillar 2) → | Agents (Pillar 3) | "The agents that power the work system" |
| ARB (Pillar 3) → | Roadmap (Pillar 1) | "The vision these decisions serve" |
| Architecture (Pillar 3) → | Work System (Pillar 2) | "See the architecture in operation" |

---

## Migration Notes

### Content that moves or merges

- **Pitch visuals** (fracture grid, loop SVG, stat boxes, timeline, comparison strip, two-plane diagram) stay on pitch.html. If any of these visuals would enhance the Concept Brief or Methodology pages, they should be **duplicated/adapted**, not moved. The pitch page must remain visually complete.
- **index.html** current content (loop strip, card grid) gets replaced by pitch.html content or index.html redirects to pitch.html.
- **visual-brief.html** becomes a link/CTA on pitch.html, removed from any nav.

### What doesn't change

- All page files keep their current filenames.
- All page-specific CSS remains intact (the Light/Rich model continues).
- All existing visual components are preserved (CON-SITE-008 still applies).
- File size baselines still apply (CON-SITE-006 still applies).

### Implementation order

1. **Update nav HTML on all 18 pages** — new 3-link primary nav, pillar-appropriate sub-nav
2. **Update index.html** — either replace content with pitch.html content or redirect
3. **Add cross-links** to page content where specified
4. **Update site-spec.md** — new page inventory reflecting pillar structure
5. **Update site-contracts.md** — new nav contracts reflecting 3-link primary, pillar sub-navs
6. **Update CLAUDE.md** — new IA rules for terminal agents
7. **Verify all contracts pass**
