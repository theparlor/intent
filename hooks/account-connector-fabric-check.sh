#!/usr/bin/env python3
# account-connector-fabric-check.sh
#
# SessionStart hook: probes whether this machine expects the claude.ai
# account-connector fabric (Era, Gmail, Google Drive, Google Calendar,
# Slack, Atlassian, Granola, Harvest) and, when it does, injects a
# session-layer roster check directive into session-start context.
#
# Sensor inversion, and why: a SessionStart hook CANNOT see the session's
# tool roster. stdin carries only {session_id, transcript_path, cwd,
# hook_event_name, source} (verified empirically on claude CLI 2.1.228,
# 2026-08-19, via a stdin-dumping probe hook). The model is the only
# session-layer sensor, so this hook makes the model perform the check and
# open its first reply with a one-line warning when the fabric is absent.
#
# Origin: on 2026-08-19 two dispatched worktree sessions launched with ZERO
# account connectors while `claude mcp list` reported all account
# connectors healthy. A financial-analysis task silently blocked on the
# missing Era connector until the fabric re-attached mid-session. Signal
# (Workspaces repo):
#   .intent/signals/SIG-DISPATCH-SESSION-NO-ACCOUNT-CONNECTORS-2026-08-19.md
#
# False-alarm boundary (three levers, spec section on false alarms):
#   1. ACCOUNT_CONNECTOR_FABRIC_BYPASSED=1 -> silent. For intentionally
#      bare launches (cron, launchd, scripted harnesses). The env lever is
#      reachable here because the unit is a process launch; contrast the
#      2026-07-31 finding that MCP tool calls carry no environment.
#   2. Empty or absent claudeAiMcpEverConnected in ~/.claude.json ->
#      silent. A machine or account that never had the fabric never warns.
#   3. Everything else is ADVISORY by design: per-session intent is not
#      mechanically inferable (no roster on stdin; child-session env
#      markers appear on fabric-bearing sessions too). The directive tells
#      the model to weigh task relevance before escalating.
#
# File extension is .sh for symmetry with the other hooks in this
# directory; the script is python3 (native-connector-precedence-check.sh
# precedent) because the expectation source is structured JSON.
#
# Spec:    Core/frameworks/intent/spec/account-connector-fabric-check.md
# Install: hooks/install.sh symlinks into ~/.claude/hooks/; registration
#          is a SessionStart entry in ~/.claude/settings.json (see spec).
# Audit:   ~/.claude/audit/account-connector-fabric-checks.log
# Bypass:  ACCOUNT_CONNECTOR_FABRIC_BYPASSED=1 (logged)
#
# Fail-open discipline: any unexpected error exits 0 silently. This hook
# only injects context; it must never block a session from starting.

import json
import os
import sys
from datetime import datetime, timezone
from pathlib import Path

# Task-critical connector classes (the 2026-08-19 blast roster) with the
# match tokens the model should look for inside mcp__ tool names. Current
# builds name tools mcp__claude_ai_<Name>__<verb> (observed 2026-08-19);
# older surfaces used hex-UUID prefixes (kept as legacy alternates).
WARN_CLASSES = [
    ("Era (personal finance)", "Era_Context", "8f9971da"),
    ("Gmail", "Gmail", "2af7d4b6"),
    ("Google Drive", "Google_Drive", "af517670"),
    ("Google Calendar", "Google_Calendar", "e84bacfb"),
    ("Slack", "Slack", "bb5eb37b"),
    ("Atlassian (incl Rovo)", "Atlassian", "4ae6210b"),
    ("Granola", "Granola", "610554ec"),
    ("Harvest", "Harvest", "0ab7ee41"),
]

SIGNAL_NAME = "SIG-DISPATCH-SESSION-NO-ACCOUNT-CONNECTORS-2026-08-19.md"
SPEC_PATH = "Core/frameworks/intent/spec/account-connector-fabric-check.md"


