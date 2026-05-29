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
depth_score: 6
depth_signals:
  file_size_kb: 24.0
  content_chars: 19238
  entity_count: 3
  slide_count: 0
  sheet_count: 0
  topic_count: 1
  has_summary: 0
vocab_density: 0.21
related_entities:
  - {pair: consulting-operations ↔ teresa-torres, count: 67, strength: 0.103}
  - {pair: consulting-operations ↔ marty-cagan, count: 64, strength: 0.086}
  - {pair: consulting-operations ↔ subaru, count: 44, strength: 0.119}
  - {pair: consulting-operations ↔ slack, count: 41, strength: 0.123}
  - {pair: consulting-operations ↔ jeff-patton, count: 40, strength: 0.079}
---
# Changelog

Intent uses timestamp-based versioning: `YYYY.MM.DD-MAJOR.MINOR.PATCH`

**Version declarations:**
- **Major** — Breaking change to the work ontology, event schema, or repo pattern. Existing adopters need to migrate.
- **Minor** — New capability, significant scope expansion, or new artifact type. Non-breaking but meaningful.
- **Patch** — Bug fixes, documentation improvements, clarifications. No behavioral change.

The timestamp prefix records when the release happened. The semver suffix records what kind of change it is.

---

## 2026.05.29 — v0.13.0

### Added — Entity-Lifecycle Primitive ratified (SPEC-003 Extension 1 promoted)

Per **WS-DDR-101** (theparlor/workspaces-governance, 2026-05-29), SPEC-003 Extension 1 is promoted from `approved`-but-unbuilt to a ratified, first-class Intent primitive — a **sibling** of the work-ontology (WS-DDR-025), generalized from Cast's two-axis lifecycle (WS-DDR-071). Closes the gap named by RETRO-2026-04-08-persona-design-SIG-1: the framework could spec the *work of creating* a durable entity but could not track the *entity's own life* afterward, so four products each reinvented a divergent lifecycle state-machine.

- **Two-axis state shape.** Entities carry `pipeline` (advancement — monotonic, one terminal state) × `disposition` (editorial — free to move), replacing Extension 1's original single-axis `lifecycle` enum. Each `entity_type` declares its own enum *values*; the framework owns the *machine*. This is the one substantive amendment to Extension 1 as written.
- **`candidate` canonical entry state** for every `entity_type`, with two new contracts: **CON-ENTITY-DEDUP** (identity-key match on candidate creation raises a merge-intent — write-through dedup at the door, chain_audit sweep demoted to catch-net) and **CON-ENTITY-ONBOARD** (admission DoR). Plus **CON-ENTITY-DISPOSITION-ORTHOGONALITY** (disposition demotion never regresses pipeline — generalized WS-DDR-071 rule). **CON-008** generalized to be `entity_type`-profile-aware.
- **Cast `pipeline`/`usage` re-designated the reference instantiation** (not bespoke); `usage` maps to the generic `disposition` axis (role-rename, values unchanged).
- Fixed a stale `canonical_path` storage example in Extension 1 (`Core/personas/registry/…` → `Core/products/cast/farm/registry/…`, the pre-WS-DDR-027 path).

### Changed
- `spec/SPEC-003-intent-framework-entity-extensions.md` — Extension 1 rewritten (two-axis + `candidate` + per-type profiles + `entity.*` events); `completeness` 0.80 → 0.95; `ratified_by: WS-DDR-101`. Extensions 2–5 and CON-009…CON-014 unchanged.

### Compatibility
**Minor (backward-compatible).** Existing signals, intents, and specs are untouched; no existing entity data changes meaning. The migration that instantiates the primitive in Cast (per-type profiles, `candidate`+hooks wiring, `ENT-NNN` repair) is sequenced separately and moves no data at ratification.

---

## 2026.05.27 — v0.12.1

### Added — Substrate Exposure Phase 1 close-out (pre-Brien-deploy)

Two follow-on engineering pieces + the deploy guide Brien needs after his dentist appointment:

