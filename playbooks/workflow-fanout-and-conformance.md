---
title: Workflow Fan-out and Conformance Authoring Guide
id: PLAYBOOK-WORKFLOW-FANOUT-CONFORMANCE-001
type: playbook
maturity: active
confidentiality: internal
reusability: universal
created: 2026-07-08
updated: 2026-07-08
owner: brien
origin_signals: [SIG-2026-07-02-repo-hygiene-fanout-rate-limit, SIG-2026-07-06-workflow-fanout-burst-throttle, SIG-2026-07-07-workflow-file-conformance-gap, SIG-2026-07-07-workflow-args-not-threading]
upstream_control_path: "Core/frameworks/intent/playbooks/workflow-fanout-and-conformance.md (this file, mandatory-embed authoring guidance) + Core/products/cortege/components/bidirectional-pacing-rail.md (pacing design) + Core/reference/competitive-intel/wave-runner.reference.js (pacing reference impl) + Core/frameworks/intent/tools/conform_file.py (conformance checker)"
catch_mechanism: "Core/frameworks/intent/learnings/process-drift-catalog.md Family 5 (5.1-5.3) names these as recognized drift patterns with this playbook as prevention; the reference implementation Core/reference/competitive-intel/evaluate-entrants.workflow.js carries a live Conformance phase as the worked example any new workflow copies"
pipeline_survival: "Partial by design. The pacing rail and conform_file.py are real code, not prompt text, and survive across sessions. What does NOT yet survive automatically: nothing forces a NEW *.workflow.js to copy this pattern -- there is no lint that fails a workflow file missing a Conformance phase or an unpaced fan-out. Per the hooks/lexical-layer-freeze.yaml precedent, the correct place for that enforcement is an in-orchestrator check (like the formation-flight two-stage gate), not a new Stop/PreToolUse hook -- that is the honest remaining gap, named here rather than silently left."
---

# Workflow Fan-out and Conformance Authoring Guide

> Read this before writing (or reviewing) any `*.workflow.js` file that fans out more than one agent, or
> that has any agent write a shareable markdown file. Three incidents in one week (2026-07-02, 2026-07-06,
> 2026-07-07) trace to the same root shape: a rule existed only as a prompt instruction or a habit, not as
> code the next author automatically inherits. This doc is the inheritance point.

## 1. Fan-out pacing is mandatory, not optional

**The problem.** Two independent runs (SIG-2026-07-02, SIG-2026-07-06) tripped Anthropic's server-side
rate-limiter by dispatching agents in one unpaced burst (14-30 agents once; 23 agents once). The second was
a direct recurrence of the first through a different vehicle (the Workflow tool instead of hand-dispatched
background agents) -- proof the first fix never became a structural control, only a one-off repair.

**The control.** The bidirectional pacing rail is built and dogfooded:
- Design + algorithm: `Core/products/cortege/components/bidirectional-pacing-rail.md`
- Copy-paste reference implementation (workflow scripts cannot `import`):
  `Core/reference/competitive-intel/wave-runner.reference.js`
- Working example wired end-to-end: `Core/reference/competitive-intel/evaluate-entrants.workflow.js`

**The rule.** Any `*.workflow.js` that calls `parallel(...)` or `pipeline(...)` with more than 2-3 items
MUST embed the `runWaves()` governor (copy the function body from `wave-runner.reference.js`) and drive
dispatch through it, instead of calling `parallel()` directly on the full item list. Defaults: `startWave:
3, maxWave: 6`; tighten on any wave with a null-ratio >= 0.5, loosen by 1 on a fully clean wave. Emit a
`cortege.pacing@v1` event per state transition (schema:
`Core/products/witness/engine/schema/event-types/cortege.pacing@v1.yaml`) and return the `pace_events`
array to the caller so it can be persisted.

**Also mandatory:** every agent dispatch prompt in a fan-out includes the line "Do NOT spawn nested
agents; do your own work in your own context." Nested self-spawn is what multiplied concurrency past the
rail's own wave size in the original 2026-07-02 incident.

