#!/usr/bin/env python3
"""
test_closure_writeboundary_check.py — TDD tests for closure_writeboundary_check.py (F-4 fix)

Fixtures:
  A. status: resolved + body "needs update-mode pass (follow-up)" → FLAGGED
     (exactly the F-4 incident: overnight batch wrote this, hook missed it)
  B. status: resolved + real upstream_control_path + catch_mechanism + no weasel → NOT flagged
  C. status: symptom-repaired, upstream-pending (honest pending) → NOT flagged
  D. status: captured (not resolved) → NOT flagged
  E. status: resolved + missing catch_mechanism only → FLAGGED (missing field)
  F. status: resolved + missing upstream_control_path only → FLAGGED
  G. Multiple violations in one file → all reported
  H. Empty dir → 0 violations, exit 0
  I. Missing dir → 0 violations, exit 0 (fail-soft)
  J. --json flag produces valid JSON
"""

import json
import sys
import tempfile
import textwrap
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

import closure_writeboundary_check as cwb


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _write_signal(tmp_dir: Path, name: str, content: str) -> Path:
    p = tmp_dir / name
    p.write_text(textwrap.dedent(content), encoding="utf-8")
    return p


# ---------------------------------------------------------------------------
# Fixtures as constants
# ---------------------------------------------------------------------------

# A — THE F-4 INCIDENT PATTERN: resolved + weasel body (follow-up + needs + pending)
FIXTURE_A = """\
---
id: SIG-2026-05-27-opus-repass-pending-torres
type: processing-signal
status: resolved
created: 2026-05-27
---

# Torres repass

pipeline_survival: needs update-mode pass (follow-up) — still pending
"""

# B — CLEAN: resolved with required fields + no weasel
FIXTURE_B = """\
---
id: SIG-2026-05-27-clean-signal
type: processing-signal
status: resolved
created: 2026-05-27
---

# Clean signal

upstream_control_path: Core/products/cast/engine/scripts/synthesis_to_registry.py
catch_mechanism: chain_audit INV-SYNTHESIS-001 invariant (runs on every render_all)
pipeline_survival: yes — invariant enforced at pipeline level; will detect any regression

The work is done. Corpus written, synthesis passed, invariant fires.
"""

# C — HONEST PENDING: symptom-repaired → NOT a violation regardless of body content
FIXTURE_C = """\
---
id: SIG-2026-05-27-honest-pending
type: friction
status: symptom-repaired, upstream-pending
created: 2026-05-27
---

# Honest pending signal

This is pending. Needs follow-up. TODO: wire into CI.
upstream_control_path: not yet established
catch_mechanism: manual review for now
pipeline_survival: at risk — needs proper wiring
"""

# D — Not resolved at all → no flag
FIXTURE_D = """\
---
id: SIG-2026-05-27-captured
type: friction
status: captured
created: 2026-05-27
---

# Just captured

needs investigation
"""

# E — resolved + missing catch_mechanism → FLAGGED (missing field)
FIXTURE_E = """\
---
id: SIG-2026-05-27-missing-catch
type: processing-signal
status: resolved
created: 2026-05-27
---

# Missing catch_mechanism

upstream_control_path: Core/products/cast/engine/scripts/synthesis_to_registry.py

The synthesis pass ran. Work complete.
"""

# F — resolved + missing upstream_control_path → FLAGGED
FIXTURE_F = """\
---
id: SIG-2026-05-27-missing-upstream
type: processing-signal
status: resolved
created: 2026-05-27
---

# Missing upstream_control_path

catch_mechanism: chain_audit fires on render_all

Work complete.
"""

# G — resolved + both weasel AND missing fields → multiple violations
FIXTURE_G = """\
---
id: SIG-2026-05-27-multi-violation
type: processing-signal
status: resolved
created: 2026-05-27
---

# Multiple violations

This needs follow-up. TODO: add upstream control. Will fix later.
"""


# ---------------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------------

