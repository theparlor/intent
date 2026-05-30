#!/usr/bin/env python3
"""
flight_model.py — D-WIRE: Deterministic Coupled-Forces Autonomy Decision Layer

Implements the Autonomy Flight Model v1 (SPEC-INTENT-AUTONOMY-FLIGHT-MODEL-001).
Replaces the weighted-sum gate in signal-scoring.md with a four-coupled-forces
model that has a REAL VALUE TERM. The key move: stall (doing nothing safely)
is the worse crash — this model flags it, the v1 gate cannot.

CONTRACT: This layer sits ABOVE the hooks 1–7 deterministic floor (§13). Those
hooks are preconditions that must hold regardless. This model computes the
autonomy BAND on top of them. See ratification-tracker §D-WIRE.

Grounding specs (read exactly):
  - Core/products/forge/outputs/claude-code/critique/panel-critique-v2-balanced/variance-estimate.md
  - Core/frameworks/intent/spec/autonomy-flight-model-v1-DRAFT.md §2,3,4,16
  - Core/frameworks/methodology-library/meta/signal-scoring.md (band semantics)
  - Core/frameworks/intent/spec/autonomy-flight-model-ratification-tracker.md §12 defaults

Usage:
  # From variance-estimate YAML
  python3 flight_model.py --input sample-variance-estimate.yaml
  python3 flight_model.py --input sample-variance-estimate.yaml --json
  python3 flight_model.py --input sample-variance-estimate.yaml --lambda 1.5 --drag 0.08

  # Pipe stdin
  cat sample-variance-estimate.yaml | python3 flight_model.py

All constants below are BRIEN-OVERRIDE-ABLE — they are module-level named constants,
not magic numbers. λ in particular is tunable per-surface per §16.
"""

import json
import math
import os
import re
import sys
from enum import Enum
from typing import Any, Dict, Optional, Tuple


# ---------------------------------------------------------------------------
# MODULE-LEVEL CONSTANTS (Brien-override-able — all documented)
# ---------------------------------------------------------------------------

# Default λ (coefficient of bravery). §16 — not a system constant; persisted per-product
# in each product's .intent/INTENT.md lambda_settings.default. CLI --lambda overrides.
LAMBDA_DEFAULT: float = 1.0

# Default Drag overhead fraction (0–1). Derived from drag-report.json block_rate when
# present: overhead = 1 − block_rate. If drag-report.json absent, use this fallback.
DRAG_DEFAULT: float = 0.10

# Path to drag-report.json, resolved relative to this file at runtime.
DRAG_REPORT_PATH: str = os.path.join(os.path.dirname(os.path.abspath(__file__)), "drag-report.json")

# Envelope margins (§2 — both 0.0 by default; Brien may tighten/loosen per product).
# OVERSPEED: fires when W > L + OVERSPEED_MARGIN (Gravity exceeds Lift by margin).
# STALL:     fires when T <= D + STALL_MARGIN  (Thrust can't clear Drag overhead).
OVERSPEED_MARGIN: float = 0.0
STALL_MARGIN: float = 0.0

# AIRWORTHY band cutoffs on margin = min(L - W, T - D).
# Each cutoff is the UPPER bound of the band below it (non-inclusive at top).
# margin < BAND_L1_CUTOFF → L1
# margin < BAND_L2_CUTOFF → L2
# margin < BAND_L3_CUTOFF → L3
# margin >= BAND_L3_CUTOFF → L4
# Derived from signal-scoring.md band boundaries, mapped to margin space.
BAND_CUTOFFS: Dict[str, float] = {
    "L1": 0.15,   # margin < 0.15 → L1
    "L2": 0.35,   # margin in [0.15, 0.35) → L2
    "L3": 0.55,   # margin in [0.35, 0.55) → L3
    # L4: margin >= 0.55
}

# Dispersion demotion threshold (§uncertainty demotion).
# max_dispersion > DISPERSION_DEMOTE → demote one band, recommend probe/shadow-autonomy §9.
# max_dispersion in [DISPERSION_MODERATE, DISPERSION_DEMOTE] → moderate-uncertainty advisory.
DISPERSION_DEMOTE: float = 0.50
DISPERSION_MODERATE: float = 0.20


