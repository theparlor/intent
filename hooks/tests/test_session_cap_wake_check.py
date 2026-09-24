#!/usr/bin/env python3
"""Test harness for session-cap-wake-check.sh.

Feeds synthetic PostToolUse payloads carrying the session-cap 429 text and
asserts: the reset time is parsed correctly under several phrasings, an arm
happens (audit log line + marker file + wake script written), a second 429
naming the same reset time is skipped (idempotency), and a 429 for a
DIFFERENT reset time arms again (idempotency is per-reset-time, not global).
No real sleeping: SESSION_CAP_WAKE_SLEEP_OVERRIDE_SECONDS pins the background
wait to one second, and SESSION_CAP_WAKE_RESUME_CMD replaces the real
`claude --resume` invocation with a marker-file write so the test never spawns
a real CLI session.

Run: python3 tests/test_session_cap_wake_check.py
"""
import json
import os
import shutil
import subprocess
import sys
import tempfile
import time

HOOK = os.environ.get(
    "SESSION_CAP_WAKE_HOOK_PATH",
    os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "session-cap-wake-check.sh"),
)
TMP = tempfile.mkdtemp(prefix="session-cap-wake-test-")


def epoch_at(y, mo, d, h, mi, s=0):
    """Local-time epoch for a given Y-M-D H:M:S, independent of test TZ."""
    return time.mktime((y, mo, d, h, mi, s, 0, 0, -1))


def install_role(home, role):
    """Stand in for the claude-config machine-role helper inside the fake HOME.
    role=None leaves no helper on disk, which the hook must read as unknown."""
    helper = os.path.join(home, ".claude", "hooks", "helpers", "machine-role.sh")
    if role is None:
        if os.path.exists(helper):
            os.remove(helper)
        return
    os.makedirs(os.path.dirname(helper), exist_ok=True)
    with open(helper, "w") as f:
        f.write(f"MACHINE_ROLE={role}\nexport MACHINE_ROLE\n")


def run(text, now_epoch, session_id="sess-test", tool_name="Agent",
        home=None, sleep_override="1", resume_cmd=None, extra_env=None, role="hub"):
    home = home or tempfile.mkdtemp(prefix="home-", dir=TMP)
    install_role(home, role)
    payload = json.dumps({
        "session_id": session_id,
        "tool_name": tool_name,
        "tool_response": {"output": text},
    })
    resume_marker = os.path.join(home, "resume-invoked.marker")
    env = dict(os.environ)
    env["HOME"] = home
    env.pop("CLAUDE_CONFIG_DIR", None)
    env.pop("CLAUDE_MACHINE_JSON", None)
    env["SESSION_CAP_WAKE_NOW_EPOCH"] = str(now_epoch)
    if sleep_override is not None:
        env["SESSION_CAP_WAKE_SLEEP_OVERRIDE_SECONDS"] = str(sleep_override)
    env["SESSION_CAP_WAKE_RESUME_CMD"] = resume_cmd or f'echo RESUMED > "{resume_marker}"'
    env.pop("SESSION_CAP_WAKE_BYPASSED", None)
    if extra_env:
        env.update(extra_env)
    p = subprocess.run(["bash", HOOK], input=payload, env=env,
                        capture_output=True, text=True, timeout=30)
    return p, home, resume_marker


def audit_log(home):
    path = os.path.join(home, ".claude", "audit", "session-cap-wakes.log")
    return open(path).read() if os.path.exists(path) else ""


def state_dir(home):
    return os.path.join(home, ".claude", "audit", "session-cap-wake-state")


fails = []


def check(desc, cond, detail=""):
    ok = bool(cond)
    print(f"  {'PASS' if ok else 'FAIL'}  {desc}")
    if not ok:
        fails.append(f"{desc} {detail}".strip())


# ---------------------------------------------------------------------------
# Case 1: "resets 6pm" parses to today 18:00 relative to a 15:05 baseline,
# arms, logs, and the detached wake actually fires the resume command.
# ---------------------------------------------------------------------------
NOW_1 = epoch_at(2026, 9, 13, 15, 5, 0)
EXPECT_1 = epoch_at(2026, 9, 13, 18, 0, 0)
p1, home1, marker1 = run(
    "Error: You've hit your session limit, resets 6pm", NOW_1)
