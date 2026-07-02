#!/usr/bin/env python3
"""
value_term_audit.py — Value-Term & Outcome-vs-Activity Registry Auditor

WHY THIS EXISTS
  The highest-leverage catch-net for Brien's Intent/Coherence framework.
  It catches the anti-pattern that caused three separate production failures:

  > A score or gate that measures its own ACTIVITY (a proxy) instead of the
  > OUTCOME it serves — with no value term — saturates or accretes overhead
  > and cannot converge.

  Proven instances:
    1. CVRS freshness (cast) — measured corpus-touch (our handling mtime) instead
       of source recency → pinned 100%, meaningless.
    2. CVRS breadth/variety (cast) — measured modern channels[] instead of
       voice body-of-work → historical voices scored 0.
    3. Autonomy Stop-hook (intent) — measured regex-fires (its own firing) instead
       of drift-prevented → 95.8% overhead over 1,463 runs, arms-race can't converge.

  Known-GOOD (have real value terms + measure outcomes):
    - flight-model Thrust T = strategic_value × λ
    - cast Relevance recency as topic-weighted modifier
    - cast values_caution(voice, topic)

  Known-DEFECT for reference:
    - v1 weighted-sum gate: ~0.90 measures downside, 0.00 measures strategic value
      → operationalizes caution, not strategy. (flight-model §1)

TWO MODES

  DEFAULT — audit the registry:
    python3 value_term_audit.py [--registry PATH]
    Checks every declared score/gate in value-term-registry.yaml against four
    invariants. Exit 0 = all pass. Exit 2 = any FAIL (WARN does not fail).

  SCAN — catch-net grep over source files:
    python3 value_term_audit.py --scan PATH [--scan-strict]
    Heuristic grep over .py/.md files for activity-proxy smells in score-computing
    code: mtime, computed_at, _runs, fires, last_touch, datetime.now() as score
    input, counting own invocations. Reports candidates. Exit 0 always (advisory)
    unless --scan-strict (exit 1 on any hit).

INVARIANTS (audit mode)

  INV-1 (value term exists):
    value_term is non-empty AND does not start with "NONE" — UNLESS status in
    {defect, capped} AND remediation is non-empty. A healthy entry with no/NONE
    value_term is a FAIL: "claims healthy but has no value term — operationalizes
    caution, not strategy (flight-model §1)."

  INV-2 (measures outcome):
    status: healthy AND measures: activity → FAIL:
    "measures its own activity (proxy), not the outcome it serves — the anti-pattern."

  INV-3 (defect tracked):
    status in {defect, capped} MUST have non-empty remediation → else FAIL.

  INV-4 (saturation guard present — WARN only):
    kind: score-dimension or composite-score with status: healthy SHOULD declare
    saturation_guard. Missing → WARN (not FAIL). Saturation is how the proxy defect
    hides (feedback_recalibrate_saturated_metrics).

  INV-5 (status closed enum):
    status MUST be one of {healthy, fixed, capped, defect}. Anything else
    (including empty) → FAIL, and no other invariant is evaluated for that entry —
    its obligations are undefined. Rationale: every invariant above is keyed off
    status, so an unrecognized intermediate status ('instrumented-pending-data',
    'parked', …) silently escapes ALL enforcement. Intermediate lifecycle state is
    recorded in an annotation field (e.g. phase:) on top of one of the four
    statuses (SIG-INTENT-STATUS-ENUM-2026-07-02; loom-score-thread precedent).

RELATED
  - value-term-registry.yaml (authoritative write-through manifest)
  - Core/frameworks/intent/tools/drag_dashboard.py (cap_guard: sibling for lexical-CHECK accretion)
  - Core/frameworks/intent/spec/autonomy-flight-model-v1-DRAFT.md §1 (the "no value term" diagnosis)
  - Core/products/cast/.intent/signals/SIG-2026-05-30-cross-session-coherence.md §1-§2

USAGE
  python3 value_term_audit.py [--registry PATH] [--json OUT]
  python3 value_term_audit.py --scan PATH [--scan-strict]
"""
from __future__ import annotations