# ---------------------------------------------------------------------------
# ENVELOPE ENUM
# ---------------------------------------------------------------------------

class Envelope(str, Enum):
    AIRWORTHY = "airworthy"
    STALL = "stall"
    OVERSPEED = "overspeed"


# ---------------------------------------------------------------------------
# DRAG LOADING
# ---------------------------------------------------------------------------

def _load_drag_from_report(path: str = DRAG_REPORT_PATH) -> Optional[float]:
    """
    Try to read block_rate from drag-report.json.
    overhead = 1 − block_rate (fraction of invocations that are pure overhead).
    Returns None if file absent or malformed — caller falls back to DRAG_DEFAULT.
    """
    try:
        with open(path) as f:
            report = json.load(f)
        block_rate = report["runtime_drag"]["block_rate"]
        overhead = 1.0 - float(block_rate)
        # Clamp to [0.0, 1.0] in case of edge values
        return max(0.0, min(1.0, overhead))
    except (FileNotFoundError, KeyError, (ValueError, TypeError)):
        return None


def get_default_drag() -> float:
    """Resolve Drag: try drag-report.json; fall back to DRAG_DEFAULT."""
    d = _load_drag_from_report()
    return d if d is not None else DRAG_DEFAULT


# ---------------------------------------------------------------------------
# FLIGHT MODEL
# ---------------------------------------------------------------------------

