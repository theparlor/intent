---
id: SPEC-UPGRADE-PLAN-2026-05-20
title: Intent Framework — Upgrade Plan 2026-05-20
type: upgrade-plan
status: ratified
date: '2026-05-20'
upstream_control_path: Core/frameworks/intent/.intent/specs/2026-05-20-upgrade-plan.md (this file) — tracked in intent repo; items execute as IDD loops with their own trigger signals
catch_mechanism: plan items are numbered and autonomy-classified; overnight orchestrator (Core/frameworks/intent/spawn-prompts/overnight-exhaustive-upgrade.md) consumes this as canonical backlog feeder; overwatch sweeps enforce item-level staleness
pipeline_survival: this spec is a self-contained triad-closed artifact; items it defines become independent IDD trigger signals; each item creates its own upstream_control when resolved
audit_source: framework self-audit — all 11 dimensions from orchestrator brief; source material read in full before writing
---

# Intent Framework — Upgrade Plan 2026-05-20

> Framework self-audit results + prioritized upgrade items. All items L4 unless a specific 4-gate failure is named.

---

## Audit Findings by Dimension

### Dimension 1 — IDD Dogfood (does Intent use its own loop?)

**Finding: Partial.** The `.intent/` directory structure dogfoods the Notice→Spec→Execute→Observe loop correctly. Signal capture is live (130 signals captured). Intents and specs exist. Events JSONL exists. However, the Observe stage is structurally the weakest: events.jsonl is populated by GitHub Action on push, but there is no live Observe dashboard, no active double-loop (Observe → Knowledge update), and no OTel collector receiving the file-tail adapter output. The Execute directory is thin by design ("execution happens in other repos"), but there is no active mechanism to verify that those other repos are feeding observations back.

**Gap:** Double-loop learning (Flow 5: Observe → Knowledge update) is spec'd but not wired. The intent.jsonl has events but no consumer visualization. The dogfood is real at capture and spec stages; it is partial at observe.

---

### Dimension 2 — 5-Layer Closure-Discipline Enforcement

**Finding: 5/5 layers deployed. One documentation gap remains (Layer 4 table-cell scanner).**

| Layer | Status |
|---|---|
| Layer 1: SessionStart banner (`closure-discipline-check.sh`) | Deployed |
| Layer 2: Memory file (`feedback_closure_discipline.md`) | Present |
| Layer 3: Soft-queue regex in Stop hook | Deployed via Layer 4 |
| Layer 4: Stop hook (`closure-discipline-stop-check.sh`) | Deployed |
| Layer 5: PreToolUse signal-file check (`closure-discipline-signal-check.sh`) | Deployed |

**Gap 2.1:** Layer 4 stop-hook does not scan table-cell completion claims ("Done" in markdown tables). Catalog Entry 2.3 names this — labeled "Manual discipline (no hook for table cells yet — candidate for Layer 4 extension)." This is the only remaining uncaught closure-drift variant at the hook layer.

---

### Dimension 3 — 5-Layer Autonomy-Grant Enforcement

**Finding: 6/6 layers deployed (spec counts 5; the dispatch-hook is Layer 5 in spec, counted as Layer 6 counting the soft-queue regex deepening separately). Full coverage.**

| Layer | Status |
|---|---|
| Layer 1: SessionStart banner (`autonomy-grant-check.sh`) | Deployed |
| Layer 2: 4-gate documented protocol | Documented |
| Layer 3/4: Stop hook v2 soft-queue deepening (`autonomy-grant-stop-check.sh`) | Deployed |
| Layer 4: Stop hook v1 bare-choice pattern (`autonomy-grant-stop-check.sh`) | Deployed |
| Layer 5: Dispatch-prompt pre-flight (`autonomy-grant-dispatch-prompt-check.sh`) | Deployed |
| Layer 6: Drift-telemetry | Partial — audit logs exist; no active feedback-loop to update regex |

**Gap 3.1:** The dispatch-hook override description was missing the "meta-instructional documentation" case until 2026-05-20 (SIG-HOOK-OVERRIDE-META-INSTRUCTIONAL-2026-05-20 → docs/8041524). Fix already landed; verify hook error message text is current.

