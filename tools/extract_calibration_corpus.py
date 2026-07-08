#!/usr/bin/env python3
"""
extract_calibration_corpus.py — Build labeled-gold corpus from closure-compliant
signals and compute initial per-product λ recommendations.

Per SPEC-INTENT-AUTONOMY-FLIGHT-MODEL-001 §15.2 build step.

Outputs (to extracted-corpus/ relative to this script):
  - labeled-gold-v1.jsonl          — one row per closure-compliant signal
  - symptom-repaired-v1.jsonl      — symptom-repaired signals (gate-too-tight evidence)
  - lambda-recommendations-2026-05-26.md — per-product summary table

Heuristic input derivation (v0 — refit when schema-v2 forward-instrumented data
accumulates per signal-stream v2 amendment 2026-05-26):
  W (gravity) ← severity + pipeline_survival adjustment
  T (thrust)  ← type (discipline-upgrade=high, tooling-noise=low)
  L (lift)    ← concreteness of catch_mechanism + upstream_control_path + pipeline_survival
  D (drag)    ← default 1.0 (timing field not yet captured)

λ recommendation rule (v0):
  closure_rate < 30%: RAISE        — drift accumulating; thrust needed to drive closure
  30% ≤ rate < 60%:  HOLD          — operating in envelope
  closure_rate ≥ 60%: CONFIRM-AND-PROBE — push higher via shadow autonomy

Usage:
    python extract_calibration_corpus.py [WORKSPACES_ROOT] [OUT_DIR]
"""

from __future__ import annotations
import os, re, json, sys, shutil
from datetime import datetime, timezone
from pathlib import Path
from collections import defaultdict

try:
    import yaml
    HAVE_YAML = True
except ImportError:
    HAVE_YAML = False

# Shared skip rules — mirrors theparlor/library-index-system@8a79e07 pattern.
# Importing from sibling module keeps Core/external skip in one place within
# this product directory.
from skip_rules import SKIP_DIRS as EXCLUDE_DIRS, should_skip_subdir

CLOSURE_REQUIRED_FIELDS = ("upstream_control_path", "catch_mechanism")
PENDING_MARKERS = {"pending", "n/a", "none", "tbd", "", "null", "open"}

FRONTMATTER_RE = re.compile(r"\A---\s*\n(.*?)\n---\s*\n", re.DOTALL)


def parse_frontmatter(text: str) -> dict:
    m = FRONTMATTER_RE.match(text)
    if not m:
        return {}
    if HAVE_YAML:
        try:
            data = yaml.safe_load(m.group(1))
            return data if isinstance(data, dict) else {}
        except yaml.YAMLError:
            return {}
    return {}


def _is_concrete(value) -> bool:
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
    status = str(fm.get("status", "")).lower()
    if "resolved" not in status:
        return False
    if "pending" in status or "open" in status or "symptom-repaired" in status:
        return False
    for field in CLOSURE_REQUIRED_FIELDS:
        if not _is_concrete(fm.get(field)):
            return False
    return True


def is_symptom_repaired(fm: dict) -> bool:
    return "symptom-repaired" in str(fm.get("status", "")).lower()


def classify_product(p: Path, root: Path) -> str:
    try:
        rel = p.relative_to(root)
    except ValueError:
        return "EXTERNAL"
    parts = rel.parts
    if not parts:
        return "ROOT"
    if parts[0] == ".intent":
        return "ROOT (Workspaces-wide)"
    if parts[0] == "Core" and len(parts) >= 3 and parts[1] in {"products", "frameworks"}:
        return f"Core/{parts[1]}/{parts[2]}"
    return parts[0]


# === Flight-model input heuristics (v0) ===

SEVERITY_TO_W = {
    "structural": 0.85, "high": 0.75, "medium-high": 0.65, "medium": 0.50,
    "low-medium": 0.35, "low": 0.25, "noise": 0.10,
}

TYPE_TO_T = {
    "discipline-upgrade": 0.90, "architectural-awareness": 0.75,
    "decision-atom": 0.70, "catch-net-gap": 0.60, "wave-closure": 0.50,
    "closure-signal": 0.40, "closure-summary": 0.40, "panel-critique": 0.65,
    "tech-debt": 0.35, "tooling-correctness": 0.50, "tooling-noise": 0.20,
    "signal": 0.50, "pattern": 0.55, "unknown": 0.40,
}


def derive_w(fm: dict) -> float:
    sev = str(fm.get("severity", "medium")).lower().strip()
    w = SEVERITY_TO_W.get(sev, 0.5)
    pipe = str(fm.get("pipeline_survival", "")).lower().strip()
    if pipe.startswith("no"):
        w = min(1.0, w + 0.1)
    return round(w, 3)


