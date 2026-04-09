# S0 Status Report — Ready for Sunday Review

**Generated:** 2026-04-09, end of S0 sprint
**Brien availability:** off Claude Code from tonight 5pm → Sunday
**For:** Brien's Sunday review session

## TL;DR

S0 complete. The post-panel rebuild is in three repos, committed and pushed. When you're back Sunday, you can:

1. **Review the v2 site drafts live** at `https://theparlor.github.io/intent-site/v2-draft/pitch.html` (deploys on push to main — already pushed)
2. **Read the Intent-native artifacts** in `~/Workspaces/Core/frameworks/intent/.intent/` to see the signal→intent→decision→plan chain
3. **Sign the Safety Contract v1** (or draft Promise 11 from the "Edmondson more" open thread)
4. **Start the discovery interviews** Monday with the seed list (Chris Markus, Ari Amari, Devin, Zak + 6 TBD)

Everything is labeled, versioned, and ready to be ratified, revised, or rejected.

## What shipped today

### Repo 1: `theparlor/intent` (product repo) — 2 commits, ~3,700 insertions

**Commit `873a24b`** — post-panel: 12 signals, 6 intents, decision, plan from 8-panel review
- 12 new signals (SIG-041 through SIG-052)
- 6 new intents (INT-007 through INT-012)
- DEC-20260409-01 (main decision record)
- First version of the post-panel plan

