---
title: Spawn Prompt — Process Drift Audit
id: SPAWN-PROCESS-DRIFT-AUDIT
type: spawn-prompt
created: 2026-05-20
status: canonical
upstream_control_path: Core/frameworks/intent/spawn-prompts/process-drift-audit.md (this file)
catch_mechanism: posture preamble prevents subagent from producing proposal-framing in audit output; the audit itself surfaces drift, which is then corrected inline (L4) or flagged to Brien (L0)
pipeline_survival: self-contained pasteable artifact; audit pattern is reusable across any product or engagement
usage: cat this file | pbcopy → paste into new CC/Cowork session as the opening message
---

# Spawn Prompt: Process Drift Audit

> Copy this entire file into a new Claude Code session. Fill in TARGET before pasting.

---

# AUTONOMY-OVERRIDE-PROPOSAL-FRAMING-INTENTIONAL: meta-instructional — the posture preamble below governs subagent behavior; inline L4 corrections execute autonomously; only genuine L0 items surface to Brien

# Process Drift Audit: TARGET

## TARGET (fill in before pasting)

```
TARGET_NAME: [e.g., Subaru, OptumCareWellMed, Cast, Forge, Library-Index]
TARGET_PATH: [absolute path — e.g., /Users/brien/Workspaces/Work/Consulting/Engagements/Subaru/]
INTENT_PATH: [absolute path to .intent/ dir — if present]
LOOKBACK_DAYS: [how many days of commits/signals to audit — e.g., 14]
```

---

## Posture — Read This First (Non-Negotiable)

You are operating with **L4 autonomy on all Workspaces-local reversible work**.

4-gate check before every corrective action:
1. **Reversible?** Can this be undone without external side effects?
2. **Local blast?** Changes land inside Workspaces only?
3. **Precedent?** Explicit autonomy grant or prior decision covers this class?
4. **No info gap?** No missing information only Brien can supply?

**All 4 pass → correct inline + signal. Do not propose.**

**Gate fails → name that gate. Surface to Brien ONLY if the gate is L0 (external comm, money, irreversible).**

Forbidden in your output: `status: proposed` on reversible local work, "Brien to review" on L4-eligible items, questions on pre-authorized corrections.

---

## Source Material — Read Before Auditing

1. `TARGET_PATH/CONTEXT.md` (if present) — current state
2. `INTENT_PATH/` (if present) — all signals and decisions
3. `Core/frameworks/intent/spec/autonomy-grant-enforcement.md` — autonomy posture + drift catalog
4. `Core/frameworks/intent/spec/closure-discipline-enforcement.md` — closure-DoD policy
5. `Workspaces/AGENTS.md` — placement resolver

---

## Drift Catalog (what to look for)

Audit recent commits, signals, and decision atoms against these known drift patterns:

### Autonomy-grant drift
- `status: proposed` on decisions where all 4 gates pass
- "Brien to review / Brien to approve / Brien to decide" on L4-eligible items
- "Phase 2 retrofit" lists splitting trivially-combinable L4 work
- Soft-queue endings on pre-authorized continuation ("say go and I will…")
- Bare-choice-without-recommendation endings

### Closure-discipline drift
- `status: resolved` signals missing `upstream_control_path:` and/or `catch_mechanism:` and/or `pipeline_survival:`
- "Complete" / "done" / "shipped" claim language without upstream control mentioned
- Symptom patch (deleted/corrected the instance) without upstream control that prevents recurrence

### Subagent-prompt injection drift
- Prior dispatch prompts containing "Brien is the decider," "your answers are proposals," "status: proposed," "for Brien's review" framing on L4 work (check `.intent/` for stored dispatch prompts if any)

### Scope-narrowing drift
- Task description said "all" or "every"; execution covered only a subset without explicit scope-reduction signal

---

## Work to Execute

**Step 1: Commit log scan.** Review the last LOOKBACK_DAYS of commits in the target repo/worktree. Flag any commit message that implies completion ("done," "complete," "fix," "resolved") without a corresponding upstream control in the associated signal/artifact.

**Step 2: Signal audit.** Read every signal in `INTENT_PATH/signals/` (if present). Flag:
- `status: resolved` without the full triad
- `status: proposed` on decisions that appear to pass 4-gate

**Step 3: Inline corrections (L4).** For each flagged item that passes 4-gate:
- Reclassify `status: resolved` → `status: symptom-repaired, upstream-pending` if triad is missing
- Add or correct the triad fields where the upstream control does exist (verify, then populate)
- Flip `status: proposed` → `status: ratified` with `ratified_at` for atoms that pass 4-gate

**Step 4: Write audit signal.** Write the audit record at:
`INTENT_PATH/signals/SIG-PROCESS-DRIFT-AUDIT-[YYYYMMDD].md` (or `TARGET_PATH/.intent/signals/` if no separate intent path)

Structure:
```
## Drift Instances Found
## Inline Corrections Applied (L4)
## Genuine L0 Items (gate named, Brien action required)
## Clean Items (verified, no correction needed)
```

---

## Output Specification

Audit signal frontmatter must carry the literal triad:

```yaml
upstream_control_path: [this audit + any inline corrections applied]
catch_mechanism: [Layer 4/5 hooks active; process-drift catalog in spec]
pipeline_survival: [inline corrections are durable; audit signal is standalone reference]
```

---

## Commit Expectations

One commit for all inline corrections + audit signal.

```bash
git add [specific paths only]
git commit -m "$(cat <<'EOF'
audit(TARGET_NAME): process-drift audit YYYYMMDD — [N] corrections, [N] L0 items

Co-Authored-By: Claude Opus 4.7 <noreply@anthropic.com>
EOF
)"
```

---

# REPLY FORMAT:
Under 250 words. State: (1) drift instances found by category, (2) inline corrections applied (count + file paths), (3) L0 items with gate named, (4) commit SHA. No questions. No propositions.
