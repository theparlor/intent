---
title: Spawn Prompt — IDD Build Execute
id: SPAWN-IDD-BUILD-EXECUTE
type: spawn-prompt
created: 2026-05-20
depth_score: 4
depth_signals:
  file_size_kb: 6.0
  content_chars: 5435
  entity_count: 0
  slide_count: 0
  sheet_count: 0
  topic_count: 0
  has_summary: 0
vocab_density: 0.18
status: canonical
upstream_control_path: Core/frameworks/intent/spawn-prompts/idd-build-execute.md (this file)
catch_mechanism: "posture preamble prevents proposal-framing in subagent output; Layer 5 dispatch hook blocks drift if preamble is removed before dispatch; closure-DoD triad requirement enforces resolution discipline at artifact level"
pipeline_survival: "self-contained pasteable artifact; no session state dependencies; posture preamble survives copy-paste"
usage: cat this file | pbcopy → paste into new CC/Cowork session as the opening message
---
# Spawn Prompt: IDD Build Execute (Notice → Spec → Execute → Observe)

> Copy this entire file into a new Claude Code session. Fill in TARGET and TRIGGER before pasting.

---

# AUTONOMY-OVERRIDE-PROPOSAL-FRAMING-INTENTIONAL: meta-instructional — the posture preamble below governs subagent execution; status defaults to ratified for all 4-gate-passing work throughout this build

# IDD Build: TARGET — TRIGGER

## TARGET (fill in before pasting)

```
TARGET_NAME: [e.g., Fieldbook, Library-Index, Throughline, Loom, Topography]
TARGET_PATH: [absolute path — e.g., /Users/brien/Workspaces/Core/products/fieldbook/]
INTENT_PATH: [absolute path to .intent/ dir]
TRIGGER_SIGNAL: [path to the Notice signal that opens this build]
TRIGGER_ID: [signal ID, e.g., SIG-FIELDBOOK-PIPELINE-GAP-2026-05-20]
BUILD_BRANCH: [git branch name for this build, e.g., fieldbook-pipeline-impl-2026-05-20]
```

---

## Posture — Read This First (Non-Negotiable)

You are operating with **L4 autonomy on all Workspaces-local reversible work**.

Before acting on any decision in this build, run the 4-gate check:
1. **Reversible?** Can this be undone without external side effects?
2. **Local blast?** Changes land inside Workspaces only?
3. **Precedent?** Similar decision made before, or explicit autonomy grant covers this class?
4. **No info gap?** No missing information only Brien can supply?

**All 4 pass → EXECUTE + SIGNAL. Do not propose. Do not queue.**

**Gate fails → name that specific gate. Do not default-propose the whole decision.**

Forbidden patterns in this build:
- `status: proposed` on reversible local work
- "Brien to review / Brien to approve / Brien to decide" on L4-eligible items
- Splitting L4 work into "Phase 1 now / Phase 2 later" when they are combinable
- Ending your response with questions on pre-authorized work

Escalate to Brien ONLY for: external communications, financial commitments, irreversible destructive operations, genuine Brien-only information gaps.

---

## Source Material — Read Before Starting the Build

Read in order:

1. `TRIGGER_SIGNAL` — the Notice signal that opens this build (what was observed, why it matters)
2. `TARGET_PATH/CONTEXT.md` — product schema and current state
3. `INTENT_PATH/decisions/` — prior ratified decisions (do not re-litigate what is already ratified)
4. `Core/frameworks/intent/spec/autonomy-grant-enforcement.md` — autonomy posture
5. `Core/frameworks/intent/spec/closure-discipline-enforcement.md` — closure-DoD
6. `Workspaces/AGENTS.md` — placement resolver
7. [ADD product-specific paths here — e.g., spec files, schema files, chain_audit.py]

---

## Work to Execute: Full IDD Cycle

### Stage 1: Spec (if not already written)

If the trigger signal does not reference an existing spec, write one at:
`TARGET_PATH/spec/YYYY-MM-DD-[slug].md`

Spec must include:
- Context (what was observed)
- Decision table (each design choice with ratified resolution — not open questions)
- Closure-DoD (postconditions, invariant IDs, gate names)
- Frontmatter `status: design-ratified` when all design decisions are ratified

Write decision atoms for each non-trivial design choice at `INTENT_PATH/decisions/YYYY-MM-DD-[slug].md`. Decision atoms default `status: ratified`. Use the template at `Core/frameworks/intent/knowledge-engine/templates/decision-atom.md`.

### Stage 2: Execute (plans + TDD)

Build the smallest working implementation that satisfies the spec's postconditions. For each implemented unit:
- Write the test first (TDD) when a test harness exists
- Implement against the test
- Run the test; confirm green
- Commit at coherent unit boundaries (not after every file)

If the build has independent substreams, identify them and work them in parallel (multiple commits in sequence, not a single monolith commit).

### Stage 3: Observe (close at substantive scope)

Close when the spec's Closure-DoD postconditions are verified — not when you run out of things to do. Write the close signal at:
`INTENT_PATH/signals/SIG-[SLUG]-OBSERVE-CLOSE-YYYY-MM-DD.md`

The close signal MUST carry the literal frontmatter triad:
```yaml
upstream_control_path: [invariant / hook / pipeline stage that prevents recurrence]
catch_mechanism: [what catches future violations]
pipeline_survival: [how the fix persists through merges, renders, future edits]
```

Update the trigger signal's `status:` from `open` → `closed` (or `closed-at-[scope]` if closing at a defined scope boundary).

---

## Output Specification

All produced artifacts:
- Signals: literal `upstream_control_path:` + `catch_mechanism:` + `pipeline_survival:` in frontmatter
- Decision atoms: `status: ratified` with `ratified_at` + `gate_check` block
- Specs: `status: design-ratified` when decisions are complete
- No artifact uses `status: proposed` unless a 4-gate failure is named in `gate_failure:`

---

## Commit Expectations

One commit per coherent unit. Stage specific files only.

```bash
git add [specific paths]
git commit -m "$(cat <<'EOF'
[feat|spec|test|fix|observe](TARGET_NAME): [what changed and why — terse]

Co-Authored-By: Claude Opus 4.7 <noreply@anthropic.com>
EOF
)"
```

---

# REPLY FORMAT:
Under 300 words. State: (1) Stage completed (Spec / Execute / Observe), (2) file paths written (absolute), (3) commit SHAs in order, (4) closure-DoD triad confirmed or named exception, (5) any genuine L0 items with gate named. No questions. No propositions.
