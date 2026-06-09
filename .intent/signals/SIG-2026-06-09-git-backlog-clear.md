---
id: SIG-2026-06-09-git-backlog-clear
date: 2026-06-09
status: symptom-repaired, upstream-pending
type: execution
summary: >
  Cleared the entity-lifecycle git-risk backlog in Core/frameworks/intent:
  174 dirty files committed as 4 thematic commits, rebased onto origin/main
  (union-resolved an events.jsonl append conflict), and pushed together with
  the 4 pre-existing unpushed commits. Upstream cause — no commit-cadence
  automation — remains open; no catch-net exists for uncommitted-backlog
  accumulation in this repo.
related:
  - Core/products/org-design-tooling/.intent/signals/RETRO-2026-05-29-entity-lifecycle-SIG-3 (origin retro item)
  - memory: project_libindex_cross_product_clobber (enricher artifacts noted below)
---

# Git backlog clear — Core/frameworks/intent (2026-06-09)

## What was found

- 174 modified tracked files + 4 unpushed commits; branch `main` ahead 4 / behind 2 of origin.
- No files modified within the last 10 minutes at execution time; no untracked scratch files.
- Three coherent themes, not one:
  1. **113 files** — uv-3.12 venv rebuild churn in the two *tracked* `.venv` trees
     (`observe/adapters/.venv/`, `tools/intent-mcp/.venv/`): pyvenv.cfg, bin symlinks,
     dist-info INSTALLER/RECORD. Fallout of the 2026-06-04 workspace-wide uv migration.
  2. **60 files** — library-index nightly enrichment frontmatter rewrites
     (depth_signals re-measure, related_entities re-rank, YAML re-serialization).
     One of these (`spec/autonomy-grant-enforcement.md`) also carried a real body
     edit: lexical-layer freeze corrected CHECK 6 -> CHECK 7.
  3. **1 file** — `.intent/events/events.jsonl`, two appended `knowledge.linted`
     audit_chain events (2026-06-05).

## What was done

Four thematic commits with explicit reviewed path lists (never repo-root `-A`):

| Commit (post-rebase) | Theme | Files |
|---|---|---|
| f6d55fc | chore(env): uv-3.12 venv rebuild churn | 113 |
| dc9bce3 | docs(spec): autonomy-grant-enforcement CHECK 7 freeze correction | 1 |
| f39d71b | chore(enrichment): library-index frontmatter refresh | 59 |
| 4a97a84 | chore(events): append two audit_chain knowledge.linted events | 1 |

Then `git pull --rebase origin main`. The rebase conflicted ONLY on
`.intent/events/events.jsonl` (append-only log; both sides appended at EOF).
Resolution: **union, time-ordered** — kept upstream's appended line
(`signal.created` 2026-06-03) first, then replayed the two local
`knowledge.linted` 2026-06-05 lines after it. No event lines were dropped or
merged. Pushed `c9ff071..4a97a84` to `origin/main`; working tree clean, 0 unpushed.

## Enricher artifacts committed as-is (flagged, not fixed here)

- `spec/autonomy-flight-model-v1-DRAFT.md`: enricher brace-wrapped a `related`
  list entry (`- {Core/frameworks/...}`) — YAML now parses it as a flow mapping,
  not a string. Corruption-risk pattern for downstream YAML readers.
- Python-style booleans (`ratify_together: True`) introduced by re-serialization.
- These belong to the library-index writer thread (see libindex cross-product
  clobber memory), not to this repo's pipeline.

## Why symptom-repaired, not resolved

This clears the accumulated backlog (symptom). The upstream control —
**commit-cadence automation** for this repo (coherent-unit auto-commit per the
L4 git grant, or a staleness sweep) — does not exist yet. **No catch-net exists
for uncommitted-backlog accumulation**: nothing fires when dirty-file count or
dirty-age crosses a threshold in Core/frameworks/intent. Until such a
mechanism exists, this signal stays upstream-pending.

## Open questions (L2)

- ~~Should the two tracked `.venv` trees be untracked (`git rm -r --cached` +
  `.gitignore`, matching the existing `servers/.venv/` ignore)? They generated
  113 of the 174 dirty files and will churn again on every interpreter bump.~~
  **ANSWERED — executed 2026-06-09, see addendum below.**

## Addendum 2026-06-09 — venv churn-class fix executed

The open question above was resolved the same day (4-gate pass: reversible,
local, in-repo precedent `servers/.venv/`, no info gap). Commit `9e4cc78`:

- `git rm -r --cached` on both trees — **2535 index entries removed**
  (`observe/adapters/.venv/` 1153 + `tools/intent-mcp/.venv/` 1382); venvs
  untouched on disk, both interpreters verified functional after.
- `.gitignore` extended with `observe/adapters/.venv/` and
  `tools/intent-mcp/.venv/` alongside the existing `servers/.venv/` pattern.
- Reproducibility preserved: sibling `requirements.lock.txt` files (pip freeze
  per the python-environment-standard) were already committed by an earlier
  wave today and verified against the live venvs.

This removes the **churn class** behind theme 1 (113 of 174 dirty files):
interpreter bumps and uv rebuilds can no longer dirty the index. Themes 2-3
(enrichment rewrites, events appends) and the upstream commit-cadence
automation gap remain open — signal status unchanged
(`symptom-repaired, upstream-pending`).
