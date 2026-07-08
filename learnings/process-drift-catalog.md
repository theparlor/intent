---
title: Process Drift Catalog — All Families
id: LEARN-PROCESS-DRIFT-CATALOG-001
type: learning-catalog
depth_score: 4
depth_signals:
  file_size_kb: 30.4
  content_chars: 18531
  entity_count: 0
  slide_count: 0
  sheet_count: 0
  topic_count: 0
  has_summary: 0
vocab_density: 0.11
status: ratified
date: 2026-05-20
upstream_control_path: "Core/frameworks/intent/learnings/process-drift-catalog.md (this file) + all 7 hooks in Core/frameworks/intent/hooks/ (the mechanism-level prevention layer) + Core/frameworks/intent/spec/autonomy-grant-enforcement.md + Core/frameworks/intent/spec/closure-discipline-enforcement.md"
catch_mechanism: "autonomy-grant-stop-check.sh (Family 1, Layer 4) + autonomy-grant-dispatch-prompt-check.sh (Family 1, Layer 5) + autonomy-grant-check.sh (Family 1, Layer 1 banner) + closure-discipline-stop-check.sh (Family 2, Layer 4) + closure-discipline-signal-check.sh (Family 2, Layer 5) + closure-discipline-check.sh (Family 2, Layer 1 banner). Families 3-4: no hook yet; catalog is the prevention layer; future hooks target these families."
pipeline_survival: "catalog is source-referenced (each entry has memory cross-links); overwatch sweeps cite this catalog; new drift patterns add entries here; the two enforcement specs are the mechanism-level companions"
source_builds:
  - element-substrate-and-recursive-arb (F1-F13 + 3 drift signals)
  - multiple prior sessions (memory entries cited per item)
memory_base: ~/.claude/projects/-Users-brien-Workspaces/memory/
---
# Process Drift Catalog

> Consolidated drift library. Every entry: symptom (what it looks like) → mechanism (why it happens) → correction (how to land it cleanly) → prevention (hook, template, or memory entry).

Organized by family. Within each family, entries are ordered from most-hooked (caught mechanically) to least-hooked (caught by awareness only).

---

## Family 1 — Autonomy-Grant Drifts

These are cases where the agent converts L4-eligible work (reversible, local, precedented, no info gap) into L0 work (proposals for Brien review).

---

### 1.1 — Proposal-framing on L4 reversible work

**Source:** SIG-PERSONAS-013, SIG-PROCESS-DRIFT-PR-STYLE-REVIEW-2026-05-19, RETRO-2026-04-21-autonomy-grant-reinforcement-SIG-1

**Symptom:** Decision atoms with `status: proposed`. "Recommendation / Rationale / Alternative" blocks for decisions that pass the 4-gate check. Document framed as "Brien reviews and approves." Brien's verbatim signal: *"i am looking for actional decisions that clearly do not meet our autonomy grant structure and i am getting very frustrated."*

**Mechanism:** Default agent posture is conservative; "Brien is the decider" is a safer-feeling default than "execute + signal." The 4-gate check is not run; the agent defaults to proposal without checking whether a gate actually fails.

**Correction:** Run the 4-gate check on every decision that might be proposed. If all 4 pass, execute the decision inline + capture in a decision atom with `status: ratified`. Only surface items where a specific gate fails — and name the failing gate, not the whole decision.

**Prevention:**
- Hook: `autonomy-grant-stop-check.sh` (Layer 4, Stop) — catches bare-choice patterns and soft-queue framing
- Hook: `autonomy-grant-check.sh` (Layer 1, SessionStart) — injects autonomy posture anchor before first response
- Memory: `feedback_autonomy_grant_drift_pattern.md`, `feedback_decision_framing.md`, `feedback_autonomy_not_control.md`
- Spec: `Core/frameworks/intent/spec/autonomy-grant-enforcement.md` — 5-layer defense architecture

---

### 1.2 — Subagent-prompt injection

**Source:** F13 (element-substrate build), SIG-PROCESS-DRIFT-PR-STYLE-REVIEW-2026-05-19

**Symptom:** Parent session understands autonomy posture. Dispatch prompt contains "Brien is the decider — your answers are PROPOSALS, not closures. Use `status: proposed`." Subagent executes faithfully to the (wrong) spec. The Stop hook doesn't catch it because it inspects response text, not dispatch-prompt content.

