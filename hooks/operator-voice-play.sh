#!/usr/bin/env bash
# operator-voice-play.sh
#
# Operator Voice slice 0, playback half. Reads one utterance on stdin, takes the
# global playback lock so parallel Claude Code sessions never talk over each
# other, speaks it with built-in macOS speech (/usr/bin/say), and appends one
# record to the utterance log.
#
# Usable standalone for testing:
#   echo "the queue is empty" | operator-voice-play.sh
#
# Env (all optional):
#   OV_SESSION   session id recorded in the log (default "manual")
#   OV_SOURCE    what produced the text (default "manual")
#   OV_STATE_DIR state directory (default ~/.claude/operator-voice)
#
# Config file (optional), ~/.claude/operator-voice/config, KEY=VALUE per line:
#   voice=Samantha     say -v value; unset means the system default voice
#   rate=190           say -r value; unset means the system default rate
#   max_chars=400      hard cap on spoken characters
#
# Nothing here can block a Claude Code turn: it is invoked detached by the Stop
# hook, and it fails open (exit 0) on every error path.
#
# Slice 0 of the operator-voice plan:
#   /Users/brien/Workspaces/Core/products/_intake/2026-08-20-operator-voice/design.md
# Created 2026-08-21.

set -u

OV_TEXT="$(cat)"
export OV_TEXT

python3 <<'PY'
import datetime
import fcntl
import json
import os
import subprocess
import sys
import time

state_dir = os.environ.get("OV_STATE_DIR") or os.path.join(
    os.path.expanduser("~"), ".claude", "operator-voice"
)
try:
    os.makedirs(state_dir, exist_ok=True)
except Exception:
    sys.exit(0)

log_path = os.path.join(state_dir, "utterances.jsonl")
lock_path = os.path.join(state_dir, "queue.lock")
config_path = os.path.join(state_dir, "config")

session = os.environ.get("OV_SESSION", "manual")
source = os.environ.get("OV_SOURCE", "manual")
text = (os.environ.get("OV_TEXT") or "").strip()


def log(status, **extra):
    rec = {
        "ts": datetime.datetime.now(datetime.timezone.utc).strftime(
            "%Y-%m-%dT%H:%M:%SZ"
        ),
        "session": session,
        "source": source,
        "backend": "macos-say",
        "status": status,
    }
    rec.update(extra)
    try:
        with open(log_path, "a") as f:
            f.write(json.dumps(rec, ensure_ascii=False) + "\n")
    except Exception:
        pass


cfg = {}
try:
    if os.path.exists(config_path):
        with open(config_path) as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith("#") or "=" not in line:
                    continue
                k, v = line.split("=", 1)
                cfg[k.strip().lower()] = v.strip()
except Exception:
    cfg = {}

try:
    max_chars = int(cfg.get("max_chars", "400"))
except Exception:
    max_chars = 400

if not text:
    log("empty", chars=0)
    sys.exit(0)

if len(text) > max_chars:
    cut = text[:max_chars]
    stop = max(cut.rfind(". "), cut.rfind("! "), cut.rfind("? "))
    text = (cut[: stop + 1] if stop > int(max_chars * 0.4) else cut).strip()

if not os.path.exists("/usr/bin/say"):
    log("no-backend", chars=len(text), text=text)
    sys.exit(0)

cmd = ["/usr/bin/say"]
voice = cfg.get("voice", "")
rate = cfg.get("rate", "")
if voice:
    cmd += ["-v", voice]
if rate:
    cmd += ["-r", rate]
cmd += ["--", text]

lock_fh = None
try:
    lock_fh = open(lock_path, "a+")
except Exception:
    lock_fh = None

waited = 0.0
if lock_fh is not None:
    # Serialize playback across sessions. Give up after 180s rather than
    # queueing a status line that is no longer worth hearing.
    deadline = time.time() + 180
    got = False
    while time.time() < deadline:
        try:
            fcntl.flock(lock_fh.fileno(), fcntl.LOCK_EX | fcntl.LOCK_NB)
            got = True
            break
        except BlockingIOError:
            time.sleep(0.5)
            waited += 0.5
        except Exception:
            break
    if not got:
        log("queue-timeout", chars=len(text), text=text, waited_s=round(waited, 1))
        sys.exit(0)

started = time.time()
try:
    rc = subprocess.call(cmd)
except Exception as exc:
    log("error", chars=len(text), text=text, error=str(exc))
    sys.exit(0)
finally:
    if lock_fh is not None:
        try:
            fcntl.flock(lock_fh.fileno(), fcntl.LOCK_UN)
            lock_fh.close()
        except Exception:
            pass

duration = round(time.time() - started, 2)
log(
    "spoken" if rc == 0 else "error",
    chars=len(text),
    text=text,
    voice=voice or "system-default",
    rate=rate or "system-default",
    duration_s=duration,
    waited_s=round(waited, 1),
    exit_code=rc,
)
sys.exit(0)
PY
exit 0
