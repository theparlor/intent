#!/usr/bin/env python3
"""
apply_lambda_settings.py — Apply per-product λ values to each product's .intent/INTENT.md.

Completes the flight-model pipeline: inventory -> extract -> fit -> APPLY.

Per SPEC-INTENT-AUTONOMY-FLIGHT-MODEL-001 §16 (λ-scoping convention):
λ is persisted per-product as a top-level field in each product's .intent/INTENT.md.

Per WS-DDR-098 (Witness mandatory-recorder):
Products that emit autonomy decisions MUST declare lambda_settings. This script is
the mechanism that initially populates that declaration for the 25+ products that
the fit determined are ready to apply.

Idempotency:
  The block is bounded by sentinel comments. Re-running updates in place. Other
  frontmatter fields are preserved exactly. The sentinel-marker approach avoids
  YAML round-trip reformatting risk.

Excluded buckets (not real products):
  - .claude (CCD system directory)
  - Work/* (engagement-scoped; exempt per WS-DDR-098)
  - ROOT (Workspaces-wide signals aren't a product)

Write-through (--commit flag):
  When --commit is passed, after each successful write (action in {added, updated})
  this script commits ONLY that INTENT.md into the repo that owns it. Each product
  may live in its own nested git repo; the repo root is resolved via
  `git rev-parse --show-toplevel` relative to the file's parent directory.

  Safety gates — if ANY of the following are true the commit is SKIPPED for that
  product (recorded as "skipped-commit: <reason>", processing continues):
    1. A rebase/merge/cherry-pick/bisect is in progress (.git/REBASE_HEAD,
       .git/MERGE_HEAD, .git/CHERRY_PICK_HEAD, .git/BISECT_LOG exist).
    2. The index already has OTHER staged changes (git diff --cached --name-only
       returns entries besides our target file) — we never fold someone else's
       staged work into our commit.
    3. Our target file is already staged in the index prior to our write (we are
       conservative: if it is already staged with any content, skip).

  It is FINE if there are unrelated UNSTAGED dirty files — we stage ONLY our one
  INTENT.md file. We never run --no-verify. We never push.

  --dry-run --commit: reports what would be committed without writing or committing.

  A per-repo commit ledger is printed at the end showing committed / skipped-commit
  counts and reasons.

Catch-net companion:
  lambda_orphan_check.py (same directory) is the durable catch-net. Run it to find
  any INTENT.md files that contain a managed lambda_settings block but are NOT yet
  committed in their owning repo. Wire it as a pre-commit hook or periodic check.
  See lambda_orphan_check.py for details.

Usage:
    python apply_lambda_settings.py [--dry-run] [--commit] [CORPUS_DIR] [WORKSPACES_ROOT]
      --dry-run: report what would change without writing
      --commit:  after each write, commit that INTENT.md in its owning repo
      defaults: ./extracted-corpus and . relative to CWD
"""

from __future__ import annotations
import re
import subprocess
import sys
from pathlib import Path
from typing import Optional

try:
    import yaml
    HAVE_YAML = True
except ImportError:
    HAVE_YAML = False

EXCLUDE_PREFIXES = (
    ".claude",
    "Work",
    "ROOT",
)

START_MARKER = "# === lambda_settings (managed by apply_lambda_settings.py, do not edit by hand) ==="
END_MARKER = "# === end lambda_settings ==="

FRONTMATTER_RE = re.compile(r"\A---\s*\n(.*?)\n---\s*\n", re.DOTALL)

# Block-replacement regex: matches an existing managed block (between markers)
MANAGED_BLOCK_RE = re.compile(
    re.escape(START_MARKER) + r".*?" + re.escape(END_MARKER) + r"\n?",
    re.DOTALL,
)


def parse_lambda_settings_yaml(corpus_dir: Path) -> dict:
    """Parse lambda-settings-by-product-v1.yaml into {product_name: snippet}."""
    yaml_path = corpus_dir / "lambda-settings-by-product-v1.yaml"
    if not yaml_path.exists():
        raise FileNotFoundError(f"Cannot find {yaml_path} — run lambda_fit.py first")
    text = yaml_path.read_text(encoding="utf-8")

    result = {}
    current_product = None
    current_lines = []

    for line in text.split("\n"):
        m = re.match(r"^# === (.+) ===$", line)
        if m:
            if current_product and current_lines:
                result[current_product] = current_lines
            current_product = m.group(1).strip()
            current_lines = []
            continue
        if current_product is not None:
            current_lines.append(line)

    if current_product and current_lines:
        result[current_product] = current_lines

    return result


