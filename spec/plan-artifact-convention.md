---
title: Plan Artifact Convention + Pre-Product Intake Holding Pen
id: SPEC-PLAN-001
type: spec
maturity: draft
created: 2026-04-23
updated: 2026-04-23
supersedes:
  - docs/superpowers/plans/ (default from writing-plans skill — overridden by this convention for Workspaces-resident products)
depth_score: 4
depth_signals:
  file_size_kb: 34.6
  content_chars: 18322
  entity_count: 0
  slide_count: 0
  sheet_count: 0
  topic_count: 0
  has_summary: 0
vocab_density: 0.05
kind: governance
status: draft
author: brien
attribution:
  concept: Brien Tate (2026-04-23)
  context: Coherence gap observed during Throughline scaffold planning; plans have no canonical home
intent_beat: Notice→Spec — this spec is the Spec beat; ratification closes the Execute beat
pilot_target: Core/products/throughline/
ratification_gate: Throughline first plan executed + one _intake/ disposition exercised
related_ddrs:
  - WS-DDR-075 (filed 2026-05-09 — see Workspaces/.context/DECISIONS.md; supersedes the 061 stub which collided with pre-existing 061 entries — see SIG-DDR-061-COLLISION-2026-05-09)
  - WS-DDR-026 (engine/farm/outputs convention — plans/ is parallel to spec/)
  - WS-DDR-016 (Core/ three-way disambiguation — plans/ is Core-product-scoped reusable IP)
  - WS-DDR-025 (sibling-over-parent-child — _intake/ is sibling to products/, not nested under any one product)
related_specs:
  - Core/frameworks/intent/spec/signal-stream.md
  - Core/frameworks/intent/spec/spec-shaping-protocol.md
  - Core/frameworks/intent/spec/signal-capture-system.md
related_signals:
  - SIG-PLAN-001 (plans have no canonical home — this spec resolves it; signal pending creation)
skill_binding: "superpowers:writing-plans (persistence target — see §4)"
---
# SPEC-PLAN-001 — Plan Artifact Convention + Pre-Product Intake Holding Pen

> **Status: DRAFT.** Ratification path in §6. Pilot on Throughline (§5).
> This spec is the Spec beat of the Intent cycle for the plan-artifact governance initiative.

---

## Section 1 — Problem

Implementation plans in Brien's Workspaces have no canonical home. Claude Code's plan mode (EnterPlanMode/ExitPlanMode) is ephemeral by design — plans vanish with the session unless manually saved. The `superpowers:writing-plans` skill defaults to `docs/superpowers/plans/`, a path that sits outside the Workspaces organizational system and is therefore invisible to the placement resolver, the library index, the freshness scanner, and the signal stream. Separately, pre-product ideation — the period between "this might be worth building" and "this has a scaffold" — has no home at all. Today it drifts across journal entries, ad-hoc directories, and conversation history, none of which are discoverable, attributable, or governed. The result is two coherence gaps: (1) the *how* and *when* of execution is not preserved alongside the *what* and *why* (which live in specs), and (2) pre-product concepts cannot be audited, promoted, or killed cleanly. This spec closes both gaps with a convention that is parallel to the existing `spec/` pattern, findable by all existing governance machinery, and consistent with WS-DDR-025 (sibling-over-parent-child), WS-DDR-026 (engine/farm/outputs tri-layer), and AGENTS.md's hard gates.

---

## Section 2 — Directory Convention

### 2.1 Plans in Existing Products

**Canonical path:**

```
Core/products/[name]/plans/YYYY-MM-DD-<topic>-plan.md
```

Plans are siblings to `spec/`, not children of it. A spec answers *what* and *why*. A plan answers *how* and *when* (the sequence of concrete actions to execute the spec). Plans are authoritative artifacts — not session-local notes, not ephemeral worktree scratch — and must be created, versioned, and retired with the same discipline as specs.

#### 2.1.1 Required Frontmatter Fields

