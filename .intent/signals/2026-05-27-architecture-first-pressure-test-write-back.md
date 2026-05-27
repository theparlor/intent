---
id: SIG-ARCH-FIRST-PRESSURE-TEST-WRITEBACK-2026-05-27
timestamp: 2026-05-27T16:30:00Z
source: claude-code-session "keep going" sweep (third instance)
author: brien
confidence: 0.70
trust: 0.65
autonomy_level: L4
status: active
cluster: coherence-engineering-design-patterns
parent_signal: 2026-05-26-architecture-first-content-sequenced-pattern.md
sibling_signal: 2026-05-27-architecture-first-pressure-test-witness-adapter.md
related_principle: Core/frameworks/coherence-engineering/principles/architecture-first-content-sequenced.md
related_decisions:
  - WS-DDR-099 (substrate exposure — Track A; Phase 1 read-only, Phase 2 write-back)
  - DEC-010 (intent-knowledge MCP scope extension — 5 read verbs Day 1)
phase: 2-pressure-test
pressure_test_instance: "(c) Phase 2 write-back design (substrate exposure)"
result: PARTIAL PASS — read surface generalizes for most write verbs; Git surface for PR-as-arbiter is a genuine surface extension, not content-only
---

# Architecture-first principle pressure-test (c): Phase 2 write-back design — PARTIAL PASS

## What was tested

Pressure-test instance (c) from the architecture-first content-sequenced
principle's open-questions section: *"the eventual write-back design for
substrate exposure (Phase 2 of Track A) — does adding writes require
new ports, or does the existing read-shaped surface generalize?"*

This pressure-test is sketch-level (paper architecture). Full
observational pressure-test waits for Phase 2 implementation.

## What was found (design sketch)

The Phase 1 read surface (`intent-knowledge` MCP server) declares 5
verbs that all share a uniform policy-enforcement spine:

| Read verb | Inputs | Tier-aware policy hook |
|---|---|---|
| `query(text, scope_token, k)` | text + scope + limit | scope check, classification filter |
| `get(entity_id, scope_token)` | ID + scope | scope check, classification filter |
| `list_entities(scope_token, ...)` | scope + filters | scope check, classification filter |
| `lineage(signal_id, scope_token, depth)` | signal + scope + depth | scope check, classification filter |
| `freshness(path, scope_token)` | path + scope | scope check, classification filter |

The Phase 2 write surface would extend this with write verbs:

| Write verb (sketched) | Inputs | Tier-aware policy hook | Generalizes from read? |
|---|---|---|---|
| `write_signal(content, scope_token, classification, metadata)` | content + scope + tier + attributes | scope-write check, classification-write enforce | ✅ YES — same policy spine, inverted direction |
| `propose_intent(text, scope_token, classification, parent_signal)` | text + scope + tier + parent | scope-write check, classification-write enforce | ✅ YES — same spine |
| `update_record(entity_id, patch, scope_token)` | ID + patch + scope | scope-write check + PR-as-arbiter trigger | ⚠️ PARTIAL — policy spine generalizes, but the PR-as-arbiter mechanism is a new sibling surface |
| `record_observation(content, scope_token, classification, source_artifact)` | content + scope + tier + provenance | scope-write check, classification-write enforce | ✅ YES — same spine |

## What generalizes (architecture-first PASS for this dimension)

The **tier-aware policy enforcement point** that Phase 1 designed for
the full population of consumers (per WS-DDR-099 + D5-refined) extends
directly to writes:

- Same `scope_token` mechanism — clients carry tokens, server enforces
  per-tier.
- Same `classification.yaml`-driven enforcement — content's tier
  declared at write-time, server validates write authorization.
- Same `404 / absent` semantics for engagement-tier writes when scope
  is missing (writes refused, not silently degraded).

This is the architecture-first principle operating at the policy
spine: the surface (policy enforcement point + scope mechanism) was
designed for the full population on Day 1. Adding write verbs is
content-and-config work at this dimension — declare the new verb,
hook the policy point, done.

## What does NOT generalize (genuine surface extension required)

Three concerns are first-instantiated by Phase 2 writes and do not
exist in the Phase 1 read surface:

### 1. Git surface for PR-as-arbiter

WS-DDR-099 names PR-as-arbiter as the Phase 2 write-back arbiter. A
mobile-Claude session writing back a signal would: (a) call the MCP
write verb, (b) the server creates a branch on the canonical repo,
(c) writes the signal file there, (d) pushes, (e) opens a PR for
Brien's review, (f) returns the PR URL to the client.

The Git surface (branch creation, push, PR open via `gh`) is a
**sibling-composed external surface** that does not exist in Phase 1.
This is architectural addition, not content-sequencing. The surface
itself is new. (However, it sits at a sibling-composition seam with
the existing MCP read surface — WS-DDR-025 still holds; the read and
write paths are sibling consumers of the policy spine.)

