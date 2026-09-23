#!/usr/bin/env python3
# nested-repo-worktree-sibling-guard.sh
#
# PreToolUse hook (matcher: Bash). Refuses `git worktree add` on a nested Workspaces repo
# that carries the session kit (or on the Subaru engagement repo) unless the new worktree
# is a SIBLING of the repo's primary checkout named for its task:
#
#     <parent-of-primary>/<PrimaryBasename>-wt-<task>
#
# Supersedes subaru-worktree-sibling-guard.sh (retired 2026-09-23), which enforced the same
# rule for the Subaru repo only.
#
# Why this exists:
# - 2026-09-22: a session landed six PRs on the Subaru repo from worktrees parked in its
#   session scratchpad under /private/tmp. Brien ruled that Subaru worktrees live as
#   siblings named Subaru-wt-<task> (memory: feedback_subaru_worktree_pattern.md).
# - 2026-09-23: Brien ratified the same trunk-based branching standard for every nested
#   repo under ~/Workspaces ("approved roll this rule set out for everyone"). The marker
#   <repo>/.agents/SESSIONS.md means the session kit is installed; the helper
#   `python3 <repo>/.agents/bin/session start <task>` makes the sibling worktree.
#
# Scope:
# - Fires only on `git worktree add` in command position.
# - The target repo is resolved from `git -C`, a leading `cd`, or the tool cwd. Its PRIMARY
#   checkout is the parent of `git rev-parse --git-common-dir`, so a command run from inside
#   an existing linked worktree resolves to the same primary.
# - In scope: a primary checkout strictly inside ~/Workspaces that has .agents/SESSIONS.md,
#   or the Subaru engagement repo (by path or by origin URL). The ~/Workspaces root repo is
#   never in scope (Claude Code desktop isolates it under .claude/worktrees). A repo without
#   the kit is never in scope.
# - The new path is resolved from the command, including a simple VAR=value assignment
#   earlier in the same command. A path it cannot resolve on an in-scope repo is BLOCKED,
#   because "unknown" is exactly the scratchpad case.
# - Heredoc bodies are stripped before matching, so a commit message or a doc that quotes
#   the command never trips the guard.
# - Bypass: WORKTREE_SIBLING_GUARD_BYPASSED=1 (env or inline prefix); the retired
#   SUBARU_WORKTREE_GUARD_BYPASSED=1 is still honored. Logged.
# - Block signal: exit 2 + stderr (PreToolUse convention). An internal error fails open.
# - `--selftest` builds its own temp fixture repos for the non-Subaru cases and runs the
#   Subaru cases against the real primary checkout path when it exists on this machine.

import json
import os
import re
import shlex
import subprocess
import sys
import tempfile
from datetime import datetime, timezone
from pathlib import Path

BYPASS = "WORKTREE_SIBLING_GUARD_BYPASSED"
BYPASS_OLD = "SUBARU_WORKTREE_GUARD_BYPASSED"
HOME = str(Path.home())
WORKSPACES = HOME + "/Workspaces"
ENGAGEMENTS = WORKSPACES + "/Work/Consulting/Engagements"
SUBARU_PRIMARY = ENGAGEMENTS + "/Subaru"
SUBARU_SIBLING = re.compile(r"^Subaru-wt-[A-Za-z0-9][A-Za-z0-9._-]*$")
SUBARU_REMOTE_KEY = "engagement-subaru"
TASK_RE = r"[A-Za-z0-9][A-Za-z0-9._-]*"
KIT_MARKER = (".agents", "SESSIONS.md")
GIT_TIMEOUT = 5


def _log(msg: str) -> None:
    try:
        d = Path.home() / ".claude" / "logs"
        d.mkdir(parents=True, exist_ok=True)
        ts = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
        with (d / "worktree-sibling-guard.log").open("a") as fh:
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


def _real(p: str) -> str:
    return os.path.realpath(p)


