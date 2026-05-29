#!/usr/bin/env bash
# install-git-hooks.sh — wire the intent repo's GIT hooks (distinct from
# install.sh, which deploys Claude Code hooks into ~/.claude/hooks/).
#
# Installs the Drag cap-guard as the repo's pre-commit hook so accretion of the
# lexical enforcement layer is caught at commit time. Idempotent; re-runnable.
# Run from anywhere inside the repo. Survives fresh clones (run once per clone).

set -uo pipefail

REPO_ROOT="$(git rev-parse --show-toplevel 2>/dev/null)"
if [[ -z "${REPO_ROOT}" ]]; then
  echo "ERROR: not inside a git repo." >&2
  exit 1
fi

HOOK_SRC="${REPO_ROOT}/hooks/pre-commit-drag-guard.sh"
HOOK_DST="${REPO_ROOT}/.git/hooks/pre-commit"

if [[ ! -f "${HOOK_SRC}" ]]; then
  echo "ERROR: ${HOOK_SRC} not found." >&2
  exit 1
fi
chmod +x "${HOOK_SRC}"

if [[ -e "${HOOK_DST}" && ! -L "${HOOK_DST}" ]]; then
  echo "WARN: ${HOOK_DST} exists and is not our symlink; not overwriting."
  echo "      Merge the cap-guard call into your existing pre-commit manually:"
  echo "        python3 \"\${REPO_ROOT}/tools/drag_dashboard.py\" --check || exit 1"
  exit 1
fi

ln -sf "${HOOK_SRC}" "${HOOK_DST}"
echo "OK: pre-commit -> ${HOOK_SRC}"
echo "    (Drag cap-guard armed; fires when a commit touches hooks/.)"
