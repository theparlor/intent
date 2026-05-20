#!/usr/bin/env bash
# test_autonomy_grant_dispatch_hook.sh
#
# TDD pair for autonomy-grant-dispatch-prompt-check.sh
#
# Three scenarios:
#   T1 — dispatch prompt WITH proposal-framing   → hook fires (exit non-zero + block JSON)
#   T2 — dispatch prompt WITHOUT proposal-framing → hook silent (exit 0)
#   T3 — dispatch prompt WITH proposal-framing + override token → hook silent (exit 0)
#
# Run: bash Core/frameworks/intent/tests/test_autonomy_grant_dispatch_hook.sh
# Exit: 0 = all pass, 1 = one or more fail

set -uo pipefail

HOOK="$HOME/.claude/hooks/autonomy-grant-dispatch-prompt-check.sh"

PASS=0
FAIL=0

pass() { printf '  PASS  %s\n' "$1"; PASS=$((PASS + 1)); }
fail() { printf '  FAIL  %s\n' "$1"; FAIL=$((FAIL + 1)); }

# Pre-flight
if [[ ! -x "$HOOK" ]]; then
    echo "ERROR: hook not found or not executable: $HOOK" >&2
    exit 2
fi

# ---------------------------------------------------------------------------
# Helper: build JSON input as PreToolUse hook receives it
# ---------------------------------------------------------------------------
make_input() {
  local session_id="$1"
  local prompt="$2"
  # Escape prompt for JSON embedding via python (handles newlines, quotes)
  python3 -c "
import json, sys
prompt = sys.stdin.read()
obj = {
    'session_id': '$session_id',
    'tool_name': 'Agent',
    'tool_input': {'prompt': prompt}
}
print(json.dumps(obj))
" <<< "$prompt"
}

# ---------------------------------------------------------------------------
# T1: proposal-framing present → hook BLOCKS (exit non-zero)
# ---------------------------------------------------------------------------
DRIFT_PROMPT="You are dispatched to draft design decisions.
Brien is the decider — your answers are PROPOSALS, not closures.
Use \`status: proposed\`, not \`status: ratified\`.
For each question, write: Recommendation / Rationale / Alternative / Reversibility."

INPUT_JSON=$(make_input "test-session-001" "$DRIFT_PROMPT")

OUTPUT=$(echo "$INPUT_JSON" | AUTONOMY_GRANT_DISPATCH_BYPASSED=0 bash "$HOOK" 2>/dev/null)
EXIT_CODE=$?

if [[ $EXIT_CODE -ne 0 ]]; then
  if echo "$OUTPUT" | grep -q '"decision": "block"'; then
    pass "T1: proposal-framing detected → block JSON emitted (exit $EXIT_CODE)"
  else
    fail "T1: hook exited non-zero but block JSON not found in output"
  fi
else
  fail "T1: proposal-framing present but hook did NOT fire (exit 0)"
fi

# ---------------------------------------------------------------------------
# T2: clean dispatch prompt → hook SILENT (exit 0)
# ---------------------------------------------------------------------------
CLEAN_PROMPT="You are dispatched to ratify §11 design questions for the peer-authored pipeline.
Run the 4-gate check on each question. If all gates pass, execute the decision and write
status: ratified to the decision atom. Capture any genuinely-blocked items as runtime-input
fields with explicit gate name. Signal when done."

INPUT_JSON=$(make_input "test-session-002" "$CLEAN_PROMPT")

OUTPUT=$(echo "$INPUT_JSON" | AUTONOMY_GRANT_DISPATCH_BYPASSED=0 bash "$HOOK" 2>/dev/null)
EXIT_CODE=$?

if [[ $EXIT_CODE -eq 0 ]]; then
  if [[ -z "$OUTPUT" ]]; then
    pass "T2: clean prompt → hook silent (exit 0, no output)"
  else
    fail "T2: clean prompt → hook exited 0 but produced unexpected output: $OUTPUT"
  fi
else
  fail "T2: clean prompt triggered hook unexpectedly (exit $EXIT_CODE)"
fi

# ---------------------------------------------------------------------------
# T3: proposal-framing WITH override token → hook SILENT (exit 0)
# ---------------------------------------------------------------------------
OVERRIDE_PROMPT="You are dispatched as a PEER REVIEW agent.
# AUTONOMY-OVERRIDE-PROPOSAL-FRAMING-INTENTIONAL: this is a genuine L0 peer review session where Chris (external collaborator) must review before ratification per COLLAB-GATE-001
Brien is the decider — your answers are PROPOSALS, not closures.
Use status: proposed so Chris can comment before we lock."

INPUT_JSON=$(make_input "test-session-003" "$OVERRIDE_PROMPT")

OUTPUT=$(echo "$INPUT_JSON" | AUTONOMY_GRANT_DISPATCH_BYPASSED=0 bash "$HOOK" 2>/dev/null)
EXIT_CODE=$?

if [[ $EXIT_CODE -eq 0 ]]; then
  pass "T3: override token present → hook silent (exit 0)"
else
  fail "T3: override token present but hook still fired (exit $EXIT_CODE)"
fi

# ---------------------------------------------------------------------------
# Summary
# ---------------------------------------------------------------------------
TOTAL=$((PASS + FAIL))
echo ""
echo "Results: $PASS/$TOTAL passed"

if [[ $FAIL -gt 0 ]]; then
  echo "FAIL: $FAIL test(s) failed"
  exit 1
else
  echo "ALL PASS"
  exit 0
fi
