#!/usr/bin/env python3
"""
lambda_fit.py — Per-product λ fit from extracted calibration corpus.

Replaces the v0 heuristic recommendation table (lambda-recommendations-2026-05-26.md)
with computed λ values + lift-investment diagnostic per product.

Per SPEC-INTENT-AUTONOMY-FLIGHT-MODEL-001 §8 (Calibrating λ from the drift corpus).

Inputs:
  - extracted-corpus/labeled-gold-v1.jsonl      (229 closure-compliant signals)
  - extracted-corpus/symptom-repaired-v1.jsonl  (61 gate-too-tight signals)

Outputs:
  - extracted-corpus/lambda-fit-v1.json         (machine-readable diagnostic)
  - extracted-corpus/lambda-settings-by-product-v1.yaml (paste-ready INTENT.md snippets)
  - extracted-corpus/lambda-fit-v1-report.md    (human-readable report)

================================================================================
Fit model (v1)
================================================================================

The flight model decouples two diagnostic axes:

  λ (Thrust adjustment)        — accelerator. Drives more decisions to closure.
                                 Indicated when closure_rate is low AND lift is adequate.

  lift_investment (containment) — manufactured recovery capacity. Built BEFORE
                                 raising λ when symptom-repaired rate is high
                                 relative to closure rate (acting without
                                 adequate L→W margin produces sym-rep signals).

Per-product fit:

  stall_loss      = 1 - closure_rate
  containment_gap = sym_rep_rate / max(closure_rate, 0.1)

  λ_fit             = λ_baseline × (1 + α × stall_loss)            # α = 0.5
  lift_investment   = β × containment_gap                          # β = 0.3
  λ_apply_now       = λ_fit if lift_investment < 0.5 else λ_baseline
  lift_action       = NONE | OPTIONAL | RECOMMENDED | REQUIRED-BEFORE-λ-RAISE

Decision matrix:

  | containment_gap | lift_investment | recommendation                          |
  |-----------------|-----------------|-----------------------------------------|
  | < 0.20          | < 0.06          | NONE — apply λ_fit directly             |
  | 0.20 - 0.50     | 0.06 - 0.15     | OPTIONAL — apply λ_fit, monitor sym-rep |
  | 0.50 - 1.00     | 0.15 - 0.30     | RECOMMENDED — invest in L, then λ_fit   |
  | ≥ 1.00          | ≥ 0.30          | REQUIRED — build L FIRST, defer λ raise |

λ_apply_now is the value safe to apply today; λ_fit is the value once lift
investment lands.

================================================================================
Limitations of v1 (refit when these resolve)
================================================================================

  - Overspeed proxy is weak: our heuristic puts all closure-compliant signals at
    L≥W (airworthy). True overspeed indicators require explicit `autonomy_level`
    and `lambda_used` fields per signal-stream v2 schema amendment.
  - λ baseline is 1.0 for all products. Per-actor topology adjustments (theparlor
    solo = 1.5-2.0; cross-human-comms = 0.0) per flight-model spec §16 are NOT
    applied here — they layer on top of the fit value.
  - α and β are heuristic. They can be re-tuned when forward-instrumented data
    accumulates and a held-out test set is available.

================================================================================

Usage:
    python lambda_fit.py [CORPUS_DIR]
    (default: ./extracted-corpus relative to script)
"""

from __future__ import annotations
import json, sys
from pathlib import Path
from collections import defaultdict

try:
    import yaml
    HAVE_YAML = True
except ImportError:
    HAVE_YAML = False


# Fit constants
LAMBDA_BASELINE = 1.0
ALPHA = 0.5  # stall penalty weight
BETA = 0.3   # containment-gap weight
LIFT_REQUIRED_THRESHOLD = 0.30
LIFT_RECOMMENDED_THRESHOLD = 0.15
LIFT_OPTIONAL_THRESHOLD = 0.06


def load_jsonl(path: Path) -> list:
    if not path.exists():
        return []
    rows = []
    for line in path.read_text(encoding="utf-8").splitlines():
        if line.strip():
            try:
                rows.append(json.loads(line))
            except json.JSONDecodeError:
                continue
    return rows


