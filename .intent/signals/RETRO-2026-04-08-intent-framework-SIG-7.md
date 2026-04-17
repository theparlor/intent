---
signal_id: RETRO-2026-04-08-intent-framework-SIG-7
title: Session-start lint behavior declared in CLAUDE.md but not wired through hooks
severity: medium
detected: 2026-04-05
status: open
source: retroactive-extraction
trust_score: 0.50
autonomy: L2
---
# Session-Start Behavior Declared But Not Wired

## Observation
CLAUDE.md autonomy grants specify "Session-start behavior: execute, don't ask. Load artifact registry, check signal log, run freshness scan on active engagements, enrich context silently." But no hook or overwatch integration actually implements this. The declaration exists; the execution mechanism doesn't.

## Context
The overwatch skill already runs at session start. The artifact registry and signal log now exist with real data. The gap is the wiring — overwatch doesn't yet read the registry or signal log.

## Implication
- A future session needs to extend overwatch (or add a hook) that loads .artifact-registry/registry.md and .signal-log/LOG.md at conversation start
- Without this, each session starts cold — the knowledge graph data exists but isn't surfaced until Brien asks about it
- The fix is likely a hook in settings.json or an overwatch extension, not new methodology
