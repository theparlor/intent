---
title: Phase 2 Dispatch Brief — Code Filing Instructions
created: 2026-05-26
depth_score: 4
depth_signals:
  file_size_kb: 7.9
  content_chars: 7668
  entity_count: 0
  slide_count: 0
  sheet_count: 0
  topic_count: 0
  has_summary: 0
vocab_density: 0.26
session_origin: Cowork Phase 1
session_target: Claude Code
owner: brien
status: ready-to-dispatch
parent_deliverables: /Users/brien/Workspaces/Core/frameworks/intent/handoff/cowork-phase1-2026-05-26/
---
# Phase 2 Dispatch Brief — Filing Instructions for Code

Brien: paste this whole document into Claude Code when you're ready to file. It is self-contained — Code does not need to ask you anything before executing.

## What this is

This is the Phase 2 (filing) action plan from the 2026-05-26 Cowork Phase 1 (thinking) session. Cowork produced seven artifacts at `/Users/brien/Workspaces/Core/frameworks/intent/handoff/cowork-phase1-2026-05-26/`. Brien has closed the five open decisions (four matched recommendations; D5 was an override widening scope to include client engagements from Day 1). Code's job is mechanical filing per the routing instructions below.

## Brien's closes (canonical record)

| # | Decision | Close | Note |
|---|---|---|---|
| 1 | Hosting | **Cloud (FastMCP / Cloudflare Workers)** | matches recommendation |
| 2 | R/W scope | **Read-only first** | matches recommendation |
| 3 | Witness adapter timing | **Ship runbook now, Tier 2 conditional** | matches recommendation |
| 4 | Publish two-observabilities post | **YES (defaulted)** | 7-day rule, not overridden |
| 5 | Scope of "any product" | **D5-refined: tier-aware Day 1, redaction-map deferred** | **OVERRIDE + REFINEMENT** — Brien picked a third option beyond the original D5 binary |

D5-refined has already been re-threaded across the staged deliverables (01, 02, 03, 05, 06). Code does **not** need to re-edit these — they are filing-ready as staged.

**D5-refined in one paragraph for the Code agent:** The substrate-exposure architecture is built tier-aware Day 1 (classification schema, scope-token mechanism, binary policy enforcement at the MCP server) so engagement-tier query is a config-only light-up later, not a refactor. What ships Day 1 is internal-tier substrate query. Engagement substrate is scaffolded with full classification metadata but federation to Witness is deferred until Phase 2; chat-surface query against engagement substrate returns absent (404 / no hits) Day 1. When Brien needs engagement query, he authors that engagement's `redaction-map.yaml` (~30 min one-time), flips the federation switch, and the already-built server picks up the engagement-scope token. Phase 1 target: ~2.5-3 weeks.

## Filing actions (in dependency order)

### Step 1 — File the DDRs (lowest blast radius first)

**WS-DDR-099 (Workspaces-level):**
- Source: `/Users/brien/Workspaces/Core/frameworks/intent/handoff/cowork-phase1-2026-05-26/03-WS-DDR-099-substrate-exposure-mcp-front-repo-as-truth.md`
- Action: Append the YAML+body sections to `/Users/brien/Workspaces/.context/DECISIONS.md` after WS-DDR-098.
- Index row to add (near top of file with other WS-DDR-NNN index rows): `| WS-DDR-099 | Substrate exposure via MCP-front + repo-as-truth composition | accepted | 2026-05-26 | 0.88 |`

**DEC-010 (Intent-framework-local):**
- Source: `04-DEC-010-intent-knowledge-mcp-scope-extension.md`
- Action: Append to `/Users/brien/Workspaces/Core/frameworks/intent/spec/decision-log.md` immediately after DEC-009. Match the existing DEC-NNN heading + body shape.

**DEC-011 (Intent-framework-local):**
- Source: `05-DEC-011-intent-init-scaffold-script.md`
- Action: Append to `/Users/brien/Workspaces/Core/frameworks/intent/spec/decision-log.md` immediately after DEC-010.

### Step 2 — File the architecture brief (Track A)

