---
title: Value-Term Registry & Cross-Product Chain-Audit — Operator Doc
type: reference
maturity: active
confidentiality: internal
reusability: universal
created: 2026-05-31
updated: 2026-05-31
purpose: How the cross-product value-term/outcome catch-net works — the loop, the registry schema, and who consumes it.
---

# Value-Term Registry & Cross-Product Chain-Audit

**The discipline.** A score or gate must measure the **outcome** it serves, not its
own **activity** (its run count, its handling timestamp, which model we used). A score
with no value term — or one measuring a proxy — saturates or accretes overhead and
**cannot converge**. Proven across three production failures (CVRS freshness, CVRS
breadth, the autonomy Stop-hook) and diagnosed in flight-model §1 and
`SIG-2026-05-30-cross-session-coherence`.

This is the institutionalized catch-net for that anti-pattern.

## The loop

```
  score-owner changes a score
        │  (write-through — edit the registry beside the code)
        ▼
  <product>/value-term-registry.yaml          ← source of truth, per product
        │
        ▼
  value_term_audit.py --all  (engine)          ← discovers + audits every registry
        │                                          INV-1..4 per entry
        ▼
  value_term_invariants.py   (invariant class) ← INV-VALUE-TERM-CLEAN + -COVERAGE
        │                                          exit 0/1; --emit-signal on fail
        ▼
  .intent/signals/SIG-VALUE-TERM-*-VIOLATION    ← honest-DoD signal (open) on a violation
        │
        ▼
  governance_audit.py / overwatch (nightly)     ← runs the invariant in the suite
```

**Write-through, not central.** Each product owns `value-term-registry.yaml` **beside its
score code**, so the score-owner edits it when the score changes. A monolith (one registry
in the intent repo) was the original drift defect — a cast score declared in the intent repo
never gets touched when cast changes. The auditor *discovers* registries by name; it does
not require a central list.

## Registry schema

One file per product. Top-level `scores:` is a list of entries:

| field | meaning |
|---|---|
| `id` | stable slug, unique within the product |
| `product` | owning product (cast, topography, pulse, intent, …) |
| `kind` | `score-dimension` \| `composite-score` \| `gate` |
| `measures` | `outcome` (what it serves) or `activity` (a proxy — only allowed on non-healthy entries) |
| `value_term` | names the outcome. Empty/`NONE` is a FAIL **unless** status is defect/capped with remediation |
| `outcome_signal` | the concrete signal computed (intended vs actual, if defective) |
| `activity_proxy_risk` | the proxy it could collapse to (or "none") |
| `status` | `healthy` \| `fixed` \| `capped` \| `defect` |
| `remediation` | required for `defect`/`capped`; the tracked path to the fix |
| `saturation_guard` | the detector that catches ceiling-pinning (missing → WARN on healthy score-dims) |
| `notes` | rationale, citations (`file:line`) |

### Invariants (audit mode, per entry)

- **INV-1** value term exists — empty/`NONE` fails unless defect/capped + remediation.
- **INV-2** healthy ⇒ measures outcome — `healthy` + `measures: activity` is the anti-pattern (FAIL).
- **INV-3** defect/capped ⇒ has remediation (FAIL otherwise).
- **INV-4** healthy score-dimension/composite ⇒ declares a saturation_guard (**WARN**, not FAIL).

A **tracked defect** (`status: defect|capped` + `remediation`) PASSES — it is documented, not
hidden. That is how known violations (e.g. cast `synthesis_quality`, topography `vision_align`,
pulse activity counters) coexist with a clean (exit 0) audit and the day-one zero-violation rule.

## Consumer matrix

| Consumer | Command | When | Exit semantics |
|---|---|---|---|
| One registry | `value_term_audit.py --registry FILE` | editing one product | 0 pass / 2 any FAIL |
| Whole ecosystem | `value_term_audit.py --all [ROOT]` | cross-product sweep | 0 / 2 (any registry FAIL) |
| Unregistered-score grep | `value_term_audit.py --scan PATH [--scan-strict]` | catch-net over score code | advisory (0) / 1 strict |
| **Chain-audit invariant** | `value_term_invariants.py [--emit-signal] [--json]` | nightly / overwatch | 0 all pass / 1 any fail |

`value_term_invariants.py` exposes two invariants:
- **INV-VALUE-TERM-CLEAN** — every discovered registry audits clean (WARNs don't fail it).
- **INV-VALUE-TERM-COVERAGE** — every product in `SCORE_PRODUCTS` has a registry present.

The fuzzy `--scan` grep is the **complementary advisory** catch-net for score code not yet in any
registry; it is intentionally *not* a hard invariant gate, so the invariant stays zero-violation
on day one (`feedback_invariant_zero_violation_start`).

## Adding a new scoring product

1. Create `<product>/value-term-registry.yaml` (copy a sibling's header; fill the schema above).
2. Add it to `SCORE_PRODUCTS` in `value_term_invariants.py` (so COVERAGE catches a future deletion).
3. Run `value_term_audit.py --all` → exit 0. Add a test if the product has novel score shapes.

## Files

- `value_term_audit.py` — engine (registry audit + `--all` discovery + `--scan`). Tests: `test_value_term_audit.py`.
- `value_term_invariants.py` — chain-audit invariant class. Tests: `test_value_term_invariants.py`.
- `value-term-registry.yaml` (this dir) — intent's own scores.
- `products/{cast,topography,pulse}/value-term-registry.yaml` — those products' scores.

Convention siblings: `products/cortege/engine/scripts/chain_audit/cortege_invariants.py`,
`products/library-index/chain_audit_portfolio.py` (cross-product precedent, WS-DDR-078).
