#!/usr/bin/env python3
"""
retired_term_invariants.py — chain_audit invariant: no live "skills-engine" reintroductions.

WHY THIS EXISTS
  "skills-engine" was the former product name for Forge (renamed 2026-04 per WS-DDR-027).
  The retirement is canonically registered in:
    - ~/.claude/hooks/helpers/product-paths.sh  (SKILLS_ENGINE_PATH alias → forge)
    - Core/products/products.json               (aliases: ["skills-engine"])

  This invariant ensures the retired term is never re-introduced as a LIVE reference
  in non-allowlisted files. Allowlisted: alias definitions, historical paths
  (.intent/, journal/, corpus/, dated audit/consistency-audit files, *.DEPRECATED),
  and an extended set of historical planning/spec/corpus paths documented inline.

INVARIANT
  INV-RETIRED-TERM-SKILLS-ENGINE
    No non-allowlisted file under Core/ contains the retired product-name strings
    "skills-engine", "skills_engine", "SKILLS_ENGINE", or "SkillsEngine".
    Violations indicate a genuine new reintroduction that should be corrected to
    "forge", "Forge", or "FORGE" as appropriate.

    Zero violations on day one is guaranteed by the allowlist, which covers all
    pre-existing historical references (feedback_invariant_zero_violation_start).
    If the allowlist fires false positives, EXPAND IT — do NOT edit content files.

USAGE
  python3 retired_term_invariants.py [--root PATH] [--emit-signal] [--json]
  Exit 0 = invariant passes · 1 = violations found

COMPOSES WITH
  - value_term_invariants.py        — same invariant signature in this dir
  - cortege_invariants.py           — per-product precedent
  - chain_audit_portfolio.py        — cross-product precedent (WS-DDR-078)
  - governance_audit.py Check 20    — nightly/overwatch suite consumer
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from datetime import date
from pathlib import Path

# tools → intent → frameworks → Core
DEFAULT_ROOT = Path(__file__).resolve().parents[3]
DEFAULT_SIGNALS_DIR = Path(__file__).resolve().parents[1] / ".intent" / "signals"

# ---------------------------------------------------------------------------
# Search patterns — all variants of the retired term
# ---------------------------------------------------------------------------

RETIRED_TERM_PATTERNS: list[re.Pattern] = [
    re.compile(r"skills.engine", re.IGNORECASE),  # skills-engine, skills_engine
    re.compile(r"SkillsEngine"),
    re.compile(r"SKILLS_ENGINE"),
]

# Extensions to scan; everything else (images, compiled artifacts) is skipped.
SCAN_EXTENSIONS = {
    ".py", ".sh", ".md", ".yaml", ".yml", ".json", ".txt", ".html",
    ".toml", ".rst", ".js", ".ts", ".css",
}

# ---------------------------------------------------------------------------
# Allowlist
#
# A file is EXEMPT if ANY rule below matches.  Rationale for each block is
# inline.  If the invariant fires on a legitimate historical file, add its
# path pattern here — never edit the content file.
# ---------------------------------------------------------------------------

# Substring in the full path → exempt.
_PATH_SEGMENT_ALLOWLIST = [
    # ── Intent dogfood: signals, decisions, specs ────────────────────────────
    "/.intent/",
    "/.intent-journal/",
    # ── Historical journals and digest archives ──────────────────────────────
    "/journal/",
    "/digests/",
    "/subscriptions/",          # reference/subscriptions/ (RETRO files)
    # ── Content corpus — raw source material, always historical ──────────────
    "/corpus/",
    # ── Product farm data — operators, intake reports, pliable IR ────────────
    "/farm/",                   # covers farm/intake/, farm/pliable/, farm/operators/, farm/docs/
    # ── Archived intake and evaluation reports ───────────────────────────────
    "/_intake/",                # products/_intake/YYYY-MM-DD-*/
    # ── Historical runtime state ─────────────────────────────────────────────
    "/.state/",
    # ── Claude project command files ─────────────────────────────────────────
    "/.claude/",
    # ── Forge internals — the successor product; self-references are ─────────
    # ── historical variable names or path comments, not live product refs ─────
    "/forge/engine/",
    "/forge/outputs/",
    # ── Session-scoped working artifacts ─────────────────────────────────────
    "/working/",
    # ── Planning, spec, and prompt archives (across all products) ────────────
    "/plans/",
    "/prompts/",
    "/spec/",                   # topography/spec/, voices/spec/, fieldbook/spec/, odt/spec/
    # ── Parallax decision-support and brand map HTML ─────────────────────────
    "/decision-support/",
    "/brand/",
    # ── Reference materials and external repos — always historical ────────────
    "/reference/",
    "/external/",
    # ── Framework documentation — historical term usage is expected ───────────
    "/frameworks/",
    # ── Org-design-tooling generator scripts and audit outputs ───────────────
    "/org-design-tooling/src/",
    "/audits/",
    # ── Test fixtures ────────────────────────────────────────────────────────
    "/tests/",
    # ── Cast engine scripts — "Path-history note (2026-04-29)" comments ──────
    "/cast/engine/",
    # ── Git worktree checkouts — transient, not canonical ────────────────────
    "/.worktrees/",
    # ── Entire.io observability session metadata ─────────────────────────────
    "/.entire/",
    # ── Cowork / session-context handoff artifacts ────────────────────────────
    "/.context/",
]

# Regex matched against the filename (basename only) → exempt.
_FILENAME_PATTERN_ALLOWLIST = [
    re.compile(r"audit", re.IGNORECASE),         # *audit*.md  (consistency-audit etc.)
    re.compile(r"^RETRO", re.IGNORECASE),         # RETRO-YYYY-*.md
    re.compile(r"\.DEPRECATED$", re.IGNORECASE),  # *.DEPRECATED
    re.compile(r"\.html$", re.IGNORECASE),        # HTML dashboards and brand maps
    re.compile(r"\.json$", re.IGNORECASE),        # JSON configs (products.json etc.)
]

# Exact filenames (basename, case-sensitive) → always exempt.
# These are navigation docs, manifests, or the canonical alias-definition file
# where stale references to the old name are expected as historical notation.
_FILENAME_EXACT_ALLOWLIST = frozenset({
    "product-paths.sh",     # canonical alias: SKILLS_ENGINE_PATH → forge
    "CONTEXT.md",           # navigation index files at every level
    "TOOLS-INDEX.md",       # tools navigation index
    "PRODUCT_REGISTRY.md",  # product registry "*(was skills-engine)*" notation
    "INDEX.md",             # index docs
    "ARCHITECTURE.md",      # architecture reference docs
    "JOURNAL.md",           # journal root files
    "INTENT.md",            # product intent manifests
    "README.md",            # product READMEs
    "SKILL.md",             # skill definition files (rendered outputs)
    "CORE_IP_INDEX.md",     # master IP index (navigation doc with historical table)
    ".gitignore",           # git ignore files (often contain historical path comments)
})


def _is_allowlisted(path: Path) -> bool:
    """Return True if path is exempt from the invariant."""
    path_str = str(path)
    for seg in _PATH_SEGMENT_ALLOWLIST:
        if seg in path_str:
            return True
    if path.name in _FILENAME_EXACT_ALLOWLIST:
        return True
    for pat in _FILENAME_PATTERN_ALLOWLIST:
        if pat.search(path.name):
            return True
    return False


def _contains_retired_term(path: Path) -> bool:
    """Return True if the file text contains any retired-term pattern."""
    try:
        text = path.read_text(encoding="utf-8", errors="replace")
    except (OSError, PermissionError):
        return False
    return any(pat.search(text) for pat in RETIRED_TERM_PATTERNS)


# ---------------------------------------------------------------------------
# INV-RETIRED-TERM-SKILLS-ENGINE
# ---------------------------------------------------------------------------

def invariant_no_live_skills_engine_reference(
    root: str | Path,
) -> tuple[bool, list[str]]:
    """Scan for live 'skills-engine' references in non-allowlisted files.

    Returns (passed, violations). Each violation string is prefixed with the
    invariant ID and names the relative file path.
    """
    root = Path(root)
    violations: list[str] = []

    for path in root.rglob("*"):
        if not path.is_file() or path.is_symlink():
            continue
        if "/.git/" in str(path):
            continue
        if path.suffix not in SCAN_EXTENSIONS and path.suffix != "":
            continue
        if _is_allowlisted(path):
            continue
        if _contains_retired_term(path):
            rel = path.relative_to(root)
            violations.append(
                f"INV-RETIRED-TERM-SKILLS-ENGINE: {rel} — "
                f"contains retired product name 'skills-engine' (current name: 'forge')"
            )

    return len(violations) == 0, sorted(violations)


# ---------------------------------------------------------------------------
# Signal emission — honest closure-DoD frontmatter
# ---------------------------------------------------------------------------

def emit_signal(signals_dir: str | Path, violations: list[str]) -> Path:
    """Emit a violation signal with honest closure-DoD frontmatter."""
    signals_dir = Path(signals_dir)
    signals_dir.mkdir(parents=True, exist_ok=True)
    today = date.today().isoformat()
    path = signals_dir / f"SIG-RETIRED-TERM-SKILLS-ENGINE-VIOLATION-{today}.md"

    body = f"""---
