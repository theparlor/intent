---
id: SIG-051
timestamp: 2026-04-09T04:50:00Z
source: agent-trace
confidence: 0.95
trust: 0.8
autonomy_level: L3
status: captured
cluster: architecture-hardening
author: panel-review-2026-04-09
related_intents: []
referenced_by: []
parent_signal:
---
# Architecture hardening backlog — consolidated from ARB and Engineering panels

The ARB and Engineering panels independently produced a P0/P1/P2 engineering backlog with substantial overlap. This signal consolidates both lists into a prioritized architecture hardening track.

## P0 (this week, blocking)

1. **Fix SIG-022 (sequential ID collision) before federation expands** — both panels flagged this as unpatched P0. ULIDs or scoped prefixes like `{engagement}-SIG-{ulid}`. Sequential SIG-NNN will collide the instant two agents run concurrently.

2. **Persistence story for events.jsonl** — the deployment page literally says "Phase 4: persistence." That means the current path has no durability guarantees. Restart the FastMCP Cloud container and signals vanish. Move to SQLite+WAL or Postgres with explicit fsync semantics.

3. **Harden redaction at the tool level** — D11 says "MCP server applies confidentiality projection automatically based on engagement context" but the caller asserts the context. No mTLS, no signed JWTs, no auth policy engine. Add a cross-engagement leak test to CI that attempts a query from engagement A and asserts zero B data.

## P1 (this month)

4. **Publish runbooks and SLOs per MCP server** — one page per server: SLI definitions, error budget policy, top 5 failure modes, diagnostic commands, escalation path. Without these, "OTel-native" is a schema claim, not a capability.

5. **Collapse 4-server topology evaluation (spike)** — ARB and Engineering both recommended collapsing the 4 servers to one process with 4 modules. Not commit — SPIKE. Evaluate the blast radius and decide. Keep MCP tool surface identical. Matches D6's own "defer infrastructure" posture.

6. **Add deployment-phase event family** — `deploy.started`, `deploy.completed`, `deploy.rolled_back`, `incident.opened`, `incident.resolved`. Without these, DORA is a marketing claim. Wire them to `contract.completed` so cycle time extends all the way to production.

## P2 (this quarter)

7. **Fitness functions for architectural invariants** — no module in Layer 3 imports from Layer 1 directly; signal→spec cycle time p95 < 3 days; contract coverage of promoted intents > 80%. Enforce in CI. Without fitness functions, "evolutionary architecture" is a slogan.

8. **Wardley map and cost model** — one diagram showing where each component sits on the evolution axis; one page showing dollar-cost-per-Intent-cycle across Haiku/Sonnet/Opus routing. Converts "AI collapsed implementation cost" from slogan to measurable claim.

9. **Multi-writer CRDT story for events.jsonl** — D2 says "mergeable event streams" but Git merge on JSONL is a line-conflict generator, not a reconciliation strategy.

## Why this signal exists

Two independent senior-engineering panels produced nearly the same list. That's not opinion — that's a structural gap. This backlog goes directly into the intent product repo (`theparlor/intent`) as engineering work, not site content.

## Trust Factors

- Clarity: 0.95 (two panels converged with specific recommendations)
- Blast radius: 0.6 (architecture changes are higher impact)
- Reversibility: 0.5 (some changes are hard to undo, e.g., ID format migration)
- Testability: 0.95 (these are falsifiable engineering tests)
- Precedent: 0.95 (standard operability hygiene)