import argparse
import json
import os
import re
import sys
from pathlib import Path

# ---------------------------------------------------------------------------- paths
DEFAULT_REGISTRY = Path(__file__).parent / "value-term-registry.yaml"

# ---------------------------------------------------------------------------- YAML loading
# Try pyyaml first; fall back to a minimal parser sufficient for this flat schema.
# The fallback handles:  top-level `scores:` list, each entry is a list of key: "value" lines.
# Block scalars are NOT needed — seed data uses double-quoted single-line values.

def _parse_yaml_fallback(text: str) -> list[dict]:
    """
    Minimal YAML parser for the value-term-registry shape:
      scores:
        - id: foo
          key: "value"
          ...
    Supports:
      - Top-level `scores:` list
      - List items starting with `  - id: ...`
      - key: "quoted value"  and  key: unquoted value
      - Continues until next `  - id:` or EOF
    Does NOT support nested objects, block scalars, or anchors.
    """
    entries: list[dict] = []
    in_scores = False
    current: dict | None = None

    # Strip inline comments only outside quoted strings (simplistic — adequate for seed data)
    def _strip_comment(s: str) -> str:
        # Remove trailing  # comment that is not inside quotes
        out = []
        in_q = False
        qch = None
        for i, ch in enumerate(s):
            if in_q:
                out.append(ch)
                if ch == qch:
                    in_q = False
            else:
                if ch in ('"', "'"):
                    in_q = True
                    qch = ch
                    out.append(ch)
                elif ch == '#':
                    break
                else:
                    out.append(ch)
        return "".join(out).rstrip()

    def _unquote(v: str) -> str:
        v = v.strip()
        if (v.startswith('"') and v.endswith('"')) or (v.startswith("'") and v.endswith("'")):
            return v[1:-1]
        return v

    for raw_line in text.splitlines():
        line = _strip_comment(raw_line)
        stripped = line.strip()

        if not in_scores:
            if stripped == "scores:":
                in_scores = True
            continue

        # New entry starts
        if re.match(r"^\s{2}-\s+id:", line):
            if current is not None:
                entries.append(current)
            # parse the id from this line
            m = re.match(r"^\s{2}-\s+id:\s*(.*)", line)
            val = _unquote(m.group(1).strip()) if m else ""
            current = {"id": val}
            continue

        if current is None:
            continue

        # Key-value pair inside an entry
        m = re.match(r"^\s{4}(\w[\w_-]*):\s*(.*)", line)
        if m:
            key = m.group(1)
            val = _unquote(m.group(2).strip())
            current[key] = val

    if current is not None:
        entries.append(current)

    return entries


def _load_registry(path: str | Path) -> list[dict]:
    """Load the registry YAML. Uses pyyaml if available, else fallback parser."""
    text = Path(path).read_text(encoding="utf-8", errors="replace")
    try:
        import yaml  # type: ignore
        data = yaml.safe_load(text)
        return data.get("scores", []) if isinstance(data, dict) else []
    except ImportError:
        return _parse_yaml_fallback(text)


# ---------------------------------------------------------------------------- cross-product discovery
# Per-product write-through: each product owns its value-term-registry.yaml beside
# its score-computing code. The auditor discovers them rather than reading one monolith
# (the monolith IS the write-through defect — a cast score declared in the intent repo
# drifts because the score-owner never edits it). DEFAULT_ECOSYSTEM_ROOT = Core/.

ECOSYSTEM_REGISTRY_NAME = "value-term-registry.yaml"
DEFAULT_ECOSYSTEM_ROOT = Path(__file__).resolve().parents[3]  # tools→intent→frameworks→Core
# Never audit vendored / worktree / cache / build-output copies — they are not the
# source of truth. 'dist'/'build'/'out' catch vendored bundles (e.g. forge
# outputs/dist/voices-panel vendoring the voices registry): a write-through registry
# lives beside its score-owning source, never in build output.
_EXCLUDE_DIR_PARTS = {".venv", "venv", ".worktrees", "node_modules", "__pycache__", ".git",
                      "dist", "build", "out"}