class TestCheckFile(unittest.TestCase):
    """Unit tests on check_file() with individual fixture files."""

    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.tmpdir = Path(self.tmp.name)

    def tearDown(self):
        self.tmp.cleanup()

    def _check(self, content: str, name: str = "test.md") -> list[cwb.Violation]:
        p = _write_signal(self.tmpdir, name, content)
        return cwb.check_file(p)

    # A — THE F-4 INCIDENT PATTERN
    def test_A_f4_incident_pattern_is_flagged(self):
        violations = self._check(FIXTURE_A)
        self.assertTrue(
            len(violations) > 0,
            "Expected violations for F-4 incident pattern (resolved + follow-up/needs/pending)"
        )
        reasons = " ".join(v.reason for v in violations)
        self.assertIn("PREMATURE-RESOLVED", reasons)

    # B — CLEAN
    def test_B_clean_resolved_signal_not_flagged(self):
        violations = self._check(FIXTURE_B)
        self.assertEqual(
            violations, [],
            f"Expected no violations for clean resolved signal, got: {violations}"
        )

    # C — HONEST PENDING
    def test_C_symptom_repaired_honest_pending_not_flagged(self):
        violations = self._check(FIXTURE_C)
        self.assertEqual(
            violations, [],
            f"symptom-repaired, upstream-pending must NOT be flagged, got: {violations}"
        )

    # D — NOT RESOLVED
    def test_D_captured_status_not_flagged(self):
        violations = self._check(FIXTURE_D)
        self.assertEqual(
            violations, [],
            f"status: captured must NOT be flagged, got: {violations}"
        )

    # E — MISSING CATCH_MECHANISM
    def test_E_missing_catch_mechanism_flagged(self):
        violations = self._check(FIXTURE_E)
        self.assertTrue(
            any("catch_mechanism" in v.reason for v in violations),
            f"Expected missing catch_mechanism violation, got: {violations}"
        )

    # F — MISSING UPSTREAM_CONTROL_PATH
    def test_F_missing_upstream_control_path_flagged(self):
        violations = self._check(FIXTURE_F)
        self.assertTrue(
            any("upstream_control_path" in v.reason for v in violations),
            f"Expected missing upstream_control_path violation, got: {violations}"
        )

    # G — MULTIPLE VIOLATIONS
    def test_G_multiple_violations_all_reported(self):
        violations = self._check(FIXTURE_G)
        self.assertTrue(
            len(violations) >= 2,
            f"Expected multiple violations for G, got {len(violations)}: {violations}"
        )


class TestScanDir(unittest.TestCase):
    """Integration tests on scan_signals_dir()."""

    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.tmpdir = Path(self.tmp.name)

    def tearDown(self):
        self.tmp.cleanup()

    def test_empty_dir_returns_no_violations(self):
        violations = cwb.scan_signals_dir(self.tmpdir)
        self.assertEqual(violations, [])

    def test_missing_dir_fail_soft(self):
        missing = Path("/tmp/does_not_exist_cwb_test_xyz_dir")
        violations = cwb.scan_signals_dir(missing)
        self.assertEqual(violations, [])

    def test_mixed_dir_only_flags_violations(self):
        _write_signal(self.tmpdir, "bad.md", FIXTURE_A)
        _write_signal(self.tmpdir, "good.md", FIXTURE_B)
        _write_signal(self.tmpdir, "honest.md", FIXTURE_C)
        _write_signal(self.tmpdir, "captured.md", FIXTURE_D)

        violations = cwb.scan_signals_dir(self.tmpdir)
        # Only bad.md should produce violations
        flagged_files = {Path(v.file_path).name for v in violations}
        self.assertIn("bad.md", flagged_files)
        self.assertNotIn("good.md", flagged_files)
        self.assertNotIn("honest.md", flagged_files)
        self.assertNotIn("captured.md", flagged_files)


