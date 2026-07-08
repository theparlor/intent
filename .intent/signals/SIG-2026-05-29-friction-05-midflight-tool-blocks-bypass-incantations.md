---
id: SIG-2026-05-29-friction-05-midflight-tool-blocks-bypass-incantations
created: 2026-05-29
type: road-readiness-friction
status: captured
severity: medium
confidence: 0.9
trust: 0.7
friction_class: pretool-block-and-bypass
road_ready_gate: true
parent_signal: SIG-2026-05-29-friction-00-road-readiness-drag-synthesis
related:
  - Core/frameworks/intent/hooks/native-connector-precedence-check.sh
  - Core/frameworks/intent/hooks/native-connector-precedence-map.json
  - Core/frameworks/intent/hooks/skill-intake-gate-check.sh
  - Core/frameworks/intent/hooks/closure-discipline-signal-check.sh
  - feedback_google_workspace_mcp_removed
  - feedback_build_intake_enforcement_active
---

# Friction-05: PreToolUse hooks halt tool calls mid-flight, and recovery requires secret bypass incantations

## What pauses / slows me

Several PreToolUse hooks can **block a tool call outright** and require a memorized
environment-variable bypass + a justification to proceed:

| Hook | Blocks | Bypass incantation |
|---|---|---|
| `native-connector-precedence-check.sh` | workspace-mcp calls when a native connector exists | `NATIVE_CONNECTOR_PRECEDENCE_BYPASSED=1` + reason |
| `skill-intake-gate-check.sh` | build/create/make actions without skill-intake | `BUILD_INTAKE_BYPASSED=1` (logged) |
| `closure-discipline-signal-check.sh` | `status: resolved` signal writes missing closure fields | `CLOSURE_DISCIPLINE_SIGNAL_BYPASSED=1` (logged) |
| `autonomy-grant-dispatch-prompt-check.sh` | sub-agent dispatch prompts that carry drift framing | (per-hook) |
| `forge-shim-gate-check.sh` | Forge shim-path actions | (per-hook) |

The block arrives **mid-flight** — after I've committed to the action, not before I plan
it — and the recovery path is "know the right `*_BYPASSED=1` flag and supply a reason."

## Why it's a road-readiness blocker

- **Bypass-by-secret-incantation does not transfer.** Another operator cannot recover
  from a block they don't know the escape hatch for. A gate whose override is tribal
  knowledge is not a shippable gate.
- **It's a wall where a resolver belongs.** `native-connector-precedence-map.json`
  already encodes the native↔fallback mapping as *data*. The hook uses that data to
  *block-and-make-me-retry* rather than to *route silently to the right tool*. The
  intelligence to do the right thing exists; it's wired as an obstacle instead of an
  autopilot.
- **Mid-flight blocks waste the committed action.** A PreToolUse veto after planning is
  strictly more expensive than steering the choice before it's made.

## Investigation / operationalization direction

1. **Convert precedence from block to route.** Where a deterministic mapping exists
   (native-connector-precedence-map.json), the hook should *rewrite/redirect* to the
   preferred tool transparently, reserving a hard block only for genuinely ambiguous
   cases. Silent-correct beats block-and-retry (the flight-model "Lift is manufactured"
   idea: engineer the safe path, don't gate the unsafe one).
2. **Replace env-var bypasses with a typed, logged exception surface** that any operator
   can discover and use — not a memorized flag. The bypass should be a first-class,
   documented action with a reason field, surfaced in the block message itself.
3. **Move blocks earlier (plan-time) where possible**, so the veto shapes the choice
   instead of discarding a committed call.
4. **Add PreToolUse block rate + bypass rate to the friction-00 Drag dashboard.** A high
   bypass rate means the gate is mis-scoped (we override it routinely → it's noise).

## Open

- For each PreToolUse gate: is the underlying decision deterministic enough to *route*
  instead of *block*? native-connector almost certainly yes; dispatch-prompt and
  build-intake need judgment — those keep a (discoverable, non-secret) override.

## Triage, 2026-07-08

Disposition: still pending. Checked hooks/native-connector-precedence-check.sh directly: the bypass is still the same environment-variable incantation this signal describes ("Bypass: set NATIVE_CONNECTOR_PRECEDENCE_BYPASSED=1 (logged when used)"), not the typed, discoverable, in-message exception surface this signal proposes. No evidence any of the listed PreToolUse gates were converted from block-and-retry to silent-route despite native-connector-precedence-map.json already encoding the deterministic mapping needed to do so. Needed control: unchanged, convert the native-connector precedence gate specifically from block to route (the signal's own highest-confidence candidate, "native-connector almost certainly yes"), and replace the env-var bypass pattern with a documented, in-message override field across all PreToolUse gates.
