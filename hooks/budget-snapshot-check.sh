#!/usr/bin/env bash
# budget-snapshot-check.sh
#
# SessionStart hook - ambient budget state from codeburn, with guidance that
# depends on where in the cycle you are.
#
# Why this exists: budget state was being polled by two recurring Google
# Calendar reminders, deleted 2026-07-29. They were dumb timers. They fired
# whether or not spend was near a threshold, could not say how much was left,
# and went wrong the moment a plan or reset window changed.
#
# THE THING THIS HOOK GOT WRONG ON ITS FIRST DAY, now fixed:
#
#   v1 printed "that is a throttle signal, not a spend-it-down signal" on every
#   breach, at every point in the cycle. Brien corrected that the same day:
#   protect is cycle-position-dependent, and getting it backwards is expensive
#   in BOTH directions.
#
#     Early and mid cycle, a breach IS a throttle signal. Burning to zero on
#     day 1 costs the remaining six days. That is 2026-07-19: $1,321.80 in a
#     day, bucket at 99% by 07-20, two days frozen.
#
#     Late cycle, the rule INVERTS. Unspent headroom does not roll over, it
#     evaporates. On 2026-07-29 Brien left 50% of Fable and 50% of All-Models
#     on the floor at cutover, having started too late. At T-minus-18h nothing
#     is protected by restraint, because the bucket resets before the
#     consequence lands.
#
#   So the guidance branches on hours-to-reset. Importing the 07-19 lesson into
#   the end-of-cycle window is itself the error.
#
# Lead time is the point. A drain prompt at T-3h cannot be acted on at
# Brien-scale, which is why the window is 24h and why the out-of-band trigger
# (cycle-drain-window-check.sh, launchd) exists: a SessionStart hook only fires
# if a session starts, and the whole problem is the sessions that do not.
#
# WHAT THIS HOOK DOES NOT DO, deliberately:
#
#   It does not invent a cycle percentage from codeburn. codeburn's "weekly" is
#   a ROLLING 7 DAYS, not the Wednesday-anchored bucket. Reporting one as the
#   other is the error the 2026-07-29 sweep made. Both windows print, labelled.
#
#   It does not resolve the anchor itself. That parse lives once, in
#   Core/products/org-design-tooling/src/resolve-cycle-anchor.sh, so there is
#   exactly one place the cycle can be wrong.
#
#   It does not block. Every failure path exits 0.
#
# Bypass: BUDGET_SNAPSHOT_CHECK_BYPASSED=1
#
# Created 2026-07-29. Cycle-phase branching added the same day per Brien direct.

set -u

[ "${BUDGET_SNAPSHOT_CHECK_BYPASSED:-0}" = "1" ] && exit 0

CODEBURN="${CODEBURN_BIN:-/opt/homebrew/bin/codeburn}"
command -v "$CODEBURN" >/dev/null 2>&1 || CODEBURN="$(command -v codeburn 2>/dev/null)"

WS="${WORKSPACES_ROOT:-$HOME/Workspaces}"
RESOLVER="$WS/Core/products/org-design-tooling/src/resolve-cycle-anchor.sh"

if [ -z "${CODEBURN:-}" ] || [ ! -x "$CODEBURN" ]; then
  printf '\n%s\n' "BUDGET: codeburn not found. Install it, or set CODEBURN_BIN."
  printf '%s\n' "        Until then no session has a spend reading. This is not a clean state."
  exit 0
fi

TMPDIR_B="$(mktemp -d 2>/dev/null)" || exit 0
trap 'rm -rf "$TMPDIR_B"' EXIT

# Each codeburn call takes roughly 3s (it rescans transcripts). Run the two we
# need concurrently; serial would put this hook near 7s on its own, and a slow
# SessionStart hook gets disabled by whoever is waiting for it.
( "$CODEBURN" budget --check >"$TMPDIR_B/budget" 2>/dev/null; echo $? >"$TMPDIR_B/budget.rc" ) &
BPID=$!
( [ -x "$RESOLVER" ] && "$RESOLVER" >"$TMPDIR_B/cycle" 2>/dev/null ) &
SPID=$!
wait "$BPID" "$SPID" 2>/dev/null