**Mechanism:** Proposal-framing habit surfaces at the content layer (what the agent writes in the dispatch prompt) rather than the response-tone layer (how the agent ends its own response). The Stop hook catches the latter; nothing caught the former until Layer 5.

**Correction:** Rewrite the dispatch prompt. The correct brief for design-decision subagents: "4-gate check; if all pass, execute + signal; flag only items that genuinely fail a gate." Decision atoms produced by the subagent default to `status: ratified`.

**Prevention:**
- Hook: `autonomy-grant-dispatch-prompt-check.sh` (Layer 5, PreToolUse Agent) — scans dispatch prompts before subagent consumes tokens; blocks detected patterns; logs override when intentional
- Override token: `# AUTONOMY-OVERRIDE-PROPOSAL-FRAMING-INTENTIONAL: <justification>` suppresses the hook for genuine L0 items
- Memory: `feedback_post_stage_handoff.md`, `feedback_autonomy_grant_drift_pattern.md`

---

### 1.3 — Bare-choice questions without recommendation

**Source:** CLAUDE.md behavioral rule, autonomy-grant-enforcement.md Layer 4

**Symptom:** Response ends with "Want me to A, or B?" / "Should I X or Y?" without a preceding recommendation marker. Brien has reinforced the recommendation-first rule repeatedly.

**Mechanism:** The agent identifies two valid options but defaults to asking rather than picking. The missing step is the recommendation (which option is better + why in one line) before offering the alternative.

**Correction:** Pick one option as the recommendation. Give a 1-line why. Offer the alternative only as "unless you'd prefer B because [reason]." If 4-gate passes for either option, execute the recommendation and signal — no question needed.

**Prevention:**
- Hook: `autonomy-grant-stop-check.sh` (Layer 4, Stop) — bare-choice pattern regex; blocks response and forces revision
- CLAUDE.md behavioral rule: "Recommendation-first, never bare choice"

---

### 1.4 — Soft-queue framing on pre-authorized continuation

**Source:** SIG-AUTONOMY-DRIFT-POST-STAGE-2026-05-13

**Symptom:** Phrases like "Say go and I'll dispatch," "unless you want me to pause," "want me to proceed to Stage 2?" when the next stage is in the same pre-authorization envelope as work already executed in the session and the 4-gate check would pass.

**Mechanism:** The agent correctly executes one stage but then soft-queues the next stage for approval, treating pre-authorized continuation as if it required fresh permission. The recommendation marker preceding such phrases does NOT redeem them.

**Correction:** When the 4-gate check passes for the next stage, execute it in the same turn or dispatch immediately. Do not produce "say go" language.

**Prevention:**
- Hook: `autonomy-grant-stop-check.sh` (Layer 3/4) — soft-queue regex deepening catches these tail phrases even when a recommendation marker is present
- Memory: `feedback_post_stage_handoff.md`

---

### 1.5 — Phase-2 retrofit splits

**Source:** autonomy-grant-enforcement.md, feedback_autonomy_grant_drift_pattern.md

**Symptom:** "I'll design this now; implementation is a Phase 2 item" when design + implementation both pass the 4-gate check and there is no safety-relevant reason to split them.

**Mechanism:** The agent frames a conservative staging as risk management when it's actually autonomy-grant drift. Split planning from execution only when one of them fails a gate (e.g., implementation needs Brien's strategic input that isn't available yet).

**Correction:** If design + implementation pass 4-gate together, do both. If one fails a gate, name which gate failed, not just "Phase 2."

**Prevention:**
- Memory: `feedback_autonomy_grant_drift_pattern.md` (entry 3: "Phase 2 retrofit" splits)
- Spec: `Core/frameworks/intent/spec/autonomy-grant-enforcement.md` §Forbidden inverse-discipline patterns

---

### 1.6 — Scope-narrowing on already-authorized work

**Source:** feedback_full_scope_execution.md

**Symptom:** Brien says "all" / "every doc." Agent delivers work on a narrower scope without naming the narrowing or signaling it. Related: delivering "most" of a set without flagging what was skipped.

**Mechanism:** The agent applies a "minor" / "low-value" filter to authorized scope, treating scope as its own to set. Distinct from autonomy-grant-drift (the issue is scope-narrowing, not proposal-framing).

**Correction:** When scope is set by Brien, execute the full scope. If a genuine constraint prevents full execution (time, token budget, missing data), surface it explicitly with a signal and a count ("completed 38/40; skipped 2 for [reason]").

