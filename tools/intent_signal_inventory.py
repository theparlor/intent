#!/usr/bin/env python3
"""
intent_signal_inventory.py — V1 re-grounded to Brien's actual schema.

What changed vs V0 (intent_signal_inventory_v0.py):
  - Parses YAML frontmatter from .md files (V0 only handled JSON/JSONL)
  - Uses Brien's actual signal schema: status, upstream_control_path, catch_mechanism,
    type, severity, pipeline_survival, related, discovered_by
  - "Labeled gold" definition matches closure-discipline DoD:
      status: resolved
      AND upstream_control_path is concrete (not "pending"/"n/a"/None/empty)
      AND catch_mechanism is concrete
  - Walks `**/.intent/signals/SIG-*.md`, `**/.intent/decisions.md`,
    `**/.intent/decisions/*.md`, and `.context/DECISIONS.md`
  - Reports flight-model-input backfill gap (W/T/L/D fields per signal)
  - Rolls up by product (Core/products/*, Core/frameworks/*, ROOT)
  - Identifies silent recorders: products with .intent/ but no signals at all

Usage:
    python intent_signal_inventory.py [WORKSPACES_ROOT]
    (default: current directory)

Output:
    - stdout: human-readable report
    - inventory.json in CWD: machine-readable
"""

from __future__ import annotations
import os, re, json, sys
from pathlib import Path
from datetime import datetime
from collections import Counter, defaultdict

# Optional YAML — fall back to manual parsing if unavailable
try:
    import yaml
    HAVE_YAML = True
except ImportError:
    HAVE_YAML = False

# Shared skip rules — mirrors theparlor/library-index-system@8a79e07 pattern.
# Importing from sibling module keeps Core/external skip in one place within
# this product directory.
from skip_rules import SKIP_DIRS as EXCLUDE_DIRS, should_skip_subdir

# === Brien's actual signal schema (per signal-stream.md DoD + observed signals) ===

CLOSURE_REQUIRED_FIELDS = ("upstream_control_path", "catch_mechanism")
PENDING_MARKERS = {"pending", "n/a", "none", "tbd", "", "null", "open"}

# Flight-model input fields (signal frontmatter should carry these going forward)
FLIGHT_MODEL_FIELDS = {
    "blast_radius", "strategic_value", "containment_posture",
    "detection_speed", "irreversibility", "exposure",
    "autonomy_level", "lambda_used", "w_gravity", "t_thrust", "l_lift", "d_drag",
}

# Note: `worktrees` is in EXCLUDE_DIRS (imported from skip_rules) — this excludes
# .claude/worktrees/ which contain Workspaces clones (CCD session worktrees) that
# would 10x-double-count the corpus if walked.

STALE_DAYS = 90

# === Frontmatter parsing ===

FRONTMATTER_RE = re.compile(r"\A---\s*\n(.*?)\n---\s*\n", re.DOTALL)


def parse_frontmatter(text: str) -> dict:
    """Extract YAML frontmatter dict from markdown text. Returns {} if none."""
    m = FRONTMATTER_RE.match(text)
    if not m:
        return {}
    fm_text = m.group(1)
    if HAVE_YAML:
        try:
            data = yaml.safe_load(fm_text)
            return data if isinstance(data, dict) else {}
        except yaml.YAMLError:
            return _parse_yaml_fallback(fm_text)
    return _parse_yaml_fallback(fm_text)


def _parse_yaml_fallback(fm_text: str) -> dict:
    """Minimal YAML parser for the `key: value` and `key:\\n  - item` patterns Brien uses."""
    result = {}
    cur_list = None
    for line in fm_text.split("\n"):
        stripped = line.strip()
        if not stripped or stripped.startswith("#"):
            continue
        # List item under previous key
        if line.startswith(("  -", "- ")) and cur_list is not None:
            val = stripped.lstrip("- ").strip().strip('"').strip("'")
            cur_list.append(val)
            continue
        # key: value or key: (list follows)
        if ":" in line and not line.startswith(" "):
            k, _, v = line.partition(":")
            k = k.strip()
            v = v.strip()
            if not v:
                cur_list = []
                result[k] = cur_list
            else:
                v = v.strip().strip('"').strip("'")
                result[k] = v
                cur_list = None
    return result


