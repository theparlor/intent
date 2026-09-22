#!/usr/bin/env bash
# session-cap-wake-check.sh
#
# PostToolUse hook, fires after Workflow, Agent, and Bash tool calls (matcher
# registered in ~/.claude/settings.json as "Workflow|Agent|Bash").
#
# Detects the five-hour session cap failure text ("You've hit your session
# limit, resets HH:MM" or "resets 6pm") in a tool result, parses the local
# reset time out of it, and arms a detached background sleep that fires at
# reset time plus sixty seconds. On exit that sleep re-invokes the session so
# it resumes its own queue without Brien acting as the alarm clock. No model
# judgement in the loop: pure text match plus deterministic time arithmetic.
#
# No existing wake or resume mechanism was found in this hooks tree or in
# Core/products/quartermaster (checked before writing this). The re-invocation
# step therefore uses the documented Claude Code CLI resume path:
#   claude --resume <session-id> -p "<prompt>"
# per `claude --help` (-r/--resume: "Resume a conversation by session ID";
# -p/--print: "Print response and exit"). If a durable in-harness wake
# primitive is added later, point SESSION_CAP_WAKE_RESUME_CMD at it instead
# of changing this script's default.
#
# Idempotent per reset time: one arm per parsed reset epoch. A marker file
# under $HOME/.claude/audit/session-cap-wake-state/ names the reset epoch;
# a second 429 naming the same reset time is logged as a skip, not re-armed.
#
# Install:
#   chmod +x Core/frameworks/intent/hooks/session-cap-wake-check.sh
#   ln -s "$PWD/Core/frameworks/intent/hooks/session-cap-wake-check.sh" \
#         ~/.claude/hooks/session-cap-wake-check.sh
#
# Register: add to ~/.claude/settings.json under hooks -> PostToolUse,
#   matcher "Workflow|Agent|Bash"
#
# Bypass: SESSION_CAP_WAKE_BYPASSED=1
# Role gate: arms only when the machine-role helper reports hub or travel;
#   embassy and unknown log a SKIP and exit 0.
# Audit log: ~/.claude/audit/session-cap-wakes.log
# State dir (idempotency markers): ~/.claude/audit/session-cap-wake-state/
#
# Test overrides (used only by tests/test_session_cap_wake_check.py, never
# by a real hook invocation):
#   SESSION_CAP_WAKE_NOW_EPOCH               fixes "now" for deterministic parsing
#   SESSION_CAP_WAKE_SLEEP_OVERRIDE_SECONDS  fixes the background sleep duration
#   SESSION_CAP_WAKE_RESUME_CMD              replaces the claude --resume invocation
#
# Signal: ~/Workspaces/.intent/signals/SIG-SESSION-CAP-NO-AUTO-RESUME-2026-09-02.md
# Queue task: QMT-01M1JK4DSV08TEW1R4RP5KCWNM
# Memory rule this makes mechanical: reference_five_hour_cap_binds_fanout.md,
#   feedback_schedule_wakeup_on_rate_limit.md
#
# Created: 2026-09-13

set -u

AUDIT_LOG="$HOME/.claude/audit/session-cap-wakes.log"
STATE_DIR="$HOME/.claude/audit/session-cap-wake-state"
mkdir -p "$(dirname "$AUDIT_LOG")" 2>/dev/null || true
mkdir -p "$STATE_DIR" 2>/dev/null || true

log() {
  local ts
  ts=$(date -u +%Y-%m-%dT%H:%M:%SZ)
  echo "[$ts] $1" >> "$AUDIT_LOG"
}

# Bypass
if [ "${SESSION_CAP_WAKE_BYPASSED:-0}" = "1" ]; then
  log "BYPASS env-flag set"
  exit 0
fi

# Role gate (P4): only the hub and the travel spoke ever arm a background
# resume. An embassy or an unrecognised machine (absent or unparseable
# ~/.claude/machine.json, or no helper on disk) skips, so a client-owned
# machine never gets a detached claude --resume.
_role_helper="${CLAUDE_CONFIG_DIR:-$HOME/.claude}/hooks/helpers/machine-role.sh"
if [ -r "$_role_helper" ]; then
  # shellcheck source=/dev/null
  . "$_role_helper" || MACHINE_ROLE=unknown
else
  MACHINE_ROLE=unknown
