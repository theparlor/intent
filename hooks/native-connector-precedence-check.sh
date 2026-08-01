#!/usr/bin/env python3
# native-connector-precedence-check.sh
#
# PreToolUse hook that intercepts mcp__google-workspace__* tool calls and
# blocks them when an Anthropic-native equivalent exists. Allows pass-through
# for workspace-mcp-only verbs (Docs editing, Sheets ops, advanced Calendar,
# Gmail filters, batch ops).
#
# Why this exists:
# - workspace-mcp has separate auth from Anthropic-native connectors. When its
#   auth lapses, calls fail with auth-required errors that look like real
#   blockers but aren't — the native connector is healthy the whole time.
# - Memory + skill-prompt instructions are insufficient catch-net (proven by
#   the 2026-05-27 overwatch sweep where /overwatch itself reached for
#   workspace-mcp despite the memory rule existing).
# - Mechanism-level fix: intercept the tool call and force the agent to the
#   native connector when one is available.
#
# Spec: Core/frameworks/intent/spec/native-connector-precedence.md
# Signal: SIG-2026-05-27-native-connector-precedence-hook-gap.md
# Memory: feedback_prefer_native_anthropic_connectors.md
#
# Bypass: set NATIVE_CONNECTOR_PRECEDENCE_BYPASSED=1 (logged when used).
#
# File extension is .sh for symmetry with existing hooks in this directory,
# but the script is python3 because the lookup table is structured JSON and
# python is already in the hook ecosystem (see PostToolUse hooks in
# ~/.claude/settings.json that inline python3).

import json
import os
import sys
from datetime import datetime, timezone
from pathlib import Path


def _log(filename: str, msg: str) -> None:
    """Best-effort log to ~/.claude/logs/. Failures here never block work."""
    try:
        log_dir = Path.home() / ".claude" / "logs"
        log_dir.mkdir(parents=True, exist_ok=True)
        ts = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
        with (log_dir / filename).open("a") as fh:
            fh.write(f"[{ts}] {msg}\n")
    except Exception:
        pass


GRANT_FILE = Path.home() / ".claude" / "native-connector-fallback-grant.json"
GRANT_TTL_SECONDS = 1800  # 30 minutes


def _consume_grant(tool_name: str) -> str:
    """Return the reason string if a live fallback grant covers this tool, else "".

    The grant is a small JSON file the agent writes from Bash. It exists because
    the original env-var bypass was UNREACHABLE: an MCP tool call carries no
    environment, so NATIVE_CONNECTOR_PRECEDENCE_BYPASSED=1 could never be set for
    the very calls this hook blocks. A documented escape hatch that cannot be
    used is the same as no escape hatch, which made every block absolute.

    Grant shape:
        {"tool": "mcp__google-workspace__create_drive_file" | "*",
         "reason": "why native cannot do this",
         "granted_at": "<unix seconds>"}

    Single-use per call and TTL-bounded, so it is a speed bump rather than a
    standing exemption. Malformed or stale grants are ignored (fail closed to
    the block, which is the safe direction here).
    """
    try:
        if not GRANT_FILE.is_file():
            return ""
        grant = json.loads(GRANT_FILE.read_text())
        age = datetime.now(timezone.utc).timestamp() - float(grant.get("granted_at", 0))
        if age > GRANT_TTL_SECONDS or age < -60:
            return ""
        scope = grant.get("tool", "")
        if scope not in ("*", tool_name):
            return ""
        reason = str(grant.get("reason", "")).strip()
        if len(reason) < 12:
            # A grant with no real reason is not a reason. Treat as absent.
            return ""
        return reason
    except Exception:
        return ""


