"""Catch-net for SIG-HOOKS-HARDCODE-HOME-PATH-2026-09-22, intent half.

These hooks are symlinked into ~/.claude/hooks on every machine, and their
tests run wherever the repo is cloned. A literal /Users/<account>/ path resolves
to nothing on a machine whose account is named differently. Use "$HOME/..." in
bash, os.path / Path.home() in Python, and "~/..." in prose. Recorded fixtures
under hooks/tests/fixtures are evidence and are exempt.
"""
import re
from pathlib import Path

HOOKS = Path(__file__).resolve().parent.parent
PATTERN = re.compile(r"/Users/[A-Za-z0-9_.-]+/")


def test_no_hardcoded_home_under_hooks():
    hits = []
    for path in sorted(HOOKS.rglob("*")):
        if not path.is_file() or path.is_symlink():
            continue
        rel = path.relative_to(HOOKS)
        if rel.parts[:2] == ("tests", "fixtures") or "__pycache__" in rel.parts:
            continue
        for n, line in enumerate(path.read_text(errors="replace").splitlines(), 1):
            if PATTERN.search(line):
                hits.append(f"hooks/{rel}:{n}: {line.strip()[:100]}")
    assert not hits, "hardcoded account home path(s):\n" + "\n".join(hits)