BUDGET_OUT="$(cat "$TMPDIR_B/budget" 2>/dev/null)"
BUDGET_RC="$(cat "$TMPDIR_B/budget.rc" 2>/dev/null || echo 0)"
CYCLE_JSON="$(cat "$TMPDIR_B/cycle" 2>/dev/null)"

if [ -z "$BUDGET_OUT" ] && [ -z "$CYCLE_JSON" ]; then
  printf '\n%s\n' "BUDGET: codeburn returned nothing. Run 'codeburn doctor' to see why."
  exit 0
fi

printf '\n%s\n\n' "BUDGET (codeburn is the instrument, the dashboard is the anchor)"

# --- Tripwires: codeburn's own daily / rolling-7day budgets -----------------
# Reprinted with the window named, because "weekly" here means rolling 7 days
# and reading it as cycle-percent is the documented failure mode.
if [ -n "$BUDGET_OUT" ]; then
  printf '%s\n' "$BUDGET_OUT" | while IFS= read -r line; do
    case "$line" in
      *daily:*)  printf '  today (24h)       %s\n' "$(printf '%s' "$line" | sed 's/^ *daily: *//')" ;;
      *weekly:*) printf '  rolling 7 days    %s\n' "$(printf '%s' "$line" | sed 's/^ *weekly: *//')" ;;
    esac
  done
fi

# --- Cycle position, and the guidance that depends on it --------------------
BUDGET_RC="$BUDGET_RC" python3 - <<'PY' "$CYCLE_JSON" 2>/dev/null
import json, os, sys

raw = sys.argv[1] if len(sys.argv) > 1 else ""
breached = os.environ.get("BUDGET_RC", "0") == "1"

try:
    c = json.loads(raw) if raw.strip() else {}
except ValueError:
    c = {}

if not c.get("ok"):
    err = c.get("error", "cycle resolver produced no output")
    print()
    print("  weekly cycle      UNRESOLVED: %s" % err)
    print("                    Capture the displayed 'Resets [day] [time]' and record it in")
    print("                    the Current cycle line. Without it there is no cycle position,")
    print("                    and the guidance below cannot be trusted either way.")
    if breached:
        print()
        print("  TRIPWIRE BREACHED on a rolling window. Cannot say whether that means")
        print("  throttle or drain without knowing hours-to-reset. Resolve the anchor first.")
    sys.exit(0)

phase = c["phase"]
to_reset = c["hours_to_reset"]
print()
print("  weekly cycle      next reset %s" % c["next_reset_human"])
print("                    %.0fh elapsed of 168h (%.0f%%), %.0fh to reset"
      % (c["hours_elapsed"], c["pct_elapsed"], to_reset))

if c.get("rolled_weeks"):
    n = c["rolled_weeks"]
    print()
    print("  STALE ANCHOR      recorded reset had already passed; rolled forward %d %s."
          % (n, "week" if n == 1 else "weeks"))
    print("                    Nobody has captured the dashboard in that time, and the anchor")
    print("                    is mobile. Read the displayed 'Resets [day] [time]' and record it.")

print()
if phase == "drain":
    print("  DRAIN WINDOW      %.0fh to reset. Unspent headroom does NOT roll over." % to_reset)
    print("                    It evaporates. On 2026-07-29 half of both Fable and All-Models")
    print("                    was left on the floor at cutover by starting too late.")
    print("                    Queue and drain real work into the expiring capacity now.")
    if breached:
        print()
        print("                    The breached tripwire above is a ROLLING-7-DAY reading and")
        print("                    is not a stop signal here. Do not import the 2026-07-19")
        print("                    throttle lesson into the end of a cycle.")
elif breached:
    print("  TRIPWIRE BREACHED. At %.0fh to reset, this IS a throttle signal, not a" % to_reset)
    print("  spend-it-down signal. Burning the bucket to zero this early costs the rest")
    print("  of the cycle: 2026-07-19 was $1,321.80 in a day and two frozen days after.")
