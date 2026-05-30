#!/usr/bin/env python3
"""
test_value_term_audit.py — TDD suite for value_term_audit.py

Anti-pattern under test:
  A score or gate that measures its own ACTIVITY (a proxy) instead of the
  OUTCOME it serves — with no value term — saturates or accretes overhead
  and cannot converge. (flight-model §1; SIG-2026-05-30-cross-session-coherence §1)

Run:
    python3 test_value_term_audit.py
    python3 -m pytest test_value_term_audit.py -v
"""
from __future__ import annotations

import importlib
import importlib.util
import os
import subprocess
import sys
import tempfile
import textwrap
import unittest
from pathlib import Path

TOOLS_DIR = Path(__file__).parent
REGISTRY_PATH = TOOLS_DIR / "value-term-registry.yaml"
AUDIT_SCRIPT = TOOLS_DIR / "value_term_audit.py"


# ---------------------------------------------------------------------------
# helpers
# ---------------------------------------------------------------------------

def _run_audit(*extra_args, registry_text=None, registry_file=None):
    """
    Invoke value_term_audit.py as a subprocess.
    Returns (returncode, stdout, stderr).
    If registry_text is given, write it to a temp file and pass --registry.
    If registry_file is given, pass it directly.
    """
    cmd = [sys.executable, str(AUDIT_SCRIPT)]
    if registry_text is not None:
        tf = tempfile.NamedTemporaryFile(
            mode="w", suffix=".yaml", delete=False, encoding="utf-8"
        )
        tf.write(registry_text)
        tf.flush()
        tf.close()
        cmd += ["--registry", tf.name]
    elif registry_file is not None:
        cmd += ["--registry", str(registry_file)]
    cmd += list(extra_args)

    result = subprocess.run(
        cmd, capture_output=True, text=True
    )
    return result.returncode, result.stdout, result.stderr


def _minimal_healthy(
    id="test-score",
    kind="score-dimension",
    measures="outcome",
    value_term="some real value term",
    status="healthy",
    remediation="",
    saturation_guard="some_guard.py",
):
    lines = [
        "scores:",
        f"  - id: {id}",
        f"    product: test",
        f"    kind: {kind}",
        f"    measures: {measures}",
        f"    value_term: \"{value_term}\"",
        f"    outcome_signal: \"some signal\"",
        f"    activity_proxy_risk: \"none\"",
        f"    status: {status}",
        f"    remediation: \"{remediation}\"",
        f"    saturation_guard: \"{saturation_guard}\"",
        f"    notes: \"\"",
    ]
    return "\n".join(lines) + "\n"


# ---------------------------------------------------------------------------
# INV-1: value term exists
# ---------------------------------------------------------------------------

class TestINV1ValueTermExists(unittest.TestCase):

    def test_healthy_with_real_value_term_passes(self):
        """Healthy entry with a non-empty, non-NONE value_term → exit 0."""
        rc, out, err = _run_audit(registry_text=_minimal_healthy())
        self.assertEqual(rc, 0, msg=f"Expected exit 0\nstdout: {out}\nstderr: {err}")

    def test_healthy_with_empty_value_term_fails(self):
        """Healthy entry with empty value_term → exit 2, mentions 'no value term'."""
        yaml = _minimal_healthy(value_term="")
        rc, out, err = _run_audit(registry_text=yaml)
        self.assertEqual(rc, 2, msg=f"Expected exit 2\nstdout: {out}\nstderr: {err}")
        combined = (out + err).lower()
        self.assertIn("no value term", combined,
                      msg=f"Expected 'no value term' in output\n{out}\n{err}")

    def test_healthy_with_NONE_value_term_fails(self):
        """Healthy entry with value_term starting with 'NONE' → exit 2."""
        yaml = _minimal_healthy(value_term="NONE — 0.00 of formula measures value")
        rc, out, err = _run_audit(registry_text=yaml)
        self.assertEqual(rc, 2, msg=f"Expected exit 2\nstdout: {out}\nstderr: {err}")
        combined = (out + err).lower()
        self.assertIn("no value term", combined,
                      msg=f"Expected 'no value term' in output\n{out}\n{err}")

    def test_defect_with_no_value_term_and_remediation_passes(self):
        """
        Defect entry with value_term=NONE is allowed IF remediation is non-empty.
        A known defect with a tracked fix is allowed; an undocumented one is not.
        """
        yaml = _minimal_healthy(
            value_term="NONE — superseded by flight model",
            status="defect",
            remediation="superseded by autonomy-flight-model-v1-DRAFT.md",
        )
        rc, out, err = _run_audit(registry_text=yaml)
        self.assertEqual(rc, 0, msg=f"Expected exit 0\nstdout: {out}\nstderr: {err}")

    def test_capped_with_no_value_term_and_remediation_passes(self):
        """Capped entry with NONE value_term + remediation → allowed (exit 0)."""
        yaml = _minimal_healthy(
            value_term="NONE",
            status="capped",
            remediation="lexical-layer-freeze.yaml + Layer 4.2",
        )
        rc, out, err = _run_audit(registry_text=yaml)
        self.assertEqual(rc, 0, msg=f"Expected exit 0\nstdout: {out}\nstderr: {err}")


