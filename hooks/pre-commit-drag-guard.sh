#!/usr/bin/env bash
# pre-commit-drag-guard.sh — block commits that grow the lexical enforcement
# layer past its frozen baseline without a sanctioned entry.
#
# Tracked source. Installed to .git/hooks/pre-commit by install-git-hooks.sh
# (symlink). Fires ONLY when a staged change touches hooks/ — cheap otherwise.
# Fail-OPEN: any error determining state lets the commit through (never block
# legitimate work; only block confirmed accretion-drift).
#
# Catch-net for SIG-2026-05-29-friction-00/01. The "first level" hardening:
# the Drag dashboard's cap-guard now fires automatically at commit time.
#   Cap registry : hooks/lexical-layer-freeze.yaml
#   Instrument   : tools/drag_dashboard.py --check  (exit 2 on ACCRETION-DRIFT)

set -uo pipefail

REPO_ROOT="$(git rev-parse --show-toplevel 2>/dev/null)" || exit 0
[[ -n "${REPO_ROOT}" ]] || exit 0

# Only run the cap-guard when this commit touches the hooks dir.
if git diff --cached --name-only 2>/dev/null | grep -qE '^hooks/'; then
  if command -v python3 >/dev/null 2>&1 && [[ -f "${REPO_ROOT}/tools/drag_dashboard.py" ]]; then
    if ! python3 "${REPO_ROOT}/tools/drag_dashboard.py" --check; then
      {
        echo ""
        echo "✗ commit blocked: Drag cap-guard (lexical-layer freeze)."
        echo "  A lexical CHECK was added past the frozen baseline without sanction."
        echo "  Proper path — edit hooks/lexical-layer-freeze.yaml:"
        echo "    • add a sanctioned_additions entry (Drag-budget debit + sunset clause + flight-model cross-ref), OR"
        echo "    • retire the check, OR"
        echo "    • raise frozen_at_check ONLY with the §rule justification."
        echo "  Context: SIG-2026-05-29-friction-01 · spec/autonomy-flight-model-ratification-tracker.md"
      } >&2
      exit 1
    fi
  fi
fi
exit 0
