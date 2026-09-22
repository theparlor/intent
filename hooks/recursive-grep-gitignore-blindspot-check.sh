#!/usr/bin/env python3
# recursive-grep-gitignore-blindspot-check.sh
#
# PreToolUse hook (matcher: Bash). ADVISORY ONLY: it never blocks and always
# exits 0. When a recursive grep (or rg) is about to run from a directory whose
# git repo gitignores nested git repos, it hands Claude one paragraph of
# additionalContext saying which trees the search will silently skip.
#
# Why this exists:
# - `grep` inside Claude Code Bash sessions is not /usr/bin/grep. The harness
#   defines a shell function that execs the claude binary as ugrep with
#   `-G --ignore-files --hidden -I`. `--ignore-files` honors .gitignore.
# - The Workspaces root repo gitignores its nested repos: 42 directories under
#   Core/products/ (every product and every product site), every top-level
#   directory under Work/ and Home/ (measured 2026-09-21). A recursive grep from
#   /Users/brien/Workspaces therefore searches governance-tracked files only.
# - 2026-09-21: a sweep for copy2/copytree call sites under tests/ returned zero
#   hits three times (with -r, then -R) while a targeted grep on a known file hit.
#   find plus xargs reached 678 test files and 23 call sites. An empty recursive
#   grep read as a clean sweep; it was a partial listing, the exact failure the
#   absence-claims rule forbids.
#   SIG-HARNESS-GREP-SKIPS-GITIGNORED-TREES-2026-09-21.
# - The wrapper is present in every Claude Code session and absent from a plain
#   terminal, so nothing announces the difference. This hook sits between the
#   intent and the call and announces it.
#
# Scope (advisory, fail silent: anything unresolvable means no message):
# - Fires on `grep`/`egrep`/`fgrep` in command position carrying a recursive
#   flag (-r, -R, --recursive, --dereference-recursive, or a short cluster that
#   contains r or R), and on `rg` (recursive by default).
# - Exempt: `command grep`, `\grep`, an absolute-path grep (the wrapper is a
#   function named grep, so these reach the real binary); `--no-ignore-files`
#   on grep; `--no-ignore`, `--no-ignore-vcs`, `--no-ignore-files`, `-u`, `-uu`,
#   `-uuu`, `--unrestricted` on rg; grep after `xargs` (explicit files, no
#   recursion). If the claude binary the wrapper execs is not present, the
#   wrapper falls back to plain grep, and grep is exempt too (rg is not).
# - Search roots: explicit directory arguments, else the effective cwd (a
#   leading `cd <path> &&` is honored). Each root resolves to its own git
#   toplevel; the ignored listing comes from `git ls-files --others --ignored
#   --exclude-standard --directory` (27 ms on the Workspaces root). Only ignored
#   directories that are git repos themselves count: those are whole trees, not
#   build junk.
# - Heredoc bodies are stripped before matching (a commit message that mentions
#   `grep -r` is data, not a command).
# - Throttle: one advisory per (session, repo toplevel) per 6 hours, so a session
#   that has been told once is not told on every grep. State lives in
#   ~/.claude/state/recursive-grep-blindspot-seen.json.
#
# Grep tool (matcher: Grep, same script, added 2026-09-21): the tool runs the
#   embedded ripgrep with --hidden and never passes --no-ignore, and no parameter
#   can add one (measured by replaying its argument set: from the Workspaces
#   root a string that exists only in a gitignored product file returns
#   nothing; with path scoped into that repo it is found). The advisory reads
#   tool_input.path (default cwd) and names the remedy: scope the path to the
#   nested repo, one call per repo. Same throttle, same bypass.
#
# Bypass: RECURSIVE_GREP_BLINDSPOT_BYPASSED=1 (env or inline prefix; logged).
# Output: JSON on stdout with hookSpecificOutput.additionalContext, exit 0.
#   Plain stdout on exit 0 reaches nobody for PreToolUse; additionalContext is
#   the only non-blocking path to the model.

import glob
import json
import os
import re
import shlex
import subprocess
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

BYPASS = "RECURSIVE_GREP_BLINDSPOT_BYPASSED"
THROTTLE_SECONDS = 6 * 3600
SIGNAL = "SIG-HARNESS-GREP-SKIPS-GITIGNORED-TREES-2026-09-21"


def _log(msg: str) -> None:
    try:
        d = Path.home() / ".claude" / "logs"
        d.mkdir(parents=True, exist_ok=True)
        ts = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
        with (d / "recursive-grep-blindspot.log").open("a") as fh:
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


def _wrapper_active() -> bool:
    """Mirror the harness function: it execs $CLAUDE_CODE_EXECPATH, else
    ~/.local/bin/claude, and falls back to plain grep when neither is executable."""
    cand = os.environ.get("CLAUDE_CODE_EXECPATH") or ""
    if cand and os.access(cand, os.X_OK):
        return True
    fallback = Path.home() / ".local" / "bin" / "claude"
    return os.access(str(fallback), os.X_OK)


