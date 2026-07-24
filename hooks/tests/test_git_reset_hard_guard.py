#!/usr/bin/env python3
"""Test harness for git-reset-hard-dirty-tree-block.sh.

Builds throwaway git repos in a temp dir (never touches a real one) and asserts the
block/allow matrix. The load-bearing property under test: a DIRTY tree blocks, a CLEAN
tree passes, and every non-destructive lookalike (reset --soft, a heredoc commit message
that mentions the phrase, a grep for it) passes untouched.

Run: python3 tests/test_git_reset_hard_guard.py
"""
import json, os, subprocess, sys, tempfile

HOOK = "/Users/brien/Workspaces/Core/frameworks/intent/hooks/git-reset-hard-dirty-tree-block.sh"
TMP = tempfile.mkdtemp(prefix="reset-guard-test-")
DIRTY = os.path.join(TMP, "dirty")
CLEAN = os.path.join(TMP, "clean")
FAKE_HOME = os.path.join(TMP, "home")
os.makedirs(FAKE_HOME, exist_ok=True)


def sh(*args, cwd=None):
    subprocess.run(args, cwd=cwd, check=True, capture_output=True)


def make_repo(path, dirty):
    os.makedirs(path)
    sh("git", "init", "-q", cwd=path)
    sh("git", "config", "user.email", "t@example.com", cwd=path)
    sh("git", "config", "user.name", "t", cwd=path)
    open(os.path.join(path, "f.txt"), "w").write("base\n")
    sh("git", "add", "f.txt", cwd=path)
    sh("git", "commit", "-qm", "base", cwd=path)
    if dirty:
        open(os.path.join(path, "f.txt"), "w").write("uncommitted work\n")


def run(cmd, cwd, tool="Bash", env_bypass=False):
    payload = json.dumps({"tool_name": tool, "cwd": cwd, "tool_input": {"command": cmd}})
    env = dict(os.environ)
    env["HOME"] = FAKE_HOME
    if env_bypass:
        env["GIT_RESET_HARD_GUARD_BYPASSED"] = "1"
    else:
        env.pop("GIT_RESET_HARD_GUARD_BYPASSED", None)
    p = subprocess.run([sys.executable, HOOK], input=payload, env=env,
                       capture_output=True, text=True)
    return p.returncode


make_repo(DIRTY, dirty=True)
make_repo(CLEAN, dirty=False)

BLOCK, ALLOW = 2, 0
CASES = [
    ("dirty + reset --hard",            "git reset --hard origin/main",              DIRTY, BLOCK),
    ("dirty + reset --hard HEAD~1",     "git reset --hard HEAD~1",                   DIRTY, BLOCK),
    ("dirty + checkout -f",             "git checkout -f main",                      DIRTY, BLOCK),
    ("dirty + checkout --force",        "git checkout --force main",                 DIRTY, BLOCK),
    ("dirty + cd <repo> && reset",      f"cd {DIRTY} && git reset --hard origin/main", TMP,  BLOCK),
    ("dirty + git -C <repo> reset",     f"git -C {DIRTY} reset --hard origin/main",  TMP,   BLOCK),
    ("dirty + chained after &&",        "git fetch && git reset --hard origin/main", DIRTY, BLOCK),
    # allow: the tree is clean, so the call destroys nothing
    ("clean + reset --hard",            "git reset --hard origin/main",              CLEAN, ALLOW),
    ("clean + checkout -f",             "git checkout -f main",                      CLEAN, ALLOW),
    # allow: non-destructive verbs
    ("dirty + reset --soft",            "git reset --soft origin/main",              DIRTY, ALLOW),
    ("dirty + reset --mixed",           "git reset --mixed origin/main",             DIRTY, ALLOW),
    ("dirty + bare reset",              "git reset",                                 DIRTY, ALLOW),
    ("dirty + plain checkout",          "git checkout main",                         DIRTY, ALLOW),
    # allow: the phrase appears as DATA, not as a command
    ("heredoc body mentions phrase",
     "git commit -F - <<EOF\nnote: never git reset --hard on a dirty tree\nEOF",      DIRTY, ALLOW),
    ("grep for the phrase",             'grep -rn "git reset --hard" docs/',          DIRTY, ALLOW),
    ("echo the phrase",                 'echo "git reset --hard is dangerous"',       DIRTY, ALLOW),
    # allow: bypass + non-Bash + unresolvable
    ("inline bypass",
     "GIT_RESET_HARD_GUARD_BYPASSED=1 git reset --hard origin/main",                  DIRTY, ALLOW),
    ("non-Bash tool",                   "git reset --hard origin/main",               DIRTY, ALLOW),
]

fails = []
for desc, cmd, cwd, want in CASES:
    tool = "Write" if desc == "non-Bash tool" else "Bash"
    got = run(cmd, cwd, tool=tool)
    ok = got == want
    if not ok:
        fails.append(f"{desc}: want rc={want} got rc={got}")
    print(f"  {'PASS' if ok else 'FAIL'}  {desc:<32} rc={got}")

# env-var bypass on an otherwise-blocking case
got = run("git reset --hard origin/main", DIRTY, env_bypass=True)
print(f"  {'PASS' if got == ALLOW else 'FAIL'}  {'env bypass':<32} rc={got}")
if got != ALLOW:
    fails.append(f"env bypass: want rc={ALLOW} got rc={got}")

# the dirty repo must still be dirty: the hook must never mutate a repo
still = subprocess.run(["git", "-C", DIRTY, "status", "--porcelain"],
                       capture_output=True, text=True).stdout.strip()
print(f"  {'PASS' if still else 'FAIL'}  {'hook did not mutate the repo':<32} {still!r}")
if not still:
    fails.append("hook mutated the test repo")

print()
if fails:
    print(f"FAILED ({len(fails)}):")
    for f in fails:
        print("  -", f)
    sys.exit(1)
print(f"All {len(CASES) + 2} cases passed.")
