#!/usr/bin/env python3
"""
methodology_coverage_invariant.py — Forge↔methodology-library coverage chain_audit invariant.

WHY THIS EXISTS
  The methodology library (Core/frameworks/methodology-library/) is the canonical
  source of process knowledge that Forge skills render. ARCHITECTURE.md §3 states
  the Rule-of-Three gate as a MANUAL discipline — nothing fails loud when a Forge
  skill ships with no methodology ancestry, or when a skill points at a methodology
  module that does not exist. Two audits flagged this missing automated catch-net:
    - SIG-AUDIT-2026-05-20 (methodology-library)
    - SIG-EXEC-2026-05-20-ML-SPEC-001-CONT follow-up #1
  This module IS that catch-net. Pure stdlib (no pyyaml) so it runs anywhere the
  overwatch/nightly suite runs.

INVARIANTS
  INV-METHODOLOGY-COVERAGE  (hard)
    Every Forge skill DOMAIN that contains >=1 SKILL.md has a corresponding
    methodology-library/{domain}/ directory holding >=1 module file. Catches a new
    skill domain shipped with no methodology ancestry, or a domain's modules
    deleted. Zero-violation as of 2026-06-03 (the critique extraction closed the
    last domain gap).

  INV-METHODOLOGY-NODANGLING  (hard)
    Every `methodology:` frontmatter pointer in a SKILL.md resolves to an existing
    module file. Catches the docx-edit-safety class (a pointer to a deferred/absent
    module). Zero-violation as of 2026-06-03.

  INV-METHODOLOGY-WIRING  (advisory — WARN, does NOT fail the suite by default)
    Every SKILL.md SHOULD carry a `methodology:` pointer so consumption is
    machine-traceable (ML-SPEC-005). Skills with no pointer are WARNed, except
    documented deferrals (DEFERRED_SKILLS). Advisory so the hard suite stays
    zero-violation on day one (feedback_invariant_zero_violation_start); the WARN
    count is the wiring-completeness metric ML-SPEC-005 drives to zero. Promote to
    a hard failure with --strict-wiring once wiring is complete.

USAGE
  python3 methodology_coverage_invariant.py [--root PATH] [--emit-signal] [--json] [--strict-wiring]
  Exit 0 = hard invariants pass · 1 = one or more hard invariants failed.

COMPOSES WITH
  - value_term_invariants.py / repos_clean_invariant.py — same governance shape
  - org-design-tooling governance_audit.py / overwatch — intended nightly consumer
"""
from __future__ import annotations

import argparse
import json
import sys
from datetime import date
from pathlib import Path

# tools → intent → frameworks → Core
DEFAULT_ROOT = Path(__file__).resolve().parents[3]
DEFAULT_SIGNALS_DIR = Path(__file__).resolve().parents[1] / ".intent" / "signals"

SKILLS_REL = "products/forge/outputs/claude-code"
LIB_REL = "frameworks/methodology-library"

# Dirs under claude-code/ that are NOT skill domains (no SKILL.md ancestry expected).
NON_SKILL_DIRS = {"personas", "workflows"}
# Files in a domain dir that are navigation/architecture, not methodology modules.
NON_MODULE_FILES = {"CONTEXT.md", "README.md", "ARCHITECTURE.md"}

# Skills whose methodology extraction is DOCUMENTED-deferred (Rule-of-Three not met).
# Keyed "domain/skill". The WIRING check skips these (a deferral is not a gap).
DEFERRED_SKILLS = {
    "operations/docx-edit": (
        "Rule-of-Three not met (2 incidents, both Subaru); extraction to "
        "operations/docx-edit-safety.md deferred per SKILL.md."
    ),
}


# ---------------------------------------------------------------------------
# helpers
# ---------------------------------------------------------------------------

def iter_skills(root: str | Path):
    """Yield (domain, skill, skill_md_path) for every SKILL.md under the skills root."""
    skills_root = Path(root) / SKILLS_REL
    if not skills_root.is_dir():
        return
    for skill_md in sorted(skills_root.glob("*/*/SKILL.md")):
        domain = skill_md.parent.parent.name
        if domain in NON_SKILL_DIRS:
            continue
        yield domain, skill_md.parent.name, skill_md


def domain_modules(root: str | Path, domain: str) -> list[Path]:
    """Module files in methodology-library/{domain}/ (excludes nav/architecture files)."""
    d = Path(root) / LIB_REL / domain
    if not d.is_dir():
        return []
    return sorted(
        p for p in d.glob("*.md")
        if p.name not in NON_MODULE_FILES
    )