def _effective_dir(cmd: str, cwd, m):
    """The directory git runs in: cwd, then a leading cd, then git -C (each relative to the last)."""
    base = os.path.expanduser(cwd) if cwd else None
    cm = re.search(r"(?:^|[;&|\n])\s*cd\s+([^\s;&|]+)", cmd)
    if cm:
        c = os.path.expanduser(cm.group(1).strip("\"'"))
        base = c if os.path.isabs(c) or not base else os.path.join(base, c)
    gm = re.search(r"-C\s+(\S+)", m.group("g") or "")
    if gm:
        c = os.path.expanduser(gm.group(1).strip("\"'"))
        base = c if os.path.isabs(c) or not base else os.path.join(base, c)
    return base


def _primary_of(d: str):
    """Primary checkout of the repo containing d, or None."""
    try:
        r = subprocess.run(["git", "-C", d, "rev-parse", "--git-common-dir"],
                           capture_output=True, text=True, timeout=GIT_TIMEOUT)
        if r.returncode != 0 or not r.stdout.strip():
            return None
        common = r.stdout.strip()
        if not os.path.isabs(common):
            common = os.path.join(d, common)
        common = _real(common)
        if os.path.basename(common) != ".git":
            return None  # bare repo or unusual layout: not ours to police
        return os.path.dirname(common)
    except Exception:
        return None


def _is_subaru(primary: str) -> bool:
    try:
        if _real(primary) == _real(SUBARU_PRIMARY):
            return True
        r = subprocess.run(["git", "-C", primary, "remote", "get-url", "origin"],
                           capture_output=True, text=True, timeout=GIT_TIMEOUT)
        return r.returncode == 0 and SUBARU_REMOTE_KEY in r.stdout
    except Exception:
        return False


def _subaru_by_path(d: str):
    """Fallback when d is not (yet) inside a git repo: the retired guard's path test."""
    real = _real(d)
    prim = _real(SUBARU_PRIMARY)
    if real == prim or real.startswith(prim + "/"):
        return SUBARU_PRIMARY
    parent, base = os.path.split(real)
    if _real(parent) == _real(ENGAGEMENTS) and SUBARU_SIBLING.match(base):
        return SUBARU_PRIMARY
    return None


def _in_scope(primary: str) -> bool:
    ws = _real(WORKSPACES)
    p = _real(primary)
    if p == ws:
        return False
    if p.startswith(ws + "/") and os.path.isfile(os.path.join(p, *KIT_MARKER)):
        return True
    return _is_subaru(p)


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
    """Return (verdict, detail, primary). verdict is 'allow' or 'block'."""
    if re.search(r"\b(?:" + BYPASS + "|" + BYPASS_OLD + r")=1\b", cmd):
        return "allow", "inline bypass", None
    stripped = _strip_heredocs(cmd)
    for m in re.finditer(_WT_ADD, stripped, re.M):
        d = _effective_dir(stripped, cwd, m)
        if not d or not os.path.isdir(d):
            continue
        primary = _primary_of(d) or _subaru_by_path(d)
        if not primary or not _in_scope(primary):
            continue
        primary = _real(primary)
        raw = _target_path(stripped, m.group("a") or "")
        if raw is None:
            return ("block", "the new worktree path could not be resolved "
                    "(a variable with no assignment in this command, or no path)", primary)
        raw = os.path.expanduser(raw)
        full = raw if os.path.isabs(raw) else os.path.join(d, raw)
        parent, name = os.path.split(os.path.normpath(full))
        parent_real = _real(parent) if os.path.isdir(parent) else os.path.normpath(parent)
        sibling = re.compile(r"^" + re.escape(os.path.basename(primary)) + r"-wt-" + TASK_RE + r"$")
        if parent_real == os.path.dirname(primary) and sibling.match(name):
            continue  # this add is fine; keep checking any later adds in the same command
        return "block", os.path.join(parent_real, name), primary
    return "allow", "no in-scope worktree add", None


