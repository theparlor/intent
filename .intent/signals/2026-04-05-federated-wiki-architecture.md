---
id: SIG-026
timestamp: 2026-04-05T15:30:00Z
source: conversation
confidence: 0.85
trust: 0.6
autonomy_level: L2
status: active
cluster: methodology-adoption
author: brien
related_intents: []
referenced_by: []
parent_signal: SIG-025
---
# Intent's three-layer architecture must federate across Core and bounded engagements

Brien's practice operates multiple concurrent engagements (Subaru, ASA, F&G) plus a Core IP library. The three-layer architecture (raw/ + knowledge/ + .intent/) built for SIG-025 works for a single project but doesn't address how Core methodology continuously grows while each engagement benefits from and contributes to it.

**The architectural decision:** Federate using the same topology Brien already uses for Workspaces — Core = universal substrate, engagements = bounded instances. Three flows:
1. **Inherit down:** Engagements inherit Core schema, templates, archetypes, themes
2. **Promote up:** Generalizable insights sanitized and promoted from engagement → Core
3. **Never leak sideways:** Client-specific content never flows between engagements

**Maps to:** Brien's existing federated glossary pattern (org-specific terms stay in engagement glossary.md, never centralized). Also maps to Beer's VSM (Core = S4+5, engagements = S1, federation = S2+3).

**Key mechanisms:** Schema inheritance (engagement AGENTS.md extends Core knowledge-engine/AGENTS.md), reference notation (`Core:PER-001`), `_core_refs.md` inheritance manifest, confidentiality enforcement via lint, sanitized promotion protocol.

**Spec:** knowledge-engine/spec/federation.md

## Trust Factors

- Clarity: 0.9 — Full spec with three flows, schema extension model, lifecycle, anti-patterns
- Blast radius: 0.3 — Additive to Core; engagement directories don't exist yet; no existing files modified
- Reversibility: 0.9 — Convention-based; removing federation conventions doesn't break anything
- Testability: 0.6 — Can be validated when first engagement scaffolds its knowledge base
- Precedent: 0.8 — Mirrors Brien's proven Workspaces topology and federated glossary pattern
