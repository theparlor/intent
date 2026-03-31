---
id: CLU-005
name: "methodology-adoption"
title: "Methodology & Adoption"
status: active
signals: [SIG-006, SIG-007, SIG-009, SIG-010, SIG-019, SIG-020]
weight: 1.9
formed_date: 2026-03-30
promoted_to: ""
promoted_date:
---
# Cluster: Methodology & Adoption

## Theme
Founding observations, four-product thesis, vocabulary friction, and site information architecture. This is the cluster about what Intent *is* and how people encounter it. SIG-006 identified the bootstrap gap — Intent describes a model but doesn't yet enable practitioners to install and test it Monday morning. SIG-007 captured the ceremony wall that teams hit around sprint 3 with AI agents. SIG-009 reframed Intent as four products, not one. SIG-010 brought external validation from Ari's team, who independently rewired around AI. SIG-019 flagged that "Notice" and "Execute" aren't landing as phase names. SIG-020 identified the site IA problem. This cluster is blocked on the vocabulary decision (SIG-019) which cascades into site, docs, CLI, and MCP naming.

## Member Signals

| Signal | Title | Trust | Date |
|--------|-------|-------|------|
| SIG-006 | Intent is a description, not an enabler — practitioners can't install and test it Monday morning | 0.55 | 2026-03-29 |
| SIG-007 | Teams using AI agents hit a ceremony wall around sprint 3 | 0.10 | 2026-03-29 |
| SIG-009 | Intent is four products (Notice, Spec, Execute, Observe), not one | 0.15 | 2026-03-29 |
| SIG-010 | Engineer's team rewired around AI: tickets became bot specs, refinement became design sessions | 0.10 | 2026-03-29 |
| SIG-019 | "Notice" and "Execute" aren't landing as loop phase names | 0.50 | 2026-03-30 |
| SIG-020 | Intent site needs two-tier information architecture | 0.50 | 2026-03-30 |

## Promotion Criteria
A cluster is ready for promotion to intent when:
- [x] 3+ signals with independent sources
- [x] Aggregate weight > 1.0 (sum of trust scores)
- [x] At least one signal from the last 14 days (not stale)
- [ ] Pattern is actionable (not just an observation)

## Emergence Notes
How did this cluster form? Was it:
- **Human-noticed:** Brien identified the methodology pattern across founding observations, Ari's external validation, and the vocabulary/IA friction surfaced during site development. The signals span multiple sessions and sources but all address the question of how Intent presents itself to the world.

## Open Questions
- What should replace "Notice" and "Execute" as phase names? Candidates exist but the decision cascades everywhere.
- Is the bootstrap gap (SIG-006) a packaging problem (need an installer) or a conceptual problem (need a simpler on-ramp)?
- How much of the four-product framing (SIG-009) should be visible to first-time practitioners vs. reserved for the methodology depth?
- Does Ari's team pattern (SIG-010) generalize, or is it specific to their team's AI maturity level?