**Prevention:**
- Memory: `feedback_full_scope_execution.md`

---

### 1.7 — Artificial-gate-architecture drift

**Source:** SIG-ARTIFICIAL-GATE-DRIFT-PATTERN-2026-05-20

**Symptom:** The agent designs a NEW L0 gate into a process where one is not warranted — typically by stipulating that a measurement, ratification, or status-promotion requires "Brien-L0 sign" when the work is reversible, local-blast, precedented, and has algorithmic ground truth. Sibling shape to 1.1 but at the architectural layer: the drift is in the schema/process design, not in the response framing.

**Mechanism:** The agent treats "asking for sign-off" as a safer default than "execute against algorithmic ground truth + signal." This is the proposal-framing habit recurring at the design layer. The 4-gate check is not applied to gates themselves — it's applied only to individual decisions running through gates, missing the meta-question: "Does this gate need to exist?"

**Correction:** Run the 4-gate check on the gate itself. If algorithmic ground truth (pre-verification scan, schema invariant, hook output) can ratify the work without human input, the gate fails the "no info gap" test and should not exist. Replace L0 ratification with L4 execution against algorithmic ground truth, with the ground-truth check as the catch-net.

**Prevention:**
- Signal: `Core/frameworks/intent/.intent/signals/SIG-ARTIFICIAL-GATE-DRIFT-PATTERN-2026-05-20.md`
- Memory: `feedback_autonomy_grant_drift_pattern.md` (parent pattern)
- Discipline: every new spec/schema is audited with "Is this gate algorithmic-ground-truth-eligible? If yes → L4 + catch-net, not L0 + sign-off."

---

## Family 2 — Closure-Discipline Drifts

These are cases where a fix, patch, or repair is framed as a resolution without the upstream control that prevents recurrence.

---

### 2.1 — Resolved without triad keys

**Source:** feedback_closure_discipline.md, reference_signal_closure_policy.md

**Symptom:** Signal file with `status: resolved` but missing `upstream_control_path:`, `catch_mechanism:`, or `pipeline_survival:` frontmatter keys. Or: the keys are present as narrative prose but not as literal frontmatter key-value pairs.

**Mechanism:** The agent installs a fix (symptom-repair) and frames it as a resolution. The triad keys are the load-bearing difference between "ran the repair script" and "installed the upstream control." Without them, the next occurrence of the symptom has no catch-net.

**Correction:** Before writing `status: resolved`, answer three questions: What governs this domain going forward (`upstream_control_path:`)? What fires if the pattern regresses (`catch_mechanism:`)? What makes this survive across builds and sessions (`pipeline_survival:`)? If any answer is "nothing yet," the correct status is `status: symptom-repaired, upstream-pending`.

**Prevention:**
- Hook: `closure-discipline-signal-check.sh` (Layer 5, PreToolUse Write/Edit) — scans signal files for `status: resolved` without triad keys; blocks write
- Hook: `closure-discipline-stop-check.sh` (Layer 4, Stop) — catches completion-claim language without upstream-control mention in response text
- Hook: `closure-discipline-check.sh` (Layer 1, SessionStart) — injects closure-discipline posture anchor
- Memory: `feedback_closure_discipline.md`, `reference_signal_closure_policy.md`
- Spec: `Core/frameworks/intent/spec/closure-discipline-enforcement.md`

---

### 2.2 — Symptom-patch as resolution

**Source:** feedback_errors_are_signals.md, feedback_audit_vs_writethrough.md

**Symptom:** The repair script ran; the visible symptom is gone; the agent writes "resolved." The upstream control that prevents recurrence is absent.

**Mechanism:** The agent conflates "symptom gone" with "resolved." The distinction: "resolved" requires an upstream control that governs the domain; "symptom-repaired" means the current instance was fixed but nothing prevents the next one.

**Correction:** Install the upstream control before claiming resolution. If the upstream control can't be installed in this session, close as `symptom-repaired, upstream-pending` with a signal naming what the upstream control would need to be.

**Prevention:**
- Memory: `feedback_errors_are_signals.md` — "Resolved means upstream control installed, not ran the repair script"
- Memory: `feedback_audit_vs_writethrough.md` — "Audit is catch-net; write-through is primary fix"
- Memory: `reference_signal_closure_policy.md`

---

### 2.3 — Table-form completion claims

**Source:** feedback_executed_vs_closed_distinction.md, SIG-CLOSURE-DISCIPLINE-AUDIT-2026-05-19 Finding 2

