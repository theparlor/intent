"""Walker skip rules — shared across all intent/tools walker modules.

Single source of truth for which directories the intent-tools walkers
should skip. Mirrors the pattern in Core/products/library-index/skip_rules.py
(see theparlor/library-index-system@8a79e07).

Catch-net for: vendored-external indexing drift — a new walker added to
intent/tools can't forget to skip Core/external because it must import
from here.

See Core/external/superpowers/FORK_RATIONALE.md and
SIG-2026-05-28-sibling-walker-skip-extension.md.
"""
from pathlib import Path

# Bare directory names to skip regardless of where they appear in the tree.
SKIP_DIRS: frozenset = frozenset({
    '.git', 'node_modules', '.venv', '__pycache__', '.cache', 'venv',
    'dist', 'build', '.next', '.turbo', '.pytest_cache', '.mypy_cache',
    'worktrees',
})

# Workspace-relative paths to skip entirely (vendored externals, etc.).
# Use POSIX-style relative paths from the workspaces root.
SKIP_RELATIVE_PATHS: frozenset = frozenset({
    'Core/external',  # vendored upstream forks — see FORK_RATIONALE.md
})


def should_skip_subdir(dirname: str, dirpath, root) -> bool:
    """Path-aware skip — combines bare-name skip with relative-path check.

    Use this in walker loops:
        dirnames[:] = [d for d in dirnames
                       if not should_skip_subdir(d, dirpath, root)]

    Arguments:
        dirname:  bare directory name (one entry from os.walk's dirnames list)
        dirpath:  current directory path (str or Path — the first value from os.walk)
        root:     workspace root (str or Path — passed as the starting point to os.walk)
    """
    if dirname in SKIP_DIRS or dirname.startswith('.'):
        return True
    try:
        rel = Path(dirpath).relative_to(root).as_posix()
    except ValueError:
        return False
    full_rel = f"{rel}/{dirname}" if rel != '.' else dirname
    return full_rel in SKIP_RELATIVE_PATHS
