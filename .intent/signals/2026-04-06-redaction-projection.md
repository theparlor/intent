---
id: SIG-029
timestamp: 2026-04-06T10:30:00Z
source: conversation
confidence: 0.85
trust: 0.5
autonomy_level: L2
status: resolved
upstream_control_path: "memory/feedback_no_preemptive_redaction.md (ratified 2026-06-10)"
catch_mechanism: "policy decision overtook the premise: redaction is a per-recipient human call at share time, never an automated pipeline projection generated on demand"
verification_command: "cat /Users/brien/.claude/projects/-Users-brien-Workspaces/memory/feedback_no_preemptive_redaction.md"
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

## Triage, 2026-07-08

Disposition: overtaken. This signal proposed a four-tier confidentiality projection engine (public/internal/client-confidential/nda) generated on demand from a single underlying dataset; knowledge-engine/spec/redaction.md was written the same day (still maturity: draft) but the automated projection mechanism it specced was never built. The premise itself was superseded by a later ratified decision: memory/feedback_no_preemptive_redaction.md (2026-06-10, SE-002 Amendment 1) establishes that Brien's own access is unredacted everywhere, peer sharing is a per-recipient human contract decision, and automated redaction transforms apply only at the public-distribution boundary, built only when there is real motive, not as a standing pipeline. Same disposition this pass's batch 1 gave the equivalent Cast-side signal (SIG-020).
