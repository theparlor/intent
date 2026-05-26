#!/usr/bin/env bash
# signal-recorder-silent-check.sh
#
# PreToolUse hook — Witness mandatory-recorder enforcement per WS-DDR-098.
#
# Detects intent-decorated-but-silent products: products that have declared
# `lambda_settings:` in their .intent/INTENT.md (or autonomy_grants:) but have
# emitted no signal to their .intent/signals/ directory in the last N days.
#
# Surfaces the silent-recorder gap as an actionable signal rather than blocking
# the action — the rule is "products MUST route through Witness," not "blocking
# every action until they do." The catch-net is observability; the user/agent
# is informed and the gap surfaces as a follow-up signal candidate.
#
# Per WS-DDR-098: products that emit autonomy decisions MUST route through
# Witness; non-routing products are Intent-decorated, not Intent-enabled.
# Engagement-scoped products (Work/.../Engagements/[Client]/.intent/) are
# EXEMPT from this enforcement.
#
# Spec: Workspaces/.context/DECISIONS.md WS-DDR-098
# Signal: .intent/signals/SIG-2026-05-26-flight-model-ingestion.md
# Companion: Core/frameworks/intent/hooks/autonomy-grant-stop-check.sh (Layer 4)
#
# Install: chmod +x and symlink to ~/.claude/hooks/
# Register: add PreToolUse entry to ~/.claude/settings.json with matcher
#   limited to high-leverage tool calls (Bash for git, Edit/Write on
#   .intent/, etc.) to avoid running on every tool call.
#
# Bypass: SIGNAL_RECORDER_SILENT_BYPASSED=1
# Audit log: ~/.claude/audit/signal-recorder-silent-detections.log
# Telemetry: ~/.claude/logs/signal-recorder-silent.jsonl
#
# Posture: WARN-ONLY (does not block). The recorder-MANDATORY rule is policy;
# the hook surfaces gaps but never blocks legitimate work — blocking would
# create exactly the Drag (caution overhead) the flight-model spec penalizes.
#
# Created: 2026-05-26 — companion to WS-DDR-098 ratification.

set -u

AUDIT_LOG="$HOME/.claude/audit/signal-recorder-silent-detections.log"
TELEMETRY_LOG="$HOME/.claude/logs/signal-recorder-silent.jsonl"
mkdir -p "$(dirname "$AUDIT_LOG")" 2>/dev/null || true
mkdir -p "$(dirname "$TELEMETRY_LOG")" 2>/dev/null || true

# Bypass
if [ "${SIGNAL_RECORDER_SILENT_BYPASSED:-0}" = "1" ]; then
  exit 0
fi

# Read input JSON from stdin
INPUT=$(cat)

# Threshold: products silent for >30 days are flagged
STALE_DAYS=30

