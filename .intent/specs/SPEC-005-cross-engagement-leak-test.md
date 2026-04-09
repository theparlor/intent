---
id: SPEC-005
title: "Cross-engagement leak test in CI — assert knowledge engine redaction is not aspirational"
status: draft
version: 1.0
author: brien
created_date: 2026-04-09T19:40:00Z
approved_date:
intent: INT-009
source_signals: [SIG-051]
related_specs: [SPEC-004]
related_decisions: [DEC-20260409-01, WS-DDR-005]
priority: P0
interim_ship: "tests/test_engagement_isolation.py pytest scaffold + workflow (2026-04-09) — smoke test only, needs engagement fixtures"
---

# SPEC-005 — Cross-Engagement Leak Test in CI

## Problem Statement

Per INT-009 P0 #3 and the ARB panel 2026-04-09 finding:

> **"Cross-engagement leak test in CI — attempts query from engagement A's
> context, asserts zero B data returns. Until this exists, D11 (redaction
> at tool level) is aspirational."**

The Knowledge Engine architecture (WS-DDR-005, WS-DDR-010, Decision #18
in CLAUDE.md) claims that:

- Core/ contains universal IP available to all engagements
- Each engagement has bounded knowledge scoped to itself
- Queries scoped to engagement A must NEVER return engagement B data
- The federation principle is "inherit down, promote up, never leak sideways"
- Redaction is enforced at the tool level (the MCP server applies
  confidentiality projection automatically based on engagement context)

None of this is currently verified. The claim "redaction at tool level"
is architecturally stated but not tested. Per the panel's diagnosis: it
is aspirational until a test can prove it.

This is foundational for multi-tenant operation. Without the leak test:
- Any claim that engagement data is isolated is unverifiable
- Any client-confidentiality commitment in an engagement agreement
  rests on a behavior that hasn't been tested
- The blue-green/feature-flag prerequisites from DEC-20260409-02 answer
  5d presume measurable isolation that nothing currently measures

## Solution Description

Build a pytest test suite that verifies engagement isolation via the
Knowledge Engine's query layer:

1. **Fixture setup** — create three test knowledge trees:
   - `tests/fixtures/core-knowledge/` — universal (Core/ equivalent)
   - `tests/fixtures/engagement-alpha/` — scoped to "Alpha"
   - `tests/fixtures/engagement-beta/` — scoped to "Beta"

   Each contains marker documents with distinctive content (e.g.,
   "ALPHA_SECRET_XYZ", "BETA_SECRET_PQR") that the leak test can grep for.

2. **Query simulation** — invoke the Knowledge Engine's query path with
   engagement context set to "Alpha". The test asserts:
   - Alpha's marker strings ARE in the result
   - Core's marker strings ARE in the result
   - Beta's marker strings ARE NOT in the result (the key assertion)

3. **Reverse direction** — query with context "Beta":
   - Beta's markers IN
   - Core's markers IN
   - Alpha's markers OUT

4. **Unscoped query** — query with no engagement context:
   - Core's markers IN
   - Alpha's markers OUT
   - Beta's markers OUT

5. **Tool-level redaction** — verify that the MCP server's response
   payload itself does not contain Alpha markers when Beta's tool is
   invoked. This is the tool-level projection check.

6. **CI integration** — the tests run on every push to main AND on every
   PR via GitHub Actions. A failure blocks the build.

## Interim ship (2026-04-09)

Before the full fixture + assertion suite is built, a scaffold ships:

- `tests/__init__.py` — pytest package marker
- `tests/test_engagement_isolation.py` — pytest file with the intended
  test structure and TWO smoke tests that pass today:
  1. `test_fixture_directories_exist` — will fail until fixtures created
  2. `test_core_marker_not_leaked_to_engagement` — placeholder that
     XFAILs until the KE query layer is wired
- `.github/workflows/leak-test.yml` — GitHub Actions workflow that runs
  `pytest tests/test_engagement_isolation.py`
- Tests marked with `@pytest.mark.xfail(strict=False, reason="SPEC-005 in draft")` so CI doesn't fail on the missing fixtures

This establishes the CI machinery so that when fixtures and the real
query layer land, the test starts enforcing automatically. It does NOT
claim engagement isolation is verified in v1.0.

## Implementation plan

### Phase 1 — Fixture design (0.5 day)

1. Define fixture document structure:
```
tests/fixtures/
├── core-knowledge/
│   ├── personas/
│   │   └── universal-persona.md         # CORE_MARKER_X7Q2
│   └── templates/
│       └── ddr.md                       # CORE_MARKER_M4K9
├── engagement-alpha/
│   ├── knowledge/
│   │   └── dossier-alpha.md             # ALPHA_SECRET_XYZ, should_not_leak
│   └── from-client/
│       └── alpha-client-notes.md        # ALPHA_CLIENT_QRS
└── engagement-beta/
    ├── knowledge/
    │   └── dossier-beta.md              # BETA_SECRET_PQR
    └── from-client/
        └── beta-client-notes.md         # BETA_CLIENT_MNL
```

