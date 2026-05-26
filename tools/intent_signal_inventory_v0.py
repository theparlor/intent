#!/usr/bin/env python3
"""
intent_signal_inventory.py — V0 archived. See intent_signal_inventory.py for re-grounded V1.

V0 limitation noted at ingestion 2026-05-26:
  This script handles JSON/JSONL streams only. Brien's actual signal corpus is YAML
  frontmatter in markdown files at `**/.intent/signals/SIG-*.md`, `**/.intent/decisions.md`,
  and `**/.context/DECISIONS.md`. Running V0 against Brien's Workspaces would
  underreport the corpus by >95% — the labeled-gold count would round to zero not
  because the corpus is empty but because the format is wrong.

  Field-name assumptions (`boundary_crossed`, `human_decision`) also don't match
  Brien's closure-discipline DoD schema. The actual "labeled gold" definition is:
  status=resolved AND both `upstream_control_path:` and `catch_mechanism:` are
  populated with concrete values (not "pending"/"n/a"/None).

Preserved verbatim from prior-Claude session 2026-05-25 for archeology.
For Brien's actual corpus, use the V1 in the sibling file.

================================================================================

Purpose: turn "I don't know what calibration data I have or where" into a measurement.
This does NOT normalize or extract a training set yet — it INVENTORIES. Discovery
before extraction. It makes no assumptions about exact field names; it reports the
schema it actually finds and counts records that look like autonomy-calibration gold.

Usage:
    python intent_signal_inventory.py /path/to/intent-repo /path/to/productA /path/to/productB ...

Output:
    - human-readable report to stdout
    - machine-readable inventory.json in the current directory
"""

from __future__ import annotations
import json, sys, os
from pathlib import Path
from collections import Counter, defaultdict

# --- What we hunt for -------------------------------------------------------

INTENT_MARKERS = [".intent", "spec", "specs"]            # dirs that mean "intent-wired"
JSONL_GLOBS = ["*.jsonl", "*.ndjson"]                    # event streams
JSON_GLOBS = ["events*.json", "drift*.json", "*signals*.json"]
MD_SIGNAL_HINTS = ("signal", "drift", "ddr", "contract") # md filenames worth counting

# Keys that, if present on a record, indicate autonomy-calibration relevance.
AUTONOMY_KEYS = {
    "boundary_crossed", "review_flagged",
    "autonomy_level", "old_autonomy", "new_autonomy",
    "trust", "old_trust", "new_trust", "trust_factors",
    "blast_radius", "reversibility", "testability", "clarity", "precedent",
}
# Keys that suggest a human verdict exists -> the was-the-grant-right LABEL (gold).
LABEL_KEYS = {
    "human_decision", "override", "overridden", "accepted", "rejected",
    "approved", "approver", "outcome", "verdict", "human_in_loop", "resolution",
}


def iter_records(path: Path):
    """Yield dict records from a .jsonl/.ndjson (one per line) or .json (array/obj)."""
    try:
        if path.suffix.lower() in (".jsonl", ".ndjson"):
            with path.open("r", encoding="utf-8", errors="ignore") as fh:
                for line in fh:
                    line = line.strip()
                    if not line:
                        continue
                    try:
                        obj = json.loads(line)
                        if isinstance(obj, dict):
                            yield obj
                    except json.JSONDecodeError:
                        continue
        else:  # .json
            with path.open("r", encoding="utf-8", errors="ignore") as fh:
                data = json.load(fh)
            if isinstance(data, list):
                for obj in data:
                    if isinstance(obj, dict):
                        yield obj
            elif isinstance(data, dict):
                # common wrapper shapes: {"events": [...]} / {"signals": [...]}
                for v in data.values():
                    if isinstance(v, list):
                        for obj in v:
                            if isinstance(obj, dict):
                                yield obj
                yield data
    except (OSError, json.JSONDecodeError):
        return


def classify_record(rec: dict) -> dict:
    keys = set(rec.keys())
    has_autonomy = bool(keys & AUTONOMY_KEYS)
    has_label = bool(keys & LABEL_KEYS)
    # event type, under whatever key the implementation used
    etype = rec.get("type") or rec.get("event_type") or rec.get("kind") or "?"
    return {"autonomy": has_autonomy, "label": has_label, "etype": etype, "keys": keys}


