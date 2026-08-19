#!/usr/bin/env python3
"""Test harness for account-connector-fabric-check.sh. Runs the hook under a
throwaway HOME so the real ~/.claude.json and audit logs are untouched.

Contract under test (SIG-DISPATCH-SESSION-NO-ACCOUNT-CONNECTORS-2026-08-19):
- SessionStart hook. stdin = JSON {session_id, transcript_path, cwd,
  hook_event_name, source}. Always exit 0 (context injector, never a gate).
- Expectation source: ~/.claude.json claudeAiMcpEverConnected (list of
  connector display names). Non-empty -> emit the roster-check directive.
- Empty, absent, or malformed expectation -> silent (false-alarm lever 2).
- ACCOUNT_CONNECTOR_FABRIC_BYPASSED=1 -> silent (false-alarm lever 1).
- Garbage stdin -> fail open, directive still emitted when expectation holds.
- Every run appends one audit line to
  ~/.claude/audit/account-connector-fabric-checks.log under the active HOME.

The hook path resolves relative to this file so the harness tests the
checkout it lives in (worktree-safe), not a hardcoded main-checkout path.
"""
import json
import os
import subprocess
import sys
import tempfile

HOOK = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..", "account-connector-fabric-check.sh")
)

STDIN = json.dumps(
    {
        "session_id": "test-session-0001",
        "transcript_path": "/tmp/none.jsonl",
        "cwd": "/tmp",
        "hook_event_name": "SessionStart",
        "source": "startup",
    }
)

EVER_CONNECTED = [
    "claude.ai Gmail",
    "claude.ai Google Calendar",
    "claude.ai Granola",
    "claude.ai Slack",
    "claude.ai Atlassian",
    "claude.ai Harvest",
    "claude.ai Google Drive",
    "claude.ai Era Context",
]


def run(home_payload, stdin=STDIN, env_extra=None):
    """Run the hook with a fresh throwaway HOME. Returns (rc, out, audit)."""
    tmp = tempfile.mkdtemp(prefix="fabric-check-test-")
    home = os.path.join(tmp, "home")
    os.makedirs(home, exist_ok=True)
    if home_payload is not None:
        with open(os.path.join(home, ".claude.json"), "w") as fh:
            fh.write(home_payload)
    env = dict(os.environ)
    env["HOME"] = home
    env.pop("ACCOUNT_CONNECTOR_FABRIC_BYPASSED", None)
    env["CLAUDE_CODE_ENTRYPOINT"] = "test-harness"
    env["CLAUDE_CODE_CHILD_SESSION"] = "1"
    if env_extra:
        env.update(env_extra)
    p = subprocess.run(
        ["python3", HOOK], input=stdin, env=env, capture_output=True, text=True
    )
    audit_path = os.path.join(
        home, ".claude", "audit", "account-connector-fabric-checks.log"
    )
    audit = ""
    if os.path.exists(audit_path):
        with open(audit_path) as fh:
            audit = fh.read()
    return p.returncode, p.stdout, audit


failures = []


def check(name, cond, detail=""):
    status = "PASS" if cond else "FAIL"
    print(f"{status}: {name}" + (f" ({detail})" if detail and not cond else ""))
    if not cond:
        failures.append(name)


# T1: expectation present -> directive emitted, audit says so
rc, out, audit = run(json.dumps({"claudeAiMcpEverConnected": EVER_CONNECTED}))
check("T1 rc=0 with expectation", rc == 0, f"rc={rc}")
check("T1 emits fabric header", "ACCOUNT-CONNECTOR FABRIC CHECK" in out)
check("T1 names Era class", "Era (personal finance)" in out)
check("T1 names Harvest class", "Harvest" in out)
check("T1 cites the origin signal", "SIG-DISPATCH-SESSION-NO-ACCOUNT-CONNECTORS-2026-08-19.md" in out)
check("T1 teaches current prefix scheme", "mcp__claude_ai_" in out)
check("T1 teaches legacy prefix scheme", "mcp__2af7d4b6-" in out)
check("T1 prescribes the one-line warning", "ACCOUNT-CONNECTOR FABRIC ABSENT" in out)
check("T1 session class telemetry", "entrypoint=test-harness" in out)
check("T1 audit line", "verdict=directive-emitted" in audit and "expected=8" in audit)

# T2: bypass env -> silent, audited
rc, out, audit = run(
    json.dumps({"claudeAiMcpEverConnected": EVER_CONNECTED}),
    env_extra={"ACCOUNT_CONNECTOR_FABRIC_BYPASSED": "1"},
)
check("T2 rc=0 under bypass", rc == 0, f"rc={rc}")
check("T2 silent under bypass", out.strip() == "", f"out={out[:80]!r}")
check("T2 audit says bypassed", "verdict=bypassed" in audit)

# T3: no ~/.claude.json at all -> silent (machine never had the fabric)
rc, out, audit = run(None)
check("T3 rc=0 without config", rc == 0, f"rc={rc}")
check("T3 silent without config", out.strip() == "", f"out={out[:80]!r}")
check("T3 audit says no expectation", "verdict=silent-no-expectation" in audit)

# T4: empty ever-connected list -> silent
rc, out, audit = run(json.dumps({"claudeAiMcpEverConnected": []}))
check("T4 silent on empty list", rc == 0 and out.strip() == "")
check("T4 audit says no expectation", "verdict=silent-no-expectation" in audit)

# T5: malformed config JSON -> fail open, silent
rc, out, audit = run("{not valid json")
check("T5 rc=0 on malformed config", rc == 0, f"rc={rc}")
check("T5 silent on malformed config", out.strip() == "")

# T6: garbage stdin with valid expectation -> directive still emitted
rc, out, audit = run(
    json.dumps({"claudeAiMcpEverConnected": EVER_CONNECTED}), stdin="not-json"
)
check("T6 rc=0 on garbage stdin", rc == 0, f"rc={rc}")
check("T6 directive despite garbage stdin", "ACCOUNT-CONNECTOR FABRIC CHECK" in out)
check("T6 audit records unknown session", "session=unknown" in audit)

print()
if failures:
    print(f"{len(failures)} FAILURE(S): {failures}")
    sys.exit(1)
print("ALL TESTS PASSED")
sys.exit(0)