2. Marker strings are deliberately distinctive to enable grep-based
   post-query leak detection.

### Phase 2 — Query layer wiring (1 day)

3. Identify the KE query entrypoint. Candidates:
   - `servers/knowledge.py` function that scopes queries by engagement
   - A CLI command `intent-knowledge query --engagement alpha`
   - An MCP tool call pattern

4. Wire the test to invoke the chosen entrypoint with engagement context.

### Phase 3 — Assertion suite (1 day)

5. Write the four test cases from the Solution section.
6. Each test runs a real query and asserts marker presence/absence.
7. Tests fail hard on any leak (no xfail).

### Phase 4 — CI integration (0.5 day)

8. Update `.github/workflows/leak-test.yml` to:
   - Check out the repo
   - Install Python + test dependencies (pytest, whatever KE needs)
   - Run `pytest tests/test_engagement_isolation.py -v`
   - Fail the build on any test failure
9. Optional: make the test a PR status check required for merge.

### Phase 5 — Documentation (0.5 day)

10. Update CLAUDE.md Key Decisions #18 (redaction at tool level) to
    link to this test as the verification artifact.
11. Add to `.intent/decisions/` a decision record stating that redaction
    is now test-verified, not aspirational.

## Acceptance Criteria

All criteria blocking until the full ship (not v1.0 scaffold):

- [ ] Fixture tree in `tests/fixtures/` exists with marker strings
- [ ] Query layer entrypoint identified and callable from pytest
- [ ] Test 1 (Alpha context): asserts Alpha + Core markers present,
  Beta markers absent. PASSES.
- [ ] Test 2 (Beta context): reverse of Test 1. PASSES.
- [ ] Test 3 (unscoped): only Core markers present. PASSES.
- [ ] Test 4 (tool-level redaction): MCP tool response does not include
  other engagement's markers. PASSES.
- [ ] CI workflow runs the test suite on every push to main
- [ ] CI workflow runs the test suite on every PR
- [ ] Failed tests block the build
- [ ] CLAUDE.md updated with link to this test as verification artifact
- [ ] At least one deliberate leak test (e.g., inject a fake leak and
  verify the test catches it) — don't trust a test that has never failed

## Out of Scope

- **Adversarial fuzzing.** v1.0 uses fixed marker strings. A follow-up
  could generate random markers on each run to defeat any hardcoded
  exemptions.
- **Performance regression testing.** The test asserts isolation, not
  latency.
- **Cross-surface leak test.** v1.0 tests the query layer only. The
  GitHub Actions event emitter, the CLI, and other surfaces have their
  own isolation concerns that will need their own tests.
- **Migration of existing `knowledge/` content into fixtures.** Fixtures
  are synthetic for test isolation — they must not reference real
  engagement content.

## Test Scenarios

Beyond the 4 core tests above:

5. **Symlink escape** — put a symlink in engagement A that points into
   engagement B. Verify the query layer does not follow it.

6. **Path traversal** — attempt to query with engagement context
   `../engagement-beta` and verify no Beta data is returned.

7. **Case sensitivity** — query with `Alpha`, `ALPHA`, `alpha`. Verify
   consistent behavior (either all work or all fail).

8. **Empty engagement** — query with an empty engagement string and
   verify it does not match a real engagement named "".

9. **Unicode collision** — create a fake engagement named `alρha` (with
   Greek rho) and verify queries for `alpha` don't return it.

## Dependencies

- **pytest** (add to `requirements.txt` if not present)
- **servers/knowledge.py** — the current KE query entrypoint
- **Fixture tree** — to be created in `tests/fixtures/`

## Open Questions

1. **Is the KE query layer actually in `servers/knowledge.py`, or is it
   split across multiple modules?** Need to trace through the current
   code to identify the single chokepoint where the test should inject.

2. **Does the KE have engagement scoping implemented yet, or is this
   test going to fail immediately?** If the scoping doesn't exist,
   the test + implementation are the same ship, not separable.

3. **How does engagement context propagate?** Environment variable?
   Function argument? Thread-local? The test has to set it the same way
   real callers set it.

4. **Should the test run against a real engagement knowledge tree, or
   only against synthetic fixtures?** Synthetic is safer (no risk of
   real leakage during testing) but may miss real-world edge cases.
   Recommendation: synthetic + a separate read-only smoke test against
   real engagements that does not print/log contents.

## Lineage

- **INT-009 P0 #3** — the architecture hardening backlog entry
- **SIG-051** — the consolidated architecture hardening signal
- **WS-DDR-005** — Federation: inherit down, promote up, never leak
- **WS-DDR-010** — Persona federation: universal vs. engagement-scoped
- **CLAUDE.md Decision #18** — Redaction at tool level
- **ARB panel 2026-04-09** — flagged this as "aspirational until tested"
- **DEC-20260409-02 Answer 5d** — measurability-as-prerequisite principle
- **Amy Edmondson via panel-review always-on voice** — any mechanism
  applied to humans must be testably safe; engagement isolation is a
  human-safety concern when client-confidential data is involved
