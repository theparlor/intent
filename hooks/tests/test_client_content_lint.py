#!/usr/bin/env python3
"""Test harness for client-visible-content-lint.sh. Runs the hook under a throwaway HOME
so real logs and grant files are untouched. Asserts the block/allow matrix, the read-verb
exemption, Bash local-clause stripping, both bypass paths, and fail-closed token loading.

Contract under test (SIG-MCP-LEAK-IN-CLIENT-JIRA-2026-05-04, mechanism 1):
- PreToolUse hook. stdin = JSON {tool_name, tool_input}. exit 0 allow, exit 2 block.
- Atlassian write verbs (any mcp prefix): scan every string value in tool_input.
- Atlassian read verbs: never scanned (a JQL search FOR a token is legitimate).
- Slack-ish servers: send-shaped verbs scanned, read-shaped allowed.
- Bash: scanned only when the command targets *.atlassian.net or the Slack API with a
  write method; cd/source/@file local-path clauses are stripped before scanning so the
  standard `cd scripts && source soa.env && curl -X PUT ...` idiom does not false-positive.
- Bypass: env CLIENT_CONTENT_LINT_BYPASSED=1 + CLIENT_CONTENT_LINT_REASON (>=12 chars)
  for Bash-path calls; single-use TTL grant file for MCP calls (which carry no env).
- Tokens file missing or unreadable: fail CLOSED (exit 2), because a leak guard that
  silently disables itself is half a mechanism and exit-0 stderr is invisible.
"""
import json, os, subprocess, tempfile, time, sys

HOOK = "/Users/brien/Workspaces/Core/frameworks/intent/hooks/client-visible-content-lint.sh"
TMP = tempfile.mkdtemp(prefix="content-lint-test-")
FAKE_HOME = os.path.join(TMP, "home")
os.makedirs(os.path.join(FAKE_HOME, ".claude", "logs"), exist_ok=True)
LOG = os.path.join(FAKE_HOME, ".claude", "logs", "client-visible-content-lint.log")
GRANT = os.path.join(FAKE_HOME, ".claude", "client-visible-content-lint-grant.json")


def run(tool_name, tool_input, env_extra=None):
    payload = json.dumps({"tool_name": tool_name, "tool_input": tool_input})
    env = dict(os.environ)
    env["HOME"] = FAKE_HOME
    env.pop("CLIENT_CONTENT_LINT_BYPASSED", None)
    env.pop("CLIENT_CONTENT_LINT_REASON", None)
    env.pop("CLIENT_CONTENT_LINT_TOKENS", None)
    if env_extra:
        env.update(env_extra)
    p = subprocess.run(["python3", HOOK], input=payload, env=env,
                       capture_output=True, text=True)
    return p.returncode, p.stderr


def log_lines():
    if not os.path.exists(LOG):
        return []
    with open(LOG) as fh:
        return fh.readlines()


results = []
def check(name, cond):
    results.append((name, cond))
    print(("PASS " if cond else "FAIL ") + name)


ATL = "mcp__4ae6210b-a30e-4336-979b-7301cd434920__"
SLACK = "mcp__bb5eb37b-8361-4b5a-9a53-dcf2e5d3e089__"

# T1: createJiraIssue with MCP in description -> block, names the token id and the signal
rc, err = run(ATL + "createJiraIssue",
              {"cloudId": "cfb9d2c5", "projectKey": "MTEC", "summary": "Align sprint scope",
               "description": "The Atlassian MCP does not expose deleteIssueLink."})
check("T1 createJiraIssue MCP -> block", rc == 2 and "BLOCKED" in err)
check("T1 stderr names token id", "mcp" in err)
check("T1 stderr names signal", "SIG-MCP-LEAK-IN-CLIENT-JIRA-2026-05-04" in err)

# T2: clean createJiraIssue -> allow
rc, err = run(ATL + "createJiraIssue",
              {"projectKey": "MTEC", "summary": "Align sprint scope with release calendar",
               "description": "Move the two remaining stories into the 2026-08-20 release."})
check("T2 clean create -> allow", rc == 0)

# T3: editJiraIssue nested fields with a workspace path -> block
rc, err = run(ATL + "editJiraIssue",
              {"issueIdOrKey": "NS-12",
               "fields": {"description": "See working/jira-migration/BACKLOG.md for the list."}})
