---
signal_id: SIG-2026-09-26-change-carries-its-own-verification-plan
title: "Cursor Rollouts ships the pattern Intent lacks: a change writes its own verification plan up front, and the later verdict can be 'inconclusive'"
type: signal
kind: observation
status: open
date: 2026-09-26
created: 2026-09-26
confidence: medium
severity: low
discovered_by: intake drain, 2026-09-26
lineage: theparlor/intake#77
source: https://thenewstack.io/cursor-rollouts-firetiger-production/
related:
  - https://github.com/theparlor/intake/issues/77
  - /Users/brien/Workspaces/Core/frameworks/intent/spec/typed-evaluation-verdicts.md
  - /Users/brien/Workspaces/Core/frameworks/intent/.intent/signals/SIG-VERIFIER-COMPOSITION-RULE-2026-09-16.md
---

# A change carries its own verification plan

## What was noticed

Brien captured The New Stack's 2026-09-24 piece on Cursor Rollouts (built from the Firetiger acquisition) with the ask "can we use or relocate." The product needs Cursor Teams or Enterprise plus live deploy telemetry, so using it is lab stage 0 (Noticed) until a repo with real deploys exists. The pattern is what relocates.

How Rollouts works, in two moments:

1. **When the change is proposed** (PR open), an agent reads the diff and writes a monitoring plan: intended behavior, risks, the signals to watch, and the gaps in instrumentation. A human can edit the plan before merge.
2. **After the change lands** (each deploy, staging and prod judged separately), it compares telemetry to that plan and returns one of three verdicts: verified healthy, regression detected, or **inconclusive**. On regression it names the suspect change and can open a revert PR for review; it never merges or rolls back by itself.

## Why it matters to Intent

- **Plan written by the change, before the outcome.** Intent's Spec step names acceptance, but nothing asks a change to state, before it runs, which signals would show it working and which it cannot see. That is the Notice to Observe link made explicit per change.
- **"Inconclusive" as a first-class verdict.** `spec/typed-evaluation-verdicts.md` types who authored the criteria, but its outcome space is pass or fail. A verdict of "we could not tell" is currently forced into one or the other; the SIG-VERIFIER-COMPOSITION-RULE gap (strict AND over verdicts) gets worse when an unknown is silently read as a pass.
- **Instrumentation gaps as a named output.** A plan that lists what it cannot observe is a catch-net for itself: the gap becomes a record, not an absence.
- **Plan-then-verdict fits the intake drain too.** Each triaged issue could carry "what would prove this routing right" in its receipt, checked at close.

## Candidate moves (not decisions)

- Add `inconclusive` to the verdict outcome space in typed-evaluation-verdicts.md, with the consumption rule that it never closes a spec.
- Add an optional `verification_plan` block (signals to watch, instrumentation gaps) to the Spec template, checked at Observe.
- Compare Cursor's Bot Development Kit (`@cursor/bdk`, agents defined in Markdown plus TypeScript with tools, skills, subagents, webhooks, schedules) to Claude Code skills and subagents as a harness shape.

## By the record

Other facts in the source: shipped with an upgraded Security Reviewer bot (review time reported down about 21 percent, comment acceptance up from roughly 45 to 50 percent to 60 to 70 percent); works with GitHub or Cursor's Origin forge; competitive set named as Datadog Bits Release, Harness deployment verification, LaunchDarkly Guarded Rollouts, Zed Delta. Vendor-reported numbers, unverified.
