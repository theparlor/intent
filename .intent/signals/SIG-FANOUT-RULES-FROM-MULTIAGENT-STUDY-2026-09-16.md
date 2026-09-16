---
id: SIG-FANOUT-RULES-FROM-MULTIAGENT-STUDY-2026-09-16
title: "Fan-out rules now ship with the dispatch template instead of living in five memory notes, and Formation Flight gains a third crash mode"
type: signal
kind: decision
status: resolved
severity: medium
confidence: high
created: 2026-09-16
discovered_by: host-pickup wave, intake issue 43
scope: intent framework, subagent dispatch
affects:
  - /Users/brien/Workspaces/Core/frameworks/intent/knowledge-engine/templates/subagent-dispatch-prompt.md
  - /Users/brien/Workspaces/Core/frameworks/intent/spec/autonomy-flight-model-v1-DRAFT.md
  - /Users/brien/Workspaces/Core/frameworks/intent/spec/SPEC-INTENT-FORMATION-FLIGHT-001.md
related:
  - https://github.com/theparlor/intake/issues/43
  - SIG-COH-EXT-MULTIAGENT-PAPER-2026-09-16
lineage:
  - https://github.com/theparlor/intake/issues/43
upstream_control_path: "/Users/brien/Workspaces/Core/frameworks/intent/knowledge-engine/templates/subagent-dispatch-prompt.md section 'Fan-out rules (if this task dispatches further)', inside the copy-paste template body. Every brief built from the template carries the nine rules; the rationale and the evidence table sit outside the fence for whoever edits the template later. Previously these rules existed only as five separate memory notes, each of which fires only when a session happens to load it."
catch_mechanism: "Rule 6 inside the template requires a replayable verification_command in every child brief and requires the parent to replay it, so a claim-without-execution is detectable by replay rather than by trust. That is the catch for the specific failure class (see feedback_subagent_claim_vs_execute). The Layer 5 dispatch-prompt hook at /Users/brien/Workspaces/Core/frameworks/intent/hooks/autonomy-grant-dispatch-prompt-check.sh inspects every Agent dispatch before it fires but does NOT yet assert that the fan-out section is present. That assertion is queued, not built, and is named as a gap rather than claimed."
verification_command: "grep -c 'Fan-out rules (if this task dispatches further)' /Users/brien/Workspaces/Core/frameworks/intent/knowledge-engine/templates/subagent-dispatch-prompt.md && grep -c 'A third crash mode: formation conformity' /Users/brien/Workspaces/Core/frameworks/intent/spec/SPEC-INTENT-FORMATION-FLIGHT-001.md"
---

# What changed and why anyone should care

**In plain language.** When Brien fans work out to a group of agents, the brief he hands them
is copied from one template file. That template told each agent how much authority it had and
how to report honestly. It said nothing about how a group of agents fails as a group.

An external study published 2026-08-13 measured exactly that, at up to eighty agents, and every
failure it names has already happened in this workspace. Nine rules now sit in the template,
each with the evidence behind it and the local incident it repairs. Anyone who writes a brief
from the template gets them without reading anything else.

**The substantive addition to canon:** Formation Flight (SPEC-INTENT-FORMATION-FLIGHT-001)
named two formation crash modes, mid-air collision and formation breakup. There is a third, and
the spec's own detectors are blind to it: **formation conformity**, where every agent makes the
same wrong decision because every agent is the same agent. Collision detectors see no overlap.
Breakup detectors see a perfectly shared frame. Every instrument reads airworthy. The formation
is coherently wrong. Section 3a of that spec now names it, gives the external and local
evidence, and states plainly that no detector exists yet, with the two candidate designs.

**The correction to the autonomy model:** model tier is not a proxy for earned trust in either
direction, because the study shows prosociality is orthogonal to capability and that stronger
models take forceful action sooner. Recorded as an additive subsection under the ratified
lambda-scoping convention, which it does not amend.

**Residual.** No hook asserts that a dispatch brief carries the fan-out section, so a brief
written from memory rather than from the template still skips them. No detector exists for
formation conformity. Both are named here rather than papered over.