fi
case "${MACHINE_ROLE:-unknown}" in
  hub|travel) ;;
  *) log "SKIP role=${MACHINE_ROLE:-unknown} never arms a background resume"; exit 0 ;;
esac

# Read tool input/response JSON from stdin.
INPUT=$(cat)

# Pull session_id, tool_name, and a flattened text blob covering tool_response
# (and tool_input, defensively) so the grep below works regardless of which
# tool shape carried the 429 text -- Bash puts it in stdout/stderr, Agent and
# Workflow results carry it in nested content blocks.
PARSED=$(python3 -c "
import json, sys
try:
    d = json.loads(sys.stdin.read() or '{}')
except Exception:
    d = {}
sid = d.get('session_id', 'unknown')
tname = d.get('tool_name', '')
blob_parts = []
for key in ('tool_response', 'tool_output', 'tool_input'):
    if key in d:
        try:
            blob_parts.append(json.dumps(d[key]))
        except Exception:
            blob_parts.append(str(d[key]))
blob = ' '.join(blob_parts)
print(sid)
print(tname)
print(blob)
" <<< "$INPUT" 2>/dev/null)

SESSION_ID=$(printf '%s\n' "$PARSED" | sed -n '1p')
TOOL_NAME=$(printf '%s\n' "$PARSED" | sed -n '2p')
TEXT_BLOB=$(printf '%s\n' "$PARSED" | sed -n '3,$p')

[ -z "$SESSION_ID" ] && SESSION_ID="unknown"

# Defensive tool-name gate -- the settings.json matcher already restricts
# invocation to Workflow|Agent|Bash, but a wildcard matcher or a direct test
# invocation may call this hook for other tools. Only Workflow/Agent/Bash
# results ever carry a Claude Code session-cap 429.
if [ -n "$TOOL_NAME" ]; then
  case "$TOOL_NAME" in
    Workflow|Agent|Bash) : ;;
    *) exit 0 ;;
  esac
fi

[ -z "$TEXT_BLOB" ] && exit 0

# Fast substring gate before the more expensive python parse.
LOWER_BLOB=$(printf '%s' "$TEXT_BLOB" | tr '[:upper:]' '[:lower:]')
case "$LOWER_BLOB" in
  *"session limit"*"resets"*) : ;;
  *"resets"*"session limit"*) : ;;
  *) exit 0 ;;
esac

# ---------------------------------------------------------------------------
# Parse the reset time out of the text. Handles "resets 6pm", "resets 6:30pm",
# "resets 18:00", "resets 6" (ambiguous -- picks the soonest future candidate
# between AM and PM interpretations).
# ---------------------------------------------------------------------------
NOW_OVERRIDE="${SESSION_CAP_WAKE_NOW_EPOCH:-}"

