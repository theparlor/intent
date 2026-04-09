# Post-Panel Plan — 2026-04-09 (v2: compressed)

> Redeveloped plan of pursuit after the 8-panel site review, compressed per Brien's "reach farther faster" instruction (2026-04-09 afternoon). See DEC-20260409-01 and DEC-20260409-02 for decision records and SIG-041 through SIG-053 for the signal chain.

## Compressed timeline — S0/S1/S2 sprints instead of 3 weeks

Brien's availability: off Claude Code from tonight at 5pm through Sunday. Budget for this session is higher than usual. The original 3-week plan is compressed into front-loaded sprints:

### S0 — TODAY (through ~5pm, 2026-04-09)

Brien is still present this afternoon. Maximize S0 so Brien returns Sunday to reviewable drafts, not a task list.

- Site archive (DONE — committed 64760f0)
- 12 signals extracted (DONE — committed 873a24b)
- 6 intents (INT-007 through INT-012) (DONE)
- DEC-20260409-01 (DONE)
- DEC-20260409-02 (new — captures Brien's 5 answers)
- 13th signal SIG-053 (measurability prerequisite)
- INT-013 (safety + change workstream)
- Psychological Safety Contract v1 with 10 promises + Edmondson thread open
- Edmondson 4-dimensions analysis
- Change management analysis (Bridges + Kotter applied)
- Discovery interview protocol + participant profile with seed names + outreach templates + synthesis + OST templates
- Persona updates: Dunford to foundational, Gilad to foundational, Aakash Gupta added at foundational
- Updated plan (THIS DOCUMENT)
- **New pitch.html draft** with committed target user + hypothesis framing + lineage
- **New Ending, Neutral Zone, Who Loses, When-NOT-to-Adopt page drafts**
- **Operator persona v1** (brien-operator)
- **Panel-review skill scaffold** in skills-engine
- All updates committed in batches by end of session

**Brien returns Sunday to:** a complete reviewable rebuild, not a plan. Drafts of every new page, operator persona, skill scaffold, safety contract, and all Intent-native artifacts tracking the work.

### S1 — Monday 4/13 → Friday 4/17 (5 days)

- **Brien reviews S0 drafts** Sunday evening / Monday morning
- **Discovery interviews** — all 10 this week, not spread over 2. Follow the protocol. Target: complete by Friday.
- **P0 architecture:** SIG-022 ULID migration, events.jsonl persistence, cross-engagement leak test
- **P1 architecture:** runbooks + SLOs, 4-server topology spike (decision only)
- **Site publish v2** — Friday target, after panel re-review passes
- **Panel re-review #1** — the rebuilt site goes through the 8-panel dispatch again; measure if findings F1-F10 dropped
- **Operator persona v1 finalized** with panel-review governance loop demonstrated

### S2 — Monday 4/20 → Friday 4/24 (5 days)

- **Discovery synthesis** — write THM-external-discovery-wave-1 and DOM-spec-pain-OST
- **Safety Contract v2** — resolve the "Edmondson more" thread with Brien; Promise 11 drafted or explicitly deferred
- **Change management rollout playbook** — Kotter 8-step with week-by-week adoption milestones, guiding coalition template, new-hire onboarding guide
- **Trust score + signal + event schema updates** for safety fields (used_for, visibility, failure_type)
- **Panel re-review #2** — Safety Contract and Change docs go through the safety panel
- **Next wave planning** — what does discovery wave 2 target?

### Quarter ambition (compressed from 12 weeks to 6 weeks)

Sprints S0 through S5 cover 6 weeks. After S2 (safety + change), S3-S5 cover:
- **S3 (4/27 → 5/1):** First pilot engagement — apply Intent + Safety Contract to a real adopter who passes the prerequisite checklist
- **S4 (5/4 → 5/8):** Measurement — DORA metrics, signal quality metrics, safety contract compliance metrics
- **S5 (5/11 → 5/15):** Discovery wave 2 + next iteration based on pilot findings

## One-line summary (unchanged)

**Subtract first, discover second, rebuild third, harden in parallel — with panel-review becoming a first-class primitive that gets called after every cycle.**

Plus (v2): **reach farther faster by front-loading S0 while Brien is still present today.**

## The three big decisions (plus two new ones)

1. **One site, not two.** Ratified unconditionally in DEC-20260409-02. Two-site split is dead.
2. **Subtract before build.** Front-loaded into S0. By end of today, the subtraction is done AND the rebuild drafts exist. This is not build-before-subtract; it's subtract-and-rebuild-same-session because the budget permits.
3. **Panel-review becomes the primitive.** Shipping as a skill in S0 (scaffold) and S1 (operational).
4. **NEW: Target user committed.** Staff+ engineers on teams of 2–7 using Claude Code daily. Sweet spot 2–5. Reaches 1–7. Over 7 is out of scope.
5. **NEW: Infrastructure prerequisites are hard constraints.** Blue-green / feature flags / automated testing / visible measurement are required for safe adoption. Without them, Intent cannot generate valid signals.

## One-line summary

**Subtract first, discover second, rebuild third, harden in parallel — with panel-review becoming a first-class primitive that gets called after every cycle.**

## The three big decisions

1. **One site, not two.** Brien's two-site instinct is overridden. The panels' #1 finding was "no target user" — splitting compounds that. The fix is one site with progressive depth.
2. **Subtract before build.** Brien's instinct to "build new material in as many repos as needed" is deferred one week. The subtraction pass must complete first. This is SIG-052 (the "build-more reflex" pattern) and its corrective.
3. **Panel-review becomes the primitive.** The biggest win from this session wasn't a critique — it was the realization that panel-dispatch IS the product. Agents call it after every cycle. Shipping it as a skill is the highest-leverage move.

## The three-week rollout

### Week 1 (2026-04-09 → 2026-04-16): Subtract + Primitive + P0 Architecture

**Parallel tracks. Nothing new is built until subtraction is done.**

#### Track A: Site subtraction (INT-008)

- [ ] Archive current intent-site content to `/archive/v1.2-multi-framing/` subfolder
- [ ] Preserve `review-2026-04-09.html` as the forcing-function artifact
- [ ] Delete 5 of 6 category framings across every remaining page
- [ ] Rewrite every "Intent does..." as "you will..."
- [ ] Remove multi-product framing from the hero
- [ ] Measure: 30% content reduction by end of week

#### Track B: Panel-review primitive (INT-007)

- [ ] Scaffold new skill at `Core/products/skills-engine/skills/claude-code/meta/panel-review/`
- [ ] Write SKILL.md with input/output contract
- [ ] Port the 8-panel dispatch pattern from this session as v1 preset
- [ ] Add "output signals as byproduct" capability
- [ ] Test on a non-site target (e.g., a spec file) to prove generality
- [ ] Document how any agent calls it during a cycle

#### Track C: Architecture P0 (INT-009)

In `theparlor/intent` product repo, NOT the site:
- [ ] Fix SIG-022 (sequential ID collision) — ULID migration
- [ ] Persistence spike for events.jsonl (SQLite+WAL proof-of-concept)
- [ ] Cross-engagement leak test in CI
- [ ] ADR for each P0 decision

#### Track D: Operator persona schema (INT-011)

- [ ] Add `operator` type to `Core/personas/registry/_schema.yaml`
- [ ] Draft `brien-operator` v1 from CLAUDE.md + memory/ + session journals
- [ ] Include SIG-052 (build-more reflex) as a known failure mode with corrective prompt
- [ ] Wire it into the panel-review primitive as one of the voices

### Week 2 (2026-04-16 → 2026-04-23): Discovery + Content Rebuild Draft

#### Track A: External discovery interviews (INT-010) — THE HIGHEST LEVERAGE MOVE

- [ ] Draft candidate list of 10 senior ICs/PMs using Claude Code daily
- [ ] Mom Test protocol prep — sharpen questions to avoid leading
- [ ] Schedule 10 interviews for the week
- [ ] Conduct interviews, capture verbatim quotes
- [ ] Write 10 signal files to `.intent/signals/external/`
- [ ] Target: 10 interviews complete by end of week

#### Track B: Content rebuild draft (INT-012, after subtraction complete)

- [ ] Draft new `pitch.html` with single target user + hypothesis framing
- [ ] Draft new `concept-brief.html` with tablestakes/evolutionary/open-question labels
- [ ] Draft new `lineage.html` crediting Torres/Patton/Cagan/Boyd/Deming/Ries/Argyris/Edmondson
- [ ] Draft `safety-contract.html` (psychological safety page)
- [ ] Wire named attribution throughout existing pages
- [ ] DRAFTS ONLY — not published until panel-review validates

#### Track C: Architecture P1 (INT-009)

- [ ] Runbooks + SLOs for each MCP server
- [ ] 4-server topology spike (decision doc, not code change)
- [ ] Deploy-phase event family specced

### Week 3 (2026-04-23 → 2026-04-30): Validate + Publish + Pressure-test

#### Track A: Re-run panel review

- [ ] Call panel-review primitive (now a skill) on the rebuilt drafts
- [ ] Measure: did F1 (no target user) drop below 3 panels? F3 (category confusion) below 2? F10 (psych safety) get addressed?
- [ ] If not, iterate before publishing
- [ ] If yes, merge drafts to main

#### Track B: Publish v2

- [ ] Push rebuilt site
- [ ] Verify progressive disclosure works (hero → story → substrate → proof)
- [ ] Wire cross-links between layers
- [ ] Announce nothing externally yet — wait for discovery synthesis

#### Track C: Discovery synthesis

- [ ] Write `knowledge/themes/THM-external-discovery-wave-1.md` from the 10 interviews
- [ ] Build opportunity tree: `knowledge/domain-models/DOM-spec-pain-OST.md`
- [ ] Identify 2-3 candidate pilot teams from the interviews
- [ ] Decide if the hypothesis-framed site matches what practitioners actually said

## Repos affected

| Repo | What changes | Why |
|------|--------------|-----|
| `theparlor/intent` (product) | Signals, intents, decisions, plan, ADRs, P0/P1 architecture work, panel-review skill draft | Source of truth for methodology + architecture |
| `theparlor/intent-site` | Subtraction pass, archival, rebuilt drafts, new pages (lineage, safety-contract), panel-review output page | Public site |
| `Core/products/skills-engine` | New `panel-review` skill in `skills/claude-code/meta/` | First-class primitive |
| `Core/personas` | New `operator` persona type + `brien-operator` first instance | Self-persona for self-directed cycles |
| `Core/personas/corpus/external-interviews/` (new) | 10 interview transcripts + signal derivations | Discovery evidence |

## What we are explicitly NOT doing

- **NOT splitting the site into two properties.** One site, progressive depth. Can revisit if progressive disclosure fails.
- **NOT building new pages before the subtraction pass completes.** Sequence matters.
- **NOT announcing externally until discovery synthesis is done.** Don't try to convince people of a hypothesis until we have evidence from people.
- **NOT shipping the 4-server MCP collapse this quarter.** Spike only — decide, don't commit yet.
- **NOT building operator personas for anyone but Brien in v1.** Prove the pattern first.

## How we know it worked

Re-run the panel review in week 3 against the rebuilt site. Compare findings:

| Finding | Week 1 baseline | Week 3 target |
|---------|-----------------|---------------|
| F1 — No target user | 6/8 panels | ≤1/8 |
| F2 — Discovery theater | 4/8 panels | ≤0/8 (10 external signals exist) |
| F3 — Category confusion | 5/8 panels | ≤1/8 |
| F4 — Reader not hero | 4/8 panels | ≤1/8 |
| F5 — Double-loop asserted | 3/8 panels | ≤1/8 (Challenge-the-Intent pass shipped) |
| F6 — Math replaces politics | 3/8 panels | ≤1/8 (weights publish their provenance) |
| F7 — 4-server unjustified | 2/8 panels | ADR decision documented |
| F8 — No runbooks/SLOs | 3/8 panels | Runbooks exist for each server |
| F9 — Lineage unacknowledged | 2/8 panels | 0/8 (lineage.html shipped) |
| F10 — Psych safety | 1/8 panels | 0/8 (safety-contract.html shipped) |

If the numbers don't drop, we have a double-loop problem — the decision itself is wrong and we need to reopen it.

## Panel review becomes the continuous signal

After week 3, panel-review runs are scheduled:
- After every major content change (catches regressions in positioning)
- After every architecture ADR (catches tradeoff blind spots)
- After every discovery synthesis (catches confirmation bias)
- After every engagement rollout decision (catches change-management gaps)

This is the genuine feedback loop Intent was supposed to have but didn't. The panels are the loop. The loop is the product.

## Open questions for Brien

1. **Target user sharpness:** "practitioner-architect" is close. Is it "staff+ engineers using Claude Code daily on 5-15 person teams"? Or something tighter? Need to commit before week 1 subtraction completes.

2. **Discovery interview participants:** Who are the 10? Brien's network has candidates but needs explicit list before week 2.

3. **Operator persona governance:** Who updates brien-operator over time? Manual only? Agent-proposed with human review? Frequency?

4. **Two-site exit criterion:** If the one-site progressive-disclosure approach fails at the week-3 panel review, at what point do we revisit the two-site split? Define the failure condition now so we don't argue about it later.

5. **Psych safety contract content:** Brien needs to weigh in on what trust scores are NOT used for. This is a policy statement, not a code change, and requires explicit stance-taking.