def discover_registries(root: str | Path) -> list[Path]:
    """Find every value-term-registry.yaml under root, skipping vendored/worktree/cache dirs.

    Returns a sorted list of Paths. This is the cross-product seam: each product's
    write-through registry is found by name, wherever it lives.
    """
    root = Path(root)
    found: list[Path] = []
    for p in sorted(root.rglob(ECOSYSTEM_REGISTRY_NAME)):
        if any(part in _EXCLUDE_DIR_PARTS for part in p.parts):
            continue
        found.append(p)
    return found


# ---------------------------------------------------------------------------- invariant checks

ACTIVITY_PROXY_SMELLS = [
    r"\bmtime\b",
    r"\bst_mtime\b",
    r"\bcomputed_at\b",
    r"\b_runs\b",
    r"\.fires\b",
    r"\blast_touch\b",
    r"\btouch\b(?!.*date)",   # 'touch' but not 'touch_date' (source publication idiom)
    r"datetime\.now\(\)",
    r"time\.time\(\)",
    r"\binvocation_count\b",
    r"\bcheck_count\b",
    r"\.stat\(\)\.st_mtime",
    r"os\.stat\(",
]

# Compiled once
_SMELL_RE = re.compile("|".join(ACTIVITY_PROXY_SMELLS))

STATUS_KNOWN_DEFECT = {"defect", "capped"}
# CLOSED status enum (INV-5). Every invariant below is keyed off status, so an
# unrecognized status silently escapes ALL enforcement (the loom
# 'instrumented-pending-data' near-miss, SIG-INTENT-STATUS-ENUM-2026-07-02).
# Obligations by status:
#   healthy       → INV-1 (value term), INV-2 (measures outcome), INV-4 (saturation guard, WARN)
#   fixed         → INV-1 (value term)
#   defect|capped → INV-3 (remediation required); INV-1 exemption applies
# Intermediate lifecycle state goes in an ANNOTATION field (e.g. phase:) on top of
# one of these four — never a new status value.
KNOWN_STATUSES = {"healthy", "fixed", "capped", "defect"}
SCORE_KINDS = {"score-dimension", "composite-score"}


def _vt_is_missing(vt: str) -> bool:
    """True if value_term is empty or starts with 'NONE'."""
    if not vt or not vt.strip():
        return True
    return vt.strip().upper().startswith("NONE")