def inventory_root(root: Path) -> dict:
    report = {
        "root": str(root),
        "exists": root.exists(),
        "intent_wired": False,
        "intent_markers_found": [],
        "files_scanned": 0,
        "total_records": 0,
        "autonomy_records": 0,
        "labeled_records": 0,        # autonomy + human verdict = calibration gold
        "event_types": Counter(),
        "sample_key_sets": [],
        "md_signal_files": 0,
        "silent": False,
    }
    if not root.exists():
        return report

    # intent-wired?
    for m in INTENT_MARKERS:
        if (root / m).is_dir():
            report["intent_wired"] = True
            report["intent_markers_found"].append(m)

    seen_shapes = set()
    for dirpath, dirnames, filenames in os.walk(root):
        # don't descend into noise
        dirnames[:] = [d for d in dirnames if d not in {".git", "node_modules", ".venv", "__pycache__"}]
        d = Path(dirpath)
        for fn in filenames:
            fp = d / fn
            low = fn.lower()
            if any(h in low for h in MD_SIGNAL_HINTS) and low.endswith(".md"):
                report["md_signal_files"] += 1
            is_stream = low.endswith((".jsonl", ".ndjson")) or \
                        (low.endswith(".json") and any(h in low for h in ("event", "drift", "signal")))
            if not is_stream:
                continue
            report["files_scanned"] += 1
            for rec in iter_records(fp):
                report["total_records"] += 1
                c = classify_record(rec)
                report["event_types"][c["etype"]] += 1
                if c["autonomy"]:
                    report["autonomy_records"] += 1
                    if c["label"]:
                        report["labeled_records"] += 1
                    shape = tuple(sorted(c["keys"] & (AUTONOMY_KEYS | LABEL_KEYS)))
                    if shape and shape not in seen_shapes and len(report["sample_key_sets"]) < 5:
                        seen_shapes.add(shape)
                        report["sample_key_sets"].append(list(shape))

    # the silent-recorder finding: wired but emitting nothing
    report["silent"] = report["intent_wired"] and report["autonomy_records"] == 0
    report["event_types"] = dict(report["event_types"].most_common(12))
    return report


def fmt(report: dict) -> str:
    if not report["exists"]:
        return f"  X {report['root']}  - path not found"
    flag = ""
    if report["silent"]:
        flag = "   ! SILENT RECORDER (intent-wired, zero autonomy signal)"
    elif not report["intent_wired"]:
        flag = "   . not intent-wired"
    lines = [
        f"  {report['root']}{flag}",
        f"      files scanned: {report['files_scanned']:>5} | records: {report['total_records']:>7}",
        f"      autonomy records: {report['autonomy_records']:>5} | LABELED (gold): {report['labeled_records']:>5} | md signal files: {report['md_signal_files']}",
    ]
    if report["event_types"]:
        top = ", ".join(f"{k}x{v}" for k, v in list(report["event_types"].items())[:6])
        lines.append(f"      event types: {top}")
    for ks in report["sample_key_sets"]:
        lines.append(f"      calib-shape: {ks}")
    return "\n".join(lines)


def main(argv):
    roots = [Path(a).expanduser().resolve() for a in argv[1:]]
    if not roots:
        print(__doc__)
        return 1
    reports = [inventory_root(r) for r in roots]

    print("\n=== Intent Signal Inventory (V0 - ARCHIVED) ===\n")
    for rep in reports:
        print(fmt(rep)); print()

    tot_labeled = sum(r["labeled_records"] for r in reports)
    tot_auto = sum(r["autonomy_records"] for r in reports)
    silent = [r["root"] for r in reports if r["silent"]]

    print("--- Roll-up ---")
    print(f"  autonomy records total: {tot_auto}")
    print(f"  labeled (calibration-ready) total: {tot_labeled}")
    if silent:
        print(f"  silent recorders to fix: {len(silent)}")
        for s in silent:
            print(f"      - {s}")
    print()
    # the verdict that decides the next move
    if tot_labeled >= 50:
        print("  -> Warm start available: enough labeled records to fit an initial lambda prior.")
    elif tot_auto > 0:
        print("  -> Thin history: usable as weak prior; plan to rely on forward flight-test.")
    else:
        print("  -> No usable history: skip salvage, go straight to instrumented flight-test.")

    Path("inventory.json").write_text(json.dumps(reports, indent=2, default=list))
    print("\n  wrote inventory.json")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
