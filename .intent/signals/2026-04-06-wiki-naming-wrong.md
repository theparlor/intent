---
id: SIG-030
timestamp: 2026-04-06T09:00:00Z
source: conversation
confidence: 1.0
trust: 0.9
autonomy_level: L3
status: resolved
cluster: methodology-adoption
author: brien
related_intents: []
referenced_by: []
parent_signal: SIG-025
---
# "Wiki" is the wrong name — this is a compiled knowledge base, not a human-maintained wiki

Brien identified that "wiki" (inherited from Karpathy's directory naming) does not accurately describe what we build. A wiki is human-authored, human-linked, human-maintained. What we build is human-curated sources → agent-compiled artifacts → auto-generated cross-references → lint-audited coverage. This is a compiled knowledge base or knowledge graph.

**Resolved:** Renamed `wiki/` → `knowledge/` across entire project. All references updated. Karpathy's own use of "wiki" preserved in source attributions.

## Trust Factors

- Clarity: 1.0 — The distinction is unambiguous
- Blast radius: 0.3 — Naming change only, no structural change
- Reversibility: 0.9 — Directory can be renamed back
- Testability: 1.0 — Already done and verified
- Precedent: 1.0 — Resolved
