---
id: SIG-035
timestamp: 2026-05-19T17:35:00Z
source: agent-trace
confidence: 0.95
trust: 0.65
autonomy_level: L3
status: resolved
cluster: null
author: brien
related_intents: []
referenced_by: []
parent_signal: SIG-034
---

# Intent's own MCP servers hardcode ports — the exact bug we just fixed upstream

## Summary

Checking whether Intent consumes `taylorwilsdon/google_workspace_mcp` internally
(it does not — zero references; only dep is `fastmcp>=2.0`) surfaced a dogfood
gap: Intent's own MCP servers hardcode their ports with no fallback, the exact
pattern `#768` fixed upstream.

- `servers/notice.py:478` → `mcp.run(transport="streamable-http", host="0.0.0.0", port=8001)`
- `servers/spec.py:418` → `port=8002`
- `servers/observe.py:319` → `port=8003`
- `servers/knowledge.py` → documented port 8004

No preferred-plus-fallback resolution, no late binding, fixed `0.0.0.0` host.

## Why it might matter

Same failure class #768 addressed: a second instance (multi-machine, hosted/
always-on mode per the deployment-topology plan, or dev + prod on one box, or an
orphaned process holding the port) → "port 8001 already in use" boot failure.
The hosted/always-on direction in CLAUDE.md makes concurrent instances likely,
not hypothetical. We just wrote and merged the canonical fix for this exact
problem in someone else's codebase while carrying the un-fixed version in ours.

The design is already validated in the wild (#768 survived 19 commits unchanged
conceptually). Porting the pattern is low-risk, high-precedent work.

## Proposed actions

1. Extract the port-resolver pattern (preferred port + configurable fallback
   range, two-stage availability probe) and apply to the four Intent servers.
2. Env-var config mirroring upstream (`INTENT_<SERVER>_PORT`, fallback count).
3. Update startup logging to report the actually-bound port (the operability
   lesson from SIG-034 #768 retro — don't repeat the blind spot here).

## Resolution (2026-05-19, L3 — agent executed, human monitors)

Implemented `servers/port_resolver.py` (clean-room reimplementation of the
#768 pattern): preferred port + configurable fallback range, two-stage
availability probe (loopback connect, then real bind), env-driven config,
`PortConfigError` / `NoAvailablePortError`. Wired into the `__main__` blocks
of `notice.py` (8001), `spec.py` (8002), `observe.py` (8003); each now logs
the port it actually bound (the SIG-034 operability lesson applied — not
repeated). `knowledge.py` has no in-process bind (deployed via `fastmcp run`)
so it was correctly left untouched. Functional tests cover preferred bind,
fallback on conflict, env override, malformed config, and range exhaustion.
Operator docs updated in `servers/DEPLOYMENT.md`. No new lint errors
introduced (pre-existing ruff findings on these files are unchanged and
left out of scope).

## Trust Factors

- Clarity: high — exact files/lines identified, reference implementation exists.
- Blast radius: low-medium — server bootstrap only; localized, well-tested upstream.
- Reversibility: high — revert to fixed port trivially.
- Testability: high — spin two instances, assert second binds fallback not crash.
- Precedent: high — merged upstream reference implementation (#768) to port from.
