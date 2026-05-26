---
title: IDD Build Pattern — Intent-Driven Development
id: PLAYBOOK-IDD-BUILD-PATTERN-001
type: playbook
depth_score: 4
depth_signals:
  file_size_kb: 16.5
  content_chars: 15493
  entity_count: 0
  slide_count: 0
  sheet_count: 0
  topic_count: 0
  has_summary: 0
vocab_density: 0.13
status: ratified
date: 2026-05-20
upstream_control_path: "Core/frameworks/intent/playbooks/idd-build-pattern.md (this file) + all 7 hooks in Core/frameworks/intent/hooks/ (the mechanism-level enforcement layer)"
catch_mechanism: "autonomy-grant-stop-check.sh (Layer 4, Stop event) + autonomy-grant-dispatch-prompt-check.sh (Layer 5, PreToolUse Agent) + closure-discipline-stop-check.sh (Layer 4, Stop event) + closure-discipline-signal-check.sh (Layer 5, PreToolUse Write/Edit) + autonomy-grant-check.sh (Layer 1, SessionStart) + closure-discipline-check.sh (Layer 1, SessionStart)"
pipeline_survival: "hooks run on every session and every agent dispatch; playbook is referenced from ARCHITECTURE.md; cross-product applicability map (cross-product-applicability.md sibling) propagates pattern to all Workspaces products; process-drift-catalog.md (sibling) provides per-family drift prevention"
source_build: element-substrate-and-recursive-arb (Core/products/cast/.worktrees/element-substrate-recursive-arb/)
source_learnings: .intent/learnings/2026-05-19-element-substrate-build-F1-F13.md
---
# IDD Build Pattern

> Intent-Driven Development (IDD) is the execution discipline used across all Workspaces products, frameworks, and engagement work. This playbook synthesizes the pattern from the element-substrate-and-recursive-arb build — 13 learnings, 3 drift signals, and a full Observe-stage close. It is reusable across any non-trivial build.

---

## Frame: The IDD Arc

IDD runs four stages. Each is a gate, not a phase — the work at each stage is load-bearing for the next.

```
NOTICE → SPEC → EXECUTE → OBSERVE
```

**NOTICE** — a trigger (invariant violation, diagnostic count, observation, signal) surfaces a model error or gap. The notice signal is the authoritative anchor for the entire loop. It names:
- The specific trigger (what fired, what count, what commit)
- The proposed resolution (spec path, branch, plan shape)
- The autonomy level and autonomy grants in scope

**SPEC** — a design document that commits to:
- The plan structure (Plan A / B / C / D, etc.) with explicit success gates per plan
- All design decisions ratified before implementation begins (not deferred to "Brien review")
- DoR/DoD per plan step (entry and exit criteria)
- The closure-discipline triad keys populated in the spec's frontmatter

**EXECUTE** — plan steps run. Within each plan step:
- Strict red-green TDD: every task gets a failing test on record before the fix lands
- Implementer-escalation contracts: the plan step names which classes of finding go to the controller vs. can be resolved autonomously
- Subagent-driven-development pattern at the dispatch layer (independent tasks parallel; dependent tasks sequenced)
- 4-gate check on every decision that might otherwise be framed as a proposal

**OBSERVE** — the close signal. Not a summary — a verification. It must:
- Cite the actual trigger-resolution mechanism (which commit, which upstream control)
- State the build's substantive contribution (which may differ from the trigger resolution — see F8)
- Confirm all plan gates passed or carry-forwarded honestly
- Name sibling capabilities opened during the session as independent IDD loops
- Close at the correct scope (model-correction scope, not sibling-capability scope)

---

## Five Load-Bearing Patterns

### 1. Trigger-vs-Correction Distinction (F8 Mandate)

**Pattern:** The trigger (the symptom that motivated the build) and the correction (the model change the build makes) are different things. They may be resolved by different commits, different agents, or different timelines.

