#!/usr/bin/env bash
# install.sh — deploy intent hooks into ~/.claude/hooks/
#
# Safe to re-run. Uses symlinks so hook updates in Core/ propagate without
# re-install. Does NOT modify ~/.claude/settings.json — hook registration
# is a manual step (printed at the end).

set -euo pipefail

HOOK_DIR="${HOME}/.claude/hooks"
SOURCE_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

mkdir -p "${HOOK_DIR}"

install_hook() {
  local name="$1"
  local src="${SOURCE_DIR}/${name}"
  local dst="${HOOK_DIR}/${name}"

  if [[ ! -f "${src}" ]]; then
    echo "SKIP: ${name} (source not found at ${src})"
    return
  fi

  chmod +x "${src}"

  if [[ -L "${dst}" && "$(readlink "${dst}")" == "${src}" ]]; then
    echo "OK:   ${name} (already symlinked)"
  elif [[ -e "${dst}" ]]; then
    echo "WARN: ${dst} exists and is not our symlink; not overwriting"
    return 1
  else
    ln -s "${src}" "${dst}"
    echo "OK:   ${name} (symlinked -> ${src})"
  fi
}

install_hook autonomy-grant-check.sh

cat << 'EOF'

Next step (manual): register the hook in ~/.claude/settings.json

Add to the hooks.SessionStart array:

  {
    "matcher": "*",
    "hooks": [
      {
        "type": "command",
        "command": "~/.claude/hooks/autonomy-grant-check.sh"
      }
    ]
  }

Then start a new Claude Code session and confirm the autonomy-grant banner
appears in session-start context. See
Core/frameworks/intent/spec/autonomy-grant-enforcement.md §Verification.
EOF
