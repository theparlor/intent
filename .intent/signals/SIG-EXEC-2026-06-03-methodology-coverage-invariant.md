---
id: SIG-EXEC-2026-06-03-methodology-coverage-invariant
product: intent
type: execution-report
status: resolved
created: 2026-06-03
upstream_control_path: |
  Core/frameworks/intent/tools/methodology_coverage_invariant.py — automated chain_audit
  verifying every Forge skill domain has methodology ancestry (INV-METHODOLOGY-COVERAGE)
  and every `methodology:` pointer resolves (INV-METHODOLOGY-NODANGLING). Plus the 33
  newly-wired Forge SKILL.md `methodology:` pointers and the modules they reference.
catch_mechanism: |
  methodology_coverage_invariant.py (hard COVERAGE + NODANGLING; advisory WIRING,
  --strict-wiring promotes to hard) + test_methodology_coverage_invariant.py (7 tests,
  all pass). Runnable in the nightly/overwatch suite. This IS the automated catch-net
  whose ABSENCE was flagged in SIG-AUDIT-2026-05-20 and
  SIG-EXEC-2026-05-20-ML-SPEC-001-CONT follow-up #1 — now closed.
pipeline_survival: |
  SAFE. The invariant is a read-only auditor; methodology modules + skill frontmatter are
  source-of-truth, not pipeline outputs. Zero-violation start verified — hard invariants
  PASS against the live tree on day one (feedback_invariant_zero_violation_start).
addresses:
  - SIG-AUDIT-2026-05-20 (methodology-library): automated coverage audit follow-up
  - SIG-EXEC-2026-05-20-ML-SPEC-001-CONT follow-up #1
  - ML-SPEC-005 (Forge methodology wiring) — substantially executed
---

# SIG-EXEC-2026-06-03 — Methodology Coverage Invariant + Forge Wiring

Executes both follow-ups from the critique-extraction session (SIG-EXEC-2026-06-03-critique-domain-extraction, methodology-library repo).

## #1 — Automated chain_audit invariant (the missing catch-net, now built)

`Core/frameworks/intent/tools/methodology_coverage_invariant.py` — pure stdlib (no pyyaml; runs anywhere the overwatch/nightly suite runs). Same governance shape as `value_term_invariants.py` / `repos_clean_invariant.py`.

| Invariant | Kind | State (2026-06-03) |
|-----------|------|--------------------|
| INV-METHODOLOGY-COVERAGE | hard | **PASS** — every skill domain (≥1 SKILL.md) has ≥1 methodology module. Zero-violation; the critique extraction closed the last domain gap. |
| INV-METHODOLOGY-NODANGLING | hard | **PASS** — every `methodology:` pointer resolves to a real module. |
| INV-METHODOLOGY-WIRING | advisory WARN (`--strict-wiring` → hard) | 41 → **8** unwired + 1 deferred. Advisory so the hard suite is zero-violation on day one. |

Tests: `test_methodology_coverage_invariant.py` — 7/7 pass (coverage pass/fail, non-skill-dir ignore, dangling detect, deferred skip, pointer resolve). Registered in `Core/TOOLS-INDEX.md`.

## #2 — Forge skill wiring (ML-SPEC-005)

33 of 41 unwired skills now carry a `methodology:` pointer to their canonical module:
- **26 deterministic** — coaching (hub+specific), competitive (1:1), operations (1:1; docx-edit excluded), organization (all → information-architecture), planning (1:1), research/freshen → research-core, strategy (all → strategy-core; company-strategy-review → product-strategy).
- **7 meta (judgment)** — budget-calculator→context-budget, intent-orchestrator→skill-graph, overwatch→governance-spec, scout→autonomous-investigation, session-extract→intent-journal, signal-detector→signal-scoring, skill-intake→skill-authoring-patterns.

(Note: scout/ is an untracked skill from a concurrent session; its pointer is on disk and rides with that session's commit, so 32 are committed in the Forge commit here.)

## Honestly left unwired (advisory — NOT forced)

8 meta operational tools with no clean single-module ancestry: **cortege, daily-digest, harvest-gate, output-hygiene, panel-review, prepare-to-share, product-open-sweep, weekly-summary**. Plus **operations/docx-edit** (extraction documented-deferred, Rule-of-Three not met). Forcing pointers here would be dishonest; the invariant tracks them as advisory WARNs. If/when modules are authored for these (e.g. a fetch-fabric or digest methodology hits Rule-of-Three), wiring them drives WIRING toward zero, at which point `--strict-wiring` can be enabled in the suite.

## Verification (real output)

- `python3 methodology_coverage_invariant.py` → hard PASS, EXIT 0, WIRING 8 unwired + 1 deferred.
- `python3 test_methodology_coverage_invariant.py` → 7/7 pass.