def _audit_entry(entry: dict) -> tuple[list[str], list[str]]:
    """
    Return (fails, warns) for one registry entry.
    fails → exit 2; warns → printed only.
    """
    eid = entry.get("id", "<unknown>")
    status = (entry.get("status") or "").strip().lower()
    measures = (entry.get("measures") or "").strip().lower()
    kind = (entry.get("kind") or "").strip().lower()
    vt = entry.get("value_term") or ""
    remediation = (entry.get("remediation") or "").strip()
    saturation_guard = (entry.get("saturation_guard") or "").strip()
    outcome_signal = (entry.get("outcome_signal") or "").strip()

    fails: list[str] = []
    warns: list[str] = []

    # INV-5: status is a CLOSED enum — checked first. Every other invariant is
    # keyed off status, so an unknown status means the entry's obligations are
    # undefined and it would otherwise drop out of enforcement entirely.
    if status not in KNOWN_STATUSES:
        fails.append(
            f"[INV-5] {eid}: unknown status {status!r} — status is a closed enum "
            f"{sorted(KNOWN_STATUSES)}. An unrecognized status escapes ALL "
            f"status-keyed enforcement (INV-1..4). For intermediate lifecycle "
            f"state, keep one of the four statuses and add an annotation field "
            f"(e.g. phase:) — see loom-score-thread."
        )
        return fails, warns

    # INV-1: value term exists
    if _vt_is_missing(vt):
        if status not in STATUS_KNOWN_DEFECT:
            fails.append(
                f"[INV-1] {eid}: claims {status!r} but has no value term — "
                f"operationalizes caution, not strategy (flight-model §1)."
            )
        elif not remediation:
            # Defect/capped with no remediation → INV-3 will catch it; INV-1 adds context
            fails.append(
                f"[INV-1+3] {eid}: status={status!r}, value_term=NONE/empty, and no remediation — "
                f"undocumented defect. Add remediation path or fix the value term."
            )
        # else: defect/capped with remediation → allowed (known defect with tracked fix)

    # INV-2: healthy entries must measure outcome, not activity —
    # UNLESS the entry honestly declares itself observability-only with an
    # explicit outcome-close. An activity dimension labeled `measures: activity`
    # whose `outcome_signal` begins with "n/a by design" has done exactly the
    # honest disclosure the discipline prescribes: it states it is NOT outcome-
    # bearing and points to the sibling dimension that closes the outcome. That
    # is the GOOD pattern, not the anti-pattern. The real anti-pattern is an
    # activity score *treated as* the outcome — silent about the gap, or claiming
    # an outcome_signal while measuring activity. Without this exemption the
    # invariant penalizes the very disclosure it exists to encourage and cannot
    # hold zero-violation-start for any honest observability term.
    # See gauge value-term-registry.yaml (gauge-audit / gauge-ensemble-pass);
    # feedback_audit_vs_writethrough (when a fix is correct but the audit keeps
    # firing, suspect the comparator).
    if status == "healthy" and measures == "activity":
        if not outcome_signal.lower().startswith("n/a by design"):
            fails.append(
                f"[INV-2] {eid}: status=healthy but measures='activity' — "
                f"measures its own activity (proxy), not the outcome it serves — the anti-pattern. "
                f"An honest observability-only term must declare "
                f"outcome_signal: 'n/a by design — <outcome-close>'."
            )

    # INV-3: defect/capped must have remediation
    if status in STATUS_KNOWN_DEFECT and not remediation:
        # Only append if INV-1+3 not already raised (avoid duplicate)
        already = any("[INV-1+3]" in f and eid in f for f in fails)
        if not already:
            fails.append(
                f"[INV-3] {eid}: status={status!r} but remediation is empty — "
                f"undocumented defect. Every known defect must have a tracked remediation path."
            )

    # INV-4: saturation guard (WARN for score-dimensions/composite-scores that are healthy)
    if status == "healthy" and kind in SCORE_KINDS and not saturation_guard:
        warns.append(
            f"[INV-4 WARN] {eid}: healthy {kind} has no saturation_guard — "
            f"saturation is how the proxy defect hides (feedback_recalibrate_saturated_metrics). "
            f"Declare a saturation detector."
        )

    return fails, warns


def _audit_registry(registry_path: str | Path) -> tuple[list[str], list[str], int]:
    """
    Audit all entries. Returns (all_fails, all_warns, entry_count).
    """
    entries = _load_registry(registry_path)
    all_fails: list[str] = []
    all_warns: list[str] = []
    for entry in entries:
        f, w = _audit_entry(entry)
        all_fails.extend(f)
        all_warns.extend(w)
    return all_fails, all_warns, len(entries)


# ---------------------------------------------------------------------------- scan mode

def _scan_path(target: Path, strict: bool) -> tuple[list[dict], int]:
    """
    Heuristic grep over .py and .md files under target (or target itself).
    Returns (candidates, exit_code).
    candidates: list of {file, line_no, line, smell}
    """
    candidates: list[dict] = []

    def _check_file(fp: Path) -> None:
        try:
            lines = fp.read_text(encoding="utf-8", errors="replace").splitlines()
        except Exception:
            return
        for i, line in enumerate(lines, 1):
            m = _SMELL_RE.search(line)
            if m:
                candidates.append({
                    "file": str(fp),
                    "line_no": i,
                    "line": line.rstrip(),
                    "smell": m.group(0),
                })

    if target.is_file():
        _check_file(target)
    elif target.is_dir():
        for ext in ("*.py", "*.md"):
            for fp in sorted(target.rglob(ext)):
                _check_file(fp)

    exit_code = 1 if (strict and candidates) else 0
    return candidates, exit_code


# ---------------------------------------------------------------------------- rendering (mirrors drag_dashboard banner style)

