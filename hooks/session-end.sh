#!/usr/bin/env bash
# hooks/session-end.sh (Tier 1 session.end event emitter)
#
# Emits an OTel-shaped `session.end` event to
# <product>/.intent/events/events.<machine-id>.jsonl at the close of an agent
# session. One shard per machine (P4, single-writer change plan section 1): two
# machines never append to the same tracked file, so their rows never conflict
# on a pull, and the lander unions every shard. The legacy events.jsonl is no
# longer written; it stays as history and readers glob events*.jsonl.
#
# Installed per-product by `bin/intent-init`:
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
#     "version": "0.2.0",
#     "event": "session.end",
#     "trace_id": "<intent-trace>",
#     "span_id": "<session-uuid>",
#     "parent_id": null,
#     "timestamp": "<iso8601-utc>",
#     "source": {
#       "system": "<product-name>",
#       "instance": "<session-uuid>",
#       "machine": {"serial": "<machine-id>", "role": "<hub|travel|embassy|unknown>",
#                   "name": "<operator name or empty>"}
#     },
#     "data": {
#       "files_touched": [...],
#       "commit_sha": "<sha-or-null>",
#       "signals_captured": [...],
#       "signals_seen": [...],
#       "decisions_recorded": [...],
#       "decisions_seen": [...]
#     }
#   }
#
# signals_captured vs signals_seen (2026-09-14, loom PR 9 rung-2 fix):
#   signals_seen is the old best-effort proxy: every .intent/signals/*.md
#   file whose mtime falls inside the session window, regardless of who
#   touched it. On a day with several sessions open at once that proxy
#   claims one session's stop for everyone else's work too, so it is kept
#   verbatim but demoted: nothing downstream should trust it as attribution.
#   signals_captured is narrowed to files this session has EVIDENCE for,
#   strongest first:
#     1. frontmatter naming this session (session:, session_id:,
#        originSessionId: the value is tokenized, so
#        "session: <id> (worktree name)" still matches)
#     2. a Write or Edit tool_use in this session's own transcript
#        (transcript_path from the hook payload) naming the file
#     3. a commit on the cwd's current branch touching the file inside
#        the session window
#   Every rung is best-effort and independently fail-open: an unreadable
#   transcript, a detached HEAD, or a git error just drops that rung,
#   never the event. Loom's harvest reads signals_captured as its second
#   attribution rung; signals_seen is not read by that path.
#
# decisions_recorded vs decisions_seen (2026-09-14, same evidence ladder):
#   decisions_recorded used to be the mtime sweep verbatim: every
#   .intent/decisions/*.md file changed in the last 60 minutes, whoever
#   wrote it, which has the identical over-claiming failure mode
#   signals_captured had before the loom PR 9 fix above. It now runs
#   through the SAME three-rung evidence ladder (shared helper, see
#   evidence_ladder_captured() below) against .intent/decisions/ instead
#   of .intent/signals/. The old mtime sweep is kept verbatim under the
#   new decisions_seen field, so nothing is lost. Confirmed 2026-09-14:
#   Loom's harvest (src/harvest.py, harvest_events()) reads
#   decisions_recorded directly, producing a session-attributed "decision"
#   record per entry, the same way it reads signals_captured for "signal"
#   records. This narrowing therefore has the same direct benefit for
#   Loom's decision attribution that the loom PR 9 fix had for signals.
#
# machine id (0.2.0): the lowercased hardware serial (IOPlatformSerialNumber),
#   falling back to a lowercased slug of the ComputerName, then of the hostname.
#   INTENT_SESSION_END_MACHINE overrides it (tests). The role and name come from
#   the machine-role helper in the claude config (guarded source; absent helper
#   or absent ~/.claude/machine.json means role "unknown"). Capture is never
#   gated on role: every machine writes, only the file name differs.
#
# Append: one os.write of row plus newline on an O_APPEND descriptor under an
#   exclusive fcntl.flock, then fsync. The lock serialises concurrent sessions on
#   one machine; nothing relies on PIPE_BUF atomicity.
#
# Closure-DoD:
#   upstream_control_path: this hook (the emitter) + bin/intent-init (the installer)
#   catch_mechanism: loom harvest reads every events*.jsonl shard
#   pipeline_survival: YES. Each shard is append-only and git-tracked; the
#     quartermaster lander unions .intent/events/events.*.jsonl

set -uo pipefail

# --- Configuration -----------------------------------------------------------

# Allow override of the product root for testing.
PRODUCT_ROOT="${INTENT_SESSION_END_ROOT:-${CLAUDE_PROJECT_DIR:-$PWD}}"

