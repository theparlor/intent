---
title: IDD Build Pattern — Cross-Product Applicability Matrix
id: PLAYBOOK-CROSS-PRODUCT-APPLICABILITY-001
type: applicability-map
depth_score: 4
depth_signals:
  file_size_kb: 20.3
  content_chars: 19070
  entity_count: 0
  slide_count: 0
  sheet_count: 0
  topic_count: 0
  has_summary: 0
vocab_density: 0.37
status: ratified
date: 2026-05-20
upstream_control_path: "Core/frameworks/intent/playbooks/idd-build-pattern.md (pattern definitions) + Core/frameworks/intent/playbooks/cross-product-applicability.md (this file, applicability mapping)"
catch_mechanism: "idd-build-pattern.md is the source of truth for pattern definitions; this matrix is a derived artifact — if patterns are updated in the source, this matrix must be updated to match. Session overwatch sweeps catch stale derived artifacts."
pipeline_survival: "matrix is product-agnostic and survives product changes; rows are stable (products don't disappear); columns are stable (5 patterns are generalized from cross-build evidence, not product-specific); new products add rows"
source_build: element-substrate-and-recursive-arb (Core/products/cast/.worktrees/element-substrate-recursive-arb/)
---
# IDD Build Pattern — Cross-Product Applicability

> This matrix maps the 5 load-bearing IDD patterns to every Workspaces product, framework, and engagement tier. Use it to identify where to apply IDD discipline when starting a new build loop.

**Pattern columns (from `idd-build-pattern.md`):**
- **P1** — Trigger-vs-Correction Distinction (F8 Mandate)
- **P2** — Closure-Discipline Triad (upstream_control_path / catch_mechanism / pipeline_survival)
- **P3** — Autonomy 4-Gate Execution (including dispatch-prompt injection risk)
- **P4** — Sibling-Architecture Closure Scope
- **P5** — TDD/SDD Double Discipline (red-green + implementer-escalation contracts)

**Cell legend:**
- ✓ — pattern applies directly
- ◐ — pattern applies with adaptation (noted)
- ✗ — pattern not applicable here (reason noted)

---

## Products

### Cast — Persona Engine
`Core/products/cast/`

| Pattern | Status | What it looks like here |
|---|---|---|
| **P1** Trigger-vs-correction | ✓ | chain_audit invariant fires → investigate whether the violation was pre-existing or introduced by this build before claiming correction credit. F8 is the canonical Cast example. |
| **P2** Closure triad | ✓ | Every chain_audit invariant is the `catch_mechanism`; the invariant script path is the `upstream_control_path`; `pipeline_survival` = "invariant runs on every audit invocation." |
| **P3** Autonomy 4-gate | ✓ | Design decisions about schema fields, axis values, provenance types, and heuristic strategies all pass 4-gate. Dispatch prompts for design subagents must not contain proposal-framing. |
| **P4** Sibling-scope closure | ✓ | The element-substrate build is the canonical example. Recursive ARB engine (Plan C), peer-authored pipeline (§15), entire.io adapter (F2) all opened as sibling loops — not held in the element-substrate close. |
| **P5** TDD/SDD | ✓ | Strict red-green TDD per plan step (element-substrate: 14 tests before first green). chain_audit as the harness. Implementer-escalation: M-class findings stay with implementer; I-class escalate to controller. |

---

### Forge — Composition Engine
`Core/products/forge/`

| Pattern | Status | What it looks like here |
|---|---|---|
| **P1** Trigger-vs-correction | ✓ | Skill intake violations (SKILL.md gate failures) are triggers; the correction is the upstream gate or methodology module, not the individual skill re-write. |
| **P2** Closure triad | ✓ | `upstream_control_path` = SKILL.md mandatory section that governs the domain; `catch_mechanism` = skill-intake-gate-check.sh PreToolUse hook; `pipeline_survival` = "hook runs on every Agent dispatch." |
| **P3** Autonomy 4-gate | ✓ | Skill rendering decisions (persona × methodology × platform mappings) pass 4-gate. New output surface decisions (Copilot rendering) also pass 4-gate — execute + signal, don't propose. |
| **P4** Sibling-scope closure | ◐ | Forge renders Cast personas, Voices dissents, Throughline vision-threads — but each rendering contract is a sibling IDD loop, not a sub-task of Forge's own IDD. Forge's loop closes on the rendering engine; consumer product loops close independently. |
| **P5** TDD/SDD | ◐ | Forge skills are declarative (SKILL.md), not code. "TDD" here means: define the output contract (DoD) before writing the SKILL.md, then verify the rendered output against the contract. Red-green discipline still applies; the test is a reference run, not a unit test. |