### 2. Identity / attribution surface

Phase 1 read does not need to know *who* is reading (only what scope
they hold). Phase 2 write needs author attribution — every signal
file carries an `author:` frontmatter field; every commit needs an
author identity. The client (mobile-Claude session) needs to declare
identity at write time, and the server needs to record + verify it.

This is a new **identity surface** at the write boundary. It can be
sibling-composed (an `Identity` provider plugs into the MCP server's
auth pipeline) but the boundary itself is genuinely added in Phase 2.

### 3. Conflict resolution / concurrency

Two non-desktop surfaces could concurrently propose writes to the
same path. Phase 1 reads have no conflict semantics. Phase 2 write
needs conflict-resolution discipline — at minimum: (a) write-time
optimistic concurrency control via expected-base-commit-SHA in the
request, (b) PR-as-arbiter as serialization point.

This is a new **concurrency-control surface**. The mechanism itself
is well-understood (etag-style); but the surface didn't exist in
Phase 1.

## Honest scoring against the principle

The architecture-first principle's strongest claim — *"the architecture
never refactors because it was always designed for the population"* —
is **partially upheld** by this pressure-test:

- **Policy spine dimension: PASS.** The tier-aware enforcement point
  generalizes from reads to writes with content-only extension. No
  refactor of the existing read verbs needed; new write verbs attach
  to the same spine.
- **Surface-extension dimension: FAIL** (in the strict reading) or
  **PARTIAL PASS** (in the principled reading). Git, identity, and
  concurrency surfaces are genuinely new in Phase 2. They are not
  refactors of Phase 1's existing surfaces — they are sibling-composed
  additions at new boundaries.

The principle should be REFINED to note: the surface designed for the
full population at the **declared boundary** does not refactor, but
the addition of new boundaries (new sibling-composed surfaces) is
expected work for new pipeline positions. The architecture-first claim
is about a given boundary, not about the absence of new boundaries.

This is structurally similar to how WS-DDR-025 itself works: sibling-
over-parent-child does not forbid new siblings; it requires that each
sibling sit at its own declared pipeline position. The architecture-
first principle inherits this — at each pipeline position, the surface
is designed for the full population at that position; new positions
add new surfaces.

## Recommendation: refine principle text

Update the principle doc to make this distinction explicit. Suggested
clarification (to add to the §Statement or §Operational tests
section):

> The principle governs **per-pipeline-position surface design**, not
> the absence of new pipeline positions. When a new sibling-composed
> position legitimately enters the system (e.g., the Git surface
> entering at Phase 2 for write-back arbitration), adding that
> position is expected work and is not a refactor of existing
> surfaces. The principle's claim is: at each position, the surface
> is designed for the full population THERE.

Without this refinement, instance (c) reads as a counterexample. With
it, instance (c) is a PARTIAL PASS that surfaces a needed precision in
the principle's claim.

## Cumulative pressure-test progress (updated)

| Instance | Type | Status |
|---|---|---|
| (a) Witness adapter completion (WIT-004 #5) | Structural | PASS 2026-05-27 (sibling signal) |
| (a) Witness adapter completion | Observational | PENDING (WIT-004 #5 implementation) |
| (b) Client-engagement onboarding flow | Both | NOT YET TESTED |
| (c) Phase 2 write-back design | Sketch | PARTIAL PASS 2026-05-27 (this signal) — policy spine generalizes; new boundaries (Git, identity, concurrency) require sibling-composed surface extension |
| (c) Phase 2 write-back design | Observational | PENDING (Phase 2 implementation) |

**Progress toward external articulation: ~0.6 of 3 instances** (was ~0.5 after (a) structural). The +0.1 increment reflects (c) sketch-level engagement; observational pressure-test for both (a) and (c) still pending.

## Refinement candidate for the principle — APPLIED

The pressure-test surfaced a needed refinement that, if adopted,
strengthens the principle's claim rather than weakening it. This is
the kind of refinement that comes from real pressure-testing — the
principle's strongest version requires the per-pipeline-position
qualification.

**Status: APPLIED 2026-05-27** in commit `12ff124` (coherence-engineering/main).
New §"Per-pipeline-position scope (refinement 2026-05-27)" sub-section
added under §Statement of `Core/frameworks/coherence-engineering/principles/architecture-first-content-sequenced.md`.
The refinement makes the principle precise: claim is per-pipeline-position
surface design, NOT absence-of-new-positions. New sibling-composed
positions follow WS-DDR-025; the principle says the existing
per-position surface doesn't refactor, not that the system never grows
new positions.

## Trigger

User typed "keep going" in current session — triggered execution of
the three queued items from prior response. This signal is item 2 of 3.