class FlightModel:
    """
    Deterministic coupled-forces autonomy decision model.

    Forces (§2):
      W (Gravity) = blast_radius × exposure × irreversibility              — product, 0–1
      T (Thrust)  = strategic_value × λ                                    — value term, can exceed 1
      L (Lift)    = mean(containment_posture, detection_speed,              — normalized to 0–1
                         recovery_options)
      [§2 writes Lift as a sum; we normalize to mean so L is directly
       comparable to W in the OVERSPEED check (W > L). This is documented
       here per the §2 citation requirement — the normalization is defensive
       for the AIRWORTHY check, not an alteration of the spec's intent.]
      D (Drag)    = measured overhead fraction 0–1

    Crash modes (§3):
      OVERSPEED: W > L + OVERSPEED_MARGIN  — gravity exceeds lift
      STALL:     T ≤ D + STALL_MARGIN     — thrust can't clear drag
      AIRWORTHY: neither

    §3 is explicit: STALL is the worse crash. A valueless-but-safe action
    that yields STALL is NOT a comfortable L0 — it is a system failure.
    """

    def __init__(
        self,
        strategic_value: float,
        blast_radius: float,
        irreversibility: float,
        exposure: float,
        containment_posture: float,
        detection_speed: float,
        recovery_options: float,
        lam: float = LAMBDA_DEFAULT,
        drag: Optional[float] = None,
        max_dispersion: float = 0.0,
        routing_hint: str = "low-uncertainty",
        flags: Optional[list] = None,
    ):
        self.strategic_value = strategic_value
        self.blast_radius = blast_radius
        self.irreversibility = irreversibility
        self.exposure = exposure
        self.containment_posture = containment_posture
        self.detection_speed = detection_speed
        self.recovery_options = recovery_options
        self.lam = lam
        self.drag = drag if drag is not None else get_default_drag()
        self.max_dispersion = max_dispersion
        self.routing_hint = routing_hint
        self.flags = flags or []

    def compute(self) -> Dict[str, Any]:
        """
        Run the deterministic flight model.

        Returns structured result:
          {inputs, W, T, L, D, envelope, band, binding_constraint,
           recommended_action, uncertainty}
        """
        # --- Force computation ---
        W = self.blast_radius * self.exposure * self.irreversibility
        T = self.strategic_value * self.lam
        L = (self.containment_posture + self.detection_speed + self.recovery_options) / 3.0
        D = self.drag

        # --- Envelope determination (§3) ---
        # Stall check FIRST — it is the worse crash (§3).
        # A zero-value action that is perfectly safe STALLS here, not at a comfortable L0.
        if T <= D + STALL_MARGIN:
            envelope = Envelope.STALL
            band = "L0"
            binding_constraint = "thrust"
            recommended_action = (
                "STALL — the worse crash (§3): Thrust (strategic_value × λ = "
                f"{T:.3f}) does not clear Drag overhead ({D:.3f}). "
                "This is NOT a safe default — it is a stall. Operationalizing caution, "
                "not strategy (§1). Fix: raise λ (bravery throttle) to increase thrust, "
                "cut Drag by reducing hook overhead, or reconsider whether this action "
                "has strategic_value at all. A do-nothing-safely stall starves the "
                "Observe loop of signal and decays calibration capacity. See §3."
            )
        elif W > L + OVERSPEED_MARGIN:
            # OVERSPEED: gravity exceeds lift — acting past recovery capacity
            envelope = Envelope.OVERSPEED
            band = "L0"
            binding_constraint = "gravity"
            recommended_action = (
                "OVERSPEED: Gravity (W={:.3f}) exceeds Lift (L={:.3f}). "
                "Invest in Lift (sandbox / branch / flag / rollback / canary / "
                "ephemeral-wiki / dry-run) to raise L above W before acting. "
                "Reversibility is a budget to spend, not a fixed property (§5). "
                "After Lift investment, re-estimate and re-run."
            ).format(W, L)
        else:
            # AIRWORTHY — compute margin and map to band
            envelope = Envelope.AIRWORTHY
            gravity_margin = L - W       # how much Lift exceeds Gravity
            thrust_margin = T - D        # how much Thrust exceeds Drag
            margin = min(gravity_margin, thrust_margin)
            binding_constraint = "gravity" if gravity_margin <= thrust_margin else "thrust"

            band = self._margin_to_band(margin)
            recommended_action = self._airworthy_action(band, margin, W, T, L, D)

            # Uncertainty demotion (must happen AFTER band is assigned)
            band, recommended_action = self._apply_dispersion_demotion(
                band, recommended_action, margin
            )

        # Degraded-mode check: bravery-prior-gap flag forces cap at L2
        if any("bravery-prior-gap" in f for f in self.flags):
            band_order = ["L0", "L1", "L2", "L3", "L4"]
            if band_order.index(band) > band_order.index("L2"):
                band = "L2"
                recommended_action = (
                    "[DEGRADED-MODE: bravery-prior-gap flag — panel under-composed. "
                    "Cannot certify above L2. Intake bold-prior personas (§10/§11.3) "
                    "and re-run panel before raising band.] " + recommended_action
                )

        return {
            "inputs": {
                "strategic_value": self.strategic_value,
                "blast_radius": self.blast_radius,
                "irreversibility": self.irreversibility,
                "exposure": self.exposure,
                "containment_posture": self.containment_posture,
                "detection_speed": self.detection_speed,
                "recovery_options": self.recovery_options,
                "lam": self.lam,
                "drag": self.drag,
                "max_dispersion": self.max_dispersion,
            },
            "W": W,
            "T": T,
            "L": L,
            "D": D,
            "envelope": envelope,
            "band": band,
            "binding_constraint": binding_constraint,
            "recommended_action": recommended_action,
            "uncertainty": {
                "max_dispersion": self.max_dispersion,
                "routing_hint": self.routing_hint,
            },
        }

    def _margin_to_band(self, margin: float) -> str:
        """Map airworthy margin to L1–L4 band via BAND_CUTOFFS constants."""
        if margin < BAND_CUTOFFS["L1"]:
            return "L1"
        elif margin < BAND_CUTOFFS["L2"]:
            return "L2"
        elif margin < BAND_CUTOFFS["L3"]:
            return "L3"
        else:
            return "L4"

    def _airworthy_action(self, band: str, margin: float, W: float, T: float, L: float, D: float) -> str:
        band_descriptions = {
            "L1": "Enrich only — agent assists, human decides. Lightweight enrichment, no external action.",
            "L2": "Investigate — dispatch bounded Sonnet research; human reviews finding before further action.",
            "L3": "Hypothesize — investigate + Opus interprets findings; human monitors, may redirect.",
            "L4": "Full autonomy — execute skill chain; Brien reviews deliverable, not the decision.",
        }
        desc = band_descriptions.get(band, "")
        return (
            f"AIRWORTHY — band {band} (margin={margin:.3f}, binding={self._binding_label(W, T, L, D)}). "
            f"{desc}"
        )

    def _binding_label(self, W: float, T: float, L: float, D: float) -> str:
        gravity_margin = L - W
        thrust_margin = T - D
        if gravity_margin <= thrust_margin:
            return f"gravity (L-W={gravity_margin:.3f})"
        else:
            return f"thrust (T-D={thrust_margin:.3f})"

    def _apply_dispersion_demotion(
        self, band: str, action: str, margin: float
    ) -> Tuple[str, str]:
        """
        Apply uncertainty demotion based on max_dispersion (variance-estimate §uncertainty-demotion).

        - max_dispersion > DISPERSION_DEMOTE (0.50): demote one band (min L1)
          + recommend probe/shadow-autonomy §9
        - max_dispersion in [DISPERSION_MODERATE, DISPERSION_DEMOTE] (0.20–0.50):
          advisory only — mention Lift investment + re-estimate
        """
        if band == "L0":
            return band, action  # already floor, no demotion needed

        BAND_ORDER = ["L0", "L1", "L2", "L3", "L4"]
        idx = BAND_ORDER.index(band)

        if self.max_dispersion > DISPERSION_DEMOTE:
            # Demote one band, minimum L1
            new_idx = max(1, idx - 1)
            new_band = BAND_ORDER[new_idx]
            new_action = (
                f"[UNCERTAINTY DEMOTION: max_dispersion={self.max_dispersion:.2f} > {DISPERSION_DEMOTE} — "
                f"panel spread too wide to certify {band}. Demoted to {new_band}. "
                "Route to a cheap probe (ephemeral wiki / dry-run / shadow-autonomy §9) "
                "before any live grant. Re-compose panel with wider bold/safety spread and re-estimate.] "
                + action
            )
            return new_band, new_action
        elif self.max_dispersion >= DISPERSION_MODERATE:
            # Advisory — no demotion, but flag
            advisory = (
                f" [MODERATE UNCERTAINTY: max_dispersion={self.max_dispersion:.2f} in "
                f"[{DISPERSION_MODERATE},{DISPERSION_DEMOTE}]. Consider a Lift investment (§5) "
                "then re-estimate before live grant.]"
            )
            return band, action + advisory
        else:
            return band, action


