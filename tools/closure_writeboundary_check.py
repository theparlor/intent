#!/usr/bin/env python3
"""
closure_writeboundary_check.py — F-4 fix (SIG-2026-05-29-road-readiness-friction-series)

Applies closure-DoD at the WRITE BOUNDARY for signal files, catching the asymmetry
where automated/overnight batch writers emit `status: resolved` signals that admit
the work hasn't actually landed (weasel-marker body text, missing required fields).

Background (F-4):
  The closure-discipline Stop hook gates the INTERACTIVE model's responses against
  premature-resolved claims.  But an automated batch that WROTE signals with
  `status: resolved` + `pipeline_survival: "needs update-mode pass (follow-up)"`
  bypassed the hook entirely — because Stop hooks only run at interactive turn end,
  not at file-write time.  This is an enforcement asymmetry: the interactive agent
  is constrained; the automated writer is not.

This tool is the CATCH-NET.  Per feedback_audit_vs_writethrough, the write-through
fix is teaching automated writers to RUN this tool before emitting (pre-write gate).
The catch-net is a safety net, not the primary prevention.

What counts as a violation:
  `status: resolved` (claiming done) combined with ANY of:
    (a) weasel markers in pipeline_survival / catch_mechanism / upstream_control_path
        or anywhere in the body text: follow-up, follow up, not yet, pending, needs,
        TODO, "to be", incomplete, "will " (future-tense signal that the work is not
        done yet).
    (b) MISSING upstream_control_path OR catch_mechanism fields (closure-DoD requires
        both for resolved status).

What does NOT count as a violation:
  `status: symptom-repaired, upstream-pending` — this is the HONEST not-yet-done
  designation.  It explicitly signals incompleteness; it is correct, not a violation.
  Only `status: resolved` (claiming done-done) combined with evidence it is NOT done
  is the violation pattern.  A signal that says it is pending IS pending; leave it alone.

Exit codes:
  0  — no violations found (or no signals dir)
  2  — one or more premature-resolved violations found

Usage:
  python3 closure_writeboundary_check.py [--dir PATH] [--json]
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import NamedTuple

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

DEFAULT_SIGNALS_DIR = (
    Path(__file__).parent.parent / ".intent" / "signals"
)

# Weasel markers — phrases that indicate the work is not actually done.
# Any of these in a `status: resolved` signal body → PREMATURE-RESOLVED.
#
# Precision rules applied:
#   - "follow-up" / "follow up": strong signal of deferred work.
#   - "not yet": explicit admission of incompleteness.
#   - "pending": match only as a standalone word in context (field value, body prose),
#     NOT in signal IDs/slugs. We match "pending" only when preceded by colon/space
#     and followed by end-of-line or a space (i.e. it IS the value, not part of a slug).
#   - "needs [to|a|update|...]": verb phrase "needs X" in body prose.
#     Match "needs" followed by a non-newline word to avoid matching slugs.
#   - "TODO": all-caps, strong intent marker.
#   - "to be [done|fixed|resolved|completed|verified|wired|established]": explicit deferral.
#   - "incomplete": direct admission.
#   - "will [verb]" in future-tense deferral context: only match "will " before a
#     common deferral verb (fix, be, need, address, follow, complete, require, update,
#     add, wire, establish, verify, land, ship) — NOT capability verbs like "will detect",
#     "will catch", "will fire", "will run", "will prevent" (those describe the catch-net).
WEASEL_PATTERNS: list[re.Pattern] = [
    # "follow-up" or "follow up" — strong deferred-work signal
    re.compile(r"\bfollow[- ]up\b", re.IGNORECASE),
    # "not yet" — explicit incompleteness
    re.compile(r"\bnot yet\b", re.IGNORECASE),
    # "pending" as a field value or standalone word in prose (not inside a slug/ID)
    # Match: "pending" preceded by ": " or "is " or at start of line, or followed by newline/end
    re.compile(r"(?::\s+|^|\s)pending(?:\s*$|\s+—|\s+\()", re.IGNORECASE | re.MULTILINE),
    # "needs [word]" — verb phrase indicating something still required
    # "this needs a follow-on pass" / "needs update-mode pass" / "needs wiring"
    re.compile(r"\bneeds\s+\w", re.IGNORECASE),
    # TODO: all-caps deferred work marker
    re.compile(r"\bTODO\b"),
    # "to be [done/fixed/resolved/completed/verified/wired/established]"
    re.compile(r"\bto be\s+(?:done|fixed|resolved|completed|verified|wired|established|built|shipped)\b", re.IGNORECASE),
    # "incomplete" — direct admission
    re.compile(r"\bincomplete\b", re.IGNORECASE),
    # "will [fix/be/need/address/follow/complete/require/update/add/wire/establish]"
    # ONLY future-tense deferral verbs — NOT capability verbs (detect/catch/fire/run/prevent).
    # 2026-07-03 precision pass: "verify" removed from the deferral list — it is a
    # capability verb in catch-net descriptions ("overwatch sweeps will verify staleness"),
    # which is exactly where it kept false-firing (SIG-EXEC-2026-05-20 residual).
    re.compile(
        r"\bwill\s+(?:fix|be\s+done|need|address|follow|complete|require|update|add|wire|establish|land|ship)\b",
        re.IGNORECASE,
    ),
]

# ---------------------------------------------------------------------------
# Precision exemptions (2026-07-03 pass — Brien-authorized remediation, register
# row 4). Derived from the 8 residual false-positives after the 22-finding
# remediation: every residual fell into one of these classes. Each exemption is
# deliberately narrow; the founding F-4 case (pipeline_survival admitting
# "needs update-mode pass (follow-up)" with no reference, no negation, no
# honesty declaration) still flags under all of them.
# ---------------------------------------------------------------------------

# (a) Cross-reference lines: a weasel token inside a line that names another
#     signal by ID is a REFERENCE to that signal (often to its title, e.g.
#     "SIG-EXEC-...-CONT follow-up #1 — now closed"), not a deferral of this
#     signal's own work.
_SIGNAL_REF_RE = re.compile(r"\b(?:SIG|RETRO|INT|SPEC|DDR|CON)-[A-Za-z0-9]")

# (b) Closed-follow-up evidence on the same line ("— now closed", "(landed
#     2026-06-03: path)"): the language records completion, not deferral.
_CLOSED_EVIDENCE_RE = re.compile(
    r"now closed|\(closed\b|— closed\b|\(landed\b|landed 20\d\d|closed 20\d\d|completed 20\d\d",
    re.IGNORECASE,
)

# (c) Negation immediately governing "needs", including across a line wrap
#     ("no new\n   invariant needs to be authored"). Checked against a two-line
#     window (tail of previous line + current line).
_NEGATED_NEEDS_RE = re.compile(
    r"\bno(?:thing|ne)?\s+(?:\w+[-']?\w*\s+){0,3}needs\b", re.IGNORECASE
)

# (d) Explicit honesty declaration: "Honest status:" inside a DoD field value is
#     the sanctioned convention for qualifying a catch-net's current scope
#     without claiming more than exists (closure-DoD allows an explicit
#     no-catch-net/partial-catch-net justification). Lines carrying the marker
#     are self-declared qualifications, not premature-resolution evidence.
_HONEST_STATUS_RE = re.compile(r"\bHonest status:", re.IGNORECASE)

# (e) Inline code spans quote trigger phrases and regex literals verbatim
#     ("`brien needs to decide`"); stripped before matching. Blockquote lines
#     ("> ...") quote OTHER documents' text; skipped entirely.
_INLINE_CODE_RE = re.compile(r"`[^`]+`")

# Required closure-DoD fields (must appear as YAML-key: or body-key: lines)
REQUIRED_FIELDS = ["upstream_control_path:", "catch_mechanism:"]

# Pattern to detect status: resolved
RESOLVED_RE = re.compile(
    r"^status:\s*resolved\s*$",
    re.IGNORECASE | re.MULTILINE,
)

# Pattern to detect status: symptom-repaired (honest pending — NOT a violation)
SYMPTOM_REPAIRED_RE = re.compile(
    r"^status:\s*symptom-repaired",
    re.IGNORECASE | re.MULTILINE,
)

# ---------------------------------------------------------------------------
# Control B (SIG-2026-06-27): downstream-fix ⇒ upstream-examination signal.
#
# A resolved signal that records a downstream/leaf fix of an upstream-originated
# drift (convention, contract, naming, schema) must point at the upstream
# examination it triggered — else the correction-propagation reflex stays a
# habit, not a mechanism. Enforced here as a write-boundary detector arm.
#
# ZERO-VIOLATION-START: date-scoped to signals dated on/after the effective date.
# Legacy resolved signals (and undated ones) are out of scope, so the live tree
# fires clean on day one (feedback_invariant_zero_violation_start).
# ---------------------------------------------------------------------------
UPSTREAM_EXAM_CUTOFF = "2026-07-02"

# Downstream-fix FRAME markers — specific enough not to fire on any signal that
# merely mentions "downstream". These describe a leaf patch of an upstream drift.
DOWNSTREAM_FIX_PATTERNS: list[re.Pattern] = [
    re.compile(r"\bleaf[- ]fix\b", re.IGNORECASE),
    re.compile(r"\b(?:patched|fixed|updated) the (?:caller|consumer)\b", re.IGNORECASE),
    re.compile(r"\bdownstream (?:fix|consumer|caller|patch|leaf)\b", re.IGNORECASE),
    re.compile(r"\bconsumers?\s+(?:still\s+)?bound\b", re.IGNORECASE),
    re.compile(r"\bbound to the (?:old|dead|retired|previous)\b", re.IGNORECASE),
    re.compile(r"\bretired convention\b", re.IGNORECASE),
]

# The field that satisfies the clause: points at the sibling upstream signal, or
# explicitly waives it with a rationale.
UPSTREAM_EXAM_FIELD_RE = re.compile(
    r"^(?:triggers_upstream_examination|upstream_examination):", re.IGNORECASE | re.MULTILINE
)

_CREATED_RE = re.compile(r"^created:\s*(\d{4}-\d{2}-\d{2})", re.IGNORECASE | re.MULTILINE)
_ANY_DATE_RE = re.compile(r"(\d{4}-\d{2}-\d{2})")


# ---------------------------------------------------------------------------
# Data types
# ---------------------------------------------------------------------------

class Violation(NamedTuple):
    file_path: str
    reason: str
    offending_line: str   # the specific line that triggered the flag (or "")


# ---------------------------------------------------------------------------
# Core logic
# ---------------------------------------------------------------------------

def _is_resolved(text: str) -> bool:
    """Return True only for status: resolved — NOT for symptom-repaired."""
    if RESOLVED_RE.search(text):
        # Double-check it's not the symptom-repaired variant on the same line
        # (they're different patterns but guard anyway)
        if SYMPTOM_REPAIRED_RE.search(text):
            return False
        return True
    return False


def _has_required_fields(text: str) -> tuple[bool, list[str]]:
    """Return (all_present, missing_list)."""
    missing = []
    for field in REQUIRED_FIELDS:
        if field.lower() not in text.lower():
            missing.append(field)
    return (len(missing) == 0), missing


def _find_weasel(text: str) -> list[tuple[re.Pattern, str]]:
    """Return list of (pattern, offending_line) for all weasel hits.

    Applies the 2026-07-03 precision exemptions (see the exemption constants
    above): blockquotes, inline-code spans, signal cross-references,
    closed-follow-up evidence, negated "needs", and "Honest status:" declared
    qualifications are not deferral evidence.
    """
    hits: list[tuple[re.Pattern, str]] = []
    lines = text.splitlines()
    prev_line = ""
    for line in lines:
        stripped = line.strip()
        # Blockquotes quote other documents; never this signal's own admission.
        if stripped.startswith(">"):
            prev_line = line
            continue
        # Explicit honesty declaration is sanctioned qualification language.
        if _HONEST_STATUS_RE.search(line):
            prev_line = line
            continue
        # Match against the line with inline-code spans removed (quoted
        # trigger phrases / regex literals are not prose claims).
        checkable = _INLINE_CODE_RE.sub("", line)
        two_line_window = prev_line[-60:] + " " + checkable
        for pat in WEASEL_PATTERNS:
            if not pat.search(checkable):
                continue
            # Cross-reference or recorded-completion lines are not deferrals.
            if _SIGNAL_REF_RE.search(checkable) or _CLOSED_EVIDENCE_RE.search(checkable):
                continue
            # Negation governing "needs", including across a wrapped line.
            if "needs" in pat.pattern and _NEGATED_NEEDS_RE.search(two_line_window):
                continue
            hits.append((pat, stripped))
        prev_line = line
    return hits


def _signal_date(text: str, path: Path) -> str | None:
    """Best-effort signal date: `created:` field, else a date in the filename."""
    m = _CREATED_RE.search(text)
    if m:
        return m.group(1)
    m = _ANY_DATE_RE.search(path.name)
    return m.group(1) if m else None


def check_upstream_examination(path: Path, text: str, cutoff: str = UPSTREAM_EXAM_CUTOFF) -> list[Violation]:
    """Control B: a post-cutoff resolved downstream-fix signal must declare the
    upstream examination it triggered (or explicitly waive it)."""
    if not _is_resolved(text):
        return []
    d = _signal_date(text, path)
    if d is None or d < cutoff:
        return []  # legacy / undated → out of scope (zero-violation-start)
    if UPSTREAM_EXAM_FIELD_RE.search(text):
        return []  # already declares triggers_upstream_examination / upstream_examination
    for line in text.splitlines():
        for pat in DOWNSTREAM_FIX_PATTERNS:
            if pat.search(line):
                return [Violation(
                    file_path=str(path),
                    reason=(
                        "DOWNSTREAM-FIX-NO-UPSTREAM-SIGNAL: status: resolved records a "
                        "downstream/leaf fix of an upstream-originated drift but declares no "
                        "`triggers_upstream_examination:` (point it at a sibling open signal, or "
                        "set `upstream_examination: not-applicable` with a one-line rationale)."
                    ),
                    offending_line=line.strip()[:200],
                )]
    return []


def check_file(path: Path) -> list[Violation]:
    """Check a single .md file; return violations (empty = clean)."""
    try:
        text = path.read_text(encoding="utf-8", errors="replace")
    except OSError:
        return []

    # Must claim `status: resolved` to be in scope
    if not _is_resolved(text):
        return []

    violations: list[Violation] = []

    # Control B: downstream-fix must trigger an upstream-examination signal
    violations.extend(check_upstream_examination(path, text))

    # Check 1: missing required fields
    all_present, missing = _has_required_fields(text)
    if not all_present:
        violations.append(
            Violation(
                file_path=str(path),
                reason=(
                    f"PREMATURE-RESOLVED: status: resolved but missing required "
                    f"closure-DoD field(s): {', '.join(missing)}"
                ),
                offending_line="",
            )
        )

    # Check 2: weasel markers anywhere in the body
    weasel_hits = _find_weasel(text)
    seen_lines: set[str] = set()
    for pat, line in weasel_hits:
        if line in seen_lines:
            continue
        seen_lines.add(line)
        violations.append(
            Violation(
                file_path=str(path),
                reason=(
                    f"PREMATURE-RESOLVED: status: resolved but body contains weasel "
                    f"marker '{pat.pattern}' — work not yet complete"
                ),
                offending_line=line[:200],
            )
        )

    return violations


def scan_signals_dir(signals_dir: Path) -> list[Violation]:
    """Scan all .md files in signals_dir; return all violations."""
    if not signals_dir.is_dir():
        return []

    all_violations: list[Violation] = []
    for md_file in sorted(signals_dir.glob("*.md")):
        all_violations.extend(check_file(md_file))

    return all_violations


# ---------------------------------------------------------------------------
# Reporting
# ---------------------------------------------------------------------------

def print_report(violations: list[Violation], as_json: bool) -> int:
    if as_json:
        print(
            json.dumps(
                {
                    "summary": {
                        "violations": len(violations),
                        "clean": len(violations) == 0,
                    },
                    "violations": [v._asdict() for v in violations],
                },
                indent=2,
            )
        )
    else:
        print(f"\nclosure_writeboundary_check — {len(violations)} violation(s)\n")
        if violations:
            for v in violations:
                tag = v.reason.split(":", 1)[0]
                print(f"  [{tag}] {Path(v.file_path).name}")
                print(f"    reason: {v.reason}")
                if v.offending_line:
                    print(f"    line:   {v.offending_line}")
                print()
            print(
                "ACTION: These signals claim `status: resolved` but their body text "
                "admits the work is incomplete.\n"
                "Fix: change status to `symptom-repaired, upstream-pending` and add "
                "upstream_control_path + catch_mechanism + pipeline_survival keys,\n"
                "OR genuinely close the upstream gap and re-resolve.\n"
                "Write-through: teach automated writers to run this check BEFORE emitting "
                "(per feedback_audit_vs_writethrough)."
            )
        else:
            print("  All resolved signals pass closure-DoD. No premature-resolved violations.")

    return 2 if violations else 0


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument(
        "--dir",
        type=Path,
        default=DEFAULT_SIGNALS_DIR,
        help=f"Signals directory to scan (default: {DEFAULT_SIGNALS_DIR})",
    )
    parser.add_argument(
        "--json",
        action="store_true",
        dest="as_json",
        help="Output results as JSON",
    )
    args = parser.parse_args(argv)

    violations = scan_signals_dir(args.dir)
    return print_report(violations, args.as_json)


if __name__ == "__main__":
    sys.exit(main())