PARSE_OUT=$(python3 -c "
import re, sys, time, datetime

text = sys.stdin.read()
now_override = '''${NOW_OVERRIDE}'''.strip()
now_ts = float(now_override) if now_override else time.time()
now_dt = datetime.datetime.fromtimestamp(now_ts)

m = re.search(r'resets?\s*(?:at\s+)?(\d{1,2})(?::(\d{2}))?\s*([aApP]\.?[mM]\.?)?', text)
if not m:
    print('NOPARSE')
    sys.exit(0)

hour = int(m.group(1))
minute = int(m.group(2)) if m.group(2) else 0
ampm_raw = (m.group(3) or '').lower().replace('.', '')

def next_occurrence(hour24, minute):
    target = now_dt.replace(hour=hour24, minute=minute, second=0, microsecond=0)
    if target <= now_dt:
        target = target + datetime.timedelta(days=1)
    return target

if ampm_raw == 'am':
    hour24 = 0 if hour == 12 else hour
    target = next_occurrence(hour24, minute)
elif ampm_raw == 'pm':
    hour24 = 12 if hour == 12 else hour + 12
    target = next_occurrence(hour24, minute)
elif hour > 12 or hour == 0:
    # unambiguous 24-hour form, e.g. 'resets 18:00'
    target = next_occurrence(hour, minute)
else:
    # ambiguous 1-12 with no am/pm marker: soonest future of the two readings
    cand_am = next_occurrence(hour % 12, minute)
    cand_pm = next_occurrence((hour % 12) + 12, minute)
    target = min(cand_am, cand_pm)

print('OK')
print(int(target.timestamp()))
print(m.group(0))
" <<< "$TEXT_BLOB" 2>/dev/null)

STATUS=$(printf '%s\n' "$PARSE_OUT" | sed -n '1p')

if [ "$STATUS" != "OK" ]; then
  log "NOPARSE session=$SESSION_ID tool=$TOOL_NAME (matched session-limit/resets substrings but could not parse a time)"
  exit 0
fi

RESET_EPOCH=$(printf '%s\n' "$PARSE_OUT" | sed -n '2p')
RESET_MATCH=$(printf '%s\n' "$PARSE_OUT" | sed -n '3p')

if ! [[ "$RESET_EPOCH" =~ ^[0-9]+$ ]]; then
  log "NOPARSE session=$SESSION_ID tool=$TOOL_NAME (reset epoch computation failed)"
  exit 0
fi

# ---------------------------------------------------------------------------
# Idempotency: one arm per reset epoch. Atomic create via noclobber.
# ---------------------------------------------------------------------------
MARKER="$STATE_DIR/armed-${RESET_EPOCH}.marker"

if [ -e "$MARKER" ]; then
  log "SKIP-IDEMPOTENT session=$SESSION_ID tool=$TOOL_NAME reset_epoch=$RESET_EPOCH marker=$MARKER already armed"
  exit 0
fi

if ! ( set -o noclobber; : > "$MARKER" ) 2>/dev/null; then
  log "SKIP-RACE session=$SESSION_ID tool=$TOOL_NAME reset_epoch=$RESET_EPOCH marker=$MARKER lost the create race"
  exit 0
fi
echo "session=$SESSION_ID tool=$TOOL_NAME reset_match='$RESET_MATCH' armed_at=$(date -u +%Y-%m-%dT%H:%M:%SZ)" > "$MARKER"

# ---------------------------------------------------------------------------
# Compute sleep duration (reset + 60s buffer) and arm the detached wake.
# ---------------------------------------------------------------------------
WAKE_EPOCH=$((RESET_EPOCH + 60))

if [ -n "${SESSION_CAP_WAKE_SLEEP_OVERRIDE_SECONDS:-}" ]; then
  SLEEP_SECONDS="$SESSION_CAP_WAKE_SLEEP_OVERRIDE_SECONDS"
else
  NOW_EPOCH=$(python3 -c "print(int(float('''${NOW_OVERRIDE:-0}''' or __import__('time').time())))" 2>/dev/null)
  [ -z "$NOW_EPOCH" ] && NOW_EPOCH=$(date -u +%s)
  SLEEP_SECONDS=$((WAKE_EPOCH - NOW_EPOCH))
  [ "$SLEEP_SECONDS" -lt 1 ] && SLEEP_SECONDS=1
fi

if [ -n "${SESSION_CAP_WAKE_RESUME_CMD:-}" ]; then
  RESUME_LINE="$SESSION_CAP_WAKE_RESUME_CMD"
else
  RESUME_LINE='claude --resume "'"${SESSION_ID}"'" -p "SESSION_CAP_WAKE: five-hour cap reset. Resume the Quartermaster queue and any dropped Workflow/Agent work."'
fi

WAKE_SCRIPT="$STATE_DIR/wake-${RESET_EPOCH}.sh"
cat > "$WAKE_SCRIPT" <<EOS
#!/usr/bin/env bash
sleep ${SLEEP_SECONDS}
echo "[\$(date -u +%Y-%m-%dT%H:%M:%SZ)] WAKE-FIRED session=${SESSION_ID} tool=${TOOL_NAME} reset_epoch=${RESET_EPOCH}" >> "${AUDIT_LOG}"
${RESUME_LINE} >> "${AUDIT_LOG}" 2>&1
echo "[\$(date -u +%Y-%m-%dT%H:%M:%SZ)] RESUME-INVOKED session=${SESSION_ID} rc=\$?" >> "${AUDIT_LOG}"
rm -f "${WAKE_SCRIPT}"
EOS
chmod +x "$WAKE_SCRIPT"

nohup "$WAKE_SCRIPT" >/dev/null 2>&1 &
disown 2>/dev/null || true

log "ARMED session=$SESSION_ID tool=$TOOL_NAME reset_match='$RESET_MATCH' reset_epoch=$RESET_EPOCH wake_epoch=$WAKE_EPOCH sleep_seconds=$SLEEP_SECONDS marker=$MARKER wake_script=$WAKE_SCRIPT"

exit 0
