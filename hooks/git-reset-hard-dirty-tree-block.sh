#!/usr/bin/env python3
# git-reset-hard-dirty-tree-block.sh
#
# PreToolUse hook (matcher: Bash). Blocks `git reset --hard` / `git checkout -f`
# when the target repo has UNCOMMITTED TRACKED modifications, because those
# commands delete them with no git object left behind to recover from.
#
# Why this exists:
# - 2026-07-23: a cleanup sweep ran `git reset --hard origin/main` across six
#   repos to realign local main after landing commits via PR. Eight unstaged file
#   modifications were destroyed. Unrecoverable: never staged, so git held no
#   blob, and there were no APFS local snapshots.
#   SIG-RESET-HARD-DESTROYED-UNCOMMITTED-WORK-2026-07-23.
# - 2026-07-24: the IDENTICAL failure recurred, in a scheduled task, one day
#   later, with yesterday's signal sitting on disk and printed in the session's
#   own startup git-hygiene output. 5,440 bytes of Subaru CRM runbook findings
#   destroyed. Recovered only by replaying the authoring session's transcript.
#   SIG-RESET-HARD-DESTROYED-UNCOMMITTED-WORK-2026-07-24.
# - Memory, a signal file, and a git-hygiene SessionStart hook were all present
#   and all insufficient: none of them sits BETWEEN the intent and the call.
#   This hook does. It is the mechanism-level fix.
#
# Scope (conservative — a dirty tree is the ONLY thing that makes these calls
# destructive, so a clean tree always passes):
# - Triggers on `git reset --hard` (any arg order) and `git checkout -f`/
#   `--force` in command position. NOT on `reset --soft`/`--mixed`, not on
#   `git clean` (that is an untracked-file decision with different tradeoffs).
# - Blocks ONLY when `git status --porcelain` in the resolved repo reports a
#   TRACKED change. Untracked (`??`) entries are ignored: `reset --hard` does
#   not touch them.
# - Anything it cannot resolve → ALLOW (fail open). Better to miss than misfire.
#
# The safe realign after a PR merges (the case that caused both incidents):
#     git reset --soft origin/main     # keeps the working tree
#     git stash && git reset --hard origin/main && git stash pop
# Recorded practice for the PR-only repos: memory project_quartermaster_repo_requires_pr.
#
# Linked-worktree rule (added 2026-09-13, SIG-SUBAGENT-BRIEF-PROHIBITIONS-IGNORED-UNDER-DRIFT):
# - Inside a LINKED WORKTREE (git-dir under <common>/worktrees/, or a path containing
#   /.worktrees/ or /.claude/worktrees/) the guard blocks `git stash` (every mutating
#   form: bare, push, save, pop, apply, drop, clear, branch, create, store) and
#   `git reset --hard` / `git checkout -f` REGARDLESS of tree state. The stash stack is
#   shared with the main checkout and every other session's worktree, so a stash there
#   can be popped by someone else, and a reset --hard is never the right realign in a
#   worktree: `git rebase origin/main` or a WIP commit is. A Sonnet subagent did exactly
#   this on 2026-09-13 after being told not to; prose in a brief lost to a known idiom.
# - `git stash list` and `git stash show` are read-only and always pass.
# - Outside a linked worktree, stash is untouched by this hook (scope is deliberate).
#
# Bypass: GIT_RESET_HARD_GUARD_BYPASSED=1 (logged). Honored from the hook's own
#   environment AND as an inline command prefix, since env prefixes on the user
#   command never reach the hook process (the venv-guard reachability lesson,
#   SIG-2026-06-12).
# Heredoc bodies are stripped before matching: a commit message that mentions
#   `git reset --hard` is data, not a command (the venv-guard heredoc false
#   positive, SIG-2026-06-12-venv-guard-heredoc-false-positive.md).
# Block signal: exit 2 + stderr (PreToolUse convention).

import json
import os
import re
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

BYPASS = "GIT_RESET_HARD_GUARD_BYPASSED"


def _log(msg: str) -> None:
    try:
        d = Path.home() / ".claude" / "logs"
        d.mkdir(parents=True, exist_ok=True)
        ts = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
        with (d / "git-reset-hard-guard.log").open("a") as fh:
            fh.write(f"[{ts}] {msg}\n")
    except Exception:
        pass


def _strip_heredocs(cmd: str) -> str:
    """Drop heredoc BODIES before matching. The line carrying `<<MARKER` is kept;
    every line up to and including the terminator is dropped. Over-stripping only
    under-blocks, which matches the fail-open posture."""
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


