#!/usr/bin/env python3
# subaru-worktree-sibling-guard.sh
#
# PreToolUse hook (matcher: Bash). Refuses `git worktree add` on the Subaru engagement
# repo (theparlor/engagement-subaru) unless the new worktree is a SIBLING of the primary
# checkout named for its task: <...>/Work/Consulting/Engagements/Subaru-wt-<task>.
#
# Why this exists:
# - 2026-09-22: a session running in a Workspaces worktree landed six PRs on the Subaru repo
#   from worktrees parked in its session scratchpad under /private/tmp, and once tried to
#   write into the primary checkout (the Write tool refused that; nothing refused the
#   scratchpad). The engagement's own .agents/WORKFLOW.md had prescribed the sibling form
#   since August. Brien: "we have to make sure we have the branching and checkout pattern
#   resolved at this point" and then "move the worktrees to the Subaru-wt sibling pattern
#   going forward." Memory: feedback_subaru_worktree_pattern.md.
# - A memory and a WORKFLOW.md are not a mechanism. This hook sits between the intent and
#   the call. The repo's .githooks/pre-commit (section 7) carries the backstop for
#   worktrees made outside Claude Code.
#
# Scope:
# - Fires only on `git worktree add` in command position, only when the repo it targets is
#   the Subaru engagement repo (by path under Engagements/Subaru*, or by origin URL).
# - Resolves the new path from -C, a leading cd, or the tool cwd; resolves a simple
#   VAR=value assignment earlier in the same command. A path it cannot resolve on a Subaru
#   repo is BLOCKED (state the path literally), because "unknown" is exactly the scratchpad
#   case. On any other repo it never fires.
# - Bypass: SUBARU_WORKTREE_GUARD_BYPASSED=1 (env or inline prefix), logged.
# - Block signal: exit 2 + stderr (PreToolUse convention).
# - `--selftest` runs the cases below against the real primary checkout path.

import json
import os
import re
import shlex
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

BYPASS = "SUBARU_WORKTREE_GUARD_BYPASSED"
HOME = str(Path.home())
ENGAGEMENTS = HOME + "/Workspaces/Work/Consulting/Engagements"
PRIMARY = ENGAGEMENTS + "/Subaru"
SIBLING = re.compile(r"^Subaru-wt-[A-Za-z0-9][A-Za-z0-9._-]*$")
REMOTE_KEY = "engagement-subaru"


def _log(msg: str) -> None:
    try:
        d = Path.home() / ".claude" / "logs"
        d.mkdir(parents=True, exist_ok=True)
        ts = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
        with (d / "subaru-worktree-guard.log").open("a") as fh:
            fh.write(f"[{ts}] {msg}\n")
    except Exception:
        pass


def _strip_heredocs(cmd: str) -> str:
    out, term = [], None
    for line in cmd.split("\n"):
        if term is not None:
            if line.strip() == term:
                term = None
            continue
        m = re.search(r"<<-?\s*(['\"]?)([A-Za-z_][A-Za-z0-9_]*)\1", line)
        out.append(line)
        if m:
            term = m.group(2)
    return "\n".join(out)


_CMDPOS = (
    r"(?:^|[;&|({`])\s*"
    r"(?:(?:sudo|env|command|exec|nohup|time|timeout|xargs|nice|stdbuf|caffeinate)\s+"
    r"|-\S+\s+"
    r"|\d+[smh]?\s+"
    r"|[A-Za-z_][A-Za-z0-9_]*=\S*\s+"
    r")*"
)
_WT_ADD = _CMDPOS + r"git\b(?P<g>(?:\s+-\S+(?:\s+\S+)?)*)\s+worktree\s+add\b(?P<a>[^;&|\n]*)"
_VALUE_OPTS = {"-b", "-B", "--reason", "--orphan"}


def _repo_dirs(cmd: str, cwd, m) -> list:
    cands = []
    gm = re.search(r"-C\s+(\S+)", m.group("g") or "")
    if gm:
        cands.append(gm.group(1).strip("\"'"))
    cm = re.search(r"(?:^|[;&|\n])\s*cd\s+([^\s;&|]+)", cmd)
    if cm:
        cands.append(cm.group(1).strip("\"'"))
    if cwd:
        cands.append(cwd)
    return [os.path.expanduser(c) for c in cands]


def _is_subaru_repo(d: str) -> bool:
    try:
        real = os.path.realpath(d)
        if real == PRIMARY or real.startswith(PRIMARY + "/"):
            return True
        parent, base = os.path.split(real)
        if os.path.realpath(parent) == os.path.realpath(ENGAGEMENTS) and SIBLING.match(base):
            return True
        r = subprocess.run(["git", "-C", d, "remote", "get-url", "origin"],
                           capture_output=True, text=True, timeout=10)
        return r.returncode == 0 and REMOTE_KEY in r.stdout
    except Exception:
        return False


def _resolve_var(cmd: str, token: str):
    m = re.match(r'^"?\$\{?([A-Za-z_][A-Za-z0-9_]*)\}?"?(/.*)?$', token)
    if not m:
        return token
    var, tail = m.group(1), m.group(2) or ""
    am = re.search(r"(?:^|[;&|\n\s])" + re.escape(var) + r"=([^\s;&|]+)", cmd)
    if not am:
        return None
    return am.group(1).strip("\"'") + tail


def _target_path(cmd: str, args: str):
    try:
        toks = shlex.split(args)
    except ValueError:
        toks = args.split()
    i = 0
    while i < len(toks):
        t = toks[i]
        if t in _VALUE_OPTS:
            i += 2
            continue
        if t.startswith("-"):
            i += 1
            continue
        return _resolve_var(cmd, t)
    return None


