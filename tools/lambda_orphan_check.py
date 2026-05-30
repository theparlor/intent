#!/usr/bin/env python3
"""
lambda_orphan_check.py — Durable catch-net for uncommitted lambda_settings blocks.

WHY THIS EXISTS
  apply_lambda_settings.py writes a managed lambda_settings block into each product's
  .intent/INTENT.md. The --commit flag (write-through) is the PRIMARY fix that prevents
  orphans from accumulating. This script is the catch_mechanism — a durable, wireable
  completeness tally that can be run as a pre-commit hook, periodic cron, or on-demand
  audit to detect any orphaned λ blocks that slipped past the write-through.

  This is the "catch-net for the catch-net" per feedback_audit_vs_writethrough:
    - Write-through (apply_lambda_settings.py --commit) is the upstream control.
    - This script is the safety net if write-through is skipped, fails, or predates
      the --commit flag.

WHAT AN ORPHAN IS
  A file is an ORPHAN if:
    1. It contains the managed lambda_settings block (bounded by START_MARKER /
       END_MARKER from apply_lambda_settings.py), AND
    2. The file is uncommitted/dirty/untracked relative to its owning git repo
       (detected via `git status --porcelain -- <file>` returning non-empty output).
  Files not in any git repo are also treated as orphans (can't be committed).

WHAT IS NOT FLAGGED
  - INTENT.md files that do NOT contain a lambda_settings block (even if dirty).
  - Files in excluded buckets (.claude, Work/, ROOT/).
  - Directories: .venv, node_modules.

EXIT CODES
  0 — no orphans found
  2 — one or more orphans found

USAGE
    python lambda_orphan_check.py [--root DIR] [--json OUT.json]
      --root DIR     root to walk (default: /Users/brien/Workspaces/Core)
      --json OUT     write machine-readable orphan list to OUT.json

Stdlib only. Fails soft on missing/unreadable files (same defensive posture as
drag_dashboard.py). A directory that can't be walked is skipped with a warning.

PRIMARY FIX:   apply_lambda_settings.py --commit  (upstream_control_path)
CATCH-NET:     this script                         (catch_mechanism)
"""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path
from typing import Optional

# Sentinel strings copied verbatim from apply_lambda_settings.py — must stay in sync.
START_MARKER = "# === lambda_settings (managed by apply_lambda_settings.py, do not edit by hand) ==="

# Directories to skip when walking
SKIP_DIRS = {".venv", "node_modules", ".git", "__pycache__"}

# Bucket prefixes (relative to root) to exclude — mirrors apply_lambda_settings.py
EXCLUDE_BUCKET_PREFIXES = (".claude", "Work", "ROOT")

DEFAULT_ROOT = "/Users/brien/Workspaces/Core"


def _has_lambda_block(path: Path) -> bool:
    """Return True if the file contains the managed lambda_settings block."""
    try:
        text = path.read_text(encoding="utf-8", errors="replace")
        return START_MARKER in text
    except OSError:
        return False


def _is_excluded(path: Path, root: Path) -> bool:
    """Return True if the path falls under an excluded bucket."""
    try:
        rel = path.relative_to(root)
    except ValueError:
        return False
    parts = rel.parts
    if not parts:
        return False
    return parts[0].startswith(EXCLUDE_BUCKET_PREFIXES)


def _resolve_git_root(path: Path) -> Optional[Path]:
    """Return the git repo root owning `path`, or None if not in any repo.

    Returns the resolved (symlink-free) real path so that relative_to comparisons
    work correctly on macOS where /tmp → /private/tmp.
    """
    try:
        r = subprocess.run(
            ["git", "-C", str(path.parent), "rev-parse", "--show-toplevel"],
            capture_output=True,
            text=True,
            check=True,
        )
        # resolve() normalises /tmp → /private/tmp on macOS
        return Path(r.stdout.strip()).resolve()
    except (subprocess.CalledProcessError, FileNotFoundError):
        return None