**The F8 mandate:** Before closing any Observe stage, verify the actual trigger-resolution mechanism. If the trigger count moved to zero during the build, it may have resolved independently (a prior commit, a data change, an external fix). The build's contribution is what it actually changed — not what it happened to coincide with.

**Structural consequence:** The Observe close signal MUST cite the specific commit that resolved the trigger. Framing the build as "this resolved the trigger" without verification is a honesty violation — an overclaim that corrupts the IDD record.

**Application:** Any time a diagnostic count changes during a build, run an investigation commit before the Observe close. Trace the actual mechanism. Cite it correctly.

---

### 2. Closure-Discipline Triad

**Pattern:** Every signal or artifact claiming resolution MUST carry three literal frontmatter keys. Not narrative descriptions — literal key-value pairs:

```yaml
upstream_control_path: <file path that governs the domain going forward>
catch_mechanism: <the hook/invariant/test/gate that fires if the pattern regresses>
pipeline_survival: <what makes this fix survive across builds and sessions>
```

**These are literal keys.** Markdown headers (`## Upstream Control`) do not satisfy the hook. Prose descriptions ("the chain_audit script handles this") do not satisfy the hook. The closure-discipline-signal-check.sh (Layer 5) reads frontmatter; it cannot parse prose.

**Status vocabulary discipline:**
- `status: resolved` = upstream control installed + catch_mechanism active + pipeline_survival verified
- `status: symptom-repaired, upstream-pending` = visible symptom fixed; upstream control not yet installed
- `status: captured` = observation recorded; no closure claim; triad keys optional
- `status: iteration-closed` = sub-phase complete; build remains open; triad keys present + explicit NOT-build-closed statement

**When `status: captured` is correct:** metric observations, finding records, observation signals — anything that makes no closure claim. The triad is optional for these. The hook only fires on `resolved`/`closed`/`done`.

---

### 3. Autonomy 4-Gate Execution

**Pattern:** Every decision that might be framed as a proposal must first pass the 4-gate check. If all 4 pass, execute and signal — never propose, never queue, never ask.

The 4 gates:
1. **Reversible?** Can the action be undone without external side effects?
2. **Local blast?** Do changes land inside Workspaces, not in external systems?
3. **Precedent?** Has a similar decision been made, or is there an explicit autonomy grant covering this class?
4. **No info gap?** Is there no missing information only Brien can supply?

**The subagent-prompt injection risk (F13):** Dispatch prompts are a drift vector not caught by response-level hooks. The parent session may understand the autonomy posture; the dispatch prompt may still re-inject proposal framing. The correction: dispatch prompts for design-decision work MUST NOT include "Brien is the decider," "status: proposed," or "your answers are PROPOSALS." The correct brief is: "4-gate check; if all pass, execute + signal; flag only items that genuinely fail a gate."

Layer 5 (autonomy-grant-dispatch-prompt-check.sh) catches this at PreToolUse time — before the subagent consumes tokens.

**Override token:** when a dispatch prompt genuinely needs proposal framing (L0 gate — external human review, Chris consent, cross-org legal), include:
```
# AUTONOMY-OVERRIDE-PROPOSAL-FRAMING-INTENTIONAL: <justification>
```
This suppresses the hook and logs the override.

---

### 4. Sibling-Architecture Closure Scope

**Pattern:** Close a build at the scope of its substantive contribution. Sibling capabilities that surfaced during the build — but whose notice, design, and implementation are independent — are NOT part of this build's closure. They are new IDD loops with their own Notice signals.

**The scope-creep trap:** When Plan C (a sibling capability) surfaces during a build of Plan A + B, the default instinct is to hold the build's Observe stage open until Plan C completes. This conflates the build's contribution with the sibling's progress. Per WS-DDR-025 (sibling-over-parent-child): close Plan A+B at its substantive contribution scope; open a separate IDD loop for Plan C.

**Structural wholeness assertion:** A build is structurally whole when its own plans have landed, its own gates have passed, and its own catch-nets are active. A sibling capability's readiness does not determine structural wholeness.

