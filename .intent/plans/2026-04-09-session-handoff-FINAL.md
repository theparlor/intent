# Session Handoff — 2026-04-09 Final State

> Written at end-of-session when Claude Desktop started showing UI instability. All work below is committed and pushed to git. This file is the single entry point for the next session (Sunday or later).

## Read this first in the next session

1. **This file**
2. `./2026-04-09-s0-status-report.md` (earlier status from mid-session)
3. `./2026-04-09-post-panel-plan.md` (the compressed S0/S1/S2 plan)
4. `../decisions/DEC-20260409-01-panel-review-response.md`
5. `../decisions/DEC-20260409-02-open-questions-answered.md`
6. `/Users/brien/Workspaces/Core/personas/operators/brien.yaml` (the brien-operator persona for self-prompt continuity)

## Three repos, all pushed, all clean

| Repo | Last commit | State |
|------|-------------|-------|
| `theparlor/intent` | `a0dd7d7` SIG-054 + `6e1c117` S0 batch 1 | Clean, pushed |
| `theparlor/intent-site` | `dcc2a00` logo fix | Clean, pushed, GitHub Pages deployed |
| `theparlor/skills-engine` | `165037f` panel-review skill v0.1 scaffold | Clean, pushed |

## Everything shipped in the 2026-04-09 session

### Intent product repo (theparlor/intent)

**Signals captured (SIG-041 through SIG-054 — 14 new):**
- SIG-041: Panel-as-async-feedback-loop is the genuine breakthrough
- SIG-042: No target user (6/8 panels)
- SIG-043: Discovery theater — N=1 external voice (4/8)
- SIG-044: Category confusion — 6 framings across 6 pages
- SIG-045: Reader never the hero
- SIG-046: Methodology lineage unacknowledged
- SIG-047: Hypothesis framing missing
- SIG-048: Operator self-persona gap
- SIG-049: Psychological safety never addressed (critical, 1/8 panels)
- SIG-050: Double-loop asserted but not architected
- SIG-051: Architecture hardening backlog (P0/P1/P2 consolidated)
- SIG-052: Subtract-before-build reflex (Brien meta-pattern)
- SIG-053: Measurability + visibility as infrastructure prerequisite
- SIG-054: Panel-review needs first-click-simulation pass

**Intents (INT-007 through INT-013):**
- INT-007: Ship panel-review as first-class skill (the primitive) — v2 updated with foundational panel presets
- INT-008: Ruthless subtraction pass (accepted, target user committed)
- INT-009: Architecture hardening backlog
- INT-010: 10 external discovery interviews (Mom Test protocol)
- INT-011: Operator persona type + brien-operator first instance (governance: agent-proposed-with-panel-review)
- INT-012: Content rebuild with hypothesis framing + named attribution
- INT-013: Safety + change workstream (combined, interdependent)