# === Signal classification ===


def _is_concrete(value) -> bool:
    """A field is concrete iff it's a non-empty value not flagged as pending/n.a./tbd."""
    if value is None:
        return False
    s = str(value).strip().lower()
    if not s:
        return False
    head = s[:30]
    for marker in PENDING_MARKERS:
        if marker and marker in head:
            return False
    return True


def is_closure_compliant(fm: dict) -> bool:
    """Closure-discipline DoD: status=resolved AND both upstream/catch concrete."""
    status = str(fm.get("status", "")).lower()
    if "resolved" not in status:
        return False
    if "pending" in status or "open" in status or "symptom-repaired" in status:
        return False
    for field in CLOSURE_REQUIRED_FIELDS:
        if not _is_concrete(fm.get(field)):
            return False
    return True


def has_flight_model_inputs(fm: dict) -> bool:
    """True iff signal carries any flight-model input field (W/T/L/D facets)."""
    return bool(set(fm.keys()) & FLIGHT_MODEL_FIELDS)


def signal_age_days(fm: dict, path: Path) -> int | None:
    """Best-effort signal age. Try date field; fall back to filename SIG-YYYY-MM-DD-."""
    date_str = fm.get("date") or fm.get("created") or fm.get("updated")
    if not date_str:
        m = re.search(r"(\d{4}-\d{2}-\d{2})", path.name)
        if m:
            date_str = m.group(1)
    if not date_str:
        return None
    try:
        d = datetime.fromisoformat(str(date_str)[:10])
        return (datetime.now() - d).days
    except (ValueError, TypeError):
        return None


def classify_product(sig_path: Path, root: Path) -> str:
    """Bucket a signal by which product/scope it belongs to."""
    try:
        rel = sig_path.relative_to(root)
    except ValueError:
        return "EXTERNAL"
    parts = rel.parts
    if not parts:
        return "ROOT"
    if parts[0] == ".intent":
        return "ROOT (Workspaces-wide)"
    if parts[0] == "Core" and len(parts) >= 3 and parts[1] in {"products", "frameworks"}:
        return f"Core/{parts[1]}/{parts[2]}"
    if parts[0] == "Work":
        return f"Work/{parts[1] if len(parts) > 1 else '?'}"
    return parts[0]


# === Crawler ===


def find_signals(root: Path):
    """Walk root yielding signal-file Paths."""
    seen = set()
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = sorted([
            d for d in dirnames
            if not should_skip_subdir(d, dirpath, root)
        ])
        d = Path(dirpath)
        name = d.name
        parent_name = d.parent.name

        if name == "signals" and parent_name == ".intent":
            for fn in filenames:
                if fn.startswith("SIG-") and fn.endswith(".md"):
                    p = d / fn
                    if p not in seen:
                        seen.add(p)
                        yield p

        if name == ".intent":
            for fn in filenames:
                if fn == "decisions.md":
                    p = d / fn
                    if p not in seen:
                        seen.add(p)
                        yield p

        if name == "decisions" and parent_name == ".intent":
            for fn in filenames:
                if fn.endswith(".md"):
                    p = d / fn
                    if p not in seen:
                        seen.add(p)
                        yield p

        if name == ".context":
            for fn in filenames:
                if fn == "DECISIONS.md":
                    p = d / fn
                    if p not in seen:
                        seen.add(p)
                        yield p


def find_intent_wired_products(root: Path):
    """Yield product-rooted dirs that contain a .intent/ subdir."""
    seen = set()
    for dirpath, dirnames, _ in os.walk(root):
        dirnames[:] = sorted([
            d for d in dirnames
            if not should_skip_subdir(d, dirpath, root)
        ])
        d = Path(dirpath)
        if ".intent" in dirnames:
            try:
                rel = d.relative_to(root)
            except ValueError:
                continue
            parts = rel.parts
            if not parts:
                product = "ROOT (Workspaces-wide)"
            elif parts[0] == "Core" and len(parts) >= 3 and parts[1] in {"products", "frameworks"}:
                product = f"Core/{parts[1]}/{parts[2]}"
            elif parts[0] == "Work":
                continue  # engagement-scoped — out of corpus
            else:
                product = str(rel)
            if product not in seen:
                seen.add(product)
                yield product