def decide(cmd: str, cwd):
    """Return (verdict, detail). verdict is 'allow' or 'block'."""
    if re.search(r"\b" + BYPASS + r"=1\b", cmd):
        return "allow", "inline bypass"
    stripped = _strip_heredocs(cmd)
    for m in re.finditer(_WT_ADD, stripped, re.M):
        base = None
        subaru = False
        for d in _repo_dirs(stripped, cwd, m):
            if os.path.isdir(d):
                base = d
                subaru = _is_subaru_repo(d)
                break
        if not subaru:
            continue
        raw = _target_path(stripped, m.group("a") or "")
        if raw is None:
            return "block", "the new worktree path could not be resolved (a variable with no assignment in this command, or no path)"
        raw = os.path.expanduser(raw)
        full = raw if os.path.isabs(raw) else os.path.join(base or cwd or ".", raw)
        parent, name = os.path.split(os.path.normpath(full))
        parent_real = os.path.realpath(parent) if os.path.isdir(parent) else os.path.normpath(parent)
        if parent_real == os.path.realpath(ENGAGEMENTS) and SIBLING.match(name):
            return "allow", os.path.join(parent_real, name)
        return "block", os.path.join(parent_real, name)
    return "allow", "no subaru worktree add"


def _block(detail: str, cmd: str) -> int:
    _log(f"BLOCK target={detail} cmd={cmd[:160]!r}")
    print("\n".join([
        "",
        "BLOCKED: subaru-worktree-sibling-guard: a Subaru worktree lives beside the primary checkout or nowhere",
        "",
        f"  Requested: {detail}",
        f"  Allowed:   {ENGAGEMENTS}/Subaru-wt-<task>",
        "",
        "  The Subaru engagement repo is nested and gitignored from Workspaces, so a Workspaces",
        "  worktree never contains it; its primary checkout is user-owned; and scratchpad",
        "  worktrees vanish with the session. The engagement's .agents/WORKFLOW.md prescribes",
        "  one sibling worktree per task. Brien, 2026-09-22: move to the Subaru-wt sibling pattern.",
        "",
        "  Do this instead, from the primary checkout:",
        "    cd " + PRIMARY + " && git fetch -q origin main && \\",
        "      git worktree add ../Subaru-wt-<task> -b agent/claude/<yyyy-mm-dd>-<task> origin/main",
        "  Then commit there, PR, merge, `git worktree remove ../Subaru-wt-<task>`, and",
        "  `git pull --ff-only origin main` in the primary checkout.",
        "",
        "  Bypass only with a reason you would put in the commit message:",
        f"    {BYPASS}=1 <retry-command>",
        "",
        "  Memory: feedback_subaru_worktree_pattern.md",
        "",
    ]), file=sys.stderr)
    return 2


def _selftest() -> int:
    cases = [
        ("git worktree add ../Subaru-wt-foo -b agent/claude/2026-09-22-foo origin/main", PRIMARY, "allow"),
        ("cd " + PRIMARY + " && git fetch -q origin main && git worktree add ../Subaru-wt-foo -b x origin/main", HOME + "/Workspaces", "allow"),
        ("git worktree add -q -b land/x /private/tmp/claude-501/scratchpad/engagement-subaru-wt origin/main", PRIMARY, "block"),
        ("WT=/private/tmp/claude-501/scratchpad/engagement-subaru-wt && git worktree add -q -b land/x \"$WT\" origin/main", PRIMARY, "block"),
        ("git -C " + PRIMARY + " worktree add /tmp/x -b y", HOME, "block"),
        ("git worktree add ../Subaru-wt-foo", HOME + "/Workspaces", "allow"),
        ("git worktree add ../foo -b y origin/main", PRIMARY, "block"),
        ("git worktree add " + HOME + "/Workspaces/.claude/worktrees/Subaru-wt-foo -b y", PRIMARY, "block"),
        ("git worktree add \"$UNSET_VAR\" -b y", PRIMARY, "block"),
        ("git worktree list", PRIMARY, "allow"),
        ("git worktree remove ../Subaru-wt-foo", PRIMARY, "allow"),
        ("cat <<'EOF'\ngit worktree add /tmp/x\nEOF", PRIMARY, "allow"),
        (BYPASS + "=1 git worktree add /tmp/x", PRIMARY, "allow"),
    ]
    bad = 0
    for cmd, cwd, want in cases:
        got, detail = decide(cmd, cwd)
        ok = got == want
        bad += 0 if ok else 1
        print(f"{'PASS' if ok else 'FAIL'} want={want} got={got} :: {cmd[:70]!r} :: {detail}")
    print(f"selftest {len(cases) - bad}/{len(cases)}")
    return 0 if bad == 0 else 1


def main() -> int:
    if "--selftest" in sys.argv:
        return _selftest()
    if os.environ.get(BYPASS) == "1":
        _log(f"BYPASS session={os.environ.get('CLAUDE_SESSION_ID', 'unknown')}")
        return 0
    raw = sys.stdin.read()
    if not raw.strip():
        return 0
    try:
        payload = json.loads(raw)
    except Exception:
        return 0
    if (payload.get("tool_name") or "") != "Bash":
        return 0
    cmd = ((payload.get("tool_input") or {}).get("command") or "")
    if not cmd.strip() or "worktree" not in cmd:
        return 0
    verdict, detail = decide(cmd, payload.get("cwd"))
    if verdict == "block":
        return _block(detail, cmd)
    return 0


if __name__ == "__main__":
    sys.exit(main())