# Parse input to extract working directory hint (best-effort)
WORK_DIR=$(python3 -c "
import json, sys, os
try:
    d = json.loads(sys.stdin.read() or '{}')
    # PreToolUse hook gets tool_input — try to extract a file path
    tool_input = d.get('tool_input', {})
    path = (tool_input.get('file_path') or tool_input.get('path') or
            tool_input.get('command', '').split()[1] if tool_input.get('command') else None)
    if path and os.path.exists(path):
        # Walk up to find a directory containing .intent/
        cur = os.path.dirname(os.path.abspath(path))
        while cur and cur != '/':
            if os.path.isdir(os.path.join(cur, '.intent')):
                print(cur)
                sys.exit(0)
            cur = os.path.dirname(cur)
    print('')
except Exception:
    print('')
" <<< "$INPUT" 2>/dev/null)

TIMESTAMP=$(date -u +%Y-%m-%dT%H:%M:%SZ)

# No working dir resolved → exit cleanly (no detection possible)
if [ -z "$WORK_DIR" ] || [ ! -d "$WORK_DIR/.intent" ]; then
  # Telemetry: still emit so frequency trends observable
  printf '{"ts":"%s","work_dir":"","detection":"no-context","outcome":"skip"}\n' "$TIMESTAMP" >> "$TELEMETRY_LOG" 2>/dev/null || true
  exit 0
fi

# Exempt engagement-scoped paths
case "$WORK_DIR" in
  */Work/*/Engagements/*)
    printf '{"ts":"%s","work_dir":"%s","detection":"engagement-exempt","outcome":"skip"}\n' "$TIMESTAMP" "$WORK_DIR" >> "$TELEMETRY_LOG" 2>/dev/null || true
    exit 0
    ;;
esac

INTENT_DIR="$WORK_DIR/.intent"
INTENT_MD="$INTENT_DIR/INTENT.md"

# Check if this product has declared lambda_settings or autonomy_grants
DECLARES_LAMBDA=0
if [ -f "$INTENT_MD" ]; then
  if grep -qE "^(lambda_settings|autonomy_grants):" "$INTENT_MD" 2>/dev/null; then
    DECLARES_LAMBDA=1
  fi
fi

# Not a flight-model-eligible product → exit cleanly
if [ "$DECLARES_LAMBDA" = "0" ]; then
  printf '{"ts":"%s","work_dir":"%s","detection":"no-lambda-declaration","outcome":"skip"}\n' "$TIMESTAMP" "$WORK_DIR" >> "$TELEMETRY_LOG" 2>/dev/null || true
  exit 0
fi

# Check signal emission recency
SIGNALS_DIR="$INTENT_DIR/signals"
LATEST_SIG_DAYS=999
if [ -d "$SIGNALS_DIR" ]; then
  # Find newest SIG-*.md file mtime in days
  LATEST_MTIME=$(find "$SIGNALS_DIR" -name "SIG-*.md" -type f -print0 2>/dev/null | xargs -0 ls -t 2>/dev/null | head -1)
  if [ -n "$LATEST_MTIME" ]; then
    LATEST_SIG_DAYS=$(python3 -c "
import os, sys, time
try:
    age = (time.time() - os.path.getmtime('$LATEST_MTIME')) / 86400
    print(int(age))
except Exception:
    print(999)
")
  fi
fi

# Within threshold → exit cleanly
if [ "$LATEST_SIG_DAYS" -le "$STALE_DAYS" ]; then
  printf '{"ts":"%s","work_dir":"%s","detection":"recorder-active","latest_sig_days":%d,"outcome":"skip"}\n' "$TIMESTAMP" "$WORK_DIR" "$LATEST_SIG_DAYS" >> "$TELEMETRY_LOG" 2>/dev/null || true
  exit 0
fi

# Silent recorder detected — surface warning (warn-only, do not block)
echo "[$TIMESTAMP] SILENT-RECORDER work_dir=$WORK_DIR latest_sig_days=$LATEST_SIG_DAYS declares_lambda=1" >> "$AUDIT_LOG"
printf '{"ts":"%s","work_dir":"%s","detection":"silent-recorder","latest_sig_days":%d,"outcome":"warn"}\n' "$TIMESTAMP" "$WORK_DIR" "$LATEST_SIG_DAYS" >> "$TELEMETRY_LOG" 2>/dev/null || true

# Warn-only output to stderr — surfaces to user without blocking tool call
cat >&2 <<EOF
[Witness mandatory-recorder warning — WS-DDR-098]
Product at $WORK_DIR has declared lambda_settings/autonomy_grants but
its .intent/signals/ has not emitted a SIG-*.md in $LATEST_SIG_DAYS days
(threshold: $STALE_DAYS days).

Per WS-DDR-098 the product is Intent-decorated, not Intent-enabled, until
it routes through Witness. Tool call NOT blocked — this is observability,
not enforcement. Capture a signal documenting recent autonomy decisions
to clear the gap.
EOF

# Exit 0 — warn-only posture, do not block the tool call
exit 0
