#!/usr/bin/env python3
"""
test_lambda_pipeline.py — TDD tests for lambda write-through + orphan catch-net.

Tests use stdlib unittest + real git via subprocess in hermetic tempfile repos.
No real Workspaces repos are touched.

Coverage:
  1. orphan_check: uncommitted INTENT.md with lambda block → exit 2, listed
  2. orphan_check: after git commit → exit 0
  3. orphan_check: INTENT.md WITHOUT lambda block, uncommitted → NOT flagged
  4. apply --commit: successful write → exactly one new commit, only INTENT.md staged
  5. apply --commit SAFETY: pre-staged unrelated file → skipped-commit, no fold
  6. apply --dry-run --commit → no writes, no commits
"""

from __future__ import annotations

import os
import subprocess
import sys
import tempfile
import textwrap
import unittest
from pathlib import Path

# ── Resolve the tools directory so we can import sibling modules ──────────────
TOOLS_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(TOOLS_DIR))

import lambda_orphan_check as orphan_mod
import apply_lambda_settings as apply_mod

# ── Constants (must match the real module) ────────────────────────────────────
START_MARKER = apply_mod.START_MARKER
END_MARKER = apply_mod.END_MARKER

# A minimal but valid managed lambda_settings block
LAMBDA_BLOCK = textwrap.dedent(f"""\
    {START_MARKER}
    lambda_settings:
      lambda: 1.025
      fit_date: 2026-05-26
      fit_model: autonomy-flight-model-v1
    {END_MARKER}
""")

# A minimal INTENT.md with YAML frontmatter that contains a lambda block
INTENT_WITH_LAMBDA = textwrap.dedent(f"""\
    ---
    title: Test Product
    type: product-manifest
    {LAMBDA_BLOCK}---

    # Test product intent
    Some body text.
""")

# An INTENT.md WITHOUT a lambda block
INTENT_WITHOUT_LAMBDA = textwrap.dedent("""\
    ---
    title: Test Product
    type: product-manifest
    ---

    # Test product intent
    No lambda block here.
""")

# A minimal lambda-settings-by-product YAML (parsed by parse_lambda_settings_yaml)
LAMBDA_YAML_CONTENT = textwrap.dedent(f"""\
    # === testprod ===
    lambda_settings:
      lambda: 1.025
      fit_date: 2026-05-26
      fit_model: autonomy-flight-model-v1
""")


# ── Helpers ───────────────────────────────────────────────────────────────────

def _git(*args, cwd, check=True, extra_env=None):
    """Run git with headless identity config and controlled environment."""
    env = os.environ.copy()
    env.update({
        "GIT_AUTHOR_NAME": "test",
        "GIT_AUTHOR_EMAIL": "test@test",
        "GIT_COMMITTER_NAME": "test",
        "GIT_COMMITTER_EMAIL": "test@test",
        "HOME": str(cwd),  # avoid picking up host ~/.gitconfig hooks etc.
        "GIT_CONFIG_NOSYSTEM": "1",
    })
    if extra_env:
        env.update(extra_env)
    return subprocess.run(
        ["git", *args],
        cwd=str(cwd),
        capture_output=True,
        text=True,
        check=check,
        env=env,
    )


def _init_repo(tmpdir: Path) -> Path:
    """Create a new git repo at tmpdir with a base empty commit. Returns repo root."""
    _git("init", cwd=tmpdir)
    _git("config", "user.email", "test@test", cwd=tmpdir)
    _git("config", "user.name", "test", cwd=tmpdir)
    # Create an initial empty commit so HEAD exists
    _git("commit", "--allow-empty", "-m", "init", cwd=tmpdir)
    return tmpdir


def _commit_count(repo: Path) -> int:
    """Count commits in the repo (number of lines from git log)."""
    r = _git("rev-list", "--count", "HEAD", cwd=repo, check=True)
    return int(r.stdout.strip())


def _staged_files(repo: Path) -> list[str]:
    """Return list of relative paths currently staged."""
    r = _git("diff", "--cached", "--name-only", cwd=repo, check=True)
    return [line for line in r.stdout.splitlines() if line.strip()]


# ── Test cases ────────────────────────────────────────────────────────────────

class TestOrphanCheckUncommitted(unittest.TestCase):
    """orphan_check: uncommitted INTENT.md with lambda block → exit 2, listed."""

    def test_uncommitted_lambda_block_detected(self):
        with tempfile.TemporaryDirectory() as tmpdir_str:
            repo = Path(tmpdir_str)
            _init_repo(repo)

            # Create prod/.intent/INTENT.md with a lambda block, do NOT commit
            intent_dir = repo / "prod" / ".intent"
            intent_dir.mkdir(parents=True)
            intent_path = intent_dir / "INTENT.md"
            intent_path.write_text(INTENT_WITH_LAMBDA, encoding="utf-8")

            orphans = orphan_mod.check_orphans(repo)

            self.assertEqual(len(orphans), 1, f"Expected 1 orphan, got {len(orphans)}: {orphans}")
            self.assertEqual(orphans[0]["path"], str(intent_path))
            self.assertEqual(orphans[0]["reason"], "uncommitted-lambda-block")

    def test_after_commit_no_orphan(self):
        with tempfile.TemporaryDirectory() as tmpdir_str:
            repo = Path(tmpdir_str)
            _init_repo(repo)

            intent_dir = repo / "prod" / ".intent"
            intent_dir.mkdir(parents=True)
            intent_path = intent_dir / "INTENT.md"
            intent_path.write_text(INTENT_WITH_LAMBDA, encoding="utf-8")

            # Now commit it
            _git("add", str(intent_path), cwd=repo)
            _git("commit", "-m", "add lambda block", cwd=repo)

            orphans = orphan_mod.check_orphans(repo)
            self.assertEqual(len(orphans), 0, f"Expected 0 orphans after commit, got: {orphans}")