def _block(detail: str, primary: str, cmd: str) -> int:
    _log(f"BLOCK primary={primary} target={detail} cmd={cmd[:160]!r}")
    base = os.path.basename(primary)
    parent = os.path.dirname(primary)
    print("\n".join([
        "",
        "BLOCKED: nested-repo-worktree-sibling-guard: a session worktree lives beside the primary checkout or nowhere",
        "",
        f"  Repo:      {primary}",
        f"  Requested: {detail}",
        f"  Allowed:   {parent}/{base}-wt-<task>   (task: letters, digits, . _ -)",
        "",
        "  Every nested Workspaces repo is trunk-based: main is the only long-lived branch, the",
        "  primary checkout stays on main and is never written to by agents, and every session",
        "  works in its own sibling worktree. Scratchpad worktrees vanish with the session, and",
        "  worktrees inside another checkout get swept up by its git status.",
        "",
        "  Do this instead:",
        f"    python3 {primary}/.agents/bin/session start <task>",
        "  If the kit helper is not there yet, the same thing by hand:",
        f"    cd {primary} && git fetch -q origin && \\",
        f"      git worktree add ../{base}-wt-<yyyy-mm-dd>-<task> -b agent/claude/<yyyy-mm-dd>-<task> origin/main",
        "  Land: rebase on origin/main, PR, squash merge, delete the branch, remove the worktree,",
        "  then `git pull --ff-only origin main` in the primary checkout.",
        "",
        "  Bypass only with a reason you would put in the commit message:",
        f"    {BYPASS}=1 <retry-command>",
        "",
    ]), file=sys.stderr)
    return 2


# ---------------------------------------------------------------- selftest

def _git(*args, cwd=None):
    subprocess.run(["git", "-c", "core.hooksPath=/dev/null", "-c", "user.name=selftest",
                    "-c", "user.email=selftest@example.invalid", "-c", "commit.gpgsign=false",
                    *args], cwd=cwd, check=True, capture_output=True, timeout=30)


def _mkrepo(path: str, kit: bool, commit: bool = False) -> str:
    os.makedirs(path, exist_ok=True)
    _git("init", "-q", "-b", "main", path)
    if kit:
        os.makedirs(os.path.join(path, ".agents"), exist_ok=True)
        Path(path, *KIT_MARKER).write_text("session kit marker (selftest)\n")
    if commit:
        _git("commit", "-q", "--allow-empty", "-m", "init", cwd=path)
    return path