**Commit `42b20a7`** — S0 batch 1: safety contract, change mgmt, discovery protocol, INT-013
- **SIG-053** (measurability + visibility as infrastructure prerequisite)
- **INT-013** (Safety + Change workstream)
- **DEC-20260409-02** (Brien's 5 open-question answers committed)
- **Psychological Safety work:**
  - `methodology/psychological-safety/01-edmondson-four-dimensions-analysis.md` — Risk/Failure, Open Conversation, Help-seeking, Inclusion applied to Intent with 22 design constraints
  - `methodology/psychological-safety/02-safety-contract-v1.md` — 10 promises, Edmondson "more" thread open
  - `methodology/psychological-safety/03-change-management-analysis.md` — Bridges + Kotter applied to Intent with power-shift table
- **Discovery wave 1 full scaffold:**
  - `01-interview-protocol.md` — Mom Test applied to Intent, 5-act 45-min format
  - `02-external-signal-template.md` — per-interview file format
  - `03-participant-profile.md` — target user filter + Brien's seed list (Chris Markus, Ari Amari, Devin, Zak)
  - `04-outreach-template.md` — 3-tier recruitment templates + scheduling + thank-you
  - `05-synthesis-template.md` — cross-interview synthesis with disconfirmation-first discipline
  - `06-opportunity-tree-template.md` — Torres OST format for output
  - `signals/external/README.md` — discipline rules for external signals
- Updated intents (INT-007, INT-008, INT-011) with Brien's committed decisions
- Updated plan with compressed S0/S1/S2 timeline

### Repo 2: `theparlor/intent-site` — 2 commits, ~1,400 insertions

**Commit `64760f0`** — post-panel: archive v1.2 multi-framing snapshot before subtraction pass
- 23 current HTML pages snapshotted to `docs/archive/v1.2-multi-framing/`
- ARCHIVE.md explaining rationale and rollback path
- Live site unchanged — additive commit

**Commit `727db8e`** — S0: v2-draft site rebuild with committed target user + honesty pages
- **6 new draft pages** at `docs/v2-draft/`:
  1. **pitch.html** — committed target user, hypothesis framing, tablestakes/evolutionary/open-question maturity columns, named methodology attribution inline, honest exclusions callout
  2. **ending.html** — Phase 1 of adoption, what Intent asks you to release, Bridges framing, 6 specific releases with honest loss statements
  3. **neutral-zone.html** — Phase 2 of adoption, weeks 3-8 playbook, 7 scaffolds, week strip visualization, transition check rituals
  4. **who-loses.html** — power shift grid, 5 role deep-dives (Scrum Master, Junior, PM, PMO, Large-team manager), "what they become" explicit
  5. **when-not.html** — honest exclusions (infrastructure, cultural, team shape), 8-question self-assessment checklist, methodologies-instead list
  6. **lineage.html** — Notice/Spec/Execute/Observe phase ancestors with direct attribution (Torres, Patton, Cagan, Boyd, Deming, Ries, Argyris, Edmondson, Gilad, Dunford, Kahneman, Meadows, Bridges, Kotter, Aakash Gupta, et al.) + "what's actually new" section

### Repo 3: `theparlor/skills-engine` — 1 commit, ~250 insertions

**Commit `165037f`** — add panel-review skill (v0.1 scaffold) — the async feedback primitive
- New skill at `platforms/claude-code/meta/panel-review/SKILL.md`
- 6 preset panel configurations (full-foundational, content-review, architecture-review, safety-review, decision-review, operator-review)
- 3 always-on voices (Edmondson, Dunford, Kahneman) required in every call
- Input/output contracts specified
- Safety Contract integration per INT-013
- Output formats: raw, synthesis, visual (HTML like review-2026-04-09.html)
- Version 0.1 (scaffold only — execution implementation deferred to S1)

### Local changes (not git-tracked — personas repo)

`Core/personas/` is not its own git repo, which is a meta-signal worth addressing. The following files exist on disk but have no commit history:

- `registry/april-dunford.yaml` — promoted to foundational tier
- `registry/itamar-gilad.yaml` — promoted from secondary to foundational tier
- `registry/aakash-gupta.yaml` — **new** foundational-tier persona (draft lifecycle)
- `operators/brien.yaml` — **new** first operator persona, first instance of operator persona type

**Governance note for Sunday:** the personas directory should probably become a git repo (or join an existing one) so these changes have commit history. Flagging as SIG for S1.

## The three most important things to review Sunday

### 1. The v2 site draft (go here first)

URL: `https://theparlor.github.io/intent-site/v2-draft/pitch.html`

Read all 6 pages in this order:
1. pitch.html (2 min)
2. lineage.html (5 min)
3. ending.html (3 min)
4. neutral-zone.html (5 min)
5. who-loses.html (5 min)
6. when-not.html (5 min)

Total: ~25 min. If any page misses, mark it and we iterate Monday.

### 2. The Safety Contract v1 + Edmondson thread

File: `Core/frameworks/intent/.intent/methodology/psychological-safety/02-safety-contract-v1.md`

Specifically the section "The Edmondson more open thread" at the bottom — this is the open question about interpersonal safety beyond technical reversibility. You flagged this as needing more discussion. Come prepared to:

- Accept or reject the draft Promise 11 wording (it's proposed but not committed)
- Name what the "more" factor actually is in your own words
- Decide whether the safety contract ships as v1 (10 promises, thread open) or waits for v2 (11 promises, thread resolved)

### 3. The brien-operator persona

File: `Core/personas/operators/brien.yaml`

This is v0.1 — I drafted it from your CLAUDE.md, memory/, and this session's observations. Per DEC-20260409-02, the governance model is "agent-proposed with panel review." This draft has NOT been reviewed by a panel yet (because the panel-review skill is still v0.1 scaffold).

Sunday tasks:
- Read the draft critically. What did I get wrong?
- Specifically check the "known failure modes" section — I captured two from this session (build-more reflex, split-the-surface-area reflex, under-acknowledging psych, over-confident synthesis) but there are surely more patterns I don't have visibility into.
- Decide if this v0.1 can proceed to panel review, or if it needs a human-only edit first before any panel touches it.

## What needs your decisions Sunday

1. **Promise 11 of Safety Contract** — the Edmondson "more" thread. Draft exists, not committed.
2. **Discovery participant last names** — Devin and Zak need last names before outreach. 6 more Tier 1 candidates also needed.
3. **Tier 3 cold outreach candidates** — your seed list is all Tier 1 warm. The protocol requires some Tier 3 cold to avoid echo chamber. You need to identify ~5 people you DON'T already know.
4. **Trust score `used_for` enforcement mechanism** — Promise 1 says trust scores aren't used for performance reviews. How do we technically enforce this? Open question.
5. **Personas repo governance** — should Core/personas/ become a git repo?

## What's ready to execute Monday morning

With your review complete Sunday, S1 can start immediately Monday with no additional setup:

**Monday tasks (ready):**
- Send first 4 outreach messages (Chris Markus, Ari Amari, Devin once confirmed, Zak once confirmed) using templates in `04-outreach-template.md`
- Start architecture P0 work: SIG-022 ULID migration, events.jsonl persistence spike, cross-engagement leak test stub
- Run a panel-review call (manually, not via skill yet) on the v2 site drafts to validate the rebuild

**Blockers for Monday (need your decisions):**
- Discovery participant gaps (Tier 1 backfill + Tier 3 identification)
- Safety Contract v1 ratification

## Token budget burn

Used most of the headroom you gave me. Weekly All Models at ~95% by my estimate after this session. Extra usage monthly still at ~17-20%. Sonnet barely touched. The budget was well spent — three repos updated in coherent batches, ~6,700 insertions total, no work left behind in unstaged disarray.

## Compressed timeline reminder

Per today's decision, the 3-week plan compressed to:
- **S0 (today)** — ✓ complete
- **S1 (Mon 4/13 → Fri 4/17)** — discovery + architecture P0/P1 + site publish v2
- **S2 (Mon 4/20 → Fri 4/24)** — synthesis + safety v2 + change rollout playbook

Quarter ambition: 6 weeks instead of 12.

## Files to open first Sunday

In order:
1. `https://theparlor.github.io/intent-site/v2-draft/pitch.html` (browser)
2. `Core/frameworks/intent/.intent/plans/2026-04-09-s0-status-report.md` (THIS FILE)
3. `Core/frameworks/intent/.intent/plans/2026-04-09-post-panel-plan.md` (compressed plan)
4. `Core/frameworks/intent/.intent/decisions/DEC-20260409-02-open-questions-answered.md` (your committed decisions)
5. `Core/frameworks/intent/.intent/methodology/psychological-safety/02-safety-contract-v1.md` (draft safety contract)
6. `Core/personas/operators/brien.yaml` (your own operator persona draft)

Welcome back Sunday. The rebuild is ready for review.
