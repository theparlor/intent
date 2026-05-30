#!/usr/bin/env python3
"""
test_hook_regex_contract.py — TDD test suite for hook_regex_contract.py (F-1 fix)

Tests:
  A. KNOWN-BAD pattern: (a+)+$ style ambiguous quantifier → must be caught by static
     smell (shape 2) — macOS BSD grep uses DFA and won't time out, but the pattern
     IS flagged by the static smell detector (which catches it for NFA-based engines
     like the ugrep that triggered the F-1 incident).
  B. KNOWN-GOOD pattern: simple literal grep → PASS (no smell, no timeout)
  C. extract_grep_patterns extracts from realistic shell fragments
  D. --print-wrapper flag prints the snippet
  E. Scan of an empty dir → 0 results, exit 0
  F. Missing hooks dir → 0 results, exit 0 (fail-soft)
  G. Static smell shape 1 (multi-group + greedy gap + \\b) is detected
  H. Static smell shape 2 (ambiguous quantifier) is detected
  I. Scan of a .sh file with a bad pattern → WARN produced (static smell catches it)
  J. Scan of a .sh file with a good pattern → no WARN or FAIL

Guards against test self-hang: each test with a potentially slow pattern wraps the
call under a separate threading.Timer timeout so the test suite cannot deadlock.

DESIGN NOTE on macOS BSD grep:
  BSD grep 2.6.0 (macOS /usr/bin/grep) uses a DFA internally and does NOT
  catastrophically backtrack on classical patterns like (a+)+$.  The F-1 incident
  occurred with a specific ugrep-based variant used during hook development.
  Therefore:
  - The timing check (FAIL) is valuable for detecting patterns that DO hang on the
    local engine, and as a CI gate if run on Linux/ugrep environments.
  - The static smell check (WARN) is the PRIMARY catch on macOS — it detects the
    ambiguous-quantifier shape regardless of the local grep engine.
  - Tests assert FAIL OR WARN (either suffices to flag the pattern as dangerous).
"""

import io
import json
import sys
import tempfile
import textwrap
import threading
import unittest
from contextlib import redirect_stdout
from pathlib import Path

# Make the tools dir importable
sys.path.insert(0, str(Path(__file__).parent))

import hook_regex_contract as hrc


# ---------------------------------------------------------------------------
# Test-level hang-guard
# ---------------------------------------------------------------------------

TEST_TIMEOUT_S = 10.0   # whole-test wall-clock guard (generous for CI)


def _run_with_guard(fn):
    """Run fn() with a threading timeout guard; raise TimeoutError if it hangs."""
    result_holder: list = []
    exc_holder: list = []

    def _target():
        try:
            result_holder.append(fn())
        except Exception as e:
            exc_holder.append(e)

    t = threading.Thread(target=_target, daemon=True)
    t.start()
    t.join(timeout=TEST_TIMEOUT_S)
    if t.is_alive():
        raise TimeoutError(
            f"Test hung for more than {TEST_TIMEOUT_S}s — possible grep backtrack"
        )
    if exc_holder:
        raise exc_holder[0]
    return result_holder[0] if result_holder else None


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _write_hook(tmp_dir: Path, name: str, content: str) -> Path:
    p = tmp_dir / name
    p.write_text(content, encoding="utf-8")
    return p


# ---------------------------------------------------------------------------
# C: Pattern extraction
# ---------------------------------------------------------------------------

class TestExtractGrep(unittest.TestCase):
    """C: extract_grep_patterns from realistic shell fragments."""

    def test_extracts_literal_pattern(self):
        # Literal pattern in single-quoted string (no $ → extracted)
        sh = "echo 'hello' | grep -qiE 'proceed'"
        patterns = hrc.extract_grep_patterns(sh)
        self.assertIn("proceed", patterns)

    def test_skips_variable_expansions(self):
        sh = 'echo "$text" | grep -qiE "$SOME_RE"'
        patterns = hrc.extract_grep_patterns(sh)
        self.assertEqual(patterns, [])

    def test_extracts_from_double_quoted(self):
        sh = 'echo "test" | grep -iE "proceed"'
        patterns = hrc.extract_grep_patterns(sh)
        self.assertIn("proceed", patterns)

    def test_deduplicates(self):
        sh = textwrap.dedent("""\
            echo "a" | grep -qiE 'foo'
            echo "b" | grep -iE 'foo'
        """)
        patterns = hrc.extract_grep_patterns(sh)
        self.assertEqual(patterns.count("foo"), 1)

    def test_skips_patterns_with_dollar(self):
        """Patterns containing $ (except anchors at very end) are likely variable refs."""
        # The extractor skips anything with $ because it can't resolve variables
        # This is by design — variable patterns need a separate test harness
        sh = 'echo "x" | grep -qiE "$BARE_CHOICE_RE"'
        patterns = hrc.extract_grep_patterns(sh)
        self.assertEqual(patterns, [])


