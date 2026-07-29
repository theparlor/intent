#!/usr/bin/env bash
# budget-snapshot-check.sh
#
# SessionStart hook - ambient budget state from codeburn.
#
# Why this exists: budget state was being polled by two recurring Google
# Calendar reminders ("Budget check: 18h to weekly reset" and "Budget check:
# reset today 12:59 PM ET"), scheduled out to 2027-04-20. They were dumb
# timers. They fired whether or not spend was anywhere near a threshold, they
# could not say how much was left, and they went wrong the moment a plan or
# reset window changed. The calendar was being used as a polling loop for
# state a real instrument already holds.
#
# codeburn is that instrument. It scans transcripts, so it is surface-
# independent, unlike ~/.claude/headroom.json which is written only by the
# statusline and is blind in every surface that does not render one.
#
# WHAT THIS HOOK DOES NOT DO, deliberately:
#
#   It does not invent a cycle percentage. codeburn's "weekly" is a ROLLING
#   7 DAYS, not the Wednesday-anchored bucket. Reporting one as the other is
#   exactly the error the 2026-07-29 sweep made (it read codeburn's 103%
#   rolling figure as though it were cycle-percent). Both numbers appear
#   here, each labelled with which window it came from.
#
#   It does not hardcode the reset anchor. Per the resolution order in
#   .claude/commands/overwatch.md Section 8, the displayed dashboard value is
#   the only authoritative source; this hook reads resolution-order source 2,
#   the "Current cycle" line in Core/reference/project-index/usage-tracking.md,
#   and says so on screen. A hardcoded Friday anchor sat in Section 8 for
#   three months and shipped a burn window off by two days
#   (SIG-OVERWATCH-RESET-ANCHOR-FRIDAY-REGRESSION-2026-07-29). Never again in
#   a file that runs every session.
#
#   It does not block. A SessionStart hook that fails a session is worse than
#   the drift it catches. Every failure path exits 0.
#
# Bypass: BUDGET_SNAPSHOT_CHECK_BYPASSED=1
#
# Created: 2026-07-29 (closes step 3 of
#   .intent/plans/HANDOFF-CODEBURN-AS-BUDGET-SOURCE-OF-TRUTH-2026-07-29.md,
#   and the "not yet built" session-start burn summary logged as latent
#   backlog in Core/reference/usage-tracker/usage-model.md)

set -u

[ "${BUDGET_SNAPSHOT_CHECK_BYPASSED:-0}" = "1" ] && exit 0

CODEBURN="${CODEBURN_BIN:-/opt/homebrew/bin/codeburn}"
command -v "$CODEBURN" >/dev/null 2>&1 || CODEBURN="$(command -v codeburn 2>/dev/null)"

WS="${WORKSPACES_ROOT:-$HOME/Workspaces}"
ANCHOR_FILE="$WS/Core/reference/project-index/usage-tracking.md"

if [ -z "${CODEBURN:-}" ] || [ ! -x "$CODEBURN" ]; then
  printf '\n%s\n' "BUDGET: codeburn not found. Install it, or set CODEBURN_BIN."
  printf '%s\n' "        Until then no session has a spend reading. This is not a clean state."
  exit 0
fi

TMPDIR_B="$(mktemp -d 2>/dev/null)" || exit 0
trap 'rm -rf "$TMPDIR_B"' EXIT

# Each codeburn call takes roughly 3s (it rescans transcripts), so run the two
# we need concurrently rather than serially. Serial would put this hook near
# 7s on its own, and a slow SessionStart hook gets disabled by whoever is
# waiting for it.
( "$CODEBURN" budget --check >"$TMPDIR_B/budget" 2>/dev/null; echo $? >"$TMPDIR_B/budget.rc" ) &
BPID=$!
( "$CODEBURN" status --format json >"$TMPDIR_B/status" 2>/dev/null ) &
SPID=$!
wait "$BPID" "$SPID" 2>/dev/null

BUDGET_OUT="$(cat "$TMPDIR_B/budget" 2>/dev/null)"
BUDGET_RC="$(cat "$TMPDIR_B/budget.rc" 2>/dev/null || echo 0)"
STATUS_JSON="$(cat "$TMPDIR_B/status" 2>/dev/null)"

if [ -z "$BUDGET_OUT" ] && [ -z "$STATUS_JSON" ]; then
  printf '\n%s\n' "BUDGET: codeburn returned nothing. Run 'codeburn doctor' to see why."
  exit 0
fi

printf '\n%s\n' "BUDGET (codeburn is the instrument, the dashboard is the anchor)"
printf '\n'

