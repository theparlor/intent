---
id: SIG-INTENT-DIST-VENDORED-REGISTRY-2026-07-02
date: 2026-07-02
severity: low
status: resolved
upstream_control_path: Core/frameworks/intent/tools/value_term_audit.py (_EXCLUDE_DIR_PARTS includes 'dist' in discover_registries)
catch_mechanism: test_value_term_audit.py::TestDiscoverRegistries::test_discover_skips_dist_build_output
pipeline_survival: exclusion lives in the discovery function itself; any future rglob run applies it. Fixture test regresses loudly if the set is narrowed.
related: SIG-INTENT-STATUS-ENUM-2026-07-02
---

# Vendored build-output registry double-audited by --all

## Notice
`discover_registries()` excluded {.venv, venv, .worktrees, node_modules,
__pycache__, .git} but not build-output dirs. The forge bundle at
`Core/products/forge/outputs/dist/voices-panel/Core/products/voices/value-term-registry.yaml`
is a vendored copy of the voices registry and was discovered and audited by
`--all` (12 registries reported where 11 are real), contradicting the module's
own comment: "Never audit vendored / worktree / cache copies — they are not
the source of truth."

## Decision
Add `dist` to `_EXCLUDE_DIR_PARTS` rather than a path-substring rule like
`outputs/dist`. Rationale: `dist` is the universal build-output convention;
a write-through registry lives beside its score-owning source, never in build
output. Excluding all of `outputs/` was rejected as broader than the evidence
(some products may legitimately keep source-of-truth material under outputs/).

## Execute / Observe
RED-first fixture test reproducing the forge/voices path shape failed as
expected (2 found where 1 expected), fix made it pass. Full suites green
(45 tests, test_value_term_audit + test_value_term_invariants). Live `--all`:
11 registries, 0 FAIL, vendored path no longer listed.

Observed during SIG-INTENT-STATUS-ENUM-2026-07-02 (status closed-enum fix).
