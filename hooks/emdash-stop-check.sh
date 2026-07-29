#!/usr/bin/env bash
# emdash-stop-check.sh
#
# Stop hook -- enforces Brien's no-dash-glyph rule (memory: feedback_no_emdashes).
#
# Brien's peers read em-dashes as an AI tell, which blocks his ability to confidently
# share Claude-produced material. The preference recurred 5+ times in a single session
# (2026-06-19) despite memory and explicit correction, so this is the mechanism-level fix:
# Claude cannot SEND a response containing the glyphs. No reprieve, regardless of whether
# the glyph was historically used correctly.
#
# Blocked glyphs anywhere in the assistant's response text:
#   em-dash (U+2014), en-dash (U+2013), horizontal bar (U+2015),
#   rightwards/left/both arrows (U+2192 U+2190 U+2194), heavy/double arrows (U+21D2 etc.),
#   ellipsis (U+2026)
# Use periods, commas, colons, parentheses, the words "to"/"vs", or a plain hyphen instead.
# NO code-block exemption -- airtight by default; use the bypass for a verbatim source quote.
#
# Bypass: EMDASH_BYPASSED=1   (use ONLY when quoting a source verbatim that must keep the glyph)
# Audit:  ~/.claude/audit/emdash-detections.log
#
# Created 2026-06-19. Mirrors link-format-stop-check.sh. Fails OPEN on any error so a script
# bug can never permanently block responses.

set -u

AUDIT_LOG="$HOME/.claude/audit/emdash-detections.log"
mkdir -p "$(dirname "$AUDIT_LOG")" 2>/dev/null || true

[ "${EMDASH_BYPASSED:-0}" = "1" ] && exit 0

INPUT=$(cat)

EMDASH_HOOK_INPUT="$INPUT" python3 - "$AUDIT_LOG" <<'PY'
import json, sys, os, datetime

audit_log = sys.argv[1]
try:
    d = json.loads(os.environ.get("EMDASH_HOOK_INPUT", "") or "{}")
except Exception:
    sys.exit(0)

# Recursion guard
if d.get("stop_hook_active"):
    sys.exit(0)

tpath = d.get("transcript_path") or ""
sid = d.get("session_id", "unknown")
if not tpath or not os.path.exists(tpath):
    sys.exit(0)

# Extract the last assistant message text (fail open on any error)
last = None
try:
    with open(tpath) as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                o = json.loads(line)
            except Exception:
                continue
            if o.get("type") == "assistant":
                last = o
except Exception:
    sys.exit(0)
if not last:
    sys.exit(0)

content = last.get("message", {}).get("content", [])
if isinstance(content, list):
    text = "\n".join(b.get("text", "") for b in content
                     if isinstance(b, dict) and b.get("type") == "text")
elif isinstance(content, str):
    text = content
else:
    text = ""
if not text.strip():
    sys.exit(0)

# Glyph -> human label. Scan the FULL response (no code-fence exemption).
GLYPHS = {
    "—": "em-dash",
    "–": "en-dash",
    "―": "horizontal-bar",
    "→": "right-arrow",
    "←": "left-arrow",
    "↔": "both-arrow",
    "⇒": "double-arrow",
    "…": "ellipsis",
}
found = []
for g, name in GLYPHS.items():
    if g in text:
        found.append(name)

if not found:
    sys.exit(0)

ts = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
try:
    with open(audit_log, "a") as a:
        a.write("[%s] CAUGHT session=%s glyphs=%s\n" % (ts, sid, ",".join(found)))
except Exception:
    pass

reason = (
    "DASH-GLYPH DRIFT (feedback_no_emdashes): your response contains glyphs Brien's peers read "
    "as an AI tell, which blocks his ability to share this material -- detected: "
    + ", ".join(found) + ". These are banned with no reprieve, in conversation and in every "
    "drafted/shareable artifact (Slack, email, Jira, Confluence, deliverables). Rewrite using "
    "periods, commas, colons, parentheses, the words 'to'/'vs', or a plain hyphen (-) instead. "
    "If you ran a mechanical strip on a file, also fix the resulting comma-splices by hand. "
    "Bypass with EMDASH_BYPASSED=1 ONLY when quoting a source verbatim that must keep the glyph."
)
print(json.dumps({"decision": "block", "reason": reason}))
sys.exit(0)
PY
exit 0
