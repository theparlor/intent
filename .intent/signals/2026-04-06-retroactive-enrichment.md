---
id: SIG-028
timestamp: 2026-04-06T10:15:00Z
source: conversation
confidence: 0.85
trust: 0.5
autonomy_level: L2
status: resolved
upstream_control_path: "CLAUDE.md Key Decision 17 (Retroactive enrichment = suggested) + Core/frameworks/intent/knowledge-engine/spec/enrichment.md"
catch_mechanism: "lint-detects-opportunity, surfaces-as-signal, on-demand-execution replaces the automatic-cascade model this signal originally proposed"
verification_command: "ls /Users/brien/Workspaces/Core/frameworks/intent/knowledge-engine/spec/enrichment.md"
cluster: methodology-adoption
author: brien
related_intents: []
referenced_by: []
parent_signal: SIG-027
---
# New Knowledge Engine capabilities must be retroactively applied to prior engagement knowledge

When Brien develops a new capability (e.g., company dossier autogeneration, industry-level analysis), it should be reapplied against all prior engagement knowledge to pressure-test the capability, enrich prior knowledge, and surface cross-engagement patterns for newer clients with less context.

This is the recompilation cascade — same raw sources, upgraded compiler, potentially better output. Creates a career flywheel where every engagement makes Core stronger, which makes every future engagement start from a higher baseline.

**Spec:** `knowledge-engine/spec/enrichment.md`

## Trust Factors

- Clarity: 0.8 — Pattern well-defined but implementation details TBD
- Blast radius: 0.5 — Recompilation touches prior engagement knowledge
- Reversibility: 0.6 — Recompiled artifacts could be regenerated but changes to confidence scores cascade
- Testability: 0.7 — Can be validated by running a new capability against existing Subaru/ASA data
- Precedent: 0.5 — Novel pattern; Karpathy's system doesn't do retroactive enrichment

## Triage, 2026-07-08

Disposition: control exists now via ratified decision, not built automation. This signal's recompilation-cascade proposal was decided the same day: CLAUDE.md's Key Decision 17 ("Retroactive enrichment = suggested. Lint detects recompilation opportunities, surfaces as signals. On-demand execution. Not automatic cascades.") answers this exact signal, and knowledge-engine/spec/enrichment.md exists as the formal spec. The decision is a lighter-weight answer than the signal's original "reapply automatically against all prior engagement knowledge" framing, but it is a considered, ratified answer, not a gap.