def main() -> int:
    # Legacy env bypass. Retained for hook invocations that DO carry an
    # environment (Bash-driven paths), but it cannot fire for MCP tool calls.
    if os.environ.get("NATIVE_CONNECTOR_PRECEDENCE_BYPASSED") == "1":
        session_id = os.environ.get("CLAUDE_SESSION_ID", "unknown")
        _log("native-connector-bypass.log", f"BYPASS session={session_id}")
        return 0

    # Resolve the lookup-map file path. Hook may be invoked via symlink;
    # resolve to the real script directory so the map sits adjacent.
    try:
        script_path = Path(__file__).resolve()
    except Exception:
        # Pathological case — fail open.
        return 0
    map_file = script_path.parent / "native-connector-precedence-map.json"

    if not map_file.is_file():
        _log("native-connector-warnings.log", f"map file missing at {map_file} — allowing call")
        return 0

    # Read PreToolUse payload from stdin.
    raw_stdin = sys.stdin.read()
    if not raw_stdin.strip():
        # No input — nothing to check. Allow.
        return 0
    try:
        payload = json.loads(raw_stdin)
    except json.JSONDecodeError as e:
        print(f"[native-connector-precedence] WARN failed to parse stdin: {e}", file=sys.stderr)
        return 0

    tool_name = (payload.get("tool_name") or "").strip()

    # Early exit — only inspect workspace-mcp tools.
    if not tool_name.startswith("mcp__google-workspace__"):
        return 0

    try:
        with map_file.open() as fh:
            mapping = json.load(fh)
    except Exception as e:
        _log("native-connector-warnings.log", f"failed to load map: {e}")
        return 0

    blocked = mapping.get("blocked_with_native_equivalent", {})
    fallback_section = mapping.get("fallback_allowed", {})
    fallback = set(fallback_section.get("verbs", []))
    native_prefixes = mapping.get("_meta", {}).get("native_prefixes", {})

    # Explicit fallback — allow.
    if tool_name in fallback:
        return 0

    entry = blocked.get(tool_name)
    if entry:
        native_label = entry.get("native_prefix", "")
        native_uuid = native_prefixes.get(native_label, "")
        native_verb = entry.get("native_verb", "<unknown>")
        note = entry.get("note", "")

        # A live, reasoned grant downgrades the block to a warning. This is the
        # load-on-demand case: the native connector does not cover what is being
        # asked, or it was tried and failed. Precedence still holds by default;
        # it just is not absolute any more.
        reason = _consume_grant(tool_name)
        if reason:
            session_id = os.environ.get("CLAUDE_SESSION_ID", "unknown")
            _log(
                "native-connector-bypass.log",
                f"GRANT session={session_id} tool={tool_name} reason={reason}",
            )
            try:
                GRANT_FILE.unlink()  # single use
            except Exception:
                pass
            print(
                f"[native-connector-precedence] ALLOWED via fallback grant: {tool_name}\n"
                f"  Reason on record: {reason}\n"
                f"  Grant consumed. Native equivalent remains {native_uuid}{native_verb}.",
                file=sys.stderr,
            )
            return 0

        lines = [
            "",
            "BLOCKED: native-connector-precedence",
            "",
            f"  Tool requested: {tool_name}",
            f"  Native equivalent: {native_uuid}{native_verb}",
            "",
            f"  Reason: Anthropic-native {native_label.capitalize()} connector is the",
            "  primary tool surface. workspace-mcp is a fallback. Use the native verb",
            "  above instead.",
        ]
        if note:
            lines += ["", f"  Note: {note}"]
        lines += [
            "",
            "  This is precedence, not prohibition. workspace-mcp is load-on-demand.",
            "  If the native verb genuinely cannot do this (missing capability, or you",
            "  tried it and it failed), record why and retry. Run this in Bash first:",
            "",
            "    python3 - <<'EOF'",
            "    import json, time, pathlib",
            "    p = pathlib.Path.home() / '.claude' / 'native-connector-fallback-grant.json'",
            "    p.parent.mkdir(parents=True, exist_ok=True)",
            f"    p.write_text(json.dumps({{'tool': '{tool_name}',",
            "        'reason': 'STATE THE ACTUAL GAP OR FAILURE, min 12 chars',",
            "        'granted_at': time.time()}))",
            "    EOF",
            "",
            "  Single use, 30 minute TTL, logged with your reason. A grant with no real",
            "  reason is ignored. Do not reach for this reflexively: if the native verb",
            "  can do the job, it is still the right call and it is more reliable.",
            "",
            "  (The old NATIVE_CONNECTOR_PRECEDENCE_BYPASSED=1 env bypass cannot work",
            "  for MCP tool calls, which carry no environment. That is why this exists.)",
            "",
            "  Spec: Core/frameworks/intent/spec/native-connector-precedence.md",
            "  Memory: feedback_prefer_native_anthropic_connectors.md",
            "",
        ]
        print("\n".join(lines), file=sys.stderr)
        # Exit 2 = block + show stderr to model.
        return 2

    # Unknown workspace-mcp verb. Warn but allow — map needs an update.
    print(
        f"[native-connector-precedence] WARN unknown workspace-mcp verb '{tool_name}' "
        f"— add to native-connector-precedence-map.json (either blocked_with_native_equivalent "
        f"or fallback_allowed). Allowing for now.",
        file=sys.stderr,
    )
    _log("native-connector-warnings.log", f"unknown verb: {tool_name}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
