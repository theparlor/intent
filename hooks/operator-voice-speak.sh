#!/usr/bin/env bash
# operator-voice-speak.sh
#
# Stop hook -- Operator Voice slice 0. When a turn ends, pull the TL;DR line out
# of the response anchor block (memory: feedback_response_anchor_block guarantees
# it is there on every substantive turn) and speak it with built-in macOS speech.
# No LLM call, no network, no account, nothing leaves the machine.
#
# Why: long agent sessions end in walls of terminal text. Brien is away from the
# screen a lot, so finished work sits unread. One spoken sentence at end of turn
# is the cheapest possible test of whether spoken agent output gets used at all.
# The gate on this slice is the mute test, not feature completeness.
#
# Gates, in order (every decision is logged, including the silent ones, because
# the log IS the adoption measure for the mute test):
#   1. recursion guard (stop_hook_active)
#   2. mute flag file present            -> silent, logged "muted"
#   3. quiet-until timestamp in future   -> silent, logged "quiet"
#   4. no TL;DR line in the last message -> silent, logged "no-anchor"
#   5. same text already spoken for this session -> silent, logged "duplicate"
#
# State (never in git, never in a repo): ~/.claude/operator-voice/
#   muted             presence = muted        (operator-voice-ctl.sh off)
#   quiet-until       epoch seconds           (operator-voice-ctl.sh quiet 60)
#   config            voice/rate/max_chars
#   utterances.jsonl  the log
#   queue.lock        cross-session playback lock
#
# This hook NEVER blocks a response: it prints nothing, exits 0 on every path,
# and dispatches playback to a detached child so the turn does not wait on audio.
#
# Slice 0 of the operator-voice plan:
#   /Users/brien/Workspaces/Core/products/_intake/2026-08-20-operator-voice/design.md
# Created 2026-08-21.

set -u

INPUT=$(cat)

OV_HOOK_INPUT="$INPUT" \
OV_PLAYER="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)/operator-voice-play.sh" \
python3 <<'PY'
import datetime
import hashlib
import json
import os
import re
import subprocess
import sys
import time

state_dir = os.environ.get("OV_STATE_DIR") or os.path.join(
    os.path.expanduser("~"), ".claude", "operator-voice"
)
log_path = os.path.join(state_dir, "utterances.jsonl")
player = os.environ.get("OV_PLAYER", "")

try:
    os.makedirs(os.path.join(state_dir, "last"), exist_ok=True)
except Exception:
    sys.exit(0)

try:
    d = json.loads(os.environ.get("OV_HOOK_INPUT", "") or "{}")
except Exception:
    sys.exit(0)

session = d.get("session_id", "unknown")


def log(status, **extra):
    rec = {
        "ts": datetime.datetime.now(datetime.timezone.utc).strftime(
            "%Y-%m-%dT%H:%M:%SZ"
        ),
        "session": session,
        "source": "stop-hook",
        "backend": "macos-say",
        "status": status,
    }
    rec.update(extra)
    try:
        with open(log_path, "a") as f:
            f.write(json.dumps(rec, ensure_ascii=False) + "\n")
    except Exception:
        pass


# 1. recursion guard
if d.get("stop_hook_active"):
    sys.exit(0)

# 2. mute flag
if os.path.exists(os.path.join(state_dir, "muted")):
    log("muted")
    sys.exit(0)

# 3. quiet window (manual stand-in for calendar-aware suppression; a meeting
#    must never be interrupted by a status line)
quiet_path = os.path.join(state_dir, "quiet-until")
try:
    if os.path.exists(quiet_path):
        with open(quiet_path) as f:
            until = float((f.read() or "0").strip() or 0)
        if time.time() < until:
            log("quiet", quiet_until=int(until))
            sys.exit(0)
except Exception:
    pass

# Last assistant message of the turn
tpath = d.get("transcript_path") or ""
if not tpath or not os.path.exists(tpath):
    sys.exit(0)

last = None
try:
    with open(tpath, errors="replace") as f:
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
    body = "\n".join(
        b.get("text", "")
        for b in content
        if isinstance(b, dict) and b.get("type") == "text"
    )
elif isinstance(content, str):
    body = content
else:
    body = ""

# 4. find the TL;DR line of the anchor block
TLDR = re.compile(r"TL\s*;?\s*DR", re.IGNORECASE)
raw = ""
for line in body.splitlines():
    if TLDR.search(line):
        raw = line
        break

if not raw.strip():
    log("no-anchor")
    sys.exit(0)

# Take everything after the TL;DR marker and its separator.
raw = TLDR.split(raw, 1)[1] if TLDR.search(raw) else raw
raw = re.sub("^[\\s>*_`:\\-\u2014\u2013\u2192\u23f9\ufe0f]+", "", raw)


def speakable(s):
    """Markdown and glyph hygiene only. Turning arbitrary output into a spoken
    register is slice 2 (the speakable register plus the styling pass); slice 0
    speaks the sentence Brien already wrote, minus the syntax that TTS chokes
    on."""
    s = re.sub(r"!\[[^\]]*\]\([^)]*\)", "", s)          # images
    s = re.sub(r"\[([^\]]*)\]\([^)]*\)", r"\1", s)      # links keep their text
    s = re.sub(r"<https?://[^>]+>", "", s)              # angle-bracket urls
    s = re.sub(r"https?://\S+", "", s)                  # bare urls
    s = s.replace("`", "")
    s = re.sub(r"\*\*|__|~~", "", s)
    s = re.sub(r"(?<!\w)[*_](?=\S)|(?<=\S)[*_](?!\w)", "", s)
    # Long absolute paths read terribly; the basename carries the meaning.
    s = re.sub(r"(?:~|/Users)(?:/[\w.\- ]+){2,}/([\w.\-]+)", r"\1", s)
    # Drop symbols and emoji that have no spoken form.
    s = re.sub(
        "[\u2190-\u21ff\u2300-\u23ff\u2460-\u27bf\u2b00-\u2bff\ufe0f\U0001F000-\U0001FAFF]",
        " ",
        s,
    )
    s = s.replace("\u2014", ", ").replace("\u2013", "-").replace("\u2026", ".")
    s = re.sub(r"\s+", " ", s)
    return s.strip(" -:;,").strip()


text = speakable(raw)
if len(text) < 3:
    log("no-anchor")
    sys.exit(0)

# 5. per-session duplicate guard
fp = hashlib.sha1(text.encode("utf-8", "replace")).hexdigest()
fp_path = os.path.join(state_dir, "last", re.sub(r"[^\w.\-]", "_", session))
try:
    if os.path.exists(fp_path):
        with open(fp_path) as f:
            if f.read().strip() == fp:
                log("duplicate", chars=len(text))
                sys.exit(0)
    with open(fp_path, "w") as f:
        f.write(fp)
except Exception:
    pass

# Dispatch detached so the turn never waits on audio.
if not player or not os.path.exists(player):
    log("no-player", text=text)
    sys.exit(0)

try:
    env = dict(os.environ)
    env["OV_SESSION"] = session
    env["OV_SOURCE"] = "stop-hook"
    p = subprocess.Popen(
        ["/bin/bash", player],
        stdin=subprocess.PIPE,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        env=env,
        start_new_session=True,
    )
    p.stdin.write(text.encode("utf-8", "replace"))
    p.stdin.close()
except Exception as exc:
    log("error", text=text, error=str(exc))

sys.exit(0)
PY
exit 0