def _audit(msg: str) -> None:
    """Best-effort one-line audit append. Failures never block the hook."""
    try:
        audit_dir = Path.home() / ".claude" / "audit"
        audit_dir.mkdir(parents=True, exist_ok=True)
        ts = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
        log = audit_dir / "account-connector-fabric-checks.log"
        with log.open("a") as fh:
            fh.write(f"[{ts}] {msg}\n")
    except Exception:
        pass


def _read_stdin_meta() -> dict:
    """Parse the SessionStart stdin JSON. Fail open to an empty dict."""
    try:
        return json.loads(sys.stdin.read() or "{}")
    except Exception:
        return {}


def _ever_connected() -> list:
    """Return the claude.ai connector names ever connected on this machine.

    Source: ~/.claude.json key claudeAiMcpEverConnected (a list of display
    names like "claude.ai Gmail"). Missing file, malformed JSON, or a
    non-list value all read as "no expectation" -> the hook stays silent.
    """
    try:
        cfg = json.loads((Path.home() / ".claude.json").read_text())
        names = cfg.get("claudeAiMcpEverConnected")
        if isinstance(names, list):
            return [str(n) for n in names if str(n).strip()]
    except Exception:
        pass
    return []


def main() -> int:
    meta = _read_stdin_meta()
    session = meta.get("session_id", "unknown")
    source = meta.get("source", "unknown")
    cwd = meta.get("cwd", os.getcwd())
    entrypoint = os.environ.get("CLAUDE_CODE_ENTRYPOINT", "unknown")
    child = os.environ.get("CLAUDE_CODE_CHILD_SESSION", "0")
    base = (
        f"session={session} source={source} entrypoint={entrypoint} "
        f"child={child} cwd={cwd}"
    )

    if os.environ.get("ACCOUNT_CONNECTOR_FABRIC_BYPASSED", "0") == "1":
        _audit(f"{base} verdict=bypassed")
        return 0

    names = _ever_connected()
    if not names:
        _audit(f"{base} expected=0 verdict=silent-no-expectation")
        return 0

    display = ", ".join(
        n[len("claude.ai "):] if n.startswith("claude.ai ") else n
        for n in names
    )
    classes = ", ".join(c[0] for c in WARN_CLASSES)
    legacy = ", ".join(f"mcp__{c[2]}-" for c in WARN_CLASSES[:3])

    print(f"""🔌 ACCOUNT-CONNECTOR FABRIC CHECK (session-layer sensor is the model)

claude.ai connectors on record for this account ({len(names)}): {display}
Task-critical classes: {classes}
Session class: entrypoint={entrypoint} child={child} source={source}

A SessionStart hook cannot see this session's tool roster (stdin carries
no MCP data; verified 2026-08-19). You, the model, can. Before your first
reply, silently scan your tool names (active plus deferred listings) for
the fabric: prefix "mcp__claude_ai_" on current builds, legacy hex-UUID
prefixes (for example {legacy}) on older ones.

  1. NONE present: open your FIRST reply with one line:
     "⚠ ACCOUNT-CONNECTOR FABRIC ABSENT: 0 claude.ai connectors attached;
     missing <the task-critical classes, or the subset the task needs>."
     If the task needs any missing class, surface the block to Brien
     BEFORE grinding local fallbacks. Known blast pattern: account layer
     healthy while a dispatched session launches bare; the fabric can
     re-attach mid-session, so recheck before declaring a task blocked.
     Signal: .intent/signals/{SIGNAL_NAME}
  2. PARTIAL (a class the task needs is missing): same one-line warning
     naming just the missing classes.
  3. Fabric present, or the task plainly needs none of it: say nothing
     about this check.

This check is ADVISORY: per-session intent is not mechanically inferable.
Intentionally bare launches silence it with
ACCOUNT_CONNECTOR_FABRIC_BYPASSED=1. Machines with no claude.ai connectors
on record never see it.

Spec: {SPEC_PATH}""")

    _audit(f"{base} expected={len(names)} verdict=directive-emitted")
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except Exception as exc:  # fail open, never block session start
        _audit(f"verdict=fail-open error={exc!r}")
        sys.exit(0)