# --- Tripwires: codeburn's own daily / rolling-7day budgets -----------------
# codeburn prints these as "  daily: $309.77 of $400.00 (77%) [OK]". Reprint
# them with the window named, because "weekly" here means rolling 7 days and
# reading it as cycle-percent is the documented failure mode.
if [ -n "$BUDGET_OUT" ]; then
  printf '%s\n' "$BUDGET_OUT" | while IFS= read -r line; do
    case "$line" in
      *daily:*)  printf '  today (24h)       %s\n' "$(printf '%s' "$line" | sed 's/^ *daily: *//')" ;;
      *weekly:*) printf '  rolling 7 days    %s\n' "$(printf '%s' "$line" | sed 's/^ *weekly: *//')" ;;
    esac
  done
fi

if [ "$BUDGET_RC" = "1" ]; then
  printf '\n  %s\n' "TRIPWIRE BREACHED. At least one configured budget is over."
  printf '  %s\n' "That is a throttle signal, not a spend-it-down signal. The 2026-07-19"
  printf '  %s\n' "freeze came from burning a bucket to zero and losing the next two days."
fi

# --- The real cycle: Wednesday-anchored, resolved not hardcoded -------------
python3 - "$ANCHOR_FILE" <<'PY' 2>/dev/null
import re, sys
from datetime import datetime, timedelta
try:
    from zoneinfo import ZoneInfo
except ImportError:
    sys.exit(0)

path = sys.argv[1]
try:
    text = open(path, encoding="utf-8").read()
except OSError:
    print()
    print("  weekly cycle      anchor file unreadable: %s" % path)
    print("                    Capture the dashboard and record it there.")
    sys.exit(0)

# Resolution-order source 2: the "Current cycle" line. Deliberately NOT a
# constant in this file. See the header note on the Friday regression.
m = re.search(
    r"next reset\s+\w+\s+(\d{4}-\d{2}-\d{2})\s+(\d{1,2}):(\d{2})\s*([AaPp])\.?[Mm]\.?\s*ET",
    text,
)
if not m:
    print()
    print("  weekly cycle      no 'next reset' found in the Current cycle line.")
    print("                    Source: %s" % path)
    sys.exit(0)

date_s, hh, mm, ampm = m.group(1), int(m.group(2)), int(m.group(3)), m.group(4).lower()
if ampm == "p" and hh != 12:
    hh += 12
elif ampm == "a" and hh == 12:
    hh = 0

ET = ZoneInfo("America/New_York")
y, mo, d = (int(x) for x in date_s.split("-"))
nxt = datetime(y, mo, d, hh, mm, tzinfo=ET)
now = datetime.now(ET)

# Forward-roll whole weeks if the recorded reset has already passed. This is a
# staleness indicator, not a correction: it means nobody has captured the
# dashboard since then, and the anchor is mobile by Anthropic's discretion.
rolled = 0
while nxt <= now:
    nxt += timedelta(days=7)
    rolled += 1

to_reset = (nxt - now).total_seconds() / 3600.0
elapsed = 168.0 - to_reset
pct = max(0.0, min(100.0, elapsed / 168.0 * 100.0))

print()
print("  weekly cycle      %s" % nxt.strftime("next reset %a %Y-%m-%d %-I:%M %p ET"))
print("                    %.0fh elapsed of 168h (%.0f%%), %.0fh to reset" % (elapsed, pct, to_reset))

if rolled:
    weeks = "week" if rolled == 1 else "weeks"
    print()
    print("  STALE ANCHOR      recorded reset had already passed; rolled forward %d %s."
          % (rolled, weeks))
    print("                    Nobody has captured the dashboard in that time, and the")
    print("                    anchor is mobile. Read the displayed 'Resets [day] [time]'")
    print("                    and record it in the Current cycle line.")
PY

printf '\n'
printf '  %s\n' "Read these correctly:"
printf '  %s\n' "- The rolling 7 days above is NOT the cycle. It is a tripwire window."
printf '  %s\n' "  Cycle percent consumed comes from the dashboard only."
printf '  %s\n' "- Dollars are API-equivalent notional on a Max subscription, not"
printf '  %s\n' "  out-of-pocket. They measure bucket draw, not money leaving an account."
printf '  %s\n' "- Fable draws the weekly bucket at roughly 4.8x Opus per token, so a"
printf '  %s\n' "  cheap-looking Fable fan-out is the most expensive thing available."
printf '  %s\n' "- Anchor source: Core/reference/project-index/usage-tracking.md"
printf '\n'

exit 0
