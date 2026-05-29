#!/usr/bin/env python3
"""
drag_dashboard.py — Aggregate-Drag instrument for the behavioral-enforcement layer.

WHY THIS EXISTS
  Every behavioral-discipline hook (autonomy-grant, closure-discipline, etc.) was
  added reactively and filed as a `status: resolved` control-upgrade. Each emits
  per-hook telemetry, but NOTHING rolls them up. The sum is unmeasured Drag — the
  exact force the autonomy-flight-model names (W/T/L/D) but its ratification backlog
  does not instrument. This tool makes the accretion visible.

  Friction backlog: Core/frameworks/intent/.intent/signals/SIG-2026-05-29-friction-*
  Designed fix:     Core/frameworks/intent/spec/autonomy-flight-model-v1-DRAFT.md

WHAT IT MEASURES
  A. Static inventory (filesystem — always available):
       - wired hooks (count, KB, mtime → accretion timeline)
       - lexical CHECK count in the autonomy Stop hook (growth tracker)
       - 6-layer enforcement-stack depth per drift class
  B. Runtime Drag (telemetry logs — if present):
       - invocation volume (every response pays this)
       - block rate = blocks / invocations  (how often the hook ACTUALLY acts;
         a low number means the hook is nearly pure overhead)
       - per-check trigger distribution (a never-firing check is dead weight)
       - FP-proxy (fp_suppressed) and bypass rate (high bypass = mis-scoped gate)
  C. Cap-guard (the accretion catch-net):
       - reads lexical-layer-freeze.yaml; flags any CHECK beyond the frozen
         baseline that is not a sanctioned addition (with debit + sunset).

USAGE
    python3 drag_dashboard.py [--since YYYY-MM-DD] [--json OUT.json]
                              [--hooks-dir DIR] [--logs-dir DIR] [--audit-dir DIR]
                              [--settings PATH] [--freeze PATH]

OUTPUT
    - stdout: human-readable Drag report
    - --json: machine-readable rollup (default: drag-report.json beside this file)

Stdlib only. Fails soft on missing/malformed inputs — same defensive posture as the
hooks it measures. A missing telemetry log degrades to "no runtime data"; the static
inventory still renders.
"""
from __future__ import annotations

import argparse
import glob
import json
import os
import re
import sys
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path

# ----------------------------------------------------------------------------- paths
HOME = Path(os.path.expanduser("~"))
DEFAULT_HOOKS_DIR = Path("/Users/brien/Workspaces/Core/frameworks/intent/hooks")
DEFAULT_LOGS_DIR = HOME / ".claude" / "logs"
DEFAULT_AUDIT_DIR = HOME / ".claude" / "audit"
DEFAULT_SETTINGS = HOME / ".claude" / "settings.json"
DEFAULT_FREEZE = DEFAULT_HOOKS_DIR / "lexical-layer-freeze.yaml"

TS_RE = re.compile(r"(\d{4}-\d{2}-\d{2})[T ](\d{2}:\d{2}:\d{2})")
CHECK_DEF_RE = re.compile(r"\bCHECK\s*([0-9]+)\b")
CAUGHT_RE = re.compile(r"CHECK(\d+)-CAUGHT")
AUDIT_TS_RE = re.compile(r"^\[(\d{4}-\d{2}-\d{2})T")


def _parse_date(s):
    try:
        return datetime.strptime(s, "%Y-%m-%d").date()
    except Exception:
        return None


def _iter_jsonl(path):
    """Yield parsed JSON objects from a JSONL file, skipping malformed lines."""
    if not path or not Path(path).exists():
        return
    try:
        with open(path, "r", errors="replace") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                try:
                    yield json.loads(line)
                except Exception:
                    continue
    except Exception:
        return


def _row_date(obj):
    ts = obj.get("ts") or obj.get("timestamp") or ""
    m = TS_RE.search(str(ts))
    return _parse_date(m.group(1)) if m else None