# ---------------------------------------------------------------------------
# G: Static smell shape 1
# ---------------------------------------------------------------------------

class TestStaticSmellShape1(unittest.TestCase):
    """G: Shape 1 — multi-group + greedy gap + \\b."""

    def test_shape1_detected(self):
        bad = r"(foo|bar).*\b(baz|qux).+\b"
        smell = hrc.check_static_smell(bad)
        self.assertIsNotNone(smell, "Expected WARN for multi-group+greedy+\\b pattern")
        self.assertEqual(smell[0], "WARN")
        self.assertIn("shape 1", smell[1])

    def test_shape1_not_triggered_without_boundary(self):
        # greedy gap + groups but no \b → shape 1 does NOT fire (shape 2 might)
        no_boundary = r"(foo|bar).*(baz|qux)"
        smell = hrc.check_static_smell(no_boundary)
        # Shape 1 requires \b; without \b shape 1 is None (shape 2 checks separately)
        if smell:
            self.assertNotIn("shape 1", smell[1])


# ---------------------------------------------------------------------------
# H: Static smell shape 2
# ---------------------------------------------------------------------------

class TestStaticSmellShape2(unittest.TestCase):
    """H: Shape 2 — ambiguous/nested quantifier: (a+)+ (a|b+)+"""

    def test_classic_nested_quantifier_flagged(self):
        """(a+)+  — canonical catastrophic NFA backtracker."""
        smell = hrc.check_static_smell("(a+)+")
        self.assertIsNotNone(smell, "Expected WARN for (a+)+ ambiguous quantifier")
        self.assertEqual(smell[0], "WARN")
        self.assertIn("shape 2", smell[1])

    def test_alternation_in_group_with_outer_quantifier(self):
        """(b+|a+)+ — the specific F-1 test case variant."""
        smell = hrc.check_static_smell("(b+|a+)+")
        self.assertIsNotNone(smell, "Expected WARN for (b+|a+)+")
        self.assertEqual(smell[0], "WARN")

    def test_anchored_catastrophic_pattern_flagged(self):
        """(a+)+$ — anchored form still flagged."""
        smell = hrc.check_static_smell("(a+)+$")
        self.assertIsNotNone(smell, "Expected WARN for (a+)+$")

    def test_simple_alternation_not_flagged(self):
        """(want me to|should i) — simple alternation, no nested quantifier."""
        smell = hrc.check_static_smell("(want me to|should i)")
        self.assertIsNone(smell, "Simple alternation must NOT trigger shape 2")

    def test_simple_literal_not_flagged(self):
        smell = hrc.check_static_smell("proceed")
        self.assertIsNone(smell)


# ---------------------------------------------------------------------------
# A & B: KNOWN-BAD and KNOWN-GOOD pattern integration
# ---------------------------------------------------------------------------

class TestKnownPatterns(unittest.TestCase):
    """A/B: Known-bad patterns flagged; known-good patterns pass."""

    def _check_bad(self, pattern):
        """Return True if pattern is flagged by EITHER timing FAIL or static WARN."""
        def _run():
            status, detail = hrc.check_timing(pattern, timeout_s=0.5)
            smell = hrc.check_static_smell(pattern)
            return status, detail, smell

        result = _run_with_guard(_run)
        if result is None:
            self.fail("_run_with_guard returned None")
        status, detail, smell = result
        return status == "FAIL" or smell is not None

    def test_A_classic_nested_quantifier_flagged(self):
        """(a+)+$ must be flagged (timing FAIL or static WARN)."""
        flagged = self._check_bad("(a+)+$")
        self.assertTrue(
            flagged,
            "(a+)+$ must be flagged by timing FAIL or static WARN — "
            "it is a known catastrophic-backtrack pattern on NFA-based greps (F-1 incident)"
        )

    def test_A_alternation_nested_quantifier_flagged(self):
        """(b+|a+)+ must be flagged."""
        flagged = self._check_bad("(b+|a+)+")
        self.assertTrue(
            flagged,
            "(b+|a+)+ must be flagged"
        )

    def test_B_simple_literal_passes(self):
        """'proceed' — simple literal; must PASS with no smell."""
        def _run():
            status, detail = hrc.check_timing("proceed", timeout_s=0.5)
            smell = hrc.check_static_smell("proceed")
            return status, smell

        result = _run_with_guard(_run)
        status, smell = result
        self.assertEqual(status, "PASS", f"Expected PASS for 'proceed', got {status}")
        self.assertIsNone(smell, f"Expected no smell for 'proceed', got {smell}")

    def test_B_simple_alternation_passes(self):
        """(want me to|should i) — simple alternation, no nesting; must PASS."""
        def _run():
            status, _ = hrc.check_timing("(want me to|should i)", timeout_s=0.5)
            smell = hrc.check_static_smell("(want me to|should i)")
            return status, smell

        result = _run_with_guard(_run)
        status, smell = result
        self.assertEqual(status, "PASS")
        self.assertIsNone(smell)