- **`servers/DEPLOYMENT-INTENT-KNOWLEDGE.md`** — ~370-line click-by-click deploy guide for the 4th MCP server on FastMCP Cloud. Covers pre-deploy checklist (verify tests + commit + catalog freshness), 5-step deploy procedure, MCP client config, smoke test against DEC-009, Phase 1 vs Phase 2 backend modes, classification/scope-token configuration, troubleshooting (404s, 0-hits, build failures, port collisions), and validation criteria mapped to substrate-exposure-architecture.md.
- **`bin/intent-init` Step 3b** — Stop-hook registration in `<product>/.claude/settings.local.json`. The hook-file install (step 3) already worked; this completes the Tier 1 wiring so the hook actually fires on Claude Code Stop events. Idempotent (re-run is a no-op). Test suite 40/40 → **45/45** with 5 new assertions covering registration shape + idempotency.
- **`servers/lib/library_index_client.py` Phase 2 swap** — direct Python import of library-index-mcp's BM25 ranking (Option A). 3-stage fallback chain: BM25 (Phase 2 primary) → word-hit (Phase 1) → repo-keyword (last resort). Server never goes dark. Test suite 34/34 → **36/36** with 2 new tests covering BM25 path + import-failure fallback.

### Changed
- `servers/DEPLOYMENT.md` — cross-ref to `DEPLOYMENT-INTENT-KNOWLEDGE.md` at top; intent-knowledge added to project list, MCP config, local-dev terminals (3 → 4), env-var table.
- `spec/substrate-exposure-architecture.md` Phase 1 progress checkpoint — Phase 2 swap + Stop-hook flipped from "in progress / documented" to "shipped" with commit SHAs; Closure-DoD assertions for each component updated to **resolved** (was symptom-repaired-upstream-pending for intent-knowledge substrate verbs).

### Closure status
All Phase 1 implementation work is **resolved** per Closure-DoD assertions. Only the Brien-driven FastMCP Cloud deploy itself remains.

---

## 2026.05.26 — v0.12.0

### Added — Substrate Exposure Phase 1 (filing + foundational implementation)

The 2026-05-26 Cowork Phase 1 session on substrate exposure + Witness/Entire composition produced load-bearing decisions and their first implementations. Files DEC-009 (filed earlier this date), DEC-010, DEC-011, and WS-DDR-099 (workspaces-governance). Implementations follow.

**Decisions:**
- **DEC-009** — Entire.io scoped as authoring-provenance (supersedes DEC-007). Distinguishes authoring observability (Entire) from running-system observability (OTel/Grafana stack); both are siblings, neither replaces the other.
- **DEC-010** — Intent-knowledge MCP server scope extended to substrate exposure. Adds 5 read verbs (query/get/list/lineage/freshness) alongside existing ingest/query/lint. Composes with library-index for ranked retrieval on the query verb.
- **DEC-011** — `bin/intent-init` scaffold CLI for products + client engagements. Tier-aware classification schema universal Day 1; Witness federation selective by tier per D5-refined (internal Day 1, engagement deferred to Phase 2).
- **WS-DDR-099** (workspaces-governance) — Substrate exposure via MCP-front + repo-as-truth composition. Sibling-composed identity (repo), reachability (MCP), liveness (decoupled). Phase 1 read-only, Phase 2 write-back via PR-as-arbiter.

**Architecture artifact:**
- **`spec/substrate-exposure-architecture.md`** — full architecture brief for the Phase 1 ship target (~2.5-3 weeks). Cross-referenced from ARCHITECTURE.md.

**Runbook:**
- **`playbooks/spawn-a-product.md`** — Tier 0 → Tier 3 composition runbook. Includes engagement-classification operational section per D5-refined.

### Added — Phase 1 Implementations Shipping Today

- **`bin/intent-init`** — Python scaffold CLI implementing DEC-011 (516 lines). 40/40 tests passing in `bin/test-intent-init.sh` across 7 scenarios (internal-default, confidential-engagement, engagement-without-classification-rejection, idempotent re-run, tier-mismatch refusal, invalid-classification rejection, public-tier federation). Auto-creates `Core/engagements/` for confidential tiers; adds `--declared-by` and `--dry-run` quality-of-life flags.
- **`hooks/session-end.sh`** — Tier 1 session.end event emitter (192 lines). OTel-shaped per DEC-004. Detects product context via walk-up from `.intent/`, captures files_touched + commit_sha + signals_captured + decisions_recorded (best-effort, last-60-min window), appends to `.intent/events/events.jsonl` with flock+fsync on Linux, atomic append on macOS.
- **`spec/classification-schema.md`** — `.intent/classification.yaml` v1 schema docs. Three tiers: public, internal, confidential:<engagement-slug>. Read by intent-init at scaffold time; will be read by intent-knowledge MCP server on every substrate query.

