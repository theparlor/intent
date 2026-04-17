---
id: SIG-034
timestamp: 2026-04-13T01:30:00Z
source: research-synthesis
confidence: 0.85
trust: 0.7
autonomy_level: L2
status: resolved
cluster: methodology-adoption
author: agent
related_intents: []
referenced_by:
  - SIG-032
parent_signal: SIG-032
---
# Trust scoring is Boyd's orientation quality proxy — formalize this mapping

Chet Richards' analysis of Boyd's OODA (Necesse 2020) reveals that the Implicit Guidance & Control (IG&C) bypass — Orient directly to Act, skipping Decide — only works when orientation is accurate AND shared. Wrong orientation + IG&C = fast, confident, wrong actions.

**Intent's trust score is the proxy for orientation quality.** High trust means the knowledge base has sufficient compiled orientation (personas validated, DDRs established, journeys confirmed) to bypass explicit Spec authoring and move directly from Notice to Execute. Low trust forces the full Spec cycle (Boyd's Decide node).

This is not just an analogy — it's a structural mapping:

| Boyd | Intent | Condition |
|---|---|---|
| Orient → Act (IG&C bypass) | Notice → Execute (skip Spec) | Trust ≥ L3, established repertoire |
| Orient → Decide → Act (full path) | Notice → Spec → Execute | Trust < L3, novel situation |
| Orient → Observe (confirmation loop) | KB only surfacing confirming signals | Overwatch absent or suppressed |

**Action needed:** DDR-008 — formalize trust scoring as orientation quality proxy. Define decay mechanics (trust decays with time since last validation, not just with negative observations). Define the IG&C threshold — at what trust level can Notice skip Spec?

**Grounded in:** Richards (2020), Boyd's IG&C mechanism, RAT-003 (dual-circuit architecture).
