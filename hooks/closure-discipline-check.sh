#!/usr/bin/env bash
# closure-discipline-check.sh
#
# SessionStart hook — Layer 2 of closure-discipline enforcement.
#
# Loads the closure-DoD posture into the session context as additional
# system context. Anchors the discipline that "resolved" requires
# upstream control + catch-mechanism, else use "symptom-repaired,
# upstream-pending".
#
# Spec: Core/frameworks/intent/spec/closure-discipline-enforcement.md
#
# Install: chmod +x and symlink to ~/.claude/hooks/
# Register: add SessionStart entry to ~/.claude/settings.json
#
# Bypass: CLOSURE_DISCIPLINE_BYPASSED=1
#
# Created: 2026-04-30 — promotes the closure-DoD policy from
# memory-only enforcement to mechanism-level write-boundary enforcement
# in response to recurring symptom-patch-disguised-as-resolution drift.

set -u

# Bypass
if [ "${CLOSURE_DISCIPLINE_BYPASSED:-0}" = "1" ]; then
  exit 0
fi

cat <<'EOF'
🔧 CLOSURE-DISCIPLINE POSTURE (load-bearing, pre-completion anchor)

When closing a fix/audit/cleanup task, "resolved" requires THREE assertions:

  1. UPSTREAM CONTROL — file path of the resolver in the pipeline,
     not "I ran the script." If the fix is a one-shot script that
     could need re-running for new entities, it is downstream-only.

  2. CATCH-NET — chain_audit invariant ID, test, or explicit
     "no catch-net possible because…" justification. The audit
     should flag this gap if it regresses.

  3. PIPELINE SURVIVAL — will this fix survive the next render_all
     or equivalent pipeline run? If a downstream stage can wipe it
     (the compute-cvrs regex sibling-wipe pattern), the fix isn't
     stable and "resolved" is wrong.

If ALL three hold: status: resolved with upstream_control_path: and
catch_mechanism: fields populated.

If ANY are missing: status: symptom-repaired, upstream-pending —
with a follow-up signal capturing what the upstream control would
need to be.

FORBIDDEN closure-claim patterns (will be blocked by Layer 4 Stop hook):

  • Ending response with "complete / done / resolved / fixed / shipped"
    without any mention of upstream control, pipeline integration,
    catch-net invariant, or future-regression prevention
  • Writing a signal file with status: resolved without
    upstream_control_path: and catch_mechanism: fields
  • Declaring a wave/audit/sweep "closed" while the pattern that
    produced the gap is still live
  • Declaring victory based on running a one-shot patch script

Reinforcement history: Brien has reinforced the closure-DoD policy
multiple times. Memory entries (feedback_errors_are_signals,
feedback_audit_vs_writethrough, reference_signal_closure_policy) and
the existing signal-stream.md DoD library haven't closed the drift.
This hook IS the mechanism-level fix.

Spec: Core/frameworks/intent/spec/closure-discipline-enforcement.md
EOF
