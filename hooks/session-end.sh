#!/usr/bin/env bash
# hooks/session-end.sh — Tier 1 session.end event emitter
#
# Emits an OTel-shaped `session.end` event to <product>/.intent/events/events.jsonl
# at the close of an agent session. Installed per-product by `bin/intent-init`:
#
#   cp hooks/session-end.sh <product>/.claude/hooks/session-end
#   chmod +x <product>/.claude/hooks/session-end
#
# Then wired into the product's Claude Code Stop hook (or invoked at end of any
# agent session that touches the product). The hook is the Tier 1 capture surface
# documented in playbooks/spawn-a-product.md.
#
# Event schema (per DEC-004 + spawn-a-product runbook):
#   {
#     "version": "0.1.0",
#     "event": "session.end",
#     "trace_id": "<intent-trace>",
#     "span_id": "<session-uuid>",
#     "parent_id": null,
#     "timestamp": "<iso8601-utc>",
#     "source": {
#       "system": "<product-name>",
#       "instance": "<session-uuid>"
#     },
#     "data": {
#       "files_touched": [...],
#       "commit_sha": "<sha-or-null>",
#       "signals_captured": [...],
#       "decisions_recorded": [...]
#     }
#   }
#
# Closure-DoD:
#   upstream_control_path: this hook (the emitter) + bin/intent-init (the installer)
#   catch_mechanism: events.jsonl tail per-session; library-index nightly read
#   pipeline_survival: YES — events.jsonl is append-only, git-tracked

set -uo pipefail

# --- Configuration -----------------------------------------------------------

# Allow override of the product root for testing.
PRODUCT_ROOT="${INTENT_SESSION_END_ROOT:-${CLAUDE_PROJECT_DIR:-$PWD}}"

# Allow override of the session UUID. Claude Code may set $CLAUDE_SESSION_ID;
# otherwise we generate one.
SESSION_UUID="${CLAUDE_SESSION_ID:-$(uuidgen 2>/dev/null || python3 -c 'import uuid; print(uuid.uuid4())')}"

# --- Locate .intent/ by walking up from PRODUCT_ROOT -------------------------

find_intent_root() {
  local dir="$1"
  while [[ "$dir" != "/" && "$dir" != "" ]]; do
    if [[ -d "$dir/.intent" ]]; then
      printf '%s\n' "$dir"
      return 0
    fi
    dir="$(dirname "$dir")"
  done
  return 1
}

INTENT_ROOT="$(find_intent_root "$PRODUCT_ROOT")"
if [[ -z "${INTENT_ROOT:-}" ]]; then
  # No .intent/ in scope — nothing to emit. Exit silently (this is correct
  # behavior for sessions in directories that aren't Intent-instrumented).
  exit 0
fi

EVENTS_DIR="$INTENT_ROOT/.intent/events"
EVENTS_FILE="$EVENTS_DIR/events.jsonl"
mkdir -p "$EVENTS_DIR"

# --- Derive event fields -----------------------------------------------------

# Product name: last path segment of INTENT_ROOT.
PRODUCT_NAME="$(basename "$INTENT_ROOT")"

# Timestamp: ISO 8601 UTC.
TIMESTAMP="$(date -u +"%Y-%m-%dT%H:%M:%SZ")"

# trace_id: use SESSION_UUID for now (per-session trace). A future hook can
# walk up to find a parent trace_id if Intent's trace hierarchy lands.
TRACE_ID="$SESSION_UUID"
SPAN_ID="$SESSION_UUID"

# commit_sha: HEAD of the product repo (best-effort; null if not a git repo
# or no commits yet).
COMMIT_SHA="null"
if git -C "$INTENT_ROOT" rev-parse --git-dir >/dev/null 2>&1; then
  if SHA="$(git -C "$INTENT_ROOT" rev-parse HEAD 2>/dev/null)"; then
    COMMIT_SHA="\"$SHA\""
  fi
fi