class TestOrphanCheckNoLambdaBlock(unittest.TestCase):
    """orphan_check: INTENT.md WITHOUT lambda block, uncommitted → NOT flagged."""

    def test_intent_without_lambda_not_flagged(self):
        with tempfile.TemporaryDirectory() as tmpdir_str:
            repo = Path(tmpdir_str)
            _init_repo(repo)

            intent_dir = repo / "prod" / ".intent"
            intent_dir.mkdir(parents=True)
            intent_path = intent_dir / "INTENT.md"
            intent_path.write_text(INTENT_WITHOUT_LAMBDA, encoding="utf-8")
            # Do NOT commit — it's dirty, but no lambda block

            orphans = orphan_mod.check_orphans(repo)
            self.assertEqual(len(orphans), 0,
                             f"Expected 0 orphans (no lambda block), got: {orphans}")


class TestApplyWithCommit(unittest.TestCase):
    """apply --commit: successful write → exactly one new commit, only INTENT.md staged."""

    def _setup_apply_env(self, tmpdir: Path):
        """Build the corpus dir and workspaces root for apply_lambda_settings."""
        # Corpus dir with lambda-settings-by-product-v1.yaml
        corpus_dir = tmpdir / "corpus"
        corpus_dir.mkdir()
        (corpus_dir / "lambda-settings-by-product-v1.yaml").write_text(
            LAMBDA_YAML_CONTENT, encoding="utf-8"
        )

        # Workspaces root: product "testprod" inside the same repo
        ws_root = tmpdir / "ws"
        ws_root.mkdir()
        return corpus_dir, ws_root

    def test_commit_on_successful_write(self):
        with tempfile.TemporaryDirectory() as tmpdir_str:
            tmpdir = Path(tmpdir_str)
            corpus_dir, ws_root = self._setup_apply_env(tmpdir)

            # Init a git repo at ws_root
            _init_repo(ws_root)

            # Create the product INTENT.md (with frontmatter, no lambda block yet)
            product_dir = ws_root / "testprod" / ".intent"
            product_dir.mkdir(parents=True)
            intent_path = product_dir / "INTENT.md"
            intent_path.write_text(INTENT_WITHOUT_LAMBDA, encoding="utf-8")

            # Commit the initial INTENT.md so working tree is clean at start
            _git("add", str(intent_path), cwd=ws_root)
            _git("commit", "-m", "add intent stub", cwd=ws_root)

            before_count = _commit_count(ws_root)

            # Run apply with --commit
            argv = ["apply_lambda_settings.py", "--commit",
                    str(corpus_dir), str(ws_root)]
            ret = apply_mod.main(argv)

            self.assertEqual(ret, 0, "apply_lambda_settings.main should return 0")

            after_count = _commit_count(ws_root)
            self.assertEqual(after_count, before_count + 1,
                             f"Expected exactly 1 new commit; before={before_count}, after={after_count}")

            # Verify the INTENT.md now contains the lambda block
            final_text = intent_path.read_text(encoding="utf-8")
            self.assertIn(START_MARKER, final_text, "Lambda block should be present after apply")

            # Verify working tree is clean (no orphans)
            orphans = orphan_mod.check_orphans(ws_root)
            self.assertEqual(len(orphans), 0,
                             f"After --commit, orphan_check should be clean: {orphans}")

    def test_commit_message_and_only_intent_staged(self):
        """Verify commit message matches spec and only our INTENT.md was in the commit."""
        with tempfile.TemporaryDirectory() as tmpdir_str:
            tmpdir = Path(tmpdir_str)
            corpus_dir, ws_root = self._setup_apply_env(tmpdir)

            _init_repo(ws_root)

            product_dir = ws_root / "testprod" / ".intent"
            product_dir.mkdir(parents=True)
            intent_path = product_dir / "INTENT.md"
            intent_path.write_text(INTENT_WITHOUT_LAMBDA, encoding="utf-8")

            _git("add", str(intent_path), cwd=ws_root)
            _git("commit", "-m", "add intent stub", cwd=ws_root)

            # Create an UNRELATED unstaged dirty file (should NOT end up committed)
            (ws_root / "unrelated.txt").write_text("dirty", encoding="utf-8")

            apply_mod.main(["apply_lambda_settings.py", "--commit",
                            str(corpus_dir), str(ws_root)])

            # Check commit message
            r = _git("log", "-1", "--format=%s", cwd=ws_root)
            msg = r.stdout.strip()
            self.assertIn("write-through fitted λ block", msg,
                          f"Commit message should mention write-through: {msg!r}")

            # Check only the INTENT.md was in the last commit's diff
            r = _git("diff", "--name-only", "HEAD~1", "HEAD", cwd=ws_root)
            changed = [f.strip() for f in r.stdout.splitlines() if f.strip()]
            self.assertEqual(len(changed), 1, f"Only 1 file should be in commit: {changed}")
            self.assertIn("INTENT.md", changed[0], f"The committed file should be INTENT.md: {changed}")

            # Unrelated file must still be unstaged/dirty
            r = _git("status", "--porcelain", "--", "unrelated.txt", cwd=ws_root)
            self.assertTrue(r.stdout.strip(), "unrelated.txt should still be dirty/untracked")


