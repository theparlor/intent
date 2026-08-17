#!/usr/bin/env python3
# client-visible-content-lint.sh
#
# PreToolUse content lint for CLIENT-VISIBLE write surfaces. Scans outbound
# payloads (Jira issue create/edit/comment, Confluence page create/update,
# Slack sends, Bash POST/PUT to *.atlassian.net or the Slack API) for internal
# tooling references before submission, and blocks with a redaction message.
#
# Why this exists:
# - SIG-MCP-LEAK-IN-CLIENT-JIRA-2026-05-04: TSD-46 was published to client
#   Jira naming the Atlassian MCP, a sub-agent codename (W2-TSD-HYGIENE) and
#   an audit codename. Memory advisories did not prevent recurrence: 99 days
#   later (2026-08-11) the pattern recurred via the auth runbook, with the AI
#   vendor name reaching client-visible surfaces.
# - Client team members have not been told about the production tooling layer
#   and should never process it alongside the deliverable.
# - Advisory rules are not mechanisms. This hook is the mechanism at the only
#   place all writers pass: the tool-call boundary (direct calls AND sub-agent
#   calls AND future tools).
#
# Scope discipline (D-N145, operating-vs-historical):
# - OUTBOUND payloads only. This hook never lints local corpus files; archived
#   audits legitimately contain every one of these tokens as historical record.
# - Read verbs are exempt: a JQL search FOR a forbidden token is legitimate
#   investigation, not publication.
#
# Fail-closed on a missing/corrupt token file (deliberate deviation from the
# fail-open sibling native-connector-precedence-check.sh): exit-0 stderr is
# invisible in practice, so failing open would silently disable a leak guard.
# Refusing client-surface writes until the token spec loads is loud and gets
# fixed immediately; the JQL catch-net is the backstop, not the substitute.
#
# Bypass (false-positive valve, both logged with a reason of 12+ chars):
# - MCP tool calls carry no environment, so they use a single-use, 30-minute
#   grant file written from Bash (pattern proven by the native-connector hook,
#   whose env-only bypass was unreachable for the calls it blocked).
# - Bash-path calls may instead prefix CLIENT_CONTENT_LINT_BYPASSED=1
#   CLIENT_CONTENT_LINT_REASON='...'.
#
# Registration (settings.json PreToolUse matcher):
#   Bash|mcp__.*(atlassian|slack|4ae6210b|bb5eb37b).*|mcp__.*__(createJiraIssue|editJiraIssue|transitionJiraIssue|addCommentToJiraIssue|addWorklogToJiraIssue|createConfluencePage|updateConfluencePage|createConfluenceFooterComment|updateConfluenceFooterComment)
#
# Token spec: client-visible-content-lint-tokens.json (adjacent; the JQL
# catch-net scanner consumes the same file, one list, two enforcement points).
# Signal: SIG-MCP-LEAK-IN-CLIENT-JIRA-2026-05-04
# Tests: tests/test_client_content_lint.py

import json
import os
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

SIGNAL_ID = "SIG-MCP-LEAK-IN-CLIENT-JIRA-2026-05-04"
GRANT_FILE = Path.home() / ".claude" / "client-visible-content-lint-grant.json"
GRANT_TTL_SECONDS = 1800
MIN_REASON = 12

ATLASSIAN_WRITE_VERBS = {
    "createJiraIssue", "editJiraIssue", "transitionJiraIssue",
    "addCommentToJiraIssue", "addWorklogToJiraIssue",
    "createConfluencePage", "updateConfluencePage",
    "createConfluenceFooterComment", "updateConfluenceFooterComment",
}
ATLASSIAN_SERVER_MARKS = ("atlassian", "4ae6210b-a30e-4336-979b-7301cd434920")
SLACK_SERVER_MARKS = ("slack", "bb5eb37b-8361-4b5a-9a53-dcf2e5d3e089")

