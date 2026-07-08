---
id: SIG-034
timestamp: 2026-05-19T17:30:00Z
source: conversation
confidence: 0.85
trust: 0.5
autonomy_level: L2
status: captured
cluster: null
author: brien
related_intents: []
referenced_by: []
parent_signal: SIG-033
---

# A fire-and-forget external contribution is an un-instrumented Observe phase

## Summary

theparlor authored `taylorwilsdon/google_workspace_mcp#768` (late-bind OAuth
callback port), opened the PR, and disengaged. Over the next 10 days and ~12
follow-up commits the maintainer carried it to merge alone. Reconstructing what
happened after disengagement yields a methodology lesson, not just a code one.

The core design survived unchanged — strong external validation. But:

1. **Quality gates not run before submit.** Repeated `ruff`/`pytest` commits +
   CodeRabbit flags (mypy-strict types, `PortConfigError` docstrings, exception
   chaining `from exc`, env-var precedence) = the patch didn't clear the repo's
   lint/type/test bar on arrival. Cheaply catchable locally; maintainer absorbed it.
2. **Problem framed issue-local, not system-local.** `"roll #790 into late bind
   fix"` — an adjacent failure mode in the same subsystem had to be folded in.
   We solved the three issues we cited and missed the one we didn't look for.
3. **Operability dimension missed.** Startup-logging / reuse-state refactors were
   needed because late-binding the port changed what operators see at startup and
   we changed behavior without updating the human-facing signal.
4. **Learning loop never closed.** Every tradeoff call after submit was the
   maintainer's. We have no first-hand record of *why* anything changed — only
   inferred from terse commit messages. The feedback never came back to us.

## Why it might matter

Intent's whole thesis is that Observe is a first-class product and double-loop
learning requires the feedback to actually return. An outbound contribution that
is opened and abandoned is an Observe phase with no instrumentation: the system
that reshaped our work is exactly the kind of signal source Intent exists to
capture, and we captured none of it. This generalizes to any agent- or
human-authored work that leaves our repo (PRs, issues, specs handed to others).

## Proposed: "definition of done" for outbound contributions

- Run the target repo's own lint / type / test gates locally before submitting.
- Scan adjacent open issues in the same subsystem; frame the fix system-local.
- Update operator-facing logging/docs when runtime behavior changes.
- Stay subscribed to the PR through merge so the learning loop closes — capture
  post-submit changes as Observe-phase signals (what changed, inferred why).

Note: the PR-activity subscription now active on `theparlor/intent#2` is exactly
the instrument that was missing on #768. The mechanism already exists; the gap
is making it part of the contribution protocol, not an ad-hoc afterthought.

## Trust Factors

- Clarity: high — concrete evidence (commit log + review feedback).
- Blast radius: low — a process/checklist change, opt-in, no runtime surface.
- Reversibility: high.
- Testability: medium — "did the contributor run gates / stay subscribed?" is
  observable but the value (better merges) is lagging.
- Precedent: low — no existing contribution protocol DDR.

## Triage, 2026-07-08

Disposition: still pending. Searched the repo for any written "definition of done" for outbound contributions (the four-item checklist this signal proposed: run target repo's own lint/type/test gates, scan adjacent issues, update operator-facing docs on behavior change, stay subscribed through merge); no CONTRIBUTING.md, no CLAUDE.md section, and no protocol doc encodes it. The one mechanism the signal called out as already existing, PR-activity subscription, is a session behavior, not a written protocol, so there is nothing to point to as the control. Needed control: write the outbound-contribution checklist into a durable doc (CLAUDE.md or a dedicated protocol file) so it survives past the session that produced this signal.
