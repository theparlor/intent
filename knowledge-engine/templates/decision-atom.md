---
title: Decision Atom — Template
id: TEMPLATE-DECISION-ATOM
type: template
created: 2026-05-20
updated: 2026-05-20
depth_score: 4
depth_signals:
  file_size_kb: 7.7
  content_chars: 6109
  entity_count: 0
  slide_count: 0
  sheet_count: 0
  topic_count: 0
  has_summary: 0
vocab_density: 0.16
status: canonical
origin: brien-original
upstream_control_path: "Core/frameworks/intent/knowledge-engine/templates/decision-atom.md (this file) + Layer 5 hook (autonomy-grant-dispatch-prompt-check.sh) blocks dispatch prompts that instruct subagents to produce status:proposed atoms on 4-gate-passing work"
catch_mechanism: "Layer 4 Stop hook catches proposal-framing in parent-session response text; Layer 5 dispatch hook catches proposal-framing injected into subagent prompts before dispatch; this template's default status:ratified + required gate_failure field for non-ratified atoms makes drift visible at the artifact level"
pipeline_survival: "decision atoms produced from this template carry the 4-gate frontmatter; any future audit of .intent/decisions/ directories will find ratified atoms with verifiable gate records; non-ratified atoms are distinguishable by the presence of gate_failure"
related_specs:
  - Core/frameworks/intent/spec/autonomy-grant-enforcement.md
  - Core/frameworks/intent/spec/closure-discipline-enforcement.md
related_hooks:
  - Core/frameworks/intent/hooks/autonomy-grant-dispatch-prompt-check.sh
  - Core/frameworks/intent/hooks/autonomy-grant-stop-check.sh
related_signals:
  - SIG-PROCESS-DRIFT-PR-STYLE-REVIEW-2026-05-19 (the drift event that motivated this template)
related_examples:
  - Core/products/cast/.worktrees/element-substrate-recursive-arb/.intent/decisions/2026-05-19-peer-authored-pipeline-section-11-answer-drafts.md
---
# Decision Atom — Template

## What This Template Is

A decision atom is a **ratified record of a design choice** — not a proposal, not a question, not a PR-review recommendation. The default output of any decision process where all 4 autonomy-grant gates pass is `status: ratified`.

**ANTI-PATTERN ALERT — READ BEFORE USING:**

<!-- AUTONOMY-OVERRIDE-PROPOSAL-FRAMING-INTENTIONAL: template documents anti-pattern as content; subagent output defaults status: ratified -->

The recurring drift pattern (SIG-PROCESS-DRIFT-PR-STYLE-REVIEW-2026-05-19) is: producing decision atoms with `status: proposed` and "Recommendation / Rationale / Alternative / Reversibility" PR-review blocks for work that passes the 4-gate check. This is exactly inverse to the autonomy grant.

If you find yourself writing PR-style review framing — `status: proposed`, "Brien is the decider," "for Brien's review," recommendations-as-options-awaiting-approval — STOP. Run the 4-gate check. If all 4 pass, the correct action is `status: ratified`.

<!-- End anti-pattern documentation -->

### The 4-Gate Check

1. **Reversible?** — can the decision be walked back without external side effects?
2. **Local blast?** — does the decision affect only Workspaces-local artifacts (not external humans, external systems, money)?
3. **Precedent?** — has a similar decision been made before, OR does an explicit autonomy grant cover this class?
4. **No info gap?** — is there no missing information that only Brien can supply?

**All 4 pass → `status: ratified`**. Populate `ratified_at` and `ratified_by`. Do not propose.

**Any gate fails → `status: deferred` or `status: awaiting-input`** with a `gate_failure:` field naming WHICH gate failed and exactly why. Do not default the whole decision to proposed because one input is missing.

---

## Template — Copy from here

---