def read_methodology_pointer(skill_md: Path) -> str | None:
    """Return the top-level `methodology:` frontmatter value, or None. Stdlib only."""
    try:
        text = skill_md.read_text(encoding="utf-8")
    except OSError:
        return None
    if not text.startswith("---"):
        return None
    # isolate the frontmatter block (between the first two '---' fences)
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        return None
    for i in range(1, len(lines)):
        if lines[i].strip() == "---":
            block = lines[1:i]
            break
    else:
        return None
    for line in block:
        # top-level key only (no leading whitespace)
        if line.startswith("methodology:") or line.startswith("methodology_source:"):
            val = line.split(":", 1)[1].strip().strip('"').strip("'")
            return val or None
    return None


def resolve_pointer(root: str | Path, pointer: str) -> Path | None:
    """Resolve a `Core/...`-style or root-relative module pointer to an existing file."""
    root = Path(root)
    candidates = [
        root.parent / pointer,                       # pointer like "Core/frameworks/..."
        root / pointer,                              # pointer relative to Core/
        root / pointer.replace("Core/", "", 1),      # defensive
    ]
    for c in candidates:
        if c.is_file():
            return c
    return None


# ---------------------------------------------------------------------------
# INV-METHODOLOGY-COVERAGE
# ---------------------------------------------------------------------------

def invariant_domain_coverage(root: str | Path) -> tuple[bool, list[str]]:
    """Every skill domain (>=1 SKILL.md) has >=1 methodology module."""
    domains_with_skills: dict[str, int] = {}
    for domain, _skill, _path in iter_skills(root):
        domains_with_skills[domain] = domains_with_skills.get(domain, 0) + 1

    violations: list[str] = []
    for domain in sorted(domains_with_skills):
        if not domain_modules(root, domain):
            violations.append(
                f"INV-METHODOLOGY-COVERAGE: skill domain '{domain}' has "
                f"{domains_with_skills[domain]} skill(s) but NO methodology module in "
                f"{LIB_REL}/{domain}/ — skills in this domain have no methodology ancestry."
            )
    return len(violations) == 0, violations


# ---------------------------------------------------------------------------
# INV-METHODOLOGY-NODANGLING
# ---------------------------------------------------------------------------

def invariant_no_dangling(root: str | Path) -> tuple[bool, list[str]]:
    """Every `methodology:` pointer in a SKILL.md resolves to an existing module."""
    violations: list[str] = []
    for domain, skill, skill_md in iter_skills(root):
        ptr = read_methodology_pointer(skill_md)
        if ptr and resolve_pointer(root, ptr) is None:
            violations.append(
                f"INV-METHODOLOGY-NODANGLING: skill '{domain}/{skill}' points at "
                f"methodology '{ptr}' which does not exist on disk."
            )
    return len(violations) == 0, violations


# ---------------------------------------------------------------------------
# INV-METHODOLOGY-WIRING  (advisory)
# ---------------------------------------------------------------------------

def check_wiring(root: str | Path) -> tuple[list[str], list[str]]:
    """Return (warns, deferred_skipped). A skill with no pointer (and not deferred) WARNs."""
    warns: list[str] = []
    deferred: list[str] = []
    for domain, skill, skill_md in iter_skills(root):
        key = f"{domain}/{skill}"
        if read_methodology_pointer(skill_md):
            continue
        if key in DEFERRED_SKILLS:
            deferred.append(f"{key} — {DEFERRED_SKILLS[key]}")
            continue
        warns.append(
            f"INV-METHODOLOGY-WIRING: skill '{key}' carries no `methodology:` pointer "
            f"(consumption traceable only by grep; ML-SPEC-005)."
        )
    return warns, deferred


# ---------------------------------------------------------------------------
# Signal emission (honest closure-DoD frontmatter)
# ---------------------------------------------------------------------------

def emit_signal(signals_dir: str | Path, invariant_id: str, violations: list[str]) -> Path:
    signals_dir = Path(signals_dir)
    signals_dir.mkdir(parents=True, exist_ok=True)
    today = date.today().isoformat()
    path = signals_dir / f"SIG-METHODOLOGY-{invariant_id}-VIOLATION-{today}.md"
    body = f"""---
id: SIG-METHODOLOGY-{invariant_id}-VIOLATION-{today}
product: intent
type: invariant-violation
status: open
created: {today}
invariant: {invariant_id}
upstream_control_path: "Core/frameworks/intent/tools/methodology_coverage_invariant.py — the methodology modules in Core/frameworks/methodology-library/{{domain}}/ are the source-of-truth; this invariant verifies every Forge skill has ancestry."
catch_mechanism: "methodology_coverage_invariant.py {invariant_id} + test_methodology_coverage_invariant.py — run in the nightly/overwatch invariant suite."
pipeline_survival: "Methodology modules are source-of-truth inputs, not pipeline outputs; no render_all wipes them. A violation surfaces a coverage/wiring gap and does not block execution."
---

# {invariant_id} Violation — {today}

## Violations

"""
    for v in violations:
        body += f"- {v}\n"
    body += f"""
## Required action

Author the missing methodology module in methodology-library/{{domain}}/ (Rule-of-Three:
3+ skills sharing the knowledge), or fix the dangling `methodology:` pointer to a real
module. Re-run `python3 methodology_coverage_invariant.py` to verify, then close this
signal with upstream_control_path + catch_mechanism.

*Auto-emitted by methodology_coverage_invariant.py {today}.*
"""
    path.write_text(body, encoding="utf-8")
    return path


