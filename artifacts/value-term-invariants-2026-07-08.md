---
title: Value-term chain-audit invariant result, 2026-07-08
type: analysis
maturity: final
created: 2026-07-08
purpose: Dated result artifact for value_term_invariants.py. The 2026-07-08 scout global sweep found no dated result artifact anywhere despite the tool existing; this closes that witnessed-evidence gap.
---

# Value-Term Invariant Run, 2026-07-08

Runner: /Users/brien/Workspaces/Core/frameworks/intent/tools/value_term_invariants.py
Interpreter: /Users/brien/Workspaces/Core/products/cast/.venv/bin/python (intent framework carries no venv; nearest component venv used per venv-guard)
Root scanned: /Users/brien/Workspaces/Core

## Result

```
[PASS] INV-VALUE-TERM-CLEAN

[PASS] INV-VALUE-TERM-COVERAGE

All value-term invariants PASS: every score measures an outcome (or is a tracked
defect), every score-product has a registry.
```

## Context

Registry coverage at run time: 10 products carry a value-term-registry.yaml
(cast 7 entries, gauge 6, pulse 3, topography 2, library-index 2, voices 2,
loom 1, cortege 1, org-design-tooling 1, forge 1; 26 total).

Re-run cadence: overwatch and scout both read this artifact class; regenerate by
re-running the tool and writing a new dated file alongside this one.