def inventory(root: Path) -> dict:
    rep = {
        "root": str(root),
        "have_yaml_lib": HAVE_YAML,
        "total_signals": 0,
        "by_status": Counter(),
        "by_type": Counter(),
        "labeled_gold": 0,  # closure-discipline-compliant resolved
        "symptom_repaired": 0,
        "open_signals": 0,
        "have_flight_inputs": 0,
        "need_backfill": 0,
        "stale_signals": 0,
        "by_product": defaultdict(lambda: {
            "signals": 0, "compliant": 0, "stale": 0,
            "open": 0, "symptom_repaired": 0,
        }),
        "silent_recorders": [],
        "sample_compliant": [],
        "sample_symptom_repaired": [],
        "sample_open": [],
    }

    rep["by_kind"] = Counter()

    for sig_path in find_signals(root):
        try:
            text = sig_path.read_text(encoding="utf-8", errors="ignore")
        except OSError:
            continue
        fm = parse_frontmatter(text)
        if not fm:
            continue

        # Classify kind so signals/decisions/ws-decisions are countable separately
        name = sig_path.name
        parent = sig_path.parent.name
        if name.startswith("SIG-"):
            kind = "signal"
        elif name == "decisions.md" or parent == "decisions":
            kind = "decision"
        elif name == "DECISIONS.md":
            kind = "ws-decision"
        else:
            kind = "other"
        rep["by_kind"][kind] += 1

        rep["total_signals"] += 1

        status_raw = fm.get("status", "unknown")
        status = str(status_raw).lower().strip()
        rep["by_status"][status[:50]] += 1

        sig_type = str(fm.get("type", "unknown"))
        rep["by_type"][sig_type[:50]] += 1

        product = classify_product(sig_path, root)
        rep["by_product"][product]["signals"] += 1

        sample = {
            "id": fm.get("id", sig_path.name),
            "product": product,
            "type": sig_type,
            "status": status,
            "path": str(sig_path.relative_to(root)) if sig_path.is_relative_to(root) else str(sig_path),
        }

        if is_closure_compliant(fm):
            rep["labeled_gold"] += 1
            rep["by_product"][product]["compliant"] += 1
            if len(rep["sample_compliant"]) < 5:
                rep["sample_compliant"].append(sample)
        elif "symptom-repaired" in status:
            rep["symptom_repaired"] += 1
            rep["by_product"][product]["symptom_repaired"] += 1
            if len(rep["sample_symptom_repaired"]) < 5:
                rep["sample_symptom_repaired"].append(sample)
        elif "open" in status or "pending" in status or status == "unknown":
            rep["open_signals"] += 1
            rep["by_product"][product]["open"] += 1
            if len(rep["sample_open"]) < 5:
                rep["sample_open"].append(sample)

        if has_flight_model_inputs(fm):
            rep["have_flight_inputs"] += 1
        else:
            rep["need_backfill"] += 1

        age = signal_age_days(fm, sig_path)
        if age is not None and age > STALE_DAYS:
            rep["stale_signals"] += 1
            rep["by_product"][product]["stale"] += 1

    # Silent recorders = intent-wired but no signals in by_product
    products_with_signals = set(rep["by_product"].keys())
    for product in find_intent_wired_products(root):
        if product not in products_with_signals:
            rep["silent_recorders"].append(product)

    # JSON-serializable
    rep["by_status"] = dict(rep["by_status"].most_common(20))
    rep["by_type"] = dict(rep["by_type"].most_common(20))
    rep["by_product"] = {k: dict(v) for k, v in rep["by_product"].items()}
    rep["by_kind"] = dict(rep["by_kind"])
    return rep


# === Output formatting ===