# ----------------------------------------------------------------- A. static inventory
def static_inventory(hooks_dir, settings_path):
    """Filesystem + settings.json view of the enforcement layer."""
    out = {"hooks": [], "wired": {}, "lexical_checks": None, "errors": []}

    # Hook files (count / size / mtime → accretion timeline)
    try:
        for p in sorted(Path(hooks_dir).glob("*.sh")):
            st = p.stat()
            out["hooks"].append({
                "name": p.name,
                "kb": round(st.st_size / 1024, 1),
                "mtime": datetime.fromtimestamp(st.st_mtime, tz=timezone.utc)
                .date().isoformat(),
            })
    except Exception as e:
        out["errors"].append(f"hooks-dir: {e}")

    # settings.json wiring (event → [hook scripts])
    try:
        s = json.loads(Path(settings_path).read_text())
        for evt, arr in (s.get("hooks") or {}).items():
            names = []
            for entry in arr:
                for hk in entry.get("hooks", []):
                    names += re.findall(r"[\w-]+\.sh", hk.get("command", ""))
            out["wired"][evt] = names
    except Exception as e:
        out["errors"].append(f"settings: {e}")

    # Live lexical CHECK count in the autonomy Stop hook
    stop_hook = Path(hooks_dir) / "autonomy-grant-stop-check.sh"
    try:
        txt = stop_hook.read_text(errors="replace")
        nums = [int(n) for n in CHECK_DEF_RE.findall(txt)]
        out["lexical_checks"] = max(nums) if nums else 0
    except Exception as e:
        out["errors"].append(f"stop-hook: {e}")

    out["hook_count"] = len(out["hooks"])
    out["total_kb"] = round(sum(h["kb"] for h in out["hooks"]), 1)
    return out


# ------------------------------------------------------------------- B. runtime drag
def runtime_drag(logs_dir, audit_dir, since):
    """Telemetry rollup: volume, fire rate, block rate, FP-proxy, bypass rate."""
    logs_dir, audit_dir = Path(logs_dir), Path(audit_dir)
    out = {
        "window": {"since": since.isoformat() if since else None,
                   "first": None, "last": None},
        "autonomy_stop": {"invocations": 0, "by_check": Counter(),
                          "fp_suppressed": 0, "dispatch_present": 0},
        "blocks": Counter(),         # CHECKn-CAUGHT events from audit logs
        "blocks_by_day": defaultdict(Counter),
        "detections": Counter(),     # per audit-log file → caught lines
        "bypasses": Counter(),
        "other_logs": {},
        "errors": [],
    }

    dates_seen = []

    # --- autonomy-stop-check.jsonl: the per-response tax ledger
    stop_jsonl = logs_dir / "autonomy-stop-check.jsonl"
    for obj in _iter_jsonl(stop_jsonl):
        d = _row_date(obj)
        if d:
            dates_seen.append(d)
        if since and d and d < since:
            continue
        chk = str(obj.get("check", "1-4"))
        # "main" rows (checks 1-4) carry bare_match/soft_queue_*; numbered rows are 5/6
        if "check" in obj:
            out["autonomy_stop"]["by_check"][f"check{chk}_runs"] += 1
            if obj.get("trigger"):
                out["autonomy_stop"]["by_check"][f"check{chk}_trigger"] += 1
            if obj.get("fp_suppressed"):
                out["autonomy_stop"]["fp_suppressed"] += 1
        else:
            out["autonomy_stop"]["by_check"]["check1-4_runs"] += 1
            for k in ("bare_match", "soft_queue_trigger", "next_stage"):
                if obj.get(k):
                    out["autonomy_stop"]["by_check"][f"{k}"] += 1
        if obj.get("dispatch"):
            out["autonomy_stop"]["dispatch_present"] += 1
        out["autonomy_stop"]["invocations"] += 1

    # --- audit detection logs: the ACTUAL blocks (where the hook changed behavior)
    try:
        for ap in sorted(audit_dir.glob("*.log")):
            caught = 0
            try:
                for line in ap.read_text(errors="replace").splitlines():
                    md = AUDIT_TS_RE.match(line)
                    d = _parse_date(md.group(1)) if md else None
                    if d:
                        dates_seen.append(d)
                    if since and d and d < since:
                        continue
                    mc = CAUGHT_RE.search(line)
                    if mc:
                        out["blocks"][f"CHECK{mc.group(1)}"] += 1
                        if d:
                            out["blocks_by_day"][d.isoformat()][f"CHECK{mc.group(1)}"] += 1
                        caught += 1
                    elif "CAUGHT" in line or "BLOCK" in line:
                        caught += 1
            except Exception as e:
                out["errors"].append(f"{ap.name}: {e}")
            if caught:
                out["detections"][ap.name] = caught
    except Exception as e:
        out["errors"].append(f"audit-dir: {e}")

    # --- bypass ledgers (high bypass rate = mis-scoped gate, per friction-05)
    for name in ("native-connector-bypass.log", "build-intake-bypasses.log"):
        p = logs_dir / name
        if not p.exists():
            p = audit_dir / name
        try:
            if p.exists():
                n = sum(1 for ln in p.read_text(errors="replace").splitlines()
                        if ln.strip())
                out["bypasses"][name] = n
        except Exception as e:
            out["errors"].append(f"{name}: {e}")

    # --- other JSONL volume (signal-recorder etc.)
    for p in logs_dir.glob("*.jsonl"):
        if p.name == "autonomy-stop-check.jsonl":
            continue
        out["other_logs"][p.name] = sum(1 for _ in _iter_jsonl(p))

    if dates_seen:
        out["window"]["first"] = min(dates_seen).isoformat()
        out["window"]["last"] = max(dates_seen).isoformat()
    out["total_blocks"] = sum(out["blocks"].values())
    inv = out["autonomy_stop"]["invocations"]
    out["block_rate"] = round(out["total_blocks"] / inv, 4) if inv else None
    return out


