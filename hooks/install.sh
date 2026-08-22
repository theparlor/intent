#!/usr/bin/env bash
# install.sh: deploy intent hooks into ~/.claude/hooks/
#
# Safe to re-run. Uses symlinks so hook updates in Core/ propagate without
# re-install. Does NOT modify ~/.claude/settings.json. Hook registration
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
install_hook presend-assertion-check.sh
install_hook budget-snapshot-check.sh
install_hook client-visible-content-lint.sh
install_hook account-connector-fabric-check.sh
# RETIRED 2026-08-22: Operator Voice slice 0 is UNHOOKED. The Stop hook fired on
# every session end, including unattended overnight launchd runs, and spoke aloud
# through the night (8 utterances between 01:02 and 07:07 on 2026-08-22). It woke
# the household. Do NOT re-register the Stop hook without a hard gate on
# unattended sessions plus a quiet-hours window. Scripts are left on disk,
# unregistered, so the work is recoverable; the registration is what was wrong.
#   install_hook operator-voice-speak.sh
#   install_hook operator-voice-play.sh
#   install_hook operator-voice-ctl.sh

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

# Symlink the token spec for the client-visible content lint so it stays
# adjacent to the script when invoked via ~/.claude/hooks/. The Subaru JQL
# catch-net scanner reads the same file: one list, two enforcement points.
TOKENS_NAME="client-visible-content-lint-tokens.json"
TOKENS_SRC="${SOURCE_DIR}/${TOKENS_NAME}"
TOKENS_DST="${HOOK_DIR}/${TOKENS_NAME}"
if [[ -f "${TOKENS_SRC}" ]]; then
  if [[ -L "${TOKENS_DST}" && "$(readlink "${TOKENS_DST}")" == "${TOKENS_SRC}" ]]; then
    echo "OK:   ${TOKENS_NAME} (already symlinked)"
  elif [[ -e "${TOKENS_DST}" ]]; then
    echo "WARN: ${TOKENS_DST} exists and is not our symlink; not overwriting"
  else
    ln -s "${TOKENS_SRC}" "${TOKENS_DST}"
    echo "OK:   ${TOKENS_NAME} (symlinked -> ${TOKENS_SRC})"
  fi
else
  echo "SKIP: ${TOKENS_NAME} (source not found at ${TOKENS_SRC})"
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

Add to hooks.SessionStart (same matcher-* entry as the posture hooks):

  {
    "type": "command",
    "command": "~/.claude/hooks/account-connector-fabric-check.sh",
    "timeout": 10,
    "statusMessage": "Connector fabric: checking claude.ai account-connector expectation"
  }

Operator Voice slice 0: RETIRED 2026-08-22. DO NOT add it to hooks.Stop.
The Stop hook has no awareness of whether a session is attended, so scheduled
launchd runs spoke aloud overnight and woke the household. Any revival needs
(a) an unattended-session gate and (b) a quiet-hours window, both enforced
before the say call, not by the operator remembering to mute.

Then start a new Claude Code session and confirm:
  - The autonomy-grant banner appears in session-start context
  - The account-connector fabric check block appears in session-start context
  - Calling `mcp__google-workspace__search_gmail_messages` is blocked with a
    pointer to the native equivalent

Specs:
  Core/frameworks/intent/spec/autonomy-grant-enforcement.md §Verification
  Core/frameworks/intent/spec/native-connector-precedence.md §Closure DoD
  Core/frameworks/intent/spec/account-connector-fabric-check.md §Verification
EOF
