---
id: SIG-029
timestamp: 2026-04-06T10:30:00Z
source: conversation
confidence: 0.85
trust: 0.5
autonomy_level: L2
status: active
cluster: methodology-adoption
author: brien
related_intents: []
referenced_by: []
parent_signal: SIG-027
---
# Knowledge Farm needs full-fidelity named context for solo work but privacy-safe projections for sharing

Brien works solo and needs full named context (real clients, people, metrics) for maximum signal. But when generating proposals for new clients, sharing frameworks externally, or reasoning across engagement boundaries, client-identifying details must be redacted while preserving the insight.

This is a projection model, not a one-time sanitization — same underlying data, different views depending on audience. Four confidentiality tiers: public, internal, client-confidential, nda. Projections are generated on demand, never persisted as separate copies.

**Spec:** `knowledge-engine/spec/redaction.md`

## Trust Factors

- Clarity: 0.8 — Tier model well-defined, projection implementation TBD
- Blast radius: 0.4 — Redaction failure = confidentiality breach
- Reversibility: 0.8 — Projections are ephemeral, never persisted
- Testability: 0.6 — Needs real engagement data to validate redaction completeness
- Precedent: 0.6 — Brien's federated glossary is a simpler version of this pattern