_SEP = "=" * 78
_THIN = "─" * 40


def _render_audit(fails: list[str], warns: list[str], entry_count: int,
                  registry_path: str) -> str:
    lines = [
        _SEP,
        "  VALUE-TERM AUDIT — score/gate outcome-vs-activity registry",
        "  Anti-pattern: a score measuring its own activity, not the outcome it serves",
        "  (flight-model §1 · SIG-2026-05-30-cross-session-coherence §1)",
        _SEP,
        "",
        f"  Registry : {registry_path}",
        f"  Entries  : {entry_count}",
        "",
    ]

    if not fails and not warns:
        lines += [
            "  ✓ ALL INVARIANTS PASS — no activity-proxy defects in registry.",
            "",
            "  Every declared score/gate has:",
            "    INV-1 ✓  value_term naming the outcome (or tracked defect+remediation)",
            "    INV-2 ✓  measures: outcome for all healthy entries",
            "    INV-3 ✓  remediation path for all defect/capped entries",
            "    INV-4 ✓  saturation_guard declared (or not applicable)",
            "    INV-5 ✓  status within the closed enum {healthy, fixed, capped, defect}",
        ]
    else:
        if fails:
            lines += [f"── FAILs ({len(fails)}) " + _THIN]
            for f in fails:
                lines.append(f"  ✗ {f}")
            lines.append("")

        if warns:
            lines += [f"── WARNs ({len(warns)}) " + _THIN]
            for w in warns:
                lines.append(f"  ⚠ {w}")
            lines.append("")

    lines += [
        "",
        _SEP,
        "  Run with --scan PATH to grep source files for unregistered activity-proxy smells.",
        "  Every new score/gate should be registered here before going to production.",
        _SEP,
    ]
    return "\n".join(lines)


def _render_scan(candidates: list[dict], target: str, strict: bool) -> str:
    lines = [
        _SEP,
        "  VALUE-TERM SCAN — activity-proxy smell detector (advisory catch-net)",
        "  Finds score-computing code NOT yet in the registry. Register or fix.",
        _SEP,
        "",
        f"  Target : {target}",
        f"  Mode   : {'STRICT (exit 1 on hit)' if strict else 'advisory (exit 0)'}",
        "",
    ]
    if not candidates:
        lines.append("  ✓ No activity-proxy smells detected.")
    else:
        lines.append(f"  {len(candidates)} candidate(s) found — review and register or fix:\n")
        for c in candidates:
            lines.append(f"  POSSIBLE activity-proxy — register it or fix it.")
            lines.append(f"    file    : {c['file']}")
            lines.append(f"    line {c['line_no']:>4}: {c['line']}")
            lines.append(f"    smell   : {c['smell']!r}")
            lines.append("")
    lines += [
        _SEP,
        "  This is the catch-net-for-the-catch-net. It complements (does not replace)",
        "  the registry. Register confirmed scores in value-term-registry.yaml.",
        _SEP,
    ]
    return "\n".join(lines)


def _render_all(sections: list[tuple], root: str, n: int) -> str:
    """Render the cross-product ecosystem audit (one block per discovered registry)."""
    total_fails = sum(len(f) for _, f, _, _ in sections)
    total_warns = sum(len(w) for _, _, w, _ in sections)
    lines = [
        _SEP,
        "  VALUE-TERM ECOSYSTEM AUDIT — every per-product write-through registry",
        "  Anti-pattern: a score measuring its own activity, not the outcome it serves",
        "  (flight-model §1 · SIG-2026-05-30-cross-session-coherence §1)",
        _SEP,
        "",
        f"  Root       : {root}",
        f"  Registries : {n}",
        "",
    ]
    if not sections:
        lines += ["  (no value-term-registry.yaml found under root)", ""]
    for path, fails, warns, count in sections:
        status = "✗ FAIL" if fails else ("⚠ WARN" if warns else "✓ PASS")
        lines.append(f"  [{status}] {path}  ({count} entries)")
        for f in fails:
            lines.append(f"        ✗ {f}")
        for w in warns:
            lines.append(f"        ⚠ {w}")
    lines += [
        "",
        _SEP,
        f"  ECOSYSTEM: {total_fails} FAIL · {total_warns} WARN across {n} registries.",
        ("  ✓ Every declared score/gate measures an outcome (or is a tracked defect)."
         if not total_fails else
         "  ✗ Untracked activity-proxy defect(s) found — register or fix above."),
        _SEP,
    ]
    return "\n".join(lines)