def _is_dirty_or_untracked(intent_path: Path, repo_root: Path) -> bool:
    """
    Return True if `intent_path` is dirty (modified) or untracked relative to
    `repo_root` (i.e. `git status --porcelain -- <file>` returns non-empty).

    Both paths are resolved before comparison to handle macOS /tmp → /private/tmp
    symlinks (git rev-parse returns the real path; the Python Path may not).
    """
    try:
        real_intent = intent_path.resolve()
        real_root = repo_root.resolve()
        relative = str(real_intent.relative_to(real_root))
        r = subprocess.run(
            ["git", "-C", str(real_root), "status", "--porcelain", "--", relative],
            capture_output=True,
            text=True,
            check=True,
        )
        return bool(r.stdout.strip())
    except (subprocess.CalledProcessError, FileNotFoundError, ValueError):
        # If anything goes wrong assume it's dirty (conservative / fail-safe)
        return True


def find_intent_mds(root: Path) -> list[Path]:
    """
    Walk root and yield candidate INTENT.md paths, skipping excluded directories.
    Matches both `.intent/INTENT.md` and plain `INTENT.md`.
    """
    candidates: list[Path] = []
    if not root.is_dir():
        print(f"[warn] root not a directory, skipping: {root}", file=sys.stderr)
        return candidates

    try:
        for p in root.rglob("INTENT.md"):
            # Skip if any path component is in SKIP_DIRS
            if any(part in SKIP_DIRS for part in p.parts):
                continue
            # Skip excluded buckets
            if _is_excluded(p, root):
                continue
            candidates.append(p)
    except PermissionError as e:
        print(f"[warn] permission error walking {root}: {e}", file=sys.stderr)

    return candidates


def check_orphans(root: Path) -> list[dict]:
    """
    Walk root and return a list of orphan records (dicts with path, repo, reason).
    """
    orphans: list[dict] = []
    candidates = find_intent_mds(root)

    for intent_path in sorted(candidates):
        if not _has_lambda_block(intent_path):
            continue  # No managed block — not our concern

        repo_root = _resolve_git_root(intent_path)
        if repo_root is None:
            orphans.append({
                "path": str(intent_path),
                "repo": None,
                "reason": "not-in-git-repo",
            })
            continue

        if _is_dirty_or_untracked(intent_path, repo_root):
            orphans.append({
                "path": str(intent_path),
                "repo": str(repo_root),
                "reason": "uncommitted-lambda-block",
            })

    return orphans


def main(argv: list[str]) -> int:
    root = Path(DEFAULT_ROOT)
    json_out: Optional[Path] = None

    i = 1
    while i < len(argv):
        arg = argv[i]
        if arg == "--root" and i + 1 < len(argv):
            root = Path(argv[i + 1]).expanduser().resolve()
            i += 2
        elif arg == "--json" and i + 1 < len(argv):
            json_out = Path(argv[i + 1]).expanduser().resolve()
            i += 2
        elif arg in ("--help", "-h"):
            print(__doc__)
            return 0
        else:
            print(f"Unknown argument: {arg}", file=sys.stderr)
            return 1

    if not root.exists():
        print(f"[error] root does not exist: {root}", file=sys.stderr)
        return 1

    orphans = check_orphans(root)

    if orphans:
        print(f"ORPHANED lambda_settings blocks found: {len(orphans)}")
        print("These INTENT.md files contain a managed λ block but are NOT committed:")
        for o in orphans:
            repo_tag = f"  repo={o['repo']}" if o["repo"] else "  repo=NONE (not in git)"
            print(f"  {o['path']}{repo_tag}  ({o['reason']})")
        print()
        print("Fix: run apply_lambda_settings.py --commit  (write-through)")
        print("     or manually: git add <file> && git commit -m 'chore(intent): commit λ block'")
    else:
        print("OK — no orphaned lambda_settings blocks found.")

    if json_out is not None:
        payload = {"orphan_count": len(orphans), "orphans": orphans}
        try:
            json_out.write_text(json.dumps(payload, indent=2), encoding="utf-8")
            print(f"JSON output written to {json_out}")
        except OSError as e:
            print(f"[warn] could not write JSON output: {e}", file=sys.stderr)

    return 2 if orphans else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
