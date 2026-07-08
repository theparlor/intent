---
signal_id: RETRO-2026-04-08-intent-framework-SIG-7
title: Session-start lint behavior declared in CLAUDE.md but not wired through hooks
severity: medium
detected: 2026-04-05
status: open
last_triaged: 2026-06-17
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

---

## Triage note — 2026-06-17 (still open; partial — mechanism exists, specific wiring does not)

**Disposition: stays open, narrowed.** The signal's original claim ("no hook or overwatch integration actually implements this") is now partially false: `~/.claude/settings.json` registers SessionStart hooks (`overwatch-staleness-check.sh`, `overwatch-nested-init-check.sh`), and overwatch runs at session start. So the *mechanism* for session-start behavior now exists. But the SPECIFIC wiring this signal named — loading the artifact registry (`.artifact-registry/registry.md`) and signal log (`.signal-log/LOG.md`) silently at conversation start — is NOT what those hooks do (they check staleness and nested-init drift). The "each session starts cold w.r.t. the knowledge-graph data" gap remains. Low urgency; not closing because the named behavior is still unwired.

## Triage, 2026-07-08

Disposition: still pending, unchanged since the 2026-06-17 narrowing triage already on this file. Re-verified: .artifact-registry and .signal-log directories now exist, but only under Core/products/forge/, not referenced by any SessionStart hook. The registered SessionStart hooks (overwatch-staleness-check.sh, overwatch-nested-init-check.sh) still do staleness/drift checks, not the specific silent registry-and-log load this signal named. The 2026-06-17 narrowing stands: mechanism exists (overwatch runs at session start), the specific wiring does not.
