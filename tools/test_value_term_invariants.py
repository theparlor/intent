#!/usr/bin/env python3
"""
test_value_term_invariants.py — TDD suite for value_term_invariants.py

value_term_invariants.py is the CROSS-PRODUCT chain_audit invariant class that
promotes value_term_audit.py from a single-registry tool into an ecosystem-wide
governance invariant (matching the cortege_invariants.py / chain_audit_portfolio.py
convention: invariant_*() -> (passed, violations), INV-* IDs, emit_signal with
honest-DoD frontmatter, exit 0/1).

Run:
    python3 -m pytest test_value_term_invariants.py -v
"""
from __future__ import annotations

import importlib.util
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

TOOLS_DIR = Path(__file__).parent
INV_SCRIPT = TOOLS_DIR / "value_term_invariants.py"
CORE_ROOT = TOOLS_DIR.resolve().parents[2]  # tools → intent → frameworks → Core


def _import_inv():
    spec = importlib.util.spec_from_file_location("value_term_invariants", str(INV_SCRIPT))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def _write_registry(dirpath, body, name="value-term-registry.yaml"):
    p = Path(dirpath) / name
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(body, encoding="utf-8")
    return p


_CLEAN = """scores:
  - id: ok
    product: t
    kind: score-dimension
    measures: outcome
    value_term: "real outcome term"
    outcome_signal: "sig"
    activity_proxy_risk: "none"
    status: healthy
    remediation: ""
    saturation_guard: "guard.py"
    notes: ""
"""

# healthy + measures:activity + NONE value_term → INV-2 FAIL (the anti-pattern)
_DIRTY = """scores:
  - id: bad
    product: t
    kind: score-dimension
    measures: activity
    value_term: "NONE"
    outcome_signal: ""
    activity_proxy_risk: "its own firing"
    status: healthy
    remediation: ""
    saturation_guard: ""
    notes: ""
"""


# ---------------------------------------------------------------------------
# INV-VALUE-TERM-CLEAN: every discovered registry audits clean
# ---------------------------------------------------------------------------

class TestInvRegistriesAuditClean(unittest.TestCase):

    def test_clean_root_passes(self):
        mod = _import_inv()
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            _write_registry(root / "a", _CLEAN)
            _write_registry(root / "b", _CLEAN)
            passed, violations = mod.invariant_registries_audit_clean(root)
            self.assertTrue(passed, msg=f"Expected pass, violations: {violations}")
            self.assertEqual(violations, [])

    def test_dirty_root_fails_and_names_registry(self):
        mod = _import_inv()
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            _write_registry(root / "good", _CLEAN)
            _write_registry(root / "baddir", _DIRTY)
            passed, violations = mod.invariant_registries_audit_clean(root)
            self.assertFalse(passed, msg="Expected fail for dirty registry")
            self.assertTrue(any("baddir" in v for v in violations),
                            msg=f"Violation should name the failing registry: {violations}")


# ---------------------------------------------------------------------------
# INV-VALUE-TERM-COVERAGE: every score-product has a registry present
# ---------------------------------------------------------------------------

class TestInvScoreProductCoverage(unittest.TestCase):

    def test_all_present_passes(self):
        mod = _import_inv()
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            products = {"cast": "cast/value-term-registry.yaml",
                        "pulse": "pulse/value-term-registry.yaml"}
            _write_registry(root / "cast", _CLEAN)
            _write_registry(root / "pulse", _CLEAN)
            passed, violations = mod.invariant_score_product_coverage(root, products)
            self.assertTrue(passed, msg=f"violations: {violations}")

    def test_missing_registry_fails_and_names_product(self):
        mod = _import_inv()
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            products = {"cast": "cast/value-term-registry.yaml",
                        "pulse": "pulse/value-term-registry.yaml"}
            _write_registry(root / "cast", _CLEAN)
            # pulse registry deliberately absent
            passed, violations = mod.invariant_score_product_coverage(root, products)
            self.assertFalse(passed)
            self.assertTrue(any("pulse" in v for v in violations),
                            msg=f"Violation should name the missing product: {violations}")


# ---------------------------------------------------------------------------
# emit_signal: honest closure-DoD frontmatter
# ---------------------------------------------------------------------------

class TestEmitSignalHonestDoD(unittest.TestCase):

    def test_emit_signal_has_closure_dod_keys(self):
        mod = _import_inv()
        with tempfile.TemporaryDirectory() as d:
            sigdir = Path(d) / "signals"
            path = mod.emit_signal(sigdir, "INV-VALUE-TERM-CLEAN", ["registry X: untracked defect"])
            self.assertTrue(path.exists(), msg="emit_signal must write a file")
            text = path.read_text(encoding="utf-8")
            for key in ("upstream_control_path:", "catch_mechanism:", "pipeline_survival:"):
                self.assertIn(key, text, msg=f"Signal frontmatter missing {key}\n{text}")
            self.assertIn("registry X: untracked defect", text,
                          msg="Signal must list the violations")


# ---------------------------------------------------------------------------
# Day-one zero-violation guarantee (feedback_invariant_zero_violation_start)
# ---------------------------------------------------------------------------

class TestDayOneZeroViolations(unittest.TestCase):
    """Against the REAL Core ecosystem, both invariants PASS on day one.
    The 3 known violations are registered as tracked defects (defect+remediation),
    so they do not FAIL the audit — they are tracked, not untracked."""

    def test_real_ecosystem_audits_clean(self):
        mod = _import_inv()
        passed, violations = mod.invariant_registries_audit_clean(CORE_ROOT)
        self.assertTrue(passed,
                        msg=f"Real ecosystem has UNTRACKED value-term defects: {violations}")

    def test_real_coverage_complete(self):
        mod = _import_inv()
        passed, violations = mod.invariant_score_product_coverage(CORE_ROOT)
        self.assertTrue(passed,
                        msg=f"A score-product is missing its registry: {violations}")


# ---------------------------------------------------------------------------
# main() exit codes
# ---------------------------------------------------------------------------

class TestMainExitCodes(unittest.TestCase):

    def test_main_real_exit_0(self):
        """Running against the real ecosystem (default root) exits 0 on day one."""
        r = subprocess.run([sys.executable, str(INV_SCRIPT)], capture_output=True, text=True)
        self.assertEqual(r.returncode, 0, msg=f"stdout:{r.stdout}\nstderr:{r.stderr}")

    def test_main_json_flag(self):
        r = subprocess.run([sys.executable, str(INV_SCRIPT), "--json"],
                           capture_output=True, text=True)
        self.assertEqual(r.returncode, 0, msg=f"{r.stdout}\n{r.stderr}")
        self.assertIn("INV-VALUE-TERM-CLEAN", r.stdout)


if __name__ == "__main__":
    unittest.main(verbosity=2)