### Added — Phase 1 Investigation + Follow-on Spec

- **`spec/library-index-composition-investigation-2026-05-26.md`** — investigation report on library-index ↔ intent-knowledge composition. Finds library-index has no BM25+vector retrieval today; recommended path is a half-day Port A extension (`library_search_ranked` tool added to library-index-mcp). qmd full-BM25+vector backend is correct architecture but full-day sub-milestone.

### Shipped post-CHANGELOG-entry (verified 2026-05-27)

The two "in progress" items at the time of the 2026-05-26 v0.12.0 entry
landed in the same commit wave and have test coverage. Verified
2026-05-27 by code + test inventory check:

- **library-index-mcp `library_search_ranked` Port A tool** — registered as `@mcp.tool(name="library_search_ranked")` at `Core/products/library-index-mcp/server.py`. Dedicated test file `Core/products/library-index-mcp/tests/test_library_search_ranked.py`. BM25-ranked retrieval over CATALOG.json + sidecar excerpts.
- **`intent-knowledge` MCP server 5 substrate verbs** — registered in `Core/frameworks/intent/servers/knowledge.py`: `query` (line 720), `get` (line 799), `list_entities` (line 880, renamed from reserved `list`), `lineage` (line 954), `freshness` (line 1027). All accept `scope_token: str = "internal"` for D5-refined tier enforcement. Test coverage: 34 test functions in `Core/frameworks/intent/servers/test_knowledge.py`.

### Added — Public Communications Draft

- **`intent-site/posts/two-observabilities.md`** — ~750-word draft articulating the DEC-009 distinction (cockpit voice recorder vs. flight data recorder metaphor; authoring observability vs. running-system observability). Promotion-path documented for future HTML lift into Pillar 3 (The Build) of the intent-site IA.

### Filed (governance + meta)

- WS-DDR-098 index row recovery (workspaces-governance) — discovered ratified body had no index entry.
- 8 hygiene-sweep commits across intent, intent-site, workspaces-governance: nightly library-index metadata refresh batches + cron-session-accumulation cleanup + scheduled-tasks archive + GH issue #62472 draft + timestamp-divergence + forge-persona-count signals + architecture-first signal + jira-canonical-fields spawn-prompt.

---

## 2026.05.20 — v0.11.0

### Added — IDD Build Discipline Playbooks
- **IDD playbook (core):** `learnings/idd-playbook.md` — 7-stage IDD loop with DoR/DoD gates, build-intake enforcement, and phase-specific agent posture rules
- **Cross-product applicability:** `learnings/idd-cross-product-applicability.md` — how IDD maps across Cast, Forge, Voices, Loom, Topography, Throughline, and Fieldbook
- **Build-intake enforcement spec:** `spec/build-intake-enforcement.md` — 5-layer gate enforcement preventing premature Execute entry; hooks at SessionStart, Stop, PreToolUse

### Added — Process Drift Catalog v1 (families 1–4, 16 entries + 2 new)
- **Catalog:** `learnings/process-drift-catalog.md` — canonical catalog of recurring AI-agent drift patterns across 4 families (Autonomy, Closure, Signal, Coordination)
- **Family 1.7 — Artificial-gate-architecture drift:** Over-gating reversible work with invented L0 sign-offs; prevention via 4-gate silent check + L4 posture enforcement
- **Family 4.7 — Governance-skill-without-trigger:** Periodic governance operations left with no structural firing mechanism; prevention via SessionStart hook + scheduled task