def derive_t(fm: dict) -> float:
    t = str(fm.get("type", "unknown")).lower().strip()
    return TYPE_TO_T.get(t, 0.4)


def derive_l(fm: dict) -> float:
    l = 0.2
    if _is_concrete(fm.get("catch_mechanism")):
        l += 0.3
    if _is_concrete(fm.get("upstream_control_path")):
        l += 0.3
    pipe = str(fm.get("pipeline_survival", "")).lower().strip()
    if pipe.startswith("yes"):
        l += 0.2
    return round(min(1.0, l), 3)


def derive_d(fm: dict) -> float:
    return 1.0


def derive_outcome(fm: dict) -> str:
    if is_closure_compliant(fm):
        w = derive_w(fm)
        l = derive_l(fm)
        return "airworthy-and-resolved" if l >= w else "resolved-with-thin-lift"
    if is_symptom_repaired(fm):
        return "symptom-repaired-gate-too-tight"
    return "open"


def find_signals(root: Path):
    seen = set()
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = sorted([
            d for d in dirnames
            if not should_skip_subdir(d, dirpath, root)
        ])
        d = Path(dirpath)
        if d.name == "signals" and d.parent.name == ".intent":
            for fn in filenames:
                if fn.startswith("SIG-") and fn.endswith(".md"):
                    p = d / fn
                    if p not in seen:
                        seen.add(p)
                        yield p


def extract(root: Path):
    gold = []
    symptom = []
    by_product = defaultdict(
        lambda: {"resolved": 0, "symptom_repaired": 0, "open": 0, "total": 0}
    )

    for sig_path in find_signals(root):
        try:
            text = sig_path.read_text(encoding="utf-8", errors="ignore")
        except OSError:
            continue
        fm = parse_frontmatter(text)
        if not fm:
            continue
        product = classify_product(sig_path, root)
        by_product[product]["total"] += 1

        w = derive_w(fm)
        l = derive_l(fm)
        row = {
            "id": fm.get("id", sig_path.name),
            "path": str(sig_path.relative_to(root)) if sig_path.is_relative_to(root) else str(sig_path),
            "product": product,
            "type": fm.get("type", "unknown"),
            "severity": fm.get("severity", "medium"),
            "status": fm.get("status", "unknown"),
            "pipeline_survival": fm.get("pipeline_survival"),
            "W_gravity": w,
            "T_thrust_default": derive_t(fm),
            "L_lift": l,
            "D_drag_default": derive_d(fm),
            "L_minus_W": round(l - w, 3),
            "outcome_label": derive_outcome(fm),
        }

        if is_closure_compliant(fm):
            by_product[product]["resolved"] += 1
            gold.append(row)
        elif is_symptom_repaired(fm):
            by_product[product]["symptom_repaired"] += 1
            symptom.append(row)
        elif "open" in str(fm.get("status", "")).lower() or "pending" in str(fm.get("status", "")).lower():
            by_product[product]["open"] += 1

    return gold, symptom, dict(by_product)


def lambda_recommendation(closure_rate: float):
    if closure_rate < 0.30:
        return ("RAISE", "λ × 1.3-1.5 — drift accumulating; thrust needed to drive closure")
    elif closure_rate < 0.60:
        return ("HOLD", "λ unchanged — operating in envelope")
    else:
        return ("CONFIRM-AND-PROBE", "λ × 1.1-1.2 — closing well; push higher via shadow autonomy")


def backup_if_exists(path: Path) -> Path | None:
    """Copy an existing file to a timestamped .bak sibling before it gets
    overwritten. Returns the backup path, or None if there was nothing to
    back up. Guards against the exact failure this fixes: a re-run silently
    clobbering a prior corpus snapshot with empty or partial output (per
    RETRO-2026-05-29-enforcement-drag-SIG-2, org-design-tooling).
    """
    if not path.exists():
        return None
    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    backup_path = path.with_name(f"{path.name}.pre-{stamp}.bak")
    shutil.copy2(path, backup_path)
    return backup_path


def write_text_with_backup(path: Path, content: str) -> None:
    backup_if_exists(path)
    path.write_text(content)