# --------------------------------------------------------------------- C. cap-guard
def cap_guard(freeze_path, live_checks):
    """The accretion catch-net: live CHECK count vs frozen baseline."""
    out = {"freeze_found": False, "baseline": None, "live": live_checks,
           "sanctioned": 0, "status": "unknown", "rule": None}
    try:
        txt = Path(freeze_path).read_text(errors="replace")
        out["freeze_found"] = True
        m = re.search(r"frozen_at_check:\s*(\d+)", txt)
        if m:
            out["baseline"] = int(m.group(1))
        # count sanctioned_additions list items (lines beginning "- check:" under it)
        seg = txt.split("sanctioned_additions:", 1)
        if len(seg) == 2:
            block = seg[1].split("\nrule:", 1)[0]
            out["sanctioned"] = len(re.findall(r"^\s*-\s", block, re.M))
        rule = re.search(r"no_new_check_without:(.*?)(\n\s*\w+:|\Z)", txt, re.S)
        if rule:
            items = []
            for x in rule.group(1).splitlines():
                x = x.strip()
                if x.startswith("-"):
                    v = x.lstrip("- ").split("#", 1)[0].strip()  # drop inline comment
                    if v:
                        items.append(v)
            out["rule"] = items
    except FileNotFoundError:
        out["status"] = "NO-FREEZE-REGISTRY"
        return out
    except Exception as e:
        out["status"] = f"error: {e}"
        return out

    if out["baseline"] is None or live_checks is None:
        out["status"] = "indeterminate"
    elif live_checks <= out["baseline"] + out["sanctioned"]:
        out["status"] = "WITHIN-FREEZE"
    else:
        out["status"] = "ACCRETION-DRIFT"  # CHECK added without sanction
    return out


