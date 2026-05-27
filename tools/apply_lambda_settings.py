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

Usage:
    python apply_lambda_settings.py [--dry-run] [CORPUS_DIR] [WORKSPACES_ROOT]
      --dry-run: report what would change without writing
      defaults: ./extracted-corpus and . relative to CWD
"""

from __future__ import annotations
import re
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


def main(argv) -> int:
    dry_run = "--dry-run" in argv
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
    print(f"Mode: {'DRY-RUN (no writes)' if dry_run else 'APPLY (writes enabled)'}")
    print()

    results = {"added": [], "updated": [], "no-change": [], "skipped": [], "no-intent-md": []}

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

    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
