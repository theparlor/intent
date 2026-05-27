---
title: Tasks
type: framework
maturity: final
confidentiality: shareable
reusability: universal
domains:
  - consulting-operations
created: 2026-03-29
updated: 2026-03-30
frameworks:
  - double-loop-learning
depth_score: 4
depth_signals:
  file_size_kb: 7.8
  content_chars: 7093
  entity_count: 1
  slide_count: 0
  sheet_count: 0
  topic_count: 1
  has_summary: 0
vocab_density: 0.42
related_entities:
  - {pair: consulting-operations ↔ teresa-torres, count: 66, strength: 0.111}
  - {pair: consulting-operations ↔ marty-cagan, count: 63, strength: 0.094}
  - {pair: consulting-operations ↔ subaru, count: 44, strength: 0.121}
  - {pair: consulting-operations ↔ slack, count: 41, strength: 0.124}
  - {pair: consulting-operations ↔ jeff-patton, count: 40, strength: 0.085}
---
# Tasks

> The living backlog. Partitioned by autonomy level, not sprint boundary.
> See `spec/product-roadmap.md` for the full four-product assessment and signal cluster analysis.

---

## Layer 1 — Domain Knowledge Base Implementation (Three-Layer Architecture)

> Added 2026-04-05. Karpathy LLM Knowledge Base pattern integrated as Layer 1.
> Schema: `knowledge-engine/AGENTS.md`. Research: `reference/karpathy-synthesis/`.

### Ingest Pipeline
- [ ] Implement `ingest` operation: drop source in raw/ → LLM compiles into knowledge artifacts → updates _index.md + log.md
- [ ] Wire ingest into intent-notice MCP server (or new intent-knowledge server) — see WS-DDR-099 + DEC-010 (2026-05-26): `intent-knowledge` MCP server is now the scoped host for ingest + substrate-exposure verbs
- [ ] Test with Intent's own dogfood data as first raw/ corpus