# ------------------------------------------------------------------------- rendering
def render(inv, rt, guard):
    L = []
    p = L.append
    p("=" * 78)
    p("  AGGREGATE-DRAG DASHBOARD — behavioral-enforcement layer")
    p("  (SIG-2026-05-29-friction-00 · autonomy-flight-model W/T/L/D · D-force)")
    p("=" * 78)

    # A. static inventory
    p("\n── A. STATIC INVENTORY (filesystem) " + "─" * 40)
    p(f"  Wired hook scripts : {inv['hook_count']}   total {inv['total_kb']} KB")
    p(f"  Lexical CHECKs live: {inv['lexical_checks']}  (autonomy-grant-stop-check.sh)")
    for evt, names in inv.get("wired", {}).items():
        p(f"    {evt:<13}: {len(names)} hook(s)")
    # accretion timeline — the 5 most recently grown hooks
    timeline = sorted(inv["hooks"], key=lambda h: h["mtime"], reverse=True)[:6]
    p("  Accretion (most recently modified):")
    for h in timeline:
        p(f"    {h['mtime']}  {h['kb']:>6} KB  {h['name']}")

    # B. runtime drag
    p("\n── B. RUNTIME DRAG (telemetry) " + "─" * 45)
    w = rt["window"]
    if rt["autonomy_stop"]["invocations"] == 0 and rt["total_blocks"] == 0:
        p("  No runtime telemetry in window (logs absent/empty).")
    else:
        p(f"  Window           : {w['first']} → {w['last']}"
          + (f"  (since {w['since']})" if w["since"] else ""))
        inv_n = rt["autonomy_stop"]["invocations"]
        p(f"  Stop-hook runs   : {inv_n:,}   ← every response pays this tax")
        br = rt["block_rate"]
        p(f"  Total blocks     : {rt['total_blocks']:,}")
        if br is not None:
            pct = br * 100
            verdict = ("nearly pure overhead" if pct < 2 else
                       "low-yield" if pct < 10 else "active")
            p(f"  BLOCK RATE       : {pct:.2f}%   ({verdict} — "
              f"{100 - pct:.1f}% of runs changed nothing)")
        p(f"  FP-suppressed    : {rt['autonomy_stop']['fp_suppressed']:,}  "
          "(built-in false-positive proxy; true FP needs manual labels)")
        if rt["blocks"]:
            p("  Blocks by check  : " +
              ", ".join(f"{k}={v}" for k, v in sorted(rt["blocks"].items())))
        if rt["detections"]:
            p("  Detections/log   :")
            for name, n in sorted(rt["detections"].items(), key=lambda x: -x[1]):
                p(f"      {n:>5}  {name}")
        if rt["bypasses"]:
            p("  Bypass ledgers   : " +
              ", ".join(f"{k}={v}" for k, v in rt["bypasses"].items()) +
              "   (high = mis-scoped gate, friction-05)")
        if rt["other_logs"]:
            p("  Other log volume : " +
              ", ".join(f"{k}={v:,}" for k, v in rt["other_logs"].items()))

    # C. cap-guard
    p("\n── C. CAP-GUARD (accretion catch-net) " + "─" * 38)
    g = guard
    flag = {"WITHIN-FREEZE": "✓", "ACCRETION-DRIFT": "✗ DRIFT",
            "NO-FREEZE-REGISTRY": "⚠ no registry"}.get(g["status"], "?")
    p(f"  Status           : {flag}  ({g['status']})")
    p(f"  Baseline / live  : CHECK {g['baseline']} frozen  vs  CHECK {g['live']} live"
      f"  (+{g['sanctioned']} sanctioned)")
    if g["status"] == "ACCRETION-DRIFT":
        p("  ►► A CHECK was added past the frozen baseline without a sanctioned")
        p("     entry (Drag-budget debit + sunset clause). Add it to")
        p("     lexical-layer-freeze.yaml:sanctioned_additions or retire the check.")
    if g.get("rule"):
        p("  No new CHECK without: " + " · ".join(g["rule"]))

    p("\n" + "=" * 78)
    p("  Read with: SIG-2026-05-29-friction-00 (synthesis) · cap the lexical layer,")
    p("  ship Layer 4.2 (structural), sunset CHECKs 1-6 on a MEASURED schedule.")
    p("=" * 78)
    return "\n".join(L)


def main(argv=None):
    ap = argparse.ArgumentParser(description="Aggregate-Drag dashboard for the enforcement layer.")
    ap.add_argument("--since", type=_parse_date, default=None,
                    help="only count telemetry on/after YYYY-MM-DD")
    ap.add_argument("--hooks-dir", default=str(DEFAULT_HOOKS_DIR))
    ap.add_argument("--logs-dir", default=str(DEFAULT_LOGS_DIR))
    ap.add_argument("--audit-dir", default=str(DEFAULT_AUDIT_DIR))
    ap.add_argument("--settings", default=str(DEFAULT_SETTINGS))
    ap.add_argument("--freeze", default=str(DEFAULT_FREEZE))
    ap.add_argument("--json", default=str(Path(__file__).with_name("drag-report.json")))
    args = ap.parse_args(argv)

    inv = static_inventory(args.hooks_dir, args.settings)
    rt = runtime_drag(args.logs_dir, args.audit_dir, args.since)
    guard = cap_guard(args.freeze, inv.get("lexical_checks"))

    report = render(inv, rt, guard)
    print(report)

    rollup = {
        "generated_input_window": rt["window"],
        "static_inventory": inv,
        "runtime_drag": {k: (dict(v) if isinstance(v, (Counter, defaultdict)) else v)
                         for k, v in rt.items()},
        "cap_guard": guard,
    }
    # normalize nested counters
    rollup["runtime_drag"]["autonomy_stop"]["by_check"] = dict(
        rt["autonomy_stop"]["by_check"])
    rollup["runtime_drag"]["blocks"] = dict(rt["blocks"])
    rollup["runtime_drag"]["blocks_by_day"] = {k: dict(v)
                                               for k, v in rt["blocks_by_day"].items()}
    rollup["runtime_drag"]["detections"] = dict(rt["detections"])
    rollup["runtime_drag"]["bypasses"] = dict(rt["bypasses"])
    try:
        Path(args.json).write_text(json.dumps(rollup, indent=2, default=str))
        print(f"\n[machine rollup → {args.json}]")
    except Exception as e:
        print(f"\n[could not write json rollup: {e}]", file=sys.stderr)

    # exit non-zero on accretion drift so this can gate CI / pre-commit later
    return 2 if guard.get("status") == "ACCRETION-DRIFT" else 0


if __name__ == "__main__":
    sys.exit(main())