_PREFIX = (
    r"(?:(?:sudo|env|exec|nohup|time|timeout|nice|stdbuf|caffeinate)\s+"
    r"(?:-\S+\s+)*(?:\d+[smh]?\s+)?"
    r"|[A-Za-z_][A-Za-z0-9_]*=\S*\s+)*"
)
_INVOKE = re.compile(
    r"(?:^|[;&|({`\n])\s*" + _PREFIX +
    r"(?P<real>command\s+|\\)?(?P<path>(?:/[\w.+\-]+)+/)?"
    r"(?P<name>grep|egrep|fgrep|rg)\b(?P<args>[^;&|\n]*)",
    re.M,
)
_CD = re.compile(r"(?:^|[;&|\n])\s*(?:cd|pushd)\s+([^\s;&|]+)", re.M)

# short options that take a separate argument, per binary
_ARG_SHORT = {
    "grep": {"-e", "-f", "-A", "-B", "-C", "-m", "-d", "-D", "-N", "-K", "-J"},
    "rg": {"-e", "-f", "-A", "-B", "-C", "-m", "-g", "-t", "-T", "-j", "-M", "-E", "-r", "-d"},
}
_ARG_LONG = {
    "--regexp", "--file", "--include", "--exclude", "--exclude-dir", "--include-dir",
    "--max-count", "--after-context", "--before-context", "--context", "--type",
    "--type-not", "--glob", "--iglob", "--max-depth", "--color", "--colour", "--sort",
    "--sortr", "--pre", "--replace", "--encoding", "--threads", "--max-columns",
    "--ignore-file", "--exclude-from", "--include-from", "--filter", "--config",
}
_RG_EXEMPT = {"--no-ignore", "--no-ignore-vcs", "--no-ignore-files", "--no-ignore-global",
              "--unrestricted", "-u", "-uu", "-uuu"}


def _parse(name: str, args: str):
    """Return (recursive, exempt, paths) for one invocation."""
    try:
        toks = shlex.split(args, posix=True)
    except ValueError:
        toks = args.split()
    binkey = "rg" if name == "rg" else "grep"
    recursive = name == "rg"
    exempt = False
    pattern_given = False
    positionals = []
    i = 0
    while i < len(toks):
        t = toks[i]
        if t == "--":
            positionals.extend(toks[i + 1:])
            break
        if t.startswith("--"):
            base = t.split("=", 1)[0]
            if binkey == "grep" and base == "--no-ignore-files":
                exempt = True
            if binkey == "rg" and base in _RG_EXEMPT:
                exempt = True
            if base in ("--recursive", "--dereference-recursive"):
                recursive = True
            if base in ("--regexp", "--file"):
                pattern_given = True
            if base in _ARG_LONG and "=" not in t:
                i += 1
            i += 1
            continue
        if t.startswith("-") and len(t) > 1:
            if binkey == "rg" and t in _RG_EXEMPT:
                exempt = True
            if t in _ARG_SHORT[binkey]:
                if t in ("-e", "-f"):
                    pattern_given = True
                i += 2
                continue
            if binkey == "grep" and re.match(r"^-[A-Za-z]*[rR][A-Za-z]*$", t):
                recursive = True
            # a cluster ending in an arg-taking letter, e.g. -rne PATTERN
            if t[-1] in {s[1] for s in _ARG_SHORT[binkey]} and len(t) > 2:
                if t[-1] in ("e", "f"):
                    pattern_given = True
                i += 2
                continue
            i += 1
            continue
        positionals.append(t)
        i += 1
    if not pattern_given and positionals:
        positionals = positionals[1:]
    return recursive, exempt, positionals


def _effective_cwd(cmd: str, upto: int, cwd: str) -> str:
    base = os.path.expanduser(cwd or os.getcwd())
    for m in _CD.finditer(cmd):
        if m.start() >= upto:
            break
        target = os.path.expanduser(m.group(1).strip("\"'"))
        base = target if os.path.isabs(target) else os.path.join(base, target)
    return base


def _roots(paths, cwd: str):
    out = []
    if not paths:
        out.append(cwd)
    for p in paths:
        p = os.path.expanduser(p)
        full = p if os.path.isabs(p) else os.path.join(cwd, p)
        matches = glob.glob(full) if any(ch in full for ch in "*?[") else [full]
        out.extend(m for m in matches if os.path.isdir(m))
    seen, uniq = set(), []
    for r in out:
        rp = os.path.realpath(r)
        if rp not in seen:
            seen.add(rp)
            uniq.append(rp)
    return uniq


def _hidden_repos(root: str):
    """(toplevel, [ignored nested repos under root, repo-relative]) or None."""
    try:
        top = subprocess.run(["git", "-C", root, "rev-parse", "--show-toplevel"],
                             capture_output=True, text=True, timeout=10)
        if top.returncode != 0:
            return None
        top_s = os.path.realpath(top.stdout.strip())
        ls = subprocess.run(["git", "-C", top_s, "ls-files", "--others", "--ignored",
                             "--exclude-standard", "--directory"],
                            capture_output=True, text=True, timeout=20)
        if ls.returncode != 0:
            return None
        nested = []
        for line in ls.stdout.splitlines():
            if not line.endswith("/"):
                continue
            abs_dir = os.path.realpath(os.path.join(top_s, line))
            if abs_dir != root and not abs_dir.startswith(root + os.sep):
                continue
            if os.path.exists(os.path.join(abs_dir, ".git")):
                nested.append(line.rstrip("/"))
        return top_s, sorted(nested)
    except Exception:
        return None


