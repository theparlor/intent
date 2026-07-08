---
id: SIG-049
timestamp: 2026-04-09T04:46:00Z
source: agent-trace
confidence: 0.9
trust: 0.7
autonomy_level: L2
status: resolved
cluster: methodology-gaps
author: panel-review-2026-04-09
related_intents: []
referenced_by: []
parent_signal:
upstream_control_path: ".intent/methodology/psychological-safety/02-safety-contract-v1.md"
catch_mechanism: "The Psychological Safety Contract exists with nine promises (plus Promise 10) covering every required outcome named here: Promise 1 (trust scores are about the artifact, not the person), Promise 2 (scoped signal visibility), Promise 3 (appeal surface with trust-appeal/spec-critique-appeal/panel-review-appeal signal types), Promise 5 (accountability routing), Promise 6 (disagreement is protected), Promise 9 (cultures that cannot honor the contract must not adopt Intent)"
verification_command: "grep -c '^### Promise' /Users/brien/Workspaces/Core/frameworks/intent/.intent/methodology/psychological-safety/02-safety-contract-v1.md"
---
# Psychological safety is the biggest latent failure mode — Org Design panel (sole owner, critical)

The Organizational Design review panel (Edmondson voice dominant) was the only panel to flag this, but they flagged it as the biggest latent failure mode in the entire methodology. The site never addresses psychological safety once.

Direct quote: *"Intent is built by engineers for engineers and treats safety as emergent. It isn't. Trust scoring is literally a scoring system applied to humans' clarity. If my specs keep scoring L1, am I the bottleneck? Signals capture friction with attribution — in a low-trust org this is a dossier mechanism. Who sees my signals? Can my manager read what I noticed? This is a performance-management shadow system waiting to happen."*

## Why this matters

- Every other methodology adoption failure traces back to psych safety (Edmondson's 20 years of research)
- Trust scoring is the most dangerous surface — it looks like math but becomes performance evaluation
- Signals-with-attribution in a low-trust org becomes a dossier
- This is NOT a content fix. It's a methodology fix that requires new policy and enforcement

## Required outcome

- New page: Psychological Safety Contract
- Explicit statements: who sees signals, what trust scores are NOT used for (performance reviews), how disagreeing with a spec is protected, how agent-output accountability is assigned
- Agents reviewing specs must cite the contract when scoring clarity
- Trust scores must carry provenance (who scored what, when, why)
- L3/L4 autonomy decisions must have an appeal surface

## Dependency on other signals

- Gates team pilot readiness (SIG-043 discovery interviews will surface which orgs have the safety to adopt and which don't)
- Inputs to double-loop learning (SIG-050) — questioning the scoring mechanism itself is double-loop
- Relates to operator persona (SIG-048) — operator persona should include "how I handle disagreement"

## Trust Factors

- Clarity: 0.9 (Edmondson's research is extensive; panel was specific)
- Blast radius: 0.7 (affects methodology, not just site — high)
- Reversibility: 0.6 (contract changes are policy changes)
- Testability: 0.5 (psych safety is measurable but not easily)
- Precedent: 1.0 (Fearless Organization, Amy Edmondson)

## Triage, 2026-07-08

Disposition: control exists now. The Org Design panel's single-owner warning got a full policy document, not a token gesture: the safety contract names who sees signals, states trust scores are not performance evaluation, protects disagreement, and gives autonomy decisions an appeal path. The contract's own "Open questions and uncertainties" section honestly flags residual risk (for example, self-attribution incentives in Promise 4's failure classification) rather than claiming the problem is fully solved, which matches this signal's own standard for what a real fix looks like.
