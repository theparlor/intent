#!/usr/bin/env python3
"""
convention_migration_invariant.py — Control A of SIG-2026-06-27
(contract/convention migration observability — the migration sensor).

WHY THIS EXISTS
  Intent asserts chain-observability: the signal stream should surface incoherence
  as it forms. But when an UPSTREAM product migrates a named contract/convention
  (e.g. Cast's synthesis filename convention, ~2026-04-17), nothing enumerated the
  DOWNSTREAM consumers still bound to the retired form. Three Forge/Voices consumers
  degraded silently for ~2 months and were found by accident. This invariant makes
  "a bound consumer still references a retired convention" a mechanical catch, not
  something the operator has to remember.

  Framework-owned by design: intent is the layer that claims chain-observability, so
  the sensor lives here (tools/), in the exact shape of value_term_invariants.py and
  methodology_coverage_invariant.py. It is pointed at a product's contracts + code via
  --contracts-root / --consumer-root, so it runs against Cast/Forge/Voices from the
  overwatch/nightly suite without depending on those repos being vendored here.

SOURCE OF TRUTH
  A port contract (`*-port.md`) declares, in its YAML frontmatter, two optional blocks:

    bound_consumers:            # files/globs that READ this surface
      - products/forge/skills/panel-critique/**/*.md
      - products/voices/voices-server/tools.py
    forbidden_legacy_patterns:  # retired forms that MUST NOT appear in a bound consumer
      - opus-synthesis-*

  A contract with neither block is ignored (zero-violation-start: declare bound_consumers
  only where it already holds, so day one fires clean).

INVARIANTS
  INV-MIGRATION-NO-LEGACY (hard)
    No bound_consumers file contains any forbidden_legacy_patterns token. This is the
    assertion that would have fired the day the Forge skills were not migrated.

  INV-MIGRATION-CONSUMER-RESOLVES (advisory; --strict promotes to hard)
    Every declared consumer path/glob resolves to at least one existing file. Catches a
    consumer that was renamed/deleted so its binding silently stopped being checked.

USAGE
  python3 convention_migration_invariant.py [--contracts-root PATH] [--consumer-root PATH]
                                            [--strict] [--emit-signal] [--json]
  Exit 0 = pass · 1 = one or more hard violations.

COMPOSES WITH
  - tools/value_term_invariants.py            — same invariant-class shape
  - tools/closure_writeboundary_check.py      — Control B (downstream-fix ⇒ upstream signal)
  - spec/signal-stream.md                     — the chain-observability claim this backs
"""
from __future__ import annotations

import argparse
import fnmatch
import json
import re
import sys
from datetime import date
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_SIGNALS_DIR = REPO_ROOT / ".intent" / "signals"


# ---------------------------------------------------------------------------
# Frontmatter parsing (stdlib only — minimal YAML list-block reader)
# ---------------------------------------------------------------------------

def _frontmatter(text: str) -> str:
    """Return the YAML frontmatter block (between the first two '---'), or ''."""
    if not text.startswith("---"):
        return ""
    end = text.find("\n---", 3)
    return text[3:end] if end != -1 else ""


def parse_list_block(frontmatter: str, key: str) -> list[str]:
    """Collect the `- item` lines under `key:` in a YAML frontmatter block.

    Handles the common flow-list form too (`key: [a, b]`). Returns [] if absent.
    """
    items: list[str] = []
    lines = frontmatter.splitlines()
    for i, line in enumerate(lines):
        m = re.match(rf"^{re.escape(key)}:\s*(.*)$", line)
        if not m:
            continue
        inline = m.group(1).strip()
        if inline.startswith("[") and inline.endswith("]"):
            return [x.strip().strip("'\"") for x in inline[1:-1].split(",") if x.strip()]
        # block form: subsequent more-indented "- item" lines
        for nxt in lines[i + 1:]:
            if re.match(r"^\s*-\s+", nxt):
                items.append(re.sub(r"^\s*-\s+", "", nxt).strip().strip("'\""))
            elif nxt.strip() == "":
                continue
            else:
                break
        break
    return items


def discover_port_contracts(contracts_root: str | Path) -> list[Path]:
    return sorted(Path(contracts_root).rglob("*-port.md"))


def _legacy_regex(pattern: str) -> re.Pattern:
    """A forbidden pattern may contain `*` globs; match it as a token in file text."""
    # translate glob -> regex fragment, but search as a substring (not full-string)
    frag = fnmatch.translate(pattern)
    # fnmatch.translate wraps with (?s:...)\Z ; strip the end-anchor so it matches inline
    frag = frag.replace(r"\Z", "")
    return re.compile(frag)


# ---------------------------------------------------------------------------
# Invariants
# ---------------------------------------------------------------------------

def _bindings(contracts_root: str | Path):
    """Yield (contract_path, bound_consumers, forbidden_patterns) for declared contracts."""
    for c in discover_port_contracts(contracts_root):
        fm = _frontmatter(c.read_text(encoding="utf-8", errors="replace"))
        consumers = parse_list_block(fm, "bound_consumers")
        forbidden = parse_list_block(fm, "forbidden_legacy_patterns")
        if consumers or forbidden:
            yield c, consumers, forbidden


def _resolve(consumer_root: Path, glob: str) -> list[Path]:
    # absolute globs are honored as-is; relative ones resolve under consumer_root
    if glob.startswith("/"):
        base = Path(glob).anchor
        rel = glob[len(base):]
        return sorted(Path(base).glob(rel))
    return sorted(consumer_root.glob(glob))


