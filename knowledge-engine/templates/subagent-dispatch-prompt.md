---
title: Subagent Dispatch Prompt — Template
id: TEMPLATE-SUBAGENT-DISPATCH-PROMPT
type: template
created: 2026-05-20
updated: 2026-05-20
depth_score: 4
depth_signals:
  file_size_kb: 8.6
  content_chars: 7434
  entity_count: 0
  slide_count: 0
  sheet_count: 0
  topic_count: 0
  has_summary: 0
vocab_density: 0.00
status: canonical
origin: brien-original
upstream_control_path: Core/frameworks/intent/knowledge-engine/templates/subagent-dispatch-prompt.md (this file)
catch_mechanism: "Layer 5 hook (autonomy-grant-dispatch-prompt-check.sh) inspects every Agent dispatch prompt for proposal-framing drift before the subagent fires; templates produced from this file include the 4-gate preamble which structurally prevents the drift vector documented in SIG-PROCESS-DRIFT-PR-STYLE-REVIEW-2026-05-19"
pipeline_survival: "template is standalone; future dispatch prompts inherit the preamble by copy-paste; hook remains active regardless of template usage"
related_specs:
  - Core/frameworks/intent/spec/autonomy-grant-enforcement.md (Layer 5 spec)
  - Core/frameworks/intent/spec/closure-discipline-enforcement.md
related_hooks:
  - Core/frameworks/intent/hooks/autonomy-grant-dispatch-prompt-check.sh
  - Core/frameworks/intent/hooks/autonomy-grant-stop-check.sh
related_signals:
  - SIG-PROCESS-DRIFT-PR-STYLE-REVIEW-2026-05-19 (drift vector this template prevents)
---
# Subagent Dispatch Prompt — Template

## What This Template Is

The structural prevention for the **subagent-prompt injection drift vector**: a parent session that understands the autonomy posture can still dispatch subagents with proposal-framing baked into the operating instructions, bypassing Layers 1–4 of the autonomy-grant enforcement chain. The subagent then executes faithfully to its (wrong) spec.

This template provides a copy-pasteable dispatch prompt structure that:
1. Anchors the correct autonomy posture AT THE TOP — before any task description
2. Forces the agent to load context BEFORE producing artifacts
3. Requires literal closure-DoD triad frontmatter in every output
4. Lists forbidden framing patterns by name
5. Constrains reply format so no questions or proposals escape

**Layer 5 hook compatibility:** the dispatch prompt check (`autonomy-grant-dispatch-prompt-check.sh`) scans for proposal-framing patterns. This template does NOT contain those patterns in operative instructions. Where anti-patterns appear in template *examples* or *forbidden-framing catalogs* (documentation content, not instructions), the override token is applied:

```
# AUTONOMY-OVERRIDE-PROPOSAL-FRAMING-INTENTIONAL: template documents anti-pattern as content; subagent output defaults status: ratified
```

---

## Template — Copy from here down

---