def aggregate_by_product(gold: list, symptom: list) -> dict:
    """Group rows by product. Open-signal counts come in via supplementary input."""
    by_product = defaultdict(lambda: {
        "n_closure": 0,
        "n_symptom": 0,
        "n_open": 0,
        "closure_W_mean": 0.0,
        "closure_L_mean": 0.0,
        "closure_T_mean": 0.0,
        "symptom_W_mean": 0.0,
        "symptom_L_mean": 0.0,
    })

    closure_w_sum = defaultdict(float)
    closure_l_sum = defaultdict(float)
    closure_t_sum = defaultdict(float)
    symptom_w_sum = defaultdict(float)
    symptom_l_sum = defaultdict(float)

    for r in gold:
        p = r["product"]
        by_product[p]["n_closure"] += 1
        closure_w_sum[p] += r.get("W_gravity", 0.5)
        closure_l_sum[p] += r.get("L_lift", 0.5)
        closure_t_sum[p] += r.get("T_thrust_default", 0.4)

    for r in symptom:
        p = r["product"]
        by_product[p]["n_symptom"] += 1
        symptom_w_sum[p] += r.get("W_gravity", 0.5)
        symptom_l_sum[p] += r.get("L_lift", 0.5)

    for p in by_product:
        n_c = by_product[p]["n_closure"]
        n_s = by_product[p]["n_symptom"]
        if n_c:
            by_product[p]["closure_W_mean"] = round(closure_w_sum[p] / n_c, 3)
            by_product[p]["closure_L_mean"] = round(closure_l_sum[p] / n_c, 3)
            by_product[p]["closure_T_mean"] = round(closure_t_sum[p] / n_c, 3)
        if n_s:
            by_product[p]["symptom_W_mean"] = round(symptom_w_sum[p] / n_s, 3)
            by_product[p]["symptom_L_mean"] = round(symptom_l_sum[p] / n_s, 3)

    return dict(by_product)


def attach_open_counts(by_product: dict, corpus_dir: Path) -> dict:
    """Read inventory.json from prior crawler run to attach open-signal counts."""
    inv_path = corpus_dir.parent.parent.parent.parent / "inventory.json"
    # Try alternate path: corpus_dir/../inventory.json (less likely)
    alt_path = corpus_dir.parent / "inventory.json"
    inv_path = inv_path if inv_path.exists() else alt_path
    if not inv_path.exists():
        # Fallback: inventory.json in /tmp from earlier run
        for candidate in [Path("/tmp/inventory.json"), Path("inventory.json")]:
            if candidate.exists():
                inv_path = candidate
                break
    if not inv_path.exists():
        print(f"  (no inventory.json found — open counts default to 0)", file=sys.stderr)
        return by_product
    try:
        inv = json.loads(inv_path.read_text())
    except (OSError, json.JSONDecodeError):
        return by_product

    by_prod_inv = inv.get("by_product", {})
    for p, stats in by_prod_inv.items():
        if p in by_product:
            by_product[p]["n_open"] = stats.get("open", 0)
        elif stats.get("open", 0) > 0:
            # Product has open signals but no gold or sym — add it
            by_product[p] = {
                "n_closure": 0,
                "n_symptom": 0,
                "n_open": stats.get("open", 0),
                "closure_W_mean": 0.0,
                "closure_L_mean": 0.0,
                "closure_T_mean": 0.0,
                "symptom_W_mean": 0.0,
                "symptom_L_mean": 0.0,
            }
    return by_product