# Self-surface destinations: Brien's own status channels, where the internal
# tooling layer is the subject matter rather than a leak. Added 2026-08-17 after
# the hook blocked a Pulse weekly digest post to #pulse on two tokens: "MCP"
# inside a verbatim public article title, and "Claude" in the digest's own
# mark-consumed instruction. Both are correct content for that destination.
#
# The defect this fixes is that the hook classified by TOOL when the risk lives
# in the DESTINATION. slack_send_message to #pulse and slack_send_message to a
# client channel are the same tool with opposite risk profiles. A blanket
# per-tool grant would have disabled the lint for every Slack destination
# including client and peer channels, which is exactly the leak class
# SIG-MCP-LEAK-IN-CLIENT-JIRA-2026-05-04 exists to stop. Scoping by channel_id
# keeps every other destination linted with no change in behavior.
#
# Membership rule: a destination belongs here only if Brien is the sole audience.
# A channel with peers or clients in it NEVER qualifies, even inside his own
# workspace. engineers-united contains Brien's peers; only the dedicated #pulse
# channel inside it is a self-surface. A DM to another human is never eligible.
SELF_SURFACE_DESTINATIONS = {
    "C0BFLP20U2Y": "#pulse, Brien's dedicated Pulse digest channel "
                   "(pre-authorized self-surface, 2026-07-06)",
}
WRITE_SHAPED = ("send", "post", "publish", "reply", "schedule", "broadcast",
                "update", "create", "edit", "add", "set", "transition")
READ_SHAPED = ("search", "read", "get", "list", "history", "info", "fetch",
               "lookup", "describe")

# Bash: a command is in scope only when it targets a client surface with a
# write method. $JIRA_BASE/$DEV are the engagement idioms for the tenant URLs.
BASH_HOST_RE = re.compile(
    r"atlassian\.net|\$\{?JIRA_BASE\}?|\$\{?DEV\}?\b|hooks\.slack\.com|slack\.com/api/")
BASH_WRITE_RE = re.compile(
    r"(?i)(-X\s*(POST|PUT|PATCH)\b|--request[\s=]+(POST|PUT|PATCH)\b|--data(-\w+)?\b"
    r"|--json\b|(?<![\w-])-d\s|--form\b|(?<![\w-])-F\s"
    r"|requests\.(post|put|patch)\(|\.post\(|\.put\(|\.patch\()")
# Local-path clauses stripped before scanning so `cd .../scripts && source
# .../soa.env && curl ...` does not trip path tokens on its own arguments.
BASH_LOCAL_CLAUSE_RE = re.compile(r"(?:^|(?<=&&)|(?<=;))\s*(?:cd|source|\.)\s+[^&;|]+")
BASH_AT_FILE_RE = re.compile(r"@[\w./~-]+")


def _log(msg: str) -> None:
    """Best-effort log to ~/.claude/logs/. Failures here never block work."""
    try:
        log_dir = Path.home() / ".claude" / "logs"
        log_dir.mkdir(parents=True, exist_ok=True)
        ts = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
        with (log_dir / "client-visible-content-lint.log").open("a") as fh:
            fh.write(f"[{ts}] {msg}\n")
    except Exception:
        pass


def _fail_closed(detail: str) -> int:
    print(
        "\nBLOCKED: client-visible-content-lint (guard cannot load its spec)\n\n"
        f"  {detail}\n\n"
        "  This hook fails CLOSED: client-surface writes wait until the tokens\n"
        "  file loads, because a leak guard that silently disables itself is\n"
        "  not a guard. Fix the file (or the symlink), then retry.\n"
        f"  Signal: {SIGNAL_ID}\n",
        file=sys.stderr,
    )
    _log(f"FAIL-CLOSED {detail}")
    return 2