# ---------------------------------------------------------------------------
# VARIANCE-ESTIMATE YAML PARSING
# ---------------------------------------------------------------------------

def _fallback_load_variance_estimate(path: str) -> Tuple[Dict[str, float], Dict[str, Any]]:
    """
    Minimal fallback parser for the flight-model-variance-estimate block.
    Handles the fixed block shape from variance-estimate.md.
    YAML must have single-line scalar values for point_estimate and dispersion
    (as the spec's sample enforces).

    Returns: (facets: {name: point_estimate}, meta: {max_dispersion, routing_hint, flags})
    """
    FACET_NAMES = [
        "strategic_value", "blast_radius", "irreversibility", "exposure",
        "containment_posture", "detection_speed", "recovery_options",
    ]

    facets: Dict[str, float] = {}
    max_dispersion: float = 0.0
    routing_hint: str = "low-uncertainty"
    flags: list = []

    with open(path) as f:
        content = f.read()

    # Extract the flight-model-variance-estimate block
    block_match = re.search(
        r"flight-model-variance-estimate:(.*?)(?=^---|\Z)",
        content,
        re.DOTALL | re.MULTILINE,
    )
    if not block_match:
        raise ValueError("No 'flight-model-variance-estimate:' block found in file.")

    block = block_match.group(1)

    # Extract point_estimate per facet.
    # Matches: "    strategic_value:\n      ...\n      point_estimate: 0.65"
    # or inline after the facet. We scan for "point_estimate:" after each facet block.
    current_facet: Optional[str] = None
    for line in block.splitlines():
        stripped = line.strip()

        # Detect facet start (non-indented within the block, or 4-space indented under facets:)
        for facet in FACET_NAMES:
            if stripped.startswith(facet + ":"):
                current_facet = facet
                break

        if current_facet and stripped.startswith("point_estimate:"):
            val_str = stripped.split(":", 1)[1].strip()
            # Strip inline comment
            val_str = val_str.split("#")[0].strip()
            try:
                facets[current_facet] = float(val_str)
            except ValueError:
                pass
            current_facet = None

        # Aggregate max_dispersion
        if stripped.startswith("max_dispersion:") and "max_dispersion_facet" not in stripped:
            val_str = stripped.split(":", 1)[1].strip().split("#")[0].strip()
            try:
                max_dispersion = float(val_str)
            except ValueError:
                pass

        # Routing hint
        if stripped.startswith("consumer_routing_hint:"):
            routing_hint = stripped.split(":", 1)[1].strip().strip('"').strip("'")

        # Flags (simple list detection)
        if stripped.startswith("flags:"):
            flags_str = stripped.split(":", 1)[1].strip()
            if flags_str and flags_str != "[]":
                # Parse inline list [a, b, c] or note multi-line
                flags_str = flags_str.strip("[]")
                flags = [f.strip().strip('"').strip("'") for f in flags_str.split(",") if f.strip()]

    return facets, {"max_dispersion": max_dispersion, "routing_hint": routing_hint, "flags": flags}