else:
    print("  Mid-cycle, no tripwire breached. Protect headroom; the drain-window")
    print("  guidance flips on at %.0fh to reset." % c.get("drain_window_h", 24))

# Forfeit ladder (budget-policy.yaml amendment 4, ratified 2026-08-04). This
# block STATES the exception's conditions so no session judges from memory;
# it enforces nothing. The rungs here mirror the policy file: change both
# together or the statement becomes the lie the signal warned about.
print()
if to_reset <= 72:
    rung = 15 if to_reset <= 24 else (30 if to_reset <= 48 else 50)
    print("  FORFEIT LADDER    active rung: at %.0fh to reset, Fable on engagement work" % to_reset)
    print("                    is permitted ONLY if the dashboard shows %d%% or more of" % rung)
    print("                    the weekly bucket still available (ladder: 72h needs 50%,")
    print("                    48h needs 30%, 24h needs 15%) AND no queued Brien-product")
    print("                    work would consume it. Bucket percent is DASHBOARD-OBSERVED")
    print("                    ONLY, never inferred from codeburn dollars.")
    # Count from the board's own generated summary line ("N ready, ..."); the
    # row format is not stable and a wrong 0 here would be a false all-clear.
    import re as _re
    try:
        ready_path = os.path.expanduser("~/Workspaces/.intent/queue/READY.md")
        m = _re.search(r"(\d+)\s+ready\b", open(ready_path).read())
        if m:
            print("                    Ready board reports %s ready items; the exception needs" % m.group(1))
            print("                    none of them to be bucket-consuming product work.")
        else:
            print("                    Ready board count unreadable; check .intent/queue/READY.md")
            print("                    yourself for queued product work before dispatching.")
    except OSError:
        print("                    Ready board missing; check the quartermaster queue yourself")
        print("                    for queued product work before dispatching.")
    print("                    Policy: Workspaces/.intent/queue/budget-policy.yaml, amendment 4.")
else:
    print("  FORFEIT LADDER    dormant: first rung opens at 72h to reset (72h needs 50%")
    print("                    available, 48h needs 30%, 24h needs 15%; policy amendment 4).")
PY

printf '\n'
printf '  %s\n' "Read these correctly:"
printf '  %s\n' "- The rolling 7 days above is NOT the cycle. It is a tripwire window."
printf '  %s\n' "  Cycle percent consumed comes from the dashboard only."
printf '  %s\n' "- Dollars are API-equivalent notional on a Max subscription, not"
printf '  %s\n' "  out-of-pocket. They measure bucket draw, not money leaving an account."
printf '  %s\n' "- Fable draws the weekly bucket at roughly 4.8x Opus per token. That cuts"
printf '  %s\n' "  both ways: worst thing to fan out early, best thing to drain late."
printf '  %s\n' "- WIDTH IS THE CHEAP MODE. Measured: parallel lanes cost \$0.111/1K output"
printf '  %s\n' "  against \$0.212/1K for long serial work on the same model. A throttle"
printf '  %s\n' "  signal bounds the RATE of new work, it does NOT mean narrow the fan-out."
printf '  %s\n' "  Capping width pushes work into the EXPENSIVE serial mode. Source: the"
printf '  %s\n' "  header of Core/products/org-design-tooling/hooks/burn-rate-dispatch-gate.sh,"
printf '  %s\n' "  which deliberately bounds rate and explicitly refuses to cap width."
printf '  %s\n' "- A budget signal is NEVER a reason to silently deliver less work. If cost"
printf '  %s\n' "  would force a smaller scope than asked, SAY SO and get a ruling. Trading"
printf '  %s\n' "  completeness for cost without telling Brien takes a decision that is his."
printf '  %s\n' "  Added 2026-08-09: a session read the tripwire above, concluded it argued"
printf '  %s\n' "  against fanning out, ran solo, and delivered a partial audit. Both halves"
printf '  %s\n' "  of that were wrong: parallel was the cheaper mode, and the trade was never"
printf '  %s\n' "  surfaced."
printf '  %s\n' "- Anchor source: /Users/brien/Workspaces/Core/reference/project-index/usage-tracking.md"
printf '\n'

exit 0