# ---------------------------------------------------------------------------
# INV-2: measures outcome
# ---------------------------------------------------------------------------

class TestINV2MeasuresOutcome(unittest.TestCase):

    def test_healthy_measures_outcome_passes(self):
        """Healthy + measures:outcome → exit 0."""
        rc, out, err = _run_audit(registry_text=_minimal_healthy(measures="outcome"))
        self.assertEqual(rc, 0, msg=f"{out}\n{err}")

    def test_healthy_measures_activity_fails(self):
        """Healthy + measures:activity → exit 2, mentions 'activity'."""
        yaml = _minimal_healthy(measures="activity")
        rc, out, err = _run_audit(registry_text=yaml)
        self.assertEqual(rc, 2, msg=f"Expected exit 2\nstdout: {out}\nstderr: {err}")
        combined = (out + err).lower()
        self.assertIn("activity", combined,
                      msg=f"Expected 'activity' in output\n{out}\n{err}")

    def test_defect_measures_activity_allowed_with_remediation(self):
        """Defect + measures:activity + remediation → not a new FAIL (INV-2 only applies to healthy)."""
        yaml = _minimal_healthy(
            measures="activity",
            status="defect",
            remediation="being fixed in v2",
        )
        rc, out, err = _run_audit(registry_text=yaml)
        self.assertEqual(rc, 0, msg=f"Expected exit 0 for defect entry\n{out}\n{err}")


# ---------------------------------------------------------------------------
# INV-3: defect tracked
# ---------------------------------------------------------------------------

class TestINV3DefectTracked(unittest.TestCase):

    def test_defect_without_remediation_fails(self):
        """Defect entry with no remediation → exit 2."""
        yaml = _minimal_healthy(
            status="defect",
            remediation="",
            value_term="some term",
        )
        rc, out, err = _run_audit(registry_text=yaml)
        self.assertEqual(rc, 2, msg=f"Expected exit 2\nstdout: {out}\nstderr: {err}")

    def test_defect_with_remediation_passes(self):
        """Defect entry with remediation → exit 0."""
        yaml = _minimal_healthy(
            status="defect",
            remediation="fix tracked in SIG-XYZ",
            value_term="some term",
        )
        rc, out, err = _run_audit(registry_text=yaml)
        self.assertEqual(rc, 0, msg=f"Expected exit 0\nstdout: {out}\nstderr: {err}")

    def test_capped_without_remediation_fails(self):
        """Capped entry with no remediation → exit 2."""
        yaml = _minimal_healthy(
            status="capped",
            remediation="",
            value_term="NONE",
        )
        rc, out, err = _run_audit(registry_text=yaml)
        self.assertEqual(rc, 2, msg=f"Expected exit 2\nstdout: {out}\nstderr: {err}")


# ---------------------------------------------------------------------------
# INV-4: saturation guard (WARN, not FAIL)
# ---------------------------------------------------------------------------

class TestINV4SaturationGuard(unittest.TestCase):

    def test_healthy_score_dim_without_saturation_guard_warns_but_passes(self):
        """
        Healthy score-dimension without saturation_guard → WARN but exit 0.
        Saturation is how the proxy defect hides (feedback_recalibrate_saturated_metrics).
        """
        yaml = _minimal_healthy(saturation_guard="")
        rc, out, err = _run_audit(registry_text=yaml)
        # Must still exit 0 (WARN does not fail)
        self.assertEqual(rc, 0, msg=f"Expected exit 0 (warn only)\nstdout: {out}\nstderr: {err}")
        # Should produce some warning mention
        combined = (out + err).lower()
        self.assertIn("saturation", combined,
                      msg=f"Expected saturation warning\n{out}\n{err}")

    def test_healthy_gate_without_saturation_guard_passes_silently(self):
        """
        Gates don't require saturation_guard (INV-4 applies only to score dimensions).
        """
        yaml = _minimal_healthy(kind="gate", saturation_guard="")
        rc, out, err = _run_audit(registry_text=yaml)
        self.assertEqual(rc, 0, msg=f"Expected exit 0 for gate\n{out}\n{err}")