```yaml
---
title: "[Topic] Implementation Plan"
id: PLAN-[PRODUCT]-NNN               # e.g. PLAN-THROUGHLINE-001
kind: plan
status: draft | accepted | executing | completed | abandoned | deferred
established: YYYY-MM-DD
updated: YYYY-MM-DD
author: brien
source_spec: Core/products/[name]/spec/YYYY-MM-DD-[spec-file].md
# ^^^ REQUIRED — plans must point at a spec. A plan without a source spec is a signal of a missing spec.
# [DECISION: if no spec exists yet, write "TBD — spec pending" and emit SIG-PLAN-NO-SPEC; do not skip the field]
dor_refs:                            # Definition of Ready refs (from dor-dod-library.md)
  - DOR-PLN-001
dod_refs:                            # Definition of Done refs
  - DOD-PLN-001
supersedes: []                       # List of plan IDs this replaces, if any
related_signals:
  - SIG-[ID]                         # Signals that motivated this plan
related_ddrs:
  - WS-DDR-NNN                       # Governance decisions that constrain this plan
---
```

**Status lifecycle:**

| Status | Meaning |
|--------|---------|
| `draft` | Plan is being written or has not been reviewed |
| `accepted` | Plan reviewed; execution authorized |
| `executing` | Active — tasks are being worked |
| `completed` | All DoD criteria met; execution closed |
| `abandoned` | Stopped before completion; reason in plan body |
| `deferred` | Not executing now; explicit review-date in plan body |

#### 2.1.2 Required Sections

Every plan must contain these sections in order:

```markdown
## Goal
One sentence. What does completing this plan produce?

## Scope
What is in. Bullet list of systems/artifacts/behaviors this plan addresses.

## Non-Goals
Explicit callouts of what this plan does NOT address — reduces scope-creep drift.

## Dependencies
- Other plans that must complete first (with plan IDs)
- External systems or approvals needed
- Signals whose resolution is prerequisite

## Tasks
[See granularity guidance below]

## Success Criteria / DoD
Observable, checkable conditions. Maps to dod_refs in frontmatter.
- [ ] Criterion 1
- [ ] Criterion 2

## Risks
| Risk | Likelihood | Impact | Mitigation |
|------|-----------|--------|------------|
| ... | ... | ... | ... |

## Rollback
How to undo this plan's changes if execution goes wrong. Required for any plan that
modifies files outside a single product's directory.

## Handoff
What the next session or agent needs to know to pick this up mid-execution.
What signals to emit when plan completes (or is abandoned).
```

#### 2.1.3 Task Granularity Guidance

Tasks must be **bite-sized** — each task is one atomic action (create a file, write a schema, run a test, emit a signal). Do not write tasks that span multiple concerns. Prefer 15–25 tasks over 5 large ones. Each task uses checkbox syntax (`- [ ]`) so progress is trackable. File paths in tasks are always absolute.

Tasks that modify more than three files should be decomposed. Tasks that span multiple sessions should include a Handoff note.

#### 2.1.4 Filename Convention

```
YYYY-MM-DD-<kebab-case-topic>-plan.md
```