### Substrate Exposure Phase 1 — added 2026-05-26 (WS-DDR-099 + DEC-010 + DEC-011)
- [x] **DEC-011 scaffold shipped:** `bin/intent-init` (intent@bd3f49f, 40/40 tests) + `hooks/session-end.sh` (intent@b6d837d) + `.intent/classification.yaml` schema docs (intent@63c84ba)
- [x] **library-index composition path investigated:** report at `spec/library-index-composition-investigation-2026-05-26.md` (intent@53df962); recommended half-day Port A extension
- [ ] **library-index-mcp Port A `library_search_ranked` tool** — in progress, dispatched 2026-05-26
- [ ] **intent-knowledge MCP server 5 substrate verbs** — in progress, dispatched 2026-05-26 (query/get/list/lineage/freshness with classification enforcement)
- [ ] **Deploy `intent-knowledge.fastmcp.cloud/mcp`** — pending Agent 2 + Agent 4 completion
- [ ] **`entire-io.py` adapter** (WIT-004 #5) — separate Witness track; activates Tier 2 federation for Entire-trace path
- [ ] **Hook `session-end.sh` into Claude Code Stop event** — wiring step for per-product activation

### Query Operation
- [ ] Implement `query` operation: question → read _index.md → synthesize answer with [[citations]] → offer to file as new knowledge artifact
- [ ] Wire Flow 2: spec authoring queries knowledge base for personas, journeys, DDRs before writing specs

### Lint Operation
- [ ] Implement `lint` operation: contradictions, orphans, stale claims, missing cross-refs, coverage gaps
- [ ] Wire Flow 1: lint findings → suggested signals for Notice phase
- [ ] Add `lint_specs` tool to intent-observe MCP server (Recommendation #1)

### Bidirectional Flows
- [ ] Wire Flow 5: observe → domain knowledge base updates (double-loop learning)
- [ ] Wire Flow 6: observe → spec corpus updates (single-loop learning)
- [ ] Add `update_domain_knowledge` tool to intent-observe MCP server

### Navigation & Indexing
- [ ] Adopt _index.md + log.md navigation pattern in .intent/ (Recommendation #2)
- [ ] Implement compiled capability overview pages (Recommendation #3)

### Contamination & Provenance
- [ ] Add `origin` field (human | agent | synthetic) to all artifact schemas (Recommendation #6)
- [ ] Implement origin-aware trust scoring in signal-trust-framework

### Obsidian Bridge
- [ ] Ensure all markdown is Obsidian-compatible (YAML frontmatter, [[wikilinks]], Dataview-queryable)
- [ ] Publish Obsidian vault template (Recommendation #7)

## Autonomous — Agents can execute now

- [ ] Execute trace propagation → `tasks/trace-propagation.md` (unlocks all Observe work)
- [ ] Execute file tail adapter → `tasks/file-tail-adapter.md` (depends: trace propagation)
- [ ] Execute Grafana dashboard → `tasks/grafana-dashboard.md` (depends: file tail adapter)
- [ ] Emit signal cluster files to `.intent/` using cluster template (6 clusters identified in product-roadmap.md)
- [ ] Add `referenced_by` field to signal schema + update amplification scoring in models.py
- [ ] Refresh VERSION → 1.0.0, update CHANGELOG with three-layer architecture, domain knowledge base, knowledge-engine/AGENTS.md

## Completed — Done since last update

- [x] Build Intent, Spec, Contract templates → `.intent/templates/` (13 templates total)
- [x] Build `intent-spec` CLI tool → `bin/intent-spec`
- [x] Build 3 MCP servers (notice, spec, observe) → `servers/`
- [x] Define 6 subagent architecture → `servers/AGENT_DEFINITIONS.md`
- [x] Capture 24 signals (SIG-001 through SIG-024)
- [x] Spec observability stack (27KB) → `spec/observability-stack.md`
- [x] Configure OTel Collector → `observe/otel-collector-config.yaml`
- [x] Separate site to `theparlor/intent-site` with 23 pages, 3 pillars, 10 contracts
- [x] Enable GitHub Pages → live at `theparlor.github.io/intent/`
- [x] Update CLAUDE.md with four-product framing, agent handoff protocol

## Needs Learning — Requires human voice, external input, or architecture decision

- [ ] Write the Intent Manifesto — sharp, opinionated, shareable, 1500 words max (requires Brien's voice)
- [ ] Interview 5 practitioners experiencing AI + Agile friction (start with Ari's team)
- [ ] Document Brien's personal Intent methodology as Case Study #1
- [ ] Resolve vocabulary friction: "Notice" and "Execute" naming (SIG-019)
- [ ] Decide signal ID strategy for distributed environments (SIG-022/023)
- [ ] Sharpen audience personas — add company sizes, industries, day-in-the-life detail

## Parked — Blocked on prerequisite work

- [ ] Spec-to-agent handoff format (blocked: vocabulary decision + spec validation)
- [ ] Signal intelligence: clustering, pattern detection, promotion suggestions (blocked: ID strategy + trace propagation)
- [ ] Metrics framework (blocked: Grafana dashboard must be live with real data)
- [ ] Enterprise adoption path design (blocked: practitioner validation)
- [ ] Team size boundary research beyond 5 people (blocked: practitioner validation)

## Upgrade Plan Items — 2026-05-20 Audit (L4 backlog)

> Added 2026-05-20 from framework self-audit (14 items across 6 tracks).
> Source: `.intent/specs/2026-05-20-upgrade-plan.md`

### Track A — Catalog Completeness
- [x] **A1** — Family 1.7 (Artificial-gate-architecture drift) appended to `learnings/process-drift-catalog.md` — DONE 2026-05-20 (commit 07d40cf)
- [x] **A2** — Family 4.7 (Governance-skill-without-trigger) appended to `learnings/process-drift-catalog.md` — DONE 2026-05-20 (commit 07d40cf)

### Track B — Hook Completeness
- [x] **B1** — Layer 4 table-cell scanner: `COMPLETION_RE` in `hooks/closure-discipline-stop-check.sh` extended to catch `| Done |` / `| Complete |` / `| ✅ |` table cells — DONE 2026-05-20
- [x] **B2** — Overwatch staleness SessionStart hook: `hooks/overwatch-staleness-check.sh` installed + registered — DONE 2026-05-20 (commit 07d40cf)
- [ ] **B3** — Spec-age lint hook: PreToolUse/scheduled-task that identifies `.intent/specs/*.md` with `status: approved|ratified` + no corresponding `src/`/`bin/` code after 30 days. Emit signal per stale spec. (L4)

### Track C — Documentation Refresh
- [x] **C1** — CHANGELOG.md + VERSION bumped to `2026.05.20-0.11.0` — DONE 2026-05-20
- [x] **C2** — TASKS.md updated with audit items (this section) — DONE 2026-05-20
- [x] **C3** — Spawn prompt `spawn-prompts/framework-self-audit.md` authored — DONE 2026-05-20

### Track D — Signal Stream Hygiene
- [x] **D1** — ULID migration audit: 7 `SIG-NNN` + 79 date-slug legacy signals identified post-SPEC-003; migration tracking signal emitted — DONE 2026-05-20
- [x] **D2** — `.intent/README.md` subdirectory index authored — DONE 2026-05-20

### Track E — Implementation Gaps
- [x] **E1** — MCP tool count: `tools/intent-mcp/server.py` has 6 tools (not 7); CLAUDE.md `## MCP Server (7 tools)` heading corrected to 6 — DONE 2026-05-20
- [x] **E2** — FastMCP vs legacy migration: spec authored at `.intent/specs/SPEC-MCP-MIGRATION-2026-05-20.md` — DONE 2026-05-20
- [x] **E3** — KE CLI trigger signal emitted: `SIG-KE-CLI-IDD-TRIGGER-2026-05-20.md` filed; `bin/intent-knowledge` implementation deferred to its own IDD Execute loop — DONE 2026-05-20

### Track F — Observe Stage (L2 — deferred)
- [ ] **F1** — Observe dashboard spec refresh: L2 gate (Brien's preferred visualization surface unknown). Options: Grafana (`tasks/grafana-dashboard.md`), custom artifact (`artifacts/` React), or hosted service. Awaiting directional signal from Brien before speccing. Once directed, implementation is L4.

---

*Updated: 2026-05-20*
