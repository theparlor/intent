#!/usr/bin/env bash
# operator-voice-ctl.sh
#
# Operator Voice slice 0, control surface. The mute flag has to be one command
# away or the mute test measures friction instead of adoption.
#
#   operator-voice-ctl.sh off            mute (silent until you turn it back on)
#   operator-voice-ctl.sh on             unmute
#   operator-voice-ctl.sh quiet 60       stay silent for the next 60 minutes
#   operator-voice-ctl.sh resume         cancel the quiet window
#   operator-voice-ctl.sh status         current state plus a 7-day tally
#   operator-voice-ctl.sh log [N]        last N log records (default 15)
#   operator-voice-ctl.sh test [text]    speak a line through the real queue
#
# State: ~/.claude/operator-voice/   (override with OV_STATE_DIR)
# Slice 0 of the operator-voice plan:
#   /Users/brien/Workspaces/Core/products/_intake/2026-08-20-operator-voice/design.md
# Created 2026-08-21.

set -u

STATE_DIR="${OV_STATE_DIR:-$HOME/.claude/operator-voice}"
HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PLAYER="${HERE}/operator-voice-play.sh"
mkdir -p "${STATE_DIR}" 2>/dev/null || true

CMD="${1:-status}"

case "${CMD}" in
  off|mute)
    : > "${STATE_DIR}/muted"
    echo "Operator Voice: MUTED. Turn it back on with: operator-voice-ctl.sh on"
    ;;
  on|unmute)
    rm -f "${STATE_DIR}/muted" "${STATE_DIR}/quiet-until"
    echo "Operator Voice: ON. Anchor-block TL;DR lines will be spoken at end of turn."
    ;;
  quiet)
    MINS="${2:-60}"
    OV_STATE_DIR="${STATE_DIR}" MINS="${MINS}" python3 - <<'PY'
import os, time
mins = float(os.environ.get("MINS", "60") or 60)
p = os.path.join(os.environ["OV_STATE_DIR"], "quiet-until")
until = time.time() + mins * 60
open(p, "w").write(str(until))
print("Operator Voice: quiet until %s (%g min)."
      % (time.strftime("%H:%M", time.localtime(until)), mins))
PY
    ;;
  resume)
    rm -f "${STATE_DIR}/quiet-until"
    echo "Operator Voice: quiet window cancelled."
    ;;
  status)
    OV_STATE_DIR="${STATE_DIR}" python3 - <<'PY'
import json, os, time
sd = os.environ["OV_STATE_DIR"]
muted = os.path.exists(os.path.join(sd, "muted"))
qp = os.path.join(sd, "quiet-until")
quiet = ""
if os.path.exists(qp):
    try:
        u = float(open(qp).read().strip() or 0)
        if u > time.time():
            quiet = " quiet until %s" % time.strftime("%H:%M", time.localtime(u))
    except Exception:
        pass
print("Operator Voice: %s%s" % ("MUTED" if muted else "ON", quiet))

cfg = os.path.join(sd, "config")
print("  config: %s" % (cfg if os.path.exists(cfg) else "none (system default voice and rate)"))

log = os.path.join(sd, "utterances.jsonl")
if not os.path.exists(log):
    print("  log:    no records yet")
    raise SystemExit
cut = time.time() - 7 * 86400
tally, total = {}, 0
for line in open(log, errors="replace"):
    try:
        r = json.loads(line)
        t = time.mktime(time.strptime(r["ts"], "%Y-%m-%dT%H:%M:%SZ")) - time.timezone
    except Exception:
        continue
    if t < cut:
        continue
    tally[r.get("status", "?")] = tally.get(r.get("status", "?"), 0) + 1
    total += 1
print("  log:    %s" % log)
print("  last 7 days: %d records %s"
      % (total, ", ".join("%s=%d" % kv for kv in sorted(tally.items())) or "(none)"))
print("  mute test: spoken count trending to zero, or muted/quiet climbing, means park it.")
PY
    ;;
  log)
    N="${2:-15}"
    OV_STATE_DIR="${STATE_DIR}" N="${N}" python3 - <<'PY'
import json, os
sd = os.environ["OV_STATE_DIR"]
n = int(os.environ.get("N", "15") or 15)
p = os.path.join(sd, "utterances.jsonl")
if not os.path.exists(p):
    print("no records yet")
    raise SystemExit
rows = open(p, errors="replace").read().strip().splitlines()[-n:]
for line in rows:
    try:
        r = json.loads(line)
    except Exception:
        continue
    print("%s  %-12s %s" % (r.get("ts", "?"), r.get("status", "?"),
                            (r.get("text", "") or "")[:100]))
PY
    ;;
  test)
    shift || true
    TEXT="${*:-Operator Voice is working. This is the built in macOS speech backend.}"
    printf '%s' "${TEXT}" | OV_SESSION=ctl-test OV_SOURCE=ctl-test /bin/bash "${PLAYER}"
    echo "Spoke: ${TEXT}"
    ;;
  *)
    echo "usage: operator-voice-ctl.sh {on|off|quiet MINUTES|resume|status|log [N]|test [text]}"
    exit 2
    ;;
esac
exit 0
