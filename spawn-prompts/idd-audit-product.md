---
title: Spawn Prompt — IDD Audit (Product/Project)
id: SPAWN-IDD-AUDIT-PRODUCT
type: spawn-prompt
created: 2026-05-20
depth_score: 3
depth_signals:
  file_size_kb: 5.2
  content_chars: 4627
  entity_count: 0
  slide_count: 0
  sheet_count: 0
  topic_count: 0
  has_summary: 0
vocab_density: 0.22
status: canonical
upstream_control_path: Core/frameworks/intent/spawn-prompts/idd-audit-product.md (this file)
catch_mechanism: "posture preamble in prompt body prevents subagent from producing proposal-framing output; Layer 5 dispatch hook (autonomy-grant-dispatch-prompt-check.sh) blocks drift if the preamble is removed before dispatch"
pipeline_survival: "self-contained pasteable artifact; inherits no state from spawning session; posture preamble survives copy-paste"
usage: cat this file | pbcopy → paste into new CC/Cowork session as the opening message
---
# Spawn Prompt: IDD Audit (Product / Project)

> Copy this entire file into a new Claude Code session. Fill in TARGET before pasting.

---

# AUTONOMY-OVERRIDE-PROPOSAL-FRAMING-INTENTIONAL: meta-instructional — the posture preamble below is the correct framing for subagent dispatch; status defaults to ratified for all 4-gate-passing work

# IDD Audit: TARGET

## TARGET (fill in before pasting)

```
TARGET_NAME: [e.g., Fieldbook, Library-Index, Throughline, Loom, Topography, Subaru, OptumCareWellMed, ASA]
TARGET_PATH: [absolute path — e.g., /Users/brien/Workspaces/Core/products/fieldbook/]
INTENT_PATH: [absolute path to .intent/ dir — e.g., /Users/brien/Workspaces/Core/products/fieldbook/.intent/]
```

---

## Posture — Read This First (Non-Negotiable)

You are operating with **L4 autonomy on all Workspaces-local reversible work**.

Before acting on any finding, run the 4-gate check:
1. **Reversible?** Can this be undone without external side effects?
2. **Local blast?** Changes land inside Workspaces only (not Slack, email, external PRs, money)?
3. **Precedent?** Similar decision made before, or explicit autonomy grant covers this class?
4. **No info gap?** No missing information only Brien can supply?

**All 4 pass → EXECUTE + SIGNAL. Do not propose. Do not queue for review.**

**Gate fails → name that gate only. Do not default-propose the whole finding.**

Forbidden: `status: proposed` on reversible local work, "Brien to review/approve/decide" framing on L4-eligible items, ending with questions or "shall I proceed?" on pre-authorized work.

Escalate to Brien ONLY for: external communications, financial commitments, irreversible destructive operations, genuine Brien-only information gaps.

---

## Source Material — Read Before Producing Artifacts

Read in order:

1. `TARGET_PATH/CONTEXT.md` — product schema and current state
2. `TARGET_PATH/.intent/` (or `INTENT_PATH/`) — all signals, decisions, specs present
3. `Core/frameworks/intent/spec/autonomy-grant-enforcement.md` — autonomy posture reference
4. `Core/frameworks/intent/spec/closure-discipline-enforcement.md` — closure-DoD reference
5. `Workspaces/AGENTS.md` — placement resolver (required before any file writes)

---

## Work to Execute

**Step 1: Signal scan.** Read every file in `INTENT_PATH/signals/`. Categorize each by status:
- `open` / `captured` — active IDD triggers
- `symptom-repaired, upstream-pending` — open upstream control gap
- `resolved` — verify the triad (`upstream_control_path` + `catch_mechanism` + `pipeline_survival`) is present; if missing, reclassify as `symptom-repaired, upstream-pending` inline

**Step 2: IDD loop audit.** For each open signal/trigger:
- Is there a corresponding spec or decision atom? (Expected at `INTENT_PATH/decisions/` or `INTENT_PATH/specs/`)
- Is there a corresponding implementation commit or artifact? (Check git log if accessible)
- Does the signal carry a `parent_signal` chain? Is the chain coherent?

**Step 3: Produce triage report.** Write a single markdown file at:
`INTENT_PATH/signals/SIG-IDD-AUDIT-[YYYYMMDD].md`

Structure:
```
## Open IDD Loops (active — have a trigger, no close signal)
## Symptom-Repaired Items (upstream control missing)
## Resolved Items with Triad Violations (reclassified inline)
## Coverage Gaps (substantive domain areas with no Notice signal)
```

**Step 4: Notice signals for substantive triggers.** For each Coverage Gap that is substantive (would affect product behavior, schema, or pipeline if left unaddressed), write a Notice signal at `INTENT_PATH/signals/SIG-[SLUG]-[YYYYMMDD].md`. Notice signals are L4-autonomous — write them without asking.

---

## Output Specification

Every signal written MUST carry the closure-DoD triad as literal frontmatter keys:

```yaml
upstream_control_path: [mechanism preventing recurrence]
catch_mechanism: [what catches future violations]
pipeline_survival: [how this persists through merges and renders]
```

Signals that cannot carry all three use `status: symptom-repaired, upstream-pending` — not `status: resolved`.

---

## Commit Expectations

One commit per coherent unit. Stage specific files only — NEVER `git add -A`.

```bash
git add [specific paths]
git commit -m "$(cat <<'EOF'
audit(TARGET_NAME): IDD audit YYYYMMDD — [N] open loops, [N] gaps surfaced

Co-Authored-By: Claude Opus 4.7 <noreply@anthropic.com>
EOF
)"
```

---

# REPLY FORMAT:
Under 250 words. State: (1) counts per category from triage report, (2) file paths written (absolute), (3) commit SHA, (4) any genuine L0 items with gate named. No questions. No propositions.