# files_touched: git status --short (best-effort). Returns an empty array if
# not a git repo or status is clean.
FILES_TOUCHED="[]"
if [[ "$COMMIT_SHA" != "null" ]]; then
  # shellcheck disable=SC2207
  TOUCHED=($(git -C "$INTENT_ROOT" status --short 2>/dev/null | awk '{print $NF}'))
  if [[ ${#TOUCHED[@]} -gt 0 ]]; then
    # JSON-array-encode the file list (quote, comma-join).
    FILES_TOUCHED="["
    local_sep=""
    for f in "${TOUCHED[@]}"; do
      FILES_TOUCHED+="${local_sep}\"${f//\"/\\\"}\""
      local_sep=","
    done
    FILES_TOUCHED+="]"
  fi
fi

# signals_captured: signal files in .intent/signals/ modified during this
# session. Best-effort proxy: signals modified in the last 60 minutes.
SIGNALS_CAPTURED="[]"
SIGNALS_DIR="$INTENT_ROOT/.intent/signals"
if [[ -d "$SIGNALS_DIR" ]]; then
  # Find files modified in the last 60 minutes (Claude Code session-typical).
  # On macOS, use `-newermt` with date math; on GNU find use `-mmin`.
  if find --version >/dev/null 2>&1; then
    # GNU find
    RECENT=$(find "$SIGNALS_DIR" -type f -name '*.md' -mmin -60 -printf '%f\n' 2>/dev/null || true)
  else
    # BSD find (macOS): use -mtime with minute resolution via -mmin if available
    RECENT=$(find "$SIGNALS_DIR" -type f -name '*.md' -mmin -60 2>/dev/null | xargs -n1 basename 2>/dev/null || true)
  fi
  if [[ -n "${RECENT:-}" ]]; then
    SIGNALS_CAPTURED="["
    sep=""
    while IFS= read -r line; do
      [[ -z "$line" ]] && continue
      SIGNALS_CAPTURED+="${sep}\"${line//\"/\\\"}\""
      sep=","
    done <<< "$RECENT"
    SIGNALS_CAPTURED+="]"
  fi
fi

# decisions_recorded: decision atoms or decision-log entries modified in
# the last 60 minutes. Best-effort.
DECISIONS_RECORDED="[]"
DECISIONS_DIR="$INTENT_ROOT/.intent/decisions"
if [[ -d "$DECISIONS_DIR" ]]; then
  if find --version >/dev/null 2>&1; then
    RECENT_DEC=$(find "$DECISIONS_DIR" -type f -name '*.md' -mmin -60 -printf '%f\n' 2>/dev/null || true)
  else
    RECENT_DEC=$(find "$DECISIONS_DIR" -type f -name '*.md' -mmin -60 2>/dev/null | xargs -n1 basename 2>/dev/null || true)
  fi
  if [[ -n "${RECENT_DEC:-}" ]]; then
    DECISIONS_RECORDED="["
    sep=""
    while IFS= read -r line; do
      [[ -z "$line" ]] && continue
      DECISIONS_RECORDED+="${sep}\"${line//\"/\\\"}\""
      sep=","
    done <<< "$RECENT_DEC"
    DECISIONS_RECORDED+="]"
  fi
fi

# --- Compose + emit event ----------------------------------------------------

EVENT=$(cat <<EOF
{"version":"0.1.0","event":"session.end","trace_id":"${TRACE_ID}","span_id":"${SPAN_ID}","parent_id":null,"timestamp":"${TIMESTAMP}","source":{"system":"${PRODUCT_NAME}","instance":"${SESSION_UUID}"},"data":{"files_touched":${FILES_TOUCHED},"commit_sha":${COMMIT_SHA},"signals_captured":${SIGNALS_CAPTURED},"decisions_recorded":${DECISIONS_RECORDED}}}
EOF
)

# --- Append with fsync + best-effort lock ------------------------------------

if command -v flock >/dev/null 2>&1; then
  (
    flock -x 200
    printf '%s\n' "$EVENT" >> "$EVENTS_FILE"
    sync "$EVENTS_FILE" 2>/dev/null || sync
  ) 200>"${EVENTS_FILE}.lock"
else
  # macOS fallback: shell-level append is atomic for single lines under PIPE_BUF (4096B);
  # session.end events are well under that. Still call sync for durability.
  printf '%s\n' "$EVENT" >> "$EVENTS_FILE"
  sync
fi

# --- Verbose mode (for debugging hook installation) --------------------------

if [[ "${INTENT_SESSION_END_VERBOSE:-0}" == "1" ]]; then
  printf 'session.end: product=%s session=%s -> %s\n' \
    "$PRODUCT_NAME" "$SESSION_UUID" "$EVENTS_FILE" >&2
fi

exit 0