def _load_tokens():
    """Returns (compiled_list, error_string). compiled_list is [(id, regex)]."""
    override = os.environ.get("CLIENT_CONTENT_LINT_TOKENS", "").strip()
    if override:
        path = Path(override)
    else:
        try:
            path = Path(__file__).resolve().parent / "client-visible-content-lint-tokens.json"
        except Exception as e:
            return None, f"cannot resolve script directory: {e}"
    if not path.is_file():
        return None, f"tokens file missing at {path}"
    try:
        spec = json.loads(path.read_text())
        compiled = []
        for tok in spec.get("tokens", []):
            flags = re.IGNORECASE if "i" in tok.get("flags", "") else 0
            compiled.append((tok["id"], re.compile(tok["pattern"], flags)))
        if not compiled:
            return None, f"tokens file at {path} contains no tokens"
        return compiled, ""
    except Exception as e:
        return None, f"tokens file at {path} unreadable: {e}"


def _iter_strings(obj, path="tool_input"):
    if isinstance(obj, str):
        yield path, obj
    elif isinstance(obj, dict):
        for k, v in obj.items():
            yield from _iter_strings(v, f"{path}.{k}")
    elif isinstance(obj, (list, tuple)):
        for i, v in enumerate(obj):
            yield from _iter_strings(v, f"{path}[{i}]")


def _classify(tool_name: str, tool_input) -> str:
    """'scan-mcp' | 'scan-bash' | 'allow'."""
    if tool_name == "Bash":
        cmd = tool_input.get("command", "") if isinstance(tool_input, dict) else ""
        if BASH_HOST_RE.search(cmd) and BASH_WRITE_RE.search(cmd):
            return "scan-bash"
        return "allow"
    if "__" not in tool_name or not tool_name.startswith("mcp__"):
        return "allow"
    server, _, verb = tool_name[len("mcp__"):].rpartition("__")
    if not server:
        return "allow"
    server_l, verb_l = server.lower(), verb.lower()
    if verb in ATLASSIAN_WRITE_VERBS:
        return "scan-mcp"
    is_atlassian = any(m in server_l for m in ATLASSIAN_SERVER_MARKS)
    is_slack = any(m in server_l for m in SLACK_SERVER_MARKS)
    if not (is_atlassian or is_slack):
        return "allow"
    # Destination scoping (see SELF_SURFACE_DESTINATIONS). Only exact channel_id
    # matches exempt, and only for Slack: a thread reply inherits its parent's
    # channel_id, so threads on a self-surface are covered without a second rule.
    # Anything that is not a plain string id (a name, a user id for a DM, a
    # missing field) falls through to the scan, so the failure direction is
    # toward linting rather than toward leaking.
    if is_slack and isinstance(tool_input, dict):
        dest = tool_input.get("channel_id")
        if isinstance(dest, str) and dest.strip() in SELF_SURFACE_DESTINATIONS:
            return "allow"
    if any(r in verb_l for r in READ_SHAPED):
        return "allow"
    if any(w in verb_l for w in WRITE_SHAPED):
        return "scan-mcp"
    return "allow"


def _scan(strings, tokens):
    findings = []
    for path, text in strings:
        for tok_id, rx in tokens:
            m = rx.search(text)
            if m:
                start = max(0, m.start() - 20)
                excerpt = text[start:m.end() + 20].replace("\n", " ")
                findings.append((tok_id, path, excerpt))
    return findings


def _consume_grant(tool_name: str) -> str:
    """Reason string if a live grant covers this tool, else ''. Single use."""
    try:
        if not GRANT_FILE.is_file():
            return ""
        grant = json.loads(GRANT_FILE.read_text())
        age = datetime.now(timezone.utc).timestamp() - float(grant.get("granted_at", 0))
        if age > GRANT_TTL_SECONDS or age < -60:
            return ""
        if grant.get("tool", "") not in ("*", tool_name):
            return ""
        reason = str(grant.get("reason", "")).strip()
        if len(reason) < MIN_REASON:
            return ""
        try:
            GRANT_FILE.unlink()
        except Exception:
            pass
        return reason
    except Exception:
        return ""


