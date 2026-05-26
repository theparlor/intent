---
title: "Spawn Prompt — Overnight Exhaustive Upgrade (all Workspaces products/frameworks/skills) + Overwatch-Driven Backlog"
id: SPAWN-OVERNIGHT-EXHAUSTIVE-UPGRADE
type: orchestrator-spawn-prompt
created: 2026-05-20
updated: 2026-05-20 (overwatch integration; overwatch is the canonical work-backlog feeder)
depth_score: 4
depth_signals:
  file_size_kb: 24.6
  content_chars: 18590
  entity_count: 0
  slide_count: 0
  sheet_count: 0
  topic_count: 0
  has_summary: 0
vocab_density: 0.22
target: new Claude Code session (NOT Cowork — orchestrator dispatches Agent subagents in parallel)
status: canonical
model_pin: Opus (orchestrator); subagent model varies (Sonnet for mechanical, Opus for synthesis)
upstream_control_path: Core/frameworks/intent/spawn-prompts/overnight-exhaustive-upgrade.md (this file)
catch_mechanism: "posture preamble + dispatch hook (Layer 5) blocks any subagent prompt that injects proposal-framing; closure-DoD triad required in every artifact; reply-format constraint forbids questions back to Brien except on genuine L0; full /overwatch sweep is mandatory Phase 1 before any dispatch"
pipeline_survival: "self-contained pasteable artifact; orchestrator session burns the token budget over its wall-clock window; every artifact lands inline with commits; nothing waits on Brien; overwatch-rehabilitation track installs SessionStart staleness hook so this never silently rots again"
usage: "cat ~/Workspaces/Core/frameworks/intent/spawn-prompts/overnight-exhaustive-upgrade.md | pbcopy Open a NEW Claude Code session (NOT Cowork — orchestrator needs Agent tool to dispatch subagents). Pin Opus. Paste as opening message. Set yourself a sleep timer; come back at reset."
---
# Overnight Exhaustive Upgrade — All Workspaces Products / Frameworks / Skills

> You are the ORCHESTRATOR for an overnight exhaustive upgrade pass across the entire Workspaces ecosystem. You have ~10 hours of wall-clock + 55% of the weekly All Models budget remaining. Brien has set a hard autonomy grant — execute, do not propose, do not gate on him. He is sleeping; he expects to wake to landed work.

---

## Posture (load-bearing — DO NOT skip; the dispatch hook will block any subagent prompt that violates this)

Read these specs into context BEFORE dispatching ANY subagent:

1. `~/Workspaces/Core/frameworks/intent/spec/autonomy-grant-enforcement.md`
2. `~/Workspaces/Core/frameworks/intent/spec/closure-discipline-enforcement.md`
3. `~/Workspaces/Core/frameworks/intent/playbooks/idd-build-pattern.md`
4. `~/Workspaces/Core/frameworks/intent/playbooks/cross-product-applicability.md`
5. `~/Workspaces/Core/frameworks/intent/learnings/process-drift-catalog.md`
6. `~/Workspaces/Core/frameworks/intent/.intent/signals/SIG-ARTIFICIAL-GATE-DRIFT-PATTERN-2026-05-20.md` (the freshest drift pattern — do NOT architect new L0 gates)
7. `~/Workspaces/Core/frameworks/intent/knowledge-engine/templates/subagent-dispatch-prompt.md` (use this template for EVERY subagent dispatch)
8. `~/.claude/CLAUDE.md` (Brien's global instructions; autonomy grants and project inventory)

**Autonomy posture for THIS overnight run:**
- Default: L4 — execute + signal for all Workspaces-local reversible work
- **No L0 gates may be created** during this run. The artificial-gate-architecture drift pattern is freshly captured — do NOT replicate it. If a substream produces an artifact that would normally trigger "Brien-L0 sign", instead: produce the artifact + a pre-verification scan + leave it ratified with the algorithmic ground truth as source of truth.
- **No proposal framing** in any subagent dispatch prompt. Use the dispatch-prompt template; the Layer 5 hook will block violations.
- **No "designed human checkpoints" introduced** in any new spec. Audit every proposed gate with the question: "Is human judgment the ONLY source of truth?" If no → L4, not L0.
- L0 boundary is unchanged: external comms with humans, money movements, sign-offs only Brien can give. Nothing in this run should hit L0 except discovery of genuinely external dependencies.

---

## Workspaces inventory (your dispatch targets)

### Products (`Core/products/`)
1. **Cast** — persona engine (`Core/products/cast/`)
2. **Forge** — composition engine, skill rendering (`Core/products/forge/`)
3. **Voices** — judgment/critique, ARB engine (`Core/products/voices/`)
4. **Loom** — coordination substrate, awareness pipeline (`Core/products/loom/`)
5. **Topography** — planning, score/active/handoff (`Core/products/topography/`)
6. **Throughline** — Phase 1 intent-trace, vision-thread (`Core/products/throughline/`)
7. **Parallax** — Phase 3 umbrella (`Core/products/parallax/`)
8. **Fieldbook** — expense lifecycle (`Core/products/fieldbook/`)
9. **Library-Index** — library catalog + MCP (`Core/products/library-index/`, `library-index-mcp/`)
10. **Cortège** — fetch fabric (`Core/products/cortege/`)
11. **Pulse** — daily brief, alpha watch (`Core/products/pulse/`)
12. **Witness** — observability (`Core/products/witness/`)
13. **Conduit** — `Core/products/conduit/`
14. **Digital-Declutter** — `Core/products/digital-declutter/`
15. **Reference-Substrate** — `Core/products/reference-substrate/`
16. **Studio-Control** — `Core/products/studio-control/`
17. **Org-Design-Tooling** — `Core/products/org-design-tooling/`

### Frameworks (`Core/frameworks/`)
1. **Intent** — IDD framework (`Core/frameworks/intent/`)
2. **Coherence-Engineering** — discipline (`Core/frameworks/coherence-engineering/`)
3. **Methodology-Library** — (`Core/frameworks/methodology-library/`)
4. **Knowledge-Engine** — (`Core/frameworks/knowledge-engine/`)
5. **Operating-Model** — (`Core/frameworks/operating-model/`)
6. **Capability-Maturity** — (`Core/frameworks/capability-maturity/`)
7. **Design-Systems** — (`Core/frameworks/design-systems/`)
8. **Governance** — (`Core/frameworks/governance/`)
9. **Investment** — (`Core/frameworks/investment/`)
10. **Measurement** — (`Core/frameworks/measurement/`)
11. **Patterns** — (`Core/frameworks/patterns/`)
12. **Protocols** — (`Core/frameworks/protocols/`)
13. **Transformation** — (`Core/frameworks/transformation/`)
14. **Assessment** — (`Core/frameworks/assessment/`)
15. **Product-Academy** — (`Core/frameworks/product-academy/`)
16. **Intent-Site** — (`Core/frameworks/intent-site/`)

### Skills + assets
- **62 Claude Code skills** rendered through Forge at `Core/products/forge/outputs/claude-code/`
- **244 rendered personas** at `Core/products/forge/outputs/claude-code/personas/` (220 personality + 14 archetype + 2 discipline + 4 role + 2 integrated + 2 audience)
- **Skill catalog**: read `Core/products/forge/outputs/claude-code/INDEX.md` or equivalent
- **Reference assets**: `Core/reference/rate-card/`, `Core/reference/materials/brass/`, `Core/reference/usage-tracker/`, etc.

---

## The overnight plan — 7 phases, parallelized (overwatch-fed)

### Phase 0 — Orchestrator boot (your first 10 minutes)

1. Read all 8 posture sources above. Internalize.
2. Run `ls Core/products/ Core/frameworks/` to confirm the inventory above matches reality (catch new directories that landed since this prompt was authored).
3. For each product + framework, do a 30-second `ls` and `head CONTEXT.md` to know what state it's in (active, dormant, just-scaffold, deeply-built). This shapes your phase-3 dispatch grouping.
4. DO NOT build the task list yet — wait for overwatch findings (Phase 0.5) to feed in. Premature task lists miss governance/MCP/memory drift the overwatch sweep surfaces.

### Phase 0.5 — RUN /overwatch IN FULL (mandatory; do this before dispatching ANY subagent)

> **Why this exists:** The last overwatch journal in `Core/products/org-design-tooling/journal/` is dated 2026-05-08 — **12 days stale as of this prompt's authoring**. Overwatch is a manual `/overwatch` slash command with ZERO auto-trigger hooks. Brien has ADHD and forgets to run it. The governance skill that catches drift is itself subject to drift because nothing reminds anyone to fire it. This is the failure mode that allowed this orchestrator prompt to be authored without a fresh state-of-the-system view. **The orchestrator MUST run overwatch first; the overwatch findings ARE the work-backlog feeder.**

1. Invoke `/overwatch` (the skill at `~/Workspaces/.claude/commands/overwatch.md`, also rendered at `Core/products/forge/outputs/claude-code/meta/overwatch/`). Run ALL 11 sections fully, not the lightweight version.
2. As findings land, classify each into one of four buckets:
   - **INLINE-FIXABLE** — stale memory entry (no write-through hook), governance compliance miss, dead MCP probe with restart recipe, dark-zone signal stub-creation → fix inline during Phase 2
   - **WRITE-THROUGH FAILURE** — memory file stale despite having a hook (e.g., `engagement-onboarding.sh` not firing; persona-intake Stage 6 not syncing) → emit a closure-disciplined signal AND dispatch a Sonnet agent to repair the hook in Phase 2 → catch_mechanism is the hook itself
   - **PRODUCT-LEVEL UPGRADE** — finding implicates a specific product/framework's standard (e.g., persona freshening pipeline never fired; loom/topography in dark zone) → feed into the per-product audit in Phase 3
   - **STRUCTURAL GAP** — an active engagement or product has no `.intent/` directory at all → backlog into Phase 8 (Overwatch Rehabilitation track)
3. Write the overwatch report to `~/Workspaces/Core/products/org-design-tooling/journal/JRN-20260520-overwatch-overnight-orchestrator.md` AND its sibling `EXT-20260520-overwatch-overnight-orchestrator.md` (matching the existing journal pattern).
4. ALSO read the 9 carry-forward items in `~/Workspaces/Core/products/forge/.intent/HANDOFF-2026-04-15-overwatch-hardening.md` — most have not shipped. Merge them into the four buckets above.
5. NOW build the task list using `TaskCreate` — one task per product, one per framework, plus the four bucket-derived task families from overwatch, plus the Phase 8 rehabilitation tasks. Aim for ~40-55 tasks total.

### Phase 1 — Parallel audit + upgrade-plan generation (per product/framework, overwatch-informed)

Dispatch N Sonnet subagents (one per product, one per framework — aim for ~25-30 parallel agents over the phase, but launch in waves of 8-10 to keep your context manageable). **Each subagent dispatch prompt MUST include the per-product overwatch findings** (the PRODUCT-LEVEL UPGRADE bucket from Phase 0.5), not just the generic standard. Each agent:

1. **Audits** the target product/framework against "highest internal standard" as defined by:
   - IDD pattern (5 load-bearing patterns from playbook)
   - Closure-DoD triad present in every closure claim
   - 4-gate autonomy posture honored in every decision artifact
   - Test coverage at the substantive-contribution level (not coverage-theater)
   - Schema invariants present and enforced
   - Cross-product boundaries respected (WS-DDR-070 Cast↔Forge↔Voices boundary; WS-DDR-025 sibling-over-parent-child)
   - Documentation present (CONTEXT.md, INTENT.md if applicable, ARCHITECTURE.md if applicable, README.md)
   - **Overwatch findings for this product** — disconfirmation tensions (11a), dark zones (11b), high-risk freshening (11c), governance miss (9a-9e), MCP probe failures (5), structural gap on `.intent/` dir
2. **Produces an upgrade plan** as `~/Workspaces/Core/products/<name>/.intent/specs/2026-05-20-upgrade-plan.md` (or framework equivalent). Plan structure:
   - Frontmatter with literal triad keys
   - Current state assessment (including overwatch findings for this product, verbatim)
   - Gap to highest standard (specific items, not vague)
   - Plan items: numbered, each with target file path, exit criterion, autonomy class (L4 default), TDD-applicable-yes/no
   - Anti-pattern audit (which Family 1-4 drifts present, if any)
   - Dependency graph (what blocks what within this product)
3. **Identifies L4-eligible items** that can be executed in Phase 2 by another agent without further input

Dispatch prompt template for each: use the subagent-dispatch-prompt template at `~/Workspaces/Core/frameworks/intent/knowledge-engine/templates/subagent-dispatch-prompt.md`. Customize per-product but keep the posture preamble verbatim. **Append the per-product overwatch findings section to the customization slot.**

### Phase 2 — Parallel execution: per-product L4 upgrades + overwatch INLINE-FIXABLE + WRITE-THROUGH-FAILURE repairs

Three parallel work streams in this phase. NO PR-style review of plans — execute. Each agent commits per item with terse HEREDOC + Co-Authored-By.

**Stream 2a — Per-product L4 upgrades.** For each upgrade plan from Phase 1, dispatch a Sonnet agent to execute the L4-eligible plan items inline. Each agent:
- Loads the upgrade plan from Phase 1
- Executes each L4 item in order (or in parallel within-plan if safe)
- TDD where applicable (RED before GREEN)
- Reports completion + remaining-L0 items per plan (should be NEAR-ZERO L0 items per the artificial-gate posture)

**Stream 2b — Overwatch INLINE-FIXABLE bucket.** For each finding tagged INLINE-FIXABLE in Phase 0.5, dispatch a Sonnet agent (or batch into a single agent if mechanical) to fix in place. Examples: stale memory entries without write-through hooks (grace-period fix), dead MCP probe with restart recipe, dark-zone signal stub creation, governance compliance misses (root-clean, Core-clean, engagement schema). One-line commits.

**Stream 2c — Overwatch WRITE-THROUGH-FAILURE repairs.** For each write-through hook overwatch flagged as broken or not-firing, dispatch a Sonnet agent to:
1. Read the existing hook script (e.g., `Core/products/org-design-tooling/src/engagement-onboarding.sh`)
2. Diagnose why it isn't firing (missing trigger, broken edit step, schedule absent)
3. Repair the hook
4. Open a closure-disciplined signal with `upstream_control_path:` = the hook script path and `catch_mechanism:` = the hook itself
5. Run the hook manually to verify the write-through pipeline now closes

Reference: `Core/products/forge/.intent/HANDOFF-2026-04-15-overwatch-hardening.md` Track A items A1-A3 are the carry-forward write-through repairs already specced — execute them here if overwatch surfaces them.

**Hard rule:** Phase 2 agents may NOT introduce new L0 gates. If a Phase 1 plan item is labeled L0 erroneously, the Phase 2 agent runs the 4-gate audit and reclassifies to L4 inline. If it genuinely fails 4-gate (rare), it gets named with the failing-gate justification and the rest of the plan proceeds.

### Phase 3 — Architectural documentation refresh (per product)

After Phase 2 lands, dispatch Sonnet agents to refresh architectural docs per product/framework:
- `ARCHITECTURE.md` — current architecture, design decisions, boundaries
- `CONTEXT.md` — schema, what's in the directory, how it composes with siblings
- `INTENT.md` — the IDD anchor if applicable (Notice → Spec → Execute → Observe state)
- `README.md` — top-level entry point
- Cross-product references: every doc that mentions another product must cite the current canonical path

Per product, write a single commit per file-type refreshed. NO mass-rewrites that destroy history; surgical updates preserving structure.

### Phase 4 — Marketing / promotional / how-to-use documentation

For each product, dispatch a Sonnet agent (with Opus reserved for the cross-product narrative) to produce:
- `docs/how-to-use.md` — quickstart, common workflows, the 3 most-valuable invocations
- `docs/positioning.md` — what this product is FOR (audience, problem, value), how it fits in the ecosystem
- `docs/examples/` — 2-3 concrete worked examples per product

**Marketing voice constraints (from Brien's memory):**
- NO sports metaphors (per `feedback_no_sports_metaphors.md`)
- Visual analogies + system-design metaphors land well
- Direct, specific, tradeoff-naming language
- First principles framing over best-practices framing
- Cite the masters (Cagan, Torres, Dunford, Patton, etc.) accurately when invoked; never templates

### Phase 5 — Ecosystem-level synthesis (Opus required)

Dispatch ONE Opus agent (the heavy lift) to produce the cross-product synthesis:
- `~/Workspaces/Core/ECOSYSTEM-ARCHITECTURE-2026-05-20.md` — the canonical ecosystem map: how all products + frameworks compose; the data flows; the dissent oracle; the IDD loops
- `~/Workspaces/Core/ECOSYSTEM-MARKETING-NARRATIVE-2026-05-20.md` — the unifying narrative: what this body of work IS, why it exists, what it enables, who it serves
- `~/Workspaces/Core/ECOSYSTEM-HOW-TO-USE-2026-05-20.md` — the entry-point guide: where to start, common cross-product workflows, how to dispatch subagents using the spawn-prompts library
- Run a final closure-discipline audit across ALL artifacts produced during this run; reclassify any drift inline

### Phase 5.5 — Overwatch Rehabilitation track (NEW — prevents the 12-day-stale failure mode from recurring)

> **Why this exists:** Overwatch was 12 days stale when this prompt was authored. It is the governance skill that catches drift everywhere else, but it has no auto-trigger of its own — so it silently rots. The orchestrator MUST install structural fixes so this never recurs.

Dispatch ONE Sonnet agent to execute this track in parallel with the per-product work:

**Item 5.5.1 — SessionStart staleness alarm hook.** Author `~/.claude/hooks/overwatch-staleness-check.sh` that:
1. Reads the most recent `JRN-*overwatch*` file mtime from `Core/products/org-design-tooling/journal/`
2. If `> 7 days` old, emits a SessionStart banner: `⚠️ Overwatch last ran N days ago — run /overwatch before non-trivial work`
3. If `> 14 days` old, escalates the banner to load-bearing posture (similar in tone to the closure-discipline-enforcement and autonomy-grant-enforcement banners) so it cannot be silently ignored
4. Register the hook in `~/.claude/settings.json` (or local equivalent) under the SessionStart event
5. Test by running the hook manually; verify the banner emits correctly given current 12-day staleness

**Item 5.5.2 — Scheduled overwatch (optional, L4).** If the scheduled-tasks MCP is operational, create a `mcp__scheduled-tasks__create_scheduled_task` entry for a weekly `/overwatch` run (every Mon 09:00 ET). This is L4: reversible (task list management), local blast (writes only to journal), precedent (other Brien-solo scheduled tasks exist), no info gap. Just do it. If the scheduled-tasks MCP is unavailable, document the gap in a signal and fall back to the staleness banner alone.

**Item 5.5.3 — Address HANDOFF-2026-04-15-overwatch-hardening.md carry-forward items.** Read `Core/products/forge/.intent/HANDOFF-2026-04-15-overwatch-hardening.md` and execute the un-shipped items (A1-A3 Track A, B-track spawn prompts). Specifically:
- A1: Fix `engagement-onboarding.sh` write-through (P1) — this is also a Stream 2c WRITE-THROUGH-FAILURE candidate; coordinate to avoid double-execution
- A2: Run first persona-freshening pipeline cycle (P2) — the 2026-04-29 deadline is past; treat as overdue, not just upcoming
- A3: Active-engagement `.intent/signals/` stub auto-creation (P2) — close the structural gaps overwatch flags

**Item 5.5.4 — Surface overwatch in the daily/weekly summary skills.** Update `weekly-summary` and `daily-digest` skills (at `Core/products/forge/outputs/claude-code/`) to include an "Overwatch status" section that shows the last-run date and any open findings. This makes overwatch visible in the existing reporting cadence Brien already consumes.

**Item 5.5.5 — Capture the meta-pattern as a drift entry.** Add a drift-catalog entry at `Core/frameworks/intent/learnings/process-drift-catalog.md` documenting the pattern: "Governance skills without auto-triggers silently rot. Manual invocation depends on the operator remembering; ADHD + 12-day gaps are predictable. Fix: every governance skill MUST have a SessionStart staleness alarm OR a scheduled trigger OR both." Cross-reference the new signal `SIG-OVERWATCH-STALENESS-PATTERN-2026-05-20.md` (Brien is authoring this in the seed session that produced this prompt).

DoD for Phase 5.5: staleness banner verified to fire on next SessionStart; scheduled task entry created OR documented as gap; HANDOFF-2026-04-15 items closed inline (with their write-through hooks installed, not just one-shot-script'd); drift-catalog updated.

### Phase 6 — Continuous push discipline

You do NOT batch pushes to end-of-run. Push each repo's commits as substantive units complete:
- Cast (`theparlor/persona-engine`)
- Voices (`theparlor/voices`)
- Forge (verify remote first; likely `theparlor/forge` or `theparlor/skills-engine`)
- Intent framework (`theparlor/intent`)
- Workspaces governance (`theparlor/workspaces-governance`)
- Other product repos: `git remote -v` to discover; push to origin/main or topic branches as appropriate

Push is L4 in `theparlor/*` per CLAUDE.md. Never force-push main. Never amend pushed.

---

## Token budget guidance

You have ~55% of weekly All Models budget + ~10 hours wall-clock. Burn discipline:
- **Spend Opus on synthesis** — Phase 5 ecosystem-level work; cross-product architecture decisions; deep IDD-pattern audits where Sonnet would miss subtle drift
- **Spend Sonnet on per-product work** — Phase 1 audits, Phase 2 execution, Phase 3 doc refreshes, Phase 4 marketing copy
- **Burn the headroom** — Brien explicitly said "it would be a crime to leave those tokens on the table." If you're under-utilizing budget at hour 5, INCREASE the dispatch fanout: launch waves of 10-12 parallel agents on the products/frameworks that still have phases pending.
- **Don't burn on ceremony** — no PR-style review docs; no "for Brien's review" framing; no decision atoms with non-ratified status defaults.
- **DO burn on substance** — deep audits that catch latent drift; comprehensive doc refreshes; marketing narratives that cite Brien's masters accurately; cross-product synthesis.

---

## Reply format constraint (when Brien wakes up)

When Brien returns to the session, your final report must be UNDER 1800 WORDS and include:

1. **Top of report — single-sentence verdict** (e.g., "Overwatch run + all 33 products/frameworks audited; 28 had L4 upgrades executed; 5 had no gaps; ecosystem-architecture refresh landed at `~/Workspaces/Core/ECOSYSTEM-*.md`; overwatch staleness hook installed.")
2. **Overwatch summary** (Phase 0.5) — total findings by bucket (INLINE-FIXABLE / WRITE-THROUGH-FAILURE / PRODUCT-LEVEL UPGRADE / STRUCTURAL GAP); how many closed inline vs deferred to per-product work; journal path
3. **Per-phase summary** (Phases 1-5, one short paragraph each, commit ranges)
4. **Phase 5.5 (Overwatch Rehabilitation) status** — staleness banner installed? scheduled task created? HANDOFF-2026-04-15 items closed? drift-catalog updated?
5. **Total commits + pushes** (count, repos touched)
6. **Drift findings** (any new drift patterns discovered; what was corrected inline; any genuine L0 items surfaced)
7. **Token budget consumed** (rough %; if you didn't burn ≥40% of available, explain why)
8. **The single critical decision surface (if any)** — the ONE item that genuinely needs Brien's attention. NOT a list of 10. NOT "want me to..." framing. The one (if any) genuine L0 gate that arose.
9. **What's now possible that wasn't 12 hours ago** — concrete capabilities unlocked

NO QUESTIONS. NO PROPOSALS. NO "want me to". Brien wakes to landed work.

---

## Honest framing — call this out at the top of your final report

- This run was framed by the artificial-gate-drift lesson (SIG-ARTIFICIAL-GATE-DRIFT-PATTERN-2026-05-20). You actively avoided introducing L0 gates throughout.
- Per-product upgrade plans are PLANS, not unilateral execution decisions; where a plan item depended on Brien's editorial judgment (e.g., naming things, brand voice choices, strategic positioning), it was framed as L4 with algorithmic-ground-truth-or-explicit-input-needed flagged, not L0-blocking.
- The IDD pattern was applied as a *discipline*, not as a *prescriptive recipe*. Where products don't have IDD loops yet (Fieldbook, several frameworks), Notice signals were opened to start their IDD anchors — but no implementation was forced where 4-gate failed on "no info gap."

---

## Cross-references

- Playbook: `~/Workspaces/Core/frameworks/intent/playbooks/idd-build-pattern.md`
- Applicability matrix: `~/Workspaces/Core/frameworks/intent/playbooks/cross-product-applicability.md`
- Drift catalog: `~/Workspaces/Core/frameworks/intent/learnings/process-drift-catalog.md`
- New drift pattern (artificial-gate): `~/Workspaces/Core/frameworks/intent/.intent/signals/SIG-ARTIFICIAL-GATE-DRIFT-PATTERN-2026-05-20.md`
- Subagent template: `~/Workspaces/Core/frameworks/intent/knowledge-engine/templates/subagent-dispatch-prompt.md`
- Decision-atom template: `~/Workspaces/Core/frameworks/intent/knowledge-engine/templates/decision-atom.md`
- Spawn-prompt siblings: `~/Workspaces/Core/frameworks/intent/spawn-prompts/`
- Brien CLAUDE.md (autonomy + projects): `~/.claude/CLAUDE.md`
- Hooks: `~/Workspaces/Core/frameworks/intent/hooks/` (7 hooks; all auto-fire)

---

# EXECUTE

Begin Phase 0 immediately. Dispatch waves continuously. Push as substantive units land. Burn the budget.
