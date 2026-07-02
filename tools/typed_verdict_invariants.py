#!/usr/bin/env python3
"""
typed_verdict_invariants.py — repo-local chain_audit invariant for typed
evaluation verdicts (SIG-2026-06-09-typed-evaluation-verdicts).

WHY THIS EXISTS
  The Observe-loop LLM-as-Judge protocol was amended 2026-06-09
  (spec/event-catalog.md §Verdict Typing; spec/typed-evaluation-verdicts.md):
  an `observation.evaluated` verdict graded against the spec's OWN prose
  criteria (`criteria_origin: self`, same lineage, same repo) is a test-grade
  instrument and MUST NOT be consumed at UAT-grade authority — it cannot close
  a spec. The amendment is write-through (emitters populate the fields; the
  Observe-loop steps refuse closure on a self pass). This module is the named
  CATCH-NET — `INV-INTENT-NO-SELF-GRADED-CLOSURE` — so the rule is machine-
  checked in the events stream, not only asserted in spec prose.

  Per spec/typed-evaluation-verdicts.md §5 the catch-net may be registered in
  the library-index portfolio OR "a repo-local chain_audit for Core/frameworks/
  intent if one is stood up first." The portfolio product is not present in this
  checkout; this is the repo-local route.

INVARIANT
  INV-INTENT-NO-SELF-GRADED-CLOSURE (two checks, both date-scoped to the
  2026-06-09 amendment so day one fires clean — feedback_invariant_zero_violation_start):

    A. Schema completeness. Every `observation.evaluated` event emitted on or
       after 2026-06-09 carries all three required fields with valid values:
       data.criteria_origin ∈ {self, distilled, derived},
       data.evaluator_model (non-empty), data.evaluator_repo ∈ {same-repo, external}.
       (event-catalog.md §Verdict Typing.) Pre-amendment events are grandfathered
       as criteria_origin:self and are NOT judged here.

    B. No self-graded closure. A post-amendment `observation.evaluated` verdict
       that is CONSUMED AT CLOSURE (verdict pass|conditional_pass AND marked as
       closing a spec at acceptance authority) must have criteria_origin: derived,
       OR be overridden by a `decision.recorded` event referencing it. Otherwise
       it is a self/distilled verdict occupying a gate position → violation.
       (typed-evaluation-verdicts.md §3–5, event-catalog.md L312/L322.)

  Closure-marking: emitter instrumentation for the closure marker is still
  pending (the amendment changed no emitter code). This check reads the closure
  intent from whichever of these the emitter sets on the event's data, matching
  the normative rule rather than a not-yet-frozen field name:
  data.closes_spec is truthy, OR data.authority ∈ {acceptance, uat}, OR
  data.consumed_at == "closure". Until an emitter sets one of these, no event is
  "closing" and Check B is vacuously clean — the honest zero-violation start.

USAGE
  python3 typed_verdict_invariants.py [--events PATH] [--emit-signal] [--json]
  Exit 0 = invariant passes · 1 = one or more violations.

COMPOSES WITH
  - spec/event-catalog.md §Verdict Typing        — the write-through protocol
  - spec/typed-evaluation-verdicts.md            — rationale + this catch-net's name
  - tools/value_term_invariants.py               — sibling invariant-class convention
  - tools/closure_writeboundary_check.py         — adjacent (signal-frontmatter) catch-net
"""
from __future__ import annotations

import argparse
import json
import sys
from datetime import date
from pathlib import Path

# The 2026-06-09 amendment date. ISO date strings compare lexicographically, so
# a "YYYY-MM-DD" prefix comparison is a correct date comparison.
CUTOFF = "2026-06-09"

VALID_ORIGIN = {"self", "distilled", "derived"}
VALID_REPO = {"same-repo", "external"}
CLOSING_VERDICTS = {"pass", "conditional_pass"}

DEFAULT_EVENTS = Path(__file__).resolve().parents[1] / ".intent" / "events" / "events.jsonl"
DEFAULT_SIGNALS_DIR = Path(__file__).resolve().parents[1] / ".intent" / "signals"

