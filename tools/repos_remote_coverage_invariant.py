#!/usr/bin/env python3
"""
repos_remote_coverage_invariant.py — every product repo is backed up to GitHub.

WHY THIS EXISTS
  SIG-REPO-COVERAGE-2026-06-04: lodestone (and then understudy) shipped with NO git
  remote and were only caught by a manual `git remote` sweep. Local-only product
  material is at disk-loss risk and sits outside the L4 push flow. This promotes the
  manual sweep into a cross-product chain_audit invariant — the same governance shape
  as repos_clean_invariant.py — so a remote-less or unpushed product FAILS LOUDLY in
  the nightly/overwatch suite instead of slipping.

INVARIANTS
  INV-REPO-HAS-REMOTE   Every git repo under Core/products/<X> has an `origin` remote.
  INV-REPO-PUSHED       No product repo's checked-out branch is ahead of its upstream
                        (committed work not on GitHub). No-upstream → advisory.

  Zero-violation-start (feedback_invariant_zero_violation_start): as of 2026-06-04 all
  Core/products/* repos have remotes and are pushed (lodestone + understudy remotes
  created; forge/fieldbook/org-design-tooling pushed), so this fires zero violations
  on install.

USAGE
  python3 repos_remote_coverage_invariant.py [--root PATH] [--scope products|all] [--json] [--emit-signal]
  Exit 0 = all covered · 1 = one or more coverage gaps.

COMPOSES WITH
  - repos_clean_invariant.py        — sibling invariant (dirty-churn lens); same shape
  - org-design-tooling governance_audit.py — the intended nightly consumer
"""
from __future__ import annotations

import argparse
import json
import subprocess
import sys
from datetime import date
from pathlib import Path

# tools → intent → frameworks → Core → Workspaces
DEFAULT_ROOT = Path(__file__).resolve().parents[4]
DEFAULT_SIGNALS_DIR = Path(__file__).resolve().parents[1] / ".intent" / "signals"


def _git(repo: Path, *args: str) -> subprocess.CompletedProcess:
    return subprocess.run(["git", "-C", str(repo), *args], capture_output=True, text=True)


def _product_repos(root: Path, scope: str) -> list[Path]:
    bases = [root / "Core" / "products"]
    if scope == "all":
        bases.append(root / "Core" / "frameworks")
    repos: list[Path] = []
    for base in bases:
        if not base.exists():
            continue
        for child in sorted(base.iterdir()):
            if not child.is_dir() or child.name.startswith("_"):
                continue
            if (child / ".git").exists():
                repos.append(child)
    return repos


def invariant_coverage(root: Path, scope: str):
    """Returns (passed, violations, advisories)."""
    violations: list[str] = []
    advisories: list[str] = []
    for repo in _product_repos(root, scope):
        rel = str(repo.relative_to(root))
        if _git(repo, "remote", "get-url", "origin").returncode != 0:
            violations.append(
                f"INV-REPO-HAS-REMOTE: {rel} has no `origin` remote — local-only, at "
                f"disk-loss risk. Fix: gh repo create theparlor/{repo.name} --private "
                f"--source={repo} --push")
            continue
        r = _git(repo, "rev-list", "--count", "@{u}..HEAD")
        if r.returncode != 0:
            advisories.append(
                f"advisory: {rel} — current branch has no upstream tracking; can't verify pushed state.")
            continue
        ahead = int((r.stdout or "0").strip() or 0)
        if ahead > 0:
            violations.append(
                f"INV-REPO-PUSHED: {rel} is {ahead} commit(s) ahead of its remote — "
                f"committed work not on GitHub. Fix: git -C {repo} push")
    return len(violations) == 0, violations, advisories


def run(root: Path, scope: str) -> dict:
    ok, v, adv = invariant_coverage(root, scope)
    return {
        "passed": ok,
        "scope": scope,
        "invariants": {"INV-REPO-COVERAGE": {"passed": ok, "violations": v}},
        "advisories": adv,
    }


def main() -> int:
    ap = argparse.ArgumentParser(description="product-repo remote-coverage chain_audit invariant")
    ap.add_argument("--root", type=Path, default=DEFAULT_ROOT)
    ap.add_argument("--scope", choices=["products", "all"], default="products")
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--emit-signal", action="store_true")
    args = ap.parse_args()

    res = run(args.root.resolve(), args.scope)

    if args.json:
        print(json.dumps(res, indent=2))
    else:
        d = res["invariants"]["INV-REPO-COVERAGE"]
        print(f"{'✅ PASS' if d['passed'] else '❌ FAIL'}  INV-REPO-HAS-REMOTE / INV-REPO-PUSHED  (scope={res['scope']})")
        for v in d["violations"]:
            print(f"    {v}")
        if res["advisories"]:
            print(f"\nℹ {len(res['advisories'])} advisory(ies):")
            for a in res["advisories"]:
                print(f"    {a}")
        print(f"\n{'✅ ALL PRODUCT REPOS COVERED' if res['passed'] else '❌ COVERAGE GAP'}")

    if args.emit_signal and not res["passed"]:
        DEFAULT_SIGNALS_DIR.mkdir(parents=True, exist_ok=True)
        sig = DEFAULT_SIGNALS_DIR / f"SIG-REPO-COVERAGE-VIOLATION-{date.today().isoformat()}.md"
        body = ["---", "type: notice", "series: repo-coverage",
                f"date: {date.today().isoformat()}", "status: open",
                "source: repos_remote_coverage_invariant.py", "---", "",
                "# repo remote-coverage violation", ""]
        for v in res["invariants"]["INV-REPO-COVERAGE"]["violations"]:
            body.append(f"- {v}")
        sig.write_text("\n".join(body) + "\n")
        print(f"\nemitted: {sig}")

    return 0 if res["passed"] else 1


if __name__ == "__main__":
    sys.exit(main())
