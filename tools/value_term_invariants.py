#!/usr/bin/env python3
"""
value_term_invariants.py — cross-product value-term chain_audit invariant class.

WHY THIS EXISTS
  The value-term/outcome discipline (a score must measure the OUTCOME it serves,
  not its own ACTIVITY) was proven across three production failures and captured
  in value_term_audit.py + per-product value-term-registry.yaml files. This module
  PROMOTES that catch-net into a cross-product chain_audit invariant class — the
  same governance shape as cortege_invariants.py and chain_audit_portfolio.py — so
  it can run in the nightly/overwatch invariant suite and emit honest-DoD signals.

  It institutionalizes the anti-pattern the whole road-readiness arc proved
  (handoff 2026-05-31 §1; flight-model §1; SIG-2026-05-30-cross-session-coherence §1).

INVARIANTS
  INV-VALUE-TERM-CLEAN
    Every per-product value-term-registry.yaml discovered under root audits clean
    (no healthy-but-activity score, no untracked defect). Known defects registered
    as status: defect|capped WITH remediation are TRACKED, not violations — so the
    invariant fires zero violations on day one (feedback_invariant_zero_violation_start).

  INV-VALUE-TERM-COVERAGE
    Every product known to compute a decision-driving score (SCORE_PRODUCTS) has a
    value-term-registry.yaml present. Catches: a new scoring product shipped without
    a registry, or a registry deleted. Structural/deterministic (cf. cortege
    INV-CORTEGE-POLICY-COMPLETENESS).

  (The fuzzy --scan grep in value_term_audit.py is the complementary ADVISORY
   catch-net for unregistered score code; it is intentionally not a hard gate here,
   so the invariant stays zero-violation on day one.)

USAGE
  python3 value_term_invariants.py [--root PATH] [--emit-signal] [--json]
  Exit 0 = all invariants pass · 1 = one or more failed.

COMPOSES WITH
  - value_term_audit.py            — the engine (discover_registries + _audit_registry)
  - cortege_invariants.py          — same invariant signature, per-product scope
  - library-index/chain_audit_portfolio.py — cross-product precedent (WS-DDR-078)
  - org-design-tooling governance_audit.py — the intended nightly consumer
"""
from __future__ import annotations

import argparse
import json
import sys
from datetime import date
from pathlib import Path

# Import the engine (sibling file). Add tools/ to sys.path so this works from any CWD.
sys.path.insert(0, str(Path(__file__).resolve().parent))
import value_term_audit as vta  # noqa: E402


# tools → intent → frameworks → Core
DEFAULT_ROOT = Path(__file__).resolve().parents[3]
DEFAULT_SIGNALS_DIR = Path(__file__).resolve().parents[1] / ".intent" / "signals"

# Products known to compute decision-driving scores → each MUST own a registry.
# Paths are relative to the ecosystem root. Extend this when a new scoring product ships.
SCORE_PRODUCTS = {
    "cast": "products/cast/value-term-registry.yaml",
    "topography": "products/topography/value-term-registry.yaml",
    "pulse": "products/pulse/value-term-registry.yaml",
    "intent": "frameworks/intent/tools/value-term-registry.yaml",
}


# ---------------------------------------------------------------------------
# INV-VALUE-TERM-CLEAN
# ---------------------------------------------------------------------------

def invariant_registries_audit_clean(root: str | Path) -> tuple[bool, list[str]]:
    """Every discovered per-product registry audits clean (zero FAILs).

    Returns (passed, violations). Each violation is prefixed with the registry path.
    WARNs (e.g. missing saturation_guard) are advisory and do NOT fail the invariant.
    """
    violations: list[str] = []
    for reg in vta.discover_registries(root):
        fails, _warns, _count = vta._audit_registry(reg)
        for f in fails:
            violations.append(f"INV-VALUE-TERM-CLEAN: {reg}: {f}")
    return len(violations) == 0, violations


# ---------------------------------------------------------------------------
# INV-VALUE-TERM-COVERAGE
# ---------------------------------------------------------------------------

def invariant_score_product_coverage(
    root: str | Path, products: dict[str, str] | None = None
) -> tuple[bool, list[str]]:
    """Every score-product in the manifest has a registry present under root.

    Returns (passed, violations).
    """
    products = products if products is not None else SCORE_PRODUCTS
    root = Path(root)
    violations: list[str] = []
    for name, rel in sorted(products.items()):
        if not (root / rel).exists():
            violations.append(
                f"INV-VALUE-TERM-COVERAGE: score-product '{name}' has no registry at "
                f"{rel} — a product that computes a decision-driving score must own a "
                f"value-term-registry.yaml (write-through)."
            )
    return len(violations) == 0, violations