INV_ID = "INV-INTENT-NO-SELF-GRADED-CLOSURE"


# ---------------------------------------------------------------------------
# Loading
# ---------------------------------------------------------------------------

def load_events(path: str | Path) -> list[dict]:
    """Parse a JSONL event stream. Blank and unparseable lines are skipped."""
    path = Path(path)
    if not path.exists():
        return []
    events: list[dict] = []
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            events.append(json.loads(line))
        except json.JSONDecodeError:
            continue
    return events


def _event_date(ev: dict) -> str:
    """First 10 chars of the timestamp (YYYY-MM-DD), or '' if absent."""
    ts = ev.get("timestamp") or ev.get("time") or ""
    return str(ts)[:10]


def _is_post_cutoff(ev: dict) -> bool:
    d = _event_date(ev)
    return bool(d) and d >= CUTOFF


def _verdict_id(ev: dict) -> str:
    """Best-effort stable identity for an observation.evaluated verdict."""
    data = ev.get("data") or {}
    return str(data.get("verdict_id") or ev.get("span_id") or ev.get("id") or "")


def _is_closing(ev: dict) -> bool:
    """Is this verdict consumed at acceptance authority (i.e. closes a spec)?"""
    data = ev.get("data") or {}
    if str(data.get("verdict", "")).lower() not in CLOSING_VERDICTS:
        return False
    if data.get("closes_spec"):
        return True
    if str(data.get("authority", "")).lower() in {"acceptance", "uat"}:
        return True
    if str(data.get("consumed_at", "")).lower() == "closure":
        return True
    return False


# ---------------------------------------------------------------------------
# INV-INTENT-NO-SELF-GRADED-CLOSURE
# ---------------------------------------------------------------------------

def invariant_no_self_graded_closure(
    events: list[dict], cutoff: str = CUTOFF
) -> tuple[bool, list[str]]:
    """Return (passed, violations) for the typed-verdict closure invariant.

    Date-scoped to `cutoff` so pre-amendment events (grandfathered as `self`)
    never fire — zero-violation start by construction.
    """
    violations: list[str] = []

    evaluated = [
        e for e in events
        if e.get("event") == "observation.evaluated" and (not cutoff or _event_date(e) >= cutoff)
    ]

    # Index Brien-override decisions by the verdict id they reference.
    overridden: set[str] = set()
    for e in events:
        if e.get("event") != "decision.recorded":
            continue
        data = e.get("data") or {}
        ref = data.get("overrides_verdict") or data.get("overrides")
        if ref and (data.get("override") is not False):
            overridden.add(str(ref))

    for e in evaluated:
        data = e.get("data") or {}
        vid = _verdict_id(e) or "<unidentified>"

        # Check A — schema completeness
        origin = data.get("criteria_origin")
        if origin not in VALID_ORIGIN:
            violations.append(
                f"{INV_ID}/A: observation.evaluated {vid} ({_event_date(e)}) has "
                f"criteria_origin={origin!r} — must be one of {sorted(VALID_ORIGIN)} "
                f"(event-catalog.md §Verdict Typing; a missing/invalid field voids the verdict)."
            )
        if not data.get("evaluator_model"):
            violations.append(
                f"{INV_ID}/A: observation.evaluated {vid} ({_event_date(e)}) is missing "
                f"required field evaluator_model."
            )
        if data.get("evaluator_repo") not in VALID_REPO:
            violations.append(
                f"{INV_ID}/A: observation.evaluated {vid} ({_event_date(e)}) has "
                f"evaluator_repo={data.get('evaluator_repo')!r} — must be one of {sorted(VALID_REPO)}."
            )

        # Check B — no self-graded (or distilled) verdict at closure authority
        if _is_closing(e) and origin != "derived":
            if vid in overridden:
                continue  # a recorded Brien override carries the authority, not the verdict
            violations.append(
                f"{INV_ID}/B: observation.evaluated {vid} ({_event_date(e)}) closes a spec "
                f"at acceptance authority with criteria_origin={origin!r}. Only "
                f"criteria_origin='derived' — or a decision.recorded Brien override "
                f"referencing this verdict — may close a spec (typed-evaluation-verdicts.md §3)."
            )

    return len(violations) == 0, violations