**Gap 3.2:** Layer 6 (drift telemetry) has audit log files but no active feedback loop to surface regex-tuning recommendations. Audit logs accumulate silently.

**Gap 3.3:** Artificial-gate-architecture drift (Family 1, new pattern 1.7) is captured in SIG-ARTIFICIAL-GATE-DRIFT-PATTERN-2026-05-20 as a signal but is NOT yet added as an entry to `process-drift-catalog.md`. The signal explicitly flags this as a pending catalog addition.

---

### Dimension 4 — Signal-Stream Operational Health

**Finding: 130 signals captured; lifecycle schema correct; DoD library enforced by hooks.**

Signals span 2026-03-28 through 2026-05-20. The naming convention is mixed: original signals use `YYYY-MM-DD-slug.md`; newer signals use `SIG-NNN` sequential IDs and `SIG-LONG-ID-YYYY-MM-DD.md` patterns. ULID migration (SPEC-003, SIG-022) was specced — ID generation library exists in `bin/lib/id_gen.sh` per CLAUDE.md — but new signals since SPEC-003 continue to use sequential or date-slug names, not ULIDs. ULID migration is incomplete at the signal-file layer.

**Gap 4.1:** ULID migration (SPEC-003) is specced but new signals after SPEC-003 still use legacy naming. Approximately 11+ new `SIG-NNN` files were created post-SPEC-003.

**Gap 4.2:** `.intent/` structure listed in CLAUDE.md includes `approvals/`, `clusters/`, `config/`, `discovery/`, `elevations/`, `methodology/`, `plans/` directories not in the original CLAUDE.md spec inventory. No CONTEXT.md or README.md explains these subdirectories. Directory sprawl without index.

---

### Dimension 5 — Process-Drift-Catalog Completeness

**Finding: 4 families, 16 entries as of 2026-05-19. One new pattern captured but NOT yet appended inline.**

The catalog frontmatter (`status: ratified`, `date: 2026-05-20`) suggests it was updated today. But SIG-ARTIFICIAL-GATE-DRIFT-PATTERN-2026-05-20 explicitly states: "add to Family 1 as process-drift-catalog.md (append… new pattern entry)." The signal body describes the new pattern completely (symptom, mechanism, correction, prevention vector). The catalog file itself does not yet contain a "1.7 — Artificial-gate-architecture drift" entry.

**Gap 5.1:** New drift pattern 1.7 (Artificial-gate-architecture) exists as a signal but is not yet in the catalog body. Catalog is incomplete by one entry.

---

### Dimension 6 — Spawn-Prompts Library Coverage

**Finding: 7 prompts exist. Coverage is comprehensive; one gap identified.**

Current prompts:
1. `autonomy-grant-correction.md` — corrective posture restoration
2. `closure-discipline-audit.md` — audit for closure-discipline debt
3. `cowork-idd-with-panel-critique.md` — Cowork-targeted IDD + panel critique
4. `idd-audit-product.md` — product-level IDD audit
5. `idd-build-execute.md` — IDD build execution
6. `overnight-exhaustive-upgrade.md` — overnight orchestrator (updated 2026-05-20)
7. `process-drift-audit.md` — drift pattern audit

**Gap 6.1:** No spawn prompt exists for the "framework self-audit" pattern (the exact pattern this plan was created to address). The overnight orchestrator runs exhaustive product + framework + skill sweeps; a lighter `framework-self-audit.md` prompt would enable targeted Intent-only audits without the full overnight-scale context load. This is a legitimate new spawn prompt.

**Gap 6.2:** No spawn prompt for "overwatch rehabilitation" — the SIG-OVERWATCH-STALENESS-PATTERN-2026-05-20 identifies this as needed (Phase 5.5 items). Currently embedded in overnight orchestrator; extractable as standalone.

---

### Dimension 7 — Knowledge Engine Product Separation (DDR-005)

**Finding: Respected. No conflation found in current artifacts.**

