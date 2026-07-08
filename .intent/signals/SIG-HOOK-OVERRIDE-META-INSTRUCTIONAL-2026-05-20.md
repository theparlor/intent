---
id: SIG-HOOK-OVERRIDE-META-INSTRUCTIONAL-2026-05-20
type: hook-pattern-gap-observed
status: resolved
resolved: '2026-05-20'
date: '2026-05-20'
hook_affected: Core/frameworks/intent/hooks/autonomy-grant-dispatch-prompt-check.sh
upstream_control_path: "Core/frameworks/intent/hooks/autonomy-grant-dispatch-prompt-check.sh (line 156, override-condition message confirmed widened to include \"(b) the prompt is meta-instructional content that catalogs the anti-pattern as documented learning\")"
catch_mechanism: "hook error-message text (verified at line 156) now names TWO legitimate override cases: (a) genuinely L0 external work and (b) meta-instructional documentation. Future hook authors reading the error message will see the full override taxonomy. Override token AUTONOMY-OVERRIDE-PROPOSAL-FRAMING-INTENTIONAL mechanism was already correct; this closure confirms the description now matches."
pipeline_survival: "hook is git-tracked at Core/frameworks/intent/hooks/; symlinked from ~/.claude/hooks/; registered in ~/.claude/settings.json; message text persists across sessions. No behavior change, correction was documentation only."
---

# Hook override description widened: meta-instructional case added (hook line 156)

## What happened
During the cross-product transferability artifact dispatch (2026-05-20), the Layer 5 dispatch-prompt hook fired correctly on TWO parallel agent prompts that contained `status: proposed` strings — but inside *meta-instructional context* (instructing the subagents to CATALOG `status: proposed` as an anti-pattern, NOT to use it).

The hook's override mechanism (`# AUTONOMY-OVERRIDE-PROPOSAL-FRAMING-INTENTIONAL: <justification>`) exists for exactly this case, but at the time the override DESCRIPTION text in the hook's error message only mentioned "genuinely L0 external work" as a valid override case. Meta-instructional documentation of the anti-pattern was a SECOND legitimate override case missing from the message (widening landed same session; re-verified 2026-07-03 at `Core/frameworks/intent/hooks/autonomy-grant-dispatch-prompt-check.sh` line 156).

## Pattern (generalizable)
Hooks that catch anti-pattern strings will fire on any artifact that DOCUMENTS the anti-pattern as content — playbooks, learning catalogs, drift signals, templates that show what NOT to do, post-mortem signals. Override mechanisms must explicitly name "meta-instructional documentation" as a legitimate use alongside "genuinely L0 external work."

## Correction landed inline (this session)
Both dispatch prompts re-fired with the override token + honest meta-instructional justification:
- `# AUTONOMY-OVERRIDE-PROPOSAL-FRAMING-INTENTIONAL: meta-instructional — this prompt documents the anti-pattern as content to be cataloged; subagent output is status: ratified`
- Both subagents executed cleanly with the override; six artifacts landed in `Core/frameworks/intent/`.

## Description widening (landed 2026-05-20: hooks/autonomy-grant-dispatch-prompt-check.sh line 156)
The hook's error-message override-condition description was widened to name TWO legitimate cases:
1. Genuinely L0 external work (existing)
2. Meta-instructional content that documents the anti-pattern as cataloged learning (added)

Pure description widening, no behavior change. The override token mechanism already worked at the mechanism level; the correction was documentation. Re-verified 2026-07-03: line 156 block message reads "Override if EITHER (a) this is genuinely L0 external work, OR (b) the prompt is meta-instructional content that catalogs the anti-pattern as documented learning (playbook, drift catalog, template showing what NOT to do, post-mortem signal)".

## Cross-references
- Hook: `Core/frameworks/intent/hooks/autonomy-grant-dispatch-prompt-check.sh`
- Parent drift signal: `Core/products/cast/.worktrees/element-substrate-recursive-arb/.intent/signals/SIG-PROCESS-DRIFT-PR-STYLE-REVIEW-2026-05-19.md`
- Artifacts that motivated this finding (the playbook + drift catalog necessarily reference the anti-pattern verbatim):
  - `Core/frameworks/intent/playbooks/idd-build-pattern.md` (commit 75cf04b)
  - `Core/frameworks/intent/learnings/process-drift-catalog.md` (commit a78f44e)
  - `Core/frameworks/intent/knowledge-engine/templates/subagent-dispatch-prompt.md` (commit 1c88a06)
  - `Core/frameworks/intent/spawn-prompts/*.md` (commit 51a0b5c)