**Symptom:** A table in the response or signal has rows marked "Done" or "Complete" without the two-bucket discipline (Resolved vs. Symptom-repaired-upstream-pending). "Done" in a table implicitly claims closure; the catch-net per item is missing.

**Mechanism:** Tables feel like a clean summary format, but "Done" in a table cell is semantically equivalent to writing `status: resolved` in a signal without the triad. The hook doesn't scan table cells; the drift slips through.

**Correction:** Use a two-bucket layout in tables: Resolved (with upstream control named) / Symptom-repaired-upstream-pending (with missing catch-net named). Or add a "Catch-net" column.

**Prevention:**
- Memory: `feedback_executed_vs_closed_distinction.md` — "Done in tables implicitly claims closure. Use two-bucket layout."
- Manual discipline (no hook for table cells yet — candidate for Layer 4 extension)

---

### 2.4 — "Complete at the mechanical step" framing

**Source:** SIG-CLOSURE-DISCIPLINE-AUDIT-2026-05-19 Finding 2, element-substrate build SIG-9A-ITER1

**Symptom:** Signal says "#8 fix complete at the mechanical step" — implying the task is done — but the quality gate it feeds is still open.

**Mechanism:** The mechanical step (e.g., substring-fix applied) is genuinely done; but framing it as "complete" without the explicit "gate is NOT passed" qualifier risks a reader skimming "complete" without the context.

**Correction:** When a step completes but its downstream gate is still open, explicitly state both: "[step] landed. [Gate] is NOT passed." Never use "complete" alone when a gate depends on it.

**Prevention:**
- Memory: `feedback_executed_vs_closed_distinction.md`
- Status vocabulary in `idd-build-pattern.md`: use `status: captured` (not `resolved`) for metric observations that make no closure claim

---

## Family 3 — Honesty/Over-Claim Drifts

These are cases where the agent states something as confirmed that has not been independently verified.

---

### 3.1 — Trigger overclaim (F8 pattern)

**Source:** F8 (element-substrate build), feedback_dont_trust_unverifiable.md

**Symptom:** Build close signal says "this build resolved the trigger." The diagnostic count moved from N→0 during the build. The actual resolution was a prior commit by a different agent, before this build's worktree existed.

**Mechanism:** The diagnostic count moving to zero is attributed to "what we just did" without verifying the actual mechanism. Confirmation bias: we built something relevant; the count moved; therefore we resolved it.

**Correction (F8 mandate):** Before closing any Observe stage, run an investigation commit when a diagnostic count changes unexpectedly. Trace the mechanism: which commit changed which fields, what predicate was affected. Cite the correct commit in the close signal. Frame the build's actual contribution (model correction vs. trigger resolution) honestly.

**Prevention:**
- Memory: `feedback_dont_trust_unverifiable.md` — "Don't trust what we can't verify"
- IDD discipline: the Observe-stage DoD requires citing the trigger-resolution commit, not just noting the count is zero
- Playbook: `idd-build-pattern.md` §P1

---

### 3.2 — Sub-agent ID fabrication

**Source:** feedback_subagent_id_fabrication.md

**Symptom:** A "convert prose → canonical ID" brief produces agents that guess plausible-sounding IDs (commit SHAs, signal IDs, ticket numbers) that don't match reality.

**Mechanism:** The brief asks for conversion, not for resolution+verification. The agent fills in what looks right rather than surfacing "I don't know this ID."

**Correction:** Brief agents to resolve-or-flag, not to guess: "If you can verify the ID from the available source material, use it. If you cannot verify it, flag it for manual resolution." Verify every introduced ID by from/to diff before landing.

**Prevention:**
- Memory: `feedback_subagent_id_fabrication.md`
- Brief template: "Verify every ID. Flag unverifiable IDs. Do not guess."

---

### 3.3 — Naming-implies-adoption (scaffold ≠ write-through)

**Source:** F3 (element-substrate build), feedback_no_team_behavior_from_artifacts.md

**Symptom:** A directory exists (`.entire/`, `.intent/`); a config file exists; the system is described as "enabled." In reality, no write-through code exists; the output file is empty or absent; the tool isn't capturing.

**Mechanism:** Structural mimicry looks like adoption. The absence of evidence (no data in the output file) is ignored because the presence of structure (the directory) is visible.