def _has_frontmatter(path: Path) -> bool:
    """Quick check: does file start with YAML frontmatter `---\\n`?"""
    try:
        with path.open("r", encoding="utf-8") as f:
            first = f.readline()
            return first.startswith("---")
    except OSError:
        return False


def product_to_intent_path(product: str, workspaces_root: Path) -> Optional[Path]:
    """Resolve product bucket name to INTENT.md path. None if exempt or N/A.

    Lookup order (preferring the file that has YAML frontmatter — required for
    the managed-block insertion logic):
      1. <product>/.intent/INTENT.md (tooling-consumed manifest) — if it has frontmatter
      2. <product>/INTENT.md (product-root human-readable manifest) — if it has frontmatter
      3. <product>/.intent/INTENT.md without frontmatter (returns it; will be
         reported as skipped-no-frontmatter so the operator knows to add frontmatter)

    The split convention: newer/more-developed products use .intent/INTENT.md;
    older/smaller products use root INTENT.md. Some products have both — preferring
    the file that has frontmatter (the only place a managed block can land).
    Pulse is the canonical mixed-convention case: .intent/INTENT.md is a markdown-
    code-block pointer (no frontmatter), root INTENT.md is the YAML-frontmatter main.
    """
    for ex in EXCLUDE_PREFIXES:
        if product.startswith(ex):
            return None
    inner = workspaces_root / product / ".intent" / "INTENT.md"
    root_intent = workspaces_root / product / "INTENT.md"
    if inner.exists() and _has_frontmatter(inner):
        return inner
    if root_intent.exists() and _has_frontmatter(root_intent):
        return root_intent
    if inner.exists():
        return inner  # will skip-no-frontmatter at update time, with the operator-visible diagnostic
    if root_intent.exists():
        return root_intent
    return None


def build_block(product: str, snippet_lines: list[str]) -> str:
    """Construct the managed lambda_settings block to insert into frontmatter."""
    # Trim leading blank lines and trailing blank lines from the snippet
    while snippet_lines and not snippet_lines[0].strip():
        snippet_lines = snippet_lines[1:]
    while snippet_lines and not snippet_lines[-1].strip():
        snippet_lines = snippet_lines[:-1]

    inner = "\n".join(snippet_lines)
    return f"{START_MARKER}\n{inner}\n{END_MARKER}"


def update_intent_md(intent_path: Path, block: str, dry_run: bool) -> dict:
    """Idempotently insert/update the managed lambda_settings block in frontmatter."""
    result = {"path": str(intent_path), "action": None, "diff_lines": 0}
    text = intent_path.read_text(encoding="utf-8")

    m = FRONTMATTER_RE.match(text)
    if not m:
        result["action"] = "skipped-no-frontmatter"
        return result

    frontmatter = m.group(1)
    after = text[m.end():]

    # Check if managed block exists
    existing = MANAGED_BLOCK_RE.search(frontmatter)
    if existing:
        new_frontmatter = MANAGED_BLOCK_RE.sub(block, frontmatter, count=1)
        if new_frontmatter == frontmatter:
            result["action"] = "no-change"
            return result
        action = "updated"
    else:
        # Append block to end of frontmatter (before closing ---)
        # Add one blank-line separator from prior content if needed
        sep = "\n" if frontmatter.endswith("\n") else "\n\n"
        new_frontmatter = frontmatter.rstrip() + "\n\n" + block
        action = "added"

    new_text = "---\n" + new_frontmatter + "\n---\n" + after
    result["action"] = action
    result["diff_lines"] = block.count("\n") + 1

    if not dry_run:
        intent_path.write_text(new_text, encoding="utf-8")
    return result


