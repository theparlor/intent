---
id: SIG-ULID-MIGRATION-AUDIT-2026-05-20
title: ULID migration audit — 86 legacy-named signals identified post-SPEC-003
type: signal
status: captured
confidence: 0.95
trust: 0.80
autonomy_level: L4
source: framework-self-audit-2026-05-20
date: '2026-05-20'
upstream_control_path: SIG-ULID-MIGRATION-AUDIT-2026-05-20.md (this file) — migration itself is a separate L4 Execute loop (rename 86 files); this signal is the Notice
catch_mechanism: file renaming is reversible via git revert; no catch-net required beyond git history
pipeline_survival: git-tracked; SPEC-003 remains the migration spec; this signal is the backpressure record
---

# ULID Migration Audit: 86 Legacy-Named Signals

## What Was Noticed

SPEC-003 (2026-04-09) mandated ULID-based IDs for all entity files: `{PREFIX}-{26-char-ulid}.md`.
As of 2026-05-20, the `.intent/signals/` directory contains:

| Naming convention | Count |
|---|---|
| `SIG-NNN` sequential (e.g., `SIG-031-workspace-hygiene-gap.md`) | **7** |
| Date-slug legacy (e.g., `2026-03-28-loop-too-slow.md`) | **79** |
| RETRO-prefix (retrospectives, pre-SPEC-003 pattern) | ~8 |
| ULID-format (correct per SPEC-003) | **0** |

**Total legacy-named signals: ~86 out of 131 total.**

New signals created after SPEC-003 (2026-04-09) that still use legacy naming:
- `SIG-031` through `SIG-037` — 7 sequential-style signals
- Multiple `SIG-*-2026-05-*` long-form date-prefixed signals (recent, still date-slug not ULID)

## Why This Signal Exists (Not Just a Task)

SPEC-003 established ULID migration as a ratified decision. The `bin/lib/id_gen.sh` library exists.
But 37+ days later, no migration has run and new signals continue to use legacy naming.

This signal creates the Notice for a dedicated migration Execute loop. It also surfaces the question: should new signal capture (via `intent-signal` CLI and MCP tools) auto-enforce ULID format, or should that wait for the migration to complete?

## IDD Loop Spec

**Notice:** This signal.
**Intent:** All signals in `.intent/signals/` use ULID naming; new signals auto-generate ULID IDs.

**Two sub-tasks (can parallelize):**

### Sub-task 1 — Rename existing files
- Generate a ULID for each legacy-named signal using `bin/lib/id_gen.sh`
- Rename `SIG-NNN-slug.md` → `SIG-{ulid}.md`
- Rename `YYYY-MM-DD-slug.md` → `SIG-{ulid}.md` (no legacy prefix for date-slugs)
- Update any cross-references in spec/intent files that reference the old filename
- Volume: ~86 files — use a Bash loop, not manual renaming

### Sub-task 2 — Enforce ULID in CLI + MCP
- Verify `bin/intent-signal` calls `generate_id SIG` from `bin/lib/id_gen.sh` (not sequential counter)
- Verify `tools/intent-mcp/server.py`'s `next_signal_id()` uses ULID (check `next_id()` function — currently uses sequential `next_id()` not ULID)
- Update `next_signal_id()` in `server.py` to use ULID generation

## Risk Assessment
- **Reversible:** yes — git revert restores original filenames
- **Blast radius:** medium — 86 file renames, potential cross-reference updates
- **Precedent:** SPEC-003 is the explicit precedent; this is executing a ratified spec
- **Info gap:** none — proceed is L4

## Do Not Rename Inline

This is a high-volume rename (86 files) that merits its own Execute session with verification.
Use `spawn-prompts/idd-build-execute.md` with this signal as Notice and Sub-tasks 1+2 as the DoD.