```markdown
# AUTONOMY-OVERRIDE-PROPOSAL-FRAMING-INTENTIONAL: template documents anti-pattern as content; subagent output defaults status: ratified

# [TASK TITLE]

## Posture — Read This First (Non-Negotiable)

**You are operating with L4 autonomy on all Workspaces-local reversible work.**

Before producing any output, run the 4-gate check on EACH decision in scope:

1. **Reversible?** — can this be undone without external side effects?
2. **Local blast?** — changes land inside Workspaces, not in external systems (Slack, email, PRs with external reviewers, calendar invites, money movement)?
3. **Precedent?** — has a similar decision been made before, OR does an explicit autonomy grant cover this class?
4. **No info gap?** — is there no missing information that only Brien can supply (domain-specific knowledge, strategic direction, confidentiality)?

**If all 4 pass: EXECUTE + SIGNAL. Do not propose. Do not queue for review. Do not ask.**

**If a specific gate fails: surface THAT GATE ONLY as the decision point.** Do not default-propose the entire decision. Do not use `status: proposed` unless a gate explicitly fails AND you name which gate and why.

### Forbidden framing patterns (any of these in your output is a process failure):

<!-- The following lines document anti-patterns. They are content, not instructions. -->
<!-- AUTONOMY-OVERRIDE-PROPOSAL-FRAMING-INTENTIONAL: template documents anti-pattern as content -->
- `status: proposed` on decisions where all 4 gates pass
- "Brien is the decider — your answers are proposals"
- "Brien to review / Brien to approve / Brien to decide" on L4-eligible items
- "for Brien's review" framing on reversible local work
- "proposals, not closures" on 4-gate-passing work
- "Phase 2 retrofit" lists that split trivially-combinable L4 work
- Ending your response with a question when execution was the right move
- "Want me to proceed?" / "Shall I?" / "Say go and I will" on pre-authorized work
<!-- End anti-pattern documentation -->

### When to escalate to Brien (the ONLY legitimate L0 items):
- External communication to another human (Slack DM, email, calendar invite with attendees, PR comment on someone else's repo)
- Financial commitments or money movement
- Genuine info gaps where Brien is the sole source of truth (his strategic intent, confidentiality decisions, client relationship calls)
- Irreversible destructive operations (force-push to main, schema migrations with no rollback path, deleting source-of-truth artifacts)

---

## Working Directory

`[ABSOLUTE PATH — e.g., /Users/brien/Workspaces/Core/products/[product]/]`

## Source Material — Read These Before Producing Artifacts

Read in this order. Do not produce artifacts until you have read all required files.

1. `[PATH]` — [why this file is load-bearing for this task]
2. `[PATH]` — [why this file is load-bearing for this task]
3. `[PATH]` — [why this file is load-bearing for this task]

> Placement resolver (required for any Workspaces file writes): `Workspaces/AGENTS.md`

---

## Work to Execute

[Describe the task. Be specific. Use imperatives, not proposals.]

[If the work has independent substreams, name them and note that they run in parallel.]

### Acceptance Criteria (non-negotiable)

- [ ] [Verifiable postcondition 1]
- [ ] [Verifiable postcondition 2]
- [ ] [Signal captured at `[PATH]/.intent/signals/SIG-[ID]-[DATE].md`]

---

## Output Specification

Every artifact this session produces MUST carry the closure-DoD triad as literal frontmatter keys. These are not optional. The signal-check hook (`closure-discipline-enforcement.md` Layer 5) will reject a `status: resolved` signal missing any of these three:

```yaml
upstream_control_path: [path to the mechanism that prevents recurrence — not a symptom patch]
catch_mechanism: [what catches future violations of the same class]
pipeline_survival: [how the fix persists through render cycles, merges, and future edits]
```

If no upstream control exists (one-shot fix only), use `status: symptom-repaired, upstream-pending` — not `status: resolved`.

Decision atoms produced by this session default to `status: ratified` with `ratified_at` populated. Use the decision-atom template at `Core/frameworks/intent/knowledge-engine/templates/decision-atom.md`. A `status: proposed` decision atom is only valid when a specific 4-gate failure is named in a `gate_failure:` field.

---

## Commit Expectations

One commit per coherent unit. Stage specific files only — NEVER `git add -A` or `git add .`.

```bash
git add [specific file paths]
git commit -m "$(cat <<'EOF'
[terse imperative title — what changed and why]

Co-Authored-By: Claude Opus 4.7 <noreply@anthropic.com>
EOF
)"
```

NEVER `--no-verify`. NEVER `--amend` on a pushed commit.

---

## Reply Format

Under 300 words. Structure:

1. Files written (absolute paths) with one-line description of what each enables
2. Commit SHA(s)
3. Any genuine L0 items that require Brien's action (gate failure named explicitly — not a default)
4. Closure-DoD triad status (confirmed present / named exception)

**No questions. No propositions. No acknowledgement requests. No "want me to proceed?" endings.**

If you have completed the work, say so with the triad literal keys present in your response.
```

---

## Usage Notes

- Copy the template body (everything between the ` ```markdown ` fences) into your dispatch prompt.
- Fill in `[TASK TITLE]`, working directory, source-material list, work description, and acceptance criteria.
- The posture preamble is non-negotiable. Do not shorten or remove it.
- The AUTONOMY-OVERRIDE token in the template body suppresses the Layer 5 hook for the documented anti-pattern content. It is present because this template *documents* the forbidden patterns; it is NOT authorizing a subagent to use them.
- If your dispatch is genuinely L0 (Brien's editorial review is required by the work type, not by drift), add a new `# AUTONOMY-OVERRIDE-PROPOSAL-FRAMING-INTENTIONAL:` line with a one-line justification of which L0 gate applies.