class TestApplyCommitSafetyPreStagedUnrelated(unittest.TestCase):
    """apply --commit SAFETY: pre-staged unrelated file → skipped-commit, no fold."""

    def test_skips_commit_when_other_file_staged(self):
        with tempfile.TemporaryDirectory() as tmpdir_str:
            tmpdir = Path(tmpdir_str)
            corpus_dir = tmpdir / "corpus"
            corpus_dir.mkdir()
            (corpus_dir / "lambda-settings-by-product-v1.yaml").write_text(
                LAMBDA_YAML_CONTENT, encoding="utf-8"
            )

            ws_root = tmpdir / "ws"
            ws_root.mkdir()
            _init_repo(ws_root)

            product_dir = ws_root / "testprod" / ".intent"
            product_dir.mkdir(parents=True)
            intent_path = product_dir / "INTENT.md"
            intent_path.write_text(INTENT_WITHOUT_LAMBDA, encoding="utf-8")

            _git("add", str(intent_path), cwd=ws_root)
            _git("commit", "-m", "add intent stub", cwd=ws_root)

            before_count = _commit_count(ws_root)

            # Pre-stage an UNRELATED file — this should trigger the safety gate
            unrelated = ws_root / "staged_by_someone_else.txt"
            unrelated.write_text("staged content", encoding="utf-8")
            _git("add", str(unrelated), cwd=ws_root)

            staged_before = _staged_files(ws_root)
            self.assertIn("staged_by_someone_else.txt", staged_before,
                          "Unrelated file should be staged before apply")

            ret = apply_mod.main(["apply_lambda_settings.py", "--commit",
                                  str(corpus_dir), str(ws_root)])
            self.assertEqual(ret, 0)

            after_count = _commit_count(ws_root)
            self.assertEqual(after_count, before_count,
                             f"No commit should be made when other files are staged; "
                             f"before={before_count}, after={after_count}")

            # Unrelated file must still be staged (we must NOT have committed it)
            staged_after = _staged_files(ws_root)
            self.assertIn("staged_by_someone_else.txt", staged_after,
                          "Unrelated staged file must NOT have been folded into a commit")

            # The INTENT.md write DID happen (apply wrote it) even though commit was skipped
            final_text = intent_path.read_text(encoding="utf-8")
            self.assertIn(START_MARKER, final_text,
                          "apply should still write the lambda block even when commit is skipped")


class TestApplyDryRunCommit(unittest.TestCase):
    """apply --dry-run --commit → no writes, no commits."""

    def test_dry_run_with_commit_flag_no_side_effects(self):
        with tempfile.TemporaryDirectory() as tmpdir_str:
            tmpdir = Path(tmpdir_str)
            corpus_dir = tmpdir / "corpus"
            corpus_dir.mkdir()
            (corpus_dir / "lambda-settings-by-product-v1.yaml").write_text(
                LAMBDA_YAML_CONTENT, encoding="utf-8"
            )

            ws_root = tmpdir / "ws"
            ws_root.mkdir()
            _init_repo(ws_root)

            product_dir = ws_root / "testprod" / ".intent"
            product_dir.mkdir(parents=True)
            intent_path = product_dir / "INTENT.md"
            intent_path.write_text(INTENT_WITHOUT_LAMBDA, encoding="utf-8")

            _git("add", str(intent_path), cwd=ws_root)
            _git("commit", "-m", "add intent stub", cwd=ws_root)

            before_count = _commit_count(ws_root)
            original_text = intent_path.read_text(encoding="utf-8")

            ret = apply_mod.main([
                "apply_lambda_settings.py", "--dry-run", "--commit",
                str(corpus_dir), str(ws_root),
            ])
            self.assertEqual(ret, 0)

            after_count = _commit_count(ws_root)
            self.assertEqual(after_count, before_count,
                             "dry-run must not create any commits")

            final_text = intent_path.read_text(encoding="utf-8")
            self.assertEqual(final_text, original_text,
                             "dry-run must not write to disk")

            # Working tree must still be clean
            orphans = orphan_mod.check_orphans(ws_root)
            self.assertEqual(len(orphans), 0,
                             "dry-run should not create orphans (file unchanged)")


if __name__ == "__main__":
    unittest.main(verbosity=2)
