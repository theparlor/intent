#!/usr/bin/env python3
"""
test_typed_verdict_invariants.py — TDD suite for typed_verdict_invariants.py.

Written RED-first against INV-INTENT-NO-SELF-GRADED-CLOSURE (the catch-net named
in spec/typed-evaluation-verdicts.md §5). Covers both checks and the
zero-violation-start guarantee (feedback_invariant_zero_violation_start).

Run:
    python3 -m unittest test_typed_verdict_invariants -v
"""
from __future__ import annotations

import importlib.util
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

TOOLS_DIR = Path(__file__).parent
INV_SCRIPT = TOOLS_DIR / "typed_verdict_invariants.py"


def _import():
    spec = importlib.util.spec_from_file_location("typed_verdict_invariants", str(INV_SCRIPT))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


tvi = _import()


def _evaluated(date="2026-06-20", **data):
    """Build an observation.evaluated event with sensible required-field defaults."""
    d = {"criteria_origin": "derived", "evaluator_model": "opus-4.8", "evaluator_repo": "external"}
    d.update(data)
    return {"event": "observation.evaluated", "timestamp": f"{date}T12:00:00Z",
            "span_id": data.get("verdict_id", "V1"), "data": d}


class TestSchemaCompleteness(unittest.TestCase):
    """Check A — required typed-verdict fields on post-cutoff events."""

    def test_missing_evaluator_repo_fails(self):
        ev = _evaluated()
        del ev["data"]["evaluator_repo"]
        passed, violations = tvi.invariant_no_self_graded_closure([ev])
        self.assertFalse(passed)
        self.assertTrue(any("evaluator_repo" in v for v in violations))

    def test_missing_evaluator_model_fails(self):
        ev = _evaluated()
        ev["data"]["evaluator_model"] = ""
        passed, violations = tvi.invariant_no_self_graded_closure([ev])
        self.assertFalse(passed)
        self.assertTrue(any("evaluator_model" in v for v in violations))

    def test_invalid_criteria_origin_fails(self):
        ev = _evaluated(criteria_origin="bogus")
        passed, violations = tvi.invariant_no_self_graded_closure([ev])
        self.assertFalse(passed)
        self.assertTrue(any("criteria_origin" in v for v in violations))

    def test_complete_schema_passes(self):
        passed, violations = tvi.invariant_no_self_graded_closure([_evaluated()])
        self.assertTrue(passed, violations)


class TestGrandfathering(unittest.TestCase):
    """Pre-2026-06-09 events are grandfathered and never judged."""

    def test_pre_cutoff_missing_fields_passes(self):
        old = {"event": "observation.evaluated", "timestamp": "2026-05-01T09:00:00Z",
               "span_id": "OLD", "data": {"verdict": "pass"}}  # no typed fields at all
        passed, violations = tvi.invariant_no_self_graded_closure([old])
        self.assertTrue(passed, violations)

    def test_pre_cutoff_self_graded_closure_passes(self):
        old = {"event": "observation.evaluated", "timestamp": "2026-06-08T23:59:59Z",
               "span_id": "OLD2",
               "data": {"verdict": "pass", "closes_spec": True, "criteria_origin": "self",
                        "evaluator_model": "opus-4.6", "evaluator_repo": "same-repo"}}
        passed, violations = tvi.invariant_no_self_graded_closure([old])
        self.assertTrue(passed, violations)


class TestNoSelfGradedClosure(unittest.TestCase):
    """Check B — a self/distilled verdict may not close a spec."""

    def test_self_graded_closure_fails(self):
        ev = _evaluated(verdict="pass", closes_spec=True, criteria_origin="self",
                        evaluator_repo="same-repo", verdict_id="V-self")
        passed, violations = tvi.invariant_no_self_graded_closure([ev])
        self.assertFalse(passed)
        self.assertTrue(any("/B" in v for v in violations))

    def test_distilled_closure_fails(self):
        ev = _evaluated(verdict="pass", authority="acceptance", criteria_origin="distilled",
                        verdict_id="V-dist")
        passed, violations = tvi.invariant_no_self_graded_closure([ev])
        self.assertFalse(passed)
        self.assertTrue(any("/B" in v for v in violations))

    def test_derived_closure_passes(self):
        ev = _evaluated(verdict="pass", closes_spec=True, criteria_origin="derived")
        passed, violations = tvi.invariant_no_self_graded_closure([ev])
        self.assertTrue(passed, violations)

    def test_self_graded_non_closing_passes(self):
        # self is a legitimate inner-loop instrument when it does NOT close a spec
        ev = _evaluated(verdict="pass", criteria_origin="self", evaluator_repo="same-repo",
                        verdict_id="V-inner")
        passed, violations = tvi.invariant_no_self_graded_closure([ev])
        self.assertTrue(passed, violations)

    def test_self_graded_closure_with_brien_override_passes(self):
        ev = _evaluated(verdict="pass", closes_spec=True, criteria_origin="self",
                        evaluator_repo="same-repo", verdict_id="V-ovr")
        override = {"event": "decision.recorded", "timestamp": "2026-06-20T12:05:00Z",
                    "data": {"overrides_verdict": "V-ovr", "override": True,
                             "note": "Brien accepts; no exterior judge exists for this class."}}
        passed, violations = tvi.invariant_no_self_graded_closure([ev, override])
        self.assertTrue(passed, violations)


class TestZeroViolationStart(unittest.TestCase):
    """The catch-net must fire clean on day one against the real stream."""

    def test_empty_stream_passes(self):
        passed, violations = tvi.invariant_no_self_graded_closure([])
        self.assertTrue(passed)
        self.assertEqual(violations, [])

    def test_live_repo_events_pass(self):
        # The real .intent/events/events.jsonl must be clean on day one.
        events = tvi.load_events(tvi.DEFAULT_EVENTS)
        passed, violations = tvi.invariant_no_self_graded_closure(events)
        self.assertTrue(passed, f"zero-violation-start broken: {violations}")


class TestCLI(unittest.TestCase):
    def test_cli_json_pass_on_empty(self):
        with tempfile.TemporaryDirectory() as d:
            empty = Path(d) / "events.jsonl"
            empty.write_text("", encoding="utf-8")
            out = subprocess.run(
                [sys.executable, str(INV_SCRIPT), "--events", str(empty), "--json"],
                capture_output=True, text=True)
            self.assertEqual(out.returncode, 0, out.stderr)
            self.assertTrue(json.loads(out.stdout)["passed"])

    def test_cli_json_fail_on_self_closure(self):
        with tempfile.TemporaryDirectory() as d:
            bad = Path(d) / "events.jsonl"
            ev = {"event": "observation.evaluated", "timestamp": "2026-07-01T00:00:00Z",
                  "span_id": "V-bad",
                  "data": {"verdict": "pass", "closes_spec": True, "criteria_origin": "self",
                           "evaluator_model": "opus-4.8", "evaluator_repo": "same-repo"}}
            bad.write_text(json.dumps(ev) + "\n", encoding="utf-8")
            out = subprocess.run(
                [sys.executable, str(INV_SCRIPT), "--events", str(bad), "--json"],
                capture_output=True, text=True)
            self.assertEqual(out.returncode, 1)
            self.assertFalse(json.loads(out.stdout)["passed"])


if __name__ == "__main__":
    unittest.main()