def main() -> int:
    raw = sys.stdin.read()
    if not raw.strip():
        return 0
    try:
        payload = json.loads(raw)
    except json.JSONDecodeError as e:
        print(f"[client-visible-content-lint] WARN failed to parse stdin: {e}", file=sys.stderr)
        return 0

    tool_name = (payload.get("tool_name") or "").strip()
    tool_input = payload.get("tool_input") or {}

    mode = _classify(tool_name, tool_input)
    if mode == "allow":
        return 0

    tokens, err = _load_tokens()
    if err:
        return _fail_closed(err)

    if mode == "scan-bash":
        cmd = tool_input.get("command", "")
        cmd = BASH_LOCAL_CLAUSE_RE.sub(" ", cmd)
        cmd = BASH_AT_FILE_RE.sub("@LOCALFILE", cmd)
        strings = [("command", cmd)]
    else:
        strings = list(_iter_strings(tool_input))

    findings = _scan(strings, tokens)
    if not findings:
        return 0

    session_id = os.environ.get("CLAUDE_SESSION_ID", "unknown")
    token_ids = sorted({f[0] for f in findings})

    # False-positive valves, in order. Env path works only for Bash-driven
    # invocations (MCP calls carry no per-call environment).
    if os.environ.get("CLIENT_CONTENT_LINT_BYPASSED") == "1":
        reason = os.environ.get("CLIENT_CONTENT_LINT_REASON", "").strip()
        if len(reason) >= MIN_REASON:
            _log(f"ENV-BYPASS session={session_id} tool={tool_name} tokens={','.join(token_ids)} reason={reason}")
            print(
                f"[client-visible-content-lint] ALLOWED via env bypass: {tool_name}\n"
                f"  Reason on record: {reason}",
                file=sys.stderr,
            )
            return 0

    reason = _consume_grant(tool_name)
    if reason:
        _log(f"GRANT session={session_id} tool={tool_name} tokens={','.join(token_ids)} reason={reason}")
        print(
            f"[client-visible-content-lint] ALLOWED via single-use grant: {tool_name}\n"
            f"  Reason on record: {reason}. Grant consumed.",
            file=sys.stderr,
        )
        return 0

    _log(f"BLOCK session={session_id} tool={tool_name} tokens={','.join(token_ids)}")

    lines = [
        "",
        "BLOCKED: client-visible-content-lint",
        "",
        f"  Tool: {tool_name}",
        "  This payload is bound for a CLIENT-VISIBLE surface and contains",
        "  internal tooling references:",
        "",
    ]
    for tok_id, path, excerpt in findings[:8]:
        lines.append(f"    - token '{tok_id}' at {path}: ...{excerpt}...")
    if len(findings) > 8:
        lines.append(f"    - and {len(findings) - 8} more")
    lines += [
        "",
        "  Client surfaces never carry the AI/tooling layer or workspace",
        "  structure: no MCP or connector references, no sub-agent or audit",
        "  codenames, no workspace paths, no internal product, script, or",
        "  register names. Rewrite the flagged text in client-plain language",
        "  and resend.",
        f"  Signal: {SIGNAL_ID}",
        "",
        "  FALSE POSITIVE? (client-domain text that legitimately uses the term,",
        "  e.g. a Salesforce 'connector' in CRM copy, or a quoted client string)",
        "  For an MCP tool call, write a single-use grant from Bash, then retry:",
        "",
        "    python3 - <<'EOF'",
        "    import json, time, pathlib",
        "    p = pathlib.Path.home() / '.claude' / 'client-visible-content-lint-grant.json'",
        f"    p.write_text(json.dumps({{'tool': '{tool_name}',",
        "        'reason': 'STATE THE LEGITIMATE USE, min 12 chars',",
        "        'granted_at': time.time()}))",
        "    EOF",
        "",
        "  For a Bash command, prefix instead:",
        "    CLIENT_CONTENT_LINT_BYPASSED=1 CLIENT_CONTENT_LINT_REASON='why' <command>",
        "",
        "  Single use, 30 minute TTL, logged with the reason. If the term truly",
        "  belongs on the client surface, say why; the log is the audit trail.",
        "",
    ]
    print("\n".join(lines), file=sys.stderr)
    return 2


if __name__ == "__main__":
    sys.exit(main())