def invariant_no_legacy(contracts_root, consumer_root) -> tuple[bool, list[str]]:
    consumer_root = Path(consumer_root)
    violations: list[str] = []
    for contract, consumers, forbidden in _bindings(contracts_root):
        if not forbidden:
            continue
        regexes = [(p, _legacy_regex(p)) for p in forbidden]
        for glob in consumers:
            for f in _resolve(consumer_root, glob):
                if not f.is_file():
                    continue
                text = f.read_text(encoding="utf-8", errors="replace")
                for pat, rx in regexes:
                    if rx.search(text):
                        violations.append(
                            f"INV-MIGRATION-NO-LEGACY: {f} contains retired convention "
                            f"'{pat}' — bound consumer of {contract.name} still references "
                            f"the dead form (migrate the consumer or update the contract)."
                        )
    return len(violations) == 0, violations


def invariant_consumer_resolves(contracts_root, consumer_root) -> tuple[bool, list[str]]:
    consumer_root = Path(consumer_root)
    violations: list[str] = []
    for contract, consumers, _forbidden in _bindings(contracts_root):
        for glob in consumers:
            if not _resolve(consumer_root, glob):
                violations.append(
                    f"INV-MIGRATION-CONSUMER-RESOLVES: {contract.name} declares bound_consumer "
                    f"'{glob}' which resolves to no existing file (renamed/deleted? the binding "
                    f"is no longer checked)."
                )
    return len(violations) == 0, violations


# ---------------------------------------------------------------------------
# Signal emission
# ---------------------------------------------------------------------------

def emit_signal(signals_dir: str | Path, violations: list[str]) -> Path:
    signals_dir = Path(signals_dir)
    signals_dir.mkdir(parents=True, exist_ok=True)
    today = date.today().isoformat()
    path = signals_dir / f"SIG-MIGRATION-LEGACY-BINDING-{today}.md"
    body = f"""---
id: SIG-MIGRATION-LEGACY-BINDING-{today}
product: intent
type: invariant-violation
status: open
created: {today}
invariant: INV-MIGRATION-NO-LEGACY
upstream_control_path: "port contract *-port.md bound_consumers + forbidden_legacy_patterns (source of truth) + tools/convention_migration_invariant.py"
catch_mechanism: "tools/convention_migration_invariant.py + tools/test_convention_migration_invariant.py — run in the nightly/overwatch invariant suite"
pipeline_survival: "Port contracts + consumer files are source-of-truth reads at audit time; no render stage rewrites them."
---

# Migration legacy-binding violation — {today}

## Violations

"""
    for v in violations:
        body += f"- {v}\n"
    body += ("\n## Required action\n\nMigrate the flagged consumer(s) off the retired convention, "
             "or update the port contract if the convention legitimately changed. Re-run "
             "`python3 tools/convention_migration_invariant.py` to verify.\n")
    path.write_text(body, encoding="utf-8")
    return path


# ---------------------------------------------------------------------------
# main
# ---------------------------------------------------------------------------

def main(argv=None) -> int:
    ap = argparse.ArgumentParser(
        description="Contract/convention migration sensor (Control A, SIG-2026-06-27).",
        formatter_class=argparse.RawDescriptionHelpFormatter, epilog=__doc__)
    ap.add_argument("--contracts-root", default=str(REPO_ROOT),
                    help="Root to discover *-port.md contracts (default: repo root).")
    ap.add_argument("--consumer-root", default=str(REPO_ROOT),
                    help="Root that bound_consumers globs resolve against (default: repo root).")
    ap.add_argument("--strict", action="store_true",
                    help="Promote INV-MIGRATION-CONSUMER-RESOLVES from advisory to hard.")
    ap.add_argument("--emit-signal", action="store_true",
                    help="Emit a violation signal on hard failure.")
    ap.add_argument("--signals-dir", default=str(DEFAULT_SIGNALS_DIR))
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args(argv)

    no_legacy_ok, no_legacy_v = invariant_no_legacy(args.contracts_root, args.consumer_root)
    resolves_ok, resolves_v = invariant_consumer_resolves(args.contracts_root, args.consumer_root)

    hard_ok = no_legacy_ok and (resolves_ok or not args.strict)
    results = {
        "INV-MIGRATION-NO-LEGACY": {"passed": no_legacy_ok, "violations": no_legacy_v, "level": "hard"},
        "INV-MIGRATION-CONSUMER-RESOLVES": {
            "passed": resolves_ok, "violations": resolves_v,
            "level": "hard" if args.strict else "advisory"},
    }
    if not hard_ok and args.emit_signal:
        results["signal_emitted"] = str(emit_signal(args.signals_dir, no_legacy_v + (resolves_v if args.strict else [])))

    if args.json:
        print(json.dumps({"passed": hard_ok, "results": results}, indent=2))
    else:
        print("=" * 78)
        print("  CONVENTION-MIGRATION SENSOR (Control A · SIG-2026-06-27)")
        print(f"  contracts-root: {args.contracts_root}")
        print("=" * 78)
        for inv, r in results.items():
            if inv == "signal_emitted":
                continue
            tag = "PASS" if r["passed"] else ("FAIL" if r["level"] == "hard" else "WARN")
            print(f"\n[{tag}] {inv} ({r['level']})")
            for v in r["violations"]:
                print(f"       {v}")
        print("\n" + ("✓ No bound consumer references a retired convention."
                      if hard_ok else "✗ Migration binding violation(s) — see above."))

    return 0 if hard_ok else 1


if __name__ == "__main__":
    sys.exit(main())