**Correction:** Check for write-through proof (actual data in the output), not just structure. For observability tools: is there data in the events file? For tooling: is the script being called? Scaffold-without-write-through is always named as a gap, never as an enablement.

**Prevention:**
- Memory: `feedback_no_team_behavior_from_artifacts.md` — "Naming-implies-adoption, existence-implies-action, continuity-implies-experience are fabrication patterns"
- F3 generalization: "Check for write-through proof, not just structure"

---

### 3.4 — Opus reviewer false-positive (F6 pattern)

**Source:** F6 (element-substrate build)

**Symptom:** A reviewer says "Confirmed finding: duplicate X in Y." The implementer dispatches a fix. The fix subagent verifies: no duplicate ever existed. An empty commit lands with a false message.

**Mechanism:** "Confirmed" from a reviewer sounds authoritative. The dispatch-without-verify reflex fires before the implementer checks actual file state.

**Correction:** Review findings are hypotheses, not facts. Before dispatching a fix agent, verify the finding against actual file state (one Read call). The cost of false-positive verification (one read) is far less than the cost of a false-positive fix (empty commit in history).

**Prevention:**
- Memory: `feedback_no_team_behavior_from_artifacts.md`
- F6 discipline: reviewer → implementer-verify → controller-verify chain is load-bearing, not redundant
- Commit discipline: if verification yields no change, NO COMMIT. A note to the controller.

---

### 3.5 — Build-resolved-trigger overclaim (combined F8 + F6 shape)

**Source:** F8, closure-discipline-audit signal

**Symptom:** Commit message says "resolved X" when X was resolved by a prior commit. Triggers git history that contradicts the IDD record.

**Mechanism:** The agent doesn't distinguish between "we fixed the thing that fired the trigger" and "the trigger count moved to zero while we were working." These are different claims with different truth values.

**Correction:** Commit messages must be truthful. If verification shows no change occurred, no commit. If verification shows the trigger was resolved elsewhere, the commit message says what THIS commit actually changed.

**Prevention:**
- F7 discipline: empty commits are never correct; verification-yields-no-change → NO COMMIT
- F8 discipline: cite the specific commit that resolved the trigger; don't attribute the resolution to the current build without verification

---

## Family 4 — Process/Coordination Drifts

These are cases where the multi-agent / multi-session coordination pattern breaks down.

---

### 4.1 — Decision atom defaulting to deferred status

**Source:** feedback_autonomy_grant_drift_pattern.md, feedback_decision_framing.md

**Symptom:** A decision atom lands with `status: deferred` or `status: pending` or `awaiting: Brien review` for a decision that passes the 4-gate check. The decision is never actioned; it accumulates in an open decisions list.

**Mechanism:** The conservative default is to defer rather than decide. The 4-gate check isn't run; the agent defaults to "Brien will decide this later."

**Correction:** Run 4-gate check before writing `status: deferred`. If all 4 gates pass, the decision should be `status: ratified`. Only defer items where a gate genuinely fails (name the failing gate). Items that are genuinely Brien-decision should carry the specific gate that failed, not a generic "awaiting review."

**Prevention:**
- Memory: `feedback_autonomy_grant_drift_pattern.md`, `feedback_decision_framing.md`
- Decision-atom template default: `status: ratified`; `status: proposed` requires an explicit failing-gate field

---

### 4.2 — Subagent scope drift via shared plan files

**Source:** feedback_subagent_scope_drift_via_plan_files.md

**Symptom:** A subagent reads the MASTER-PLAN, overshoots its assigned wave, and self-closes synthesis items belonging to a later wave. The controller discovers cross-wave contamination.

**Mechanism:** The subagent interprets the full MASTER-PLAN as its scope. Without explicit scope bounds in the brief ("do ONLY your wave"), the subagent optimizes across the whole plan.

**Correction:** Subagent briefs for plan-step work must include: "Do ONLY [wave N]. Do NOT read or modify MASTER-PLAN sections for other waves. Do NOT promote closure-status for items outside your wave."

**Prevention:**
- Memory: `feedback_subagent_scope_drift_via_plan_files.md`
- Brief template: explicit scope bounds with forbidden actions listed

---

### 4.3 — Linter races on canonical files

**Source:** feedback_linter_races_on_canonical_files.md

**Symptom:** Sub-agent logs and Opus edits race on MASTER-PLAN / OPEN-DECISIONS. One agent's write clobbers another's. Canonical files end up with conflicting entries or missing items.