# ---------------------------------------------------------------------------
# Signal emission (honest closure-DoD frontmatter)
# ---------------------------------------------------------------------------

def emit_signal(signals_dir: str | Path, violations: list[str]) -> Path:
    signals_dir = Path(signals_dir)
    signals_dir.mkdir(parents=True, exist_ok=True)
    today = date.today().isoformat()
    path = signals_dir / f"SIG-{INV_ID}-VIOLATION-{today}.md"
    body = f"""---
id: SIG-{INV_ID}-VIOLATION-{today}
product: intent
type: invariant-violation
status: open
created: {today}
invariant: {INV_ID}
upstream_control_path: "spec/event-catalog.md §Verdict Typing (emitters populate criteria_origin/evaluator_model/evaluator_repo; Observe-loop refuses closure on a self pass) + tools/typed_verdict_invariants.py"
catch_mechanism: "tools/typed_verdict_invariants.py {INV_ID} + tools/test_typed_verdict_invariants.py — run in the nightly/overwatch invariant suite"
pipeline_survival: "events.jsonl is an append-only stream read at audit time; no render stage rewrites it. A violation surfaces a self-graded verdict occupying a gate position and does not block execution."
---

# {INV_ID} Violation — {today}

## Violations

"""
    for v in violations:
        body += f"- {v}\n"
    body += f"""
## Required action

Either re-run the closing evaluation with an exterior judge that derives its own
criteria (`criteria_origin: derived`), or record an explicit Brien override
(`decision.recorded` referencing the verdict). A `criteria_origin: self` verdict
is an inner-loop instrument and may not close a spec. Re-run
`python3 tools/typed_verdict_invariants.py` to verify.

*Auto-emitted by typed_verdict_invariants.py {today}.*
"""
    path.write_text(body, encoding="utf-8")
    return path


# ---------------------------------------------------------------------------
# main
# ---------------------------------------------------------------------------

def main(argv=None) -> int:
    ap = argparse.ArgumentParser(
        description="Repo-local typed-verdict chain_audit invariant.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )
    ap.add_argument("--events", default=str(DEFAULT_EVENTS),
                    help="Path to events.jsonl (default: .intent/events/events.jsonl).")
    ap.add_argument("--emit-signal", action="store_true",
                    help="Emit a violation signal to .intent/signals/ on failure.")
    ap.add_argument("--signals-dir", default=str(DEFAULT_SIGNALS_DIR),
                    help="Where to write violation signals.")
    ap.add_argument("--json", action="store_true", help="Output results as JSON.")
    args = ap.parse_args(argv)

    events = load_events(args.events)
    passed, violations = invariant_no_self_graded_closure(events)

    result = {"invariant": INV_ID, "events": str(args.events), "passed": passed,
              "violations": violations}
    if not passed and args.emit_signal:
        result["signal_emitted"] = str(emit_signal(args.signals_dir, violations))

    if args.json:
        print(json.dumps(result, indent=2))
    else:
        print("=" * 78)
        print(f"  TYPED-VERDICT CHAIN-AUDIT — {INV_ID}")
        print(f"  Events: {args.events}")
        print("=" * 78)
        print(f"\n[{'PASS' if passed else 'FAIL'}] {INV_ID}")
        for v in violations:
            print(f"       {v}")
        if passed:
            print("\n✓ No self-graded verdict occupies a closure gate; every post-2026-06-09 "
                  "observation.evaluated carries the required typed-verdict fields.")
        else:
            print(f"\n✗ {len(violations)} violation(s).")

    return 0 if passed else 1


if __name__ == "__main__":
    sys.exit(main())