**What to record in the close signal:** name all sibling IDD loops opened during the session, with pointers to their Notice signals, but explicitly mark them as NOT part of this build's closure.

---

### 5. TDD/SDD Double Discipline

**Pattern:** Two disciplines operate at two levels simultaneously.

**Strict red-green TDD inside agents:** Every task gets a failing test on record before the implementation lands. "Red-on-record before green" is not optional. An empty commit with a false message (F7 blemish) is worse than no commit — it corrupts the git record.

**Subagent-driven-development at the dispatch layer:** Independent plan steps run in parallel agents with independent worktrees or branches. Dependent steps sequence. The implementer-escalation contract per plan step defines what the implementer resolves autonomously vs. what escalates to the controller.

**Review findings are hypotheses, not facts (F6):** The defense-in-depth chain — reviewer → implementer-verify → controller-verify — is load-bearing. When a reviewer says "Confirmed finding," verify against actual file state before dispatching a fix agent. The cost of false-positive verification (one read) is far less than the cost of a false-positive fix (an empty commit in history that didn't change anything).

**When verification yields no change:** NO COMMIT. A note to the controller. An empty commit is never correct.

---

## Closure-DoD Checklist

For every Observe-stage close, verify each of these before flipping the trigger signal to `closed`:

```
[ ] Trigger-resolution commit identified and cited (F8 mandate)
[ ] Build contribution stated as what it actually changed (not what it coincided with)
[ ] upstream_control_path: key present in trigger signal frontmatter (literal key, not narrative)
[ ] catch_mechanism: key present in trigger signal frontmatter (literal key)
[ ] pipeline_survival: key present in trigger signal frontmatter (literal key)
[ ] All plan gates confirmed passed or explicitly carry-forwarded
[ ] Sibling IDD loops named and marked as independent (NOT part of this build)
[ ] closure_class specified (e.g., model-correction-scope, feature-scope, data-scope)
[ ] No overclaims in commit messages (especially empty commits)
[ ] Closure-discipline audit run (even if clean, the audit running is worth signaling)
```

---

## Anti-Patterns Catalog

These are the drift shapes that recur. The hooks catch the worst cases; the catalog names all variants so they're recognizable before they reach the hook.

### Proposal-framing on L4 work
**Shape:** `status: proposed`, "Brien is the decider," "Recommendation / Rationale / Alternative" blocks for decisions that pass the 4-gate check.
**Root cause:** default agent posture; subagent-prompt injection re-injecting it.
**Hook:** autonomy-grant-stop-check.sh (Stop), autonomy-grant-dispatch-prompt-check.sh (PreToolUse Agent).
**Memory:** `feedback_autonomy_grant_drift_pattern.md`, `feedback_decision_framing.md`.

### Subagent-prompt injection
**Shape:** Parent session understands autonomy posture; dispatch prompt contains "Brien is the decider — your answers are PROPOSALS."
**Root cause:** proposal-framing habit surfaces at the content layer, not the response-tone layer; Stop hook doesn't inspect dispatch-prompt content.
**Hook:** autonomy-grant-dispatch-prompt-check.sh (Layer 5).
**Memory:** `feedback_post_stage_handoff.md`.

### Pending-status default
**Shape:** Decision atoms default to `status: proposed` or `status: pending` instead of `status: ratified` after the 4-gate check passes.
**Root cause:** template default is conservative; autonomy posture doesn't override template muscle memory.
**Prevention:** Decision-atom template default should be `status: ratified`; `status: proposed` requires explicit failing-gate field.

### PR-style review on reversible work
**Shape:** "Recommendation / Rationale / Alternative / Reversibility" blocks for 10 decisions, all of which pass 4-gate. Framed as a document Brien reviews and approves.
**Root cause:** Confuses "high-quality decision document" with "decisions that require Brien's approval."
**Correction:** Execute + signal all 4-gate-passing decisions inline; only surface the genuinely L0-gated items (those that fail a gate).

### Phase-2 retrofit splits
**Shape:** "I'll design this now; implementation is a Phase 2 item" for work that is neither risky nor blocked.
**Root cause:** Autonomy-grant drift toward staged approval-seeking.
**Prevention:** If design + implementation pass the 4-gate check together, do both.

### Trigger overclaim
**Shape:** Build close signal says "this build resolved the trigger" when a prior commit actually resolved it.
**Root cause:** Diagnostic count moved to zero during the build; the movement was attributed to this build without verification.
**Correction:** F8 mandate — verify the mechanism before claiming resolution.
**Prevention:** Always run an investigation commit when a count changes unexpectedly.

---

## Three Composition Shapes

### Shape 1: Sub-loops (Plan-A then Plan-B then Plan-C then Plan-D)
Sequential plans within a single IDD loop. Plan B's entry criteria are Plan A's exit criteria. Plans accumulate toward a single Observe close. Use when plans are tightly coupled and can't run independently.

**When to use:** Substrate builds (Plan A establishes invariants; Plan B builds the extractor that uses them). The ordering is load-bearing.

**Closure:** Single trigger signal closes at the end of Plan D.

### Shape 2: Parallel plans with independent worktrees
Two plan streams running in parallel branches (`element-substrate-recursive-arb` and `recursive-arb-engine`), each with independent agents. Use when plans are independent and don't share mutable state.

**When to use:** The recursive ARB engine (Plan C) didn't depend on the element substrate's daily commits. Running it in parallel saved wall time.

**Closure:** Each worktree has its own branch. They merge when both are ready. The Observe close covers both contributions.

### Shape 3: Sibling IDD loops (build closes; capability continues independently)
A capability surfaces during a build but is substantively independent. Open a Notice signal for it; let it start its own IDD loop. The parent build closes at its own scope.

**When to use:** The peer-authored persona pipeline (§15 / Markus path) surfaced during the element-substrate build. It has its own design spec, its own Notice signal, its own future branch. The element-substrate build is structurally whole without it.

**Closure:** Parent build closes. Sibling loop starts its own arc. They reference each other via cross-links but are governed independently.

---

## Hook Registry

All 7 hooks in `Core/frameworks/intent/hooks/` are load-bearing for IDD:

| Hook | Event | What it catches |
|---|---|---|
| `autonomy-grant-check.sh` | SessionStart | Injects autonomy posture anchor before first response |
| `autonomy-grant-stop-check.sh` | Stop | Bare-choice patterns, soft-queue framing on pre-authorized continuation |
| `autonomy-grant-dispatch-prompt-check.sh` | PreToolUse (Agent) | Proposal-framing injected into subagent dispatch prompts |
| `closure-discipline-check.sh` | SessionStart | Injects closure-discipline posture anchor before first response |
| `closure-discipline-stop-check.sh` | Stop | Completion-claim language without upstream-control mention |
| `closure-discipline-signal-check.sh` | PreToolUse (Write/Edit) | Signal files with `status: resolved` missing triad keys |
| `skill-intake-gate-check.sh` | PreToolUse (Agent) | Build-intake gate — prevents unauthorized skill builds |

---

## Cross-Links

- **Autonomy-grant enforcement spec:** `Core/frameworks/intent/spec/autonomy-grant-enforcement.md`
- **Closure-discipline enforcement spec:** `Core/frameworks/intent/spec/closure-discipline-enforcement.md`
- **Signal stream DoD:** `Core/frameworks/intent/spec/signal-stream.md`
- **Sibling architecture:** WS-DDR-025 (`Workspaces/.context/DECISIONS.md`)
- **Cross-product applicability:** `Core/frameworks/intent/playbooks/cross-product-applicability.md` (sibling)
- **Process drift catalog:** `Core/frameworks/intent/learnings/process-drift-catalog.md` (sibling)
- **Source build learnings:** `Core/products/cast/.worktrees/element-substrate-recursive-arb/.intent/learnings/2026-05-19-element-substrate-build-F1-F13.md`
