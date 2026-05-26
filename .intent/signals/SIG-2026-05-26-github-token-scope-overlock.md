---
id: SIG-2026-05-26-github-token-scope-overlock
timestamp: 2026-05-26T02:18:36Z
date: 2026-05-26
source: conversation
confidence: 0.9
trust: 0.5
autonomy_level: L2
status: captured
cluster:
author: brien
related_intents: []
referenced_by: []
parent_signal:
type: governance-friction
severity: high
---

# GitHub fine-grained token over-scoped — remote sessions starved of cross-repo context

## Observation

The fine-grained GitHub token wired into the Claude Code remote execution
environment is currently scoped to a single repo (`theparlor/intent`). In
this session, the user asked "why did we fork google_workspace_mcp and
what's ours vs. the original?" — a question that requires reading at least
one other `theparlor/*` repo. The agent could not answer; the repo isn't
cloned into the ephemeral container and isn't reachable through the GitHub
MCP either.

User's framing: *"This relates to us unintentionally over locking down
everything in this space and now it is almost without value or use."*

The Intent workspace is cross-repo by nature (intent + intent-site +
forked MCP servers + engagement repos + knowledge farms). A single-repo
token reduces remote sessions to local-file Q&A and breaks the value
proposition of having an always-on agent that can reason across the org.

## Decided direction

Invert the model: **blacklist (exclude specific repos) rather than
whitelist (include specific repos).**

Rationale: the default-shape of the Workspaces is "agent can see
everything"; the exceptions are sensitive engagements (client NDA repos,
credentials repos, anything with raw PII). Whitelisting forces an
enumeration that's always behind reality — every new repo silently
removes capability until someone remembers to add it.

## Risks of the blacklist approach

### R1 — Default-allow on new repos (the asymmetric failure)
The whole point of whitelisting is *fail-closed*: a new repo is invisible
until someone opts it in. Blacklisting *fails-open*: a new repo is
readable/writable by every remote session until someone opts it out. If a
sensitive repo gets created and nobody adds it to the blacklist that day,
its contents are exposed for the gap. This is the dominant risk.

Mitigation: naming-convention guard + creation-time hook. Any new repo
matching `*-client-*`, `*-engagement-*`, `*-private-*`, `secrets-*`,
`*-credentials` is auto-added to the blacklist by a GitHub Action or org
hook. Belt-and-suspenders: the blacklist file lives in `intent` and is
reviewed weekly via lint.

### R2 — Token blast radius widens with each new capability
A fine-grained token with `contents:write` + `pull_requests:write` +
`issues:write` across most of `theparlor/*` means a prompt injection or
hijacked session can rewrite/delete content across the org. Today's
single-repo scope limits the blast radius to one repo's history; the
inverted model limits it to (org − blacklist) repos.

Mitigation: split tokens by *permission tier*, not just by repo.
- Token A (broad read, narrow write): read across the inverted scope,
  write only to `intent` + repos the session explicitly registered for.
- Token B (write-elevated): only created on-demand for a specific repo
  for a specific session, with a TTL.

This makes the "I can read everything to answer questions" capability
cheap and the "I can mutate everything" capability rare.

### R3 — Secret exposure via repo contents (not just repo metadata)
Even read-only access to the inverted scope means an agent (or a prompt
injection inside source it reads) can exfiltrate `.env` files, API keys
committed by mistake, or PII inside knowledge farms. Whitelisting kept
this contained to one repo; blacklisting expands it to most of the org.