def load_variance_estimate(path: str) -> Tuple[Dict[str, float], Dict[str, Any]]:
    """
    Load a variance-estimate YAML file and extract point_estimates for all 7 facets
    plus aggregate metadata (max_dispersion, routing_hint, flags).

    Try pyyaml first (full parsing); on ImportError fall back to _fallback_load_variance_estimate.
    The fallback handles the fixed block shape defined in variance-estimate.md.

    Returns: (facets, meta) where
      facets = {facet_name: point_estimate_float, ...}
      meta = {max_dispersion: float, routing_hint: str, flags: list}
    """
    try:
        import yaml
        _yaml_available = True
    except ImportError:
        _yaml_available = False

    if not _yaml_available:
        return _fallback_load_variance_estimate(path)

    try:
        import yaml
        with open(path) as f:
            content = f.read()

        # Extract the YAML block labeled flight-model-variance-estimate
        block_match = re.search(
            r"```ya?ml\s*\nflight-model-variance-estimate:(.*?)```",
            content,
            re.DOTALL,
        )
        if block_match:
            block_text = "flight-model-variance-estimate:" + block_match.group(1)
        else:
            # Try parsing the entire file as YAML (sample file is pure YAML)
            block_text = content

        data = yaml.safe_load(block_text)

        if not isinstance(data, dict):
            raise ValueError("YAML root is not a mapping")

        # Navigate to the block
        block = data.get("flight-model-variance-estimate", data)
        if not isinstance(block, dict):
            raise ValueError("No flight-model-variance-estimate key found")

        facets_raw = block.get("facets", {})
        facets: Dict[str, float] = {}
        FACET_NAMES = [
            "strategic_value", "blast_radius", "irreversibility", "exposure",
            "containment_posture", "detection_speed", "recovery_options",
        ]
        for name in FACET_NAMES:
            entry = facets_raw.get(name, {})
            if isinstance(entry, dict):
                facets[name] = float(entry.get("point_estimate", 0.5))
            elif isinstance(entry, (int, float)):
                facets[name] = float(entry)
            else:
                facets[name] = 0.5  # defensive default

        aggregate = block.get("aggregate", {})
        max_dispersion = float(aggregate.get("max_dispersion", 0.0))
        routing_hint = aggregate.get("consumer_routing_hint", "low-uncertainty")
        flags = block.get("flags", []) or []

        return facets, {"max_dispersion": max_dispersion, "routing_hint": routing_hint, "flags": flags}

    except Exception:
        # Fall through to fallback parser
        return _fallback_load_variance_estimate(path)


# ---------------------------------------------------------------------------
# CLI REPORT FORMATTING
# ---------------------------------------------------------------------------

