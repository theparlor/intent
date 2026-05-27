---
spec_id: SPEC-NATIVE-CONNECTOR-PRECEDENCE
title: Native-Connector Precedence Enforcement
status: ratified
created: 2026-05-27
related:
  - SIG-2026-05-27-native-connector-precedence-hook-gap
  - memory/feedback_prefer_native_anthropic_connectors.md
  - Core/frameworks/intent/spec/autonomy-grant-enforcement.md (mechanism-pattern reference)
  - Core/frameworks/intent/spec/closure-discipline-enforcement.md (mechanism-pattern reference)
authority:
  upstream_control: Core/frameworks/intent/hooks/native-connector-precedence-check.sh
  lookup_table: Core/frameworks/intent/hooks/native-connector-precedence-map.json
  registration: ~/.claude/settings.json (hooks.PreToolUse matcher='mcp__google-workspace__.*')
---

# SPEC: Native-Connector Precedence Enforcement

## Problem

Anthropic provides native MCP connectors for Gmail, Calendar, and Drive. Brien also has `google_workspace_mcp` (taylorwilsdon fork at `theparlor/google_workspace_mcp`) installed as a richer-featured Google Workspace MCP server running locally on `localhost:8001`.

The two have **separate authentication lifecycles**. When workspace-mcp's OAuth token lapses (it has done so multiple times), the agent receives `auth-required` errors that look like genuine service outages but aren't — the Anthropic-native connectors stay healthy throughout.

The 2026-05-27 `/overwatch` sweep demonstrated the catch-net gap concretely: I reached for `mcp__google-workspace__*` tools first, surfaced a false CRITICAL "Google auth invalidated" finding, and was about to ask Brien to re-OAuth. Memory `feedback_prefer_native_anthropic_connectors.md` (written 08:21 ET that morning, in-context at sweep time) failed to override the explicit-tool instruction in the `/overwatch` skill's Section 5.

## Resolution principle

**Memory is a catch-net, not upstream control.** When memory + skill-prompt + spec all fail to redirect tool-picking, the mechanism-level fix is a hook that intercepts the call itself.

This follows the established pattern from:
- `autonomy-grant-enforcement.md` — when proposal-framing drift persisted despite memory + skill reinforcement, a Stop hook closed the gap.
- `closure-discipline-enforcement.md` — when closure-claim drift persisted, a Stop hook closed the gap.

## Mechanism

A `PreToolUse` hook intercepts every tool call matching `mcp__google-workspace__.*` and:

1. Looks up the tool name in `native-connector-precedence-map.json`.
2. If the tool is in `blocked_with_native_equivalent`: exits with code 2 (block + show stderr message), directing the agent to the named native verb.
3. If the tool is in `fallback_allowed` (legitimate workspace-mcp-only capabilities — Docs editing, Sheets ops, Gmail filters, batch ops, Calendar advanced features): exits 0 (allow).
4. If the tool name is unknown (new workspace-mcp verb not yet classified): warns to stderr and exits 0 (fail open). Logs the unknown verb so the map can be updated.

## Lookup table maintenance

`native-connector-precedence-map.json` has three sections:

- `_meta.native_prefixes` — UUID-prefixed identifiers for Gmail / Calendar / Drive native connectors.
- `blocked_with_native_equivalent` — workspace-mcp verbs that DO have native equivalents. Each entry has `native_prefix` (gmail/calendar/drive), `native_verb`, and `note`.
- `fallback_allowed.verbs` — workspace-mcp verbs that have NO native equivalent and are legitimate fallback use.

When a new workspace-mcp tool is added or the native connectors gain a new verb, the map MUST be updated. The hook's "unknown verb" path logs to `~/.claude/logs/native-connector-warnings.log` for periodic review.

## Bypass

Set `NATIVE_CONNECTOR_PRECEDENCE_BYPASSED=1` in the environment of the tool call. Bypasses are logged to `~/.claude/logs/native-connector-bypass.log` with timestamp and session ID. Reviewing this log surfaces drift — if bypasses accumulate, the map may be wrong (missing fallback entries) or the precedence rule itself may need reconsidering for a class of operations.

## Closure DoD

This spec is ratified once:
- [x] Hook script exists at `Core/frameworks/intent/hooks/native-connector-precedence-check.sh`
- [x] Lookup map exists at `Core/frameworks/intent/hooks/native-connector-precedence-map.json`
- [x] Both symlinked to `~/.claude/hooks/`
- [x] Hook registered in `~/.claude/settings.json` under `hooks.PreToolUse` with matcher `mcp__google-workspace__.*`
- [x] Test cases pass: blocked / fallback / non-workspace / bypass / unknown / native / empty-stdin (all 7 verified 2026-05-27)
- [x] Install script updated to deploy this hook alongside the others
- [x] This spec document committed alongside the hook

## Cross-cutting consequences

- `/overwatch` Section 5 (already updated this session) now lists native-first probe order with the fallback explicitly secondary.
- `feedback_prefer_native_anthropic_connectors.md` memory remains as the agent-readable rule but is now CATCH-NET, not upstream control.
- `reference_mcp_config.md` and `feedback_google_workspace_mcp_removed.md` should reference this spec when next edited.

## Upstream control declaration

- **upstream_control_path:** `Core/frameworks/intent/hooks/native-connector-precedence-check.sh`
- **catch_mechanism:** PreToolUse hook with regex matcher `mcp__google-workspace__.*` blocking exit code 2
- **pipeline_survival:** survives because the hook fires on every tool call regardless of skill/prompt context; no render_all or session restart can wipe it (hook registration is in settings.json, lookup table is in the Core/ source tree symlinked into ~/.claude/hooks/)
