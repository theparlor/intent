#!/usr/bin/env python3
"""
test_convention_migration_invariant.py — TDD suite for Control A (SIG-2026-06-27).

Written RED-first: a bound consumer that still contains a retired convention must
FAIL INV-MIGRATION-NO-LEGACY; a migrated consumer must PASS; a declared consumer
that resolves to nothing is advisory (WARN) unless --strict. Zero-violation-start:
the live repo (which declares no bound_consumers yet) passes on day one.

Run:
    python3 -m unittest test_convention_migration_invariant -v
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
SCRIPT = TOOLS_DIR / "convention_migration_invariant.py"


def _import():
    spec = importlib.util.spec_from_file_location("convention_migration_invariant", str(SCRIPT))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


cmi = _import()

PORT_CONTRACT = """\
---
id: cast-to-voices-port
bound_consumers:
  - forge/skills/panel-critique.md
  - voices/tools.py
forbidden_legacy_patterns:
  - opus-synthesis-*
---
# Cast → Voices synthesis surface
Current surface: corpus/{slug}/synthesis-*.md
"""


def _make_tree(consumer_body: str, contract: str = PORT_CONTRACT):
    """Build a temp tree: contracts/<x>-port.md + the two declared consumer files."""
    d = tempfile.mkdtemp()
    root = Path(d)
    (root / "contracts").mkdir()
    (root / "contracts" / "cast-to-voices-port.md").write_text(contract, encoding="utf-8")
    (root / "forge" / "skills").mkdir(parents=True)
    (root / "forge" / "skills" / "panel-critique.md").write_text(consumer_body, encoding="utf-8")
    (root / "voices").mkdir()
    (root / "voices" / "tools.py").write_text("# clean consumer\nsynthesis_glob='synthesis-*.md'\n", encoding="utf-8")
    return root


class TestNoLegacy(unittest.TestCase):
    def test_consumer_with_retired_convention_fails(self):
        root = _make_tree("load('opus-synthesis-2026-04-10.md')  # DEAD glob\n")
        ok, violations = cmi.invariant_no_legacy(root, root)
        self.assertFalse(ok)
        self.assertTrue(any("opus-synthesis-*" in v and "panel-critique.md" in v for v in violations))

    def test_migrated_consumer_passes(self):
        root = _make_tree("load('synthesis-2026-04-10-opus-foo.md')  # migrated\n")
        ok, violations = cmi.invariant_no_legacy(root, root)
        self.assertTrue(ok, violations)

    def test_contract_without_blocks_is_ignored(self):
        bare = "---\nid: bare-port\n---\n# no bindings declared\n"
        root = _make_tree("load('opus-synthesis-x.md')\n", contract=bare)
        ok, violations = cmi.invariant_no_legacy(root, root)
        self.assertTrue(ok, "a contract declaring no bindings must not gate (zero-violation-start)")


class TestConsumerResolves(unittest.TestCase):
    def test_missing_consumer_is_flagged(self):
        root = _make_tree("clean\n")
        # delete a declared consumer so its glob resolves to nothing
        (root / "voices" / "tools.py").unlink()
        ok, violations = cmi.invariant_consumer_resolves(root, root)
        self.assertFalse(ok)
        self.assertTrue(any("voices/tools.py" in v for v in violations))

    def test_all_consumers_present_passes(self):
        root = _make_tree("clean\n")
        ok, _ = cmi.invariant_consumer_resolves(root, root)
        self.assertTrue(ok)


class TestParsing(unittest.TestCase):
    def test_flow_list_form(self):
        fm = "id: x\nforbidden_legacy_patterns: [opus-synthesis-*, old-thing]\n"
        self.assertEqual(cmi.parse_list_block(fm, "forbidden_legacy_patterns"),
                         ["opus-synthesis-*", "old-thing"])

    def test_block_list_form(self):
        fm = "bound_consumers:\n  - a/b.py\n  - c/d.md\nother: 1\n"
        self.assertEqual(cmi.parse_list_block(fm, "bound_consumers"), ["a/b.py", "c/d.md"])


class TestZeroViolationStart(unittest.TestCase):
    def test_live_repo_passes(self):
        # The intent repo declares no bound_consumers yet → invariant fires clean on day one.
        ok_legacy, v1 = cmi.invariant_no_legacy(cmi.REPO_ROOT, cmi.REPO_ROOT)
        ok_res, v2 = cmi.invariant_consumer_resolves(cmi.REPO_ROOT, cmi.REPO_ROOT)
        self.assertTrue(ok_legacy, v1)
        self.assertTrue(ok_res, v2)


class TestCLI(unittest.TestCase):
    def test_cli_fails_on_legacy(self):
        root = _make_tree("x = 'opus-synthesis-y.md'\n")
        out = subprocess.run(
            [sys.executable, str(SCRIPT), "--contracts-root", str(root),
             "--consumer-root", str(root), "--json"],
            capture_output=True, text=True)
        self.assertEqual(out.returncode, 1)
        self.assertFalse(json.loads(out.stdout)["passed"])

    def test_cli_passes_clean(self):
        root = _make_tree("x = 'synthesis-y.md'\n")
        out = subprocess.run(
            [sys.executable, str(SCRIPT), "--contracts-root", str(root),
             "--consumer-root", str(root), "--json"],
            capture_output=True, text=True)
        self.assertEqual(out.returncode, 0, out.stdout)
        self.assertTrue(json.loads(out.stdout)["passed"])


if __name__ == "__main__":
    unittest.main()
