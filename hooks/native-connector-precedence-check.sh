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


def main() -> int:
    # Bypass — logged, then exit clean.
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
            "  Bypass (only when you have a documented reason workspace-mcp is required):",
            "    NATIVE_CONNECTOR_PRECEDENCE_BYPASSED=1 <retry-call>",
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
