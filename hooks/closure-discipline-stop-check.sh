#!/usr/bin/env bash
# closure-discipline-stop-check.sh
#
# Stop hook — Layer 4 of closure-discipline enforcement (response linter).
#
# Detects completion-claim language at end of response without any
# upstream-control mention anywhere in the response body. Forces the
# model to either install upstream control before declaring resolved,
# or honestly downgrade to symptom-repaired.
#
# Pattern caught: response ends with "✅ done", "complete.", "wave closed",
# "resolved.", "fixed." etc. AND nothing in the response body mentions an
# upstream control (pipeline integration, catch-net invariant, future
# regression prevention).
#
# Spec: Core/frameworks/intent/spec/closure-discipline-enforcement.md (Layer 4)
#
# Install: chmod +x and symlink to ~/.claude/hooks/
# Register: add Stop entry to ~/.claude/settings.json
#
# Bypass: CLOSURE_DISCIPLINE_STOP_BYPASSED=1
# Audit log: ~/.claude/audit/closure-discipline-stop-detections.log
#
# Created: 2026-04-30 — promotes the closure-DoD from memory-only
# enforcement to mechanism-level. Mirrors autonomy-grant-stop-check.sh
# defensive pattern.

set -u

AUDIT_LOG="$HOME/.claude/audit/closure-discipline-stop-detections.log"
mkdir -p "$(dirname "$AUDIT_LOG")" 2>/dev/null || true

# Bypass
if [ "${CLOSURE_DISCIPLINE_STOP_BYPASSED:-0}" = "1" ]; then
  exit 0
fi

# Read input JSON from stdin
INPUT=$(cat)

# Parse defensively (fail open).
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

# No transcript → fail open
if [ "$TRANSCRIPT_PATH" = "NONE" ] || [ ! -f "$TRANSCRIPT_PATH" ]; then
  exit 0
fi

# Extract last assistant message text
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

# No text extracted → fail open
if [ -z "$LAST_TEXT" ]; then
  exit 0
fi

# Last 1500 chars approximate "near-end" of response
LAST_TAIL=$(printf '%s' "$LAST_TEXT" | tail -c 1500)

LOWER_TAIL=$(printf '%s' "$LAST_TAIL" | tr '[:upper:]' '[:lower:]')
LOWER_FULL=$(printf '%s' "$LAST_TEXT" | tr '[:upper:]' '[:lower:]')

# COMPLETION-CLAIM pattern — language that asserts the work is done.
# Match: "complete." "complete!" "done." "resolved." "fixed." "shipped." etc.
# Plus emoji/visual completion markers and wave/session-close phrasings.
# Apostrophe-bearing variants ("we're done", "everything's working") are
# matched via the apostrophe-tolerant character class [\x27 ] using
# ANSI-C $'...' quoting to keep the bash single-quote scope intact.
# TABLE-CELL variant (Layer 4 extension — Catalog Entry 2.3):
#   Catches markdown table rows where a cell reads "Done", "Complete", or ✅
#   without a neighboring catch-net / upstream-control cell. Pattern matches
#   the cell value sandwiched between pipe delimiters, e.g.: | Done | or | ✅ |
COMPLETION_RE=$'(\\bcomplete[.!]|\\bcompleted[.!]|\\bdone[.!]|\\bresolved[.!]|\\bfixed[.!]|\\bshipped[.!]|\\bwave (closed|landed|done|complete)|\\bsession[ -]end|\\bsession (over|complete)|\\ball (done|set|resolved|clear)|\xe2\x9c\x85 ?(done|complete|resolved|fixed)|\\beverything[\x27 ]?s? (working|works|fine)|\\bfully working|\\bthat[\x27 ]?s done|\\bwe[\x27 ]?re done|\\bclosed out|\\|[ \\t]*(done|complete|\xe2\x9c\x85)[ \\t]*\\|)'

# TRAILING-OBSERVATION pattern — Layer 4 extension 2026-05-28 (wave-20 follow-up).
# Catches bare state-declarations at end of response that present as closure
# without action commitment OR pillar citation. Common drift variants observed
# during the 2026-05-27 Cast CONNECT 49-wave sweep:
#   - terminal "X confirmed." / "X gap." / "X reinforced." (state as terminal)
#   - terminal "X now N-source" / "N+ source" (reinforcement-strength as terminal)
#   - terminal "P0 critical." / "P0 archival." (priority-label as terminal)
#   - terminal "X hallucination flagged." / "misattribution flagged."
#   - terminal "bilateral confirmed" / "antagonist confirmed"
# Distinguished from COMPLETION-CLAIM: no explicit "done"/"complete"/"resolved"
# but the rhetorical function is the same — declaring closure-of-thought
# without committing to next action OR citing closure pillars.
# Matched against the tail (last 300 chars) since trailing-observation drift
# is by definition about how a response ENDS. Suppressed by UPSTREAM_RE OR
# INFLIGHT_RE matches anywhere in response body.
TRAILING_OBS_RE=$'(\\b(confirmed|gap|gaps|reinforced|hallucination flagged|misattribution flagged|bilateral confirmed|antagonist confirmed|now in registry|now out of registry|now [0-9]+\\+?[- ]source)[.!]?[[:space:]]*$|\\bP[0-9] (gap|critical|reinforced|archival|foundational|active)[.!]?[[:space:]]*$)'