log1 = audit_log(home1)
check("case1 rc=0", p1.returncode == 0, p1.stderr)
check("case1 ARMED logged", "ARMED" in log1, log1)
check("case1 reset_epoch parsed to today 18:00",
      f"reset_epoch={int(EXPECT_1)}" in log1, log1)
armed_marker_1 = os.path.join(state_dir(home1), f"armed-{int(EXPECT_1)}.marker")
check("case1 idempotency marker written", os.path.exists(armed_marker_1))
time.sleep(1.5)
check("case1 detached wake actually fired the resume command",
      os.path.exists(marker1), "resume marker never appeared")
log1_after = audit_log(home1)
check("case1 WAKE-FIRED logged after sleep", "WAKE-FIRED" in log1_after, log1_after)

# ---------------------------------------------------------------------------
# Case 2: 24-hour form "resets 18:00" from the same baseline parses to the
# same epoch as case 1's "6pm".
# ---------------------------------------------------------------------------
p2, home2, _ = run(
    "session limit hit, resets 18:00", NOW_1, session_id="sess-24h")
log2 = audit_log(home2)
check("case2 24h form parses to same epoch as 6pm",
      f"reset_epoch={int(EXPECT_1)}" in log2, log2)

# ---------------------------------------------------------------------------
# Case 3: idempotency -- a second 429 naming the SAME reset time (6pm) from
# a slightly later baseline, in the SAME home, is skipped, not re-armed.
# ---------------------------------------------------------------------------
NOW_1B = epoch_at(2026, 9, 13, 15, 40, 0)
dup_marker = os.path.join(home1, "sess-dup-resume.marker")
p3, _, _ = run(
    "You have hit your session limit, resets 6pm", NOW_1B,
    session_id="sess-dup", home=home1,
    resume_cmd=f'echo RESUMED_DUP > "{dup_marker}"')
log3 = audit_log(home1)
check("case3 rc=0 on duplicate", p3.returncode == 0, p3.stderr)
check("case3 SKIP-IDEMPOTENT logged", "SKIP-IDEMPOTENT" in log3, log3)
check("case3 did not re-fire the resume command",
      not os.path.exists(dup_marker), "a second, distinct resume marker file appeared")
check("case3 exactly one ARM total for this reset time",
      audit_log(home1).count("ARMED session=") == 1, audit_log(home1))

# ---------------------------------------------------------------------------
# Case 4: idempotency is per-reset-time, not global -- a 429 naming a
# DIFFERENT reset time in the same home arms again.
# ---------------------------------------------------------------------------
EXPECT_4 = epoch_at(2026, 9, 13, 20, 0, 0)
p4, _, marker4 = run(
    "session limit reached, resets 8pm", NOW_1, session_id="sess-diff-time",
    home=home1)
log4 = audit_log(home1)
check("case4 rc=0", p4.returncode == 0, p4.stderr)
check("case4 different reset time arms again",
      f"reset_epoch={int(EXPECT_4)}" in log4 and log4.count("ARMED session=") == 2,
      log4)

# ---------------------------------------------------------------------------
# Case 5: ambiguous hour with no am/pm marker picks the soonest future
# candidate. At 15:05, "resets 7" should mean 19:00 today (7pm), not 07:00
# (which already passed).
# ---------------------------------------------------------------------------
EXPECT_5 = epoch_at(2026, 9, 13, 19, 0, 0)
p5, home5, _ = run("session limit hit, resets 7", NOW_1, session_id="sess-ambig")
log5 = audit_log(home5)
check("case5 ambiguous hour resolves to soonest future (7pm not 7am)",
      f"reset_epoch={int(EXPECT_5)}" in log5, log5)

# ---------------------------------------------------------------------------
# Case 6: no-op on text that lacks either required substring, and on tool
# names other than Workflow/Agent/Bash.
# ---------------------------------------------------------------------------
p6, home6, marker6 = run("everything is fine, no errors here", NOW_1,
                          session_id="sess-clean")
log6 = audit_log(home6)
check("case6 rc=0 on unrelated text", p6.returncode == 0, p6.stderr)
check("case6 no ARM on unrelated text", "ARMED" not in log6, log6)
check("case6 no resume marker on unrelated text", not os.path.exists(marker6))

