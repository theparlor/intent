---
title: Team OS Alignment Annex to SPEC-PLAN-001
id: SPEC-PLAN-001-ANNEX-A
type: spec
maturity: draft
created: 2026-05-09
updated: 2026-05-09
depth_score: 4
depth_signals:
  file_size_kb: 13.8
  content_chars: 12438
  entity_count: 0
  slide_count: 0
  sheet_count: 0
  topic_count: 0
  has_summary: 0
vocab_density: 0.08
status: draft
author: brien
extends: Core/frameworks/intent/spec/plan-artifact-convention.md
ratification_with: SPEC-PLAN-001 (annex ratifies under same gates §6)
attribution:
  primary_lineage:
    - "Brien Tate — Intent framework + Workspaces structure (2026-02 onward); plan-arti"
    - "Karpathy — three-layer architecture (compiled knowledge base + transformation OS"
    - "Hunt & Thomas — Pragmatic Programmer, DRY (referenced in Coherence Engineering §"
    - "Evans — Domain-Driven Design, Bounded Context (CE §4)"
    - "Wiggins — 12-factor, intentional portability (CE §4)"
    - "McIlroy / Kernighan — Unix pipes, composable transforms (CE §4)"
  convergent_validation:
    - "Hannah Stulberg — Aakash Gupta podcast (2026-05); In-the-Weeds Team OS example r"
related_signals:
  - SIG-PLAN-CHECKPOINT-001 (phase-checkpoint pattern formalization)
  - SIG-PLAN-AGENT-PROMPT-001 (agent-prompt embedding pattern)
  - SIG-DOC-INDEX-001 (nested CLAUDE.md doc-index pattern — separate spec)
  - SIG-ROLLOUT-GATE-001 (update-before-rollout governance gate — separate spec)
related_ddrs:
  - WS-DDR-075 (filed 2026-05-09 — Plan Artifact Convention ratification; supersedes original 061 stub due to numbering collision per SIG-DDR-061-COLLISION-2026-05-09)
