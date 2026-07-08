---
id: SIG-033
timestamp: 2026-05-19T17:00:00Z
source: conversation
confidence: 0.9
trust: 0.35
autonomy_level: L1
status: captured
cluster: null
author: brien
related_intents: []
referenced_by: []
parent_signal: null
---

# Remote-control sessions can't reach GitHub repos outside a hardcoded session allowlist

## Summary

While working a remote-control (Claude Code on the web) session in `theparlor/intent`,
Brien asked the agent to inspect an upstream PR — `taylorwilsdon/google_workspace_mcp#768`
— that theparlor authored. The GitHub MCP server refused:

> `Access denied: repository "taylorwilsdon/google_workspace_mcp" is not configured
> for this session. Allowed repositories: theparlor/intent`

The block is **not** a token-permission issue (the running theory was the recent shift
to a fine-grained token). It is a **session-level repo allowlist** baked into the
remote execution environment at creation time. The agent fell back to public WebFetch
to answer the question, which works for public repos but is read-only, unauthenticated,
loses API fidelity (no review threads, no check runs, no diff API), and fails entirely
for private repos.

## Why it might matter

The point of remote control is that Brien can direct agent work from anywhere — phone,
travel, offline laptop. A central premise of the Intent deployment topology (hosted /
always-on processing for travel) is that the agent can act across Brien's whole surface,
not one repo. A per-session hardcoded allowlist breaks that premise: Brien cannot, by
remote control, ask the agent to triage an upstream issue, check CI on a sibling repo,
or cross-reference a contribution — exactly the multi-repo practitioner workflow Intent
is meant to support. Brien explicitly flagged he is "not convinced our MCP is configured
too tightly" and wants this captured rather than fixed blind.

## Evidence

- Session env scoped to `theparlor/intent` only (system config, not token scope).
- `mcp__github__pull_request_read` on `taylorwilsdon/google_workspace_mcp` → access denied.
- WebFetch fallback succeeded for the public PR but could not retrieve CodeRabbit review
  threads or check-run detail (would have needed the authenticated API).

## Open questions (for triage, not auto-resolution)

1. Should remote-control environments allow a configurable multi-repo allowlist
   (e.g. all repos under `theparlor/*` plus explicitly-added upstreams)?
2. Is the right control a per-session prompt-to-add-repo, a standing config in
   `.intent/config.yml`, or an environment-creation parameter?
3. Security boundary: a remote agent that can reach *any* repo Brien can touch is a
   real blast-radius increase. The allowlist may be deliberate. This needs a decision,
   not a silent widening.

## Trust Factors

- Clarity: high — the failure and its cause are unambiguous and reproduced.
- Blast radius: medium-high — widening repo scope for a remote agent expands what an
  autonomous/compromised session can reach across Brien's GitHub.
- Reversibility: high — allowlist config is trivially revertible.
- Testability: high — "ask for an out-of-scope repo, observe allow/deny" is a clean test.
- Precedent: low — no prior DDR on remote-control repo scoping; needs a decision.

## Triage, 2026-07-08

Disposition: still pending, correctly so, this signal explicitly marks its own open questions as "for triage, not auto-resolution" and flags a real security-boundary tradeoff (widening what a remote/compromised session can reach). Checked .intent/config.yml and .intent/config/ for any multi-repo allowlist schema; none exists. No DDR or PENDING_DECISIONS.md row addresses remote-control repo scoping. Needed control: this is a genuine Brien-gated decision (blast radius, medium-high; precedent, none). Registering as tracked-pending rather than resolving unilaterally, consistent with the signal's own instruction not to auto-resolve.