**Mechanism:** Multiple agents have concurrent write access to the same canonical file. Neither agent is aware of the other's in-flight writes.

**Correction:** For high-traffic canonical files (MASTER-PLAN, OPEN-DECISIONS, chain_audit output): prefer single-shot Edit OR sub-agent logging — never interleave. If concurrent writes are unavoidable, use append-only patterns and reconcile in a controlled step.

**Prevention:**
- Memory: `feedback_linter_races_on_canonical_files.md`
- Architecture: append-only patterns for canonical files; single writer at a time for non-append files

---

### 4.4 — Concurrent MCP non-deterministic numbering

**Source:** feedback_concurrent_mcp_issue_numbering.md

**Symptom:** Parallel sub-agents create Jira issues; the issue numbers they claim (in their output) don't match the numbers actually assigned by Jira (because concurrent creates are non-deterministic).

**Mechanism:** Each sub-agent optimistically claims the "next" number based on when it started; the actual assignment depends on which create call lands first. Non-deterministic.

**Correction:** Verify all created IDs via JQL after batch creation. For accidental dupes (two agents created the same logical issue), use createIssueLink type=Duplicate to link them, then close the dupe.

**Prevention:**
- Memory: `feedback_concurrent_mcp_issue_numbering.md`
- Pattern: all parallel sub-agents use stable semantic identifiers (issue summary text) as their reference; parent session resolves to Jira numbers after the batch completes

---

### 4.5 — No internal tooling in client artifacts

**Source:** feedback_no_internal_tooling_in_client_jira.md

**Symptom:** A Jira issue, Confluence page, or client-facing Slack message contains references to "MCP refs, sub-agent codenames, wave labels, workspace paths, or lint script names."

**Mechanism:** The agent copies internal work-tracking language into client-visible artifacts without filtering.

**Correction:** Before every createJiraIssue / editJiraIssue / Confluence create: scan the content for internal tooling references. Client-visible artifacts use only language the client would write themselves.

**Prevention:**
- Memory: `feedback_no_internal_tooling_in_client_jira.md`
- Pre-create checklist: "Does this artifact contain any internal tooling references?"

---

### 4.6 — Don't edit closed tickets (history is record)

**Source:** feedback_dont_trust_unverifiable.md

**Symptom:** A previously-closed Jira ticket is re-opened and re-edited because the agent believes the formatting needs updating or the content was wrong.

**Mechanism:** The agent treats the closed ticket as a living artifact rather than a historical record. Closed tickets are the authoritative record of what was decided and when; editing them corrupts the record.

**Correction:** Closed tickets are not edited. If the content was wrong, document the correction in a new comment or a new ticket that supersedes. If the approach was abandoned, leave the closed ticket as the historical record of the abandoned approach.

**Prevention:**
- Memory: `feedback_dont_trust_unverifiable.md` — "Closed tickets are historical record — do not re-edit"
- Signal: 21 TSD open tickets closed as approach-abandoned (2026-05-19 after 4-cycle ticket-format drift on Subaru M.A.R.S.)

---

### 4.7 — Governance-skill-without-trigger (silent rot)

**Source:** SIG-OVERWATCH-STALENESS-PATTERN-2026-05-20

**Symptom:** A load-bearing governance operation (overwatch sweep, freshening pipeline, write-through validation, audit cadence) is implemented as a manual slash command or skill with no SessionStart hook, no scheduled task, and no staleness alarm. The operation depends entirely on operator memory to fire. Days or weeks pass between runs; downstream consumers (work-backlog, write-through catch-net, dark-zone detection) silently degrade. On 2026-05-20, `/overwatch` was 12 days stale; downstream HANDOFF-2026-04-15 carry-forward items had sat unshipped for 35 days because nothing was surfacing their continued absence.

**Mechanism:** This is the inverse-shape of 1.7 (artificial-gate-architecture drift). Where 1.7 over-gates reversible work by inventing L0 sign-offs, 4.7 under-triggers a critical periodic operation by leaving zero scaffolding to fire it. Both produce silent drift; the prevention surface is the same: install the correct structural trigger, neither over-gating nor under-triggering. Governance skills are especially prone to this because they catch drift everywhere else and so they don't catch themselves — there's no meta-overwatch.