def _format_report(result: Dict[str, Any], input_path: str = "") -> str:
    """Produce human-readable text report from flight model result."""
    sep = "─" * 72
    inp = result["inputs"]
    unc = result["uncertainty"]

    # Force summary table
    lines = [
        sep,
        "  D-WIRE AUTONOMY FLIGHT MODEL — RESULT",
        sep,
        f"  Source:   {input_path or 'stdin'}",
        "",
        "  FORCES",
        f"    W (Gravity)  = blast_radius × exposure × irreversibility",
        f"               = {inp['blast_radius']:.3f} × {inp['exposure']:.3f} × {inp['irreversibility']:.3f}",
        f"               = {result['W']:.3f}",
        "",
        f"    L (Lift)     = mean(containment, detection_speed, recovery_options)",
        f"               = mean({inp['containment_posture']:.3f}, {inp['detection_speed']:.3f}, {inp['recovery_options']:.3f})",
        f"               = {result['L']:.3f}",
        "",
        f"    T (Thrust)   = strategic_value × λ",
        f"               = {inp['strategic_value']:.3f} × {inp['lam']:.3f}",
        f"               = {result['T']:.3f}",
        "",
        f"    D (Drag)     = {result['D']:.3f}   (overhead fraction from drag-report)",
        "",
        "  ENVELOPE",
        f"    {result['envelope'].upper():<20} band={result['band']}",
        f"    Binding constraint: {result['binding_constraint']}",
        "",
        "  UNCERTAINTY",
        f"    max_dispersion  = {unc['max_dispersion']:.3f}",
        f"    routing_hint    = {unc['routing_hint']}",
        "",
        "  RECOMMENDED ACTION",
    ]

    # Word-wrap the action text at 70 chars
    action = result["recommended_action"]
    words = action.split()
    current_line = "    "
    for word in words:
        if len(current_line) + len(word) + 1 > 72:
            lines.append(current_line.rstrip())
            current_line = "    " + word + " "
        else:
            current_line += word + " "
    if current_line.strip():
        lines.append(current_line.rstrip())

    lines.append(sep)
    return "\n".join(lines)


# ---------------------------------------------------------------------------
# CLI ENTRY POINT
# ---------------------------------------------------------------------------

def _parse_args(argv=None):
    """Minimal argparse-free CLI argument parser (stdlib only)."""
    args = {
        "input": None,
        "lam": None,
        "drag": None,
        "json": False,
    }
    argv = argv or sys.argv[1:]
    i = 0
    while i < len(argv):
        a = argv[i]
        if a in ("--input", "-i") and i + 1 < len(argv):
            args["input"] = argv[i + 1]
            i += 2
        elif a in ("--lambda", "--lam") and i + 1 < len(argv):
            args["lam"] = float(argv[i + 1])
            i += 2
        elif a in ("--drag", "-d") and i + 1 < len(argv):
            args["drag"] = float(argv[i + 1])
            i += 2
        elif a in ("--json", "-j"):
            args["json"] = True
            i += 1
        elif a in ("--help", "-h"):
            print(__doc__)
            sys.exit(0)
        else:
            # Positional: treat as input path
            if args["input"] is None and not a.startswith("-"):
                args["input"] = a
            i += 1
    return args


def main(argv=None):
    args = _parse_args(argv)

    # Read input (file or stdin)
    if args["input"]:
        path = args["input"]
        facets, meta = load_variance_estimate(path)
    else:
        # stdin — write to temp file for parsing
        import tempfile
        content = sys.stdin.read()
        with tempfile.NamedTemporaryFile(mode="w", suffix=".yaml", delete=False) as tmp:
            tmp.write(content)
            tmp_path = tmp.name
        try:
            facets, meta = load_variance_estimate(tmp_path)
            path = "<stdin>"
        finally:
            os.unlink(tmp_path)

    # Resolve drag
    drag = args["drag"] if args["drag"] is not None else get_default_drag()
    lam = args["lam"] if args["lam"] is not None else LAMBDA_DEFAULT

    fm = FlightModel(
        strategic_value=facets["strategic_value"],
        blast_radius=facets["blast_radius"],
        irreversibility=facets["irreversibility"],
        exposure=facets["exposure"],
        containment_posture=facets["containment_posture"],
        detection_speed=facets["detection_speed"],
        recovery_options=facets["recovery_options"],
        lam=lam,
        drag=drag,
        max_dispersion=meta.get("max_dispersion", 0.0),
        routing_hint=meta.get("routing_hint", "low-uncertainty"),
        flags=meta.get("flags", []),
    )
    result = fm.compute()

    if args["json"]:
        # Make envelope JSON-serializable
        out = dict(result)
        out["envelope"] = result["envelope"].value
        print(json.dumps(out, indent=2))
    else:
        print(_format_report(result, input_path=args["input"] or "<stdin>"))


if __name__ == "__main__":
    main()
