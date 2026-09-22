#!/usr/bin/env python3
"""Test harness for recursive-grep-gitignore-blindspot-check.sh.

Builds a throwaway outer git repo whose .gitignore hides a nested git repo and a
.venv, plus a tracked plain/ directory, and asserts the advise/silent matrix. The
load-bearing properties: a recursive grep or rg whose root covers a hidden nested repo
gets one advisory paragraph in hookSpecificOutput.additionalContext; every other shape
(non-recursive, the real binary, an exempting flag, a root with nothing hidden, a
heredoc mention, a non-repo, a bypass) is silent; the exit code is 0 in every case;
and the second call in the same session for the same repo is throttled.

Run: python3 tests/test_recursive_grep_blindspot.py
"""
import json, os, subprocess, sys, tempfile

HOOK = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..",
                    "recursive-grep-gitignore-blindspot-check.sh")
TMP = tempfile.mkdtemp(prefix="grep-blindspot-test-")
OUTER = os.path.join(TMP, "outer")
NESTED = os.path.join(OUTER, "products", "nested")
PLAIN = os.path.join(OUTER, "plain")
NOREPO = os.path.join(TMP, "norepo")
FAKE_HOME = os.path.join(TMP, "home")
FAKE_CLAUDE = os.path.join(TMP, "claude-bin")
os.makedirs(FAKE_HOME)
os.makedirs(NOREPO)
open(os.path.join(NOREPO, "f.txt"), "w").write("x\n")
open(FAKE_CLAUDE, "w").write("#!/bin/sh\nexit 0\n")
os.chmod(FAKE_CLAUDE, 0o755)


def sh(*args, cwd=None):
    subprocess.run(args, cwd=cwd, check=True, capture_output=True)


def make_repo(path):
    os.makedirs(path, exist_ok=True)
    sh("git", "init", "-q", cwd=path)
    sh("git", "config", "user.email", "t@example.com", cwd=path)
    sh("git", "config", "user.name", "t", cwd=path)
    open(os.path.join(path, "f.txt"), "w").write("needle\n")
    sh("git", "add", "f.txt", cwd=path)
    sh("git", "commit", "-qm", "base", cwd=path)


make_repo(OUTER)
os.makedirs(PLAIN)
open(os.path.join(PLAIN, "p.txt"), "w").write("needle\n")
open(os.path.join(OUTER, ".gitignore"), "w").write("/products/nested/\n.venv/\n")
sh("git", "add", ".gitignore", "plain/p.txt", cwd=OUTER)
sh("git", "commit", "-qm", "ignore nested", cwd=OUTER)
make_repo(NESTED)
os.makedirs(os.path.join(OUTER, ".venv", "lib"))
open(os.path.join(OUTER, ".venv", "lib", "x.py"), "w").write("needle\n")


def run(cmd, cwd, tool="Bash", session="s1", wrapper=True, env_bypass=False):
    tool_input = {"pattern": "needle", "path": cmd} if tool == "Grep" else {"command": cmd}
    if tool == "Grep" and cmd is None:
        tool_input = {"pattern": "needle"}
    payload = json.dumps({"tool_name": tool, "cwd": cwd, "session_id": session,
                          "tool_input": tool_input})
    env = dict(os.environ)
    env["HOME"] = FAKE_HOME
    env["CLAUDE_CODE_EXECPATH"] = FAKE_CLAUDE if wrapper else os.path.join(TMP, "absent")
    if env_bypass:
        env["RECURSIVE_GREP_BLINDSPOT_BYPASSED"] = "1"
    else:
        env.pop("RECURSIVE_GREP_BLINDSPOT_BYPASSED", None)
    p = subprocess.run([sys.executable, HOOK], input=payload, env=env,
                       capture_output=True, text=True)
    ctx = None
    if p.stdout.strip():
        ctx = json.loads(p.stdout)["hookSpecificOutput"]["additionalContext"]
    return p.returncode, ctx, p.stderr