def _throttled(session: str, top: str) -> bool:
    try:
        d = Path.home() / ".claude" / "state"
        d.mkdir(parents=True, exist_ok=True)
        f = d / "recursive-grep-blindspot-seen.json"
        now = time.time()
        try:
            state = json.loads(f.read_text())
        except Exception:
            state = {}
        state = {k: v for k, v in state.items() if now - float(v) < THROTTLE_SECONDS}
        key = f"{session}|{top}"
        hit = key in state
        state[key] = now
        f.write_text(json.dumps(state))
        return hit
    except Exception:
        return False


def _advise(name: str, root: str, top: str, nested: list) -> None:
    shown = ", ".join(nested[:6]) + (f", and {len(nested) - 6} more" if len(nested) > 6 else "")
    if name == "Grep":
        how = ("The Grep tool runs the embedded ripgrep without --no-ignore and no parameter "
               "can add it. Scope `path` to the nested repo itself, one call per repo, "
               f"or search from Bash with `find {root} -type f -name '<glob>' | xargs grep -n <pattern>`")
    elif name == "rg":
        how = ("Note that rg honors .gitignore by default. Re-run with `rg --no-ignore` (or -uu), "
               f"or `find {root} -type f -name '<glob>' | xargs grep -n <pattern>`")
    else:
        how = ("This grep runs through the Claude Code ugrep wrapper with --ignore-files. "
               f"Re-run with `command grep -r ...` or `find {root} -type f -name '<glob>' "
               "| xargs grep -n <pattern>`")
    msg = (
        f"ADVISORY (recursive-grep-blindspot, not a block): beneath {root} the repo {top} "
        f"gitignores {len(nested)} nested git repo(s) this search will skip silently: {shown}. "
        f"A zero-hit result here is a partial listing, not an absence. {how}, and prove reach "
        "with a control grep on one file known to match before making any absence claim. "
        f"Fires once per session per repo. Bypass: {BYPASS}=1. Signal: {SIGNAL}."
    )
    print(json.dumps({"hookSpecificOutput": {"hookEventName": "PreToolUse",
                                             "additionalContext": msg}}))


def _grep_tool(payload: dict) -> int:
    """The Grep tool: one root, the `path` input, defaulting to cwd. A file path never
    recurses, so it is silent."""
    inp = payload.get("tool_input") or {}
    cwd = payload.get("cwd") or os.getcwd()
    session = payload.get("session_id") or os.environ.get("CLAUDE_SESSION_ID") or "unknown"
    raw_path = inp.get("path") or ""
    raw_path = os.path.expanduser(raw_path)
    root = raw_path if os.path.isabs(raw_path) else os.path.join(cwd, raw_path)
    root = os.path.realpath(root)
    if not os.path.isdir(root):
        return 0
    info = _hidden_repos(root)
    if not info:
        return 0
    top, nested = info
    if not nested:
        return 0
    if _throttled(session, top):
        _log(f"SUPPRESSED tool=Grep session={session} top={top} root={root} nested={len(nested)}")
        return 0
    _log(f"ADVISE tool=Grep session={session} top={top} root={root} nested={len(nested)} "
         f"pattern={str(inp.get('pattern'))[:80]!r}")
    _advise("Grep", root, top, nested)
    return 0


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
    tool = payload.get("tool_name") or ""
    if tool == "Grep":
        return _grep_tool(payload)
    if tool != "Bash":
        return 0
    cmd = ((payload.get("tool_input") or {}).get("command") or "")
    if not cmd.strip():
        return 0
    if re.search(r"\b" + BYPASS + r"=1\b", cmd):
        _log(f"BYPASS-inline cmd={cmd[:140]!r}")
        return 0

    stripped = _strip_heredocs(cmd)
    cwd = payload.get("cwd") or os.getcwd()
    session = payload.get("session_id") or os.environ.get("CLAUDE_SESSION_ID") or "unknown"
    wrapper = _wrapper_active()

    for m in _INVOKE.finditer(stripped):
        name = m.group("name")
        if name != "rg":
            if m.group("real") or m.group("path") or not wrapper:
                continue
        recursive, exempt, paths = _parse(name, m.group("args"))
        if not recursive or exempt:
            continue
        eff = _effective_cwd(stripped, m.start(), cwd)
        for root in _roots(paths, eff):
            info = _hidden_repos(root)
            if not info:
                continue
            top, nested = info
            if not nested:
                continue
            if _throttled(session, top):
                _log(f"SUPPRESSED session={session} top={top} root={root} nested={len(nested)}")
                return 0
            _log(f"ADVISE session={session} top={top} root={root} nested={len(nested)} "
                 f"cmd={cmd[:140]!r}")
            _advise(name, root, top, nested)
            return 0
    return 0


if __name__ == "__main__":
    sys.exit(main())