DDR-005 (two-products warning) is the first thing in CLAUDE.md. The Knowledge Engine has its own directory (`knowledge-engine/`), its own AGENTS.md, its own specs. The MCP server for Knowledge Engine (`intent-knowledge`, port 8004) is specced separately from the Intent-notice MCP server. The 2026-05-20 playbooks and drift catalog use Intent methodology language without importing KE-specific operations.

**Gap 7.1:** TASKS.md Layer 1 items (Domain Knowledge Base Implementation) are listed as autonomous-executable, but the KE CLI (`intent-knowledge` with ingest/query/lint) has no implementation in `bin/` — only specs. The spec-vs-implementation gap for KE is wide and aging (specced 2026-04-06).

---

### Dimension 8 — Documentation Health

**Finding: CLAUDE.md is authoritative and current. CHANGELOG.md last updated 2026-04-13 (VERSION: 2026.04.13-0.10.0). TASKS.md accurate but stale for new items. README.md present but thin.**

**Gap 8.1:** CHANGELOG.md is 37 days stale. Multiple significant additions since 2026-04-13: IDD playbooks, drift catalog, dispatch hook (Layer 5), process-drift family additions, overnight orchestrator, overwatch rehabilitation. VERSION has not been bumped.

**Gap 8.2:** TASKS.md does not include any of the plan items identified in this audit (new Family-1.7 catalog entry, ULID migration completion, Observe dashboard, KE implementation, overwatch staleness hook). TASKS.md is a backlog but it is not live.

**Gap 8.3:** README.md has library YAML frontmatter but thin content. It is a public-facing artifact; the actual Intent methodology value is in CLAUDE.md, not README.md. The README does not reflect the current four-product maturity state or the IDD build discipline added in 2026-05.

---

### Dimension 9 — Sites Integration

**Finding: Site is in its own repo (`theparlor/intent-site`). Governance separation is correct per DDR-005 architecture. No coherence check possible without reading intent-site repo.**

**Gap 9.1:** The content-map.md in intent-site (which traces site claims back to specs here) was last referenced in CLAUDE.md context from 2026-04-06 period. The playbooks, drift catalog, IDD build pattern, and dispatch hook added since then are not referenced in any site-content trace. Content-map may be stale.

---

### Dimension 10 — CLI Suite Health

