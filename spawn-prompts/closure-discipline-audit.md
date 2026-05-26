---
title: Spawn Prompt — Closure Discipline Audit
id: SPAWN-CLOSURE-DISCIPLINE-AUDIT
type: spawn-prompt
created: 2026-05-20
depth_score: 4
depth_signals:
  file_size_kb: 6.5
  content_chars: 5777
  entity_count: 0
  slide_count: 0
  sheet_count: 0
  topic_count: 0
  has_summary: 0
vocab_density: 0.00
status: canonical
upstream_control_path: Core/frameworks/intent/spawn-prompts/closure-discipline-audit.md (this file)
catch_mechanism: "posture preamble enforces execute-not-propose posture on corrections; Layer 5 PreToolUse hook (closure-discipline-signal-check.sh) blocks status:resolved signal writes missing the triad; this audit finds violations the hook may have missed and corrects them inline"
pipeline_survival: self-contained pasteable artifact; reusable across any product or engagement
usage: cat this file | pbcopy → paste into new CC/Cowork session as the opening message
---
# Spawn Prompt: Closure Discipline Audit

> Copy this entire file into a new Claude Code session. Fill in TARGET before pasting.

---

# AUTONOMY-OVERRIDE-PROPOSAL-FRAMING-INTENTIONAL: meta-instructional — the posture preamble governs all subagent corrections; reclassifications execute inline at L4; only genuine L0 items surface to Brien

# Closure Discipline Audit: TARGET

## TARGET (fill in before pasting)

```
TARGET_NAME: [e.g., Fieldbook, Cast, Subaru, OptumCareWellMed, Throughline]
TARGET_PATH: [absolute path — e.g., /Users/brien/Workspaces/Core/products/fieldbook/]
INTENT_PATH: [absolute path to .intent/ dir — e.g., /Users/brien/Workspaces/Core/products/fieldbook/.intent/]
```

---

## Posture — Read This First (Non-Negotiable)

You are operating with **L4 autonomy on all Workspaces-local reversible work**.

4-gate check before every corrective action:
1. **Reversible?** Reclassifying a signal status is reversible (git revert); triad field additions are additive.
2. **Local blast?** Signal files are Workspaces-local artifacts.
3. **Precedent?** Closure-DoD policy is explicit in `Core/frameworks/intent/spec/closure-discipline-enforcement.md`.
4. **No info gap?** The triad fields require knowing what the upstream control IS. If you cannot determine what the upstream control is from the artifact's context, that is the L0 item.

**All 4 pass → correct inline + signal. Do not propose.**

**When upstream control is genuinely unknown → reclassify to `symptom-repaired, upstream-pending` + write a named gap signal. Do not leave `status: resolved` standing.**

Forbidden: proposing reclassifications for Brien review, "Brien to decide whether this is resolved," questions on L4-eligible corrections.

---

## Source Material — Read Before Auditing

1. `Core/frameworks/intent/spec/closure-discipline-enforcement.md` — the policy being enforced
2. `Core/frameworks/intent/spec/signal-stream.md` (if present) — signal status vocabulary
3. All files in `INTENT_PATH/signals/` — the audit targets
4. `INTENT_PATH/decisions/` (if present) — cross-reference for decision atoms claiming closure
5. `TARGET_PATH/CONTEXT.md` (if present) — product context for understanding what upstream controls exist

---

## Closure-DoD Policy (verbatim reference)

From `Core/frameworks/intent/spec/closure-discipline-enforcement.md`:

- `status: resolved` REQUIRES `upstream_control_path:` AND `catch_mechanism:` AND `pipeline_survival:`
- If any of the three is missing: use `status: symptom-repaired, upstream-pending`
- If the upstream control is a one-shot fix with no catch-net: use `status: symptom-repaired, upstream-pending` + note what the upstream control WOULD need to be

The three literal frontmatter keys (with colons):
```yaml
upstream_control_path: [path or description of the mechanism preventing recurrence]
catch_mechanism: [what catches future violations of the same class]
pipeline_survival: [how the fix persists through render cycles, merges, future edits]
```

---

## Work to Execute

**Step 1: Scan all signals.** Read every `.md` file in `INTENT_PATH/signals/`. For each:
- Does it carry `status: resolved` (or `status: closed`, `status: done`)?
- If yes: are all THREE literal triad keys present with non-empty values?
- If no: flag for correction.

**Step 2: Inline corrections.** For each flagged signal:

Case A — upstream control EXISTS but triad is absent or incomplete:
- Determine the upstream control from context (git history, referenced specs, chain_audit invariants, hooks)
- Populate the missing triad fields inline
- Update `status` to remain `resolved` (triad now complete)

Case B — upstream control CANNOT be determined from available context:
- Reclassify: `status: resolved` → `status: symptom-repaired, upstream-pending`
- Add a named-gap comment: what the upstream control would need to be
- Write a Notice signal at `INTENT_PATH/signals/SIG-CLOSURE-GAP-[SLUG]-[YYYYMMDD].md`

Case C — signal was a one-shot fix with no upstream control by design:
- Reclassify: `status: resolved` → `status: symptom-repaired, upstream-pending`
- Add: `upstream_note: one-shot-fix — no upstream control installed; recurrence remains possible`

**Step 3: Write audit summary signal.** Write at `INTENT_PATH/signals/SIG-CLOSURE-DISCIPLINE-AUDIT-[YYYYMMDD].md`:

```
## Signals Audited (count)
## Corrected — Triad Populated (Case A, count + paths)
## Reclassified — Upstream Unknown (Case B, count + paths)
## Reclassified — One-Shot (Case C, count + paths)
## Clean — No Correction Needed (count)
## Named Gaps Written (paths to SIG-CLOSURE-GAP-* signals)
```

---

## Output Specification

Audit summary signal frontmatter must carry:

```yaml
upstream_control_path: Core/frameworks/intent/spec/closure-discipline-enforcement.md + Layer 5 PreToolUse hook (closure-discipline-signal-check.sh) + this audit (inline corrections)
catch_mechanism: Layer 5 hook inspects future signal writes targeting status:resolved; this audit corrects pre-existing violations the hook did not cover
pipeline_survival: inline corrections are committed to git; reclassified signals accurately reflect actual resolution state going forward; hook prevents new violations
```

---

## Commit Expectations

One commit for all inline corrections + audit summary.

```bash
git add [specific paths only]
git commit -m "$(cat <<'EOF'
audit(TARGET_NAME): closure-discipline audit YYYYMMDD — [N] corrected, [N] reclassified

Co-Authored-By: Claude Opus 4.7 <noreply@anthropic.com>
EOF
)"
```

---

# REPLY FORMAT:
Under 250 words. State: (1) counts per case category, (2) file paths corrected/reclassified (absolute), (3) named gaps written, (4) commit SHA, (5) triad confirmed present in audit signal. No questions. No propositions.
