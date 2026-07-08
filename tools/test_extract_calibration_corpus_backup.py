#!/usr/bin/env python3
"""
test_extract_calibration_corpus_backup.py -- regression test for the
backup-before-overwrite fix in extract_calibration_corpus.py.

Origin: RETRO-2026-05-29-enforcement-drag-SIG-2 (org-design-tooling) --
extract_calibration_corpus.py overwrote a 2026-05-26 corpus (229 gold rows,
61 symptom-repaired rows) with empty output on a re-run, no backup existed,
recovery only worked because the files happened to be git-tracked.

Coverage:
  1. backup_if_exists: no prior file -> returns None, no backup written
  2. backup_if_exists: prior file exists -> backup copy created with the
     original content preserved, original path untouched by the backup call
  3. write_text_with_backup: overwriting an existing file preserves the old
     content in a .bak sibling AND writes the new content to the real path
  4. write_text_with_backup: two overwrites in a row produce two distinct
     backups (no backup-of-a-backup collision from timestamp granularity)
"""

from __future__ import annotations

import sys
import tempfile
import time
import unittest
from pathlib import Path

TOOLS_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(TOOLS_DIR))

import extract_calibration_corpus as ecc


class TestBackupIfExists(unittest.TestCase):
    def setUp(self):
        self.tmpdir = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmpdir.cleanup)
        self.root = Path(self.tmpdir.name)

    def test_no_prior_file_returns_none(self):
        target = self.root / "labeled-gold-v1.jsonl"
        result = ecc.backup_if_exists(target)
        self.assertIsNone(result)
        backups = list(self.root.glob("*.bak"))
        self.assertEqual(backups, [])

    def test_prior_file_is_backed_up_with_original_content(self):
        target = self.root / "labeled-gold-v1.jsonl"
        target.write_text('{"row": 1}\n{"row": 2}\n')

        backup_path = ecc.backup_if_exists(target)

        self.assertIsNotNone(backup_path)
        self.assertTrue(backup_path.exists())
        self.assertEqual(backup_path.read_text(), '{"row": 1}\n{"row": 2}\n')
        # Original file is untouched by the backup call itself.
        self.assertEqual(target.read_text(), '{"row": 1}\n{"row": 2}\n')
        self.assertTrue(backup_path.name.endswith(".bak"))
        self.assertIn("labeled-gold-v1.jsonl.pre-", backup_path.name)

    def test_write_text_with_backup_preserves_old_content_and_writes_new(self):
        target = self.root / "symptom-repaired-v1.jsonl"
        target.write_text("OLD-229-ROWS")

        ecc.write_text_with_backup(target, "")  # simulates the destructive re-run

        # New (even empty) content lands at the real path.
        self.assertEqual(target.read_text(), "")

        # The prior corpus survives in a backup file.
        backups = list(self.root.glob("symptom-repaired-v1.jsonl.pre-*.bak"))
        self.assertEqual(len(backups), 1)
        self.assertEqual(backups[0].read_text(), "OLD-229-ROWS")

    def test_repeated_overwrites_produce_distinct_backups(self):
        target = self.root / "lambda-recommendations-2026-05-26.md"
        target.write_text("v1")
        ecc.write_text_with_backup(target, "v2")
        time.sleep(1.1)  # timestamp granularity is whole seconds
        ecc.write_text_with_backup(target, "v3")

        self.assertEqual(target.read_text(), "v3")
        backups = sorted(self.root.glob("lambda-recommendations-2026-05-26.md.pre-*.bak"))
        self.assertEqual(len(backups), 2)
        contents = {b.read_text() for b in backups}
        self.assertEqual(contents, {"v1", "v2"})


if __name__ == "__main__":
    unittest.main()
