---
id: SIG-035
timestamp: 2026-05-19T17:35:00Z
source: agent-trace
confidence: 0.95
trust: 0.65
autonomy_level: L3
status: symptom-repaired, upstream-pending
upstream_control_path: "servers/port_resolver.py (commit ded2447, 2026-05-19) - shared preferred-plus-fallback resolver with two-stage availability probe, wired into the __main__ blocks of servers/notice.py:480, servers/spec.py:420, servers/observe.py:321 (and since extended to servers/knowledge.py:1459); env config documented in servers/DEPLOYMENT.md"
catch_mechanism: "NONE TODAY - the functional tests claimed in the Resolution were session-run and never committed; no test_port_resolver.py exists in the repo, so fallback-on-conflict, env-override, malformed-config, and range-exhaustion behavior has no regression guard"
pipeline_survival: "partial - resolver and server wiring are committed and survive (verified on disk 2026-07-03); nothing prevents a future server from hardcoding a bind, and the missing committed tests mean a regression would go uncaught"
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

## Remediation note (2026-07-03)

Closure-discipline remediation pass (checker flagged missing closure-DoD keys;
this signal predates the DoD-key convention). Repo verification results:

- VERIFIED LANDED: `servers/port_resolver.py` (commit ded2447, 2026-05-19,
  "Resolves SIG-035") with preferred port, configurable fallback range,
  two-stage probe, `PortConfigError` / `NoAvailablePortError`, env-driven
  config. Wired into the `__main__` blocks of notice.py (8001), spec.py
  (8002), observe.py (8003); each logs the actually-bound port. Operator
  docs present in `servers/DEPLOYMENT.md` (INTENT_<SERVER>_PORT,
  INTENT_MCP_HOST, INTENT_MCP_PORT_FALLBACK_COUNT). knowledge.py has since
  gained the same wiring (knowledge.py:1459), superseding the "left
  untouched" line above in the good direction.
- NOT LANDED: the "functional tests" claimed in the Resolution do not exist
  in the repo. No test_port_resolver.py in any directory or in git history;
  commit ded2447 contains no test file. They were run in-session and never
  persisted, so there is no committed catch mechanism for this fix.

Status downgraded from `resolved` to `symptom-repaired, upstream-pending`:
the upstream control (shared resolver) is real and in place, but the
closure DoD requires a catch mechanism and none exists on disk. Open item:
commit a functional test suite for `servers/port_resolver.py` covering
preferred bind, fallback on conflict, env override, malformed config, and
range exhaustion; on landing, this signal can be re-marked `resolved` with
the test path in `catch_mechanism`.

## Trust Factors

- Clarity: high — exact files/lines identified, reference implementation exists.
- Blast radius: low-medium — server bootstrap only; localized, well-tested upstream.
- Reversibility: high — revert to fixed port trivially.
- Testability: high — spin two instances, assert second binds fallback not crash.
- Precedent: high — merged upstream reference implementation (#768) to port from.