def format_report(rep: dict) -> str:
    lines = []
    lines.append("\n=== Intent Signal Inventory (V1 — re-grounded) ===")
    lines.append(f"Root: {rep['root']}")
    lines.append(f"YAML lib available: {rep['have_yaml_lib']}")
    lines.append("")
    lines.append(f"Total artifacts found: {rep['total_signals']}")
    if rep.get("by_kind"):
        kbits = ", ".join(f"{k}={v}" for k, v in sorted(rep["by_kind"].items(), key=lambda x: -x[1]))
        lines.append(f"  By kind: {kbits}")
    lines.append(f"  Closure-compliant (labeled gold): {rep['labeled_gold']}")
    lines.append(f"  Symptom-repaired, upstream-pending: {rep['symptom_repaired']}")
    lines.append(f"  Open / pending: {rep['open_signals']}")
    lines.append(f"  Have flight-model inputs (W/T/L/D): {rep['have_flight_inputs']}")
    lines.append(f"  Need backfill (no flight inputs): {rep['need_backfill']}")
    lines.append(f"  Stale (>{STALE_DAYS}d): {rep['stale_signals']}")
    lines.append("")

    if rep["by_status"]:
        lines.append("By status (top 10):")
        for s, c in list(rep["by_status"].items())[:10]:
            lines.append(f"  {s[:60]:>60}: {c}")
        lines.append("")

    if rep["by_type"]:
        lines.append("By type (top 12):")
        for t, c in list(rep["by_type"].items())[:12]:
            lines.append(f"  {t[:60]:>60}: {c}")
        lines.append("")

    if rep["by_product"]:
        lines.append("By product (by signal count):")
        sorted_products = sorted(rep["by_product"].items(), key=lambda x: -x[1]["signals"])
        for p, stats in sorted_products[:25]:
            sig = stats["signals"]
            compl = stats["compliant"]
            pct = (100 * compl / sig) if sig else 0
            lines.append(
                f"  {p[:50]:>50}: {sig:>4} sigs, {compl:>3} resolved ({pct:>3.0f}%), "
                f"{stats['symptom_repaired']:>3} sym, {stats['open']:>3} open, {stats['stale']:>3} stale"
            )
        if len(sorted_products) > 25:
            lines.append(f"  ... and {len(sorted_products) - 25} more products")
        lines.append("")

    if rep["silent_recorders"]:
        lines.append(f"⚠ Silent recorders ({len(rep['silent_recorders'])} products with .intent/ but no signals):")
        for p in rep["silent_recorders"][:20]:
            lines.append(f"  {p}")
        if len(rep["silent_recorders"]) > 20:
            lines.append(f"  ... and {len(rep['silent_recorders']) - 20} more")
        lines.append("")

    if rep["sample_compliant"]:
        lines.append("Sample closure-compliant signals (labeled gold):")
        for s in rep["sample_compliant"]:
            lines.append(f"  {s['id']} — {s['product']} ({s['type']})")
        lines.append("")

    if rep["sample_symptom_repaired"]:
        lines.append("Sample symptom-repaired signals (real catch-net gaps still live):")
        for s in rep["sample_symptom_repaired"]:
            lines.append(f"  {s['id']} — {s['product']}")
        lines.append("")

    lines.append("--- Verdict ---")
    if rep["labeled_gold"] >= 50:
        lines.append(f"WARM START: {rep['labeled_gold']} closure-compliant signals — enough for initial λ prior fit.")
    elif rep["labeled_gold"] >= 10:
        lines.append(f"THIN PRIOR: {rep['labeled_gold']} signals usable as weak prior; plan flight-test heavily.")
    else:
        lines.append(f"NO USABLE HISTORY: skip salvage, go straight to instrumented flight-test.")
    if rep["need_backfill"] > 0:
        lines.append(
            f"BACKFILL GAP: {rep['need_backfill']} signals lack flight-model input fields (W/T/L/D)."
        )
        lines.append("  Forward signal schema must include them. v2 signal-stream spec amendment needed.")
    if rep["silent_recorders"]:
        lines.append(
            f"SILENT-RECORDER GAP: {len(rep['silent_recorders'])} intent-wired products emit nothing. "
            "Witness mandatory-recorder WS-DDR fixes this."
        )
    return "\n".join(lines)


def main(argv) -> int:
    root = Path(argv[1] if len(argv) > 1 else ".").expanduser().resolve()
    if not root.exists():
        print(f"Path not found: {root}", file=sys.stderr)
        return 1
    rep = inventory(root)
    print(format_report(rep))
    Path("inventory.json").write_text(json.dumps(rep, indent=2, default=list))
    print(f"\nwrote inventory.json ({len(json.dumps(rep, default=list))} bytes)")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
