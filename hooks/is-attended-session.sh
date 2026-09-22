#!/usr/bin/env bash
# is-attended-session.sh
#
# Shared predicate for the intent hooks fabric: is a human plausibly present
# for this session? Any hook with a user-perceptible side effect (sound,
# notification, window, dialog) MUST gate on this before acting.
#
#   exit 0  attended    a human could be at the keyboard
#   exit 1  unattended  nobody is there; take no perceptible action
#
# Prints a one-line reason to stdout either way, suitable for logging.
#
# WHY THIS EXISTS
# Operator Voice slice 0 registered a Stop hook that spoke aloud at end of
# every turn. The Stop hook fires in unattended launchd sessions too, so the
# overnight scheduled routines spoke through the night of 2026-08-21 into
# 2026-08-22, eight times between 01:02 and 07:07, and woke the household.
# Its only protections were a mute flag and a manual quiet window, both of
# which require the operator to anticipate the harm and be awake to act.
#   Signal: ~/Workspaces/.intent/signals/SIG-OPERATOR-VOICE-UNATTENDED-SESSIONS-2026-08-22.md
#
# FAILS CLOSED. This is the whole point. If attendance cannot be positively
# established, the answer is "unattended". Slice 0 failed open (speak unless
# told not to); the inversion is the fix. A missed status line costs nothing.
# A false positive at 05:00 costs a night of sleep.
#
# Overrides (env):
#   INTENT_SESSION_UNATTENDED=1   force unattended. Set this in launchd plists.
#   INTENT_SESSION_ATTENDED=1     force attended. Testing only.
#
# Usage:
#   if is-attended-session.sh >/dev/null; then ...speak...; fi
#   reason=$(is-attended-session.sh) || log_silent "$reason"
#
# Created 2026-08-24 as slice 0a of the operator-voice plan.

set -u

# Explicit markers win, unattended first so a plist can never be overridden
# by a stale exported ATTENDED in the same environment.
if [[ "${INTENT_SESSION_UNATTENDED:-}" == "1" ]]; then
  echo "unattended: INTENT_SESSION_UNATTENDED=1 set explicitly"
  exit 1
fi
if [[ "${INTENT_SESSION_ATTENDED:-}" == "1" ]]; then
  echo "attended: INTENT_SESSION_ATTENDED=1 set explicitly (override)"
  exit 0
fi

python3 <<'PY'
import os
import subprocess
import sys

# Ancestors that mean a human opened this. A GUI app or a terminal emulator in
# the chain means somebody launched it; launchd alone means a scheduler did.
INTERACTIVE = (
    "Claude",              # Claude Desktop
    "Terminal", "iTerm2", "WarpTerminal", "Ghostty", "Alacritty",
    "kitty", "Hyper", "rio", "wezterm-gui",
    "Code", "Electron", "Cursor", "Windsurf",   # editors embedding a terminal
    "tmux", "screen",      # attached multiplexer
    "sshd",                # a remote human
    "login",
)


def proc(pid):
    """Return (ppid, comm) for pid, or (None, None)."""
    try:
        out = subprocess.run(
            ["ps", "-o", "ppid=,comm=", "-p", str(pid)],
            capture_output=True, text=True, timeout=5,
        ).stdout.strip()
    except Exception:
        return None, None
    if not out:
        return None, None
    parts = out.split(None, 1)
    try:
        return int(parts[0]), (parts[1] if len(parts) > 1 else "")
    except Exception:
        return None, None


def verdict():
    # 1. Walk the ancestry looking for an interactive host.
    pid = os.getpid()
    seen = []
    for _ in range(30):
        ppid, comm = proc(pid)
        if ppid is None:
            break
        base = os.path.basename(comm or "")
        seen.append(base)
        for name in INTERACTIVE:
            # match the executable name, not a substring of a path segment
            if base == name or base.startswith(name + " ") or name in base.split("/"):
                return 0, "attended: interactive ancestor %s (pid %d)" % (base, pid)
        if ppid <= 1:
            break
        pid = ppid

    # Also check the full argv path of ancestors for .app bundles, which ps
    # comm truncates. Claude Desktop shows as a long bundle path.
    try:
        pid = os.getpid()
        for _ in range(30):
            ppid, _c = proc(pid)
            if ppid is None or ppid <= 1:
                break
            full = subprocess.run(
                ["ps", "-o", "command=", "-p", str(ppid)],
                capture_output=True, text=True, timeout=5,
            ).stdout.strip()
            if ".app/Contents/MacOS/" in full:
                app = full.split(".app/Contents/MacOS/")[0].split("/")[-1]
                return 0, "attended: GUI app ancestor %s.app" % app
            pid = ppid
    except Exception:
        pass

    # 2. No interactive ancestor. Confirm there is even a console user before
    #    considering anything else; a headless or logged-out box is unattended.
    try:
        console = subprocess.run(
            ["stat", "-f%Su", "/dev/console"],
            capture_output=True, text=True, timeout=5,
        ).stdout.strip()
    except Exception:
        console = ""
    if not console or console == "root":
        return 1, "unattended: no console user (chain: %s)" % ",".join(seen[:6])

    # 3. Reached launchd with a console user present but no interactive
    #    ancestor. This is exactly the overnight scheduled-job shape.
    return 1, "unattended: no interactive ancestor, scheduler-launched (chain: %s)" % ",".join(seen[:6])


try:
    code, reason = verdict()
except Exception as exc:
    # Fail closed on any error.
    code, reason = 1, "unattended: attendance check errored (%s)" % exc
print(reason)
sys.exit(code)
PY
