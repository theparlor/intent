---
id: SIG-HOOK-OVERRIDE-META-INSTRUCTIONAL-2026-05-20
type: hook-pattern-gap-observed
status: captured
date: '2026-05-20'
hook_affected: Core/frameworks/intent/hooks/autonomy-grant-dispatch-prompt-check.sh
upstream_control_path: Core/frameworks/intent/hooks/autonomy-grant-dispatch-prompt-check.sh (the hook script's override-condition message text)
catch_mechanism: this signal flags the hook description gap; future hook iterations widen override-conditions; downstream prompts using AUTONOMY-OVERRIDE-PROPOSAL-FRAMING-INTENTIONAL token already work at the mechanism level
pipeline_survival: hook code-level override token works regardless of description text; correction is a documentation widening, not a behavior change
---

# Hook override description needs widening: meta-instructional case

## What happened
During the cross-product transferability artifact dispatch (2026-05-20), the Layer 5 dispatch-prompt hook fired correctly on TWO parallel agent prompts that contained `status: proposed` strings — but inside *meta-instructional context* (instructing the subagents to CATALOG `status: proposed` as an anti-pattern, NOT to use it).

The hook's override mechanism (`# AUTONOMY-OVERRIDE-PROPOSAL-FRAMING-INTENTIONAL: <justification>`) exists for exactly this case, but the override DESCRIPTION text in the hook's error message only mentions "genuinely L0 external work" as a valid override case. Meta-instructional documentation of the anti-pattern is a SECOND legitimate override case not yet named.

## Pattern (generalizable)
Hooks that catch anti-pattern strings will fire on any artifact that DOCUMENTS the anti-pattern as content — playbooks, learning catalogs, drift signals, templates that show what NOT to do, post-mortem signals. Override mechanisms must explicitly name "meta-instructional documentation" as a legitimate use alongside "genuinely L0 external work."

## Correction landed inline (this session)
Both dispatch prompts re-fired with the override token + honest meta-instructional justification:
- `# AUTONOMY-OVERRIDE-PROPOSAL-FRAMING-INTENTIONAL: meta-instructional — this prompt documents the anti-pattern as content to be cataloged; subagent output is status: ratified`
- Both subagents executed cleanly with the override; six artifacts landed in `Core/frameworks/intent/`.

## Follow-up (small, L4)
Widen the hook's error-message override-condition description to name TWO legitimate cases:
1. Genuinely L0 external work (existing)
2. Meta-instructional content that documents the anti-pattern as cataloged learning (new)

Pure description widening — no behavior change. The override token mechanism already works at the mechanism level; correction is documentation.

## Cross-references
- Hook: `Core/frameworks/intent/hooks/autonomy-grant-dispatch-prompt-check.sh`
- Parent drift signal: `Core/products/cast/.worktrees/element-substrate-recursive-arb/.intent/signals/SIG-PROCESS-DRIFT-PR-STYLE-REVIEW-2026-05-19.md`
- Artifacts that motivated this finding (the playbook + drift catalog necessarily reference the anti-pattern verbatim):
  - `Core/frameworks/intent/playbooks/idd-build-pattern.md` (commit 75cf04b)
  - `Core/frameworks/intent/learnings/process-drift-catalog.md` (commit a78f44e)
  - `Core/frameworks/intent/knowledge-engine/templates/subagent-dispatch-prompt.md` (commit 1c88a06)
  - `Core/frameworks/intent/spawn-prompts/*.md` (commit 51a0b5c)