**Decision records:**
- DEC-20260409-01: Post-panel review response (accept Brien's instincts, reject two-site split, add missed findings)
- DEC-20260409-02: Brien's 5 open-question answers (target user committed, discovery participants seeded, persona governance set, two-site cancelled, trust score stance + infrastructure prerequisites, Edmondson thread open)

**Psychological safety methodology:**
- `methodology/psychological-safety/01-edmondson-four-dimensions-analysis.md` — research foundation
- `methodology/psychological-safety/02-safety-contract-v1.md` — 10 promises, Promise 11 (Edmondson "more" thread) open
- `methodology/psychological-safety/03-change-management-analysis.md` — Bridges + Kotter applied

**Discovery wave 1 scaffold:**
- `discovery/wave-1/01-interview-protocol.md` — Mom Test, 5-act format
- `discovery/wave-1/02-external-signal-template.md`
- `discovery/wave-1/03-participant-profile.md` — Seed list (Chris Markus, Ari Amari, Devin, Zak + 6 TBD + 5 Tier 3 cold TBD)
- `discovery/wave-1/04-outreach-template.md`
- `discovery/wave-1/05-synthesis-template.md`
- `discovery/wave-1/06-opportunity-tree-template.md`
- `signals/external/README.md`

**Plans:**
- `plans/2026-04-09-post-panel-plan.md` — compressed S0/S1/S2 timeline
- `plans/2026-04-09-s0-status-report.md` — mid-session status
- `plans/2026-04-09-session-handoff-FINAL.md` — THIS FILE

### Intent-site repo (theparlor/intent-site)

**Archival:**
- `docs/archive/v1.2-multi-framing/` — 23-page snapshot of pre-rebuild site with ARCHIVE.md explaining rationale

**v2-draft — 10 new pages in `docs/v2-draft/`:**
1. `pitch.html` — The Hypothesis hero with committed target user ("Staff+ engineers on teams of 2–7 using Claude Code daily"), hypothesis framing, tablestakes/evolutionary/open-question maturity columns, named methodology attribution, honest exclusions callout, **full-width elliptical hero SVG** with four phase nodes + prominent INTENT center in matching ellipse
2. `ending.html` — What Intent asks you to release (Bridges phase 1)
3. `neutral-zone.html` — Weeks 3–8 adoption playbook with 7 scaffolds (Bridges phase 2)
4. `who-loses.html` — Power shift grid + 5 role deep-dives
5. `when-not.html` — Infrastructure + cultural + team-shape exclusions, 8-question self-assessment checklist
6. `lineage.html` — Full methodology ancestor attribution graph (Torres, Patton, Cagan, Boyd, Deming, Ries, Argyris, Edmondson, Gilad, Dunford, Kahneman, Meadows, Bridges, Kotter, Aakash Gupta, et al.)
7. `the-system.html` — Zone 2 landing with inline loop SVG + deeper links to v1.2 content
8. `the-build.html` — Zone 3 landing with three-layer diagram + hardening backlog + deeper links
9. `the-proof.html` — Zone 4 landing with evidence ledger, discovery wave progress, 4 falsification criteria

**Framing banner on 23 legacy pages** — applied via 5 parallel agent teams. Every v1.2 page now shows:
> ⚠ Active hypothesis · v1.2 content. This page describes current architecture work-in-progress in shipped-product voice. [See the hypothesis framing →]

Pages with banner: pitch, concept-brief, methodology, walkthrough, roadmap, work-system, flow-diagram, system-diagram, schemas, signals, personas, dogfood, observe, event-catalog, getting-started, architecture, agents, deployment, observability, arb, decisions, native-repos, products.

**Nav structure in v2-draft:** 4-zone progressive depth (Hypothesis / System / Build / Proof). Logo link points to `pitch.html` (NOT `../index.html`) so readers stay within v2 narrative.

### Persona updates (Core/personas/ — not git-tracked, this is a meta-signal)

- `registry/april-dunford.yaml` — promoted to foundational tier
- `registry/itamar-gilad.yaml` — promoted secondary → foundational
- `registry/aakash-gupta.yaml` — NEW foundational persona (draft lifecycle, needs corpus expansion)
- `operators/brien.yaml` — NEW first operator persona (v0.1, captures 4 known failure modes including "build-more reflex")

**Meta-signal:** `Core/personas/` is not a git repo, so these changes have no commit history. Should be addressed in S1.

### Skills Engine (theparlor/skills-engine)

- `platforms/claude-code/meta/panel-review/SKILL.md` — v0.1 scaffold for the async feedback primitive with 6 preset panels (full-foundational, content-review, architecture-review, safety-review, decision-review, operator-review), 3 always-on voices (Edmondson, Dunford, Kahneman), safety contract integration per INT-013

## Live URLs

- **v2-draft pitch (hero with SVG):** https://theparlor.github.io/intent-site/v2-draft/pitch.html
- **v2-draft The Build:** https://theparlor.github.io/intent-site/v2-draft/the-build.html
- **v2-draft The System:** https://theparlor.github.io/intent-site/v2-draft/the-system.html
- **v2-draft The Proof:** https://theparlor.github.io/intent-site/v2-draft/the-proof.html
- **Review that prompted the rebuild:** https://theparlor.github.io/intent-site/review-2026-04-09.html
- **v1.2 legacy (banner applied):** https://theparlor.github.io/intent-site/pitch.html and all others

## Open threads when session resumes

### Decisions needed from Brien

1. **Safety Contract Promise 11** — the "Edmondson more" thread. Reversibility alone doesn't address interpersonal social cost. Needs exploration session to name the missing dimension.
2. **Discovery participant backfill** — Devin and Zak last names, 6 more Tier 1 warm contacts, ~5 Tier 3 cold contacts (the protocol requires Tier 3 or it's an echo chamber)
3. **Trust score `used_for` enforcement mechanism** — Promise 1 says trust scores aren't used for performance reviews but there's no technical enforcement path. Needs design thinking.
4. **Personas repo governance** — Core/personas/ should probably become a git repo (or join an existing one) so changes have history. Flagged as meta-signal in SIG-054 period.
5. **Wider content max-width question** — Brien noted v2 content at 860px collapses narrower than hero. Whether to expand other pages to 1100-1200px is fully cosmetic, not blocking.

### Work ready to execute Monday (S1)

- Send first 4 outreach messages using templates in `.intent/discovery/wave-1/04-outreach-template.md` (Chris Markus, Ari Amari, Devin, Zak)
- Architecture P0:
  - SIG-022 ULID migration (sequential ID collision fix)
  - events.jsonl persistence (move from in-memory to SQLite+WAL)
  - Cross-engagement leak test in CI
- Architecture P1:
  - Runbooks + SLOs per MCP server
  - 4-server topology spike (decision only, not commit)
- Panel-review skill v0.1 → v1.0 (implementation, not just scaffold)
- Re-run panel review on v2-draft rebuild and measure F1/F3/F4/F10 drop vs baseline

### Work deferred to S2 (week of 4/20)

- 10 discovery interview synthesis → THM-external-discovery-wave-1 + DOM-spec-pain-OST
- Safety Contract v2 (resolve Edmondson more, draft Promise 11)
- Change management rollout playbook (Kotter 8-step concretized)
- Trust score + event schema updates for safety fields (used_for, visibility, failure_type)
- Second panel review on Safety Contract and Change docs
- Next discovery wave planning

## Final image generation result

After testing Midjourney, Gemini, ChatGPT/DALL-E, and Ideogram, the verdict: **DALL-E 3 won decisively for technical diagram hero visuals** — structure, text rendering, instruction following all best-in-class. Midjourney was worst (too atmospheric). Ideogram inconsistent. Gemini second place.

For pitch.html, the decision was to ship the inline SVG (animated, accessible, design-system-exact) rather than a raster image. The SVG went through three iterations:
1. Initial 960×540 viewBox with circular loop
2. 1600×540 full-width ellipse (Brien directed: flatter, wider, labels inline-left/right)
3. Label overlap fix + matching INTENT ellipse (Brien directed: labels sitting on arcs, INTENT understated)

Final state is the inline SVG in `v2-draft/pitch.html` — full-width elliptical loop, labels shifted above/below arcs for clearance, INTENT in matching-aspect-ratio ellipse with pulsing animation.

## The brien-operator persona captures today's patterns

The first operator persona (at `Core/personas/operators/brien.yaml`) explicitly captures 4 known failure modes observed during this session:
1. Build-more reflex when panels say subtract-more (SIG-052)
2. Split-the-surface-area reflex (two-site instinct)
3. Under-acknowledging psychological dimension
4. Over-confident synthesis when lineage unnamed

Each has a corrective prompt. Next session, if brien-operator is loaded into context, these corrections can self-prompt during similar patterns.

## Session continuity recommendation

When the next session starts:

1. **Read this file first.**
2. Load `Core/personas/operators/brien.yaml` into context for self-prompt continuity.
3. Check for uncommitted changes: `cd ~/Workspaces/Core/frameworks/intent && git status`, same for intent-site and skills-engine.
4. If everything is clean, proceed with Monday's S1 work: outreach + architecture P0 + panel-review skill v1.0.

## Everything is safe

All work is in git. All pushes are complete. The three repos are clean. The session UI showing weirdness is cosmetic — the actual state of the work is solid. No rush to recover, no data at risk.

Welcome back.