---

### Voices — Correctness Kernel
`Core/products/voices/`

| Pattern | Status | What it looks like here |
|---|---|---|
| **P1** Trigger-vs-correction | ✓ | Dissent-preservation violations (INV-1..10) are triggers; the correction is the conservation law enforcement at the pipeline stage, not the individual panel output. |
| **P2** Closure triad | ✓ | `upstream_control_path` = INV-1..10 invariant implementations; `catch_mechanism` = the invariant test suite; `pipeline_survival` = "tests run in CI on every commit." Voices INV-1..10 also serves as the cross-product correctness oracle (F5 — any panel-assembler can test against it). |
| **P3** Autonomy 4-gate | ✓ | Dissent-framing decisions (channel layout, sycophancy guard parameters, persona-slug attribution) pass 4-gate. |
| **P4** Sibling-scope closure | ✓ | panel-critique skill is a Forge rendering of Voices (sibling via adapter), not a sub-component. Recursive ARB engine (Plan C) is a sibling capability — its own worktree, its own IDD loop. |
| **P5** TDD/SDD | ✓ | INV-1..10 test suite is the red-green harness. Each invariant added gets a failing test before the implementation. panel-critique builds can use the existing suite as oracle (F5 generalization). |

---

### Loom — Cross-Session Coordination
`Core/products/loom/`

| Pattern | Status | What it looks like here |
|---|---|---|
| **P1** Trigger-vs-correction | ✓ | Loom's 7-verb port is the coordination substrate. A trigger is a coordination failure (session doesn't know what another session committed). The correction is the write-through port implementation, not a patch to the failing session. |
| **P2** Closure triad | ✓ | `upstream_control_path` = the 7-verb port contract; `catch_mechanism` = a session that reads Loom sees correct state; `pipeline_survival` = "Loom state is authoritative across sessions; sessions don't maintain parallel shadow state." |
| **P3** Autonomy 4-gate | ✓ | Coordination contract decisions (which verbs are in the port, how state is shared, how conflicts resolve) pass 4-gate. |
| **P4** Sibling-scope closure | ✓ | Loom is at the Awareness pipeline position; Topography is at Planning. They compose at the COMPACT seam but close independently. A Loom build doesn't hold open for Topography's build. |
| **P5** TDD/SDD | ◐ | Loom's core is the coordination protocol. "TDD" here means: define the coordination contract as a test harness before implementing the verbs. Integration-style tests (does session A see session B's commit?) rather than unit tests. |

---

### Topography — Planning Substrate
`Core/products/topography/`

| Pattern | Status | What it looks like here |
|---|---|---|
| **P1** Trigger-vs-correction | ✓ | A planning failure (score/active/handoff verbs returning stale state) is a trigger. The correction is the upstream write-through, not a patch to the stale output. |
| **P2** Closure triad | ✓ | 3-verb port (score/active/handoff) is the upstream control. `catch_mechanism` = a handoff that reads Topography sees correct active set; `pipeline_survival` = "composes with Loom at COMPACT seam — state flows through, not around." |
| **P3** Autonomy 4-gate | ✓ | Port contract decisions pass 4-gate. |
| **P4** Sibling-scope closure | ✓ | Topography at Planning position; Loom at Awareness position. They're siblings. Close independently. |
| **P5** TDD/SDD | ◐ | Same adaptation as Loom: coordination-contract tests before implementation. |

---

### Throughline — Vision-Thread & Traceability
`Core/products/throughline/`