# ---------------------------------------------------------------------------
# main
# ---------------------------------------------------------------------------

def main(argv=None) -> int:
    ap = argparse.ArgumentParser(
        description="Forge↔methodology-library coverage chain_audit invariant class.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )
    ap.add_argument("--root", default=str(DEFAULT_ROOT), help="Ecosystem root (default: Core/).")
    ap.add_argument("--emit-signal", action="store_true", help="Emit a signal on hard failure.")
    ap.add_argument("--signals-dir", default=str(DEFAULT_SIGNALS_DIR),
                    help="Where to write violation signals.")
    ap.add_argument("--json", action="store_true", help="Output results as JSON.")
    ap.add_argument("--strict-wiring", action="store_true",
                    help="Promote the advisory WIRING warning to a hard failure.")
    args = ap.parse_args(argv)
    root = args.root

    hard_checks = [
        ("INV-METHODOLOGY-COVERAGE", lambda: invariant_domain_coverage(root)),
        ("INV-METHODOLOGY-NODANGLING", lambda: invariant_no_dangling(root)),
    ]
    results: dict[str, dict] = {}
    all_passed = True
    for inv_id, fn in hard_checks:
        passed, violations = fn()
        results[inv_id] = {"passed": passed, "violations": violations}
        if not passed:
            all_passed = False
            if args.emit_signal:
                results[inv_id]["signal_emitted"] = str(emit_signal(args.signals_dir, inv_id, violations))

    warns, deferred = check_wiring(root)
    wiring_passed = (len(warns) == 0) if args.strict_wiring else True
    results["INV-METHODOLOGY-WIRING"] = {
        "passed": wiring_passed, "warns": warns, "deferred": deferred,
        "advisory": not args.strict_wiring,
    }
    if args.strict_wiring and not wiring_passed:
        all_passed = False
        if args.emit_signal:
            results["INV-METHODOLOGY-WIRING"]["signal_emitted"] = str(
                emit_signal(args.signals_dir, "INV-METHODOLOGY-WIRING", warns))

    if args.json:
        print(json.dumps({"root": str(root), "passed": all_passed, "results": results}, indent=2))
    else:
        print("=" * 78)
        print("  METHODOLOGY-COVERAGE CHAIN-AUDIT — Forge↔methodology-library")
        print(f"  Root: {root}")
        print("=" * 78)
        for inv_id in ("INV-METHODOLOGY-COVERAGE", "INV-METHODOLOGY-NODANGLING"):
            r = results[inv_id]
            print(f"\n[{'PASS' if r['passed'] else 'FAIL'}] {inv_id}")
            for v in r["violations"]:
                print(f"       {v}")
        w = results["INV-METHODOLOGY-WIRING"]
        tag = "FAIL" if (args.strict_wiring and not w["passed"]) else ("PASS" if not w["warns"] else "WARN")
        print(f"\n[{tag}] INV-METHODOLOGY-WIRING ({'advisory' if w['advisory'] else 'strict'}) "
              f"— {len(w['warns'])} skill(s) unwired, {len(w['deferred'])} deferred")
        for v in w["warns"]:
            print(f"       {v}")
        for d in w["deferred"]:
            print(f"       (deferred, OK) {d}")
        print()
        if all_passed:
            print("✓ Hard invariants PASS — every skill domain has methodology ancestry, "
                  "no dangling pointers.")
        else:
            failing = [k for k in ("INV-METHODOLOGY-COVERAGE", "INV-METHODOLOGY-NODANGLING")
                       if not results[k]["passed"]]
            if args.strict_wiring and not w["passed"]:
                failing.append("INV-METHODOLOGY-WIRING")
            print(f"✗ {len(failing)} hard invariant(s) FAILED: {', '.join(failing)}")

    return 0 if all_passed else 1


if __name__ == "__main__":
    sys.exit(main())