- Date prefix: the date the plan was established (not started, not completed)
- Topic: matches the spec topic where applicable; if a plan covers a subset of a spec, the topic narrows (e.g. `2026-04-23-vision-thread-schema-plan.md` for a plan implementing only the schema portion of Throughline's spec)
- No version numbers in filenames — use the `supersedes` field and new plan files for revisions

#### 2.1.5 Relationship to spec/

```
spec/  ─── what to build and why        (source of truth for intent)
           │
           └──► plans/ ─── how and when (execution blueprint; traces back to spec)
                           │
                           └──► execution ─── tasks run; commits made; signals emitted
                                              │
                                              └──► observe-artifacts (journal, post-execute signals, retro)
```

A plan MUST have a `source_spec` reference. A spec MAY have zero, one, or many plans (one plan per execution phase is the recommended pattern for complex specs). Plans never supersede specs — they serve specs.

---

### 2.2 Pre-Product _intake Holding Pen

**Canonical path:**

```
Core/products/_intake/YYYY-MM-DD-<topic>/
```

`_intake/` is a sibling directory to the product directories (`cast/`, `forge/`, `loom/`, etc.) under `Core/products/`. It is NOT a product. It is a holding pen for concepts that have not yet earned a scaffold. The underscore prefix causes `_intake/` to sort first in directory listings — this is intentional; it is the most volatile location and should be visible.

[DECISION: `_intake/` lives at `Core/products/_intake/` rather than at `Core/_intake/` because pre-product ideation is specifically about product candidates — frameworks go to `Core/frameworks/`, reusable IP goes to `Core/reference/`. This placement matches WS-DDR-016's three-way disambiguation and keeps the promotion path short (sibling move, not cross-zone move).]

#### 2.2.1 Why Per-Topic Subdirectory (Not a Single File)

A single `_intake.md` file cannot hold design docs, voice captures, early sketches, and early reference material simultaneously without becoming a noise sink. A per-topic subdirectory gives each concept room to grow without polluting other concepts. It also makes the promotion action (moving the whole directory to a named product) a clean `mv` rather than a content-extraction operation.

#### 2.2.2 Required Files

Every `_intake/YYYY-MM-DD-<topic>/` directory MUST contain at minimum:

**`NOTICE.md`** — The Notice beat of the Intent cycle. Answers:
- What triggered this concept? (signal ID, conversation reference, observation)
- What problem is being observed?
- What value hypothesis justifies exploring this?
- Who or what would benefit?

**`design.md`** — Best current sketch of the concept. May be thin at ideation. Must grow to include at minimum: pipeline position claim (per WS-DDR-025), known siblings, and a rough shape of what this would own. A stub is acceptable; an absent file is not.

**`STATUS.md`** — One-line current disposition + last-update date:

```markdown
# Status

disposition: ideation | active | promoted | absorbed | deferred | abandoned
last_updated: YYYY-MM-DD
review_date: YYYY-MM-DD   # required if deferred; optional otherwise
note: [one sentence — what's happening or why it's in this state]
```

#### 2.2.3 Optional Supporting Artifacts

- `references/` — links, excerpts, research inputs
- `voice-captures/` — transcript snippets or voice note transcriptions that originated the idea
- `mockups/` — diagrams, wireframes, structural sketches
- `data/` — any raw data samples relevant to the concept

#### 2.2.4 Lifecycle

Every `_intake/` topic starts as `ideation`. Status transitions are tracked in `STATUS.md`. The `_intake/` directory is **not** a permanent home — a concept that stays in `ideation` for more than 90 days without a review-date set is a stale signal that should be caught by the workspace health check.

Promotion is an action, not a status. See §2.3 for disposition rules.

---

### 2.3 Disposition Rules

When an `_intake/` topic reaches a decision point, one of four dispositions applies. Each disposition has a required audit trail.

| Disposition | Action | Audit Trail Required |
|-------------|--------|----------------------|
| **promoted** | `mv Core/products/_intake/YYYY-MM-DD-<topic>/ Core/products/<name>/` then scaffold the product directory (`.intent/`, `spec/`, `plans/`, `engine/`, `farm/`, `outputs/` per WS-DDR-026) | Tombstone at `Core/products/_intake/<topic>.PROMOTED.md` pointing to new path; WS-DDR if the product is load-bearing; signal in `Core/products/_intake/.intent/signals/` |
| **absorbed** | Merge `_intake/` contents into an existing product's `spec/` or `plans/` | `Core/products/_intake/<topic>.ABSORBED.md` pointing to absorbing product + specific artifact(s) where content landed; retain originals in the absorbing product's history (do not delete from `_intake/` until tombstone exists) |
| **deferred** | Leave in `Core/products/_intake/<topic>/`; update `STATUS.md` with `deferred` + reason + `review_date` | No file move; `STATUS.md` is the audit trail; emit a signal so the review-date is tracked |
| **abandoned** | `mv Core/products/_intake/YYYY-MM-DD-<topic>/ Core/products/_intake/_graveyard/<topic>/` | `Core/products/_intake/_graveyard/<topic>/REASON.md` required — sparse but honest (what was tried, why it failed, what was learned); emit a signal |

#### 2.3.1 Hard Audit Requirements

The following are blocking — no disposition may complete without satisfying these:

1. **No bare moves without tombstones.** Moving a directory without leaving a tombstone breaks discoverability for anyone who has a stale reference to the old path.
2. **No silent abandonment.** Moving to `_graveyard/` without `REASON.md` makes the graveyard a black hole. Honest accounting is the point.
3. **Every disposition action emits a signal** to the appropriate signal directory. For promoted topics: `Core/products/<name>/.intent/signals/SIG-INTAKE-PROMOTED-[topic].yaml`. For absorbed: `Core/products/<absorbing-product>/.intent/signals/SIG-INTAKE-ABSORBED-[topic].yaml`. For deferred/abandoned: `Core/products/_intake/.intent/signals/`.
4. **WS-DDR required for load-bearing promotions.** If a promoted product will have external API consumers, MCP adapters, or cross-product dependencies at launch, file a WS-DDR before promoting. If the product is exploratory with no cross-product contracts at launch, a WS-DDR is optional (but a signal is still required).

---

## Section 3 — Relationship to Intent Framework

Plans are the **Execute-preparation** artifact — the bridge between the Spec beat and the Execute beat in the Notice→Spec→Execute→Observe cycle. They do not replace execution; they define it clearly enough that execution can happen autonomously without Brien's continuous attention.

### 3.1 Artifact Flow

```
SIGNAL (Notice beat)
  │  Something observed; captured to .intent/signals/
  │
  ▼
NOTICE.md (pre-product Notice beat)        ← Only for pre-product concepts (_intake/)
  │  What triggered this? What problem?    ← For in-product work, signals suffice
  │
  ▼
SPEC (.../spec/YYYY-MM-DD-*.md)           ← What to build and why
  │  Source-of-truth for intent
  │
  ▼
PLAN (.../plans/YYYY-MM-DD-*-plan.md)     ← How and when (this convention)
  │  Task-by-task execution blueprint
  │  source_spec → spec
  │
  ▼
EXECUTION (tasks run; files created/modified; commits made)
  │
  ▼
OBSERVE-ARTIFACTS
  ├── Journal entry (Core/products/org-design-tooling/journal/JRN-YYYYMMDD-*.md)
  ├── Post-execute signals (.intent/signals/SIG-OBSERVE-*.yaml)
  └── Retro notes (in the plan's own file, under a new ## Retro section appended after completion)
```

### 3.2 Artifact Type × Intent Beat Table

| Artifact | Intent Beat | Owner | Produces |
|----------|-------------|-------|---------|
| Signal | Notice | `.intent/signals/` | Problem observation |
| NOTICE.md | Notice (pre-product only) | `_intake/<topic>/` | Problem framing |
| Spec | Spec | `<product>/spec/` | What + why |
| Plan | Execute-preparation | `<product>/plans/` | How + when |
| Task execution | Execute | Session / agent | Artifacts, code, files |
| Journal entry | Observe | `org-design-tooling/journal/` | Reflection |
| Post-execute signal | Observe | `.intent/signals/` | Closure event |
| Retro | Observe | Appended to plan | What we learned |

### 3.3 Position of _intake/ in the Intent Cycle

`_intake/` topics live entirely in the **Notice beat** until a decision is made. Promotion moves a topic into the **Spec beat** (the first spec gets written, the product scaffold is created). The `NOTICE.md` in the promoted product's directory (if retained) becomes the origin story for the product — it should not be deleted; it should be moved to `<product>/spec/NOTICE.md` or referenced from the first spec's frontmatter.

---

## Section 4 — Relationship to writing-plans Skill

The `superpowers:writing-plans` skill produces the implementation plan document. This convention is the **persistence target** for that skill's output when working in Brien's Workspaces.

### 4.1 Override of Default Save Path

The `writing-plans` skill defaults to `docs/superpowers/plans/YYYY-MM-DD-<feature-name>.md`. Within Workspaces, this default is **overridden** by this convention. The new persistence target is:

```
Core/products/[name]/plans/YYYY-MM-DD-<topic>-plan.md
```

[DECISION: The `writing-plans` skill's default path (`docs/superpowers/plans/`) is still correct for projects outside Workspaces — this override applies only to Brien's Workspace-resident products. Do not modify the upstream skill SKILL.md; the override lives here in this spec and in the skill's invocation context.]

### 4.2 Invocation Contract

When invoking `superpowers:writing-plans` within Workspaces:

1. **Input:** Provide the absolute path to the source spec as the primary input.
2. **Output path:** Skill writes to `Core/products/[name]/plans/YYYY-MM-DD-<topic>-plan.md`, NOT to `docs/superpowers/plans/`.
3. **Frontmatter:** Skill populates all required frontmatter fields (§2.1.1) from the spec content. `source_spec` is always populated automatically from the provided spec path.
4. **Required sections:** Skill generates all required sections (§2.1.2) with content derived from the spec.

### 4.3 No-Product Guard

If `[name]` does not exist yet as a scaffolded product directory, the skill falls back to writing the plan at:

```
Core/products/_intake/[topic]/plan.md
```

And issues this warning:

> **Warning: No product scaffold exists for `[name]`.** Plan written to `_intake/[topic]/plan.md` as a holding artifact. Before executing this plan, scaffold the product directory (`Core/products/[name]/`) with `.intent/`, `spec/`, `plans/`, and the `engine/farm/outputs` tri-layer per WS-DDR-026. Then move this plan to the canonical location: `Core/products/[name]/plans/YYYY-MM-DD-<topic>-plan.md`.

[DECISION: Writing to `_intake/[topic]/plan.md` is preferable to refusing to write the plan. A plan in the intake pen is better than no plan at all. The warning ensures the gap is not invisible.]

---

## Section 5 — Pilot on Throughline

Throughline is the next product scaffold (Phase 1 per WS-DDR-060 / SIG-PARALLAX-002, ordered before Warp and before Parallax activation). It was named 2026-04-23 during the overwatch session that produced the Parallax spec. Its pre-product state was captured in the Parallax spec itself (`Core/products/parallax/spec/2026-04-23-three-tier-umbrella-and-ecosystem-design.md` §4–§6), not in an `_intake/` directory — because it was named and positioned in the same session that it was decided.

[DECISION: There is no `_intake/` topic for Throughline. The Parallax spec serves as Throughline's NOTICE artifact. The first Throughline spec should reference the Parallax spec in its `origin` frontmatter field.]

### 5.1 What Throughline's plans/ Will Contain Initially

At scaffold, `Core/products/throughline/plans/` should contain at minimum one plan:

**`2026-04-23-throughline-phase-1-plan.md`** — covering:
- Vision-thread schema design (the artifact Throughline owns — answers DEFINITION.md §10)
- Decision-to-vision traceability mechanism (how DDRs, signals, and specs hook into a vision-thread)
- Narrative-extraction MVP (the minimum capability that lets Throughline assert "this artifact has a thread" vs. "this artifact lacks a thread")
- Scaffold tasks (directory creation, INTENT.md, first spec, AGENTS.md registration)

This plan is the first real-world exercise of this convention. It will expose any frontmatter fields that are awkward, any section that is over- or under-specified, and whether the DoR/DoD refs are sufficient.

### 5.2 Pre-Product State for Throughline

As noted above, no `_intake/` activity preceded Throughline — it emerged directly from the Parallax naming session. This means the pilot will test `plans/` convention in an existing-product-scaffold scenario, but will NOT test the `_intake/` → promoted lifecycle. A separate, genuinely pre-product concept must be used to validate the `_intake/` disposition rules before ratification.

[DECISION: The ratification gate (§6) requires at least one `_intake/` promotion or absorption to be exercised — not necessarily Throughline. Any concept that enters `_intake/` before ratification and goes through a disposition satisfies this gate.]

### 5.3 Expected Learnings from Pilot

The pilot is expected to surface answers to:

1. **Frontmatter completeness** — Are the required fields sufficient? Are any fields missing that the executing session needed?
2. **Task granularity calibration** — Is "bite-sized" the right default, or do framework-building plans need coarser tasks because they are less code-centric?
3. **DoR/DoD refs** — Does the existing `dor-dod-library.md` have a `DOR-PLN-*` / `DOD-PLN-*` entry, or must we add it?
4. **Retro discipline** — Is appending a `## Retro` section to the plan file after completion the right Observe-beat artifact, or should retros live elsewhere?
5. **skill:writing-plans override** — Does the invocation contract (§4.2) work cleanly, or does the skill's hardcoded default path need a session-level override mechanism?

Learnings feed §6 ratification and should be captured as signals (`SIG-PLAN-PILOT-*`) as they are discovered.

---

## Section 6 — Ratification Path

This spec is `draft`. Status transitions to `accepted` (ratified) when all of the following gates are met:

**Gate 1 — Throughline pilot complete**
The first plan under this convention has been written, accepted, and executed (all tasks completed or formally deferred with documented rationale). Plan file exists at `Core/products/throughline/plans/` with `status: completed` or `status: deferred`.

**Gate 2 — Intake disposition exercised**
At least one `_intake/` topic has been created and progressed through a disposition (promoted, absorbed, deferred, or abandoned). Tombstone or STATUS.md reflects the outcome. At least one signal was emitted.

**Gate 3 — dor-dod-library.md extended**
`Core/frameworks/intent/knowledge-engine/templates/dor-dod-library.md` has been extended with `DOR-PLN-001` and `DOD-PLN-001` entries covering plan artifacts specifically. Plans are a distinct work type from skills, specs, and engagement deliverables.

**Gate 4 — WS-DDR-061 filed**
The draft stub (Appendix A) has been completed and filed as WS-DDR-061 in `Workspaces/.context/DECISIONS.md`.

**Gate 5 — AGENTS.md updated**
Two new rows added to the §1 Placement Lookup Table (see below). Spec of rows:

| Artifact Type | Engagement-Scoped? | Target Path Pattern |
|---|---|---|
| implementation plan (product-resident) | no | `Core/products/[name]/plans/YYYY-MM-DD-<topic>-plan.md` |
| pre-product concept | no | `Core/products/_intake/YYYY-MM-DD-<topic>/` |

---

## Section 7 — Open Questions

1. **DoR/DoD for plans.** `Core/frameworks/intent/knowledge-engine/templates/dor-dod-library.md` needs a `DOR-PLN-001` / `DOD-PLN-001` entry. This spec cannot define them without reading the existing library for format consistency. [Flagged for Gate 3 — must be done before ratification, not before pilot.]

2. **Retro artifact placement.** Should the `## Retro` section live in the plan file itself (append-on-completion), in the product's `.intent/journal/`, or as a discrete signal? The append pattern is proposed here as the default, but it creates a mutable plan file — which conflicts with the general principle that completed artifacts should be immutable. [DECISION: append-on-completion is accepted as the pilot default; ratification may revise this to a separate `YYYY-MM-DD-<topic>-retro.md` in the same `plans/` directory if pilot shows the mutable-file problem is real.]

3. **Namespace for plan IDs.** The frontmatter proposes `PLAN-[PRODUCT]-NNN` (e.g., `PLAN-THROUGHLINE-001`). This is consistent with `SPEC-VOICES-001` but inconsistent with `SPEC-001-persona-entity-schema.md` (which uses a global sequence, not a per-product sequence). [DECISION: per-product sequences are used here (`PLAN-THROUGHLINE-001`) because plans are not cross-referenceable across products the way shared framework specs are. Plans are product-local. If a plan has cross-product scope, it lives in the narrowest product whose scope it falls within.]

4. **Framework-level plans.** This spec covers `Core/products/[name]/plans/`. What about plans for `Core/frameworks/[name]/`? The Intent framework itself is a candidate. [DECISION: the same convention applies — `Core/frameworks/[name]/plans/YYYY-MM-DD-<topic>-plan.md`. The path pattern in AGENTS.md should be broadened to cover both. This is flagged for Gate 5.]

5. **`_intake/` health-check integration.** The workspace health check (11 dimensions in `.context/CLAUDE.md`) does not currently scan `_intake/` for stale topics. A 12th dimension ("_intake/ topics with no review_date and last_updated > 90 days") should be added. [Flagged — not a ratification blocker, but a SIG-PLAN-002 candidate.]

6. **Interaction with Forge outputs convention.** The `writing-plans` skill is a Forge output surface. Does this plan convention need to be registered in `Core/products/forge/outputs/` or in `forge/farm/` to make Forge aware of the persistence target? [Deferred — evaluate after Forge output surfaces are more mature. Not a ratification blocker.]

---

## Appendix A — Draft WS-DDR-061 Stub

```yaml
id: WS-DDR-061
type: decision
created: 2026-04-23
updated: 2026-04-23
status: proposed                  # changes to accepted on ratification
confidence: 0.88
origin: human+agent
related:
  - WS-DDR-026 (engine/farm/outputs — plans/ parallels this convention)
  - WS-DDR-016 (Core/ three-way disambiguation)
  - WS-DDR-025 (sibling-over-parent-child — _intake/ is sibling, not child)
  - SPEC-PLAN-001 (this spec — the full rationale lives here)
```

### WS-DDR-061 — Plan Artifact Convention + Pre-Product Intake Holding Pen

**Status:** proposed | **Confidence:** 0.88 | **Date:** 2026-04-23

#### Context

Implementation plans had no canonical home in Workspaces. Claude Code's plan mode is ephemeral; the `superpowers:writing-plans` skill defaulted to `docs/superpowers/plans/`, which sits outside the Workspaces organizational system and is invisible to the placement resolver, library index, and signal stream. Pre-product ideation had no home at all — concepts drifted in journals, ad-hoc directories, and conversation.

This created two coherence gaps:
1. The *how* and *when* of execution was not preserved alongside the *what* and *why* (specs).
2. Pre-product concepts could not be audited, promoted, or killed with traceable audit trails.

Full context: `Core/frameworks/intent/spec/plan-artifact-convention.md` (SPEC-PLAN-001).

#### Decision

**Introduce two new directory conventions:**

1. **`Core/products/[name]/plans/YYYY-MM-DD-<topic>-plan.md`** — Implementation plans as first-class, permanent, findable artifacts. Plans are siblings to `spec/`, required to have a `source_spec` reference, required frontmatter, and required sections. The `superpowers:writing-plans` skill's persistence target within Workspaces is overridden to this path.

2. **`Core/products/_intake/YYYY-MM-DD-<topic>/`** — Pre-product holding pen for concepts that have not yet earned a scaffold. Each topic directory holds a required `NOTICE.md` (problem framing), `design.md` (best current sketch), and `STATUS.md` (disposition + last-update). Disposition rules (promoted / absorbed / deferred / abandoned) require audit trails (tombstones, signals, WS-DDRs for load-bearing promotions).

#### Alternatives Considered

| Alternative | Pros | Cons | Why Rejected |
|-------------|------|------|-------------|
| Plans in spec/ as a subdirectory | Co-location with specs | Collapses the spec/plan distinction; makes the "how" invisible inside the "what" | Violates the principle that spec is the source-of-truth for intent, plan is the execution blueprint — different artifact types at different intent beats |
| Plans in .intent/ alongside signals | Signals and plans are both governance artifacts | .intent/ is scoped to signals, decisions, and lifecycle records — not execution blueprints | Plans are not governance metadata; they are operational artifacts that belong with the product, not with the intent overlay |
| Single flat _intake.md file | Simpler (one file per concept) | Cannot hold design docs, voice captures, sketches, and references without becoming a noise sink; promotion is a content-extraction operation, not a clean mv | Per-topic subdirectory makes promotion a single mv with a tombstone |
| _intake/ at Core/ root | One level higher, visible to all domains | Pre-product concepts are specifically product candidates; non-product IP candidates go to Core/frameworks/ or Core/reference/; mixing categories at Core/ root violates WS-DDR-016 | Core/products/_intake/ keeps the promotion path short (sibling move) and the concept category clear |

#### Consequences

**Positive:**
- Plans are first-class, permanent, findable artifacts — searchable by library index, visible to freshness scanner, auditable
- `superpowers:writing-plans` output is preserved within the Workspaces system, not orphaned in `docs/`
- Pre-product ideation has a governed home with disposition audit trails
- Promotion lifecycle is clean (mv + tombstone vs. content extraction)
- Intent cycle is complete: Notice→Spec→Plan→Execute→Observe, each beat with named artifact types

**Negative:**
- AGENTS.md requires two new rows (§1 lookup table)
- `dor-dod-library.md` requires new plan-specific entries (DOR-PLN-001 / DOD-PLN-001)
- `writing-plans` skill invocation requires an explicit override to prevent default-path writes

**Neutral:**
- `_intake/_graveyard/` accumulates over time; graveyard hygiene is out of scope for this DDR but is a future concern

#### Validation Criteria

- [ ] Throughline pilot plan written, accepted, and executed under this convention (Gate 1)
- [ ] At least one `_intake/` disposition exercised with tombstone/signal audit trail (Gate 2)
- [ ] `dor-dod-library.md` has DOR-PLN-001 / DOD-PLN-001 entries (Gate 3)
- [ ] This DDR filed in `.context/DECISIONS.md` (Gate 4)
- [ ] AGENTS.md §1 has two new rows for plans and intake (Gate 5)
- [ ] `writing-plans` skill invocation in at least one session writes to the canonical path, not `docs/` (functional validation)

---

## Appendix B — Plan File Template

Ready-to-copy skeleton with all required frontmatter fields and section headers. Fill-in guidance in `[brackets]`.

```markdown
---
title: "[Topic] Implementation Plan"
id: PLAN-[PRODUCT]-NNN
kind: plan
status: draft
established: YYYY-MM-DD
updated: YYYY-MM-DD
author: brien
source_spec: Core/products/[name]/spec/YYYY-MM-DD-[spec-file].md
dor_refs:
  - DOR-PLN-001
dod_refs:
  - DOD-PLN-001
supersedes: []
related_signals:
  - SIG-[ID]
related_ddrs: []
---

# [Topic] Implementation Plan

> **For agentic workers:** Use `superpowers:executing-plans` or `superpowers:subagent-driven-development`
> to execute this plan task-by-task. Steps use checkbox syntax for tracking.

**Goal:** [One sentence — what does completing this plan produce?]

**Source spec:** `[path to source spec]`

**Architecture:** [2–3 sentences about the approach — what pattern, what sequence, what constraints]

---

## Scope

[Bullet list of what this plan covers]

## Non-Goals

[Explicit callouts of what this plan does NOT address]

## Dependencies

- [PLAN-NNN] — must complete before Task N
- [External system or approval]
- [Signal resolution: SIG-NNN must be resolved]

## Tasks

### Task 1: [Name]

**Files:**
- Create: `Core/products/[name]/[path/to/file.md]`
- Modify: `Core/products/[name]/[path/to/existing.md]`

- [ ] **Step 1: [Action]**
  [Exact content, command, or code — no placeholders]

- [ ] **Step 2: [Action]**
  [Exact content, command, or code — no placeholders]

- [ ] **Step 3: Emit signal**
  Create `Core/products/[name]/.intent/signals/SIG-[ID]-[slug].yaml`:
  ```yaml
  id: SIG-[ID]
  status: open
  summary: "[what just happened]"
  emitted: YYYY-MM-DD
  source_plan: PLAN-[PRODUCT]-NNN
  ```

### Task 2: [Name]

[Repeat structure]

---

## Success Criteria / DoD

- [ ] [Observable, checkable condition 1]
- [ ] [Observable, checkable condition 2]
- [ ] Signal emitted on plan completion

## Risks

| Risk | Likelihood | Impact | Mitigation |
|------|-----------|--------|------------|
| [Risk 1] | low/med/high | low/med/high | [How to mitigate] |

## Rollback

[How to undo this plan's changes. If plan is additive-only with no destructive steps, state that explicitly.]

## Handoff

[What the next session needs to know to pick this up. What is the last completed task? Where are the artifacts?]

---

<!-- Append after execution completes: -->
<!-- ## Retro
date: YYYY-MM-DD
completed_by: [session ID or date]
what_worked: ...
what_didn't: ...
what_to_carry_forward: ...
-->
```

---

## Appendix C — _intake/ Topic Directory Skeleton

Sample structure for a typical `_intake/` topic at the ideation stage:

```
Core/products/_intake/
├── .intent/
│   └── signals/                    # signals for intake-level events
├── _graveyard/                     # abandoned topics
│   └── [abandoned-topic]/
│       └── REASON.md
│
├── 2026-04-23-example-concept/     # a topic directory (kebab-case, date-prefixed)
│   ├── NOTICE.md                   # REQUIRED — Notice beat
│   ├── design.md                   # REQUIRED — best current sketch
│   ├── STATUS.md                   # REQUIRED — disposition + last-update
│   ├── references/                 # optional — links, excerpts, research
│   │   └── relevant-paper.md
│   ├── voice-captures/             # optional — transcript snippets, voice notes
│   │   └── 2026-04-23-session-excerpt.md
│   └── mockups/                    # optional — diagrams, structural sketches
│       └── pipeline-position-sketch.md
│
└── 2026-04-15-another-concept.PROMOTED.md  # tombstone (after promotion to product)
```

**Sample NOTICE.md:**

```markdown
# Notice — [Concept Name]

observed: YYYY-MM-DD
trigger: [Signal ID or session reference that surfaced this]

## Problem Observed

[What is being observed? What gap, failure mode, or opportunity?]

## Value Hypothesis

[Who benefits? How? What is the expected improvement?]

## Next Step

[What needs to happen for this to move from ideation to active?]
```

**Sample STATUS.md:**

```markdown
# Status

disposition: ideation
last_updated: 2026-04-23
review_date:
note: Initial observation captured. No design work started yet.
```

**Sample tombstone (2026-04-23-example-concept.PROMOTED.md):**

```markdown
# Tombstone — example-concept

promoted: YYYY-MM-DD
new_location: Core/products/example-concept/
promoted_by: [session reference]
ddr: WS-DDR-NNN (if load-bearing)
signal: SIG-INTAKE-PROMOTED-example-concept

This concept was promoted to a scaffolded product. All content moved to the new location.
This tombstone exists to preserve discoverability for any stale references to the original _intake path.
```