| Pattern | Status | What it looks like here |
|---|---|---|
| **P1** Trigger-vs-correction | ✓ | A traceability gap (decision can't be traced to vision-thread) is the trigger; the correction is the vision-thread artifact schema + the audit that detects gaps, not a patch to the individual decision. |
| **P2** Closure triad | ✓ | `upstream_control_path` = vision-thread artifact + TC-004 schema decision (pending); `catch_mechanism` = audit that checks every decision has a vision-thread cite; `pipeline_survival` = "schema governs all new vision-thread artifacts." |
| **P3** Autonomy 4-gate | ✓ | Schema decisions (TC-004) pass 4-gate. Schema is reversible and local. |
| **P4** Sibling-scope closure | ◐ | Throughline is Phase 1 of the Parallax umbrella (Throughline → Warp → Parallax). Each phase is a sibling IDD loop; Throughline doesn't block on Warp's completion. |
| **P5** TDD/SDD | ◐ | Test = "can a given decision be traced to a vision-thread entry?" Implement the audit before implementing the schema. |

---

### Parallax — Coherence Umbrella
`Core/products/parallax/`

| Pattern | Status | What it looks like here |
|---|---|---|
| **P1** Trigger-vs-correction | ✓ | Coherence failures (coordination tax accumulating, sessions diverging) are triggers. Parallax's correction is the umbrella framing (Throughline → Warp → Parallax phased GTM), not a patch to individual session behavior. |
| **P2** Closure triad | ✓ | The three-tier spec is the upstream control; `catch_mechanism` = portfolio-level coherence audit; `pipeline_survival` = "phased GTM means Throughline ships first; Warp and Parallax are sequenced, not deferred." |
| **P3** Autonomy 4-gate | ✓ | GTM framing decisions and umbrella architecture decisions pass 4-gate. |
| **P4** Sibling-scope closure | ✓ | Three-tier: Throughline / Warp / Parallax are siblings in the GTM sequence, each with its own IDD loop. |
| **P5** TDD/SDD | ◐ | Parallax is a positioning/GTM product. "Test" = does the Throughline → Warp → Parallax sequence produce coherent messaging without internal contradictions? Define the coherence check before writing the umbrella spec. |

---

### Coherence Engineering — Discipline Framework
`Core/frameworks/coherence-engineering/`

| Pattern | Status | What it looks like here |
|---|---|---|
| **P1** Trigger-vs-correction | ✓ | Coordination-tax symptoms (repeated schema conflicts, session divergence, linter races on canonical files) are triggers. The correction is the framework itself (4 altitudes, 5 axioms), not the patch to the individual symptom. |
| **P2** Closure triad | ✓ | `upstream_control_path` = DEFINITION.md + framework altitudes; `catch_mechanism` = the governance audit (overwatch); `pipeline_survival` = "coherence engineering is the discipline applied at every build — it doesn't expire." |
| **P3** Autonomy 4-gate | ✓ | Framework evolution decisions pass 4-gate. |
| **P4** Sibling-scope closure | ✓ | Coherence Engineering is a framework, not a product. Its IDD loops are framework evolution cycles, not product build cycles. Each evolution is a sibling to the others. |
| **P5** TDD/SDD | ◐ | "Test" = does applying the framework reduce coordination tax in a measurable way? Define the measurement before evolving the framework. |

---

### Fieldbook — Expense Lifecycle System
`Core/products/fieldbook/`

| Pattern | Status | What it looks like here |
|---|---|---|
| **P1** Trigger-vs-correction | ✓ | An expense leak (receipt not captured, wrong category) is the symptom; the correction is the INTAKE → LEDGER → COMPLY → NARRATE → EXPORT pipeline stage that prevents the class of leak, not the individual re-entry. |
| **P2** Closure triad | ✓ | Each pipeline stage has an upstream control (the stage contract), catch_mechanism (the confidence-scoring gate at intake), and pipeline_survival (ledger is append-only; exports are projections). |
| **P3** Autonomy 4-gate | ✓ | Ledger schema decisions, confidence-matrix configuration, category alignment (Harvest → Fieldbook) all pass 4-gate. |
| **P4** Sibling-scope closure | ✓ | Fieldbook has no IDD loop yet (HIGH LEVERAGE — see "Where to Start" below). When it does: each pipeline stage (INTAKE / LEDGER / COMPLY / NARRATE / EXPORT) is a sibling IDD loop, not a monolithic build. |
| **P5** TDD/SDD | ✓ | Ledger-first: implement the ledger schema + append-only invariant before implementing any intake parser. Receipt ingestion: define the confidence-scoring test before implementing the parser. |

---

### Library-Index — Autonomous Ops
`Core/products/library-index/`

| Pattern | Status | What it looks like here |
|---|---|---|
| **P1** Trigger-vs-correction | ✓ | A freshness failure (stale artifact in the index, wrong depth score) is the symptom; the correction is the write-through resolver that keeps the index fresh, not a one-shot re-scan. HIGH LEVERAGE — Library-Index has trigger-vs-correction risk right now (see "Where to Start"). |
| **P2** Closure triad | ✓ | `upstream_control_path` = the autonomous ops pipeline (Phase 0–2); `catch_mechanism` = the depth-score audit and freshness scan; `pipeline_survival` = "the pipeline runs on its own cron cadence; it doesn't require Brien to trigger." |
| **P3** Autonomy 4-gate | ✓ | Index schema evolution, new artifact type registration, depth-score threshold changes all pass 4-gate. |
| **P4** Sibling-scope closure | ✓ | Phase 3 (declutter) is a sibling to Phase 0–2 (already landed). Don't reopen Phase 0–2's loop for Phase 3 scope questions. |
| **P5** TDD/SDD | ✓ | Depth-score formula: define the test (expected score for a known artifact) before implementing the formula. Write-through resolver: define the idempotency test before implementing the resolver. |

---

### Cortège — Fetch Fabric
`Core/products/cortege/`

| Pattern | Status | What it looks like here |
|---|---|---|
| **P1** Trigger-vs-correction | ✓ | A 429 cascade (domain rate-limit exceeded) is the symptom; the correction is the per-domain concurrency cap + token-bucket pacing, not a retry of the failed request. |
| **P2** Closure triad | ✓ | `upstream_control_path` = per-domain concurrency cap config; `catch_mechanism` = 429-rate monitor; `pipeline_survival` = "concurrency caps are configured per-domain, not per-request." |
| **P3** Autonomy 4-gate | ✓ | Domain rate-limit configuration decisions pass 4-gate. |
| **P4** Sibling-scope closure | ✓ | LinkedIn capture skill (Tier 2/3 of SIG-039 coverage strategy) is a sibling — its IDD loop is independent of Cortège's fetch-fabric IDD loop. |
| **P5** TDD/SDD | ✓ | Define the rate-limit test (does a burst of N requests respect the concurrency cap?) before implementing the cap. Token-bucket pacing: define the timing test before implementing the pacing algorithm. |

---

### Intent Framework — Meta-Level
`Core/frameworks/intent/`

| Pattern | Status | What it looks like here |
|---|---|---|
| **P1** Trigger-vs-correction | ✓ | A hook failure (drift caught by Stop hook but not corrected) is the symptom; the correction is the hook logic update or a new layer, not a re-run of the session. |
| **P2** Closure triad | ✓ | Every hook is both a `catch_mechanism` and an `upstream_control_path`. The intent framework's IDD loops are hook deployments — each one closes with the hook in `~/.claude/settings.json` and verified firing. |
| **P3** Autonomy 4-gate | ✓ | Hook logic updates, new layer additions, regex tuning — all pass 4-gate. |
| **P4** Sibling-scope closure | ✓ | Each enforcement layer (1–5) is a sibling IDD loop. Layer 5 landing doesn't reopen Layer 1's loop. |
| **P5** TDD/SDD | ✓ | Hook tests: `Core/frameworks/intent/tests/test_autonomy_grant_dispatch_hook.sh` (three scenarios per hook). Define the test scenarios before writing the hook script. |

---

### Witness — Observability Layer
`Core/products/witness/`

| Pattern | Status | What it looks like here |
|---|---|---|
| **P1** Trigger-vs-correction | ✓ | An observability gap (session not captured, trace not emitted) is the symptom; the correction is the write-through OTLP emission at the pipeline stage, not a post-hoc re-capture. |
| **P2** Closure triad | ✓ | Phase 5 (14 tests, 2026-05-13) landed with the test suite as `catch_mechanism`. Phase 6 (Cast wiring) is a future sibling loop. |
| **P3** Autonomy 4-gate | ✓ | Witness consumer configuration (which products emit, which degraded-mode contracts apply) pass 4-gate. |
| **P4** Sibling-scope closure | ✓ | F1 (from element-substrate build) is the canonical example: Witness = preferred consumer, not prerequisite. Cast's IDD loop closed before Witness Phase 6 wired in. Witness Phase 6 is its own IDD loop. |
| **P5** TDD/SDD | ✓ | 14 tests landed before Phase 5 green. Same discipline applies to Phase 6. |

---

### Engagement Work — Consulting Tier
`Work/Consulting/Engagements/*/`

| Pattern | Status | What it looks like here |
|---|---|---|
| **P1** Trigger-vs-correction | ◐ | A client symptom (team isn't using Jira, sprint isn't being run) is the trigger; the correction is the upstream coaching/governance intervention, not the patch to the single sprint. Honesty: verify whether the symptom is active or vestigial before claiming credit for a fix (F3 analog — scaffold≠write-through applies here too). |
| **P2** Closure triad | ◐ | Engagement artifacts don't carry YAML frontmatter, but the same questions apply: what governs this domain going forward? what catches regression? what survives handoff? Name these explicitly in close-out deliverables. |
| **P3** Autonomy 4-gate | ✓ | Engagement design decisions (which framework to use, how to structure workshops, which Jira automation to configure) pass 4-gate. HIGH LEVERAGE — closure discipline gaps in engagement work are the most common source of Brien feedback. |
| **P4** Sibling-scope closure | ✓ | Each engagement module (team coaching / Jira governance / workshop design / executive advisory) is a sibling capability. A coaching module landing doesn't block the Jira governance module from closing. |
| **P5** TDD/SDD | ◐ | "Test" = agreed success criteria (DoD) for the deliverable defined before delivery. DoR/DoD as client-engagement primitives (entry/exit criteria per phase). |

---

## Where to Start (Highest-Leverage Intersections)

These 5 intersections have the highest expected return on applying IDD discipline now:

### 1. Fieldbook × P2 + P5 (No IDD loop exists yet)
Fieldbook has a design spec but no IDD loop. The highest-leverage entry point is the LEDGER pipeline stage: write the append-only invariant test (P5 red-green) and the ledger schema as the `upstream_control_path` (P2 triad) before any implementation. This creates the structural foundation that all other pipeline stages (INTAKE, COMPLY, NARRATE, EXPORT) build on. Starting here avoids the pattern of scaffold≠write-through (F3).

### 2. Library-Index × P1 (Trigger-vs-correction risk is live)
Library-Index has existing autonomous ops (Phase 0–2 landed) but the trigger-vs-correction distinction is at risk: when the freshness scan catches a stale artifact, it's tempting to claim "resolved" after a one-shot re-scan rather than verifying the write-through resolver is the active upstream control. Applying F8 discipline here means: every freshness catch must cite the write-through resolver as the `upstream_control_path` and verify it ran, not just that the artifact is now fresh.

### 3. Engagement Work × P3 (Closure discipline gaps are the recurring source of Brien feedback)
Every Jira spec, coaching deliverable, and workshop plan is a candidate for autonomy-grant drift. The highest-leverage application of P3 is in the brief given to subagents working on engagement artifacts: dispatch prompts must not contain proposal-framing. The autonomy-grant-dispatch-prompt-check.sh hook catches this mechanically, but the higher-leverage prevention is writing clean briefs from the start.

### 4. Cast × P1 + P4 (F8 mandate as standing discipline, not one-time fix)
The F8 mandate was learned in this build. It applies to every future Cast build: when a chain_audit violation count changes, run an investigation commit before the Observe close. Cast's chain_audit gives frequent trigger signals; F8 prevents trigger overclaims from becoming a pattern.

### 5. Voices × P5 (INV-1..10 as cross-product oracle)
Voices' conservation law (INV-1..10) is now the correctness oracle for ANY panel-assembler (F5 generalization). Any new panel-behavior system (Forge skill, Cast ARB engine, future products) can and should use Voices INV-1..10 as its red-green harness before building a new test suite. This is the highest-leverage TDD entry point across all products that assemble panels.
