# Changelog

Intent uses timestamp-based versioning: `YYYY.MM.DD-MAJOR.MINOR.PATCH`

**Version declarations:**
- **Major** — Breaking change to the work ontology, event schema, or repo pattern. Existing adopters need to migrate.
- **Minor** — New capability, significant scope expansion, or new artifact type. Non-breaking but meaningful.
- **Patch** — Bug fixes, documentation improvements, clarifications. No behavioral change.

The timestamp prefix records when the release happened. The semver suffix records what kind of change it is.

---

## 2026.03.29-0.4.0

**CLI suite, expanded MCP server, roadmap interfaces**

- Built full CLI suite: `intent-intent` (propose/list/show/accept), `intent-spec` (create/list/show/approve), `intent-status` (signals/intents/specs/events/roadmap dashboard)
- Expanded MCP server from 3 to 7 tools: added `intent_propose_intent`, `intent_create_spec`, `intent_status`
- Created templates for all work ontology levels: intent.md, spec.md, contract.md in `.intent/templates/`
- Built static HTML roadmap page (`docs/roadmap.html`) — four-product view with status grids, Enhance/Build/Learn investments, Now/Next/Later priorities, CLI toolkit grid
- Built interactive React roadmap artifact (`artifacts/intent-product-roadmap.jsx`) — expand/collapse product cards, progress bars, Products/Priorities toggle
- Added "Roadmap" to site navigation
- All CLI tools share consistent architecture: find_intent_root() upward walk, sequential ID generation, markdown+YAML frontmatter, event emission to events.jsonl, optional --commit flag

## 2026.03.29-0.3.0

**Bootstrap kit, signal capture system, four-product roadmap**

- Built bootstrap kit: MCP server (`tools/intent-mcp/`), CLI (`bin/intent-signal`), GitHub Action (`.github/workflows/intent-events.yml`), signal template, quickstart guide
- Designed 5-tier signal capture architecture (MCP → CLI → Slack → GitHub → AI Plugins)
- Captured 6 founding signals from build sessions (SIG-006 through SIG-011)
- Reframed Intent as four products: Notice (Operational), Spec (Conceptual), Execute (Defined), Observe (Schema-Ready)
- Created product roadmap with current state, maturity assessment, and Now/Next/Later investment priorities
- Updated CLAUDE.md with bootstrap kit documentation and four-product framing

## 2026.03.29-0.2.0

**Site restructure, full content hydration, markdown source parity**

- Rebuilt site as product landing page with five-section information architecture: Understand → Shift → Implement → Open Development → Engage
- Full long-form HTML rendering for methodology (from 9KB markdown) and concept brief (from 6KB markdown)
- Created markdown source files for all six HTML-only pages: signal-stream, decision-log, event-catalog, flow-diagram, repo-pattern, work-ontology
- Nav consistency across all 11 pages with correct active states
- Fixed visual-brief AccessDenied error (restored local iframe, removed fabricated Figma URL)
- Added comprehensive continuity documentation (CLAUDE.md) for session-independent development
- Introduced timestamp-based versioning scheme

## 2026.03.28-0.1.0

**Initial public structure — event system, flow diagrams, interactive artifacts**

- Added event catalog artifact (15 events, 6 emission mechanisms, OTel-compatible schema)
- Added flow diagram artifact (5 paths, 4 personas, trigger matrix)
- Created docs site pages for event catalog and flow diagram
- Signal stream page with 5 founding signals
- Decision log page with 6 founding decisions
- Work ontology page with seven-level hierarchy
- Repo pattern page with three-layer directory structure

## 2026.03.28-0.0.1

**Founding commit — methodology, concept brief, visual brief**

- Initial repo structure mirroring the Intent loop: notice/, spec/, execute/, observe/
- Methodology spec (intent-methodology.md) — the full walk-through of the shift from Agile to Intent
- Concept brief spec (intent-concept-brief.md) — product positioning, personas, GTM, hypotheses
- Autonomous operations design spec
- Visual brief interactive artifact (React/Vite app)
- Work system interactive artifact
- 5 founding signals in .intent/signals/
- Decision log in .intent/decisions.md
- INTENT.md project manifest
- README with core loop, repo structure, and positioning
- Docs site shell with methodology, concept brief, signals, decisions pages