# Session UUID precedence (2026-09-11, foreign-key alignment with Witness):
#   1. $CLAUDE_SESSION_ID if the harness exports it
#   2. the "session_id" field of the hook's stdin JSON (what Claude Code actually sends;
#      this is the SAME uuid that names ~/.claude/projects/<cwd>/<session>.jsonl and
#      .entire/metadata/<session>/, so intents join cc-native and entire-io events by id)
#   3. a generated uuid, only when neither is present (uppercase uuidgen output is the
#      tell that a row fell through to this branch)
# stdin is read once here, before anything else could consume it; empty or non-JSON
# input is tolerated.
HOOK_STDIN=""
if [ ! -t 0 ]; then
  HOOK_STDIN="$(cat 2>/dev/null || true)"
fi
STDIN_PARSED="$(printf '%s' "$HOOK_STDIN" | python3 -c 'import sys,json
try:
    d=json.loads(sys.stdin.read() or "{}")
    sid=d.get("session_id") or ""
    tp=d.get("transcript_path") or ""
    print(sid if isinstance(sid,str) else "")
    print(tp if isinstance(tp,str) else "")
except Exception:
    print("")
    print("")' 2>/dev/null || true)"
STDIN_SESSION_ID="$(printf '%s\n' "$STDIN_PARSED" | sed -n '1p')"
STDIN_TRANSCRIPT_PATH="$(printf '%s\n' "$STDIN_PARSED" | sed -n '2p')"
SESSION_UUID="${CLAUDE_SESSION_ID:-${STDIN_SESSION_ID:-$(uuidgen 2>/dev/null || python3 -c 'import uuid; print(uuid.uuid4())')}}"

# transcript_path: what the SessionEnd hook payload names as the session's
# own JSONL transcript. Used only as evidence for signals_captured /
# decisions_recorded below (rung 2 of the ladder), never required, since
# a missing or unreadable transcript must not block the event (fail-open).
TRANSCRIPT_PATH="${INTENT_SESSION_END_TRANSCRIPT_PATH:-$STDIN_TRANSCRIPT_PATH}"

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
  # No .intent/ in scope, so there is nothing to emit. Exit silently (this is correct
  # behavior for sessions in directories that aren't Intent-instrumented).
  exit 0
fi

# --- Machine identity (names the shard; never gates the write) ---------------

slugify() {
  printf '%s' "$1" | tr '[:upper:]' '[:lower:]' | tr -c 'a-z0-9' '-' | sed -e 's/--*/-/g' -e 's/^-//' -e 's/-$//'
}

MACHINE_ID="${INTENT_SESSION_END_MACHINE:-}"
if [[ -z "$MACHINE_ID" ]] && command -v ioreg >/dev/null 2>&1; then
  MACHINE_ID="$(ioreg -rd1 -c IOPlatformExpertDevice 2>/dev/null \
    | awk -F'"' '/IOPlatformSerialNumber/ {print $4; exit}')"
fi
if [[ -z "$MACHINE_ID" ]] && command -v scutil >/dev/null 2>&1; then
  MACHINE_ID="$(scutil --get ComputerName 2>/dev/null || true)"
fi
if [[ -z "$MACHINE_ID" ]]; then
  MACHINE_ID="$(hostname -s 2>/dev/null || hostname 2>/dev/null || true)"
fi
MACHINE_ID="$(slugify "$MACHINE_ID")"
# Last resort only when every source above is empty; the row is still written.
[[ -n "$MACHINE_ID" ]] || MACHINE_ID="unidentified"

_role_helper="${CLAUDE_CONFIG_DIR:-$HOME/.claude}/hooks/helpers/machine-role.sh"
if [[ -r "$_role_helper" ]]; then
  # shellcheck source=/dev/null
  . "$_role_helper" || MACHINE_ROLE=unknown
else
  MACHINE_ROLE=unknown
fi
MACHINE_ROLE="${MACHINE_ROLE:-unknown}"
MACHINE_NAME="${MACHINE_NAME:-}"
# JSON-escape the free-text name (backslash first, then double quote).
MACHINE_NAME_JSON="${MACHINE_NAME//\\/\\\\}"
MACHINE_NAME_JSON="${MACHINE_NAME_JSON//\"/\\\"}"

EVENTS_DIR="$INTENT_ROOT/.intent/events"
EVENTS_FILE="$EVENTS_DIR/events.${MACHINE_ID}.jsonl"
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

# JSON-array-encode a newline-delimited list of bare filenames (shared by
# signals_seen, signals_captured, decisions_seen, and decisions_recorded
# below).
json_array_from_lines() {
  local lines="$1" arr="[" sep="" line
  while IFS= read -r line; do
    [[ -z "$line" ]] && continue
    arr+="${sep}\"${line//\"/\\\"}\""
    sep=","
  done <<< "$lines"
  arr+="]"
  printf '%s' "$arr"
}

