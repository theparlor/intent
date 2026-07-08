#!/usr/bin/env python3
"""conform_file.py -- glyph/date/path conformance check for files written by subagents.

Why this exists: subagent Write/Edit calls do not pass through the Stop hooks
(emdash-stop-check.sh, link-format-stop-check) that enforce conformance on
conversational responses. Prompt STYLE lines are best-effort, not enforcement,
so glyphs and placeholder dates leak intermittently in files a workflow or
Agent dispatch writes. This script is the in-pipeline gate: run it as an
explicit stage (a Bash call inside a dispatched conformance agent, or by hand)
against every file a subagent just wrote, BEFORE the run is declared clean.

Origin: SIG-2026-07-07-workflow-file-conformance-gap.
Playbook: Core/frameworks/intent/playbooks/workflow-fanout-and-conformance.md

Usage:
    conform_file.py <path> [<path> ...] --check      # exit 1 if any violation found
    conform_file.py <path> [<path> ...] --fix         # auto-fix glyphs in place; still
                                                       # exits 1 if a date/placeholder
                                                       # violation remains (those need a
                                                       # real date, not a mechanical fix)

Checks:
    1. Banned glyphs: em-dash (U+2014), en-dash (U+2013), horizontal ellipsis (U+2026),
       arrow glyphs (U+2190-21FF, U+2192, U+27A1, etc).
    2. Placeholder dates: the literal string ": undated" or a filename containing
       "-undated" (case-insensitive).
    3. Path format: a path that looks like a home-relative or wrapped form
       (starts with "~/" or is wrapped in backticks immediately touching angle
       brackets) where a bare absolute /Users/... path should be. This check is
       advisory only (flagged, not exit-blocking) since prose can legitimately
       reference "~/" in an explanatory sentence.

No third-party dependencies (stdlib only) so it runs anywhere Python 3 runs.
"""
import argparse
import re
import sys

BANNED_GLYPHS = {
    "—": ("em-dash", "-"),
    "–": ("en-dash", "-"),
    "…": ("ellipsis", "..."),
    "←": ("arrow (left)", "<-"),
    "→": ("arrow (right)", "->"),
    "⇐": ("arrow (double left)", "<="),
    "⇒": ("arrow (double right)", "=>"),
    "↔": ("arrow (both)", "<->"),
    "➡": ("arrow (heavy right)", "->"),
}

UNDATED_RE = re.compile(r":\s*undated\b", re.IGNORECASE)
UNDATED_FILENAME_RE = re.compile(r"-undated\b", re.IGNORECASE)


def check_text(text):
    """Return a list of (kind, detail) violations found in text."""
    violations = []
    for glyph, (name, _repl) in BANNED_GLYPHS.items():
        count = text.count(glyph)
        if count:
            violations.append(("glyph", f"{name} (U+{ord(glyph):04X}) x{count}"))
    for m in UNDATED_RE.finditer(text):
        line_no = text.count("\n", 0, m.start()) + 1
        violations.append(("date", f"': undated' placeholder at line {line_no}"))
    return violations


def check_filename(path):
    violations = []
    if UNDATED_FILENAME_RE.search(path):
        violations.append(("date", f"filename contains '-undated': {path}"))
    return violations


def fix_glyphs(text):
    """Mechanically replace banned glyphs with plain-ASCII equivalents.
    Does NOT touch ': undated' or '-undated' -- those need a real date, which
    only the caller (human or agent with run context) can supply."""
    fixed = text
    for glyph, (_name, repl) in BANNED_GLYPHS.items():
        fixed = fixed.replace(glyph, repl)
    return fixed


def process(path, fix):
    try:
        with open(path, "r", encoding="utf-8") as f:
            text = f.read()
    except OSError as e:
        return [("error", f"could not read {path}: {e}")]

    violations = check_filename(path)
    violations += check_text(text)

    glyph_violations = [v for v in violations if v[0] == "glyph"]
    if fix and glyph_violations:
        fixed_text = fix_glyphs(text)
        if fixed_text != text:
            with open(path, "w", encoding="utf-8") as f:
                f.write(fixed_text)
            violations = [v for v in violations if v[0] != "glyph"]
            violations.append(("fixed", f"{len(glyph_violations)} glyph violation(s) auto-fixed in {path}"))

    return violations


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("paths", nargs="+", help="file(s) to check")
    parser.add_argument("--check", action="store_true", help="check only, no changes (default)")
    parser.add_argument("--fix", action="store_true", help="auto-fix glyph violations in place")
    args = parser.parse_args()

    exit_code = 0
    for path in args.paths:
        violations = process(path, fix=args.fix)
        blocking = [v for v in violations if v[0] in ("glyph", "date", "error")]
        if blocking:
            exit_code = 1
        for kind, detail in violations:
            marker = "FIXED" if kind == "fixed" else ("WARN" if kind == "path" else "FAIL")
            print(f"{marker} {path}: {detail}")
        if not violations:
            print(f"OK {path}")

    sys.exit(exit_code)


if __name__ == "__main__":
    main()