id: SIG-RETIRED-TERM-SKILLS-ENGINE-VIOLATION-{today}
product: intent
type: invariant-violation
status: open
created: {today}
invariant: INV-RETIRED-TERM-SKILLS-ENGINE
upstream_control_path: "Core/frameworks/intent/tools/retired_term_invariants.py — allowlist is the write-through control; if a legitimate historical reference is missing from it, expand the allowlist, do NOT edit content files"
catch_mechanism: "retired_term_invariants.py INV-RETIRED-TERM-SKILLS-ENGINE + test_retired_term_invariants.py — runs in nightly governance-audit Check 20"
pipeline_survival: "Scans the live filesystem at audit time; no pipeline stage can wipe this check. A violation persists until the new file is corrected or the allowlist is expanded."
---

# INV-RETIRED-TERM-SKILLS-ENGINE Violation — {today}

The retired product name "skills-engine" (current name: "forge", renamed per WS-DDR-027)
has been reintroduced in one or more non-allowlisted files.

## Violations

"""
    for v in violations:
        body += f"- {v}\n"

    body += f"""
## Required action

For each violating file:
1. **Historical reference** (pre-dates the rename): add the file's path pattern to
   `_PATH_SEGMENT_ALLOWLIST` or `_FILENAME_EXACT_ALLOWLIST` in
   `Core/frameworks/intent/tools/retired_term_invariants.py`. Do NOT edit the content.