# The session-window minutes used by both mtime sweeps below (signals_seen,
# decisions_seen) and the git-log rung of the evidence ladder. Overridable
# for tests.
WINDOW_MIN="${INTENT_SESSION_END_WINDOW_MIN:-60}"

# mtime_sweep: the OLD best-effort proxy, shared by signals_seen and
# decisions_seen: every *.md file directly under $1 whose mtime falls
# inside WINDOW_MIN minutes, regardless of who touched it. A coincidence-
# of-the-clock list, not attribution; see the schema note above. Prints
# bare filenames, one per line; prints nothing if $1 doesn't exist.
mtime_sweep() {
  local dir="$1"
  [[ -d "$dir" ]] || return 0
  # On macOS, use `-newermt` with date math; on GNU find use `-mmin`.
  if find --version >/dev/null 2>&1; then
    # GNU find
    find "$dir" -type f -name '*.md' -mmin "-${WINDOW_MIN}" -printf '%f\n' 2>/dev/null || true
  else
    # BSD find (macOS): use -mtime with minute resolution via -mmin if available
    find "$dir" -type f -name '*.md' -mmin "-${WINDOW_MIN}" 2>/dev/null | xargs -n1 basename 2>/dev/null || true
  fi
}

# evidence_ladder_captured: the shared three-rung evidence ladder behind
# both signals_captured and decisions_recorded. Narrows "every *.md file
# under $1 touched in the window" (mtime_sweep's job) down to files THIS
# session has evidence for, strongest first:
#   1. frontmatter naming this session (session:, session_id:,
#      originSessionId: tokenized, so "session: <id> (worktree name)"
#      still matches)
#   2. a Write or Edit tool_use in this session's own transcript
#      (TRANSCRIPT_PATH) naming a file directly under $1
#   3. a commit on the cwd's current branch touching a file under $1,
#      inside the WINDOW_MIN window
# Every rung is independently fail-open (missing transcript, detached
# HEAD, or a git error just drops that rung, never the event). Prints
# bare filenames, one per line; prints nothing if $1 doesn't exist.
evidence_ladder_captured() {
  local target_dir="$1"
  [[ -d "$target_dir" ]] || return 0
  EV_SESSION_UUID="$SESSION_UUID" \
    EV_TARGET_DIR="$target_dir" \
    EV_TRANSCRIPT_PATH="$TRANSCRIPT_PATH" \
    EV_INTENT_ROOT="$INTENT_ROOT" \
    EV_BRANCH="$BRANCH_NAME" \
    EV_WINDOW_MIN="$WINDOW_MIN" \
    python3 - <<'PYEOF' 2>/dev/null || true
import os
import re
import subprocess

session_uuid = os.environ.get("EV_SESSION_UUID", "")
target_dir = os.environ.get("EV_TARGET_DIR", "")
transcript_path = os.environ.get("EV_TRANSCRIPT_PATH", "")
intent_root = os.environ.get("EV_INTENT_ROOT", "")
branch = os.environ.get("EV_BRANCH", "")
window_min = os.environ.get("EV_WINDOW_MIN", "60")

captured = set()

# --- Rung 1: frontmatter names this session -----------------------------
FRONTMATTER_KEYS = ("session:", "session_id:", "originsessionid:", "origin_session_id:")
if target_dir and session_uuid and os.path.isdir(target_dir):
    try:
        names = [n for n in os.listdir(target_dir) if n.endswith(".md")]
    except Exception:
        names = []
    for name in names:
        fm_path = os.path.join(target_dir, name)
        try:
            fm_lines = []
            with open(fm_path, "r", errors="ignore") as f:
                for i, line in enumerate(f):
                    if i == 0:
                        if line.strip() != "---":
                            break
                        continue
                    if line.strip() == "---":
                        break
                    fm_lines.append(line)
                    if i > 60:
                        break
        except Exception:
            continue
        for line in fm_lines:
            lline = line.strip().lower()
            for key in FRONTMATTER_KEYS:
                if lline.startswith(key):
                    value = line.split(":", 1)[1] if ":" in line else ""
                    tokens = [t.lower() for t in re.split(r'[\s,()"\']+', value) if t]
                    if session_uuid.lower() in tokens:
                        captured.add(name)
                    break

# --- Rung 2: this session's own transcript wrote/edited the file --------
if transcript_path and target_dir and os.path.isfile(transcript_path):
    target_dir_abs = os.path.abspath(target_dir)
    try:
        with open(transcript_path, "r", errors="ignore") as f:
            for raw in f:
                raw = raw.strip()
                if not raw:
                    continue
                try:
                    import json as _json
                    obj = _json.loads(raw)
                except Exception:
                    continue
                if obj.get("type") != "assistant":
                    continue
                content = obj.get("message", {}).get("content", [])
                if not isinstance(content, list):
                    continue
                for block in content:
                    if not isinstance(block, dict) or block.get("type") != "tool_use":
                        continue
                    if block.get("name") not in ("Write", "Edit"):
                        continue
                    inp = block.get("input") or {}
                    fp = inp.get("file_path") or inp.get("path") or ""
                    if not fp:
                        continue
                    fp_abs = os.path.abspath(fp)
                    if fp_abs == target_dir_abs or os.path.dirname(fp_abs) == target_dir_abs:
                        captured.add(os.path.basename(fp_abs))
    except Exception:
        pass

# --- Rung 3: a commit on the cwd's current branch, inside the window ----
if branch and intent_root and target_dir and os.path.isdir(target_dir):
    try:
        rel_target = os.path.relpath(target_dir, intent_root)
        out = subprocess.run(
            ["git", "-C", intent_root, "log", f"--since={window_min} minutes ago",
             "--name-only", "--pretty=format:", "--", rel_target],
            capture_output=True, text=True, timeout=10,
        )
        if out.returncode == 0:
            for line in out.stdout.splitlines():
                line = line.strip()
                if line and line.startswith(rel_target):
                    captured.add(os.path.basename(line))
    except Exception:
        pass

for name in sorted(captured):
    print(name)
PYEOF
}

