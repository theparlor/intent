---
id: SIG-2026-05-20-l0-on-push-framing-no-hook-catch
date: 2026-05-20
status: resolved
resolved: '2026-05-20'
type: drift-pattern
severity: medium
related:
  - feedback_commit_autonomy.md (memory updated 2026-05-19; reinforcement appended 2026-05-20)
  - Core/frameworks/intent/hooks/autonomy-grant-stop-check.sh (CHECK 3 added 2026-05-20)
upstream_control_path: Core/frameworks/intent/hooks/autonomy-grant-stop-check.sh CHECK 3 block — scans for forbidden push-handoff phrases when theparlor/* commit context is detected in the response; blocks and demands push execution
catch_mechanism: Stop hook CHECK 3 regex bank matches literal phrases from feedback_commit_autonomy.md §5 ("not pushed.", "run.*git push.*from", "commit landed.*push when", "i'll commit only", "push when you're ready", "push to remote when you want"); context gate requires theparlor/* commit evidence in same response (prevents false positives on non-git responses)
pipeline_survival: hook is git-tracked at Core/frameworks/intent/hooks/; symlinked from ~/.claude/hooks/; registered in ~/.claude/settings.json as Stop hook; persists across sessions; CHECK 3 block self-documents the §5 forbidden phrase list in its block message
---

# L0-on-push framing on theparlor/* commits — no Stop-hook catch

## Observation

2026-05-19: `feedback_commit_autonomy.md` written — push on theparlor/* solo repos is L4, not L0. Memory entry was explicit.

2026-05-20 (today, ~24h later): drift recurrence during reference-substrate renumber session. Response ended with "Not pushed to remote. Run `git push` from `Core/products/reference-substrate/` when you want it on `theparlor/reference-substrate`." — exactly the framing the recalibration killed.

Detection mechanism today: Brien noticed and called it out manually ("you didn't ask this much last week and you worked harder and deeper").

## Why memory-only catch is insufficient

The existing `autonomy-grant-stop-check.sh` catches one drift class (bare-choice questions without recommendation marker). The L0-on-push framing is the same kind of drift — proposal/handoff language on L4-eligible reversible work — but routed through a different surface (push handoff, not choice handoff).

`feedback_commit_autonomy.md` §5 now lists literal forbidden phrases:
- "Not pushed. Run `git push` from <path> when you want it on <remote>."
- "Commit landed; push when you're ready."
- "I'll commit only since you said commit, not push."
- Any sentence handing the push back to Brien on a theparlor/* repo.

But memory is *behavioral guidance*, not mechanism. A Stop hook regex against those exact phrases on responses that just landed a commit to a theparlor/* repo would be the mechanism-level catch.

## What the upstream control would be

Option A (preferred): extend `autonomy-grant-stop-check.sh` with an L0-on-push regex bank, scoped to responses where the last assistant action included a `git commit` on a `theparlor/*` remote and no `git push` followed.

Option B: new sibling `commit-push-coupling-stop-check.sh` dedicated to the push-coupling failure mode.

Option A is cheaper (one script, two drift classes, same shape).

## What pipeline survival looks like

The hook fires on response-end. If installed, it would block the exact drift sentences from being sent. Future memory edits or recalibrations couldn't regress around it without explicitly disabling the regex.

## Open

- Build the hook regex bank (Option A).
- Decide whether the hook should auto-execute the `git push` it detected was withheld, or just block the response and force a revision. (Auto-execute is more useful but adds a destructive class; block-and-revise is safer.)
- Test against the literal sentence list in feedback_commit_autonomy.md §5.

This is not built today. Memory-only catch is the interim mechanism.