# ---------------------------------------------------------------------------
# Self-consistency: shipped registry audits clean
# ---------------------------------------------------------------------------

class TestShippedRegistryAuditsClean(unittest.TestCase):

    def test_shipped_registry_exists(self):
        """value-term-registry.yaml must exist before audit can run."""
        self.assertTrue(
            REGISTRY_PATH.exists(),
            msg=f"Registry not found at {REGISTRY_PATH}"
        )

    def test_shipped_registry_audits_clean(self):
        """
        The shipped value-term-registry.yaml must audit exit 0.
        This proves seed data is self-consistent (no defect masquerading as healthy).
        """
        rc, out, err = _run_audit(registry_file=str(REGISTRY_PATH))
        self.assertEqual(
            rc, 0,
            msg=f"Shipped registry failed audit (exit {rc})\nstdout: {out}\nstderr: {err}"
        )


# ---------------------------------------------------------------------------
# --scan mode: activity-proxy smell detection
# ---------------------------------------------------------------------------

class TestScanMode(unittest.TestCase):

    def _write_fixture(self, content, suffix=".py"):
        tf = tempfile.NamedTemporaryFile(
            mode="w", suffix=suffix, delete=False, encoding="utf-8"
        )
        tf.write(content)
        tf.flush()
        tf.close()
        return tf.name

    def test_scan_detects_mtime_as_score_input(self):
        """--scan over a file containing 'score = file.stat().st_mtime' reports a candidate."""
        fixture = self._write_fixture(
            "# bad pattern\nscore = file.stat().st_mtime\n"
        )
        rc, out, err = _run_audit("--scan", fixture)
        # scan mode exits 0 (advisory only)
        self.assertEqual(rc, 0, msg=f"Expected exit 0 for scan\n{out}\n{err}")
        combined = (out + err).lower()
        self.assertIn("possible", combined,
                      msg=f"Expected 'POSSIBLE' in scan output\n{out}\n{err}")
        self.addCleanup(os.unlink, fixture)

    def test_scan_detects_datetime_now_as_score(self):
        """--scan detects datetime.now() used as a score value (timestamp-as-score smell)."""
        fixture = self._write_fixture(
            "freshness_score = datetime.now().timestamp()\n"
        )
        rc, out, err = _run_audit("--scan", fixture)
        self.assertEqual(rc, 0, msg=f"scan exits 0\n{out}\n{err}")
        combined = (out + err).lower()
        self.assertIn("possible", combined,
                      msg=f"Expected 'POSSIBLE' in scan output\n{out}\n{err}")
        self.addCleanup(os.unlink, fixture)

    def test_scan_detects_runs_counter(self):
        """--scan detects _runs / fires counter used as a score or metric."""
        fixture = self._write_fixture(
            "metric = self._runs / total\n"
        )
        rc, out, err = _run_audit("--scan", fixture)
        self.assertEqual(rc, 0, msg=f"scan exits 0\n{out}\n{err}")
        combined = (out + err).lower()
        self.assertIn("possible", combined,
                      msg=f"Expected 'POSSIBLE' in scan output\n{out}\n{err}")
        self.addCleanup(os.unlink, fixture)

    def test_scan_clean_file_produces_no_candidates(self):
        """--scan over a file with no smells → no POSSIBLE in output."""
        fixture = self._write_fixture(
            "# pure outcome measure\nscore = entity.last_post_date or 0\n"
        )
        rc, out, err = _run_audit("--scan", fixture)
        self.assertEqual(rc, 0, msg=f"scan exits 0\n{out}\n{err}")
        combined = (out + err).lower()
        self.assertNotIn("possible", combined,
                         msg=f"Expected no 'POSSIBLE' for clean file\n{out}\n{err}")
        self.addCleanup(os.unlink, fixture)

    def test_scan_strict_exits_1_on_hit(self):
        """--scan --scan-strict exits 1 when a smell is found."""
        fixture = self._write_fixture(
            "score = os.stat(path).st_mtime\n"
        )
        rc, out, err = _run_audit("--scan", fixture, "--scan-strict")
        self.assertEqual(rc, 1, msg=f"Expected exit 1 for scan-strict hit\n{out}\n{err}")
        self.addCleanup(os.unlink, fixture)

    def test_scan_strict_exits_0_on_clean(self):
        """--scan --scan-strict exits 0 when no smells found."""
        fixture = self._write_fixture(
            "score = entity.source_date\n"
        )
        rc, out, err = _run_audit("--scan", fixture, "--scan-strict")
        self.assertEqual(rc, 0, msg=f"Expected exit 0 for clean scan-strict\n{out}\n{err}")
        self.addCleanup(os.unlink, fixture)