# UPSTREAM-CONTROL marker — phrases that indicate the fix is in-pipeline,
# catches future regressions, or honestly downgrades to symptom-repaired.
# Inclusive list to keep false-positive rate low.
UPSTREAM_RE=$'(upstream control|upstream fix|upstream resolver|upstream-fix|wired into|in the pipeline|in render_all|in render pipeline|stage [0-9]+ of|stage in render|invariant added|catch-net|catches future|future regression|prevents (future |regression)|auto-extract|auto-flow|auto-populate|auto-fill|permanent fix|won[\x27 ]?t recur|no recurrence|regression prevention|extends the (hook|policy|spec)|added to chain_audit|added invariant|i-tagline|i-v2max|i-frameworks|i-depth|i-vocab|chain_audit invariant|hook (catches|enforces)|pre-tool|posttool|pretooluse|sessionstart hook|stop hook|symptom-repaired|symptom repaired|upstream[ -]pending|downstream[ -]only|one-shot|patched, not fixed|not (yet )?upstream|still downstream|not in (the )?pipeline|will recur|new personas will (still |need to ))'

# IN-FLIGHT marker — Layer 4 extension 2026-05-28. Phrases indicating parallel
# work continues or a next-action is committed. Suppresses trailing-observation
# hook (legitimate mid-flight tracking is not drift). Distinct from
# upstream-control: in-flight = IMMEDIATE forward motion, upstream = pipeline
# integration.
INFLIGHT_RE=$'(in flight|waiting on|dispatched|committing|executing|processing|still waiting|next:|continuing|about to|will (now |continue|next|run|dispatch|commit|write|kick)|kicking (off|it off)|spawned|fired off|launched|retrying|in[- ]progress|writing closure|drafting|preparing|moving on|on to|to do:|todo:|next step|next up)'

# Detect
COMPLETION_MATCH=0
if echo "$LOWER_TAIL" | grep -qiE "$COMPLETION_RE"; then
  COMPLETION_MATCH=1
fi

TRAILING_OBS_MATCH=0
if echo "$LOWER_TAIL" | tail -c 300 | grep -qiE "$TRAILING_OBS_RE"; then
  TRAILING_OBS_MATCH=1
fi

UPSTREAM_MATCH=0
if echo "$LOWER_FULL" | grep -qiE "$UPSTREAM_RE"; then
  UPSTREAM_MATCH=1
fi

INFLIGHT_MATCH=0
if echo "$LOWER_FULL" | grep -qiE "$INFLIGHT_RE"; then
  INFLIGHT_MATCH=1
fi

# Trigger 1: completion-claim present AND no upstream-control marker anywhere
if [ "$COMPLETION_MATCH" = "1" ] && [ "$UPSTREAM_MATCH" = "0" ]; then
  TIMESTAMP=$(date -u +%Y-%m-%dT%H:%M:%SZ)
  TAIL_SAMPLE=$(printf '%s' "$LAST_TAIL" | tail -c 300 | tr '\n' ' ' | tr "'" '_')
  echo "[$TIMESTAMP] CAUGHT-COMPLETION session=$SESSION_ID tail='$TAIL_SAMPLE'" >> "$AUDIT_LOG"

  cat <<'EOF'
{"decision": "block", "reason": "CLOSURE-DISCIPLINE DRIFT (Layer 4 detector): your response ends with completion-claim language (e.g., 'complete.', 'resolved.', 'wave closed') but no mention of an upstream control anywhere in the response body. Per the closure-DoD at Core/frameworks/intent/spec/signal-stream.md, 'resolved' requires (a) upstream_control_path — the file path of the resolver in the pipeline (not 'I ran the script'), (b) catch_mechanism — chain_audit invariant ID, test, or explicit no-catch-net justification, (c) pipeline survival — will the fix survive the next render_all run. Revise the response: either install the upstream control and state where it lives, OR honestly downgrade the closure language to 'symptom-repaired, upstream-pending' and capture the upstream gap as a follow-up signal. The pattern this hook catches is the recurring drift where one-shot patches get declared 'resolved' without an installed mechanism preventing recurrence."}
EOF
  exit 0
fi

# Trigger 2: trailing-observation drift — response ends with bare state declaration,
# no in-flight marker, no upstream marker. Reflects observation-as-conclusion
# without action commitment. Wave-20 follow-up pattern, observed throughout the
# 49-wave Cast CONNECT sweep (e.g., "X confirmed.", "Y now 3-source", "Z gap.").
if [ "$TRAILING_OBS_MATCH" = "1" ] && [ "$UPSTREAM_MATCH" = "0" ] && [ "$INFLIGHT_MATCH" = "0" ]; then
  TIMESTAMP=$(date -u +%Y-%m-%dT%H:%M:%SZ)
  TAIL_SAMPLE=$(printf '%s' "$LAST_TAIL" | tail -c 300 | tr '\n' ' ' | tr "'" '_')
  echo "[$TIMESTAMP] CAUGHT-TRAILING-OBS session=$SESSION_ID tail='$TAIL_SAMPLE'" >> "$AUDIT_LOG"

  cat <<'EOF'
{"decision": "block", "reason": "CLOSURE-DISCIPLINE DRIFT (Layer 4 detector — trailing-observation pattern): your response ends with a bare state-declaration (e.g., 'X confirmed.', 'Y now N-source', 'Z gap', 'P0 critical') without committing to a next action OR citing closure pillars. Trailing-observation drift presents as conclusion-via-observation rather than action-commitment. Revise the response: either (a) commit to a next action explicitly ('dispatching X', 'committing Y', 'waiting on Z'), OR (b) cite the closure pillars (upstream control, catch-net, pipeline survival) if work is genuinely complete, OR (c) honestly state that you are paused and signal-log the reason. Pattern identified during 2026-05-27 Cast CONNECT sweep wave-20 retrospective; this hook is the mechanism-level fix per spec at Core/frameworks/intent/spec/closure-discipline-enforcement.md Layer 4."}
EOF
  exit 0
fi

exit 0