def _run_git(args: list[str], cwd: Path, check: bool = True) -> subprocess.CompletedProcess:
    """Run a git command in `cwd`, returning CompletedProcess. Raises on non-zero if check=True."""
    return subprocess.run(
        ["git"] + args,
        cwd=str(cwd),
        capture_output=True,
        text=True,
        check=check,
    )


def _resolve_git_root(path: Path) -> Optional[Path]:
    """Return the git repo root that owns `path`, or None if not in any repo.

    Returns the resolved (symlink-free) real path so that relative_to comparisons
    work correctly on macOS where /tmp → /private/tmp.
    """
    try:
        r = _run_git(
            ["-C", str(path.parent), "rev-parse", "--show-toplevel"],
            cwd=path.parent,
            check=True,
        )
        # resolve() normalises /tmp → /private/tmp on macOS
        return Path(r.stdout.strip()).resolve()
    except (subprocess.CalledProcessError, FileNotFoundError):
        return None


def _is_git_operation_in_progress(git_dir: Path) -> Optional[str]:
    """Return a description of any in-progress git operation, or None if all clear."""
    markers = [
        ("REBASE_HEAD", "rebase"),
        ("MERGE_HEAD", "merge"),
        ("CHERRY_PICK_HEAD", "cherry-pick"),
        ("BISECT_LOG", "bisect"),
    ]
    for filename, label in markers:
        if (git_dir / filename).exists():
            return label
    return None


def _get_staged_files(repo_root: Path) -> list[str]:
    """Return list of relative paths currently staged in the index (git diff --cached)."""
    try:
        r = _run_git(["diff", "--cached", "--name-only"], cwd=repo_root, check=True)
        return [line for line in r.stdout.splitlines() if line.strip()]
    except subprocess.CalledProcessError:
        return []


def commit_intent_md(intent_path: Path, dry_run: bool) -> dict:
    """
    Attempt to commit `intent_path` into its owning git repo.

    Returns a dict with keys:
      - committed: bool
      - reason: str (if skipped: why; if committed: short message)
      - repo: str (repo root path)
    """
    result = {"committed": False, "reason": "", "repo": ""}

    # 1. Resolve repo root
    repo_root = _resolve_git_root(intent_path)
    if repo_root is None:
        result["reason"] = "not-in-git-repo"
        return result
    result["repo"] = str(repo_root)

    git_dir = repo_root / ".git"

    # 2. Safety gate: in-progress git operation
    op = _is_git_operation_in_progress(git_dir)
    if op:
        result["reason"] = f"git-{op}-in-progress"
        return result

    # 3. Safety gate: other staged changes
    staged = _get_staged_files(repo_root)
    # Resolve both paths so /tmp vs /private/tmp symlinks don't cause relative_to to fail
    try:
        relative_path = str(intent_path.resolve().relative_to(repo_root.resolve()))
    except ValueError:
        # Shouldn't happen if _resolve_git_root worked, but be defensive
        relative_path = str(intent_path)
    # Normalize separators (Windows safety, though we're on macOS)
    relative_path = relative_path.replace("\\", "/")

    # If our file is already staged (before we wrote it), skip
    if relative_path in staged:
        result["reason"] = "target-already-staged"
        return result

    # Other staged changes present → skip to avoid folding foreign work
    if staged:
        other_staged = [f for f in staged if f != relative_path]
        if other_staged:
            result["reason"] = f"other-staged-changes({','.join(other_staged[:3])})"
            return result

    if dry_run:
        result["committed"] = True
        result["reason"] = "dry-run-would-commit"
        return result

    # 4. Stage only our file
    try:
        _run_git(["-C", str(repo_root), "add", "--", str(intent_path)], cwd=repo_root, check=True)
    except subprocess.CalledProcessError as e:
        result["reason"] = f"git-add-failed: {e.stderr.strip()}"
        return result

    # 5. Commit
    commit_msg = "chore(intent): write-through fitted λ block [apply_lambda_settings]"
    try:
        _run_git(
            ["-C", str(repo_root), "commit", "-m", commit_msg],
            cwd=repo_root,
            check=True,
        )
        result["committed"] = True
        result["reason"] = "committed"
        return result
    except subprocess.CalledProcessError as e:
        # If nothing to commit (no diff after staging), treat as a no-op success
        stderr = e.stderr.strip()
        stdout = e.stdout.strip()
        if "nothing to commit" in stderr or "nothing to commit" in stdout:
            result["committed"] = False
            result["reason"] = "nothing-to-commit-after-add"
        else:
            result["reason"] = f"git-commit-failed: {stderr}"
        return result