p7, home7, marker7 = run("You've hit your session limit, resets 6pm", NOW_1,
                          session_id="sess-wrongtool", tool_name="Write")
log7 = audit_log(home7)
check("case7 rc=0 on non-matcher tool", p7.returncode == 0, p7.stderr)
check("case7 no ARM for Write tool_name", "ARMED" not in log7, log7)

# ---------------------------------------------------------------------------
# Case 8: bypass flag suppresses everything.
# ---------------------------------------------------------------------------
p8, home8, marker8 = run("You've hit your session limit, resets 6pm", NOW_1,
                          session_id="sess-bypass",
                          extra_env={"SESSION_CAP_WAKE_BYPASSED": "1"})
log8 = audit_log(home8)
check("case8 rc=0 under bypass", p8.returncode == 0, p8.stderr)
check("case8 BYPASS logged, no ARM", "BYPASS" in log8 and "ARMED" not in log8, log8)
check("case8 no resume marker under bypass", not os.path.exists(marker8))

# ---------------------------------------------------------------------------
# Case 9: role gate (P4). travel arms like the hub; embassy and an absent
# helper (unknown) log a SKIP and never arm.
# ---------------------------------------------------------------------------
p9, home9, marker9 = run("You've hit your session limit, resets 6pm", NOW_1,
                          session_id="sess-travel", role="travel")
log9 = audit_log(home9)
check("case9 travel arms", p9.returncode == 0 and "ARMED" in log9, log9)

for label, role in (("embassy", "embassy"), ("absent helper", None)):
    p10, home10, marker10 = run("You've hit your session limit, resets 6pm", NOW_1,
                                session_id="sess-norole", role=role)
    log10 = audit_log(home10)
    check(f"case10 {label}: rc=0", p10.returncode == 0, p10.stderr)
    check(f"case10 {label}: SKIP role logged, no ARM",
          "SKIP role=" in log10 and "ARMED" not in log10, log10)
    check(f"case10 {label}: no marker written",
          not os.path.isdir(state_dir(home10)) or not any(
              n.startswith("armed-") for n in os.listdir(state_dir(home10))))

# ---------------------------------------------------------------------------
# Case 11: the armed sleeper sleeps the DELTA to reset plus 60 s, never the
# epoch itself. Regression for 2026-09-24: with no sleep override the hook
# computed NOW_EPOCH as 0 (the string '0' is truthy in Python), so every
# sleeper slept for the wake epoch value, about 56 years, and no wake ever
# fired. The wake script is read back rather than run, so nothing sleeps here;
# the script is then removed so no detached sleeper outlives the test.
# ---------------------------------------------------------------------------
NOW_11 = epoch_at(2026, 9, 24, 12, 5, 0)
EXPECT_11 = epoch_at(2026, 9, 24, 18, 0, 0)
p11, home11, marker11 = run("You've hit your session limit, resets 6pm", NOW_11,
                            session_id="sess-delta", sleep_override=None)
log11 = audit_log(home11)
expected_sleep = int(EXPECT_11) + 60 - int(NOW_11)
check("case11 rc=0 and ARMED", p11.returncode == 0 and "ARMED" in log11, log11)
check("case11 sleep_seconds is the delta to reset plus 60",
      f"sleep_seconds={expected_sleep} " in log11, log11)
check("case11 sleep_seconds is under a day (not the epoch)",
      f"sleep_seconds={int(EXPECT_11) + 60} " not in log11, log11)
wake11 = os.path.join(state_dir(home11), f"wake-{int(EXPECT_11)}.sh")
check("case11 wake script sleeps the same delta",
      os.path.exists(wake11) and f"sleep {expected_sleep}\n" in open(wake11).read(),
      open(wake11).read() if os.path.exists(wake11) else "no wake script")
subprocess.run(["pkill", "-f", wake11], capture_output=True)
if os.path.exists(wake11):
    os.remove(wake11)

print()
shutil.rmtree(TMP, ignore_errors=True)
if fails:
    print(f"FAILED ({len(fails)}):")
    for f in fails:
        print("  -", f)
    sys.exit(1)
print("All session-cap-wake-check cases passed.")
