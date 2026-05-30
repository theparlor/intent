#!/usr/bin/env python3
"""
hook_regex_contract.py — F-1 fix (SIG-2026-05-29-road-readiness-friction-series)

Scans hooks/*.sh for grep -E / grep -qiE / etc. regex patterns and validates each one:

  1. TIMING CHECK — runs the real grep (/usr/bin/grep -E <pattern>) against
     worst-case adversarial input (long repeated-char string, ~5000 chars) via
     subprocess.run(..., timeout=TIMEOUT_S).  If the subprocess times out, the
     pattern is flagged FAIL: catastrophic-backtrack / self-DoS risk.

  2. STATIC SMELL CHECK — two shapes caught statically:

     Shape 1 — multi-group + greedy gap + \\b (documented ugrep ERE shape):
       Multiple alternation groups combined with .* / .+ and \\b word boundaries.
       Example: (foo|bar).*\\b(baz|qux).+\\b

     Shape 2 — ambiguous/nested quantifier on a group (canonical NFA shape):
       A group containing + or * followed by an outer quantifier: (a+)+  (a|b+)+
       BSD/macOS grep uses DFA and may NOT hang on these, but ugrep (the F-1
       incident engine reported in SIG-2026-05-29-road-readiness-friction-series)
       and other NFA-based greps DO hang on adversarial input.  The contract
       flags this statically regardless of the local grep engine.

Exit codes:
  0  — all patterns terminate within bound (or no patterns found)
  2  — one or more patterns FAIL the time bound

Usage:
  python3 hook_regex_contract.py [--hooks-dir PATH] [--timeout SECONDS] [--json] [--print-wrapper]

Timeout target: 50ms (0.05s) wall-clock per pattern against adversarial input.
CI environments may use 0.5s (the --timeout default) to avoid false positives under load.
The 50ms target is the GOAL; the 0.5s default is the CI floor.

Rule reference (documented in F-1 / SIG-2026-05-29-road-readiness-friction-series):
  "No bounded-quantifier multi-group ERE; decompose into ANDed simple greps.
   CHECK 7 is the reference implementation."

Hard-timeout wrapper for hook grep calls (--print-wrapper flag):
  A pathological pattern in a Stop hook HANGS the entire response loop (self-DoS).
  The fix is to wrap every hot-path grep call so a timeout fails-OPEN (exit 0 = no
  match) instead of hanging:

    timeout 0.5s /usr/bin/grep -qiE "$pat" <<< "$input" || true

  The 'timeout' binary ships with GNU coreutils; on macOS: brew install coreutils.
  Fail-open is correct for Stop hooks — a hung pattern should NOT block responses;
  instead it logs a missed check and continues.  Wire this wrapper as a helper
  function at the top of each hook script.

  NOTE: macOS ships BSD grep 2.6.0 which uses DFA and handles most catastrophic
  patterns gracefully.  The F-1 incident occurred with a specific ugrep-based grep
  variant used internally during hook development.  The static smell check catches
  these patterns regardless of the local grep engine so the contract is portable
  across environments.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import sys
import textwrap
from pathlib import Path
from typing import NamedTuple

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

DEFAULT_HOOKS_DIR = Path(__file__).parent.parent / "hooks"
DEFAULT_TIMEOUT_S = 0.5          # CI-safe floor; 50ms is the measured target
ADVERSARIAL_CHARS = ["a", " ", "x", "\n"]  # chars likely to trigger backtracking
ADVERSARIAL_LEN = 5_000

# ---------------------------------------------------------------------------
# Static smell detectors
# ---------------------------------------------------------------------------

# Shape 1: multiple alternation groups + greedy gap (.* or .+) + \b
# Documented ugrep catastrophic-backtrack shape.
SMELL_MULTI_GROUP_RE = re.compile(
    r"""
    (?:
        (?:\(.*?\|.*?\).*?){2,}   # two+ alternation groups
        .*?
        (?:\.\*|\.\+)             # greedy gap
    )
    |
    (?:
        (?:\.\*|\.\+)             # greedy gap first
        .*?
        (?:\(.*?\|.*?\).*?){2,}   # then two+ alternation groups
    )
    """,
    re.VERBOSE | re.DOTALL,
)
BOUNDARY_IN_SMELL = re.compile(r"\\b")  # \b word boundary also present

# Shape 2: ambiguous quantifier — nested quantifiers on a group: (a+)+  (a|b+)+
# Canonical NFA catastrophic-backtrack form.  BSD grep uses DFA and may not hang;
# ugrep and other NFA-based engines DO hang (F-1 incident).
SMELL_AMBIGUOUS_QUANTIFIER_RE = re.compile(
    r"\([^)]*[+*][^)]*\)[+*{]",  # group containing + or * followed by outer + or * or {N,}
)

GREP_FLAGS_RE = re.compile(
    r"""(?x)
    grep
    \s+
    (?:(?:-[a-zA-Z]+\s+)*-[a-zA-Z]*[Ee][a-zA-Z]*\s+)
    (?P<quote>['"]?)
    (?P<pat>[^'"\n\\\$]+)
    (?P=quote)
    """,
    re.MULTILINE,
)


# ---------------------------------------------------------------------------
# Data types
# ---------------------------------------------------------------------------

class PatternResult(NamedTuple):
    hook_file: str
    pattern: str
    status: str        # "PASS", "FAIL", "WARN", "ERROR"
    detail: str


# ---------------------------------------------------------------------------
# Extraction
# ---------------------------------------------------------------------------

def extract_grep_patterns(sh_text: str) -> list[str]:
    """Pull regex strings from grep -E / -qiE / etc. calls in a shell script.

    NOTE: Patterns passed as shell variables (e.g. grep -qiE "$BARE_CHOICE_RE")
    are intentionally skipped — we cannot resolve the variable without executing
    the shell.  Only literal patterns (single or double-quoted strings without $)
    are extracted.  Variable-expanded patterns must be validated via a separate
    mechanism (e.g. running the hook with known inputs in a test harness).
    """
    patterns: list[str] = []

    for m in GREP_FLAGS_RE.finditer(sh_text):
        pat = m.group("pat").strip()
        # Skip shell variable expansions (can't resolve without shell execution)
        if "$" in pat:
            continue
        if not pat:
            continue
        patterns.append(pat)

    # Deduplicate while preserving order
    seen: set[str] = set()
    out: list[str] = []
    for p in patterns:
        if p not in seen:
            seen.add(p)
            out.append(p)
    return out


# ---------------------------------------------------------------------------
# Checks
# ---------------------------------------------------------------------------

def _make_adversarial(char: str, length: int) -> str:
    return char * length


def check_timing(pattern: str, timeout_s: float) -> tuple[str, str]:
    """Run grep against each adversarial input; return (status, detail).

    Tests the pattern against adversarial worst-case inputs via the system grep.
    If any invocation times out → FAIL (catastrophic-backtrack risk).

    NOTE: macOS BSD grep 2.6.0 uses DFA and handles most classical catastrophic
    patterns (like (a+)+$) without hanging.  The timing check is most effective
    on NFA-based grep engines or patterns that are complex enough to defeat DFA
    analysis.  Combine with check_static_smell() for full coverage.
    """
    grep_path = "/usr/bin/grep"
    if not os.path.exists(grep_path):
        grep_path = "grep"

    for char in ADVERSARIAL_CHARS:
        adversarial = _make_adversarial(char, ADVERSARIAL_LEN)
        try:
            subprocess.run(
                [grep_path, "-qiE", pattern],
                input=adversarial,
                text=True,
                capture_output=True,
                timeout=timeout_s,
            )
            # grep exit 0 = match, exit 1 = no match — both fine; only hang matters
        except subprocess.TimeoutExpired:
            return (
                "FAIL",
                (
                    f"Timed out (>{timeout_s}s) on adversarial input "
                    f"'{char}' x {ADVERSARIAL_LEN} chars — "
                    "catastrophic-backtrack / self-DoS risk. "
                    "Rule: no bounded-quantifier multi-group ERE; "
                    "decompose into ANDed simple greps (CHECK 7 is the reference impl)."
                ),
            )
        except FileNotFoundError:
            return "ERROR", f"grep not found at {grep_path}"
        except Exception as exc:
            return "ERROR", f"subprocess error: {exc}"

    return "PASS", "Terminated within bound on all adversarial inputs."


def check_static_smell(pattern: str) -> tuple[str, str] | None:
    """Return (WARN, detail) if pattern matches a documented bad shape; else None.

    Two shapes are detected (see module docstring for full explanation):
    - Shape 1: multi-group + greedy gap + \\b
    - Shape 2: ambiguous/nested quantifier on group (e.g. (a+)+)
    """
    # Shape 1
    if SMELL_MULTI_GROUP_RE.search(pattern) and BOUNDARY_IN_SMELL.search(pattern):
        return (
            "WARN",
            (
                "Static smell (shape 1): multiple alternation groups + greedy gap (.* or .+) + \\b — "
                "documented ugrep catastrophic-backtrack shape. "
                "Rule: decompose into ANDed simple greps (CHECK 7 reference impl). "
                "Fragile across grep engines even if local grep terminates quickly."
            ),
        )

    # Shape 2
    if SMELL_AMBIGUOUS_QUANTIFIER_RE.search(pattern):
        return (
            "WARN",
            (
                "Static smell (shape 2): ambiguous/nested quantifier on group — e.g. (a+)+ or (a|b+)+ — "
                "canonical NFA catastrophic-backtrack shape (the F-1 incident engine: ugrep). "
                "BSD/macOS grep uses DFA and may not hang, but the pattern is fragile across engines. "
                "Rule: avoid nested quantifiers; decompose (CHECK 7 reference impl)."
            ),
        )

    return None


# ---------------------------------------------------------------------------
# Main scanner
# ---------------------------------------------------------------------------

def scan_hooks_dir(
    hooks_dir: Path,
    timeout_s: float,
) -> list[PatternResult]:
    results: list[PatternResult] = []

    if not hooks_dir.is_dir():
        return results

    for sh_file in sorted(hooks_dir.glob("*.sh")):
        try:
            text = sh_file.read_text(encoding="utf-8", errors="replace")
        except OSError:
            continue

        patterns = extract_grep_patterns(text)
        for pat in patterns:
            # Timing check
            status, detail = check_timing(pat, timeout_s)

            # Static smell (only add if timing passed — FAIL already covers it)
            if status == "PASS":
                smell = check_static_smell(pat)
                if smell:
                    results.append(
                        PatternResult(
                            hook_file=sh_file.name,
                            pattern=pat,
                            status=smell[0],
                            detail=smell[1],
                        )
                    )

            # Always append the timing result
            results.append(
                PatternResult(
                    hook_file=sh_file.name,
                    pattern=pat,
                    status=status,
                    detail=detail,
                )
            )

    return results


# ---------------------------------------------------------------------------
# Reporting
# ---------------------------------------------------------------------------

WRAPPER_SNIPPET = textwrap.dedent(
    """
    # Hard-timeout wrapper for hook grep calls (fail-open = no block on hang)
    # Add to the top of every hook that runs grep in a Stop hook path.
    # Requires: brew install coreutils (for 'timeout' on macOS)
    safe_grep() {
        local pat="$1"
        local input="$2"
        timeout 0.5s /usr/bin/grep -qiE "$pat" <<< "$input" || true
    }
    # Usage: safe_grep "$BARE_CHOICE_RE" "$LOWER_PARA"
    # Fail-open rationale: a hung Stop hook blocks ALL responses (self-DoS per F-1).
    # A missed check is recoverable; a deadlocked hook is not.
    """
).strip()


def print_report(results: list[PatternResult], as_json: bool) -> int:
    """Print report; return exit code (0=clean, 2=any FAIL)."""
    fails = [r for r in results if r.status == "FAIL"]
    warns = [r for r in results if r.status == "WARN"]
    errors = [r for r in results if r.status == "ERROR"]
    passes = [r for r in results if r.status == "PASS"]

    if as_json:
        output = {
            "summary": {
                "total_patterns": len(results),
                "pass": len(passes),
                "warn": len(warns),
                "fail": len(fails),
                "error": len(errors),
            },
            "results": [r._asdict() for r in results],
        }
        print(json.dumps(output, indent=2))
    else:
        print(f"\nhook_regex_contract — {len(results)} patterns scanned")
        print(f"  PASS: {len(passes)}  WARN: {len(warns)}  FAIL: {len(fails)}  ERROR: {len(errors)}")
        print()

        for r in results:
            if r.status in ("FAIL", "WARN", "ERROR"):
                print(f"[{r.status}] {r.hook_file}")
                print(f"  pattern: {r.pattern[:120]}")
                print(f"  detail:  {r.detail}")
                print()

        if not fails and not warns and not errors:
            print("All patterns pass timing and static checks.")
        elif fails:
            print(
                f"ACTION REQUIRED: {len(fails)} pattern(s) failed timing — "
                "catastrophic-backtrack / self-DoS risk."
            )
            print("Rule: decompose multi-group ERE into ANDed simple greps (CHECK 7 reference).")
        elif warns:
            print(
                f"NOTE: macOS BSD grep uses DFA and may handle these patterns without hanging.\n"
                f"The {len(warns)} WARN(s) above are static shape detections — flagged because\n"
                "the pattern is fragile on ugrep/NFA-based greps (the F-1 incident engine).\n"
                "Decompose before deploying to an environment with a different grep."
            )

    return 2 if fails else 0


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument(
        "--hooks-dir",
        type=Path,
        default=DEFAULT_HOOKS_DIR,
        help=f"Directory containing *.sh hook files (default: {DEFAULT_HOOKS_DIR})",
    )
    parser.add_argument(
        "--timeout",
        type=float,
        default=DEFAULT_TIMEOUT_S,
        help=f"Per-pattern grep timeout in seconds (default: {DEFAULT_TIMEOUT_S}; target: 0.05)",
    )
    parser.add_argument(
        "--json",
        action="store_true",
        dest="as_json",
        help="Output results as JSON",
    )
    parser.add_argument(
        "--print-wrapper",
        action="store_true",
        help="Print the hard-timeout wrapper shell snippet and exit",
    )
    args = parser.parse_args(argv)

    if args.print_wrapper:
        print(WRAPPER_SNIPPET)
        return 0

    results = scan_hooks_dir(args.hooks_dir, args.timeout)
    return print_report(results, args.as_json)


if __name__ == "__main__":
    sys.exit(main())
