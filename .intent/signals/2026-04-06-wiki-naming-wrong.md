---
id: SIG-030
timestamp: 2026-04-06T09:00:00Z
source: conversation
confidence: 1.0
trust: 0.9
autonomy_level: L3
status: resolved
upstream_control_path: CLAUDE.md repo-structure section and knowledge-engine/AGENTS.md define `knowledge/` as the canonical compiled layer; rename rationale recorded in knowledge/log.md (2026-04-06 UPDATE entry)
catch_mechanism: NONE TODAY for vocabulary reintroduction (no lint flags "wiki/" usage in new docs; spec/substrate-exposure-architecture.md and servers/DEPLOYMENT-INTENT-KNOWLEDGE.md, authored May 2026, reuse the term as substrate shorthand). Directory-level regression is structurally guarded because `knowledge/` paths are load-bearing in servers/knowledge.py and knowledge-engine/AGENTS.md.
pipeline_survival: verified 2026-07-03, wiki/ absent and knowledge/ present with _index.md, log.md, traceability.md plus 7 artifact dirs; any regression of the directory name breaks every knowledge-engine operation immediately
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

## Remediation note (2026-07-03)

Flagged by the closure write-boundary checker for missing closure-DoD keys, which post-date this April signal. Fresh verification confirms the claimed work landed and holds: `wiki/` is absent, `knowledge/` exists with the full compiled structure (_index.md, log.md, traceability.md, personas/, journeys/, decisions/, themes/, domain-models/, design-rationale/, dossiers/), and the rename is recorded in knowledge/log.md (2026-04-06 UPDATE entry). Remaining "wiki/" strings are either Karpathy source attributions (preserved by design per this signal) or shorthand in two May 2026 docs written after closure; that vocabulary drift is outside this signal's scope and is noted honestly in catch_mechanism above. Status stays resolved; the three DoD keys were added as part of this remediation.
