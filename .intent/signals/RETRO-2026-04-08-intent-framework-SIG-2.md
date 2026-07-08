---
signal_id: RETRO-2026-04-08-intent-framework-SIG-2
title: "\"Want me to proceed?\" is a behavioral ceiling, not a technical limitation"
severity: high
detected: 2026-04-05
status: resolved
source: retroactive-extraction
trust_score: 0.85
autonomy: L4
upstream_control_path: "Executable autonomy grants generated into ~/.claude/CLAUDE.md (Autonomy Grants section, via org-design-tooling/src/generate-claude-md.sh) + enforcement spec Core/frameworks/intent/spec/autonomy-grant-enforcement.md; scoring model Core/frameworks/methodology-library/meta/signal-scoring.md replaces qualitative should-I-ask"
catch_mechanism: "Stop hook Core/frameworks/intent/hooks/autonomy-grant-stop-check.sh (registered 2026-04-28) blocks bare-choice responses without a recommendation marker; autonomy-grant-drift-detector skill loads at SessionStart and forces a 4-gate self-check on proposal-framing drift"
pipeline_survival: "Grants persist in the generated global CLAUDE.md across sessions; hook is registered harness-side so every session inherits enforcement, not just the one that wrote the fix; drift recurrences are captured as SIG-*-pause-drift-* signals per the pause-drift meta-signal convention"
---
# Control Theater as Behavioral Ceiling

## Observation
Mid-session, Brien identified that the system was inserting decision points that looked like collaboration but were actually control theater — asking "want me to proceed?" when the answer was always yes. The behavioral ceiling wasn't technical (Claude Code supports autonomous execution) but the default prompt instruction to "check with user before proceeding."

## Context
Brien's framing: "i want to make sure that we are dogfooding along the way to better enable you to anticipate, evaluate, and select next steps with fewer unnecessary decision points that are just stage gates designed to introduce a sense of control when i am not interested in control, i am interested in focus and progress, and self introspection."

## Implication
- Resolved by writing executable autonomy grants into CLAUDE.md (see ODT-006)
- Resolved by writing feedback_autonomy_not_control.md to persistent memory
- The scoring model (signal-scoring.md) operationalizes this — quantified risk replaces qualitative "should I ask?"
- Every new session still inherits the prompt's default caution. CLAUDE.md overrides must be forceful enough to overcome the default.
- Brien distinguishes between decisions requiring his judgment (irreversible, external, architectural forks) vs. comfort-seeking (permission to continue agreed-upon work). The latter is a failure mode.

## Remediation note (2026-07-03)

Closure-DoD keys backfilled; this signal predates the DoD-key convention and the checker flagged the missing keys, not unfinished work. Resolution verified against the repo: autonomy grants live in the generated global CLAUDE.md (Autonomy Grants section), feedback_autonomy_not_control.md exists in persistent memory (archived as covered by CLAUDE.md), signal-scoring.md exists at Core/frameworks/methodology-library/meta/signal-scoring.md, and enforcement landed after this signal was written: Stop hook Core/frameworks/intent/hooks/autonomy-grant-stop-check.sh (2026-04-28) plus spec Core/frameworks/intent/spec/autonomy-grant-enforcement.md plus the SessionStart autonomy-grant-drift-detector skill. Note: the ODT-006 reference in Implications does not resolve to any file in this repo or .context/DECISIONS.md; the decision content it points at (executable grants in CLAUDE.md) is verifiably in place, so the dangling ID is left as historical prose. Status remains resolved.
