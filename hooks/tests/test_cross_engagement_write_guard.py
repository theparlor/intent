#!/usr/bin/env python3
"""Catch-net for SIG-0026 (JohnsonControls repo): cross-engagement-write-guard.sh.

Runs the hook's own --selftest, which builds a throwaway Workspaces with fixture
engagements (Alpha, Beta, Gamma) and asserts the load-bearing properties:
- the 2026-09-24 shape (an Alpha app worktree session writing a Beta lesson that names
  Beta people and a Beta team into Alpha's project memory) is BLOCKED, by Write, by a
  Bash heredoc, and by cp of another engagement's memory file;
- the repair moves (the same lesson into Beta's own memory; a name-free lesson that keeps
  engagement names into Alpha's) are silent;
- a same-engagement write is silent;
- a cross-engagement repo write gets exactly one advisory per session per engagement.
When the real material is on this machine, it also replays the actual 2026-09-24 lesson
from the Subaru project memory into the JohnsonControls project memory and expects a block.

Run: python3 hooks/tests/test_cross_engagement_write_guard.py
"""
import os
import subprocess
import sys

HOOK = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "cross-engagement-write-guard.sh")


def test_selftest_passes():
    r = subprocess.run([sys.executable, HOOK, "--selftest"], capture_output=True, text=True, timeout=300)
    assert r.returncode == 0, r.stdout + r.stderr
    assert "FAIL" not in r.stdout, r.stdout
    assert "selftest " in r.stdout


def test_empty_and_malformed_input_fail_open():
    for raw in ("", "not json", "{}"):
        r = subprocess.run([sys.executable, HOOK], input=raw, capture_output=True, text=True, timeout=60)
        assert r.returncode == 0, (raw, r.stderr)


if __name__ == "__main__":
    test_selftest_passes()
    test_empty_and_malformed_input_fail_open()
    print("ok")