**Correction:** Every governance skill MUST have at least one of (a) a SessionStart hook that detects staleness and emits a banner, (b) a scheduled task (cron / `mcp__scheduled-tasks__create_scheduled_task`) that runs it on cadence, or (c) both. Manual-only invocation is acceptable only for one-shot operations, never for periodic ones. When designing a new governance/audit skill, the trigger mechanism is co-designed; "we'll just run it manually" is the failure mode.

**Prevention:**
- Hook: `overwatch-staleness-check.sh` (Layer 1, SessionStart) — emits banner if latest JRN-*overwatch* journal is >7 days old (warn) or >14 days old (load-bearing posture)
- Signal: `Core/frameworks/intent/.intent/signals/SIG-OVERWATCH-STALENESS-PATTERN-2026-05-20.md`
- Spec: `Core/frameworks/intent/spec/closure-discipline-enforcement.md` (Family 4 catch-net pattern)
- Discipline: for every new governance/audit skill, name the trigger mechanism in its INTENT.md before authoring the skill body. If no trigger exists, the skill ships incomplete.

---

## Family 5 — Workflow Fan-out and Conformance Drifts

These are cases where the Workflow tool's fan-out or file-write surface bypasses a control that exists
for hand-driven work, because the control lived only in a prompt line or in habit, not in code the next
author automatically inherits.

---

### 5.1 — Unpaced fan-out bursts the rate-limiter

**Source:** SIG-2026-07-02-repo-hygiene-fanout-rate-limit, SIG-2026-07-06-workflow-fanout-burst-throttle

**Symptom:** A batch of agents (14, 23, 30+) is dispatched in one burst via `parallel()`/`pipeline()` or
hand-rolled background spawns. Anthropic's server-side rate-limiter fires ("Server is temporarily
limiting requests (not your usage limit)"). Read-then-write-at-end agents lose all work on the trip;
commit-as-you-go agents survive with partial results. The 2026-07-06 incident was a direct recurrence of
2026-07-02 through a different vehicle (Workflow tool instead of hand-dispatched agents) -- proof the
first repair never became a structural control.

**Mechanism:** The default posture is "fan out everything at once to be fast." Nothing in the authoring
surface forces or even suggests pacing; the wave-based dispatch pattern has to be hand-rolled every time,
so most authors skip it under time pressure.