check("T3 nested workspace path -> block", rc == 2 and "workspace-path" in err)

# T4: comment with sub-agent codenames, both alpha and digit-bearing forms -> block
rc, _ = run(ATL + "addCommentToJiraIssue",
            {"issueIdOrKey": "NS-12", "commentBody": "Scrubbed by W2-TSD-HYGIENE earlier."})
check("T4a codename W2-TSD-HYGIENE -> block", rc == 2)
rc, _ = run(ATL + "addCommentToJiraIssue",
            {"issueIdOrKey": "NS-12", "commentBody": "Handled under W2-WAVE2-TSD scope."})
check("T4b codename W2-WAVE2-TSD -> block", rc == 2)

# T5: read verb carrying a token in JQL -> allow (searching FOR a token is legitimate)
rc, _ = run(ATL + "searchJiraIssuesUsingJql",
            {"jql": 'text ~ "MCP" AND updated >= -9d', "maxResults": 50})
check("T5 read verb with token -> allow", rc == 0)

# T6: slack send with a product name -> block; slack search with token -> allow
rc, _ = run(SLACK + "slack_send_message",
            {"channel": "C123", "text": "Cortege finished the intake batch."})
check("T6a slack send Cortege -> block", rc == 2)
rc, _ = run(SLACK + "slack_search_messages", {"query": "MCP rollout"})
check("T6b slack search token -> allow", rc == 0)

# T7: lowercase common words and slash-less 'working' -> allow (case and boundary rules)
rc, _ = run(ATL + "createJiraIssue",
            {"summary": "recast the working group",
             "description": "The witness statement casts doubt; keep working on the crucible of ideas? No: lowercase passes."})
check("T7 lowercase common words -> allow", rc == 0)

# T8: Bash inline PUT to atlassian.net with an audit codename -> block
rc, err = run("Bash",
              {"command": 'curl -s -X PUT -H "Authorization: Basic $TOKEN_B64" '
                          '"$JIRA_BASE/rest/api/3/issue/NS-9?notifyUsers=false" '
                          '-d \'{"fields":{"description":"audit-2026-08-11 residual cleanup"}}\''})
check("T8 bash PUT audit codename -> block", rc == 2 and "audit-codename" in err)

# T9: Bash GET to atlassian.net with token in the URL -> allow (no write method)
rc, _ = run("Bash",
            {"command": 'curl -s -H "Authorization: Basic $TOKEN_B64" '
                        '"https://subaruofamerica.atlassian.net/rest/api/3/search/jql?jql=text%20~%20%22MCP%22"'})
check("T9 bash GET with token -> allow", rc == 0)

# T10: Bash with cd/source local clauses then a clean PUT -> allow (clauses stripped)
rc, _ = run("Bash",
            {"command": 'cd /Users/brien/Workspaces/Work/Consulting/Engagements/Subaru/working/jira-migration/scripts '
                        '&& source /Users/brien/.config/atlassian/soa.env && curl -s -X PUT '
                        '-H "Authorization: Basic $TOKEN_B64" -H "Content-Type: application/json" '
                        '"$JIRA_BASE/rest/api/3/issue/NS-9?notifyUsers=false" '
                        '-d \'{"fields":{"summary":"Release calendar alignment"}}\''})
check("T10 bash local clauses stripped -> allow", rc == 0)

# T11: Bash write that does NOT target a client surface -> allow even with tokens
rc, _ = run("Bash",
            {"command": 'git commit -m "sweep working/jira-migration for MCP references"'})
check("T11 non-client bash with tokens -> allow", rc == 0)

# T12: env bypass with a real reason -> allow and logged
before = len(log_lines())
rc, _ = run("Bash",
            {"command": 'curl -s -X PUT "$JIRA_BASE/rest/api/3/issue/NS-9" -d \'{"fields":{"description":"MCP"}}\''},
            env_extra={"CLIENT_CONTENT_LINT_BYPASSED": "1",
                       "CLIENT_CONTENT_LINT_REASON": "quoting client text that contains the term legitimately"})