def fit_product(stats: dict) -> dict:
    n_c = stats["n_closure"]
    n_s = stats["n_symptom"]
    n_o = stats["n_open"]
    n_total = n_c + n_s + n_o
    if n_total == 0:
        return None

    closure_rate = n_c / n_total
    sym_rep_rate = n_s / n_total

    stall_loss = 1.0 - closure_rate
    containment_gap = sym_rep_rate / max(closure_rate, 0.1)

    lambda_fit = LAMBDA_BASELINE * (1 + ALPHA * stall_loss)
    lift_investment = BETA * containment_gap

    if lift_investment >= LIFT_REQUIRED_THRESHOLD:
        lift_action = "REQUIRED-BEFORE-λ-RAISE"
        lambda_apply_now = LAMBDA_BASELINE
    elif lift_investment >= LIFT_RECOMMENDED_THRESHOLD:
        lift_action = "RECOMMENDED"
        lambda_apply_now = round((LAMBDA_BASELINE + lambda_fit) / 2, 3)
    elif lift_investment >= LIFT_OPTIONAL_THRESHOLD:
        lift_action = "OPTIONAL"
        lambda_apply_now = round(lambda_fit, 3)
    else:
        lift_action = "NONE"
        lambda_apply_now = round(lambda_fit, 3)

    avg_l_closure = stats.get("closure_L_mean", 0.0)
    avg_l_symptom = stats.get("symptom_L_mean", 0.0)
    lift_gap = round(avg_l_closure - avg_l_symptom, 3) if avg_l_symptom > 0 else None

    return {
        "n_closure": n_c,
        "n_symptom": n_s,
        "n_open": n_o,
        "n_total": n_total,
        "closure_rate": round(closure_rate, 3),
        "sym_rep_rate": round(sym_rep_rate, 3),
        "stall_loss": round(stall_loss, 3),
        "containment_gap": round(containment_gap, 3),
        "lambda_fit": round(lambda_fit, 3),
        "lambda_apply_now": lambda_apply_now,
        "lift_investment": round(lift_investment, 3),
        "lift_action": lift_action,
        "closure_W_mean": stats.get("closure_W_mean"),
        "closure_L_mean": stats.get("closure_L_mean"),
        "symptom_L_mean": stats.get("symptom_L_mean"),
        "L_gap_closure_minus_symptom": lift_gap,
    }