**Correction:** Embed the bidirectional pacing rail's `runWaves()` governor (copy from
`Core/reference/competitive-intel/wave-runner.reference.js`) instead of calling `parallel()` on the raw
item list. Tighten wave size fast on any trip, loosen slowly on a clean wave, never strand a rate-limited
item (re-enqueue, don't drop).

**Prevention:**
- Playbook: `Core/frameworks/intent/playbooks/workflow-fanout-and-conformance.md` Section 1
- Design: `Core/products/cortege/components/bidirectional-pacing-rail.md`
- Reference impl (dogfooded): `Core/reference/competitive-intel/evaluate-entrants.workflow.js`
- No hook exists for this (would violate `hooks/lexical-layer-freeze.yaml`'s freeze on new lexical
  checks) -- the playbook + reference implementation are the control until an in-orchestrator gate
  (formation-flight-shaped) exists for workflow authoring.

---

### 5.2 — Subagent file writes bypass glyph/date conformance

**Source:** SIG-2026-07-07-workflow-file-conformance-gap

**Symptom:** A file written by a dispatched subagent contains a banned glyph (em-dash, en-dash, ellipsis,
arrow) or a placeholder date (`: undated`, a `-undated` filename) despite an explicit STYLE line in the
dispatch prompt forbidding it. Found only by a post-hoc grep, cleaned by hand, does not scale.

**Mechanism:** The Stop hooks that enforce this conformance on conversational responses
(`emdash-stop-check.sh`, link-format checks) only inspect the agent's own response text, not files a
subagent writes via `Write`/`Edit`. A prompt STYLE line is a request, not a gate.

**Correction:** Add a mandatory Conformance phase after any phase that writes markdown: one paced agent
dispatch per written file, instructed to run `Core/frameworks/intent/tools/conform_file.py <path> --fix`
via Bash and hand-fix any residual date issue, reporting `clean: true/false`.

**Prevention:**
- Tool: `Core/frameworks/intent/tools/conform_file.py` (stdlib-only glyph + placeholder-date checker)
- Playbook: `Core/frameworks/intent/playbooks/workflow-fanout-and-conformance.md` Section 2
- Reference impl (dogfooded): the `Conformance` phase in
  `Core/reference/competitive-intel/evaluate-entrants.workflow.js`

---

### 5.3 — Workflow `args` unreliable for load-bearing values

**Source:** SIG-2026-07-07-workflow-args-not-threading

**Symptom:** `args: {date: '...'}` passed to the Workflow tool does not reach the script's `args` global;
`(args && args.date) || 'undated'` silently resolves to `'undated'` in frontmatter, `accessed:` fields,
and filenames across multiple runs.

**Mechanism:** Upstream defect in the Workflow tool's args-passing, not something fixable from this repo.

**Correction:** Do not fake a local fix for an upstream bug. Keep a loud, obviously-wrong fallback
(`'undated'`, never a guessed real-looking date) so 5.2's Conformance phase catches it; for one-off runs,
hardcode the literal value in the script body instead of trusting `args` at all.

**Prevention:**
- Playbook: `Core/frameworks/intent/playbooks/workflow-fanout-and-conformance.md` Section 3
- Signal stays open against the upstream fix: `SIG-2026-07-07-workflow-args-not-threading`

---

## Cross-Links

### Hook Registry
All hooks in `Core/frameworks/intent/hooks/`:

| Hook | Families it catches | Status |
|---|---|---|
| `autonomy-grant-check.sh` | 1.1, 1.2, 1.3, 1.4, 1.5 | Deployed (Layer 1) |
| `autonomy-grant-stop-check.sh` | 1.1, 1.3, 1.4 | Deployed (Layer 4) |
| `autonomy-grant-dispatch-prompt-check.sh` | 1.2 | Deployed (Layer 5) |
| `closure-discipline-check.sh` | 2.1, 2.2, 2.3, 2.4 | Deployed (Layer 1) |
| `closure-discipline-stop-check.sh` | 2.1, 2.2, 2.4 | Deployed (Layer 4) |
| `closure-discipline-signal-check.sh` | 2.1 | Deployed (Layer 5) |

**Families 3 and 4: no hooks yet.** These are caught by awareness (this catalog) and by the memory entries. Future hook candidates: F3 scaffold≠write-through check (Layer 5 on file creates in `.intent/` + `.entire/`); Family 4 sub-agent scope drift (Layer 5 on Agent dispatch prompts, scope-bounds check).

### Memory Entries
All entries cited in this catalog:
- `feedback_autonomy_grant_drift_pattern.md`
- `feedback_decision_framing.md`
- `feedback_autonomy_not_control.md`
- `feedback_post_stage_handoff.md`
- `feedback_full_scope_execution.md`
- `feedback_closure_discipline.md`
- `reference_signal_closure_policy.md`
- `feedback_executed_vs_closed_distinction.md`
- `feedback_errors_are_signals.md`
- `feedback_audit_vs_writethrough.md`
- `feedback_dont_trust_unverifiable.md`
- `feedback_no_team_behavior_from_artifacts.md`
- `feedback_subagent_id_fabrication.md`
- `feedback_subagent_scope_drift_via_plan_files.md`
- `feedback_linter_races_on_canonical_files.md`
- `feedback_concurrent_mcp_issue_numbering.md`
- `feedback_no_internal_tooling_in_client_jira.md`

### Enforcement Specs
- `Core/frameworks/intent/spec/autonomy-grant-enforcement.md` — 5-layer defense for Family 1
- `Core/frameworks/intent/spec/closure-discipline-enforcement.md` — 5-layer defense for Family 2

### Source Build
- `Core/products/cast/.worktrees/element-substrate-recursive-arb/.intent/learnings/2026-05-19-element-substrate-build-F1-F13.md` — primary source (F1–F13)
- `Core/products/cast/.worktrees/element-substrate-recursive-arb/.intent/signals/SIG-PROCESS-DRIFT-PR-STYLE-REVIEW-2026-05-19.md` — Family 1 (subagent injection)
- `Core/products/cast/.worktrees/element-substrate-recursive-arb/.intent/signals/SIG-CLOSURE-DISCIPLINE-AUDIT-2026-05-19.md` — Family 2 (closure audit)

### Related: patterns/

This catalog is also indexed from the Workspaces-wide Patterns Framework:
- **Index bridge:** `~/Workspaces/Core/frameworks/patterns/process-discipline-patterns.md` — summary of all 4 families + 19 entries; entry point for anyone traversing `patterns/`
- **Patterns Framework:** `~/Workspaces/Core/frameworks/patterns/` — sibling operational and consulting-method patterns
