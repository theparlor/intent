#!/usr/bin/env bash
# test_autonomy_posture_layer42.sh
#
# Smoke test for the Layer 4.2 STRUCTURAL autonomy-posture Stop hook
# (autonomy-posture-check-layer-4.2.sh), running in WARN-ONLY mode.
#
# The hook NEVER blocks. It logs what it WOULD have blocked to:
#   telemetry:  $HOME/.claude/logs/autonomy-posture-layer42.jsonl
#   detections: $HOME/.claude/audit/autonomy-posture-layer42-detections.log
# Tests run against a SANDBOX HOME so the real logs are never touched.
#
# Scenarios (per task + spec §2.2-§2.4):
#   A — next-action claim + gates pass + NO tool_use  → would_block=1 logged,
#       response STILL passes (exit 0, no block JSON on stdout)
#   B — next-action claim + corresponding tool_use     → would_block=0
#   C — no next-action claim                           → silent (would_block=0, empty next_actions)
#   D — cross-human / L0 action (gates fail)           → would_block=0
#   E — bypass env set (AUTONOMY_POSTURE_L42_BYPASSED=1)→ silent, NO telemetry line written
#   F — stop_hook_active recursion guard               → silent, NO telemetry line written
#   G — missing transcript (fail open)                 → silent
#   H — malformed input JSON (fail open)               → silent
#
# Every case also asserts the hook EXITS 0 and emits NO {"decision":"block"}.
#
# Run: bash Core/frameworks/intent/tests/test_autonomy_posture_layer42.sh
# Exit: 0 = all pass, 1 = one or more fail

set -uo pipefail

# Resolve the hook. Prefer the symlinked ~/.claude/hooks/ copy (what runs live);
# fall back to the source path in the repo.
HOOK_SYMLINK="$HOME/.claude/hooks/autonomy-posture-check-layer-4.2.sh"
HOOK_SOURCE="/Users/brien/Workspaces/Core/frameworks/intent/hooks/autonomy-posture-check-layer-4.2.sh"
if [[ -x "$HOOK_SYMLINK" ]]; then
  HOOK="$HOOK_SYMLINK"
elif [[ -x "$HOOK_SOURCE" ]]; then
  HOOK="$HOOK_SOURCE"
else
  echo "ERROR: hook not found or not executable at either:" >&2
  echo "  $HOOK_SYMLINK" >&2
  echo "  $HOOK_SOURCE" >&2
  exit 2
fi
echo "Testing hook: $HOOK"

PASS=0
FAIL=0
pass() { printf '  PASS  %s\n' "$1"; PASS=$((PASS + 1)); }
fail() { printf '  FAIL  %s\n' "$1"; FAIL=$((FAIL + 1)); }

# Sandbox HOME so we never write to the real ~/.claude logs.
SANDBOX=$(mktemp -d)
SBHOME="$SANDBOX/home"
mkdir -p "$SBHOME"
TELEMETRY="$SBHOME/.claude/logs/autonomy-posture-layer42.jsonl"
DETECTIONS="$SBHOME/.claude/audit/autonomy-posture-layer42-detections.log"
trap 'rm -rf "$SANDBOX"' EXIT

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

# Build a one-assistant-message transcript JSONL.
#   $1 = assistant text
#   $2 = JSON array of additional content blocks (tool_use blocks), or "[]"
make_transcript() {
  local text="$1"
  local tools_json="$2"
  local path="$SANDBOX/transcript-$$-$RANDOM.jsonl"
  python3 -c "
import json, sys
text = sys.argv[1]
tools = json.loads(sys.argv[2])
content = [{'type': 'text', 'text': text}] + tools
print(json.dumps({'type': 'assistant', 'message': {'content': content}}))
" "$text" "$tools_json" > "$path"
  echo "$path"
}