```markdown
---
title: "[Decision title — imperative, specific]"
id: [DECISION-ATOM-YYYYMMDD-slug or project-specific ID scheme]
type: decision-atom
created: YYYY-MM-DD
scope: [product or engagement path the decision governs]
status: ratified
ratified_at: YYYY-MM-DD
ratified_by: "[agent slug or session ID] (4-gate pass: reversible / local / precedent / no info gap)"
gate_check:
  reversible: pass  # or: fail — [reason]
  local: pass       # or: fail — [reason]
  precedent: pass   # or: fail — [reason]
  info_gap: pass    # or: fail — [reason; which person/artifact is the source of truth]
upstream_control_path: [path to the mechanism that enforces this decision going forward — spec section, invariant ID, chain_audit check, hook, or schema field]
catch_mechanism: [what catches future violations of this decision class]
pipeline_survival: [how this decision survives render cycles, merges, and future edits]
---

# Decision: [Title]

> Ratified [YYYY-MM-DD]. All 4 autonomy-grant gates pass. Implementation can proceed.
> To revise: edit this atom + update any dependent specs. No Brien approval needed for L4-reversible changes.

## Context

[Why this decision is needed now. What forces are at play. Reference the spec section, trigger signal, or build artifact that raised this question. 3–5 sentences max.]

## Decision

[What was decided. Specific and concrete. Imperative: "Use X" not "Consider using X."]

## Scope

[What this decision governs. What it explicitly does NOT govern (out-of-scope / sibling decisions handled separately).]

## Alternatives Not Taken

| Alternative | Why not chosen | Reversibility if revisited |
|-------------|----------------|---------------------------|
| [Option A]  | [Reason]       | [L2/L3/L4]               |
| [Option B]  | [Reason]       | [L2/L3/L4]               |

## Reversibility

[L2 / L3 / L4 — with specific re-engagement cost if reversing. What would have to change if this is wrong.]

## Ratification Action

[What this ratification immediately unblocks. What the next step is. If applicable: what commit SHA or signal captures the ratification.]

---

## Non-Ratified Status (use only when a gate fails)

If any gate fails, replace the frontmatter above with:

```yaml
status: deferred  # or: awaiting-input, awaiting-external-gate
gate_failure:
  gate: [reversible | local | precedent | info_gap]
  reason: "[Specific reason this gate fails. Name the missing artifact, person, or external dependency.]"
  unblocked_by: "[What must happen for this gate to pass — specific, not vague]"
```

Do NOT use `status: proposed` as a default. "Proposed" implies a recommendation awaiting approval. That framing is only valid when Brien's explicit review is the required gate (e.g., client-facing communication, financial commitment, external-party consent). Name the gate explicitly.
```

---

## Concrete Example

The concrete reference for this template is:

`Core/products/cast/.worktrees/element-substrate-recursive-arb/.intent/decisions/2026-05-19-peer-authored-pipeline-section-11-answer-drafts.md`

That document was originally produced as `status: proposed` with per-question PR-review blocks. The dispatch prompt instructed the agent to use proposal framing — "Brien is the decider, your answers are PROPOSALS." All 10 decisions passed the 4-gate check. The atom was corrected inline to `status: ratified`. See `SIG-PROCESS-DRIFT-PR-STYLE-REVIEW-2026-05-19.md` for the full drift mechanism and correction record.

The corrected atom demonstrates:
- `status: ratified` with `ratified_at` and `ratified_by` (agent + gate-pass basis)
- `chris_runtime_input_only:` as the correctly-scoped field for genuinely-deferred items (Chris's consent values — not design choices)
- `unblocked_by_ratification:` listing what immediately becomes executable
- No "Recommendation / Alternative / Brien to decide" framing — those are replaced with "Decision / Alternatives Not Taken / Ratification Action"

## File Naming Convention

`YYYY-MM-DD-[slug].md` in the `.intent/decisions/` directory of the relevant product or worktree.

For Workspaces-level decisions: `Workspaces/.context/DECISIONS.md` (append DDR format) or standalone at `Workspaces/.context/decisions/WS-DDR-NNN-[slug].md`.
