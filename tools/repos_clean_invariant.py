#!/usr/bin/env python3
"""
repos_clean_invariant.py — cross-product repo-hygiene chain_audit invariant class.

WHY THIS EXISTS
  The recurring-repo-dirty-churn problem (SIG-2026-06-02) erodes `git status` as a
  "this repo is settled" signal that the cast pre-flight gate + multi-session
  collision-avoidance rely on. The durable fix is per-producer write-through (each
  producer commits its own output); the repo-hygiene SWEEP is the catch-net. This
  module PROMOTES the catch-net into a cross-product chain_audit invariant — the
  same governance shape as value_term_invariants.py / cortege_invariants.py — so it
  runs in the nightly/overwatch invariant suite and emits honest-DoD signals.

  Charter: Core/products/parallax/spec/2026-06-02-overwatch-charter.md (§7)

INVARIANTS
  INV-REPOS-CLEAN
    No REGISTERED churn source with status: fixed is dirty again. A source the
    register declares "fixed" (durable write-through wired) whose paths show up
    dirty in the sweep is a WRITE-THROUGH REGRESSION — the exact failure mode the
    catch-net exists to catch. Sources registered open|tracked|deferred are
    ACKNOWLEDGED DEBT, not violations — so the invariant fires zero violations on
    day one (feedback_invariant_zero_violation_start). Class D (in-flight work) is
    NEVER a violation.

  INV-REPOS-CLEAN-COVERAGE
    Every repo known to emit automated churn (KNOWN_CHURN_REPOS) has a
    churn-source-register.yaml. Catches: a new churn-producing repo with no
    register, or a register deleted. Structural/deterministic.

  (Unregistered-but-detected automated churn is an ADVISORY — surfaced by the
   sweep, reported here as advisory — intentionally NOT a hard gate, so the
   invariant stays zero-violation on day one. This mirrors value_term_audit's
   fuzzy --scan being advisory, not a hard invariant.)

USAGE
  python3 repos_clean_invariant.py [--root PATH] [--emit-signal] [--json]
  Exit 0 = all invariants pass · 1 = one or more failed.

COMPOSES WITH
  - repo-hygiene-sweep.py    — the engine (classification single-source-of-truth)
  - churn-source-register.yaml (per-product, rglob-discovered) — the write-through truth
  - value_term_invariants.py — same invariant signature (the pattern this mirrors)
  - org-design-tooling governance_audit.py — the intended nightly consumer
"""
from __future__ import annotations

import argparse
import importlib.util
import json
import sys
from datetime import date
from pathlib import Path

# tools → intent → frameworks → Core → Workspaces
DEFAULT_ROOT = Path(__file__).resolve().parents[4]
DEFAULT_SIGNALS_DIR = Path(__file__).resolve().parents[1] / ".intent" / "signals"

# Load the sweep (hyphenated filename → importlib by path). Single source of truth
# for repo discovery + classification; the invariant never reimplements it.
_SWEEP_PATH = (DEFAULT_ROOT / "Core" / "products" / "org-design-tooling" /
               "src" / "repo-hygiene-sweep.py")


def _load_sweep():
    spec = importlib.util.spec_from_file_location("repo_hygiene_sweep", _SWEEP_PATH)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


# Repos known to emit automated churn → each MUST own a churn-source-register.yaml.
# Extend when a new churn-producing repo ships.
KNOWN_CHURN_REPOS = {
    "org-design-tooling": "Core/products/org-design-tooling",
    "pulse": "Core/products/pulse",
    "library-index": "Core/products/library-index",
}

# Repos with KNOWN churn whose register is owned by another track (advisory, not a
# hard coverage failure — keeps zero-violation while honestly flagging the gap).
DEFERRED_REPOS = {
    "cast": "Core/products/cast — root-class A (regen); register owned by HA-1's deterministic-write fix",
}


# ---------------------------------------------------------------------------
# INV-REPOS-CLEAN
# ---------------------------------------------------------------------------