def write_outputs(gold, symptom, by_product, out_dir: Path):
    out_dir.mkdir(parents=True, exist_ok=True)

    write_text_with_backup(
        out_dir / "labeled-gold-v1.jsonl",
        "\n".join(json.dumps(r) for r in gold) + "\n",
    )
    write_text_with_backup(
        out_dir / "symptom-repaired-v1.jsonl",
        "\n".join(json.dumps(r) for r in symptom) + "\n",
    )

    md = [
        "# Initial λ Recommendations (v0 heuristic)",
        "",
        f"Generated 2026-05-26 from {len(gold)} closure-compliant + {len(symptom)} symptom-repaired signals.",
        "",
        "## Method",
        "",
        "Per-product closure rate = `resolved / (resolved + symptom_repaired + open)`.",
        "",
        "- `closure_rate < 30%` → **RAISE** λ × 1.3-1.5",
        "- `30% ≤ rate < 60%` → **HOLD**",
        "- `closure_rate ≥ 60%` → **CONFIRM-AND-PROBE** λ × 1.1-1.2",
        "",
        "These are v0 starting points, not fits. Schema-v2 forward-instrumented data + `lambda_fit.py` will replace these once available.",
        "",
        "## Per-product recommendations",
        "",
        "| Product | Resolved | Sym-rep | Open | Closure rate | Recommendation | Rationale |",
        "|---|---:|---:|---:|---:|---|---|",
    ]

    for product, stats in sorted(by_product.items(), key=lambda x: -x[1]["total"]):
        denom = stats["resolved"] + stats["symptom_repaired"] + stats["open"]
        if denom == 0:
            continue
        cr = stats["resolved"] / denom
        rec, rationale = lambda_recommendation(cr)
        md.append(
            f"| {product} | {stats['resolved']} | {stats['symptom_repaired']} | "
            f"{stats['open']} | {cr*100:.0f}% | **{rec}** | {rationale} |"
        )

    md.extend([
        "",
        "## Aggregate λ-bias signal",
        "",
        "Products with closure_rate < 30% are the strongest stall indicators per SPEC-INTENT-AUTONOMY-FLIGHT-MODEL-001 §3. ",
        "Small-N products with closure_rate ≥ 60% (Witness, Cortège, Warp, Reference-substrate) reflect single-owner attention at low signal volume — useful as upper-envelope confirmation, not lower-envelope evidence.",
        "",
        "## Application",
        "",
        "1. Each product's `.intent/INTENT.md` adds `lambda_settings.default:` set to (current_baseline × multiplier).",
        "2. Until per-product baselines are established, treat the default at 1.0 and multiply per the table.",
        "3. Per-surface overrides remain governed by the autonomy-gate-surface-matrix (`Core/frameworks/intent/spec/autonomy-gate-surface-matrix-v0-DRAFT.md`).",
        "",
        "## Outcome-label distribution (gold)",
        "",
    ])

    outcome_counts = defaultdict(int)
    for r in gold:
        outcome_counts[r["outcome_label"]] += 1
    for k, v in sorted(outcome_counts.items(), key=lambda x: -x[1]):
        md.append(f"- `{k}`: {v}")

    outcome_counts_sym = defaultdict(int)
    for r in symptom:
        outcome_counts_sym[r["outcome_label"]] += 1
    md.append("")
    md.append("## Outcome-label distribution (symptom-repaired)")
    md.append("")
    for k, v in sorted(outcome_counts_sym.items(), key=lambda x: -x[1]):
        md.append(f"- `{k}`: {v}")

    md.extend([
        "",
        "## Next step",
        "",
        "Fit per-product λ from these counts. The fit script is the next tool to author (`lambda_fit.py`); ratification dependency for promoting SPEC-INTENT-AUTONOMY-FLIGHT-MODEL-001 from draft to accepted.",
    ])

    write_text_with_backup(out_dir / "lambda-recommendations-2026-05-26.md", "\n".join(md))

    print(f"Wrote {len(gold)} labeled-gold rows -> {out_dir}/labeled-gold-v1.jsonl")
    print(f"Wrote {len(symptom)} symptom-repaired rows -> {out_dir}/symptom-repaired-v1.jsonl")
    print(f"Wrote per-product λ recommendations -> {out_dir}/lambda-recommendations-2026-05-26.md")


def main(argv) -> int:
    root = Path(argv[1] if len(argv) > 1 else ".").expanduser().resolve()
    out_dir = Path(argv[2] if len(argv) > 2 else "extracted-corpus").expanduser().resolve()
    if not root.exists():
        print(f"Path not found: {root}", file=sys.stderr)
        return 1
    print(f"Extracting from {root}...")
    gold, symptom, by_product = extract(root)
    write_outputs(gold, symptom, by_product, out_dir)
    print(f"\nProcessed {len(by_product)} products. {len(gold)} labeled-gold + {len(symptom)} symptom-repaired.")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