2. **New live reference**: replace "skills-engine" / "skills_engine" / "SKILLS_ENGINE"
   with "forge" / "Forge" / "FORGE" as appropriate.

Re-run `python3 Core/frameworks/intent/tools/retired_term_invariants.py` to verify.

*Auto-emitted by retired_term_invariants.py {today}.*
"""
    path.write_text(body, encoding="utf-8")
    return path


# ---------------------------------------------------------------------------
# main
# ---------------------------------------------------------------------------

def main(argv=None) -> int:
    ap = argparse.ArgumentParser(
        description="chain_audit invariant: no live skills-engine retired-term references.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )
    ap.add_argument("--root", default=str(DEFAULT_ROOT),
                    help=f"Ecosystem root to scan (default: Core/).")
    ap.add_argument("--emit-signal", action="store_true",
                    help="Emit a violation signal to .intent/signals/ on failure.")
    ap.add_argument("--signals-dir", default=str(DEFAULT_SIGNALS_DIR),
                    help="Where to write violation signals.")
    ap.add_argument("--json", action="store_true", help="Output results as JSON.")
    args = ap.parse_args(argv)

    passed, violations = invariant_no_live_skills_engine_reference(args.root)

    signal_path = None
    if not passed and args.emit_signal:
        sig = emit_signal(args.signals_dir, violations)
        signal_path = str(sig)

    result = {
        "root": str(args.root),
        "passed": passed,
        "invariant": "INV-RETIRED-TERM-SKILLS-ENGINE",
        "violations": violations,
    }
    if signal_path:
        result["signal_emitted"] = signal_path

    if args.json:
        print(json.dumps(result, indent=2))
    else:
        print("=" * 78)
        print("  RETIRED-TERM chain_audit — INV-RETIRED-TERM-SKILLS-ENGINE")
        print(f"  Root: {args.root}")
        print("=" * 78)
        if passed:
            print("\n[PASS] INV-RETIRED-TERM-SKILLS-ENGINE")
            print(
                "\n✓ No live skills-engine references in non-allowlisted files. "
                "Forge is the canonical name."
            )
        else:
            print(f"\n[FAIL] INV-RETIRED-TERM-SKILLS-ENGINE — {len(violations)} violation(s)")
            for v in violations:
                print(f"       {v}")
            print(
                "\n✗ Retired term 'skills-engine' reintroduced. "
                "Expand the allowlist or correct references to 'forge'."
            )
        if signal_path:
            print(f"\nSignal emitted: {signal_path}")

    return 0 if passed else 1


if __name__ == "__main__":
    sys.exit(main())