# BRANCH_NAME: the cwd's current branch, used by rung 3 of the evidence
# ladder for both signals and decisions. Empty (and rung 3 a no-op) on a
# detached HEAD or outside a git repo.
BRANCH_NAME=""
if [[ "$COMMIT_SHA" != "null" ]]; then
  BRANCH_NAME="$(git -C "$INTENT_ROOT" branch --show-current 2>/dev/null || true)"
fi

# signals_seen / signals_captured: see the schema note above.
SIGNALS_DIR="$INTENT_ROOT/.intent/signals"
SIGNALS_SEEN="$(json_array_from_lines "$(mtime_sweep "$SIGNALS_DIR")")"
SIGNALS_CAPTURED="$(json_array_from_lines "$(evidence_ladder_captured "$SIGNALS_DIR")")"

# decisions_seen / decisions_recorded: same shape, same shared helpers,
# aimed at .intent/decisions/ instead of .intent/signals/. See the schema
# note above.
DECISIONS_DIR="$INTENT_ROOT/.intent/decisions"
DECISIONS_SEEN="$(json_array_from_lines "$(mtime_sweep "$DECISIONS_DIR")")"
DECISIONS_RECORDED="$(json_array_from_lines "$(evidence_ladder_captured "$DECISIONS_DIR")")"

# --- Compose + emit event ----------------------------------------------------

EVENT=$(cat <<EOF
{"version":"0.2.0","event":"session.end","trace_id":"${TRACE_ID}","span_id":"${SPAN_ID}","parent_id":null,"timestamp":"${TIMESTAMP}","source":{"system":"${PRODUCT_NAME}","instance":"${SESSION_UUID}","machine":{"serial":"${MACHINE_ID}","role":"${MACHINE_ROLE}","name":"${MACHINE_NAME_JSON}"}},"data":{"files_touched":${FILES_TOUCHED},"commit_sha":${COMMIT_SHA},"signals_captured":${SIGNALS_CAPTURED},"signals_seen":${SIGNALS_SEEN},"decisions_recorded":${DECISIONS_RECORDED},"decisions_seen":${DECISIONS_SEEN}}}
EOF
)

# --- Append: exclusive lock, one write, fsync ---------------------------------

if ! INTENT_EVENT_ROW="$EVENT" python3 - "$EVENTS_FILE" <<'PYEOF'
import fcntl
import os
import sys

row = (os.environ["INTENT_EVENT_ROW"] + "\n").encode("utf-8")
fd = os.open(sys.argv[1], os.O_WRONLY | os.O_CREAT | os.O_APPEND, 0o644)
try:
    fcntl.flock(fd, fcntl.LOCK_EX)
    try:
        view = memoryview(row)
        while view:
            n = os.write(fd, view)
            view = view[n:]
        os.fsync(fd)
    finally:
        fcntl.flock(fd, fcntl.LOCK_UN)
finally:
    os.close(fd)
PYEOF
then
  # python3 unavailable or the write failed: capture is never dropped, so fall
  # back to a plain shell append.
  printf '%s\n' "$EVENT" >> "$EVENTS_FILE"
fi

# --- Verbose mode (for debugging hook installation) --------------------------

if [[ "${INTENT_SESSION_END_VERBOSE:-0}" == "1" ]]; then
  printf 'session.end: product=%s session=%s -> %s\n' \
    "$PRODUCT_NAME" "$SESSION_UUID" "$EVENTS_FILE" >&2
fi

exit 0