def _selftest() -> int:
    global WORKSPACES
    results = []

    def run(label, cmd, cwd, want):
        got, detail, _ = decide(cmd, cwd)
        results.append((got == want, label, want, got, cmd, detail))

    # Subaru cases (the retired guard's set), against the real primary path.
    P = SUBARU_PRIMARY
    if os.path.isdir(P):
        run("subaru sibling", "git worktree add ../Subaru-wt-foo -b agent/claude/2026-09-22-foo origin/main", P, "allow")
        run("subaru cd then sibling", "cd " + P + " && git fetch -q origin main && git worktree add ../Subaru-wt-foo -b x origin/main", WORKSPACES, "allow")
        run("subaru scratchpad", "git worktree add -q -b land/x /private/tmp/claude-501/scratchpad/engagement-subaru-wt origin/main", P, "block")
        run("subaru scratchpad via var", "WT=/private/tmp/claude-501/scratchpad/engagement-subaru-wt && git worktree add -q -b land/x \"$WT\" origin/main", P, "block")
        run("subaru -C to /tmp", "git -C " + P + " worktree add /tmp/x -b y", HOME, "block")
        run("workspaces root, not subaru", "git worktree add ../Subaru-wt-foo", WORKSPACES, "allow")
        run("subaru wrong name", "git worktree add ../foo -b y origin/main", P, "block")
        run("subaru into .claude/worktrees", "git worktree add " + WORKSPACES + "/.claude/worktrees/Subaru-wt-foo -b y", P, "block")
        run("subaru unset var", "git worktree add \"$UNSET_VAR\" -b y", P, "block")
        run("subaru list", "git worktree list", P, "allow")
        run("subaru remove", "git worktree remove ../Subaru-wt-foo", P, "allow")
        run("subaru heredoc", "cat <<'EOF'\ngit worktree add /tmp/x\nEOF", P, "allow")
        run("subaru old bypass", BYPASS_OLD + "=1 git worktree add /tmp/x", P, "allow")
    else:
        print(f"SKIP subaru cases: {P} not on this machine")

    real_ws = WORKSPACES
    tmp = _real(tempfile.mkdtemp(prefix="wt-guard-selftest-"))
    try:
        ws = os.path.join(tmp, "Workspaces")
        WORKSPACES = ws
        _mkrepo(ws, kit=True)  # root carries the marker too: must still never fire
        prod = _mkrepo(os.path.join(ws, "Core", "products", "prod"), kit=True, commit=True)
        intent = _mkrepo(os.path.join(ws, "Core", "frameworks", "intent"), kit=True)
        adv = _mkrepo(os.path.join(ws, "Work", "Advising", "Engagements", "Foo"), kit=True)
        nokit = _mkrepo(os.path.join(ws, "Core", "products", "nokit"), kit=False)
        existing = os.path.join(ws, "Core", "products", "prod-wt-2026-09-23-existing")
        _git("worktree", "add", "-q", "-b", "agent/claude/2026-09-23-existing", existing, cwd=prod)
        scratch = os.path.join(tmp, "scratchpad", "prod-wt")

        run("products sibling", "git worktree add ../prod-wt-2026-09-23-x -b agent/claude/2026-09-23-x origin/main", prod, "allow")
        run("products scratchpad", f"git worktree add {scratch} -b y origin/main", prod, "block")
        run("products wrong basename", "git worktree add ../other-wt-x -b y", prod, "block")
        run("products no task", "git worktree add ../prod-wt- -b y", prod, "block")
        run("products unset var", "git worktree add \"$NOPE\" -b y", prod, "block")
        run("products var to sibling", f"WT={ws}/Core/products/prod-wt-2026-09-23-v && git worktree add -b y \"$WT\"", prod, "allow")
        run("products from linked worktree, sibling", "git worktree add ../prod-wt-2026-09-23-next -b z", existing, "allow")
        run("products from linked worktree, nested", "git worktree add ./nested -b z", existing, "block")
        run("products second add bad", f"git worktree add ../prod-wt-ok -b a && git worktree add {scratch} -b b", prod, "block")
        run("products list", "git worktree list", prod, "allow")
        run("products remove", f"git worktree remove {scratch}", prod, "allow")
        run("products heredoc", f"git commit -F - <<'EOF'\ngit worktree add {scratch}\nEOF", prod, "allow")
        run("products inline bypass", f"{BYPASS}=1 git worktree add {scratch}", prod, "allow")
        run("intent cd then sibling", f"cd {intent} && git fetch -q origin && git worktree add ../intent-wt-2026-09-23-foo -b b origin/main", ws, "allow")
        run("intent -C sibling", f"git -C {intent} worktree add {intent}/../intent-wt-foo -b b", tmp, "allow")
        run("intent -C into .claude/worktrees", f"git -C {intent} worktree add .claude/worktrees/x -b b", tmp, "block")
        run("advising sibling", "git worktree add ../Foo-wt-task -b b", adv, "allow")
        run("advising missing -wt-", "git worktree add ../Foo-task -b b", adv, "block")
        run("workspaces root never fires", f"git worktree add {tmp}/anywhere -b b", ws, "allow")
        run("workspaces root .claude/worktrees", "git worktree add .claude/worktrees/foo -b b", ws, "allow")
        run("repo without kit never fires", f"git worktree add {tmp}/x -b b", nokit, "allow")
        run("non-git dir never fires", f"git worktree add {tmp}/x -b b", tmp, "allow")
    finally:
        WORKSPACES = real_ws
        subprocess.run(["rm", "-rf", tmp], timeout=30)

    bad = 0
    for ok, label, want, got, cmd, detail in results:
        bad += 0 if ok else 1
        print(f"{'PASS' if ok else 'FAIL'} {label}: want={want} got={got} :: {cmd[:70]!r} :: {detail}")
    print(f"selftest {len(results) - bad}/{len(results)}")
    return 0 if bad == 0 else 1


def main() -> int:
    if "--selftest" in sys.argv:
        return _selftest()
    for var in (BYPASS, BYPASS_OLD):
        if os.environ.get(var) == "1":
            _log(f"BYPASS env={var} session={os.environ.get('CLAUDE_SESSION_ID', 'unknown')}")
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
    try:
        verdict, detail, primary = decide(cmd, payload.get("cwd"))
    except Exception as e:  # a guard bug must not wedge every Bash call
        _log(f"ERROR fail-open {type(e).__name__}: {e} cmd={cmd[:160]!r}")
        return 0
    if verdict == "block":
        return _block(detail, primary, cmd)
    if detail == "inline bypass":
        _log(f"BYPASS inline cmd={cmd[:160]!r}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