- Source: `01-track-a-substrate-exposure-architecture.md`
- Destination: `/Users/brien/Workspaces/Core/frameworks/intent/spec/substrate-exposure-architecture.md`
- Action: Copy (do not move — keep the handoff staging copy as historical record). Update frontmatter `proposed_destination` → `actual_destination` field if you want; otherwise drop the staging-frontmatter and use canonical spec-file frontmatter shape.
- Add one-line entry in `/Users/brien/Workspaces/Core/frameworks/intent/ARCHITECTURE.md` near where intent-knowledge is discussed (line 111 area): "Substrate exposure verbs land per `spec/substrate-exposure-architecture.md` (WS-DDR-099 + DEC-010, 2026-05-26)."

### Step 3 — File the composition runbook (Track B)

- Source: `02-track-b-spawn-a-product-runbook.md`
- Destination: `/Users/brien/Workspaces/Core/frameworks/intent/playbooks/spawn-a-product.md`
- Action: Copy (do not move — same reason as Step 2). The `playbooks/` directory already exists with `cross-product-applicability.md` and `idd-build-pattern.md`.
- Note: this runbook contains an engagement-classification section per Brien's D5 override. Do not remove or weaken it.

### Step 4 — Update memory hygiene

`/Users/brien/.claude/projects/-Users-brien-Workspaces/memory/reference_entire_io.md` already got refreshed in the 2026-05-26 Phase 2 work that closed the audit. No further memory updates required from this session.

### Step 5 — Optional: draft the two-observabilities post (D4 defaulted YES)

- D4 defaulted YES per the 7-day rule. Brien did not explicitly close otherwise.
- Suggested destination: `/Users/brien/Workspaces/Core/frameworks/intent-site/posts/two-observabilities.md` (verify intent-site post structure first; if the site has a different convention, follow it).
- Target length: ~600-800 words. Hook: cockpit / aircraft metaphor (per DEC-009 §"What it observes" table).
- Brien marked this as "non-blocking" — file the structural docs (Steps 1-3) first, draft the post as a follow-on commit.
- If you are out of time / context, you can defer this to a separate Cowork or Code session without breaking anything.

### Step 6 — Commit shape

Recommended commits:
1. `Phase 2 filing: WS-DDR-099 (substrate exposure), DEC-010 (intent-knowledge scope), DEC-011 (intent-init scaffold)` — DDRs only
2. `Phase 2 filing: substrate-exposure architecture brief + spawn-a-product runbook` — the two long-form docs
3. (Optional) `Phase 2 filing: draft two-observabilities framework post`

Each commit should reference the source-of-truth paths under `handoff/cowork-phase1-2026-05-26/` in its commit message for traceability.

## Validation checklist (after filing)

- [ ] WS-DDR-099 appears in `.context/DECISIONS.md` index row + body.
- [ ] DEC-010 and DEC-011 appear in `spec/decision-log.md` in order after DEC-009.
- [ ] `spec/substrate-exposure-architecture.md` exists with full architecture content.
- [ ] `playbooks/spawn-a-product.md` exists with the engagement-classification section preserved.
- [ ] `ARCHITECTURE.md` has the one-line cross-reference to the new spec.
- [ ] Handoff staging directory `cowork-phase1-2026-05-26/` is untouched (it remains the historical Phase 1 record).
- [ ] Render pipeline (if a `render_all` runs) does not throw on the new spec file or playbook.

## What this filing does NOT do

- Does not implement the MCP server (Track A). That's a future engineering milestone.
- Does not implement `bin/intent-init` (Track B). That's a future engineering milestone.
- Does not implement `engine/adapters/entire-io.py` (Witness WIT-004 #5). That's scheduled separately.
- Does not modify rendered Observe-leg pages (`observe.html`, `observe/README.md`). Phase 1 audit confirmed those are correct.

## If anything in this brief is unclear

The full Cowork Phase 1 work is at `/Users/brien/Workspaces/Core/frameworks/intent/handoff/cowork-phase1-2026-05-26/`. Read `00-README.md` first, then 01-06 as needed. The two-observabilities frame (DEC-009) and the substrate-as-sibling principle (WS-DDR-025) are the load-bearing reasoning anchors — do not weaken them when interpreting any ambiguity.

---

*Phase 1 (Cowork) thinking is complete and re-threaded for Brien's D5 override. Phase 2 (Code) action: execute steps 1-6 above. Estimated work: ~30 minutes if no surprises.*
