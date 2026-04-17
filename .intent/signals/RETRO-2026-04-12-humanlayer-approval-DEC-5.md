---
id: RETRO-2026-04-12-humanlayer-approval-DEC-5
type: decision
source: session-analysis
decided: 2026-04-12
topic: humanlayer-approval
status: decided
---

# Defer Daemon Architecture — Gate Skill Is Sufficient

## Context

HumanLayer runs a Go daemon (hld) with SQLite store, Unix domain socket, event bus, SSE streaming. Full infrastructure for multi-user, multi-session approval management.

## Decision

Defer daemon architecture. Brien's single-user workflow doesn't need a persistent process. The IntentApproval entity and gate skill can live within the existing Skills Engine + intent journal. File-based persistence (consistent with Intent's file-native design).

## Alternatives Considered

1. **Build lightweight daemon** — deferred; adds infrastructure for a single-user system
2. **Adopt HumanLayer directly** — rejected; wrong granularity (tool-level vs. autonomy-level gates)

## Consequences

- No new infrastructure required
- Approval records stored as intent journal entries (file-native)
- Future: if Brien needs multi-machine or always-on approval routing, daemon becomes relevant
- Revisit when hosted deployment mode (already on Intent roadmap) materializes