# `git` in command position: start of command/line, after ; & | ( { `, or through
# wrapper/env/VAR=val prefixes. Never fires on the word inside an argument.
_CMDPOS = (
    r"(?:^|[;&|({`])\s*"
    r"(?:(?:sudo|env|command|exec|nohup|time|timeout|xargs|nice|stdbuf|caffeinate)\s+"
    r"|-\S+\s+"
    r"|\d+[smh]?\s+"
    r"|[A-Za-z_][A-Za-z0-9_]*=\S*\s+"
    r")*"
)
# `git [-C <path>] [other global flags] reset ... --hard ...`
_GIT_RESET_HARD = _CMDPOS + r"git\b(?P<g>(?:\s+-\S+(?:\s+\S+)?)*)\s+reset\b(?P<a>[^;&|\n]*)"
_GIT_CHECKOUT_F = _CMDPOS + r"git\b(?P<g2>(?:\s+-\S+(?:\s+\S+)?)*)\s+checkout\b(?P<a2>[^;&|\n]*)"
# `git [-C <path>] stash [subcommand ...]`
_GIT_STASH = _CMDPOS + r"git\b(?P<g3>(?:\s+-\S+(?:\s+\S+)?)*)\s+stash\b(?P<a3>[^;&|\n]*)"
_STASH_READONLY = ("list", "show")


def _repo_dirs(cmd: str, cwd, m) -> list:
    """Candidate directories for the repo, most specific first."""
    cands = []
    # `git -C <path>` on the matched invocation wins.
    g = (m.groupdict().get("g") or m.groupdict().get("g2") or m.groupdict().get("g3") or "")
    gm = re.search(r"-C\s+(\S+)", g)
    if gm:
        cands.append(gm.group(1).strip("\"'"))
    # a leading `cd <path> && …` in the same command
    cm = re.search(r"(?:^|[;&|\n])\s*cd\s+([^\s;&|]+)", cmd)
    if cm:
        cands.append(cm.group(1).strip("\"'"))
    if cwd:
        cands.append(cwd)
    return [os.path.expanduser(c) for c in cands]


def _dirty_tracked(repo_dir: str):
    """Return (repo_root, [porcelain lines]) for TRACKED changes, or None if this
    is not a repo / git is unavailable / anything is unresolvable (fail open)."""
    try:
        root = subprocess.run(
            ["git", "-C", repo_dir, "rev-parse", "--show-toplevel"],
            capture_output=True, text=True, timeout=10)
        if root.returncode != 0:
            return None
        top = root.stdout.strip()
        st = subprocess.run(
            ["git", "-C", top, "status", "--porcelain"],
            capture_output=True, text=True, timeout=15)
        if st.returncode != 0:
            return None
        # `??` is untracked; `reset --hard` leaves those alone.
        lines = [ln for ln in st.stdout.splitlines()
                 if ln.strip() and not ln.startswith("??")]
        return top, lines
    except Exception:
        return None


def _linked_worktree(repo_dir: str):
    """Return the worktree root if repo_dir is inside a LINKED git worktree (or a path that
    names one), else None. Fail open on anything unresolvable."""
    try:
        top = subprocess.run(["git", "-C", repo_dir, "rev-parse", "--show-toplevel"],
                             capture_output=True, text=True, timeout=10)
        if top.returncode != 0:
            return None
        top_s = top.stdout.strip()
        if "/.worktrees/" in top_s + "/" or "/.claude/worktrees/" in top_s + "/":
            return top_s
        gd = subprocess.run(["git", "-C", repo_dir, "rev-parse", "--git-dir", "--git-common-dir"],
                            capture_output=True, text=True, timeout=10)
        if gd.returncode != 0:
            return None
        parts = gd.stdout.split()
        if len(parts) >= 2:
            git_dir = os.path.realpath(os.path.join(repo_dir, parts[0]))
            common = os.path.realpath(os.path.join(repo_dir, parts[1]))
            if git_dir != common and "/worktrees/" in git_dir:
                return top_s
        return None
    except Exception:
        return None