ADVISE, SILENT = True, False
# every case runs under its own session id so the throttle never crosses cases
CASES = [
    ("grep -rn from outer root",          "grep -rn needle .",                        OUTER,  ADVISE),
    ("grep -r no path (implicit .)",      "grep -r needle",                           OUTER,  ADVISE),
    ("grep -R cluster -RlE",              "grep -RlE 'nee.le' .",                     OUTER,  ADVISE),
    ("grep --recursive long flag",        "grep --recursive needle .",                OUTER,  ADVISE),
    ("grep -r -e pattern form",           "grep -r -e needle .",                      OUTER,  ADVISE),
    ("grep -rne cluster with arg",        "grep -rne needle .",                       OUTER,  ADVISE),
    ("grep -r with --include=",           "grep -rn --include='*.txt' needle .",      OUTER,  ADVISE),
    ("grep -r absolute outer path",       f"grep -rn needle {OUTER}",                 TMP,    ADVISE),
    ("cd outer && grep -r",               f"cd {OUTER} && grep -rl needle .",         TMP,    ADVISE),
    ("grep -r chained after &&",          "echo x && grep -rn needle .",              OUTER,  ADVISE),
    ("grep -r on products/ subtree",      "grep -rn needle products/",                OUTER,  ADVISE),
    ("rg default from outer",             "rg needle",                                OUTER,  ADVISE),
    ("rg with path",                      "rg -n needle .",                           OUTER,  ADVISE),
    ("rg without wrapper still advises",  "rg needle",                                OUTER,  "rg-nowrap"),
    # silent: nothing hidden beneath the root
    ("grep -r on plain/ only",            "grep -rn needle plain/",                   OUTER,  SILENT),
    ("grep -r inside the nested repo",    "grep -rn needle .",                        NESTED, SILENT),
    ("grep -r inside .venv (not a repo)", "grep -rn needle .venv",                    OUTER,  SILENT),
    ("grep -r in a non-repo dir",         "grep -rn needle .",                        NOREPO, SILENT),
    # silent: not recursive, or explicit files
    ("grep -n on a file",                 "grep -n needle f.txt",                     OUTER,  SILENT),
    ("find | xargs grep",                 "find . -name '*.txt' | xargs grep -n needle", OUTER, SILENT),
    ("grep -n pattern contains r",        "grep -n 'error' f.txt",                    OUTER,  SILENT),
    # silent: reaches the real binary or disables ignore handling
    ("command grep -r",                   "command grep -rn needle .",                OUTER,  SILENT),
    ("backslash grep -r",                 "\\grep -rn needle .",                      OUTER,  SILENT),
    ("absolute /usr/bin/grep -r",         "/usr/bin/grep -rn needle .",               OUTER,  SILENT),
    ("grep -r --no-ignore-files",         "grep -rn --no-ignore-files needle .",      OUTER,  SILENT),
    ("rg --no-ignore",                    "rg --no-ignore needle",                    OUTER,  SILENT),
    ("rg -uu",                            "rg -uu needle",                            OUTER,  SILENT),
    ("grep -r without wrapper present",   "grep -rn needle .",                        OUTER,  "grep-nowrap"),
    # silent: data, not a command
    ("heredoc body mentions grep -r",
     "git commit -F - <<EOF\nnote: grep -rn needle . found nothing\nEOF",             OUTER,  SILENT),
    ("echo mentions grep -r",             "echo 'run grep -r needle .'",              OUTER,  SILENT),
    # silent: bypass and non-Bash
    ("inline bypass",                     "RECURSIVE_GREP_BLINDSPOT_BYPASSED=1 grep -rn needle .", OUTER, SILENT),
    ("non-Bash tool",                     "grep -rn needle .",                        OUTER,  "non-bash"),
]

fails = []
for n, (desc, cmd, cwd, want) in enumerate(CASES):
    tool, wrapper = "Bash", True
    if want == "non-bash":
        tool, want = "Write", SILENT
    elif want == "grep-nowrap":
        wrapper, want = False, SILENT
    elif want == "rg-nowrap":
        wrapper, want = False, ADVISE
    rc, ctx, err = run(cmd, cwd, tool=tool, session=f"case-{n}", wrapper=wrapper)
    got = ctx is not None
    ok = rc == 0 and got == want and not err.strip()
    if ok and got:
        ok = ("products/nested" in ctx and "partial listing" in ctx
              and "SIG-HARNESS-GREP-SKIPS-GITIGNORED-TREES-2026-09-21" in ctx
              and ".venv" not in ctx)
        if not ok:
            fails.append(f"{desc}: advisory text incomplete: {ctx!r}")
    elif not ok:
        fails.append(f"{desc}: want advise={want} got advise={got} rc={rc} stderr={err.strip()!r}")
    print(f"  {'PASS' if ok else 'FAIL'}  {desc:<36} rc={rc} advise={got}")