def main(argv) -> int:
    dry_run = "--dry-run" in argv
    do_commit = "--commit" in argv
    args = [a for a in argv[1:] if not a.startswith("-")]
    corpus_dir = Path(args[0] if len(args) > 0 else "extracted-corpus").expanduser().resolve()
    workspaces_root = Path(args[1] if len(args) > 1 else ".").expanduser().resolve()

    if not corpus_dir.exists():
        print(f"Corpus dir not found: {corpus_dir}", file=sys.stderr)
        return 1
    if not workspaces_root.exists():
        print(f"Workspaces root not found: {workspaces_root}", file=sys.stderr)
        return 1

    snippets = parse_lambda_settings_yaml(corpus_dir)
    print(f"Loaded {len(snippets)} product snippets from lambda-settings-by-product-v1.yaml")
    mode_parts = []
    if dry_run:
        mode_parts.append("DRY-RUN (no writes)")
    else:
        mode_parts.append("APPLY (writes enabled)")
    if do_commit:
        mode_parts.append("COMMIT (write-through ON)")
    print(f"Mode: {' + '.join(mode_parts)}")
    print()

    results = {"added": [], "updated": [], "no-change": [], "skipped": [], "no-intent-md": []}
    # commit_ledger: list of (product, path, committed: bool, reason: str, repo: str)
    commit_ledger: list[tuple] = []

    for product in sorted(snippets.keys()):
        intent_path = product_to_intent_path(product, workspaces_root)
        if intent_path is None:
            # Check if this is exempt (engagement/system) or just missing INTENT.md
            if any(product.startswith(ex) for ex in EXCLUDE_PREFIXES):
                results["skipped"].append((product, "exempt-bucket"))
            else:
                results["no-intent-md"].append((product, "no-INTENT.md"))
            continue

        block = build_block(product, list(snippets[product]))
        r = update_intent_md(intent_path, block, dry_run)
        action = r["action"]
        if action == "added":
            results["added"].append((product, str(intent_path)))
        elif action == "updated":
            results["updated"].append((product, str(intent_path)))
        elif action == "no-change":
            results["no-change"].append((product, str(intent_path)))
        else:
            results["skipped"].append((product, action))

        # Write-through commit: only when the file actually changed (or would change)
        if do_commit and action in ("added", "updated"):
            cr = commit_intent_md(intent_path, dry_run=dry_run)
            commit_ledger.append((product, str(intent_path), cr["committed"], cr["reason"], cr["repo"]))

    print(f"Added new block:        {len(results['added'])}")
    for p, path in results["added"]:
        print(f"  + {p}  ->  {path}")
    print(f"\nUpdated existing block: {len(results['updated'])}")
    for p, path in results["updated"]:
        print(f"  ~ {p}  ->  {path}")
    print(f"\nNo change (idempotent): {len(results['no-change'])}")
    for p, _ in results["no-change"]:
        print(f"  = {p}")
    print(f"\nSkipped (exempt):       {len(results['skipped'])}")
    for p, reason in results["skipped"]:
        print(f"  - {p}  ({reason})")
    print(f"\nNo INTENT.md found:     {len(results['no-intent-md'])}")
    for p, _ in results["no-intent-md"]:
        print(f"  ? {p}")

    if commit_ledger:
        committed_entries = [(p, path, reason, repo) for p, path, ok, reason, repo in commit_ledger if ok]
        skipped_entries = [(p, path, reason, repo) for p, path, ok, reason, repo in commit_ledger if not ok]
        print(f"\n--- Write-through commit ledger ---")
        print(f"Committed: {len(committed_entries)}")
        for p, path, reason, repo in committed_entries:
            print(f"  ✓ {p}  [{reason}]  repo={repo}")
        print(f"Skipped commit: {len(skipped_entries)}")
        for p, path, reason, repo in skipped_entries:
            print(f"  ✗ {p}  ({reason})  repo={repo}")

    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
