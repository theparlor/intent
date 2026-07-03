---
id: DDR-009
title: Always-on hosting substrate is GitHub Actions now, with an explicit cloud trajectory
status: ratified
decided: 2026-07-03
decided_by: Brien (direct, in-session)
origin: human
supersedes: null
related_signals:
  - SIG-037 (2026-05-16-always-on-hosting-forcing-function.md)
  - SIG-2026-07-03-cross-session-awareness-ladder (Workspaces root .intent)
related_themes:
  - THM-005
---

# DDR-009: Always-on hosting substrate is GitHub Actions now, with an explicit cloud trajectory

## Context

Intent's deployment topology has had an unresolved load-bearing decision since at least
2026-05-16 (SIG-037, 48 days open at decision time): the processing pipeline, scheduled tasks,
and every L3/L4 autonomous-execution claim require a substrate that runs when the laptop is
closed or traveling. The 2026-07-03 cross-session-awareness work made the cost concrete: the
new witness-transcript-ingest preservation loop runs only while the desktop app is open, and
cron/launchd/scheduled-task reliability is structurally capped by laptop availability. Options
enumerated in CLAUDE.md since April: GitHub Actions, cloud service, dedicated machine.

## Decision

1. **GitHub Actions is the always-on substrate now.** Rationale (Brien, verbatim intent):
   it means the least amount of change because the system is already deep in git. Everything
   durable already lives in git repos (theparlor/*); Actions can run scheduled and event-driven
   jobs against those repos with no new infrastructure, no new auth model, and no new hosting
   relationship. Precedent already exists: intent-bot runs as GitHub Actions in theparlor/intent
   (reference_intent_repo_concurrency).
2. **An explicit trajectory to cloud is part of the decision, not a maybe.** Brien anticipates
   needing MCP space and cloud data space, benefits from placing applications in the cloud and
   reaching their functionality from anywhere, and intends to work with other developers. The
   Actions choice is the near-term substrate, chosen for delta-minimization, not the end state.
3. **Migration trigger conditions** (any one fires a fresh substrate DDR):
   - a second developer needs shared runtime access (not just repo access);
   - a workload exceeds the Actions execution model (long-running daemon, low-latency wake,
     job runtime beyond Actions limits);
   - an MCP server needs to be reachable from multiple clients/locations as a service.
4. **Partition axis adopted** (from SIG-037 proposed action 2): each pipeline stage gets
   classified on-demand vs must-be-always-on; only must-be-always-on stages migrate to Actions,
   on-demand stages stay local. First candidates to classify: witness-transcript-ingest,
   intake-drain, cast freshening nightly, the enrichment pipeline stages.

## Alternatives considered

- **Cloud service now.** Rejected for now: larger delta before it is needed; the multi-dev and
  MCP-space needs that justify it are anticipated, not present. Deliberately preserved as the
  named trajectory with trigger conditions above so this is a staging decision, not a rejection.
- **Dedicated machine.** Rejected: replaces one single point of availability (laptop) with
  another, plus hardware operations burden; no path to multi-dev collaboration.
- **Status quo (laptop-only).** Rejected: this is the condition that kept every L3/L4 always-on
  claim vapor for 48 days and gates the preservation loop shipped 2026-07-03.

## Consequences

- Scheduled work that must be reliable gets a git-reachable Actions expression; the app-open
  constraint on desktop scheduled tasks becomes a UX convenience layer, not the reliability layer.
- Secrets/credential handling moves into GitHub Actions secrets for any migrated stage;
  client-confidential content must NOT flow through Actions runners for NDA-scoped engagements
  without a per-engagement ruling (Work/ tree content stays out of Actions by default).
- The always-on partition classification becomes part of each product's operator doc.

## Validation criteria

- First migrated stage (recommend witness-transcript-ingest or intake-drain) runs on schedule
  for 14 consecutive days with the laptop's availability having no effect on run success.
- No NDA-scoped content appears in any Actions log or artifact (spot-audit after first 14 days).
- A fresh substrate DDR is written within one week of any migration trigger condition firing.
