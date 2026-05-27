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
install_hook native-connector-precedence-check.sh

# Symlink the lookup map for the native-connector hook so it stays adjacent
# to the script when invoked via ~/.claude/hooks/.
MAP_NAME="native-connector-precedence-map.json"
MAP_SRC="${SOURCE_DIR}/${MAP_NAME}"
MAP_DST="${HOOK_DIR}/${MAP_NAME}"
if [[ -f "${MAP_SRC}" ]]; then
  if [[ -L "${MAP_DST}" && "$(readlink "${MAP_DST}")" == "${MAP_SRC}" ]]; then
    echo "OK:   ${MAP_NAME} (already symlinked)"
  elif [[ -e "${MAP_DST}" ]]; then
    echo "WARN: ${MAP_DST} exists and is not our symlink; not overwriting"
  else
    ln -s "${MAP_SRC}" "${MAP_DST}"
    echo "OK:   ${MAP_NAME} (symlinked -> ${MAP_SRC})"
  fi
else
  echo "SKIP: ${MAP_NAME} (source not found at ${MAP_SRC})"
fi

cat << 'EOF'

Next step (manual): register the hooks in ~/.claude/settings.json

Add to hooks.SessionStart:

  {
    "matcher": "*",
    "hooks": [
      {
        "type": "command",
        "command": "~/.claude/hooks/autonomy-grant-check.sh"
      }
    ]
  }

Add to hooks.PreToolUse:

  {
    "matcher": "mcp__google-workspace__.*",
    "hooks": [
      {
        "type": "command",
        "command": "$HOME/.claude/hooks/native-connector-precedence-check.sh"
      }
    ]
  }

Then start a new Claude Code session and confirm:
  - The autonomy-grant banner appears in session-start context
  - Calling `mcp__google-workspace__search_gmail_messages` is blocked with a
    pointer to the native equivalent

Specs:
  Core/frameworks/intent/spec/autonomy-grant-enforcement.md §Verification
  Core/frameworks/intent/spec/native-connector-precedence.md §Closure DoD
EOF