def invariant_repos_clean(root: Path) -> tuple[bool, list[str], list[str]]:
    """No status:fixed registered source is dirty again. Returns (passed, violations, advisories)."""
    sweep = _load_sweep()
    result = sweep.sweep(root, apply=False)
    violations: list[str] = []
    advisories: list[str] = []
    for repo in result["repos"]:
        for f in repo["findings"]:
            cls = f["class"]
            if cls == "D":
                continue
            if f["registered"]:
                if f.get("source_status") == "fixed" and cls in ("A", "B", "C"):
                    violations.append(
                        f"INV-REPOS-CLEAN: {repo['repo']}: '{f['path']}' is dirty but its "
                        f"source ({f.get('source_id')}) is registered status:fixed — "
                        f"WRITE-THROUGH REGRESSION."
                    )
                # open|tracked|deferred = acknowledged debt, not a violation
            else:
                if cls in ("A", "B"):
                    advisories.append(
                        f"advisory: {repo['repo']}: '{f['path']}' looks like automated churn "
                        f"(class {cls}) but is UNREGISTERED — add it to "
                        f"{repo['repo']}/churn-source-register.yaml with a disposition."
                    )
    return len(violations) == 0, violations, advisories


# ---------------------------------------------------------------------------
# INV-REPOS-CLEAN-COVERAGE
# ---------------------------------------------------------------------------

def invariant_coverage(root: Path) -> tuple[bool, list[str], list[str]]:
    """Every KNOWN_CHURN_REPOS repo has a churn-source-register.yaml."""
    violations: list[str] = []
    advisories: list[str] = []
    for name, rel in KNOWN_CHURN_REPOS.items():
        reg = root / rel / "churn-source-register.yaml"
        if not reg.exists():
            violations.append(
                f"INV-REPOS-CLEAN-COVERAGE: {name} ({rel}) has automated churn but no "
                f"churn-source-register.yaml."
            )
    for name, note in DEFERRED_REPOS.items():
        rel = note.split(" — ", 1)[0].strip()  # path is the prefix before ' — '
        reg_path = root / rel / "churn-source-register.yaml"
        if not reg_path.exists():
            advisories.append(f"advisory (deferred): {name} — register pending: {note}")
    return len(violations) == 0, violations, advisories


# ---------------------------------------------------------------------------
# Runner
# ---------------------------------------------------------------------------

def run(root: Path) -> dict:
    clean_ok, clean_v, clean_adv = invariant_repos_clean(root)
    cov_ok, cov_v, cov_adv = invariant_coverage(root)
    return {
        "passed": clean_ok and cov_ok,
        "invariants": {
            "INV-REPOS-CLEAN": {"passed": clean_ok, "violations": clean_v},
            "INV-REPOS-CLEAN-COVERAGE": {"passed": cov_ok, "violations": cov_v},
        },
        "advisories": clean_adv + cov_adv,
    }


def main() -> int:
    ap = argparse.ArgumentParser(description="repos-clean chain_audit invariant")
    ap.add_argument("--root", type=Path, default=DEFAULT_ROOT)
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--emit-signal", action="store_true")
    args = ap.parse_args()

    res = run(args.root.resolve())

    if args.json:
        print(json.dumps(res, indent=2))
    else:
        for inv, d in res["invariants"].items():
            mark = "✅ PASS" if d["passed"] else "❌ FAIL"
            print(f"{mark}  {inv}")
            for v in d["violations"]:
                print(f"    {v}")
        if res["advisories"]:
            print(f"\nℹ {len(res['advisories'])} advisory(ies):")
            for a in res["advisories"]:
                print(f"    {a}")
        print(f"\n{'✅ ALL INVARIANTS PASS' if res['passed'] else '❌ INVARIANT FAILURE'}")

    if args.emit_signal and not res["passed"]:
        DEFAULT_SIGNALS_DIR.mkdir(parents=True, exist_ok=True)
        sig = DEFAULT_SIGNALS_DIR / f"SIG-REPOS-CLEAN-VIOLATION-{date.today().isoformat()}.md"
        body = ["---", "type: notice", "series: repos-clean",
                f"date: {date.today().isoformat()}", "status: open",
                "source: repos_clean_invariant.py", "---", "",
                "# repos-clean invariant violation", ""]
        for inv, d in res["invariants"].items():
            for v in d["violations"]:
                body.append(f"- {v}")
        sig.write_text("\n".join(body) + "\n")
        print(f"\nemitted: {sig}")

    return 0 if res["passed"] else 1


if __name__ == "__main__":
    sys.exit(main())