# ---------------------------------------------------------------------------- main

def main(argv=None):
    ap = argparse.ArgumentParser(
        description=(
            "Audit the value-term registry (default) or scan source files for "
            "activity-proxy smells (--scan)."
        ),
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )
    ap.add_argument(
        "--registry", default=str(DEFAULT_REGISTRY),
        help="Path to value-term-registry.yaml (default: sibling of this script)",
    )
    ap.add_argument(
        "--json", default=None, metavar="OUT",
        help="Write machine-readable result to OUT (JSON). Default: no file written.",
    )
    ap.add_argument(
        "--scan", default=None, metavar="PATH",
        help="Scan a .py/.md file or directory for activity-proxy smells (advisory). "
             "Exit 0 always unless --scan-strict.",
    )
    ap.add_argument(
        "--scan-strict", action="store_true",
        help="With --scan: exit 1 if any smell is found.",
    )
    ap.add_argument(
        "--all", nargs="?", const="", default=None, metavar="ROOT",
        help="Cross-product mode: discover + audit every per-product "
             "value-term-registry.yaml under ROOT (default: Core/). "
             "Exit 2 if any discovered registry has a FAIL.",
    )
    args = ap.parse_args(argv)

    # ── CROSS-PRODUCT --all MODE ─────────────────────────────────────────────────
    if args.all is not None:
        root = Path(args.all) if args.all else DEFAULT_ECOSYSTEM_ROOT
        registries = discover_registries(root)
        sections: list[tuple] = []
        all_fails: list[str] = []
        all_warns: list[str] = []
        for reg in registries:
            fails, warns, count = _audit_registry(reg)
            sections.append((str(reg), fails, warns, count))
            all_fails.extend(fails)
            all_warns.extend(warns)
        print(_render_all(sections, str(root), len(registries)))
        if args.json:
            Path(args.json).write_text(
                json.dumps({
                    "root": str(root),
                    "registry_count": len(registries),
                    "registries": [
                        {"path": p, "fails": f, "warns": w, "entry_count": c}
                        for p, f, w, c in sections
                    ],
                    "fails": all_fails,
                    "warns": all_warns,
                    "passed": len(all_fails) == 0,
                }, indent=2),
                encoding="utf-8",
            )
        return 2 if all_fails else 0

    # ── SCAN MODE ──────────────────────────────────────────────────────────────
    if args.scan is not None:
        target = Path(args.scan)
        if not target.exists():
            print(f"ERROR: scan target not found: {target}", file=sys.stderr)
            return 1
        candidates, exit_code = _scan_path(target, args.scan_strict)
        report = _render_scan(candidates, str(target), args.scan_strict)
        print(report)
        if args.json:
            Path(args.json).write_text(
                json.dumps({"scan_target": str(target), "candidates": candidates}, indent=2),
                encoding="utf-8",
            )
        return exit_code

    # ── AUDIT MODE ─────────────────────────────────────────────────────────────
    registry_path = args.registry
    if not Path(registry_path).exists():
        print(f"ERROR: registry not found: {registry_path}", file=sys.stderr)
        return 2

    fails, warns, entry_count = _audit_registry(registry_path)
    report = _render_audit(fails, warns, entry_count, registry_path)
    print(report)

    if args.json:
        Path(args.json).write_text(
            json.dumps({
                "registry": registry_path,
                "entry_count": entry_count,
                "fails": fails,
                "warns": warns,
                "passed": len(fails) == 0,
            }, indent=2),
            encoding="utf-8",
        )

    return 2 if fails else 0


if __name__ == "__main__":
    sys.exit(main())