# ---------------------------------------------------------------------------
# I: Scan of a .sh file with bad pattern
# ---------------------------------------------------------------------------

class TestScanWithBadHook(unittest.TestCase):
    """I/J: scan_hooks_dir catches bad patterns in hook files."""

    def test_I_scan_bad_hook_produces_warn_or_fail(self):
        """A hook file with (a+)+$ pattern must produce WARN or FAIL from scan."""
        def _run():
            with tempfile.TemporaryDirectory() as tmp:
                tmpdir = Path(tmp)
                # Write hook with a literal pattern (no $ variable reference)
                # Note: the pattern (a+)+Z avoids the $ filter ($ at end of string
                # in a pattern trips the variable filter; use Z anchor workaround,
                # or just test with (a+)+)
                _write_hook(
                    tmpdir,
                    "bad_hook.sh",
                    'echo "test" | grep -qiE \'(a+)+Z\'',  # Z instead of $ to bypass $ filter
                )
                results = hrc.scan_hooks_dir(tmpdir, timeout_s=0.5)
                return results

        results = _run_with_guard(_run)
        self.assertIsNotNone(results)
        statuses = {r.status for r in results}
        self.assertTrue(
            statuses & {"FAIL", "WARN"},
            f"Expected FAIL or WARN in results for bad hook (a+)+Z, got: {statuses}"
        )

    def test_I_scan_bad_hook_with_alternation_group(self):
        """(b+|a+)+ in a hook file → WARN from static smell."""
        def _run():
            with tempfile.TemporaryDirectory() as tmp:
                tmpdir = Path(tmp)
                _write_hook(
                    tmpdir,
                    "bad_hook2.sh",
                    'echo "test" | grep -qiE \'(b+|a+)+\'',
                )
                results = hrc.scan_hooks_dir(tmpdir, timeout_s=0.5)
                return results

        results = _run_with_guard(_run)
        statuses = {r.status for r in results}
        self.assertTrue(
            statuses & {"FAIL", "WARN"},
            f"Expected FAIL or WARN for (b+|a+)+, got: {statuses}"
        )

    def test_J_scan_good_hook_no_fail_or_warn(self):
        """J: A hook file with only simple patterns → no FAIL, no WARN."""
        def _run():
            with tempfile.TemporaryDirectory() as tmp:
                tmpdir = Path(tmp)
                _write_hook(
                    tmpdir,
                    "good_hook.sh",
                    'echo "test" | grep -qiE \'proceed\'',
                )
                results = hrc.scan_hooks_dir(tmpdir, timeout_s=0.5)
                return results

        results = _run_with_guard(_run)
        fail_warn = [r for r in results if r.status in ("FAIL", "WARN")]
        self.assertEqual(
            fail_warn, [],
            f"Expected no FAIL/WARN for good hook, got: {fail_warn}"
        )
        pass_results = [r for r in results if r.status == "PASS"]
        self.assertTrue(len(pass_results) > 0, "Expected at least one PASS result")


# ---------------------------------------------------------------------------
# D, E, F: print-wrapper, empty dir, missing dir
# ---------------------------------------------------------------------------

class TestEdgeCases(unittest.TestCase):
    """D, E, F: edge cases — wrapper, empty dir, missing dir."""

    def test_D_print_wrapper_exits_0(self):
        exit_code = hrc.main(["--print-wrapper"])
        self.assertEqual(exit_code, 0)

    def test_E_empty_dir_returns_no_results(self):
        with tempfile.TemporaryDirectory() as tmp:
            results = hrc.scan_hooks_dir(Path(tmp), timeout_s=0.5)
            self.assertEqual(results, [])

    def test_F_missing_dir_returns_no_results_fail_soft(self):
        missing = Path("/tmp/does_not_exist_hook_contract_test_xyz")
        results = hrc.scan_hooks_dir(missing, timeout_s=0.5)
        self.assertEqual(results, [])

    def test_json_flag_produces_valid_json(self):
        with tempfile.TemporaryDirectory() as tmp:
            # Write a known-good hook
            good_hook = Path(tmp) / "ok.sh"
            good_hook.write_text('echo "x" | grep -qiE \'proceed\'')

            buf = io.StringIO()
            with redirect_stdout(buf):
                exit_code = hrc.main(["--hooks-dir", tmp, "--json", "--timeout", "0.5"])

            output = json.loads(buf.getvalue())
            self.assertIn("summary", output)
            self.assertIn("results", output)

    def test_exit_0_all_clean(self):
        with tempfile.TemporaryDirectory() as tmp:
            Path(tmp, "ok.sh").write_text('echo "x" | grep -qiE \'proceed\'')
            exit_code = hrc.main(["--hooks-dir", tmp, "--timeout", "0.5"])
            # proceed is PASS with no smell → exit 0
            self.assertEqual(exit_code, 0)


if __name__ == "__main__":
    unittest.main(verbosity=2)