**Honest gap.** Nothing yet fails a new workflow file that skips this pattern. The correct home for that
enforcement is an in-orchestrator check (see `Core/frameworks/intent/formation/README.md`'s two-stage
gate for the precedent), not a new Stop/PreToolUse hook -- `hooks/lexical-layer-freeze.yaml` froze that
layer on 2026-05-29 precisely because lexical checks accrete faster than they converge. Until a formation-
style gate exists for workflow authoring, this playbook plus the reference implementation are the control.

## 2. Every file a subagent writes needs a Conformance pass

**The problem.** Subagent `Write`/`Edit` calls do not pass through the Stop hooks
(`emdash-stop-check.sh`, link-format checks) that enforce glyph and path conformance on conversational
responses. A `STYLE` line in the dispatch prompt ("never use em-dashes...") is best-effort, not
enforcement -- SIG-2026-07-07-workflow-file-conformance-gap found a leaked em-dash despite an explicit
STYLE rule already in the prompt.

**The control.** `Core/frameworks/intent/tools/conform_file.py` -- a standalone, stdlib-only checker:
- `conform_file.py <path> --check` exits 1 if it finds a banned glyph (em-dash, en-dash, ellipsis, arrow
  glyphs) or a placeholder date (`: undated` or a `-undated` filename).
- `conform_file.py <path> --fix` auto-replaces glyphs in place; date placeholders are never auto-fixed
  (they need a real date, which only run context supplies) -- it still exits 1 so the caller notices.

**The rule.** Every `*.workflow.js` phase that writes markdown files MUST be followed by a **Conformance**
phase: one paced agent dispatch per written file (or a small batch), instructing the agent to run
`conform_file.py <path> --fix` via Bash, apply any residual date fix by hand (replace `: undated` with the
run's real date), and report `clean: true/false`. See the `Conformance` phase in
`evaluate-entrants.workflow.js` for the exact prompt shape to copy.

**Do not** rely on a STYLE-line instruction alone and call it done -- that is exactly the failure mode
this control replaces. The Conformance phase is a real tool-calling agent turn, not a hope.

## 3. Workflow `args` cannot be trusted for load-bearing values (upstream bug, not fixable here)

**The problem.** SIG-2026-07-07-workflow-args-not-threading: across three runs, `args: {date: '...'}`
passed to the Workflow tool did not reach the script's `args` global. Every run silently wrote `undated`
into frontmatter, `accessed:` fields, and filenames. This is a harness-level defect in the Workflow tool
itself -- nothing in this repo can fix why `args` fails to thread.

**The workaround (documented, not a fake fix).**
1. Prefer a loud, obviously-wrong fallback over a plausible-looking one:
   `const DATE = (args && args.date) || 'undated'` -- never default to a guessed real-looking date.
   `'undated'` is deliberately the sentinel the Conformance phase (Section 2) is built to catch.
2. When a script is being fired for a specific one-off run and you can confirm the date at authoring
   time, hardcode the literal instead of trusting `args` at all -- see
   `Core/reference/competitive-intel/queue-2026-07-08/tier3-peer-dossiers.workflow.js` for the pattern:
   `const DATE = '2026-07-08'` with a comment citing this signal.
3. Before relying on any other `args.<field>` for a load-bearing value (output paths, schema-required
   fields), treat it as unverified until you have confirmed in a real run that it threads. Bake load-
   bearing values into the script body when in doubt.

**Status:** this signal stays open against the upstream Workflow-tool defect. The workaround above plus
the Conformance-phase backstop is the honest, available mitigation -- not a claim that the root cause is
fixed.

## Checklist for any new `*.workflow.js`

- [ ] Any `parallel()`/`pipeline()` fan-out over >2-3 items goes through `runWaves()` (Section 1)
- [ ] Every agent dispatch prompt says "do NOT spawn nested agents"
- [ ] Every phase that writes files has a following Conformance phase (Section 2)
- [ ] Any load-bearing value that should come from `args` has a loud fallback or a hardcoded literal
      (Section 3), never a silently-plausible guess
- [ ] `pace_events` (and, once available, conformance results) are returned so the caller can persist them
