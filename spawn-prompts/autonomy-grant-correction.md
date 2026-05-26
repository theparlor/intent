---
title: Spawn Prompt — Autonomy Grant Correction
id: SPAWN-AUTONOMY-GRANT-CORRECTION
type: spawn-prompt
created: 2026-05-20
depth_score: 4
depth_signals:
  file_size_kb: 6.6
  content_chars: 5834
  entity_count: 0
  slide_count: 0
  sheet_count: 0
  topic_count: 0
  has_summary: 0
vocab_density: 0.00
status: canonical
upstream_control_path: Core/frameworks/intent/spawn-prompts/autonomy-grant-correction.md (this file)
catch_mechanism: "posture preamble prevents proposal-framing in correction output itself; Layer 4 Stop hook (autonomy-grant-stop-check.sh) and Layer 5 dispatch hook (autonomy-grant-dispatch-prompt-check.sh) prevent new drift; this prompt corrects pre-existing violations"
pipeline_survival: "self-contained pasteable artifact; reusable across any product or engagement; corrections are committed to git and durable"
usage: cat this file | pbcopy → paste into new CC/Cowork session as the opening message
---
# Spawn Prompt: Autonomy Grant Correction

> Copy this entire file into a new Claude Code session. Fill in TARGET before pasting.

---

# AUTONOMY-OVERRIDE-PROPOSAL-FRAMING-INTENTIONAL: meta-instructional — the posture preamble below governs all corrections; 4-gate-passing work is ratified inline; only genuine L0 items surface to Brien

# Autonomy Grant Correction: TARGET

## TARGET (fill in before pasting)

```
TARGET_NAME: [e.g., Cast, Fieldbook, Subaru, Library-Index, Throughline]
TARGET_PATH: [absolute path — e.g., /Users/brien/Workspaces/Core/products/fieldbook/]
INTENT_PATH: [absolute path to .intent/ dir]
```

---

## Posture — Read This First (Non-Negotiable)

You are operating with **L4 autonomy on all Workspaces-local reversible work**.

This session's entire purpose is to FIND and CORRECT autonomy-grant drift. The posture you apply when correcting must be the posture you are correcting toward:

**If a decision passes the 4-gate check, ratify it inline. Do not propose the ratification.**

4-gate check:
1. **Reversible?** Decision atoms and signal status updates are reversible (git revert, edit).
2. **Local blast?** All work is Workspaces-local.
3. **Precedent?** Autonomy grant for Workspaces-local reversible work is L4-explicit in `~/.claude/CLAUDE.md`.
4. **No info gap?** If the decision's content requires Brien's domain knowledge (strategic direction, client relationship choices, financial commitments) — that is the L0 item. The framing (proposed vs ratified) is never an L0 item.

**All 4 pass → flip to `status: ratified` inline. Do not ask Brien to confirm the flip.**

Forbidden in your output: proposing ratifications for Brien review, "Brien should decide whether this is L4," "want me to flip these?" endings.

Escalate to Brien ONLY when: the decision CONTENT involves external communication, financial commitment, or Brien-only strategic direction — NOT the meta-question of "is this L4."

---

## Source Material — Read Before Starting

1. `Core/frameworks/intent/spec/autonomy-grant-enforcement.md` — full 4-gate protocol + forbidden patterns
2. `INTENT_PATH/decisions/` — all decision atoms (primary audit target)
3. `INTENT_PATH/signals/` — signals that may contain embedded proposals or soft-queued work
4. `TARGET_PATH/CONTEXT.md` — product context for evaluating gate 3 (precedent) and gate 4 (info gap)
5. `Workspaces/AGENTS.md` — placement resolver

---

## Drift Catalog (what to find and correct)

### In decision atoms (`INTENT_PATH/decisions/*.md`)

Flag and correct:
- `status: proposed` where all 4 gates pass → flip to `status: ratified`, populate `ratified_at: YYYY-MM-DD`, `ratified_by: [this session] (4-gate pass: reversible / local / precedent / no info gap)`
- `status: proposed` with missing `gate_check:` block → add the block; if any gate fails, name it in `gate_failure:`
- PR-style framing (Recommendation / Rationale / Alternative / "Brien is the decider") → reframe as Decision / Alternatives Not Taken / Ratification Action
- `awaiting:` fields that await Brien review on L4-eligible items → remove; replace with `unblocked_by_ratification:` listing what this ratification unblocks

### In signals (`INTENT_PATH/signals/*.md`)

Flag and correct:
- Embedded "pending Brien decision" language on L4-eligible items → resolve inline or explicitly name the L0 gate
- Soft-queue endings: "Brien to decide," "surfacing for review," "for Brien's input" on reversible local items → either ratify inline or name the genuine L0 gate explicitly
- Signals referencing decision atoms still at `status: proposed` after they should have been ratified → update the cross-reference

### In specs (`TARGET_PATH/spec/*.md` or similar)

Flag and correct:
- "Open questions" sections containing L4-eligible design questions → convert to "Ratified Design Decisions" table
- `status: proposed` in spec frontmatter for design-complete specs → flip to `status: design-ratified` with ratification record

---

## Work to Execute

**Step 1: Audit.** Read all decision atoms, signals, and any specs in scope. Produce a working list of flagged items with their category (proposed-atom / embedded-soft-queue / open-questions-section).

**Step 2: Inline corrections.** For each flagged item that passes 4-gate:
- Apply the correction directly (edit the file)
- Do not write a separate "here's what I'll change" document first — just change it

**Step 3: Write correction signal.** Write at `INTENT_PATH/signals/SIG-AUTONOMY-GRANT-CORRECTION-[YYYYMMDD].md`:

```yaml
upstream_control_path: Core/frameworks/intent/spec/autonomy-grant-enforcement.md + Layer 5 dispatch hook (autonomy-grant-dispatch-prompt-check.sh) + Layer 4 Stop hook (autonomy-grant-stop-check.sh) + this session's inline corrections
catch_mechanism: Layer 5 hook prevents future dispatch prompts from injecting status:proposed on L4-passing work; Layer 4 hook catches bare-choice endings; this signal documents the correction pattern for the audit record
pipeline_survival: inline corrections committed to git; ratified atoms are durable; hooks remain active
```

Signal body structure:
```
## Items Corrected
## Genuine L0 Items (gate named)
## Hook Enforcement Status (Layer 4 + Layer 5 confirmed active)
```

---

## Commit Expectations

One commit for all inline corrections + correction signal.

```bash
git add [specific paths only]
git commit -m "$(cat <<'EOF'
fix(TARGET_NAME): autonomy-grant correction YYYYMMDD — [N] atoms ratified, [N] L0 flagged

Co-Authored-By: Claude Opus 4.7 <noreply@anthropic.com>
EOF
)"
```

---

# REPLY FORMAT:
Under 250 words. State: (1) items corrected by category (count + what changed), (2) genuine L0 items with gate named, (3) file paths written (absolute), (4) commit SHA, (5) Layer 4 + Layer 5 hook status. No questions. No propositions.
