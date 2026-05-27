---
id: SIG-ARCH-FIRST-PRESSURE-TEST-WITNESS-2026-05-27
timestamp: 2026-05-27T14:30:00Z
source: claude-code-session "what else is doable" sweep
author: brien
confidence: 0.82
trust: 0.78
autonomy_level: L4
status: active
cluster: coherence-engineering-design-patterns
parent_signal: 2026-05-26-architecture-first-content-sequenced-pattern.md
related_principle: Core/frameworks/coherence-engineering/principles/architecture-first-content-sequenced.md
related_decisions:
  - WS-DDR-099 (substrate exposure)
  - WS-DDR-025 (sibling-over-parent-child)
phase: 2-pressure-test
pressure_test_instance: "(a) Witness adapter completion path (WIT-004 #5)"
result: structural PASS, observational PENDING (gated on WIT-004 #5 stub-to-live)
---

# Architecture-first principle pressure-test (a): Witness entire-io.py stub — structural PASS

## What was tested

Pressure-test instance (a) from the architecture-first content-sequenced
principle's open-questions section: *"the Witness adapter completion path
(WIT-004 #5) — does climbing from stub to live adapter require any
surface-level changes, or only content/config?"*

## What was found

The Witness `entire-io.py` stub at
`Core/products/witness/engine/adapters/entire-io.py` already declares the
full contract surface that a live adapter needs:

| Surface element | Declared in stub? | Implication |
|---|---|---|
| `ADAPTER_ID = "entire-io"` | ✅ Yes | Registered identity exists at the adapter-registry layer |
| `SOURCE_SYSTEM = "entire-io"` | ✅ Yes | Witness's `events_store.append(source_system=...)` already accepts this value via the existing port contract |
| `MIGRATION_ORDER = 5` | ✅ Yes | The stub knows its position in the population of N adapters |
| `SOURCE_PATTERN = ".entire/metadata/*/full.jsonl"` | ✅ Yes | The path-shape from which content will be read is declared |
| `ENTIRE_BINARY = "/opt/homebrew/bin/entire"` | ✅ Yes | External-dependency anchor is declared (with explicit "do not call directly" boundary) |
| `migrate()` function shape | ✅ Yes (`raise NotImplementedError`) | The interface signature is fixed; only the body needs to be filled in |
| Contract docstring (Source → Target schema) | ✅ Yes | The translation contract is explicit — `events_store.append(..., source_system="entire-io")` |

**Filling the stub is content-only.** The only work needed is:
1. Read each `full.jsonl` line from the Entire.io session directory.
2. Parse each JSON object (agent reasoning trace step).
3. Call `events_store.append(source_system="entire-io", ...)` per line.

The following would NOT need to change:
- Witness's `events_store` schema or its `append()` signature
- The adapter registry (the stub is already registered via its file location)
- The federation port contract (OTLP + structured stderr JSONL — adapter doesn't touch these; it appends events directly to the store)
- Other adapters (no shared state; conservation law preserved per Witness CONTEXT.md)

## What this means for the principle

**Structural pressure-test: PASS.** The stub demonstrates the principle's
prediction exactly — the surface was designed for the full population of
adapters (N expected, currently 5 stubbed); the content (each adapter's
`migrate()` body) sequences in tactically as each adapter is implemented.

**Observational pressure-test: PENDING.** True confirmation requires
actually filling in the stub and verifying no surface changes were forced
during implementation. That observational confirmation is blocked on
WIT-004 #5 + Entire.io output-format inspection (per the stub's "EXTERNAL
DEPENDENCY NOTES"). When the stub is implemented, this signal should be
revisited and the observational result recorded.

## Calibration note on the structural-vs-observational distinction

A structural pressure-test ("the stub already declares the right contract
surface") is weaker evidence than an observational pressure-test ("the
stub was filled in and no surface changes were needed"). The principle's
strongest claim — "the architecture never refactors because it was always
designed for the population" — is empirically verified only by the latter.
The former is *prediction confidence*, not *outcome confirmation*.

For the principle's external-articulation gate (per the principle doc's
`gates_before_external_articulation`), structural pressure-test should
count as ~0.5 of an observational pressure-test. So instance (a)'s
contribution to the "3 more instances" target is partial — approximately
0.5 of 3.

## Pressure-test progress (updated)

| Instance | Type | Status |
|---|---|---|
| (a) Witness adapter completion (WIT-004 #5) | Structural | PASS 2026-05-27 (this signal) |
| (a) Witness adapter completion (WIT-004 #5) | Observational | PENDING (stub-to-live) |
| (b) Client-engagement onboarding flow | Both | NOT YET TESTED |
| (c) Phase 2 write-back design (substrate exposure) | Both | NOT YET TESTED |

**Progress toward external articulation: ~0.5 of 3 instances.** Two more
observational pressure-tests needed before the principle is ready for
DEFINITION.md elevation (per `gates_before_external_articulation`).

## What triggered this pressure-test

User asked during current session: "what else from our to do list in here
is doable?" Tier 3 of the response menu was the pattern-signal pressure-
test sweep. Investigation was read-only — examined the stub, mapped its
declarations against the principle's prediction, recorded the structural
match.

## Cross-references

- Principle doc: `Core/frameworks/coherence-engineering/principles/architecture-first-content-sequenced.md`
- Parent signal: `2026-05-26-architecture-first-content-sequenced-pattern.md` (SIG-ARCH-FIRST-CONTENT-SEQUENCED-2026-05-26)
- Stub under test: `Core/products/witness/engine/adapters/entire-io.py`
- Witness adapter migration order: WIT-004 (in `Core/products/witness/.intent/decisions.md`)
- Blocking dependencies for observational pressure-test: WIT-006 (SPEC-001 ratification — gated on library-index AM-3 audit + Conduit OTLP-emit)