# Build Stop-hook input JSON.
#   $1 = session id   $2 = transcript path   $3 = stop_hook_active (true|false, default false)
make_input() {
  local session_id="$1"
  local transcript_path="$2"
  local stop_active="${3:-false}"
  python3 -c "
import json, sys
print(json.dumps({
    'session_id': sys.argv[1],
    'transcript_path': sys.argv[2],
    'stop_hook_active': (sys.argv[3] == 'true')
}))
" "$session_id" "$transcript_path" "$stop_active"
}

# Run the hook with the sandbox HOME.
# Writes stdout to $RUN_OUT_FILE and the exit code to global LAST_EXIT.
# (Capturing via command substitution would subshell the LAST_EXIT assignment
#  away under `set -u`, so we route through a temp file in the parent shell.)
LAST_EXIT=0
RUN_OUT_FILE="$SANDBOX/run-out.txt"
run_hook() {
  local input_json="$1"
  local bypass="${2:-0}"
  printf '%s' "$input_json" | HOME="$SBHOME" AUTONOMY_POSTURE_L42_BYPASSED="$bypass" bash "$HOOK" >"$RUN_OUT_FILE" 2>/dev/null
  LAST_EXIT=$?
}

# Read the would_block / has_tool_use field of the LAST telemetry line for a session.
last_telemetry_field() {
  local session="$1"
  local field="$2"   # would_block | has_tool_use | gates_pass
  python3 -c "
import json, sys, os
path = sys.argv[1]; session = sys.argv[2]; field = sys.argv[3]
val = None
if os.path.exists(path):
    with open(path) as f:
        for line in f:
            line=line.strip()
            if not line: continue
            try: obj=json.loads(line)
            except Exception: continue
            if obj.get('session')==session:
                val=obj.get(field)
print('' if val is None else val)
" "$TELEMETRY" "$session" "$field"
}

# Count telemetry lines for a session.
telemetry_count_for() {
  local session="$1"
  python3 -c "
import json, sys, os
path=sys.argv[1]; session=sys.argv[2]; n=0
if os.path.exists(path):
    with open(path) as f:
        for line in f:
            line=line.strip()
            if not line: continue
            try: obj=json.loads(line)
            except Exception: continue
            if obj.get('session')==session: n+=1
print(n)
" "$TELEMETRY" "$session"
}

# Assert the hook NEVER emitted a block decision (warn-only invariant).
assert_no_block() {
  local label="$1"
  local output="$2"
  if printf '%s' "$output" | grep -q '"decision": *"block"'; then
    fail "$label — hook emitted a block decision (warn-only VIOLATED): $(printf '%s' "$output" | head -c 160)"
    return 1
  fi
  return 0
}

# ---------------------------------------------------------------------------
# CASE A — next-action claim + gates pass + NO tool_use → would_block=1 logged,
#          response STILL passes (exit 0, no block JSON, detection line written)
# ---------------------------------------------------------------------------
A_TEXT='Done with the audit. Next L4 move: I will write apply_lambda_settings.py to walk the .intent/ products and idempotently add the managed block. This is reversible, Workspaces-local, and L4-eligible.'
A_TRANSCRIPT=$(make_transcript "$A_TEXT" "[]")
A_INPUT=$(make_input "sessA" "$A_TRANSCRIPT")
run_hook "$A_INPUT"
A_EXIT=$LAST_EXIT
A_OUT=$(cat "$RUN_OUT_FILE")
A_WB=$(last_telemetry_field "sessA" "would_block")
A_DETECT_OK=0
if [[ -f "$DETECTIONS" ]] && grep -q "L42-WOULDBLOCK session=sessA" "$DETECTIONS"; then A_DETECT_OK=1; fi

if assert_no_block "CASE A" "$A_OUT"; then
  if [[ $A_EXIT -eq 0 ]] && [[ -z "$A_OUT" ]] && [[ "$A_WB" == "1" ]] && [[ $A_DETECT_OK -eq 1 ]]; then
    pass "CASE A: next-action + gates pass + no tool_use → would_block=1 logged, response passes"
  else
    fail "CASE A — exit=$A_EXIT would_block='$A_WB' detect_ok=$A_DETECT_OK stdout='$(printf '%s' "$A_OUT" | head -c 120)'"
  fi
