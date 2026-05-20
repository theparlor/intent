---
signal_id: SIG-037
title: Layer 4 (linguistic detector / Stop hook) of autonomy-grant enforcement deployed
date: 2026-04-28
kind: closure-signal
status: symptom-repaired
source: 2026-04-28 main session — bare-choice slip on hook-vs-template-vs-CLAUDE.md decision
related:
  - Core/frameworks/intent/spec/autonomy-grant-enforcement.md
  - Core/frameworks/intent/hooks/autonomy-grant-stop-check.sh
  - Core/products/org-design-tooling/.intent/signals/RETRO-2026-04-21-autonomy-grant-reinforcement-SIG-1.md
  - Core/frameworks/coherence-engineering/.intent/signals/SIG-COH-DEBT-018.md
  - memory/feedback_decisioning_discipline.md
  - memory/feedback_autonomy_grant_drift_pattern.md
---

# SIG-037 — Layer 4 Stop hook deployed

## What happened

Brien flagged repeat bare-choice-instead-of-recommendation slips in a session where Layer 1 (SessionStart anchor) was active and decisioning-discipline memory was loaded. Failure pattern: response ending with "Want me to A, or B?" without a preceding commitment. Layer 1's posture text was insufficient; the model still generated bare-choice closings on subsequent turns.

In response, Layer 4 of the autonomy-grant enforcement spec (linguistic detector) was promoted from "future iteration" to deployed:

- **Hook script:** `Core/frameworks/intent/hooks/autonomy-grant-stop-check.sh`
- **Symlink:** `~/.claude/hooks/autonomy-grant-stop-check.sh`
- **Registration:** `~/.claude/settings.json` `hooks.Stop[*]`
- **CLAUDE.md rule:** new "Recommendation-first, never bare choice" entry in Behavioral Rules (via `claude-md-overrides.md`, regenerated)
- **Audit log:** `~/.claude/audit/autonomy-grant-stop-detections.log`

Hook was tested with six synthetic transcripts before activation:
- bare-choice + no recommendation → BLOCKS ✓
- bare-choice + recommendation marker → passes ✓
- no bare-choice → passes ✓
- bypass env var → passes ✓
- recursion guard (stop_hook_active) → passes ✓
- recommendation earlier + bare-choice later → passes ✓

## Why it matters

Layer 1 (SessionStart anchor) is consultation-dependent — it tells the model what to do but doesn't enforce. Layer 4 (Stop hook) is detection-and-block — it catches the pattern at turn-end and forces revision. Together they form a layered defense matching the build-intake enforcement precedent (SIG-045).

The Stop hook is calibrated conservative for v0: false-negative bias preferred. The recommendation regex is deliberately inclusive (~30 markers). Only egregious bare-choice patterns trigger. Audit log will inform regex tuning.

## Action

- Captured: hook deployed, registered, tested, spec updated, CLAUDE.md regenerated.
- Pending: monitor audit log over multiple sessions. If false positives emerge, tune regex. If false negatives persist (Brien manually catching slips that the hook missed), add patterns.
- Pending: Layer 3 (PreToolUse on TodoWrite/ExitPlanMode) and Layer 5 (drift telemetry feedback loop) remain future iterations. Audit log from Layer 4 partially covers Layer 5 by design.
- Open: template-gate mechanism (the third option from this session's recommendation) is NOT yet built. It would force a `recommendation:` slot in response template before any "or" question. That's a more invasive change to model output and is held for separate decision.

## Upstream control

Closes the closure criterion in RETRO-2026-04-21-autonomy-grant-reinforcement-SIG-1 and SIG-COH-DEBT-018 from "symptom-repaired" toward "resolved" once the hook has caught real slips over multiple sessions without false-positive complaints. The hook IS the upstream control — Layer 1 was anchoring; Layer 4 is enforcing.