check("T12 env bypass with reason -> allow", rc == 0)
check("T12 bypass logged", len(log_lines()) > before)

# T13: env bypass flag without an adequate reason -> block stands
rc, _ = run("Bash",
            {"command": 'curl -s -X PUT "$JIRA_BASE/rest/api/3/issue/NS-9" -d \'{"fields":{"description":"MCP"}}\''},
            env_extra={"CLIENT_CONTENT_LINT_BYPASSED": "1", "CLIENT_CONTENT_LINT_REASON": "because"})
check("T13 env bypass without reason -> block", rc == 2)

# T14: grant file with a real reason -> allow once, consumed, logged
with open(GRANT, "w") as fh:
    json.dump({"tool": ATL + "createJiraIssue",
               "reason": "client-facing text legitimately quotes the vendor connector name",
               "granted_at": time.time()}, fh)
before = len(log_lines())
rc, _ = run(ATL + "createJiraIssue",
            {"summary": "CRM integration", "description": "Enable the Salesforce connector for NS."})
check("T14 grant -> allow", rc == 0)
check("T14 grant consumed", not os.path.exists(GRANT))
check("T14 grant logged", len(log_lines()) > before)

# T15: grant with a too-short reason -> block stands
with open(GRANT, "w") as fh:
    json.dump({"tool": "*", "reason": "why", "granted_at": time.time()}, fh)
rc, _ = run(ATL + "createJiraIssue",
            {"summary": "x", "description": "Enable the Salesforce connector."})
check("T15 short-reason grant -> block", rc == 2)
os.path.exists(GRANT) and os.unlink(GRANT)

# T16: Confluence update naming a gate script -> block
rc, err = run(ATL + "updateConfluencePage",
              {"pageId": "123", "body": "Validated by check-canon-vs-live.py this morning."})
check("T16 confluence gate script -> block", rc == 2 and "script-name" in err)

# T17: Confluence create naming Claude -> block (AI-vendor extension of the signal list)
rc, _ = run(ATL + "createConfluencePage",
            {"spaceId": "9", "title": "Migration notes", "body": "Claude generated this summary."})
check("T17 Claude on client surface -> block", rc == 2)

# T18: tool outside the hook's surfaces -> allow even with tokens
rc, _ = run("mcp__foo__doThing", {"text": "MCP working/jira-migration Cortege"})
check("T18 foreign tool -> allow", rc == 0)

# T19: tokens file missing -> fail closed with a message naming the file
rc, err = run(ATL + "createJiraIssue", {"summary": "clean", "description": "clean"},
              env_extra={"CLIENT_CONTENT_LINT_TOKENS": os.path.join(TMP, "missing-tokens.json")})
check("T19 missing tokens file -> fail closed", rc == 2 and "tokens" in err.lower())

# T20: transition with an embedded comment token -> block (write verb, full-payload scan)
rc, _ = run(ATL + "transitionJiraIssue",
            {"issueIdOrKey": "NS-12", "transition": {"id": "31"},
             "fields": {"comment": "closing per canonical/decisions ruling"}})
check("T20 transition comment token -> block", rc == 2)

# T21: Bash python heredoc POST to atlassian.net with a workspace path -> block
rc, _ = run("Bash",
            {"command": 'python3 - <<\'EOF\'\nimport requests\nrequests.post('
                        '"https://subaruofamerica.atlassian.net/rest/api/3/issue", json={'
                        '"description": "per canonical/decisions/00-decision-journal.md"})\nEOF'})
check("T21 heredoc POST workspace path -> block", rc == 2)

# T22: internal register ids -> block
rc, _ = run(ATL + "addCommentToJiraIssue",
            {"issueIdOrKey": "NS-12", "commentBody": "This implements D-N145 as ruled."})
check("T22 register id D-N145 -> block", rc == 2)

# T23: malformed stdin -> allow (never break the harness on parse errors)
p = subprocess.run(["python3", HOOK], input="not json", env={**os.environ, "HOME": FAKE_HOME},
                   capture_output=True, text=True)
check("T23 malformed stdin -> allow", p.returncode == 0)

failures = [n for n, c in results if not c]
print(f"\n{len(results) - len(failures)}/{len(results)} passed")
sys.exit(1 if failures else 0)