fi

# ---------------------------------------------------------------------------
# CASE B — next-action claim + corresponding tool_use present → would_block=0
# ---------------------------------------------------------------------------
B_TEXT='I will write apply_lambda_settings.py now — it walks the .intent/ products. L4-eligible, Workspaces-local.'
B_TOOLS='[{"type":"tool_use","name":"Write","input":{"file_path":"/Users/brien/Workspaces/Core/products/x/apply_lambda_settings.py","content":"# impl"}}]'
B_TRANSCRIPT=$(make_transcript "$B_TEXT" "$B_TOOLS")
B_INPUT=$(make_input "sessB" "$B_TRANSCRIPT")
run_hook "$B_INPUT"
B_EXIT=$LAST_EXIT
B_OUT=$(cat "$RUN_OUT_FILE")
B_WB=$(last_telemetry_field "sessB" "would_block")
B_HT=$(last_telemetry_field "sessB" "has_tool_use")

if assert_no_block "CASE B" "$B_OUT"; then
  if [[ $B_EXIT -eq 0 ]] && [[ -z "$B_OUT" ]] && [[ "$B_WB" == "0" ]] && [[ "$B_HT" == "1" ]]; then
    pass "CASE B: next-action + corresponding tool_use → would_block=0 (has_tool_use=1)"
  else
    fail "CASE B — exit=$B_EXIT would_block='$B_WB' has_tool_use='$B_HT' stdout='$(printf '%s' "$B_OUT" | head -c 120)'"
  fi
fi

# ---------------------------------------------------------------------------
# CASE C — no next-action claim → silent (would_block=0, empty next_actions)
# ---------------------------------------------------------------------------
C_TEXT='Done. 4 commits landed across 4 repos. Signal closed. Filed the coverage-gap signal for the 12 products lacking an INTENT.md surface.'
C_TRANSCRIPT=$(make_transcript "$C_TEXT" "[]")
C_INPUT=$(make_input "sessC" "$C_TRANSCRIPT")
run_hook "$C_INPUT"
C_EXIT=$LAST_EXIT
C_OUT=$(cat "$RUN_OUT_FILE")
C_WB=$(last_telemetry_field "sessC" "would_block")
C_NA=$(last_telemetry_field "sessC" "next_actions")

if assert_no_block "CASE C" "$C_OUT"; then
  if [[ $C_EXIT -eq 0 ]] && [[ -z "$C_OUT" ]] && [[ "$C_WB" == "0" ]] && [[ "$C_NA" == "[]" ]]; then
    pass "CASE C: no next-action claim → silent (would_block=0, next_actions=[])"
  else
    fail "CASE C — exit=$C_EXIT would_block='$C_WB' next_actions='$C_NA' stdout='$(printf '%s' "$C_OUT" | head -c 120)'"
  fi
fi

# ---------------------------------------------------------------------------
# CASE D — cross-human / L0 action (gates fail) → would_block=0
#          (Slack/email in the head + no L4/autonomy precedent → local_blast &
#           precedent gates fail, so even with a next-action claim it won't block)
# ---------------------------------------------------------------------------
D_TEXT='Next, I will draft slack_ping.txt and send the email summary to Dean. This routes state to another human.'
D_TRANSCRIPT=$(make_transcript "$D_TEXT" "[]")
D_INPUT=$(make_input "sessD" "$D_TRANSCRIPT")
run_hook "$D_INPUT"
D_EXIT=$LAST_EXIT
D_OUT=$(cat "$RUN_OUT_FILE")
D_WB=$(last_telemetry_field "sessD" "would_block")

if assert_no_block "CASE D" "$D_OUT"; then
  if [[ $D_EXIT -eq 0 ]] && [[ -z "$D_OUT" ]] && [[ "$D_WB" == "0" ]]; then
    pass "CASE D: cross-human / L0 action (gates fail) → would_block=0"
  else
    fail "CASE D — exit=$D_EXIT would_block='$D_WB' stdout='$(printf '%s' "$D_OUT" | head -c 120)'"
  fi
