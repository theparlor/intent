---
title: Changelog
type: framework
maturity: final
confidentiality: shareable
reusability: universal
domains:
  - consulting-operations
created: 2026-03-31
technologies:
  - jira
  - figma
  - slack
depth_score: 5
depth_signals:
  file_size_kb: 11.4
  content_chars: 10735
  entity_count: 3
  slide_count: 0
  sheet_count: 0
  topic_count: 1
  has_summary: 0
vocab_density: 0.37
related_entities:
  - {pair: consulting-operations ↔ subaru, count: 791, strength: 0.426}
  - {pair: consulting-operations ↔ automotive-manufacturing, count: 769, strength: 0.416}
  - {pair: consulting-operations ↔ engagement-management, count: 498, strength: 0.269}
  - {pair: consulting-operations ↔ turnberry, count: 448, strength: 0.224}
  - {pair: consulting-operations ↔ foot-locker, count: 251, strength: 0.136}
---
# Changelog

Intent uses timestamp-based versioning: `YYYY.MM.DD-MAJOR.MINOR.PATCH`

**Version declarations:**
- **Major** — Breaking change to the work ontology, event schema, or repo pattern. Existing adopters need to migrate.
- **Minor** — New capability, significant scope expansion, or new artifact type. Non-breaking but meaningful.
- **Patch** — Bug fixes, documentation improvements, clarifications. No behavioral change.

The timestamp prefix records when the release happened. The semver suffix records what kind of change it is.

---

## 2026.03.30 — v0.9.0

### Added
- Trace propagation: make_event() now carries trace_id, span_id, parent_id (v0.2.0 events)
- TraceContext class for cross-server trace correlation via .intent/trace-context.json
- File Tail Adapter: events.jsonl → OTLP span export (observe/adapters/file-tail.py)
- OTel Collector config for Grafana Cloud + local development
- Grafana Observe dashboard definition (8 panels: stats, cycle time, trust, events, traces)
- Observability stack spec (spec/observability-stack.md)
- 6 signal clusters emitted to .intent/clusters/ from 24-signal analysis
- Signal template updated with referenced_by field
- Product roadmap rewritten: autonomy-partitioned (not time-partitioned)
- Execution ROADMAP (tasks/ROADMAP.md) for autonomous terminal operation

### Changed
- Notice server: promote_to_intent now generates trace_id and backfills cluster signals
- Spec server: create_spec inherits trace_id from parent intent
- Observe server: ingest_event carries trace context, indexes by trace_id
- Event version bumped to 0.2.0 (trace context fields)
- TASKS.md rewritten to match current state

### Site (theparlor/intent-site)
- 23 pages across 3 pillars (was 18)
- New: walkthrough, observe, getting-started, system-diagram, observability
- Expanded: event-catalog (2KB→36KB), decisions (4KB→26KB)
- Enhanced: work-system dashboard onramp
- 28 cross-links wired, 4 Mermaid source files
- All 10 site contracts pass

## 2026.03.30-0.8.0

**Two-plane architecture, storytelling pitch page, dogfood page, ARB complete**

### Architecture
- Redesigned work ontology as two-plane architecture: Work Stream (Signal → Intent → Atom → Event → Trace) orthogonal to Ownership Topology (Product → Capability → Team)
- Spec and Contract promoted to independent persistent artifacts with their own lifecycle (not embedded in atoms)
- Atom redesigned as execution envelope — references specs/contracts, doesn't contain them
- New templates pushed: atom.md (reference-based), spec.md (independent lifecycle), contract.md (independent lifecycle), product.md (ownership boundary), team.md (persistent group)

### Site
- Created `docs/pitch.html` — storytelling landing page: narrative arc from AI breaking Scrum/Jira → first principles → Intent's two-plane model. Scroll-reveal sections, inline SVG diagrams, comparison strips, timeline visualization
- Created `docs/dogfood.html` — "Intent building Intent" page showing live artifacts: 16 signals, 14 specs, event stream, pipeline flow visualization. Proves the methodology works by running on itself
- Pushed complete `docs/arb.html` — four-tab ARB artifact with tech radar (28 blips), architectural stack (10 layers), ARB panel (4 principles, 6 decisions, 4 constraints, 4 risks), atomized roadmap (21 items across 4 phases)
- Added ARB nav link to all remaining pages (roadmap, signals, schemas)
- Original homepage preserved at index.html for A/B testing against pitch.html

### Artifacts
- Created two-plane model infographic (A3 landscape PDF) — cartographic design philosophy, trust scoring, Scrum→Intent comparison, OTel mapping

## 2026.03.29-0.7.0

**Schemas page, signals dashboard overhaul, site-wide style normalization**

- Created `docs/schemas.html` — full schema inventory page covering Signal, Intent, Spec, Contract, and Event schemas with trust scoring formula, autonomy levels, status lifecycles, and links to template files
- Overhauled `docs/signals.html` — replaced static page with interactive dashboard: source taxonomy (Human Sources, System Sources, Capture Surfaces), pattern emergence timeline (Scatter → Cluster → Emerge), source markdown links per signal card, trust score visualization, autonomy level counts, cluster/list view toggle
- Added 2 new signals: SIG-014 (agent context drift during multi-file pushes), SIG-015 (signal amplification through reference frequency)
- Normalized CSS across all 12 docs pages — roadmap.html and signals.html converted from raw hex values to CSS custom properties matching `styles.css`
- Added Schemas nav link to all 12 site pages for consistent navigation
- Updated copyright year from 2025 to 2026 across all pages
- Remediated SIG-014 incident: agent-fabricated signals.html content replaced with verified correct dashboard

## 2026.03.29-0.6.0

**Signal trust schema, management CLI, all signals scored**

- Updated signal template with trust framework fields: `trust`, `autonomy_level`, `status`, `cluster`, `parent_signal`
- Extended `intent-signal` CLI with 6 new subcommands: `review` (interactive triage), `dismiss` (with reason), `cluster` (group related signals), `promote` (signal → intent), `list` (filterable), `show` (full details)
- Scored all 13 founding signals with trust values and autonomy levels (L0-L4)
- Assigned cluster groupings: work-ontology-design (3), signal-capture-surfaces (3), bootstrap-tooling (1), autonomous-infrastructure (2)
- Normalized signal frontmatter: `date:` → `timestamp:`, `confidence: high/medium` → numeric, added `author:` to all signals
- Signal status lifecycle operational: captured → active → clustered → promoted → dismissed
- Updated CLAUDE.md with signal management CLI documentation and trust scoring instructions

## 2026.03.29-0.5.0

**Signal dashboard, trust framework, agent handoff protocol**

- Built signal management dashboard (`docs/signals.html`) — operational interface replacing the read-only signals page. Features: signal lifecycle view (captured→active→clustered→promoted→dismissed), cluster grouping with promote-to-intent action, trust score visualization, L0-L4 autonomy spectrum, interactive filtering and view toggling
- Specced signal trust & autonomous execution framework (`spec/signal-trust-framework.md`) — trust scoring model (clarity×0.30 + blast_radius×0.20 + reversibility×0.20 + testability×0.20 + precedent×0.10), five autonomy levels, six-agent enrichment pipeline, disambiguation loop, builder-configurable thresholds via `.intent/config.yml`
- Captured 2 new signals: SIG-012 (autonomous signal processing with trust-based execution) and SIG-013 (multi-machine cloud requirement)
- Fixed global nav across all 10 docs pages — added Roadmap link, standardized nav pattern
- Updated CLAUDE.md with trust framework, deployment topology, and agent handoff protocol
- Defined deployment topology: config-driven local vs hosted mode, always-on processing requirement

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
