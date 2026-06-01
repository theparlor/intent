#!/usr/bin/env python3
"""
test_retired_term_invariants.py — TDD suite for retired_term_invariants.py

retired_term_invariants.py is a chain_audit invariant enforcing the retirement of
"skills-engine" as a product name (renamed to Forge per WS-DDR-027). Same invariant
signature as cortege_invariants.py / chain_audit_portfolio.py / value_term_invariants.py:
  invariant_*() -> (passed, violations), INV-* IDs, emit_signal with honest-DoD
  frontmatter, exit 0/1.

Run:
    python3 -m pytest test_retired_term_invariants.py -v
    python3 test_retired_term_invariants.py
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
INV_SCRIPT = TOOLS_DIR / "retired_term_invariants.py"
# tools → intent → frameworks → Core
CORE_ROOT = TOOLS_DIR.resolve().parents[2]


def _import_inv():
    spec = importlib.util.spec_from_file_location("retired_term_invariants", str(INV_SCRIPT))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def _write(root: Path, relpath: str, content: str) -> Path:
    p = root / relpath
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(content, encoding="utf-8")
    return p


# ---------------------------------------------------------------------------
# Behavioral: violations are detected
# ---------------------------------------------------------------------------

class TestViolationsDetected(unittest.TestCase):

    def test_clean_file_passes(self):
        mod = _import_inv()
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            _write(root, "src/feature.py",
                   "# References only forge\nFORGE_PATH = '/products/forge'\n")
            passed, violations = mod.invariant_no_live_skills_engine_reference(root)
            self.assertTrue(passed, msg=f"Clean file should pass: {violations}")
            self.assertEqual(violations, [])

    def test_hyphen_variant_detected(self):
        mod = _import_inv()
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            _write(root, "config.yaml", "product: skills-engine\n")
            passed, violations = mod.invariant_no_live_skills_engine_reference(root)
            self.assertFalse(passed)
            self.assertTrue(any("config.yaml" in v for v in violations),
                            msg=f"skills-engine not caught: {violations}")

    def test_underscore_variant_detected(self):
        mod = _import_inv()
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            _write(root, "code.py", "path = skills_engine_path\n")
            passed, violations = mod.invariant_no_live_skills_engine_reference(root)
            self.assertFalse(passed)
            self.assertTrue(any("code.py" in v for v in violations))

    def test_upper_variant_detected(self):
        mod = _import_inv()
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            _write(root, "env.sh", "SKILLS_ENGINE_ROOT=/bad\n")
            passed, violations = mod.invariant_no_live_skills_engine_reference(root)
            self.assertFalse(passed)
            self.assertTrue(any("env.sh" in v for v in violations))

    def test_camel_variant_detected(self):
        mod = _import_inv()
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            _write(root, "model.py", "class SkillsEngine: pass\n")
            passed, violations = mod.invariant_no_live_skills_engine_reference(root)
            self.assertFalse(passed)
            self.assertTrue(any("model.py" in v for v in violations))

    def test_violation_message_names_file_and_invariant(self):
        mod = _import_inv()
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            _write(root, "newfile.md", "skills-engine is back\n")
            _, violations = mod.invariant_no_live_skills_engine_reference(root)
            self.assertTrue(violations)
            self.assertIn("INV-RETIRED-TERM-SKILLS-ENGINE", violations[0])
            self.assertIn("newfile.md", violations[0])


# ---------------------------------------------------------------------------
# Allowlist: known-historical paths are exempt
# ---------------------------------------------------------------------------

class TestAllowlist(unittest.TestCase):

    def _check_exempt(self, relpath: str, content: str, label: str):
        mod = _import_inv()
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            _write(root, relpath, content)
            passed, violations = mod.invariant_no_live_skills_engine_reference(root)
            self.assertTrue(passed, msg=f"{label} should be allowlisted: {violations}")

    def test_intent_dir_exempt(self):
        self._check_exempt(".intent/signals/old.md", "# skills-engine ref", ".intent/")

    def test_intent_journal_exempt(self):
        self._check_exempt(".intent-journal/JOURNAL.md", "skills-engine", ".intent-journal/")

    def test_journal_dir_exempt(self):
        self._check_exempt("journal/2026-04.md", "skills-engine", "journal/")

    def test_corpus_dir_exempt(self):
        self._check_exempt("corpus/entity/notes.md", "skills-engine", "corpus/")

    def test_farm_dir_exempt(self):
        self._check_exempt("farm/intake/eval.md", "skills-engine", "farm/")

    def test_intake_dir_exempt(self):
        self._check_exempt("_intake/2026-04/report.md", "skills-engine", "_intake/")

    def test_state_dir_exempt(self):
        self._check_exempt(".state/RUN.md", "skills-engine", ".state/")

    def test_claude_dir_exempt(self):
        self._check_exempt(".claude/commands/check.md", "skills-engine", ".claude/")

    def test_forge_engine_exempt(self):
        self._check_exempt("forge/engine/pliable/script.py", "SKILLS_ENGINE_ROOT = x",
                           "forge/engine/")

    def test_forge_outputs_exempt(self):
        self._check_exempt("forge/outputs/claude-code/skill.md", "skills-engine",
                           "forge/outputs/")

    def test_working_dir_exempt(self):
        self._check_exempt("working/draft.md", "skills-engine", "working/")

    def test_plans_dir_exempt(self):
        self._check_exempt("plans/2026-04-plan.md", "skills-engine", "plans/")

    def test_spec_dir_exempt(self):
        self._check_exempt("spec/design.md", "skills-engine", "spec/")

    def test_decision_support_dir_exempt(self):
        self._check_exempt("decision-support/impact.md", "skills-engine", "decision-support/")

    def test_brand_dir_exempt(self):
        self._check_exempt("brand/map.html", "skills-engine", "brand/")

    def test_reference_dir_exempt(self):
        self._check_exempt("reference/contracts/registry.yaml", "skills-engine", "reference/")

    def test_external_dir_exempt(self):
        self._check_exempt("external/CONTEXT.md", "skills-engine", "external/")

    def test_frameworks_dir_exempt(self):
        self._check_exempt("frameworks/patterns/ARCH.md", "skills-engine", "frameworks/")

    def test_org_design_tooling_src_exempt(self):
        self._check_exempt("org-design-tooling/src/gen.sh", "skills-engine",
                           "org-design-tooling/src/")

    def test_audits_dir_exempt(self):
        self._check_exempt("audits/rollup.md", "skills-engine", "audits/")

    def test_tests_dir_exempt(self):
        self._check_exempt("tests/unit/test_resolver.py", "skills-engine", "tests/")

    def test_cast_engine_exempt(self):
        self._check_exempt("cast/engine/scripts/render.py",
                           "# Path-history note: was skills-engine/", "cast/engine/")

    def test_worktrees_exempt(self):
        self._check_exempt(".worktrees/branch/file.py", "skills-engine", ".worktrees/")

    def test_entire_metadata_exempt(self):
        self._check_exempt(".entire/metadata/abc123/prompt.txt", "skills-engine", ".entire/")

    def test_product_paths_sh_exempt(self):
        self._check_exempt("product-paths.sh",
                           "export SKILLS_ENGINE_PATH=${FORGE_PATH}", "product-paths.sh")

    def test_context_md_exempt(self):
        self._check_exempt("CONTEXT.md", "skills-engine is old name", "CONTEXT.md")

    def test_tools_index_md_exempt(self):
        self._check_exempt("TOOLS-INDEX.md", "skills-engine/scripts/", "TOOLS-INDEX.md")

    def test_product_registry_md_exempt(self):
        self._check_exempt("PRODUCT_REGISTRY.md", "*(was skills-engine)*",
                           "PRODUCT_REGISTRY.md")

    def test_intent_md_exempt(self):
        self._check_exempt("INTENT.md", "skills-engine was renamed", "INTENT.md")

    def test_readme_md_exempt(self):
        self._check_exempt("README.md", "skills-engine", "README.md")

    def test_skill_md_exempt(self):
        self._check_exempt("SKILL.md", "skills engine development", "SKILL.md")

    def test_html_extension_exempt(self):
        self._check_exempt("dashboard.html", "<div>skills-engine</div>", ".html")

    def test_json_extension_exempt(self):
        self._check_exempt("products.json", '{"aliases": ["skills-engine"]}', ".json")

    def test_audit_filename_exempt(self):
        self._check_exempt("claude-md-audit-2026-04.md", "skills-engine", "*audit*")

    def test_retro_filename_exempt(self):
        self._check_exempt("RETRO-2026-04-01-old.md", "skills-engine", "RETRO-*")

    def test_binary_extension_skipped(self):
        self._check_exempt("image.png", "skills-engine", ".png (non-text)")


# ---------------------------------------------------------------------------
# emit_signal: honest closure-DoD frontmatter
# ---------------------------------------------------------------------------

class TestEmitSignalHonestDoD(unittest.TestCase):

    def test_emit_creates_file_with_dod_keys(self):
        mod = _import_inv()
        with tempfile.TemporaryDirectory() as d:
            sigdir = Path(d) / "signals"
            path = mod.emit_signal(sigdir, ["INV-RETIRED-TERM-SKILLS-ENGINE: bad.py — ..."])
            self.assertTrue(path.exists())
            text = path.read_text(encoding="utf-8")
            for key in ("upstream_control_path:", "catch_mechanism:", "pipeline_survival:"):
                self.assertIn(key, text, msg=f"Missing closure-DoD key: {key}\n{text}")
            self.assertIn("bad.py", text)


# ---------------------------------------------------------------------------
# Day-one zero-violation guarantee (feedback_invariant_zero_violation_start)
# ---------------------------------------------------------------------------

class TestDayOneZeroViolations(unittest.TestCase):
    """Against the REAL Core ecosystem, the invariant PASSES on day one.
    All pre-existing skills-engine references are covered by the allowlist."""

    def test_real_ecosystem_zero_violations(self):
        mod = _import_inv()
        passed, violations = mod.invariant_no_live_skills_engine_reference(CORE_ROOT)
        self.assertTrue(
            passed,
            msg=(
                f"Day-one zero-violation contract broken — {len(violations)} violation(s).\n"
                f"ACTION: Expand allowlist in retired_term_invariants.py, "
                f"do NOT edit content files.\n"
                f"Violations:\n" + "\n".join(f"  {v}" for v in violations)
            ),
        )


# ---------------------------------------------------------------------------
# main() exit codes
# ---------------------------------------------------------------------------

class TestMainExitCodes(unittest.TestCase):

    def test_main_real_exit_0(self):
        """Against the real ecosystem, exits 0 on day one."""
        r = subprocess.run([sys.executable, str(INV_SCRIPT)], capture_output=True, text=True)
        self.assertEqual(r.returncode, 0,
                         msg=f"stdout:\n{r.stdout}\nstderr:\n{r.stderr}")

    def test_main_json_flag_passes_and_is_valid_json(self):
        r = subprocess.run([sys.executable, str(INV_SCRIPT), "--json"],
                           capture_output=True, text=True)
        self.assertEqual(r.returncode, 0, msg=f"{r.stdout}\n{r.stderr}")
        data = json.loads(r.stdout)
        self.assertTrue(data["passed"])
        self.assertEqual(data["invariant"], "INV-RETIRED-TERM-SKILLS-ENGINE")
        self.assertEqual(data["violations"], [])

    def test_main_fail_on_dirty_root(self):
        """A temp dir with a live reference exits 1."""
        with tempfile.TemporaryDirectory() as d:
            Path(d, "bad.py").write_text("skills-engine = 'active'\n", encoding="utf-8")
            r = subprocess.run(
                [sys.executable, str(INV_SCRIPT), "--root", d],
                capture_output=True, text=True,
            )
            self.assertEqual(r.returncode, 1,
                             msg=f"Expected exit 1 on violation.\nstdout:{r.stdout}")


if __name__ == "__main__":
    unittest.main(verbosity=2)