class TestCLI(unittest.TestCase):
    """CLI integration tests."""

    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.tmpdir = Path(self.tmp.name)

    def tearDown(self):
        self.tmp.cleanup()

    def test_exit_0_on_clean_dir(self):
        _write_signal(self.tmpdir, "good.md", FIXTURE_B)
        exit_code = cwb.main(["--dir", str(self.tmpdir)])
        self.assertEqual(exit_code, 0)

    def test_exit_2_on_violation(self):
        _write_signal(self.tmpdir, "bad.md", FIXTURE_A)
        exit_code = cwb.main(["--dir", str(self.tmpdir)])
        self.assertEqual(exit_code, 2)

    def test_json_output_valid(self):
        import io
        from contextlib import redirect_stdout

        _write_signal(self.tmpdir, "bad.md", FIXTURE_A)
        _write_signal(self.tmpdir, "good.md", FIXTURE_B)

        buf = io.StringIO()
        with redirect_stdout(buf):
            exit_code = cwb.main(["--dir", str(self.tmpdir), "--json"])

        output = json.loads(buf.getvalue())
        self.assertIn("summary", output)
        self.assertIn("violations", output)
        self.assertGreater(output["summary"]["violations"], 0)
        self.assertEqual(exit_code, 2)

    def test_empty_dir_exit_0(self):
        exit_code = cwb.main(["--dir", str(self.tmpdir)])
        self.assertEqual(exit_code, 0)

    def test_missing_dir_exit_0_fail_soft(self):
        exit_code = cwb.main(["--dir", "/tmp/does_not_exist_cwb_cli_test_xyz"])
        self.assertEqual(exit_code, 0)


class TestDistinctions(unittest.TestCase):
    """Precise distinction between violation classes and non-violations."""

    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.tmpdir = Path(self.tmp.name)

    def tearDown(self):
        self.tmp.cleanup()

    def _check(self, content: str) -> list[cwb.Violation]:
        p = _write_signal(self.tmpdir, "test.md", content)
        return cwb.check_file(p)

    def test_will_future_tense_in_resolved_is_weasel(self):
        """'will fix' / 'will be done' in a resolved signal is a weasel marker."""
        content = """\
---
status: resolved
---
upstream_control_path: somewhere
catch_mechanism: something
This will fix the remaining gap in the next pass.
"""
        violations = self._check(content)
        self.assertTrue(
            any("will" in v.reason.lower() for v in violations),
            f"Expected 'will' weasel marker flagged for 'will fix', got: {violations}"
        )

    def test_will_be_done_in_resolved_is_weasel(self):
        """'will be done' in a resolved signal is a weasel marker."""
        content = """\
---
status: resolved
---
upstream_control_path: somewhere
catch_mechanism: something
The wiring will be done in the next session.
"""
        violations = self._check(content)
        self.assertTrue(
            any("will" in v.reason.lower() for v in violations),
            f"Expected 'will' weasel marker flagged for 'will be done', got: {violations}"
        )

    def test_will_detect_capability_is_not_weasel(self):
        """'will detect' describes catch-net capability — NOT a deferral weasel."""
        content = """\
---
status: resolved
---
upstream_control_path: somewhere
catch_mechanism: something
The invariant will detect any regression automatically.
"""
        violations = self._check(content)
        self.assertEqual(
            violations, [],
            f"'will detect' must NOT be flagged as weasel, got: {violations}"
        )

    def test_todo_in_resolved_is_weasel(self):
        """TODO in a resolved signal is a weasel marker."""
        content = """\
---
status: resolved
---
upstream_control_path: somewhere
catch_mechanism: something
TODO: remember to verify this actually ran.
"""
        violations = self._check(content)
        self.assertTrue(
            any("TODO" in v.reason or "TODO" in v.offending_line for v in violations),
            f"Expected TODO weasel marker flagged, got: {violations}"
        )

    def test_needs_in_resolved_body_is_weasel(self):
        """'needs X' in a resolved signal body is a weasel marker."""
        content = """\
---
status: resolved
---
upstream_control_path: somewhere
catch_mechanism: something
pipeline_survival: yes
This work needs a follow-on pass to verify the rendering.
"""
        violations = self._check(content)
        self.assertTrue(
            len(violations) > 0,
            f"Expected weasel marker ('needs') flagged, got no violations"
        )

    def test_clean_resolved_no_weasel_passes(self):
        """A genuinely closed resolved signal with all fields passes."""
        content = """\
---
status: resolved
---
upstream_control_path: Core/products/cast/engine/scripts/synthesis.py
catch_mechanism: chain_audit INV-001 invariant
pipeline_survival: yes — invariant enforced
The work is complete. The corpus updated and all invariants pass.
"""
        violations = self._check(content)
        self.assertEqual(violations, [], f"Unexpected violations: {violations}")


if __name__ == "__main__":
    unittest.main(verbosity=2)
