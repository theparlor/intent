#!/usr/bin/env python3
"""Test harness for the fixtures-path exemption in closure-discipline-signal-check.sh
(SIG-2026-07-19-fixtures-exemption-ruled). Runs the hook under a throwaway HOME so
the real audit log is untouched. Style/harness follows test_response_lint.py.

Ruling under test: a write is exempt ONLY when BOTH hold: (1) the target path
contains a fixtures directory segment (a path component named `fixtures`,
`__fixtures__`, or the `tests/fixtures` sequence), AND (2) the file body
carries an explicit inert-test-data marker line (case-insensitive:
"inert-test-data" / "inert fixture" / "deliberately-malformed test fixture").
Either alone still enforces. Exempted writes must log FIXTURE-EXEMPT with
path and session so exemption use stays observable.
"""
import json, os, subprocess, tempfile, sys

HOOK = "/Users/brien/Workspaces/Core/frameworks/intent/hooks/closure-discipline-signal-check.sh"
TMP = tempfile.mkdtemp(prefix="closure-fixture-test-")
FAKE_HOME = os.path.join(TMP, "home")
os.makedirs(os.path.join(FAKE_HOME, ".claude", "audit"), exist_ok=True)
AUDIT_LOG = os.path.join(FAKE_HOME, ".claude", "audit", "closure-discipline-signal-detections.log")

RESOLVED_NO_DOD = """---
title: Some signal
type: signal
status: resolved
created: 2026-07-19
---

# Body
No upstream_control_path or catch_mechanism fields here.
"""

RESOLVED_WITH_DOD = """---
title: Some signal
type: signal
status: resolved
created: 2026-07-19
upstream_control_path: hooks/closure-discipline-signal-check.sh
catch_mechanism: test_closure_fixture_exemption.py
---

# Body
Fully closed with DoD fields present.
"""

MARKER = "\n<!-- inert-test-data -->\n"

FIXTURES_PATH = "/repo/tests/fixtures/.intent/signals/SIG-fixture-test.md"
NON_FIXTURES_PATH = "/repo/.intent/signals/SIG-real-test.md"
SESSION_ID = "test-session-fixture-exempt"

def run(file_path, content, session_id=SESSION_ID, tool_name="Write"):
    hook_input = json.dumps({
        "session_id": session_id,
        "tool_name": tool_name,
        "tool_input": {"file_path": file_path, "content": content},
    })
    env = dict(os.environ); env["HOME"] = FAKE_HOME
    p = subprocess.run(["bash", HOOK], input=hook_input, env=env,
                       capture_output=True, text=True)
    return p.stdout.strip()

def audit_log_lines():
    if not os.path.exists(AUDIT_LOG):
        return []
    with open(AUDIT_LOG) as f:
        return [l for l in f.read().splitlines() if l.strip()]

def is_block(out):
    try:
        obj = json.loads(out)
        return obj.get("decision") == "block"
    except Exception:
        return False

results = []
def check(name, cond):
    results.append((name, cond))
    print(("PASS " if cond else "FAIL ") + name)

# T1: fixtures path + marker + resolved-without-DoD -> EXEMPT (no block),
# and the exemption is logged as FIXTURE-EXEMPT with path + session.
before = len(audit_log_lines())
out = run(FIXTURES_PATH, RESOLVED_NO_DOD + MARKER)
after_lines = audit_log_lines()
check("T1 fixtures+marker -> no block", out == "")
check("T1 fixtures+marker -> exactly one new log line", len(after_lines) == before + 1)
last_line = after_lines[-1] if after_lines else ""
check("T1 log line tagged FIXTURE-EXEMPT", "FIXTURE-EXEMPT" in last_line)
check("T1 log line carries the path", FIXTURES_PATH in last_line)
check("T1 log line carries the session", SESSION_ID in last_line)

# T2: same content, fixtures path but NO marker -> path alone does not exempt; blocks.
out = run(FIXTURES_PATH, RESOLVED_NO_DOD)
check("T2 fixtures-only (no marker) -> still blocks", is_block(out))

# T3: same content, marker present but NON-fixtures path -> marker alone does not
# exempt; blocks.
out = run(NON_FIXTURES_PATH, RESOLVED_NO_DOD + MARKER)
check("T3 marker-only (non-fixtures path) -> still blocks", is_block(out))

# T4: normal resolved-WITH-DoD write passes regardless of path or fixtures/marker
# status -- the exemption must never interfere with the pre-existing pass path.
out = run(NON_FIXTURES_PATH, RESOLVED_WITH_DOD)
check("T4 resolved+DoD, non-fixtures path -> no block", out == "")

out = run(FIXTURES_PATH, RESOLVED_WITH_DOD)
check("T4b resolved+DoD, fixtures path, no marker -> no block", out == "")

out = run(FIXTURES_PATH, RESOLVED_WITH_DOD + MARKER)
check("T4c resolved+DoD, fixtures path, WITH marker -> no block", out == "")

# T5: alternate marker phrasing ("inert fixture") and alternate fixtures-segment
# form (__fixtures__) both satisfy the exemption predicate independently.
ALT_FIXTURES_PATH = "/repo/__fixtures__/.intent/signals/SIG-alt-fixture-test.md"
out = run(ALT_FIXTURES_PATH, RESOLVED_NO_DOD + "\ninert fixture, not a real record\n")
check("T5 __fixtures__ segment + 'inert fixture' marker -> no block", out == "")

print()
passed = sum(1 for _, c in results if c)
total = len(results)
print("RESULT: %d/%d passed" % (passed, total))
sys.exit(0 if passed == total else 1)