pilot:
  - PCU-2026-05-09 (Pilot
---
# SPEC-PLAN-001 Annex A — Team OS Alignment

> **Status: DRAFT.** Ratifies under SPEC-PLAN-001 §6 gates (specifically Gate 1 + Gate 2 — Throughline pilot complete + intake disposition exercised). PCU-2026-05-09 is the pilot that exercises the annex's net-new patterns.

---

## Section 1 — Lineage Statement

The plan-as-file-in-git pattern, the engine/farm/outputs convention, the `.intent/` artifact discipline, the federated glossary architecture, and the signal/decision/spec separation all **predate** Brien's exposure to Hannah Stulberg's Team OS articulation. The primary lineage is Brien's own Intent framework + Workspaces structure (active development 2026-02 onward), drawing on Karpathy (three-layer architecture), Hunt & Thomas (Pragmatic Programmer DRY), Evans (DDD bounded context), Wiggins (12-factor portability), and McIlroy/Kernighan (Unix pipes / composable transforms).

Hannah Stulberg's interview with Aakash Gupta (May 2026) and the accompanying example repo provided **convergent validation** — independent articulation of substantially the same pattern — plus ~20% net-new patterns specifically around (a) explicit phase-checkpoint marking within plans, (b) agent-prompt embedding within tasks, (c) nested CLAUDE.md doc-index hierarchies for context economy, and (d) update-before-rollout governance gates.

This annex captures (a) and (b) as extensions to SPEC-PLAN-001's §2.1.2 required sections. (c) and (d) are separate concerns flagged as follow-up signals; they belong to context-economy and workspace-governance specs respectively, not to plan-artifact convention.

The annex does **not** elevate Hannah to origin status. The lineage citation order is: Brien's Intent stack → predecessor masters (Karpathy, Hunt-Thomas, Evans, Wiggins, McIlroy-Kernighan) → Hannah as convergent validator. This ordering is load-bearing per `feedback_attribution` memory ("credit the masters, never template libraries").

---

## Section 2 — Alignment Matrix

| Hannah Stulberg's Team OS pattern | SPEC-PLAN-001 status | Annex action |
|---|---|---|
| File-based markdown plans in git repo | ✅ §2.1 canonical path | None — already covered |
| Plan ID + status lifecycle | ✅ §2.1.1 frontmatter | None |
| Required sections (Goal, Tasks, Verification) | ✅ §2.1.2 | None |
| Plan anchored to source-of-truth | ✅ §2.1.1 `source_spec:` | None |
| Cross-artifact traceability | ✅ §2.1.1 `related_*` fields | None |
| Pre-product ideation holding pen | ✅ §2.2 `_intake/` (Hannah doesn't have this — Brien-net-new) | None — Brien exceeds Hannah here |
| Standardized formats per artifact type | ✅ Templates exist (signal/decision/DDR/spec) | None |
| Per-`.claude/` directory configs | ✅ Exists as Workspaces convention | None |
| Multi-session task handoff | ✅ §2.1.2 Handoff section + §2.1.3 multi-session tasks include Handoff note | Partial — Handoff exists at end-of-plan; **annex adds phase-level checkpoints** |
| Explicit phase-checkpoint marking | ❌ Not formalized | **Annex §3** |
| Agent-prompt embedding within tasks | ⚠ Permitted but not formalized | **Annex §4** |
| Nested CLAUDE.md doc-index hierarchies | ❌ Files exist but not formalized; out of scope for plan convention | Separate spec — SIG-DOC-INDEX-001 |
| Update-before-rollout governance gate | ❌ Not codified | Separate spec — SIG-ROLLOUT-GATE-001 |

**Overlap: ~80%.** Annex contribution: 2 plan-convention extensions + 2 follow-up signal flags.

---

## Section 3 — Phase-Checkpoint Pattern (Net-New)

### 3.1 Problem

SPEC-PLAN-001 §2.1.3 specifies bite-sized atomic tasks (15-25 per plan) with Handoff notes for multi-session tasks. The Handoff section (§2.1.2) captures end-of-plan handoff. **What's missing is mid-plan handoff between phase boundaries.**

For multi-stage operations (audits, migrations, rollouts, portfolio sweeps), the plan executes over multiple sessions — possibly multiple weeks — and individual sessions hit context-window compaction or natural session boundaries. Without explicit phase-checkpoint markers, a resuming session must scan the entire task list to determine "where am I" and risks re-doing completed work or skipping incomplete work.

### 3.2 Resolution

Plans MAY group tasks into named phases. When phases are used, each phase ends with a mandatory `### CHECKPOINT — Phase N` block before the next phase begins. The checkpoint block contains:

```markdown
### CHECKPOINT — Phase N: [Phase Name] complete

**Phase verification (must pass before Phase N+1 begins):**
- [ ] [Concrete verifiable condition 1 — produces an artifact at <path>, or signal at <path>, or test passes, etc.]
- [ ] [Condition 2]
- [ ] [Condition 3]

**Phase artifacts produced:**
- `<path>` — [what it is]

**Resume instructions for next session:**
[One paragraph — if a session compacts mid-phase, what state survives, what to re-load, what to verify before continuing. If next phase requires user review/approval, name that explicitly.]

**Handoff signal (optional):**
Emit `SIG-[plan-id]-PHASE-N-COMPLETE` if cross-session handoff is expected.
```

### 3.3 When phases are appropriate

Use phases when:
- The plan spans more than one expected session
- Earlier phases produce artifacts that later phases depend on (intermediate state matters)
- Sequential dependencies prevent parallel execution of all tasks
- A natural review/approval gate exists between phases
- Per-phase verification reduces blast radius of any individual phase's failure

Do NOT use phases when:
- The plan is single-session
- All tasks are independent and parallelizable
- The plan is small (<15 tasks total)

For non-phased plans, SPEC-PLAN-001 §2.1.2 unchanged — flat Tasks list with end-of-plan Handoff is canonical.

### 3.4 Worked example

```markdown
## Tasks

### Phase 1: Per-product inventory (parallel)

- [ ] Task 1.1: Dispatch 14 Sonnet research agents in parallel — one per registered product. Brief: read INTENT.md + CONTEXT.md + top-level spec; report on TDD/observability/dashboard gaps + cross-product seams + product-specific goodness. Output: `Core/products/_intake/2026-05-09-portfolio-inventory/<product>-report.md`.
- [ ] Task 1.2: Aggregate 14 reports into portfolio gap-inventory matrix. Output: `Core/products/_intake/2026-05-09-portfolio-inventory/portfolio-matrix.md`.
- [ ] Task 1.3: Emit signals — one per cross-cutting gap detected — to `Core/products/org-design-tooling/.intent/signals/`.

### CHECKPOINT — Phase 1: Portfolio inventory complete

**Phase verification (must pass before Phase 2 begins):**
- [ ] All 14 per-product reports exist at `Core/products/_intake/2026-05-09-portfolio-inventory/<product>-report.md`
- [ ] Portfolio matrix exists at the canonical path
- [ ] At least 3 cross-cutting gap signals filed
- [ ] User reviews matrix and approves Phase 2 scope

**Phase artifacts produced:**
- 14 per-product gap reports
- Portfolio gap matrix
- N cross-cutting signals

**Resume instructions for next session:**
If session ends mid-phase: re-read `Core/products/_intake/2026-05-09-portfolio-inventory/` to see which product reports landed; dispatch agents only for missing products. If matrix incomplete, run aggregation step. Phase 2 cannot begin until checkpoint verification passes.

**Handoff signal:**
Emit `SIG-PCU-PHASE-1-COMPLETE`.

### Phase 2: Portfolio-baseline meta-spec

- [ ] Task 2.1: ...
```

### 3.5 Compatibility with §2.1.3 task granularity

Phases group tasks; they do not change task granularity. Each task within a phase remains bite-sized atomic per §2.1.3. A plan with 6 phases and 4 tasks per phase has 24 tasks — within the 15-25 envelope. Plans with significantly more tasks per phase should consider splitting into sub-plans (one plan per phase) per §2.1.5 (one plan per execution phase is the recommended pattern for complex specs).

---

## Section 4 — Agent-Prompt Embedding (Net-New)

### 4.1 Problem

SPEC-PLAN-001 §2.1.3 specifies tasks as concrete atomic actions but does not formalize embedding agent invocation prompts within tasks. For tasks that dispatch subagents (the increasingly common pattern in Brien's Workspaces), the prompt is the load-bearing instruction; without it embedded in the task, the executing session must reconstruct the prompt from context — which fails reliably across session boundaries.

Hannah's pattern: each task that dispatches a subagent includes the full prompt verbatim. The plan is then re-executable by any session that reads it.

### 4.2 Resolution

Tasks that dispatch a subagent MUST include the agent's invocation block as a code-fenced sub-element of the task. Format:

```markdown
- [ ] Task N.M: [One-line description of what the agent does]
  ```yaml
  agent_dispatch:
    subagent_type: [general-purpose | specialized agent name]
    model: [opus | sonnet | haiku — explicit; do not rely on inheritance]
    description: "[short — 3-5 word description for tool call]"
    prompt: |
      [Full prompt verbatim. Self-contained. Includes context the agent will not have. Cites file paths absolutely.]
  ```
```

### 4.3 When this applies

- Required for tasks that dispatch via the `Agent` tool.
- Recommended (not required) for tasks that issue parallel WebFetch / WebSearch / Bash commands where the exact invocation matters for reproducibility.
- Not applicable for tasks that are pure file edits or local commands.

### 4.4 Why verbatim prompts

A reconstructed prompt is a different prompt. Per `feedback_decisioning_discipline` and the wider closure-DoD posture, plans must survive pickup by any session — including a fresh session that lacks the originating context. Embedding the prompt makes the plan a complete artifact rather than a reference to a context the resuming agent must rebuild.

This also enables panel review of the prompts themselves before plan execution — the prompt is the most error-prone part of subagent dispatch and benefits from second-eyes scrutiny ahead of execution.

---

## Section 5 — Out-of-Scope Patterns (Follow-up signals)

The following Hannah-Team-OS patterns are not part of plan-artifact convention. They are flagged here for separate spec work.

### 5.1 Nested CLAUDE.md doc-index hierarchy (SIG-DOC-INDEX-001)

Hannah's pattern: lean root CLAUDE.md + per-directory CLAUDE.mds with progressive doc indexes. A query like "who are my top customers?" navigates root → directory → file via summary indexes, consuming ~3% of context window rather than loading everything.

Workspaces has ~20 CLAUDE.md files at various levels (root .context/CLAUDE.md, domain-level Personal/Home/Core/Work, product-level for several products, engagement-level for some Subaru/Turnberry/Optum/Wellmark/F&G). The pattern is partially present but not formalized as Hannah-shape progressive doc indexes.

This is a context-economy concern, not a plan-artifact concern. Author as `Core/frameworks/intent/spec/nested-claude-md-doc-index-spec.md` (or similar) — separate spec, separate ratification.

### 5.2 Update-before-rollout governance gate (SIG-ROLLOUT-GATE-001)

Hannah's rule: "feature is not rolled out until repository is updated." This is a governance gate — implicit in Brien's discipline but not codified.

Belongs in workspace governance, not plan convention. Author as a §3 hard gate in `Workspaces/AGENTS.md` (or as a Rule in `Core/products/digital-declutter/RULES.md`) — separate spec work.

---

## Section 6 — Pilot Validation

PCU-2026-05-09 (Portfolio Coherence Uplift) is **Pilot #2** for SPEC-PLAN-001, exercising:

| Annex element | PCU pilot test |
|---|---|
| §3 Phase-Checkpoint pattern | PCU plan has 6 phases with checkpoint blocks between |
| §4 Agent-prompt embedding | PCU Phase 1 dispatches 14 parallel Sonnet agents — each with embedded prompt |
| SPEC-PLAN-001 §2.2 `_intake/` | PCU Phase 1 produces inventory artifacts at `Core/products/_intake/2026-05-09-portfolio-inventory/` — closes SPEC-PLAN-001 ratification Gate 2 |

Learnings captured as signals at `Core/products/org-design-tooling/.intent/signals/` per SPEC-PLAN-001 §5.3.

---

## Section 7 — Ratification

Annex ratifies with SPEC-PLAN-001 under the same §6 gates. No separate ratification path. Annex content folds into a future SPEC-PLAN-002 if the convention evolves substantially post-ratification.

WS-DDR-061 (pending stub per SPEC-PLAN-001 Appendix A) records the ratification when gates close. Annex is referenced as `extends: SPEC-PLAN-001-ANNEX-A` in WS-DDR-061's body.
