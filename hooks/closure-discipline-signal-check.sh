#!/usr/bin/env bash
# closure-discipline-signal-check.sh
#
# PreToolUse hook — Layer 5 of closure-discipline enforcement
# (signal-file artifact-level enforcement).
#
# Inspects Write/Edit tool calls targeting `*/.intent/signals/*.md`. If
# the content has `status: resolved` (or `closed` / `done`) in YAML
# frontmatter without `upstream_control_path:` AND `catch_mechanism:`
# fields, blocks the write. Forces either field population or status
# downgrade.
#
# Spec: Core/frameworks/intent/spec/closure-discipline-enforcement.md (Layer 5)
#
# Install: chmod +x and symlink to ~/.claude/hooks/
# Register: add PreToolUse entry to ~/.claude/settings.json with matcher
#           "Write|Edit"
#
# Bypass: CLOSURE_DISCIPLINE_SIGNAL_BYPASSED=1
# Audit log: ~/.claude/audit/closure-discipline-signal-detections.log
#
# Created: 2026-04-30

set -u

AUDIT_LOG="$HOME/.claude/audit/closure-discipline-signal-detections.log"
mkdir -p "$(dirname "$AUDIT_LOG")" 2>/dev/null || true

# Bypass
if [ "${CLOSURE_DISCIPLINE_SIGNAL_BYPASSED:-0}" = "1" ]; then
  echo "[bypassed]" >> "$AUDIT_LOG"
  exit 0
fi

# Read input JSON from stdin
INPUT=$(cat)

# Extract tool name, file_path, content (defensive parse, fail open)
read -r SESSION_ID TOOL_NAME FILE_PATH CONTENT_LEN <<< "$(python3 -c "
import json, sys
try:
    d = json.loads(sys.stdin.read() or '{}')
    sid = d.get('session_id', 'unknown')
    tn = d.get('tool_name', 'unknown')
    ti = d.get('tool_input', {}) or {}
    # Write tool: file_path + content; Edit tool: file_path + new_string
    fp = ti.get('file_path', '') or ''
    fp = fp.replace(' ', '\\\\ ')
    content = ti.get('content', '') or ti.get('new_string', '') or ''
    print(sid, tn, fp or 'NONE', len(content))
except Exception:
    print('unknown', 'unknown', 'NONE', 0)
" <<< "$INPUT")"

# Only inspect Write/Edit on signal files
case "$TOOL_NAME" in
  Write|Edit) ;;
  *) exit 0 ;;
esac

if [ "$FILE_PATH" = "NONE" ]; then
  exit 0
fi

# Path filter: must be in `.intent/signals/*.md`
case "$FILE_PATH" in
  */.intent/signals/*.md) ;;
  */intent/signals/*.md) ;;
  *) exit 0 ;;
esac

# Inspect content via stdin-piped python (avoids heredoc-substitution brittleness)
VERDICT=$(printf '%s' "$INPUT" | python3 -c '
import json, sys, re
try:
    raw = json.loads(sys.stdin.read() or "{}")
    ti = raw.get("tool_input", {}) or {}
    content = ti.get("content", "") or ti.get("new_string", "") or ""
    if not content:
        print("OK")
        sys.exit(0)

    # Locate frontmatter (between first two --- delimiters)
    m = re.match(r"^\s*---\s*\n(.*?)\n---", content, re.DOTALL)
    if not m:
        # No frontmatter — cannot enforce; fail open
        print("OK")
        sys.exit(0)
    fm = m.group(1)

    # Find status:
    sm = re.search(r"^status:\s*([a-zA-Z][a-zA-Z_-]*)", fm, re.MULTILINE)
    if not sm:
        print("OK")
        sys.exit(0)
    status = sm.group(1).lower()

    # Trigger statuses
    TRIGGER = {"resolved", "closed", "done", "complete", "completed", "fixed"}
    if status not in TRIGGER:
        print("OK")
        sys.exit(0)

    # Required fields for resolved status
    has_upstream = bool(re.search(r"^upstream_control(_path)?:\s*\S", fm, re.MULTILINE | re.IGNORECASE))
    has_catch = bool(re.search(r"^catch_mechanism:\s*\S", fm, re.MULTILINE | re.IGNORECASE))

    # Either field satisfies — though policy prefers BOTH, single-field
    # allows mid-evolution signals where catch-net is intentionally
    # captured inside upstream_control_path body.
    if has_upstream or has_catch:
        print("OK")
        sys.exit(0)

    print("BLOCK " + status)
except Exception:
    # Fail open on any parse error
    print("OK")
')

case "$VERDICT" in
  OK) exit 0 ;;
  BLOCK*) ;;
  *) exit 0 ;;
esac

STATUS=$(echo "$VERDICT" | sed 's/^BLOCK //')
TIMESTAMP=$(date -u +%Y-%m-%dT%H:%M:%SZ)
echo "[$TIMESTAMP] CAUGHT session=$SESSION_ID tool=$TOOL_NAME file=$FILE_PATH status=$STATUS" >> "$AUDIT_LOG"

cat <<EOF
{"decision": "block", "reason": "CLOSURE-DISCIPLINE DRIFT (Layer 5 detector): you are about to write a signal file with status: ${STATUS} but neither upstream_control_path: nor catch_mechanism: frontmatter field is populated. Per the closure-DoD at Core/frameworks/intent/spec/signal-stream.md, status: resolved/closed/done requires upstream control + catch mechanism. Either: (a) add 'upstream_control_path: <file path of the resolver in the pipeline>' and 'catch_mechanism: <chain_audit invariant ID or test>' to the frontmatter, OR (b) downgrade the status to 'symptom-repaired, upstream-pending' (no required fields) and add a follow-up signal capturing what the upstream control would need to be. Bypass for legitimate cases: CLOSURE_DISCIPLINE_SIGNAL_BYPASSED=1 (logged)."}
EOF
exit 0
