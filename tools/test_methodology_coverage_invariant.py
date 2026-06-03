#!/usr/bin/env python3
"""
test_methodology_coverage_invariant.py — tests for the Forge↔methodology coverage invariant.

Runs under pytest OR standalone (`python3 test_methodology_coverage_invariant.py`).
Pure stdlib — builds synthetic ecosystem trees in a tempdir.
"""
from __future__ import annotations

import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import methodology_coverage_invariant as mci  # noqa: E402


def _skill(root: Path, domain: str, skill: str, methodology: str | None = None) -> None:
    d = root / mci.SKILLS_REL / domain / skill
    d.mkdir(parents=True, exist_ok=True)
    fm = ["---", f"name: {skill}", "description: test"]
    if methodology is not None:
        fm.insert(1, f"methodology: {methodology}")
    fm += ["---", "", f"# {skill}", "body"]
    (d / "SKILL.md").write_text("\n".join(fm) + "\n", encoding="utf-8")


def _module(root: Path, domain: str, name: str) -> None:
    d = root / mci.LIB_REL / domain
    d.mkdir(parents=True, exist_ok=True)
    (d / name).write_text("---\ntype: methodology\n---\n# module\n", encoding="utf-8")


def test_coverage_pass():
    with tempfile.TemporaryDirectory() as t:
        root = Path(t)
        _skill(root, "discovery", "jtbd-extractor")
        _module(root, "discovery", "discovery-core.md")
        passed, violations = mci.invariant_domain_coverage(root)
        assert passed and violations == [], violations


def test_coverage_fail_when_domain_has_no_module():
    with tempfile.TemporaryDirectory() as t:
        root = Path(t)
        _skill(root, "critique", "panel-critique")  # skill, but no critique module
        passed, violations = mci.invariant_domain_coverage(root)
        assert not passed and any("critique" in v for v in violations), violations


def test_coverage_ignores_non_skill_dirs():
    with tempfile.TemporaryDirectory() as t:
        root = Path(t)
        # 'personas' is a NON_SKILL_DIR — even with a SKILL.md it must not require a module
        _skill(root, "personas", "some-persona")
        passed, _ = mci.invariant_domain_coverage(root)
        assert passed


def test_nodangling_pass():
    with tempfile.TemporaryDirectory() as t:
        root = Path(t)
        _module(root, "critique", "panel-critique.md")
        _skill(root, "critique", "panel-critique",
               methodology="Core/frameworks/methodology-library/critique/panel-critique.md")
        passed, violations = mci.invariant_no_dangling(root)
        assert passed and violations == [], violations


def test_nodangling_fail_on_missing_target():
    with tempfile.TemporaryDirectory() as t:
        root = Path(t)
        _module(root, "operations", "workspace-hygiene.md")  # domain has a module (coverage ok)
        _skill(root, "operations", "docx-edit",
               methodology="Core/frameworks/methodology-library/operations/docx-edit-safety.md")  # absent
        passed, violations = mci.invariant_no_dangling(root)
        assert not passed and any("docx-edit-safety" in v for v in violations), violations


def test_wiring_warns_unwired_and_skips_deferred():
    with tempfile.TemporaryDirectory() as t:
        root = Path(t)
        _module(root, "operations", "workspace-hygiene.md")
        _skill(root, "operations", "meeting-processor")          # unwired -> WARN
        _skill(root, "operations", "docx-edit")                  # unwired but DEFERRED -> skip
        warns, deferred = mci.check_wiring(root)
        assert any("meeting-processor" in w for w in warns), warns
        assert any("docx-edit" in d for d in deferred), deferred
        assert not any("docx-edit" in w for w in warns), "deferred skill must not WARN"


def test_read_pointer_and_resolve():
    with tempfile.TemporaryDirectory() as t:
        root = Path(t)
        _module(root, "research", "research-core.md")
        _skill(root, "research", "freshen",
               methodology="Core/frameworks/methodology-library/research/research-core.md")
        skill_md = root / mci.SKILLS_REL / "research" / "freshen" / "SKILL.md"
        ptr = mci.read_methodology_pointer(skill_md)
        assert ptr and ptr.endswith("research-core.md"), ptr
        assert mci.resolve_pointer(root, ptr) is not None


def _run_standalone() -> int:
    tests = [v for k, v in sorted(globals().items()) if k.startswith("test_") and callable(v)]
    failed = 0
    for fn in tests:
        try:
            fn()
            print(f"PASS {fn.__name__}")
        except AssertionError as e:
            failed += 1
            print(f"FAIL {fn.__name__}: {e}")
    print(f"\n{len(tests) - failed}/{len(tests)} passed")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(_run_standalone())
