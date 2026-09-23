#!/usr/bin/env python3
# nested-repo-primary-write-guard.sh
#
# PreToolUse hook (matcher: Write|Edit|NotebookEdit|MultiEdit). Refuses a file write into
# the PRIMARY checkout of a nested Workspaces repo that carries the session kit
# (<repo>/.agents/SESSIONS.md), unless git ignores the path. Sessions write in their own
# sibling worktree instead: `python3 <repo>/.agents/bin/session start <task>`.
#
# Why this exists:
# - 2026-09-23: Brien ratified a trunk-based branching standard for every nested repo under
#   ~/Workspaces ("approved roll this rule set out for everyone"). The primary checkout stays
#   on main and is never written to by agents; parallel sessions editing the same primary
#   checkout collide, and their half-done edits strand on main. Its sibling guard for
#   `git worktree add` is nested-repo-worktree-sibling-guard.sh.
#
# Decision, for the target path:
# - Find the nearest enclosing git checkout by walking up from the path (the path or its
#   directories need not exist yet) until a `.git` entry appears.
# - `.git` is a FILE: a linked worktree. Allow.
# - `.git` is a directory: a primary checkout. Allow if it is ~/Workspaces itself (the root
#   repo, isolated by Claude Code desktop worktrees), if it lacks .agents/SESSIONS.md, or if
#   `git check-ignore` says the path is ignored (scratch, caches, local state). Else BLOCK.
# - Every internal error fails OPEN (exit 0, logged): a guard bug must never wedge writes.
# - One git subprocess on the block path, 5s timeout.
# - Bypass: NESTED_REPO_PRIMARY_WRITE_BYPASSED=1 in the environment, logged with the path.
# - Block signal: exit 2 + stderr (PreToolUse convention).
# - `--selftest` builds temp fixture repos and runs the decision table plus five end-to-end
#   stdin payloads through this file.

import json
import os
import subprocess
import sys
import tempfile
from datetime import datetime, timezone
from pathlib import Path

BYPASS = "NESTED_REPO_PRIMARY_WRITE_BYPASSED"
HOME = str(Path.home())
WORKSPACES = HOME + "/Workspaces"
KIT_MARKER = (".agents", "SESSIONS.md")
TOOLS = {"Write", "Edit", "NotebookEdit", "MultiEdit"}
GIT_TIMEOUT = 5


def _log(msg: str) -> None:
    try:
        d = Path.home() / ".claude" / "logs"
        d.mkdir(parents=True, exist_ok=True)
        ts = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
        with (d / "nested-repo-primary-write-guard.log").open("a") as fh:
            fh.write(f"[{ts}] {msg}\n")
    except Exception:
        pass


def _checkout_of(path: str):
    """(checkout_dir, git_is_file) for the nearest enclosing .git, or (None, None)."""
    d = os.path.dirname(path)
    while True:
        g = os.path.join(d, ".git")
        if os.path.lexists(g):
            return d, not os.path.isdir(g)
        up = os.path.dirname(d)
        if up == d:
            return None, None
        d = up


def decide(path: str, cwd=None):
    """Return (verdict, detail, checkout). verdict is 'allow' or 'block'."""
    if not path:
        return "allow", "no path", None
    path = os.path.expanduser(path)
    if not os.path.isabs(path):
        path = os.path.join(os.path.expanduser(cwd) if cwd else os.getcwd(), path)
    path = os.path.normpath(path)
    checkout, git_is_file = _checkout_of(path)
    if checkout is None:
        return "allow", "not in a git checkout", None
    if git_is_file:
        return "allow", "linked worktree", checkout
    if os.path.realpath(checkout) == os.path.realpath(WORKSPACES):
        return "allow", "workspaces root repo", checkout
    if not os.path.isfile(os.path.join(checkout, *KIT_MARKER)):
        return "allow", "no session kit", checkout
    rel = os.path.relpath(path, checkout)
    if rel == ".git" or rel.startswith(".git" + os.sep):
        return "allow", "inside .git", checkout
    r = subprocess.run(["git", "check-ignore", "-q", "--", rel], cwd=checkout,
                       capture_output=True, text=True, timeout=GIT_TIMEOUT)
    if r.returncode == 0:
        return "allow", "ignored path", checkout
    if r.returncode == 1:
        return "block", rel, checkout
    raise RuntimeError(f"git check-ignore rc={r.returncode}: {r.stderr.strip()[:200]}")


def _block(rel: str, checkout: str, path: str) -> int:
    _log(f"BLOCK checkout={checkout} path={path}")
    print("\n".join([
        "",
        "BLOCKED: nested-repo-primary-write-guard: this is the shared primary checkout, not your session's worktree",
        "",
        f"  Checkout: {checkout}",
        f"  Path:     {rel}",
        "",
        "  This repo runs trunk-based with the session kit: the primary checkout stays on main",
        "  and no agent writes to it, because every parallel session shares it. Start (or reuse)",
        "  your own sibling worktree and make the same edit there:",
        "",
        f"    python3 {checkout}/.agents/bin/session start <task>",
        "",
        f"  Then edit <printed worktree>/{rel}, commit there, PR, squash merge.",
        "  Git-ignored paths (scratch, caches, local state) are not affected.",
        "",
        "  Bypass only with a reason you would put in the commit message (logged):",
        f"    {BYPASS}=1 in the session environment",
        "",
    ]), file=sys.stderr)
    return 2


