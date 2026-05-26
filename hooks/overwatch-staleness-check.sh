#!/usr/bin/env bash
# overwatch-staleness-check.sh
#
# SessionStart hook that detects overwatch staleness and emits a banner
# warning when the last overwatch journal is older than the threshold.
#
# Closes upstream control for SIG-OVERWATCH-STALENESS-PATTERN-2026-05-20.
# Governance skills without auto-triggers silently rot. This hook is the
# mechanism-level prevention.
#
# Deploy: symlink to ~/.claude/hooks/overwatch-staleness-check.sh and
# register in ~/.claude/settings.json under hooks.SessionStart.
#
# Behavior:
#   - Reads latest mtime of JRN-*overwatch* files in
#     Core/products/org-design-tooling/journal/
#   - Computes days since most-recent overwatch run
#   - Emits banner to stdout (SessionStart hook stdout is injected into
#     session context) when threshold crossed
#   - Three tiers:
#       fresh (<7 days)       -> silent (no output)
#       stale  (7-13 days)    -> warn banner
#       overdue (>=14 days)   -> load-bearing posture banner
#
# Bypass: set OVERWATCH_STALENESS_BYPASSED=1 to skip the check entirely.
#
# Spec: Core/frameworks/intent/spec/closure-discipline-enforcement.md
# Signal: Core/frameworks/intent/.intent/signals/SIG-OVERWATCH-STALENESS-PATTERN-2026-05-20.md

set -euo pipefail

if [[ "${OVERWATCH_STALENESS_BYPASSED:-0}" == "1" ]]; then
  exit 0
fi

JOURNAL_DIR="${HOME}/Workspaces/Core/products/org-design-tooling/journal"

if [[ ! -d "$JOURNAL_DIR" ]]; then
  # Journal dir missing — nothing to check. Exit silently so the hook
  # never breaks a session in non-Workspaces environments.
  exit 0
fi

# Find latest JRN-*overwatch* file by mtime. We use JRN- (not EXT-)
# because JRN files are the canonical journal entries; EXT files are
# extractions/projections of the same data.
LATEST=$(find "$JOURNAL_DIR" -maxdepth 1 -name 'JRN-*overwatch*' -type f -print0 2>/dev/null \
         | xargs -0 stat -f '%m %N' 2>/dev/null \
         | sort -rn \
         | head -1)

if [[ -z "$LATEST" ]]; then
  # No overwatch journals at all. Most likely a fresh checkout — emit
  # the load-bearing banner so the session knows to run /overwatch.
  cat <<'EOF'
⚠️  OVERWATCH NEVER-RUN POSTURE (load-bearing)

No JRN-*overwatch* files found in Core/products/org-design-tooling/journal/.
Overwatch is the governance sweep that catches drift across all products,
memory, MCP connectors, governance compliance, and incestuous amplification.

Run `/overwatch` before non-trivial work this session. Without a fresh sweep,
work-backlog discovery is blind and write-through hook failures may be silent.

Signal: SIG-OVERWATCH-STALENESS-PATTERN-2026-05-20
EOF
  exit 0
fi

LATEST_MTIME=$(echo "$LATEST" | awk '{print $1}')
LATEST_PATH=$(echo "$LATEST" | cut -d' ' -f2-)
NOW=$(date +%s)
AGE_SECONDS=$((NOW - LATEST_MTIME))
AGE_DAYS=$((AGE_SECONDS / 86400))

if [[ "$AGE_DAYS" -lt 7 ]]; then
  # Fresh. Silent exit — no banner needed.
  exit 0
fi

LATEST_BASENAME=$(basename "$LATEST_PATH")

if [[ "$AGE_DAYS" -ge 14 ]]; then
  # Overdue — load-bearing posture banner. Tone-match the
  # autonomy-grant and closure-discipline anchors.
  cat <<EOF
⚠️  OVERWATCH OVERDUE — LOAD-BEARING POSTURE

Last overwatch journal: ${LATEST_BASENAME}
Age: ${AGE_DAYS} days (threshold: 14 days)

Overwatch is the governance sweep that catches drift everywhere else in the
system. Without it, the work-backlog goes invisible and write-through hook
failures propagate silently. The skill itself is subject to drift when it has
no auto-trigger — that drift is now active.

BEFORE non-trivial work this session, run \`/overwatch\` to refresh:
  - Memory index consistency (write-through validation)
  - MCP connector probes
  - Governance compliance
  - Incestuous amplification (disconfirmation, signal diversity, conclusion staleness)

If you skip the sweep, name the gate explicitly in your response (which of
the 4 autonomy gates fails for this session). Otherwise default to running it.

Pattern: SIG-OVERWATCH-STALENESS-PATTERN-2026-05-20
Spec: Core/frameworks/intent/spec/closure-discipline-enforcement.md (catch-net family)
EOF
else
  # Stale — gentle warn banner.
  cat <<EOF
ℹ️  Overwatch is stale (${AGE_DAYS} days since ${LATEST_BASENAME}; threshold 7d).

Consider running \`/overwatch\` before non-trivial work to refresh the
work-backlog and catch any silent write-through hook failures.

Pattern: SIG-OVERWATCH-STALENESS-PATTERN-2026-05-20
EOF
fi

exit 0
