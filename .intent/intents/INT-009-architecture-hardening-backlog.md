---
id: INT-009
title: "Architecture hardening backlog from ARB + Engineering panels"
status: proposed
proposed_by: "panel-review-2026-04-09"
proposed_date: 2026-04-09T05:00:00Z
accepted_date:
signals: [SIG-051]
specs: []
owner: "brien"
priority: now
product: execute
---
# Architecture hardening backlog from ARB + Engineering panels

## Problem

Two independent senior-engineering panels (ARB: Wardley/Hohpe/Ford/Fowler/Majors/Kim; Engineering: Majors/Kim/Forsgren/Humble/Farley/Skelton/Fowler/Beck/Poppendieck/Reinertsen/Smart) produced nearly the same P0/P1/P2 backlog for architectural operability. This is not opinion — this is structural.

The site currently presents Intent as a shipped product. The panels diagnosed it as a promising prototype wearing production clothes. The fix is not better copy — the fix is real engineering hardening.

## Desired Outcome

Ship the consolidated architecture backlog as explicit engineering work in the `theparlor/intent` product repo (NOT the site repo). This is code and ops work, not content.

### P0 (this week, blocking further adoption)

1. **Fix SIG-022 sequential ID collision** — migrate to ULIDs or scoped prefixes `{engagement}-SIG-{ulid}`. Before any second engagement comes online.
2. **Persistence story for events.jsonl** — move from "Phase 4 later" to SQLite+WAL with explicit fsync. Document restart semantics.
3. **Cross-engagement leak test in CI** — attempts query from engagement A's context, asserts zero B data returns. Until this exists, D11 (redaction at tool level) is aspirational.

### P1 (this month)

4. **Runbooks + SLOs per MCP server** — one page per server: SLI definitions, error budget, top 5 failure modes, diagnostic commands, escalation path.
5. **4-server topology spike** — evaluate collapsing to one process with 4 modules. NOT a commit — a decision. Document the spike findings as an ADR.
6. **Deploy-phase event family** — `deploy.started`, `deploy.completed`, `deploy.rolled_back`, `incident.opened`, `incident.resolved`. Wire to `contract.completed`. Without these, DORA is a claim.

### P2 (this quarter)

7. **Fitness functions in CI** — layer-dependency direction, schema conformance, trust-formula boundary tests, cycle-time SLOs, contract coverage thresholds.
8. **Wardley map + cost model** — one evolution-axis diagram, one cost-per-Intent-cycle page.
9. **Multi-writer CRDT story for events.jsonl** — Git merge on JSONL is a line-conflict generator, not reconciliation.

## Evidence

- **SIG-051:** Architecture hardening backlog — full consolidated list
- ARB panel verdict: "Conditional approval for pilot within a single engagement; block for multi-tenant production."
- Engineering panel verdict: "Would not let this run in production. Promising prototype, not production software."

## Constraints

- Must go in `theparlor/intent` product repo, not `theparlor/intent-site`
- Must be delivered as code + ADRs, not as site content
- Must NOT be presented as "shipped" on the site — labeled as evolutionary/open-question until P0 complete
- P0 must complete before any team pilot (internal or external)

## Specs to generate from this intent

- SPEC-SIG-022-ulid-migration
- SPEC-events-jsonl-persistence
- SPEC-cross-engagement-leak-test
- SPEC-runbook-format
- SPEC-4-server-topology-spike

## Out of Scope (deferred)

- Wardley map (P2, decision aid not delivery dependency)
- Cost model (P2)
- Fitness functions (P2 — useful but not blocking)