Mitigation: secret-scanning pre-commit hooks in every repo (already
partially in place per the 9e14ee2 commit message — "Pre-flight secret
scan: clean"). Push the standard up and make it a contract that gates
inclusion in the inverted scope.

### R4 — Audit gap on cross-repo writes
With single-repo scope, every write the agent makes is in `intent`'s git
history, which the user reviews. Inverting the model means writes can
land in repos the user doesn't habitually review. Drift, autonomous
commits, or hallucinated edits in low-attention repos can persist
unnoticed.

Mitigation: emit a `git_push` event to `intent/.intent/events/events.jsonl`
for every push the agent makes to any `theparlor/*` repo, with repo +
branch + commit SHA. Single audit trail across the inverted scope. The
existing `event: emit events for intent file changes` pattern generalizes.

### R5 — Supply-chain / fork drift
If forked tooling (google_workspace_mcp, etc.) is inside the inverted
scope and an agent can write to it, an unintended commit could diverge
the fork from upstream in a way that's hard to recover from. Whitelisting
incidentally protected forks by excluding them.

Mitigation: forked repos go on the blacklist *for write*, stay in scope
*for read*. The permission-tier split (R2 mitigation) handles this
cleanly.

### R6 — Compliance / NDA leakage across engagement boundaries
Brien's consulting engagements (Subaru, ASA, F&G, Cargill, Footlocker)
have NDA terms that may forbid the engagement's contents from being
processed by tooling outside the engagement's scope. An inverted-scope
agent that can read all engagement repos at once could constitute a
contractual breach even if no exfiltration occurs, by virtue of being a
single process with cross-engagement read access.

Mitigation: engagement repos are *never* on the inverted scope. They are
per-engagement tokens, per-engagement sessions, redaction enforced at the
MCP tool level (already a decided architecture — see Decision #18,
"Redaction at tool level"). The blacklist must explicitly enumerate every
engagement repo, and the lint that maintains it must treat
"engagement repo not on blacklist" as a critical violation.

## Risk summary

| Risk | Severity | Asymmetry | Mitigation cost |
|------|----------|-----------|-----------------|
| R1 default-allow on new repos | High | New repo silently exposed | Low (naming hook) |
| R2 widened blast radius | High | Mutation across org | Medium (token split) |
| R3 secret exposure via contents | Medium | Per-repo hygiene matters | Medium (org-wide secret scan) |
| R4 audit gap on cross-repo writes | Medium | Drift in low-attention repos | Low (event emission) |
| R5 fork drift | Medium | Hard-to-recover upstream divergence | Low (write blacklist on forks) |
| R6 NDA leakage across engagements | Critical | Contractual breach without exfil | High (per-engagement tokens) |

R1 and R6 are the dominant risks. R1 because it's the structural
weakness of the blacklist model itself; R6 because it can convert a
configuration miss into a contractual liability.

## Recommended posture

Adopt the inversion (blacklist) for the *read* tier so remote sessions
recover their cross-repo value. Keep *write* on the whitelist model with
on-demand TTL elevation. Enforce both via:

1. A blacklist file in `intent/.intent/config/github-token-scope.yml`
   that is the source of truth.
2. A creation-time GitHub Action that auto-blacklists any new repo
   matching engagement/client/credential patterns.
3. A weekly lint that compares the blacklist against the live org
   contents and flags any repo not yet classified.
4. A per-push event emitted to `events.jsonl` for any write outside
   `intent`.

This recovers the agent's value as a cross-repo reasoner while keeping
mutation and engagement-bounded data on a tighter leash.

## Trust Factors

- Clarity: 0.7 — the friction is concrete (this session demonstrates it); the inversion direction is decided; the risk surface is enumerable
- Blast radius: high — token scope changes affect every remote session and every repo in the org
- Reversibility: medium — token scope can be re-tightened, but data already read cannot be unread
- Testability: medium — can dry-run the blacklist against the live org and check coverage
- Precedent: low — this is the first inversion of the access model; no prior decision to lean on

## Open

- Where does the blacklist live? `.intent/config/github-token-scope.yml`
  is the natural home; needs schema.
- Who owns the creation-time hook? GitHub Action in `intent` repo
  watching for `repository.created` webhook on the org.
- TTL mechanism for elevated write tokens — GitHub doesn't natively do
  this; needs a wrapper.
- First blacklist entries: enumerate current engagement repos
  (Subaru/ASA/F&G/Cargill/Footlocker) + any credential repos.