def _handle(payload: dict) -> int:
    if (payload.get("tool_name") or "") not in TOOLS:
        return 0
    ti = payload.get("tool_input") or {}
    path = ti.get("file_path") or ti.get("notebook_path") or ""
    if not path:
        return 0
    if os.environ.get(BYPASS) == "1":
        _log(f"BYPASS path={path} session={os.environ.get('CLAUDE_SESSION_ID', 'unknown')}")
        return 0
    verdict, detail, checkout = decide(path, payload.get("cwd"))
    if verdict == "block":
        return _block(detail, checkout, path)
    return 0


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
        Path(path, ".gitignore").write_text("scratch/\n*.log\n")
    if commit:
        _git("commit", "-q", "--allow-empty", "-m", "init", cwd=path)
    return path


def _selftest() -> int:
    global WORKSPACES
    results = []

    def run(label, path, want, cwd=None):
        got, detail, _ = decide(path, cwd)
        results.append((got == want, label, want, got, path, detail))

    real_ws = WORKSPACES
    tmp = os.path.realpath(tempfile.mkdtemp(prefix="write-guard-selftest-"))
    try:
        ws = os.path.join(tmp, "Workspaces")
        WORKSPACES = ws
        _mkrepo(ws, kit=True)  # root carries the marker too: must still never fire
        kit = _mkrepo(os.path.join(ws, "Core", "products", "kit"), kit=True, commit=True)
        nokit = _mkrepo(os.path.join(ws, "Core", "products", "nokit"), kit=False)
        wt = os.path.join(ws, "Core", "products", "kit-wt-2026-09-23-x")
        _git("worktree", "add", "-q", "-b", "agent/claude/2026-09-23-x", wt, cwd=kit)

        run("primary with kit, tracked-style file", os.path.join(kit, "README.md"), "block")
        run("primary with kit, new nested subdir", os.path.join(kit, "new", "deeper", "x.md"), "block")
        run("primary with kit, the marker itself", os.path.join(kit, ".agents", "SESSIONS.md"), "block")
        run("primary with kit, relative path", "docs/y.md", "block", cwd=kit)
        run("primary with kit, ignored dir", os.path.join(kit, "scratch", "notes.md"), "allow")
        run("primary with kit, ignored glob", os.path.join(kit, "run.log"), "allow")
        run("primary with kit, inside .git", os.path.join(kit, ".git", "info", "exclude"), "allow")
        run("primary without kit", os.path.join(nokit, "README.md"), "allow")
        run("linked worktree", os.path.join(wt, "README.md"), "allow")
        run("linked worktree, new subdir", os.path.join(wt, "new", "x.md"), "allow")
        run("workspaces root repo", os.path.join(ws, "notes.md"), "allow")
        run("workspaces root, non-repo subdir", os.path.join(ws, "Core", "loose.md"), "allow")
        run("outside any repo", os.path.join(tmp, "elsewhere", "x.md"), "allow")

        # End to end through this file: stdin payload in, exit code out.
        me = os.path.abspath(__file__)
        env = dict(os.environ)
        env.pop(BYPASS, None)

        def e2e(label, payload, want_rc, extra_env=None):
            e = dict(env, **(extra_env or {}))
            # runpy under a non-main name, then point the loaded module at the fixture root.
            r = subprocess.run([sys.executable, "-c",
                                "import sys,runpy;g=runpy.run_path(%r,run_name='selftest_e2e');"
                                "g['main'].__globals__['WORKSPACES']=%r;sys.exit(g['main']())" % (me, ws)],
                               input=json.dumps(payload), capture_output=True, text=True,
                               timeout=30, env=e)
            ok = r.returncode == want_rc
            results.append((ok, label, f"rc={want_rc}", f"rc={r.returncode}", payload["tool_input"],
                            (r.stderr.strip().splitlines() or [""])[0][:90]))

        e2e("e2e Write into primary blocks",
            {"tool_name": "Write", "tool_input": {"file_path": os.path.join(kit, "a.md")}}, 2)
        e2e("e2e NotebookEdit into primary blocks",
            {"tool_name": "NotebookEdit", "tool_input": {"notebook_path": os.path.join(kit, "n.ipynb")}}, 2)
        e2e("e2e Edit in worktree allows",
            {"tool_name": "Edit", "tool_input": {"file_path": os.path.join(wt, "a.md")}}, 0)
        e2e("e2e bypass env allows",
            {"tool_name": "Write", "tool_input": {"file_path": os.path.join(kit, "a.md")}}, 0,
            {BYPASS: "1"})
        e2e("e2e Bash tool ignored",
            {"tool_name": "Bash", "tool_input": {"command": "echo hi"}}, 0)
    finally:
        WORKSPACES = real_ws
        subprocess.run(["rm", "-rf", tmp], timeout=30)

    bad = 0
    for ok, label, want, got, path, detail in results:
        bad += 0 if ok else 1
        print(f"{'PASS' if ok else 'FAIL'} {label}: want={want} got={got} :: {detail}")
    print(f"selftest {len(results) - bad}/{len(results)}")
    return 0 if bad == 0 else 1


def main() -> int:
    if "--selftest" in sys.argv:
        return _selftest()
    try:
        raw = sys.stdin.read()
        if not raw.strip():
            return 0
        return _handle(json.loads(raw))
    except Exception as e:  # fail open, always
        _log(f"ERROR fail-open {type(e).__name__}: {e}")
        return 0


if __name__ == "__main__":
    sys.exit(main())