**Finding: 4 CLI tools present in `bin/`. All documented in CLAUDE.md. One tool (#5) from CLAUDE.md is listed but the MCP server tool count in CLAUDE.md says "7 tools" while the server.py interface is for 6 documented tool functions.**

The `bin/lib/id_gen.sh` ULID library exists (per CLAUDE.md, SPEC-003, SIG-022). The four main tools (`intent-signal`, `intent-intent`, `intent-spec`, `intent-status`) are operational. The `servers/` directory contains four FastMCP servers (notice, spec, observe, knowledge) with their own architecture — these are distinct from `tools/intent-mcp/server.py`.

**Gap 10.1:** CLAUDE.md says MCP server has "7 tools" but `## MCP Server (7 tools)` table lists only 6 rows. The `intent_start_timer` or similar seventh tool may have been added or the count is a documentation error. Needs verification.

**Gap 10.2:** `bin/intent-knowledge` (KE CLI with ingest/query/lint) is specced in SPEC-001 but absent from `bin/`. The gap between SPEC-001 spec and implementation is untracked.

---

### Dimension 11 — MCP Server Health

**Finding: Two MCP server implementations co-exist. `tools/intent-mcp/server.py` (7 tools, base `mcp` library) is the stable surface. `servers/` (FastMCP, 4 servers) is the architecture-forward version. Relationship between them is not documented as a migration path.**

**Gap 11.1:** No documented migration plan from `tools/intent-mcp/server.py` to `servers/`. CLAUDE.md describes both as current. Dual implementation creates maintenance surface without a sunset or merge timeline.

**Gap 11.2:** None of the 4 component venvs (`./`, `servers/`, `tools/intent-mcp/`, `observe/adapters/`) have confirmed setup. CLAUDE.md section "No venv — needs setup" has been present since April. No health check script exists to verify venv readiness.

---

### Dimension 12 — Anti-Patterns Not Yet in Catalog

Patterns observed during this audit not yet formally cataloged:

**New candidate 1.7:** Artificial-gate-architecture drift (already in SIG-ARTIFICIAL-GATE-DRIFT-PATTERN-2026-05-20 — pending catalog append per that signal's stated upstream_control_path).

**New candidate 5.1 (meta-framework pattern):** Governance-skill-without-trigger (overwatch staleness). Already captured in SIG-OVERWATCH-STALENESS-PATTERN-2026-05-20 as "symptom-repaired, upstream-pending." Needs Family 5 entry in catalog, or explicit statement that it belongs in Family 4 (Process/Coordination Drifts, entry 4.7).

**New candidate 5.2:** Spec-vs-implementation gap accumulation (KE CLI, ULID migration, Observe dashboard — specs that age without ever triggering implementation as IDD loops). The spec is captured; there is no periodic lint that identifies specs with no corresponding `execute/` artifacts or `src/` code after N days.

---

## Upgrade Plan Items

> Numbered. L4 default. L0 only where named gate failure exists. status:proposed ONLY with named gate failure.

### Track A — Catalog Completeness (2 items)

**A1 — Append Family 1.7 to process-drift-catalog.md** `[L4]`
Append the Artificial-gate-architecture drift pattern to `Core/frameworks/intent/learnings/process-drift-catalog.md` Family 1, after entry 1.6. Full pattern spec is in SIG-ARTIFICIAL-GATE-DRIFT-PATTERN-2026-05-20. The signal's `upstream_control_path` explicitly names this catalog as the destination.

**A2 — Append Family 4.7 (overwatch-staleness) to process-drift-catalog.md** `[L4]`
Append "Governance-skill-without-trigger" as entry 4.7 under Family 4. Pattern body in SIG-OVERWATCH-STALENESS-PATTERN-2026-05-20. Cross-link to the sibling pattern (A1).

---

### Track B — Hook Completeness (3 items)

**B1 — Layer 4 table-cell scanner extension** `[L4]`
Extend `closure-discipline-stop-check.sh` to scan response text for markdown table rows where a cell contains "Done" or "Complete" or "✅" without a "catch-net" or "upstream control" neighbor. This is Catalog Entry 2.3 "candidate for Layer 4 extension." Extends the existing stop-hook regex; does not require new hook file.

**B2 — Overwatch staleness SessionStart hook** `[L4]`
Author `~/.claude/hooks/overwatch-staleness-check.sh` per SIG-OVERWATCH-STALENESS-PATTERN-2026-05-20 §5.5.1. Emits banner if most-recent overwatch journal mtime > 7 days; emits load-bearing posture if > 14 days. Register in `~/.claude/settings.json` SessionStart array. This is the upstream control that closes SIG-OVERWATCH-STALENESS-PATTERN-2026-05-20.

**B3 — Spec-age lint hook (new)** `[L4]`
Author a PreToolUse hook or scheduled-task audit that identifies `.intent/specs/*.md` files with `status: approved` or `status: ratified` that have no corresponding code in `src/` or `bin/`, and emits a signal per stale spec after N days (configurable threshold, default 30). Addresses new candidate 5.2 (spec-vs-implementation gap accumulation).

---

### Track C — Documentation Refresh (3 items)

**C1 — Bump CHANGELOG.md and VERSION** `[L4]`
Add entries for: IDD playbooks (2026-05-20), drift catalog (2026-05-19/20), dispatch hook Layer 5 (2026-05-19), overnight orchestrator (2026-05-20), overwatch rehabilitation. Bump VERSION from `2026.04.13-0.10.0` to `2026.05.20-0.11.0`. Minor version bump (new capabilities).

**C2 — Update TASKS.md** `[L4]`
Add plan items from this upgrade plan as backlog items in TASKS.md, partitioned by autonomy level. Current TASKS.md does not reflect the playbooks, drift catalog, dispatch hook, or overwatch work added since 2026-04-13. Do NOT use `git add .` — stage TASKS.md specifically.

**C3 — Spawn prompt: framework-self-audit** `[L4]`
Author `Core/frameworks/intent/spawn-prompts/framework-self-audit.md` — a targeted single-framework audit prompt (lighter than overnight-exhaustive-upgrade). Uses this spec as the template for output format. Covers: IDD dogfood test, hook coverage, signal health, catalog completeness, spawn-prompt gaps, documentation staleness.

---

### Track D — Signal Stream Hygiene (2 items)

**D1 — ULID migration completion audit** `[L4]`
Identify all signal files created after SPEC-003 (2026-04-09) that still use legacy naming (`SIG-NNN` sequential or `YYYY-MM-DD-slug`). Produce a count. Emit one migration-tracking signal. The migration itself (renaming files) is L4 — reversible, local, precedented — but may need separate scheduling due to volume.

**D2 — .intent/ subdirectory index** `[L4]`
Create a `Core/frameworks/intent/.intent/README.md` that indexes all subdirectories (`approvals/`, `clusters/`, `config/`, `decisions/`, `discovery/`, `elevations/`, `events/`, `intents/`, `methodology/`, `plans/`, `signals/`, `specs/`, `templates/`) with a one-line purpose per directory. Gap 4.2. Prevents directory-sprawl confusion for agents and contributors.

---

### Track E — Implementation Gaps (3 items)

**E1 — MCP server tool-count verification** `[L4]`
Read `tools/intent-mcp/server.py` and count actual tool definitions. Reconcile against CLAUDE.md claim of "7 tools" vs 6-row table. Update CLAUDE.md to match. Small but hygiene-critical (CLAUDE.md is the agent's primary orientation document).

**E2 — FastMCP vs. legacy MCP migration path** `[L4]`
Author a migration-intent spec or decision record: is `tools/intent-mcp/server.py` (legacy) being deprecated in favor of `servers/` (FastMCP)? Or are both maintained indefinitely? This is a speccing decision, not an implementation task. Clears the dual-implementation ambiguity (Gap 11.1).

**E3 — KE CLI implementation trigger** `[L4]`
Emit an IDD trigger signal for `bin/intent-knowledge` implementation (SPEC-001 specced 2026-04-06, 44 days without implementation). The signal becomes the Notice for a dedicated KE-CLI IDD loop. Do NOT implement inline — this is a scoped IDD loop that deserves its own Execute stage and DoD.

---

### Track F — Observe Stage (1 item, L2)

**F1 — Observe dashboard spec refresh** `[L2 — info gap: Brien's preferred visualization surface]`
The Observe stage roadmap (product-roadmap.md) specifies a dashboard but has multiple implementation options: signals.html in docs/ (scrapped per CLAUDE.md "no docs/ folder"), Grafana (tasks/grafana-dashboard.md), custom artifact, or the `artifacts/` React component approach. Gate failure: Brien's preferred visualization surface is not known. Surface the options and await a directional signal before speccing an Observe dashboard. Note: once directed, implementation is L4.

---

## Summary

- **Total items:** 14 upgrade plan items across 6 tracks
- **L4 items:** 13 (93%)
- **L2 items:** 1 (F1 — observe dashboard — info gap on visualization surface preference)
- **L0 items:** 0

**Top 3 gaps by priority:**
1. **Drift catalog incomplete** — new 1.7 pattern captured as signal but not appended inline (A1)
2. **Overwatch has no trigger** — governance sweep relies on Brien's memory; no hook or scheduled task fires it (B2)
3. **CHANGELOG+VERSION 37 days stale** — significant additions since April not versioned (C1)

**New drift patterns identified for catalog addition:**
- 1.7: Artificial-gate-architecture drift (Family 1 — already in signal, pending append)
- 4.7: Governance-skill-without-trigger (Family 4 — meta-pattern: overwatch/periodic governance tools with no auto-trigger)
- New candidate for Family 5: Spec-vs-implementation gap accumulation (specs that age without triggering IDD execute loops)
