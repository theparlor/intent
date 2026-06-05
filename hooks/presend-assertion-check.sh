#!/usr/bin/env bash
# presend-assertion-check.sh
#
# Stop hook — pre-send assertion audit (response linter).
#
# Detects when a response presents CLIENT-FACING SEND-READY content
# (a draft/message/reply the user is meant to paste or send to another
# human) WITHOUT evidence that its load-bearing factual claims were
# sourced. Forces a per-claim source pass before client-facing assertions
# leave the building.
#
# Pattern caught: response contains a send-ready marker ("paste-ready",
# "ready to send", "send this to Greg", a quoted reply block) AND contains
# no pre-send assertion-audit marker anywhere in the body.
#
# Origin: SIG-2026-06-04-assert-from-inference-drift — model asserted
# "the recommendation doesn't touch Build" from ABSENCE of evidence (never
# verified what Build was), and separately claimed an edit it had not made.
# Memory + the OBSERVED/IMPLIED/GAP discipline did not prevent it; the only
# catch was human challenge. This hook is the mechanism-level fix Brien
# approved 2026-06-05.
#
# Conservative by design: suppresses ONLY on an explicit assertion-audit
# marker, so loose "verified" usage still trips it. Errs toward firing.
#
# Spec: Core/frameworks/intent/spec/presend-assertion-audit.md
# Bypass: PRESEND_ASSERTION_BYPASSED=1
# Audit log: ~/.claude/audit/presend-assertion-detections.log

set -u

AUDIT_LOG="$HOME/.claude/audit/presend-assertion-detections.log"
mkdir -p "$(dirname "$AUDIT_LOG")" 2>/dev/null || true

if [ "${PRESEND_ASSERTION_BYPASSED:-0}" = "1" ]; then
  exit 0
fi

INPUT=$(cat)

read -r SESSION_ID TRANSCRIPT_PATH STOP_ACTIVE <<< "$(python3 -c "
import json, sys
try:
    d = json.loads(sys.stdin.read() or '{}')
    sid = d.get('session_id', 'unknown')
    tpath = d.get('transcript_path', '') or 'NONE'
    sactive = d.get('stop_hook_active', False)
    tpath = tpath.replace(' ', '\\\\ ')
    print(sid, tpath, 'true' if sactive else 'false')
except Exception:
    print('unknown', 'NONE', 'false')
" <<< "$INPUT")"

# Recursion guard
if [ "$STOP_ACTIVE" = "true" ]; then
  exit 0
fi

if [ "$TRANSCRIPT_PATH" = "NONE" ] || [ ! -f "$TRANSCRIPT_PATH" ]; then
  exit 0
fi

LAST_TEXT=$(python3 -c "
import json, sys
try:
    path = sys.argv[1]
    last_assistant = None
    with open(path) as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                obj = json.loads(line)
            except Exception:
                continue
            if obj.get('type') == 'assistant':
                last_assistant = obj
    if not last_assistant:
        sys.exit(0)
    msg = last_assistant.get('message', {})
    content = msg.get('content', [])
    if isinstance(content, str):
        print(content)
    elif isinstance(content, list):
        texts = []
        for block in content:
            if isinstance(block, dict) and block.get('type') == 'text':
                texts.append(block.get('text', ''))
        print('\n'.join(texts))
except Exception:
    sys.exit(0)
" "$TRANSCRIPT_PATH" 2>/dev/null)

if [ -z "$LAST_TEXT" ]; then
  exit 0
fi

LOWER_FULL=$(printf '%s' "$LAST_TEXT" | tr '[:upper:]' '[:lower:]')

# SEND marker — content is being handed to a human to paste/send.
# High-confidence phrases only, to keep false-positive friction low.
SEND_RE=$'(paste-ready|paste ready|ready to send|send-ready|send ready|ready to paste|send (this|that|it) (to|over)|send the (reply|message|email|note)|for you to send|you can send (this|that|it)|then send (this|that|it)|drop (this|that) to|reply (for|to) (greg|dean|kevin|natalie|the client|him|her|them)|message (for|to) (greg|dean|the client))'

# ASSERTION-AUDIT marker — explicit evidence the claims were sourced.
# Conservative: strong markers only, so loose "verified" does NOT suppress.
AUDIT_RE=$'(assertion[- ]audit|pre-?send (assertion|audit|check)|per[- ]claim source|claim[- ]by[- ]claim|each (factual |load-bearing )?claim (is |was )?sourced|claims sourced|sourced each (claim|assertion)|source-?audited|verified note —|verified note \(|✓ sourced|sources verified before)'

SEND_MATCH=0
if echo "$LOWER_FULL" | grep -qiE "$SEND_RE"; then
  SEND_MATCH=1
fi

AUDIT_MATCH=0
if echo "$LOWER_FULL" | grep -qiE "$AUDIT_RE"; then
  AUDIT_MATCH=1
fi

# Trigger: send-ready client content present AND no assertion-audit marker
if [ "$SEND_MATCH" = "1" ] && [ "$AUDIT_MATCH" = "0" ]; then
  TIMESTAMP=$(date -u +%Y-%m-%dT%H:%M:%SZ)
  echo "[$TIMESTAMP] CAUGHT-PRESEND session=$SESSION_ID" >> "$AUDIT_LOG"

  cat <<'EOF'
{"decision": "block", "reason": "PRE-SEND ASSERTION DRIFT: this response presents client-facing send-ready content (a reply/message to be sent to another human) but shows no pre-send assertion audit. Before client-facing assertions leave the building, run the audit: enumerate every load-bearing factual claim in the draft and, for EACH, state its basis — verified (with the file/ticket/source you actually checked), inferred (and label it as inference), or unknown (and either cut it or turn it into a question). Any claim drawn from NOT-finding something (absence) is not verified — flag it. Then revise unsourced assertions to be sourced or hedged, add a short 'assertion-audit' / 'verified note' line, and re-present. Origin: SIG-2026-06-04-assert-from-inference-drift (asserted 'doesn't touch Build' from absence). Bypass with PRESEND_ASSERTION_BYPASSED=1 only if the content carries no factual claims."}
EOF
  exit 0
fi

exit 0