def _block_worktree(verb: str, wt: str, cmd: str) -> int:
    _log(f"BLOCK-WORKTREE verb={verb} worktree={wt} cmd={cmd[:140]!r}")
    print(
        "\n".join([
            "",
            f"BLOCKED: git-reset-hard-guard: `git {verb}` inside a linked worktree",
            "",
            f"  Worktree: {wt}",
            "",
            "  The stash stack is shared with the main checkout and every other session's",
            "  worktree. A stash made here can be popped by someone else, and a stash left",
            "  behind becomes an orphan nobody owns (one sat unnoticed from 2026-05-28 to",
            "  2026-09-13). reset --hard and checkout -f have no place in a worktree either:",
            "  the tree is disposable, the commits are not.",
            "",
            "  If origin/main moved under you:",
            "    git rebase origin/main",
            "",
            "  If you must set work aside:",
            "    git add <specific files> && git commit -m 'wip: <what>'",
            "    (a commit on your own branch; squash or drop it before the PR)",
            "",
            "  git stash list / git stash show are read-only and always allowed.",
            "",
            "  Bypass only with a reason you would put in the commit message:",
            f"    {BYPASS}=1 <retry-command>",
            "",
            "  Signal: SIG-SUBAGENT-BRIEF-PROHIBITIONS-IGNORED-UNDER-DRIFT-2026-09-13",
            "",
        ]),
        file=sys.stderr,
    )
    return 2


def main() -> int:
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
    if not cmd.strip():
        return 0
    if re.search(r"\b" + BYPASS + r"=1\b", cmd):
        _log(f"BYPASS-inline cmd={cmd[:140]!r}")
        return 0

    cmd_stripped = _strip_heredocs(cmd)

    cwd = payload.get("cwd")

    # Linked-worktree rule: mutating stash is blocked outright; reset --hard and
    # checkout -f are blocked even on a clean tree.
    for m in re.finditer(_GIT_STASH, cmd_stripped, re.M):
        sub = (m.group("a3") or "").strip().split()
        if sub and sub[0] in _STASH_READONLY:
            continue
        for d in _repo_dirs(cmd_stripped, cwd, m):
            if os.path.isdir(d):
                wt = _linked_worktree(d)
                if wt:
                    return _block_worktree("stash " + (sub[0] if sub else "(push)"), wt, cmd)
                break

    hit, verb = None, None
    for m in re.finditer(_GIT_RESET_HARD, cmd_stripped, re.M):
        if re.search(r"(?:^|\s)--hard(?:\s|$|=)", m.group("a")):
            hit, verb = m, "reset --hard"
            break
    if hit is None:
        for m in re.finditer(_GIT_CHECKOUT_F, cmd_stripped, re.M):
            if re.search(r"(?:^|\s)(?:-f|--force)(?:\s|$)", m.group("a2")):
                hit, verb = m, "checkout --force"
                break
    if hit is None:
        return 0

    info = None
    for d in _repo_dirs(cmd_stripped, cwd, hit):
        if not os.path.isdir(d):
            continue
        wt = _linked_worktree(d)
        if wt:
            return _block_worktree(verb, wt, cmd)
        info = _dirty_tracked(d)
        if info is not None:
            break
    if info is None:
        return 0  # cannot resolve a repo → allow

    top, lines = info
    if not lines:
        return 0  # clean tree → the call destroys nothing → allow

    shown = "\n".join(f"      {ln}" for ln in lines[:12])
    more = f"\n      ... and {len(lines) - 12} more" if len(lines) > 12 else ""
    _log(f"BLOCK verb={verb} repo={top} dirty={len(lines)} cmd={cmd[:140]!r}")
    print(
        "\n".join([
            "",
            f"BLOCKED: git-reset-hard-guard: `git {verb}` on a DIRTY tree",
            "",
            f"  Repo: {top}",
            f"  {len(lines)} uncommitted tracked change(s) this call would DELETE:",
            shown + more,
            "",
            "  Unstaged changes have no git object. Once this runs they are gone:",
            "  `git fsck` has nothing, and reflog only covers commits.",
            "  This exact call destroyed work on 2026-07-23 (8 files, 6 repos) and",
            "  again on 2026-07-24 (5,440 bytes, recovered only from a transcript).",
            "",
            "  If you are realigning local main after a PR merged (the usual cause):",
            "    git reset --soft origin/main",
            "",
            "  If you genuinely want the remote's tree AND the local edits kept, commit",
            "  the edits first (a wip commit on a branch is recoverable; a stash is shared",
            "  with every other session and gets orphaned):",
            "    git add <specific files> && git commit -m 'wip: <what>' && git reset --hard origin/main",
            "",
            "  If the local edits belong to someone else's session, leave them alone:",
            "  a scheduled task should commit only its own artifacts.",
            "",
            "  Bypass only if you have looked at the diff and mean to discard it:",
            f"    {BYPASS}=1 <retry-command>",
            "",
            "  Signals: SIG-RESET-HARD-DESTROYED-UNCOMMITTED-WORK-2026-07-23 / -07-24",
            "",
        ]),
        file=sys.stderr,
    )
    return 2


if __name__ == "__main__":
    sys.exit(main())