# ---------------------------------------------------------------------------
# Signal emission (honest closure-DoD frontmatter)
# ---------------------------------------------------------------------------

def emit_signal(signals_dir: str | Path, invariant_id: str, violations: list[str]) -> Path:
    """Emit a SIG-VALUE-TERM-*-VIOLATION signal with honest-DoD frontmatter."""
    signals_dir = Path(signals_dir)
    signals_dir.mkdir(parents=True, exist_ok=True)
    today = date.today().isoformat()
    path = signals_dir / f"SIG-VALUE-TERM-{invariant_id}-VIOLATION-{today}.md"

    body = f"""---
id: SIG-VALUE-TERM-{invariant_id}-VIOLATION-{today}
product: intent
type: invariant-violation
status: open
created: {today}
invariant: {invariant_id}
upstream_control_path: "Core/frameworks/intent/tools/value_term_invariants.py + per-product value-term-registry.yaml (write-through; each score-owner declares its scores beside the code)"
catch_mechanism: "value_term_invariants.py {invariant_id} + test_value_term_invariants.py — run in the nightly/overwatch invariant suite"
pipeline_survival: "Registries are declarative data read at audit time; no pipeline stage (render_all etc.) wipes them. A violation surfaces governance debt and does not block product execution."
---

# {invariant_id} Violation — {today}

## Violations

"""
    for v in violations:
        body += f"- {v}\n"

    body += f"""
## Required action

Register the score in the owning product's value-term-registry.yaml (naming its
value term + whether it measures outcome or activity), or fix the score so it
measures the outcome. Re-run `python3 value_term_invariants.py` to verify. Update
this signal to `status: resolved` (with upstream_control_path + catch_mechanism)
once passing.

*Auto-emitted by value_term_invariants.py {today}.*
"""
    path.write_text(body, encoding="utf-8")
    return path


# ---------------------------------------------------------------------------
# main
# ---------------------------------------------------------------------------

def main(argv=None) -> int:
    ap = argparse.ArgumentParser(
        description="Cross-product value-term chain_audit invariant class.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )
    ap.add_argument("--root", default=str(DEFAULT_ROOT),
                    help="Ecosystem root to audit (default: Core/).")
    ap.add_argument("--emit-signal", action="store_true",
                    help="Emit a signal to .intent/signals/ on failure.")
    ap.add_argument("--signals-dir", default=str(DEFAULT_SIGNALS_DIR),
                    help="Where to write violation signals (default: intent/.intent/signals/).")
    ap.add_argument("--json", action="store_true", help="Output results as JSON.")
    args = ap.parse_args(argv)

    root = args.root
    checks = [
        ("INV-VALUE-TERM-CLEAN", lambda: invariant_registries_audit_clean(root)),
        ("INV-VALUE-TERM-COVERAGE", lambda: invariant_score_product_coverage(root)),
    ]

    results: dict[str, dict] = {}
    all_passed = True
    for inv_id, fn in checks:
        passed, violations = fn()
        results[inv_id] = {"passed": passed, "violations": violations}
        if not passed:
            all_passed = False
            if args.emit_signal:
                sig = emit_signal(args.signals_dir, inv_id, violations)
                results[inv_id]["signal_emitted"] = str(sig)

    if args.json:
        print(json.dumps({"root": str(root), "passed": all_passed, "results": results}, indent=2))
    else:
        print("=" * 78)
        print("  VALUE-TERM CHAIN-AUDIT — cross-product invariant class")
        print(f"  Root: {root}")
        print("=" * 78)
        for inv_id, r in results.items():
            print(f"\n[{'PASS' if r['passed'] else 'FAIL'}] {inv_id}")
            for v in r["violations"]:
                print(f"       {v}")
        if all_passed:
            print("\n✓ All value-term invariants PASS — every score measures an outcome "
                  "(or is a tracked defect), every score-product has a registry.")
        else:
            failing = [k for k, v in results.items() if not v["passed"]]
            print(f"\n✗ {len(failing)} invariant(s) FAILED: {', '.join(failing)}")

    return 0 if all_passed else 1


if __name__ == "__main__":
    sys.exit(main())
