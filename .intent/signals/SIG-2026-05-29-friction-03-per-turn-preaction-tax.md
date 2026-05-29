---
id: SIG-2026-05-29-friction-03-per-turn-preaction-tax
created: 2026-05-29
type: road-readiness-friction
status: captured
severity: medium
confidence: 0.9
trust: 0.7
friction_class: per-turn-startup-latency
road_ready_gate: true
parent_signal: SIG-2026-05-29-friction-00-road-readiness-drag-synthesis
related:
  - build-intake-mandatory
  - autonomy-grant-drift-detector
  - feedback_tool_discovery_discipline
  - feedback_explicit_templates_not_mimicry
  - reference_placement_resolver
---

# Friction-03: mandatory pre-action gates stack at the FRONT of nearly every turn

## What pauses / slows me

Before the first substantive action of (nearly) every turn, a stack of mandatory
pre-checks must clear. None is individually large; summed, they are a per-turn startup
tax that no one has budgeted:

| Gate | Source | Cost shape |
|---|---|---|
| **1%-rule skill check** | `using-superpowers` (SessionStart) — *"even a 1% chance a skill might apply… you ABSOLUTELY MUST invoke the skill… before ANY response including clarifying questions"* | Deliberation + possible Skill load on every turn |
| **build-intake L0** | `build-intake-mandatory` — skill-intake invocation MANDATORY before any build/create/make | Blocks the first build action |
| **4-gate self-check** | SessionStart `AUTONOMY GRANT POSTURE` anchor | Silent precondition compute before any decision |
| **drift-detector self-audit** | `autonomy-grant-drift-detector` skill | Silent 4-gate re-scan before responses with drift symptoms |
| **governance-chain walk** | CLAUDE.md / `AGENTS.md` → `RULES.md` → references → templates → schema before ANY file write | Multi-file read before a single write |
| **TOOLS-INDEX scan** | `feedback_tool_discovery_discipline` — check `Core/TOOLS-INDEX.md` before N>3 edits or new utility | Index read before bulk edit |

## The live example from the session that produced this signal

Capturing this very friction cluster forced a real deliberation about whether to invoke
the `superpowers:brainstorming` skill — on a task Brien had **explicitly scoped to signal
capture**. The 1%-rule's maximal conservatism ("even 1%… ABSOLUTELY MUST") turns a
clearly-scoped Notice activity into a skill-eligibility adjudication. The deliberation was
cheap individually and correct to resolve (brainstorming does not apply to capturing
pre-existing observations), but it is the per-turn tax made visible: the gate fires even
when the answer is obviously "no."

## Why it's a road-readiness blocker

- The gates are **uninstrumented**: we know each exists; we do not know their summed
  latency, how often each is load-bearing, or which are cargo-culted.
- **Front-loading is correct for *relevant* gates** (the Intent posture — "load context
  before acting" — is sound). The friction is *undifferentiated mandatory application*:
  a 1%-threshold and an "ALWAYS / ABSOLUTELY MUST / before ANY response" framing means
  the gate cannot distinguish a trivial turn from a consequential one. That is the same
  no-value-term defect as friction-01, at the turn-startup layer.
- For another operator, "run this 6-item checklist before every turn" is not adoptable.

## Investigation / operationalization direction

1. **Instrument the stack.** Add per-gate fire/skip telemetry to friction-00's Drag
   dashboard. Establish which gates ever change the outcome.
2. **Make gate application proportional to stakes**, not blanket. The flight-model λ /
   gate-surface-matrix already scopes by surface — apply the same idea to pre-action
   gates: a Workspaces-local signal write does not need the full build-intake +
   governance-chain ceremony a new client-facing artifact does.
3. **Audit the 1%-rule threshold specifically.** "Even 1% → MUST invoke" maximizes recall
   at the cost of per-turn precision. Decide whether a higher threshold (or a cheap
   relevance pre-filter) preserves the benefit without the blanket tax.
4. **Convert the governance-chain walk into a resolver call**, not a manual multi-file
   read (`reference_placement_resolver` is the data; the walk is the un-automated tax).

## Open

- Which of these gates are genuinely load-bearing vs. residue from a single past incident?
  Telemetry should rank them by "times this gate changed the action taken."
