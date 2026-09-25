#!/usr/bin/env python3
"""Test harness for signal-recorder-silent-check.sh (WS-DDR-098 companion hook).

Regression under test: from 2026-05-26 to 2026-09-25 the hook's path lookup read as
(file_path or path or command.split()[1]) if command else None, so every Edit and
Write call resolved to None. Its telemetry held 30,953 rows, every one no-context/skip,
and it never evaluated a product. This harness pins the detection matrix so a silent
hook shows up as a failing test instead of four months of skips.

Builds throwaway product trees under a temp dir with a fake HOME, so the real
telemetry and audit logs are never touched.

Run: python3 tests/test_signal_recorder_silent_check.py
"""
import json, os, subprocess, sys, tempfile, time

HOOK = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "signal-recorder-silent-check.sh")
TMP = tempfile.mkdtemp(prefix="recorder-silent-test-")
FAKE_HOME = os.path.join(TMP, "home")
os.makedirs(FAKE_HOME, exist_ok=True)
TELEMETRY = os.path.join(FAKE_HOME, ".claude", "logs", "signal-recorder-silent.jsonl")


def make_product(name, declares, sig_age_days, parent=TMP):
    root = os.path.join(parent, name)
    os.makedirs(os.path.join(root, ".intent", "signals"))
    os.makedirs(os.path.join(root, "src"))
    body = "lambda_settings:\n  default: L2\n" if declares else "title: plain\n"
    open(os.path.join(root, ".intent", "INTENT.md"), "w").write(body)
    target = os.path.join(root, "src", "thing.py")
    open(target, "w").write("x = 1\n")
    if sig_age_days is not None:
        sig = os.path.join(root, ".intent", "signals", "SIG-TEST.md")
        open(sig, "w").write("---\nid: SIG-TEST\n---\n")
        past = time.time() - sig_age_days * 86400
        os.utime(sig, (past, past))
    return root, target


def run(tool_input, tool="Write"):
    env = dict(os.environ, HOME=FAKE_HOME)
    env.pop("SIGNAL_RECORDER_SILENT_BYPASSED", None)
    payload = json.dumps({"tool_name": tool, "tool_input": tool_input})
    before = open(TELEMETRY).read().count("\n") if os.path.exists(TELEMETRY) else 0
    p = subprocess.run(["bash", HOOK], input=payload, capture_output=True, text=True, env=env)
    rows = open(TELEMETRY).read().splitlines()[before:] if os.path.exists(TELEMETRY) else []
    last = json.loads(rows[-1]) if rows else {}
    return p.returncode, p.stderr, last


silent_root, silent_file = make_product("silent", declares=True, sig_age_days=60)
active_root, active_file = make_product("active", declares=True, sig_age_days=2)
plain_root, plain_file = make_product("plain", declares=False, sig_age_days=None)
eng_parent = os.path.join(TMP, "Work", "Consulting", "Engagements")
os.makedirs(eng_parent)
eng_root, eng_file = make_product("Client", declares=True, sig_age_days=60, parent=eng_parent)

CASES = [
    # (label, tool, tool_input, expected detection, expect warning on stderr)
    ("Write into a silent product (the 2026-09-25 regression)", "Write",
     {"file_path": silent_file, "content": "y"}, "silent-recorder", True),
    ("Edit into a silent product", "Edit",
     {"file_path": silent_file, "old_string": "x", "new_string": "y"}, "silent-recorder", True),
    ("Bash naming an absolute path in a silent product", "Bash",
     {"command": f"python3 -m pytest {silent_file} -q"}, "silent-recorder", True),
    ("Write into an active product", "Write",
     {"file_path": active_file, "content": "y"}, "recorder-active", False),
    ("Write into a product with no autonomy declaration", "Write",
     {"file_path": plain_file, "content": "y"}, "no-lambda-declaration", False),
    ("Write into an engagement path", "Write",
     {"file_path": eng_file, "content": "y"}, "engagement-exempt", False),
    ("Bash with no path at all", "Bash",
     {"command": "ls"}, "no-context", False),
]

failures = 0
for label, tool, ti, want, warn in CASES:
    rc, err, row = run(ti, tool)
    got = row.get("detection")
    warned = "WS-DDR-098" in err
    ok = rc == 0 and got == want and warned == warn
    failures += 0 if ok else 1
    print(f"{'PASS' if ok else 'FAIL'}  {label}: detection={got} warned={warned} rc={rc}")

print(f"\n{len(CASES) - failures} passed, {failures} failed")
sys.exit(1 if failures else 0)
