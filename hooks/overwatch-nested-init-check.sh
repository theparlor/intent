#!/usr/bin/env bash
# overwatch-nested-init-check.sh
#
# SessionStart hook that detects the "embedded .git inside parent-tracked path"
# condition — where a nested git repo sits inside a subtree that the parent
# Workspaces repo (theparlor/workspaces-governance) still tracks files under.
#
# This is the preventive catch-net for the failure mode documented in
# SIG-2026-05-20-frameworks-repo-split: a `git init` inside a parent-tracked
# path creates a submodule-like boundary that parent git respects (hiding edits)
# but parent's HEAD tree doesn't reflect (no gitlink, no .gitmodules entry).
# Files silently fall out of active tracking in BOTH repos.
#
# Closes upstream control for SIG-2026-05-20-nested-init-prevention (Option 2).
#
# Deploy: symlink to ~/.claude/hooks/overwatch-nested-init-check.sh and
# register in ~/.claude/settings.json under hooks.SessionStart.
#
# Behavior:
#   - Walks /Users/brien/Workspaces/ for .git/ directories at depth >= 2
#     (skips the parent repo's own .git at depth 1)
#   - For each nested .git found, checks whether the parent repo tracks
#     any files under that path (git ls-files returns >= 1 result)
#   - If the "tracked + masked" condition exists: emits a finding banner
#     with the path, masked-file count, and resolution playbook pointer
#   - Zero findings = silent exit (no output, no banner)
#
# Bypass: set OVERWATCH_NESTED_INIT_BYPASSED=1 to skip the check entirely.
#
# Resolution playbook: SIG-2026-05-20-frameworks-repo-split.md
# Spec: Core/frameworks/intent/spec/overwatch.md
# Signal: Workspaces/.intent/signals/SIG-2026-05-20-nested-init-prevention.md

set -euo pipefail

if [[ "${OVERWATCH_NESTED_INIT_BYPASSED:-0}" == "1" ]]; then
  exit 0
fi

WORKSPACES_ROOT="${HOME}/Workspaces"

if [[ ! -d "${WORKSPACES_ROOT}/.git" ]]; then
  # Not inside the parent workspaces-governance repo. Exit silently so the
  # hook never breaks sessions in non-Workspaces environments.
  exit 0
fi

FINDINGS=()

# Walk for .git directories at depth >= 2 relative to WORKSPACES_ROOT.
# The parent's own .git is at depth 1 (${WORKSPACES_ROOT}/.git), so mindepth 2
# skips it while catching every nested repo, including shallow paths like
# .context/.git (depth 2) and deep paths like Core/products/X/.git (depth 4).
# maxdepth 8 avoids traversing into deep unrelated trees.
while IFS= read -r -d '' nested_git; do
  nested_dir="${nested_git%/.git}"
  # Compute path relative to workspaces root for the parent ls-files query
  rel_path="${nested_dir#${WORKSPACES_ROOT}/}"

  # Ask parent repo: how many files are tracked under this relative path?
  masked_count=$(git -C "${WORKSPACES_ROOT}" ls-files -- "${rel_path}" 2>/dev/null | wc -l | tr -d ' ')

  if [[ "${masked_count}" -ge 1 ]]; then
    FINDINGS+=("${rel_path} (${masked_count} masked file(s))")
  fi
done < <(find "${WORKSPACES_ROOT}" -mindepth 2 -maxdepth 8 -name ".git" -type d -print0 2>/dev/null)

if [[ "${#FINDINGS[@]}" -eq 0 ]]; then
  # Clean state. Exit silently — no banner needed.
  exit 0
fi

# One or more "tracked + masked" conditions detected. Emit a load-bearing banner.
cat <<'BANNER'
⚠️  NESTED-INIT CONFLICT DETECTED (load-bearing)

A nested .git directory exists inside a path that the parent Workspaces repo
(theparlor/workspaces-governance) still tracks files under. Edits to files in
the affected paths will be invisible to BOTH repos through normal git workflow:
  - Parent's git status respects the embedded .git boundary (treats it as an
    unregistered submodule) and silently skips changes inside it.
  - Nested repo does not track the parent-committed blobs (they were not in
    the nested init commit's tree).

This is the same failure mode documented in:
  SIG-2026-05-20-frameworks-repo-split (resolution playbook)
  Workspaces/.intent/signals/SIG-2026-05-20-frameworks-repo-split.md

BANNER

echo "Affected paths (parent-tracked files masked by nested .git):"
for finding in "${FINDINGS[@]}"; do
  echo "  - ${finding}"
done

cat <<'TRAILER'

Resolution steps (from the playbook):
  1. Decide canonical home: nested repo OR parent repo (not both).
  2. If nested is canonical: git rm --cached -r <path> in parent; commit +
     push to workspaces-governance. Re-commit missing blobs in nested with
     provenance footer pointing to parent's originating commit SHAs.
  3. If parent is canonical: remove the nested .git; commit all files to
     parent; delete or archive the nested remote if it exists.
  4. Verify: both parent ls-files and nested git status are consistent.

This check runs at SessionStart. It will continue to fire until the conflict
is resolved. To suppress for a single session: export OVERWATCH_NESTED_INIT_BYPASSED=1

Signal: SIG-2026-05-20-nested-init-prevention
TRAILER

exit 0