def write_outputs(by_product: dict, fits: dict, out_dir: Path):
    out_dir.mkdir(parents=True, exist_ok=True)

    # 1. JSON diagnostic dump
    (out_dir / "lambda-fit-v1.json").write_text(json.dumps(fits, indent=2, sort_keys=True))

    # 2. YAML — paste-ready snippets per product
    yaml_lines = [
        "# Lambda settings by product — generated 2026-05-26 by lambda_fit.py",
        "# Paste relevant block into each product's .intent/INTENT.md under lambda_settings:",
        "# Per SPEC-INTENT-AUTONOMY-FLIGHT-MODEL-001 §16 (λ-scoping convention)",
        "#",
        "# Layering: these are per-product baseline λ values. Per-surface overrides",
        "# (e.g., cross_human_comms: 0.0) and per-actor topology adjustments",
        "# (theparlor-solo += 0.5-1.0) layer on top of the fit value.",
        "",
    ]
    for product in sorted(fits.keys()):
        f = fits[product]
        if f is None:
            continue
        yaml_lines.append(f"# === {product} ===")
        yaml_lines.append(f"# closure_rate={f['closure_rate']*100:.0f}% "
                          f"(n={f['n_total']}, gold={f['n_closure']}, "
                          f"sym={f['n_symptom']}, open={f['n_open']})")
        yaml_lines.append(f"# lift_action: {f['lift_action']}")
        yaml_lines.append("lambda_settings:")
        yaml_lines.append(f"  default: {f['lambda_apply_now']}")
        yaml_lines.append(f"  fit_target: {f['lambda_fit']}  # value to apply after lift investment")
        yaml_lines.append(f"  last_fit: 2026-05-26")
        yaml_lines.append(f"  fit_source: Core/frameworks/intent/tools/lambda_fit.py")
        yaml_lines.append(f"  rationale: |")
        yaml_lines.append(f"    stall_loss={f['stall_loss']}, containment_gap={f['containment_gap']}.")
        if f['lift_action'] == "REQUIRED-BEFORE-λ-RAISE":
            yaml_lines.append(f"    Lift insufficient — invest in catch_mechanism + upstream_control")
            yaml_lines.append(f"    coverage BEFORE raising λ above baseline. Current default holds at")
            yaml_lines.append(f"    baseline 1.0; fit_target {f['lambda_fit']} applies after lift work.")
        elif f['lift_action'] == "RECOMMENDED":
            yaml_lines.append(f"    Lift investment recommended; default is mid-point of baseline and")
            yaml_lines.append(f"    fit_target. Promote default to fit_target after lift gap closes.")
        elif f['lift_action'] == "OPTIONAL":
            yaml_lines.append(f"    Lift adequate. Default = fit_target. Monitor sym-rep rate.")
        else:
            yaml_lines.append(f"    Lift solid. Default = fit_target. Shadow-autonomy probes")
            yaml_lines.append(f"    can push higher.")
        yaml_lines.append("")
    (out_dir / "lambda-settings-by-product-v1.yaml").write_text("\n".join(yaml_lines))

    # 3. Human-readable report
    md = [
        "# λ Fit v1 — Per-Product Computed Values",
        "",
        "Generated 2026-05-26 by `lambda_fit.py` from extracted calibration corpus.",
        "",
        "## Fit model",
        "",
        "```",
        f"  λ_fit             = {LAMBDA_BASELINE} × (1 + {ALPHA} × stall_loss)",
        f"  lift_investment   = {BETA} × (sym_rep_rate / max(closure_rate, 0.1))",
        f"  λ_apply_now       = λ_fit  if lift_investment < {LIFT_RECOMMENDED_THRESHOLD}",
        f"                      midpoint  if {LIFT_RECOMMENDED_THRESHOLD} ≤ lift_inv < {LIFT_REQUIRED_THRESHOLD}",
        f"                      baseline  if lift_inv ≥ {LIFT_REQUIRED_THRESHOLD}",
        "```",
        "",
        "**Key insight from the fit:** containment gap (symptom-repaired / closure-compliant) "
        "is a *Lift* problem, not a *Thrust* problem. Products with high containment_gap need "
        "to manufacture more lift (catch_mechanism + upstream_control_path coverage) BEFORE "
        "raising λ — otherwise λ raise produces more symptom-repaired, not more closure.",
        "",
        "## Per-product fit (sorted by signal count)",
        "",
        "| Product | n | Closure% | Sym% | λ_fit | λ_apply_now | Lift action |",
        "|---|---:|---:|---:|---:|---:|---|",
    ]
    for product, f in sorted(fits.items(), key=lambda kv: -(kv[1]["n_total"] if kv[1] else 0)):
        if f is None:
            continue
        action_emoji = {
            "REQUIRED-BEFORE-λ-RAISE": "🛑",
            "RECOMMENDED": "⚠",
            "OPTIONAL": "·",
            "NONE": "✓",
        }.get(f["lift_action"], "")
        md.append(
            f"| {product} | {f['n_total']} | "
            f"{f['closure_rate']*100:.0f}% | {f['sym_rep_rate']*100:.0f}% | "
            f"{f['lambda_fit']} | **{f['lambda_apply_now']}** | "
            f"{action_emoji} {f['lift_action']} |"
        )

    md.extend([
        "",
        "## Lift-action distribution",
        "",
    ])
    action_counts = defaultdict(int)
    for f in fits.values():
        if f:
            action_counts[f["lift_action"]] += 1
    for action in ["REQUIRED-BEFORE-λ-RAISE", "RECOMMENDED", "OPTIONAL", "NONE"]:
        c = action_counts.get(action, 0)
        md.append(f"- **{action}**: {c}")

    md.extend([
        "",
        "## Products needing lift investment FIRST (do not raise λ yet)",
        "",
    ])
    for product, f in sorted(fits.items(), key=lambda kv: -(kv[1]["containment_gap"] if kv[1] else 0)):
        if f and f["lift_action"] == "REQUIRED-BEFORE-λ-RAISE":
            md.append(
                f"- **{product}**: containment_gap={f['containment_gap']:.2f}, "
                f"closure={f['closure_rate']*100:.0f}%, sym={f['sym_rep_rate']*100:.0f}%. "
                f"λ stays at baseline {f['lambda_apply_now']} until lift work lands "
                f"(target: {f['lambda_fit']})."
            )

    md.extend([
        "",
        "## Products ready to apply fit λ directly",
        "",
    ])
    for product, f in sorted(fits.items(), key=lambda kv: -(kv[1]["lambda_fit"] if kv[1] else 0)):
        if f and f["lift_action"] in ("NONE", "OPTIONAL"):
            md.append(
                f"- **{product}**: λ_apply_now={f['lambda_apply_now']} "
                f"(closure={f['closure_rate']*100:.0f}%, "
                f"sym/closure ratio={f['containment_gap']:.2f})"
            )

    md.extend([
        "",
        "## Application path",
        "",
        "1. Read `lambda-settings-by-product-v1.yaml` — contains paste-ready snippets per product.",
        "2. For each product NOT in REQUIRED-BEFORE-λ-RAISE: paste the `lambda_settings:` block into that product's `.intent/INTENT.md`.",
        "3. For products in REQUIRED-BEFORE-λ-RAISE: paste the block as-is (default stays at baseline 1.0), AND open a signal capturing the lift-investment work needed for that product.",
        "4. After 30 days of post-fit data, re-run `extract_calibration_corpus.py` + `lambda_fit.py` to refit.",
        "5. Layer per-actor topology adjustments per flight-model spec §16 §Defaults by actor topology (theparlor-solo +0.5-1.0; cross-human-comms locked at 0.0).",
        "",
        "## Open dependencies",
        "",
        "- Cast schema amendment (formalize risk_appetite / decision_stance / panel_role fields)",
        "- PreToolUse `signal-recorder-silent` hook (mechanism for WS-DDR-098 enforcement)",
        "- `panel-critique-v2-balanced` Forge operator (Cast bravery-prior personas need rendering)",
        "- Schema v2 forward-instrumented signal data (will replace heuristic input derivation in next refit)",
        "",
        "## Limitations of v1 (re-fit when these resolve)",
        "",
        "- **Overspeed proxy is weak**: heuristic puts all closure-compliant signals at L≥W (airworthy). True overspeed indicators require explicit `autonomy_level` and `lambda_used` fields per signal-stream v2 schema.",
        "- **λ baseline is 1.0 globally**: per-actor topology adjustments (per flight-model spec §16) layer on top — not yet automated.",
        "- **α and β are heuristic** (0.5 and 0.3). They can be re-tuned when forward-instrumented data accumulates and a held-out test set is available.",
    ])

    (out_dir / "lambda-fit-v1-report.md").write_text("\n".join(md))

    print(f"Wrote lambda-fit-v1.json -> {out_dir}/lambda-fit-v1.json")
    print(f"Wrote lambda-settings-by-product-v1.yaml -> {out_dir}/lambda-settings-by-product-v1.yaml")
    print(f"Wrote lambda-fit-v1-report.md -> {out_dir}/lambda-fit-v1-report.md")


def main(argv) -> int:
    corpus_dir = Path(argv[1] if len(argv) > 1 else "extracted-corpus").expanduser().resolve()
    if not corpus_dir.exists():
        print(f"Corpus dir not found: {corpus_dir}", file=sys.stderr)
        return 1

    gold = load_jsonl(corpus_dir / "labeled-gold-v1.jsonl")
    symptom = load_jsonl(corpus_dir / "symptom-repaired-v1.jsonl")
    print(f"Loaded {len(gold)} labeled-gold + {len(symptom)} symptom-repaired rows.")

    by_product = aggregate_by_product(gold, symptom)
    by_product = attach_open_counts(by_product, corpus_dir)

    fits = {}
    for product, stats in by_product.items():
        fit = fit_product(stats)
        if fit is not None:
            fits[product] = fit

    write_outputs(by_product, fits, corpus_dir)

    print(f"\nFit complete: {len(fits)} products.")
    action_counts = defaultdict(int)
    for f in fits.values():
        action_counts[f["lift_action"]] += 1
    for action in ["REQUIRED-BEFORE-λ-RAISE", "RECOMMENDED", "OPTIONAL", "NONE"]:
        print(f"  {action}: {action_counts.get(action, 0)}")

    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