fi

# ---------------------------------------------------------------------------
# CASE E — bypass env set → silent, NO telemetry line written
# ---------------------------------------------------------------------------
E_TEXT='Next L4 move: I will write bypassed.py — Workspaces-local, .intent, L4-eligible.'
E_TRANSCRIPT=$(make_transcript "$E_TEXT" "[]")
E_INPUT=$(make_input "sessE" "$E_TRANSCRIPT")
run_hook "$E_INPUT" 1   # bypass=1
E_EXIT=$LAST_EXIT
E_OUT=$(cat "$RUN_OUT_FILE")
E_COUNT=$(telemetry_count_for "sessE")

if assert_no_block "CASE E" "$E_OUT"; then
  if [[ $E_EXIT -eq 0 ]] && [[ -z "$E_OUT" ]] && [[ "$E_COUNT" == "0" ]]; then
    pass "CASE E: bypass env set → silent, no telemetry written"
  else
    fail "CASE E — exit=$E_EXIT telemetry_lines=$E_COUNT stdout='$(printf '%s' "$E_OUT" | head -c 120)'"
  fi
fi

# ---------------------------------------------------------------------------
# CASE F — stop_hook_active recursion guard → silent, NO telemetry line written
# ---------------------------------------------------------------------------
F_TEXT='Next L4 move: I will write recursion.py — Workspaces-local, .intent, L4-eligible.'
F_TRANSCRIPT=$(make_transcript "$F_TEXT" "[]")
F_INPUT=$(make_input "sessF" "$F_TRANSCRIPT" "true")   # stop_hook_active=true
run_hook "$F_INPUT"
F_EXIT=$LAST_EXIT
F_OUT=$(cat "$RUN_OUT_FILE")
F_COUNT=$(telemetry_count_for "sessF")

if assert_no_block "CASE F" "$F_OUT"; then
  if [[ $F_EXIT -eq 0 ]] && [[ -z "$F_OUT" ]] && [[ "$F_COUNT" == "0" ]]; then
    pass "CASE F: stop_hook_active recursion guard → silent, no telemetry written"
  else
    fail "CASE F — exit=$F_EXIT telemetry_lines=$F_COUNT stdout='$(printf '%s' "$F_OUT" | head -c 120)'"
  fi
fi

# ---------------------------------------------------------------------------
# CASE G — missing transcript → fail open (silent)
# ---------------------------------------------------------------------------
G_INPUT=$(make_input "sessG" "/nonexistent/path/does-not-exist.jsonl")
run_hook "$G_INPUT"
G_EXIT=$LAST_EXIT
G_OUT=$(cat "$RUN_OUT_FILE")
if assert_no_block "CASE G" "$G_OUT"; then
  if [[ $G_EXIT -eq 0 ]] && [[ -z "$G_OUT" ]]; then
    pass "CASE G: missing transcript → fail open (silent)"
  else
    fail "CASE G — exit=$G_EXIT stdout='$(printf '%s' "$G_OUT" | head -c 120)'"
  fi
fi

# ---------------------------------------------------------------------------
# CASE H — malformed input JSON → fail open (silent)
# ---------------------------------------------------------------------------
H_OUT=$(printf '%s' 'not json at all {{{' | HOME="$SBHOME" bash "$HOOK" 2>/dev/null)
H_EXIT=$?
if assert_no_block "CASE H" "$H_OUT"; then
  if [[ $H_EXIT -eq 0 ]] && [[ -z "$H_OUT" ]]; then
    pass "CASE H: malformed input JSON → fail open (silent)"
  else
    fail "CASE H — exit=$H_EXIT stdout='$(printf '%s' "$H_OUT" | head -c 120)'"
  fi
fi

# ---------------------------------------------------------------------------
# Summary
# ---------------------------------------------------------------------------
echo
echo "  Total: $((PASS + FAIL))  PASS: $PASS  FAIL: $FAIL"

if [[ $FAIL -gt 0 ]]; then
  exit 1
fi
exit 0