### Added — Hook Infrastructure (Layer 5 + overwatch)
- **Autonomy-grant dispatch-prompt-check hook:** `hooks/autonomy-grant-dispatch-prompt-check.sh` — Layer 5 of autonomy-grant enforcement; PreToolUse gate for spawn_task/Agent dispatches lacking autonomy grant markers. Closes SIG-AUTONOMY-GRANT-DISPATCH-HOOK-INSTALLED-2026-05-19.
- **Overwatch staleness-check hook:** `hooks/overwatch-staleness-check.sh` — SessionStart banner when latest overwatch JRN mtime >7 days (warn) or >14 days (load-bearing posture). Closes SIG-OVERWATCH-STALENESS-PATTERN-2026-05-20. Registered in `~/.claude/settings.json`.
- **Closure-discipline stop-hook table-cell extension:** `hooks/closure-discipline-stop-check.sh` — COMPLETION_RE extended to catch markdown table rows with standalone "Done"/"Complete"/✅ cells (Catalog Entry 2.3 extension)

### Added — Overnight Orchestrator
- **Spawn prompt:** `spawn-prompts/overnight-exhaustive-upgrade.md` — multi-phase overnight orchestrator that runs exhaustive product + framework + skill self-audits. Triggers framework-self-audit, closure-discipline-audit, process-drift-audit across full Workspaces topology.

### Added — Signal Stream
- **Signal-stream spec:** `spec/signal-stream.md` — authoritative closure-DoD definitions, triad schema (upstream_control_path / catch_mechanism / pipeline_survival), and signal lifecycle policy
- **130+ signals captured** across 2026-03-28 through 2026-05-20

### Changed
- Closure-discipline stop-hook (Layer 4) extended with table-cell scanner variant

---

## 2026.04.13 — v0.10.0

### Added — 12-Factor Agent Pattern Integration (DDR-006)
- **Pause/Resume protocol:** `execution.paused` + `execution.resumed` events with checkpoint serialization schema, TTL enforcement, and trust-aware fallback actions
- **Human contact as capability:** `request_human_input` signal type — agents can proactively request human input at ANY trust level, distinct from governance gates. `human_input.requested` + `human_input.received` events with urgency routing (blocking/informational/deferred)
- **LLM-as-Judge:** `observation.evaluated` event with multi-dimensional scoring schema. Closes the gap between contract verification (mechanical) and spec satisfaction (semantic). Fail verdicts auto-emit signals back to Notice
- **Error-Retry-Escalate:** `execution.error_retry` + `execution.escalated` events. Standard retry-cap + trust-aware escalation pattern codified at platform level
- **State Philosophy:** New ARCHITECTURE.md section documenting stateful-system / stateless-invocation resolution with context resolver as bridge
- **Extension 5 (SPEC-003):** Execution checkpoint primitive with schema, TTL, resume triggers, and trust model integration
- **CON-012:** Checkpoint validity contract (TTL enforcement, span_id linkage)
- **CON-013:** Human input request independence contract (emittable at any trust level)
- **CON-014:** LLM-as-judge semantic gap detection contract
- **12-factor mapping analysis:** `knowledge-engine/analysis/12-factor-mapping.md`

### Added — SPEC-APPROVAL-GATE Execution (Phase 1)
- **IntentApproval entity:** `.intent/approvals/` directory + `_TEMPLATE.md` with full lifecycle schema (pending → approved/denied/expired)
- **Elevation entity:** `.intent/elevations/` directory + `_TEMPLATE.md` for time-boxed auto-approve grants
- **Approval gate methodology module:** `methodology/meta/approval-gate.md` — cross-cutting governance module documenting the three human-contact patterns, pause/resume integration, TTL/revalidation, elevation mechanics, and per-action-type payload schemas
- **Per-action-type payload schemas:** slack_message, email, pr_create, pr_comment, issue_comment, calendar_change — all structured in methodology module
- **4 approval events:** `intent.approval.requested`, `intent.approval.decided`, `intent.approval.expired`, `intent.approval.elevated`
- **Ambiguity flag resolution:** All 4 flags in SPEC-APPROVAL-GATE resolved via 12-factor pause/resume and human-contact-as-capability patterns
- **CLAUDE.md governance wiring:** L0 approval gate, three human-contact patterns, and approval-rules.yml documented as source of truth

### Changed
- Event catalog: 15 → 26 events (7 from 12-factor + 4 from approval gate across Execute and Observe phases)
- models.py: EVENT_TYPES updated with 11 new event types, organized by phase
- Signal trust framework: added Human Contact as Agent Capability section
- SPEC-003: added Extension 5 + 3 new contracts (CON-012 through CON-014)
- SPEC-APPROVAL-GATE: status shaped → executing, ambiguity flags resolved

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