# ---------------------------------------------------------------------------
# Multiple entries in one registry
# ---------------------------------------------------------------------------

class TestMultipleEntries(unittest.TestCase):

    def test_one_good_one_bad_fails(self):
        """One healthy entry + one defective healthy entry → exit 2."""
        yaml = textwrap.dedent("""\
            scores:
              - id: good-score
                product: test
                kind: score-dimension
                measures: outcome
                value_term: "real outcome signal"
                outcome_signal: "some.field"
                activity_proxy_risk: "none"
                status: healthy
                remediation: ""
                saturation_guard: "guard.py"
                notes: ""
              - id: bad-score
                product: test
                kind: score-dimension
                measures: activity
                value_term: "NONE"
                outcome_signal: ""
                activity_proxy_risk: "its own firing"
                status: healthy
                remediation: ""
                saturation_guard: ""
                notes: ""
        """)
        rc, out, err = _run_audit(registry_text=yaml)
        self.assertEqual(rc, 2, msg=f"Expected exit 2 for mixed registry\n{out}\n{err}")

    def test_all_good_passes(self):
        """Two healthy entries both compliant → exit 0."""
        yaml = textwrap.dedent("""\
            scores:
              - id: score-a
                product: p
                kind: score-dimension
                measures: outcome
                value_term: "source recency"
                outcome_signal: "last_post_date"
                activity_proxy_risk: "none"
                status: healthy
                remediation: ""
                saturation_guard: "audit_a.py"
                notes: ""
              - id: score-b
                product: p
                kind: gate
                measures: outcome
                value_term: "strategic value term"
                outcome_signal: "value_signal"
                activity_proxy_risk: "none"
                status: healthy
                remediation: ""
                saturation_guard: ""
                notes: ""
        """)
        rc, out, err = _run_audit(registry_text=yaml)
        self.assertEqual(rc, 0, msg=f"Expected exit 0\n{out}\n{err}")


# ---------------------------------------------------------------------------
# YAML fallback parser
# ---------------------------------------------------------------------------

class TestYAMLFallbackParser(unittest.TestCase):
    """
    The tool tries `import yaml` and falls back to a mini-parser.
    We test the fallback directly by importing the module and calling
    its _parse_yaml_fallback function (if yaml is available we still
    test parse quality — the function must exist regardless).
    """

    def _import_audit_module(self):
        """Import value_term_audit as a module for white-box testing."""
        spec = importlib.util.spec_from_file_location(
            "value_term_audit", str(AUDIT_SCRIPT)
        )
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        return mod

    def test_fallback_parser_exists(self):
        """value_term_audit must expose _parse_yaml_fallback or _load_registry."""
        mod = self._import_audit_module()
        self.assertTrue(
            hasattr(mod, "_parse_yaml_fallback") or hasattr(mod, "_load_registry"),
            "Module must expose _parse_yaml_fallback or _load_registry for testability"
        )

    def test_fallback_parser_produces_entries(self):
        """Fallback parser on a minimal single-entry YAML returns at least one entry."""
        mod = self._import_audit_module()
        yaml_text = _minimal_healthy()
        if hasattr(mod, "_parse_yaml_fallback"):
            entries = mod._parse_yaml_fallback(yaml_text)
        else:
            # _load_registry accepts a path; write temp file
            tf = tempfile.NamedTemporaryFile(
                mode="w", suffix=".yaml", delete=False, encoding="utf-8"
            )
            tf.write(yaml_text)
            tf.flush()
            tf.close()
            entries = mod._load_registry(tf.name)
            os.unlink(tf.name)

        self.assertIsInstance(entries, list, "Must return a list")
        self.assertGreaterEqual(len(entries), 1, "Must parse at least one entry")
        first = entries[0]
        self.assertIn("id", first, "Entry must have 'id'")
        self.assertEqual(first["id"], "test-score")
        self.assertEqual(first["status"], "healthy")


if __name__ == "__main__":
    unittest.main(verbosity=2)