# env-var bypass
rc, ctx, _ = run("grep -rn needle .", OUTER, session="env-bypass", env_bypass=True)
ok = rc == 0 and ctx is None
print(f"  {'PASS' if ok else 'FAIL'}  {'env bypass':<36} rc={rc} advise={ctx is not None}")
if not ok:
    fails.append("env bypass: expected silence")

# throttle: same session, same repo, second call is silent; a new session is told again
rc1, c1, _ = run("grep -rn needle .", OUTER, session="throttle")
rc2, c2, _ = run("grep -rl needle plain/ .", OUTER, session="throttle")
rc3, c3, _ = run("grep -rn needle .", OUTER, session="throttle-other")
ok = (c1 is not None) and (c2 is None) and (c3 is not None) and rc1 == rc2 == rc3 == 0
print(f"  {'PASS' if ok else 'FAIL'}  {'throttle once per session per repo':<36} "
      f"first={c1 is not None} second={c2 is not None} other={c3 is not None}")
if not ok:
    fails.append("throttle: want advise,silent,advise")

# the Grep tool: path input, default cwd; a file path or a clean root is silent
GREP_CASES = [
    ("Grep path=outer root",            OUTER,                         OUTER,  ADVISE),
    ("Grep no path (cwd outer)",        None,                          OUTER,  ADVISE),
    ("Grep relative path products/",    "products",                    OUTER,  ADVISE),
    ("Grep path=plain/ only",           PLAIN,                         OUTER,  SILENT),
    ("Grep path inside nested repo",    NESTED,                        OUTER,  SILENT),
    ("Grep path is a file",             os.path.join(OUTER, "f.txt"),  OUTER,  SILENT),
    ("Grep path in a non-repo dir",     NOREPO,                        OUTER,  SILENT),
    ("Grep path does not exist",        os.path.join(TMP, "missing"),  OUTER,  SILENT),
]
for n, (desc, path, cwd, want) in enumerate(GREP_CASES):
    rc, ctx, err = run(path, cwd, tool="Grep", session=f"grep-{n}")
    got = ctx is not None
    ok = rc == 0 and got == want and not err.strip()
    if ok and got:
        ok = "products/nested" in ctx and "one call per repo" in ctx and ".venv" not in ctx
        if not ok:
            fails.append(f"{desc}: advisory text incomplete: {ctx!r}")
    elif not ok:
        fails.append(f"{desc}: want advise={want} got advise={got} rc={rc} stderr={err.strip()!r}")
    print(f"  {'PASS' if ok else 'FAIL'}  {desc:<36} rc={rc} advise={got}")

# Grep and Bash share the throttle for the same session and repo
rc1, c1, _ = run("grep -rn needle .", OUTER, session="shared")
rc2, c2, _ = run(OUTER, OUTER, tool="Grep", session="shared")
ok = c1 is not None and c2 is None and rc1 == rc2 == 0
print(f"  {'PASS' if ok else 'FAIL'}  {'Grep shares the Bash throttle':<36} first={c1 is not None} second={c2 is not None}")
if not ok:
    fails.append("shared throttle: want advise then silent")

# the advisory names the wrapper for grep and --no-ignore for rg
rc, cg, _ = run("grep -rn needle .", OUTER, session="text-grep")
rc, cr, _ = run("rg needle", OUTER, session="text-rg")
ok = cg and "command grep -r" in cg and cr and "--no-ignore" in cr
print(f"  {'PASS' if ok else 'FAIL'}  {'remedy text matches the binary':<36}")
if not ok:
    fails.append("remedy text: grep must cite command grep, rg must cite --no-ignore")

# the hook never mutates the repos it inspects
clean = all(not subprocess.run(["git", "-C", r, "status", "--porcelain"],
                               capture_output=True, text=True).stdout.strip()
            for r in (OUTER, NESTED))
print(f"  {'PASS' if clean else 'FAIL'}  {'hook did not mutate the repos':<36}")
if not clean:
    fails.append("hook mutated a test repo")

print()
if fails:
    print(f"FAILED ({len(fails)}):")
    for f in fails:
        print("  -", f)
    sys.exit(1)
print(f"All {len(CASES) + len(GREP_CASES) + 5} cases passed.")
