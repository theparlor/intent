---
id: SIG-034
timestamp: 2026-04-13T01:30:00Z
source: research-synthesis
confidence: 0.85
trust: 0.7
autonomy_level: L2
status: resolved
upstream_control_path: knowledge/decisions/DDR-008-trust-as-orientation-proxy.md (status accepted, 2026-04-13) plus supersession protocol in CLAUDE.md "Before Making ANY Decision" (overrides require a superseding DDR)
catch_mechanism: DDR read-before-decide and supersession discipline (CLAUDE.md) guards the formalization; NO automated check today enforces DDR-008's own validation criteria (implementation-level decay and orientation-modifier behavior), which remain unchecked in the DDR and are DDR-008's lifecycle, not this signal's
pipeline_survival: yes, DDR-008 is canonical on-disk in knowledge/decisions/ and indexed in knowledge/_index.md
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

**Action taken (landed 2026-04-13):** DDR-008 (`knowledge/decisions/DDR-008-trust-as-orientation-proxy.md`, status accepted, `related_signals: SIG-034`) formalizes trust scoring as orientation quality proxy. Decay mechanics are defined (DDR-008 Decision 2: validation-based decay, full modifier 0 to 30 days, linear decay to 0.8x at 90 days, 0.7x cap past 90 days until re-validated). The IG&C threshold is defined (DDR-008 Decision 3: effective trust at or above 0.85 gives L4 IG&C-dominant bypass; the full five-band table maps effective trust to autonomy levels).

**Grounded in:** Richards (2020), Boyd's IG&C mechanism, RAT-003 (dual-circuit architecture).

## Remediation note (2026-07-03)

Closure write-boundary checker flagged this signal as PREMATURE-RESOLVED for missing closure-DoD keys (`upstream_control_path`, `catch_mechanism`), a convention this April signal predates. Verified against repo state: the asked-for deliverable, DDR-008, exists, is accepted, links back to SIG-034, and covers all three requested definitions (orientation-quality mapping, decay mechanics, IG&C threshold). Status stays `resolved`; DoD keys added with honest scope. Note the boundary: DDR-008's own validation criteria (implementation of the orientation modifier and decay in the trust scorer) remain open and belong to DDR-008 and the trust-scoring-agent backlog item, not to this signal, whose ask was the formalization itself. A `compute_effective_trust` function exists in `servers/models.py` but implements amplification-based adjustment, not the DDR-008 orientation modifier.
