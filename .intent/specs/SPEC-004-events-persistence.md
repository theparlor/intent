---
id: SPEC-004
title: "events.jsonl → SQLite+WAL persistence with explicit fsync"
status: draft
version: 1.0
author: brien
created_date: 2026-04-09T19:30:00Z
approved_date:
intent: INT-009
source_signals: [SIG-051]
related_specs: [SPEC-003]
priority: P0
interim_ship: "bin/intent-signal emit_event now has fsync + flock wrapper (2026-04-09)"
---

# SPEC-004 — events.jsonl → SQLite+WAL Persistence

## Problem Statement

Per INT-009 P0 #2 and the Engineering + ARB panel findings in the 2026-04-09
multi-panel review:

> **"Persistence story for events.jsonl — move from 'Phase 4 later' to
> SQLite+WAL with explicit fsync. Document restart semantics."**

The current event emission writes JSON lines to `.intent/events/events.jsonl`
via shell append (`echo >> file`) or Python file open/write. This has three
structural problems identified by the panels:

1. **No restart semantics.** A process killed mid-write can leave a partial
   JSON line. Downstream readers (dashboards, scripts, tests) will fail
   to parse and either silently drop events or crash.

2. **No multi-writer safety.** Two concurrent emitters (e.g., the GitHub
   Actions workflow + a local CLI run) can interleave lines. Shell append
   is atomic only for writes smaller than `PIPE_BUF` (4096 bytes on most
   systems), which our events happen to fit under but is not a guarantee.

3. **No query layer.** Every reader has to parse the entire JSONL file.
   The signals dashboard reads all events to compute counts. This is
   O(events) on every load. At 10K events this is still fast; at 1M it
   isn't.

4. **No durability guarantee.** File writes without `fsync` live in the
   OS page cache. A crash between write and flush loses data that the
   emitter believes was persisted. For a system that claims "events are
   the feedback loop," losing events silently is unacceptable.

5. **Git merge conflict generator.** `events.jsonl` in git with multiple
   committers produces line-level merge conflicts that are semantically
   wrong to resolve automatically. Two simultaneous captures should both
   persist — a merge resolver can't tell that.

## Solution Description

Replace the append-only JSONL file with a SQLite database at
`.intent/events/events.db` using Write-Ahead Logging (WAL) mode and
explicit fsync on commit.

**Storage model:**
- One table `events` with columns matching the existing JSONL schema
  (version, event, timestamp, trace_id, span_id, parent_id, source, data)
- `data` stored as TEXT containing JSON (SQLite JSON1 extension allows
  queries like `SELECT data->>'$.signal_id' FROM events`)
- Indexes on `timestamp`, `span_id`, `event` for common query patterns
- WAL mode for crash safety and multi-writer support
- `PRAGMA synchronous=FULL` + explicit `COMMIT` + `sqlite3_wal_checkpoint`
  at configurable intervals

**Legacy compatibility:**
- `.intent/events/events.jsonl` becomes a DERIVED export, not the source
  of truth. On each commit, the new entry is also appended to the JSONL
  file for backward compat with existing readers (the signals dashboard,
  the GitHub Actions workflow, any external scripts).
- A migration script (`bin/intent-events migrate`) walks the existing
  JSONL and imports all rows into the new DB. Idempotent (skips rows
  already present by timestamp+span_id composite key).
- The JSONL export can be regenerated from the DB at any time via
  `bin/intent-events export-jsonl`.

**New unified CLI:**
Create `bin/intent-event` (singular) as the canonical emitter:
- `intent-event emit --type signal.created --span SIG-xxx --data '{"..."}'`
- `intent-event query --since 2026-04-09 --type signal.created`
- `intent-event migrate` — one-time import from existing JSONL
- `intent-event export-jsonl` — regenerate legacy JSONL from DB
- `intent-event checkpoint` — force WAL checkpoint (for CI / backup)

Existing shell CLIs (`intent-signal`, `intent-intent`, `intent-spec`)
stop maintaining their own `emit_event` functions and shell out to
`bin/intent-event emit`. Python servers import from
`servers/events.py` which provides the same API.

## Interim ship (2026-04-09)

Before the full SQLite migration, a minimal safety wrapper is in place
in `bin/intent-signal emit_event()`:

- Uses `flock -x 200` to serialize concurrent writers when `flock` is
  available (Linux); falls back to POSIX single-line atomic append on
  macOS where `flock` is not standard
- Calls `sync` after each append for durability

This is NOT a replacement for the SQLite migration. It addresses the
immediate multi-writer race on macOS + Linux but does nothing for
restart semantics, query performance, or git merge conflicts.

## Implementation plan

### Phase 1 — Schema + migration (1-2 days)

1. Create `servers/events.py` with:
   - `init_db(path: Path) -> sqlite3.Connection` — opens DB, applies WAL,
     creates schema if missing
   - `emit_event(conn, version, event, timestamp, trace_id, span_id, parent_id, source, data) -> int` — inserts row, commits, returns row id
   - `query_events(conn, since=None, until=None, event_type=None, span_id=None) -> Iterable[dict]`
   - `migrate_from_jsonl(conn, jsonl_path: Path) -> int` — imports existing rows, returns count
   - `export_to_jsonl(conn, jsonl_path: Path) -> int` — writes all rows as JSONL
   - Self-test `__main__` block

2. Create `bin/intent-event` CLI that shells out to `servers/events.py`
   (or imports directly if running from a Python env). Subcommands
   mirror the Python API.

3. Schema (in `servers/events.py` or adjacent `.sql`):
```sql
CREATE TABLE IF NOT EXISTS events (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  version TEXT NOT NULL,
  event TEXT NOT NULL,
  timestamp TEXT NOT NULL,
  trace_id TEXT,
  span_id TEXT,
  parent_id TEXT,
  source TEXT NOT NULL,
  data TEXT NOT NULL,
  created_at TEXT NOT NULL DEFAULT (strftime('%Y-%m-%dT%H:%M:%fZ', 'now'))
);
CREATE INDEX IF NOT EXISTS idx_events_timestamp ON events(timestamp);
CREATE INDEX IF NOT EXISTS idx_events_span ON events(span_id);
CREATE INDEX IF NOT EXISTS idx_events_type ON events(event);
PRAGMA journal_mode=WAL;
PRAGMA synchronous=FULL;
```

### Phase 2 — Shell CLI integration (1 day)

4. Update `bin/intent-signal`, `bin/intent-intent`, `bin/intent-spec`:
   - Replace `emit_event()` function with `exec intent-event emit ...`
   - Keep JSONL fallback for the transition period — if `intent-event`
     CLI is not on PATH, fall back to the current fsync+flock wrapper
   - After the full migration, remove the JSONL fallback

### Phase 3 — Python server integration (1 day)

5. Update `servers/notice.py`, `servers/spec.py`, `tools/intent-mcp/server.py`:
   - Import `events` module
   - Replace JSON string building + append with `events.emit_event(conn, ...)`
   - Add connection lifecycle: one connection per server process, reused
     across tool calls

### Phase 4 — GitHub Actions integration (1 day)

6. Update `.github/workflows/intent-events.yml`:
   - Install sqlite3 (already available on ubuntu-latest)
   - Call `bin/intent-event emit` instead of shell append
   - After emission, run `bin/intent-event export-jsonl` to keep the
     JSONL mirror current (for readers that haven't migrated)

### Phase 5 — Dashboard migration (2-3 days)

7. Update `intent-site/docs/signals.html` to read from:
   - First preference: fetched endpoint that queries the DB
   - Fallback: the JSONL mirror (transition period)

### Phase 6 — JSONL deprecation (after all readers migrated)

8. Remove the JSONL mirror writes. JSONL becomes an on-demand export only.
9. Add a `.intent/events/events.jsonl.deprecated` notice file pointing
   readers at the DB + CLI.

## Acceptance Criteria

- [ ] `servers/events.py` passes self-test (smoke test + schema creation
  + emit + query + migrate + export)
- [ ] `bin/intent-event` CLI handles emit / query / migrate / export /
  checkpoint subcommands
- [ ] Concurrent-writer test: 10 shell processes emitting 100 events
  each produces exactly 1000 rows in the DB with zero data loss
- [ ] Crash test: kill the emitting process mid-batch and verify the DB
  contains all committed-before-kill events
- [ ] Migration from an existing `events.jsonl` (any size) is idempotent:
  running `intent-event migrate` twice produces the same row count
- [ ] `bin/intent-signal` capture events now go through `intent-event emit`
- [ ] Python server events go through `events.emit_event()`
- [ ] GitHub Actions workflow uses `intent-event emit`
- [ ] JSONL mirror stays in sync with DB (byte-identical on round-trip
  export) until deprecation phase
- [ ] Dashboard reads work from the DB (or JSONL fallback)
- [ ] Restart semantics documented: under what conditions is an event
  guaranteed persisted vs. lost

## Out of Scope

- **CRDT-based multi-repo replication.** Listed as P2 in INT-009. Git-
  based sync of the DB file is sufficient for v1.0 (SQLite DBs can be
  git-committed; merge conflicts on binary files are resolved by
  re-running migrate on the other side).
- **Event replay / rewind.** Time-travel querying is a nice-to-have,
  not a P0 requirement.
- **Event compression.** A busy Intent instance emitting 1000 events/day
  produces ~1 MB/year. Compression is not needed.
- **Event retention / GC.** Same reasoning — 1 MB/year. Retention can be
  a follow-up spec.

## Test Scenarios

1. **Concurrent writers** — 10 shell processes × 100 emits each. Expect
   1000 rows, no data loss, no line interleaving.

2. **Crash mid-batch** — emitter writes 500 events, get killed at event
   501. Expect exactly 500 rows in DB, no partial row 501.

3. **Migration idempotency** — run `intent-event migrate` twice against
   the same JSONL. Expect same row count after first and second run.

4. **Query performance** — query "all signals created this week" against
   a DB with 100K events. Expect <50ms.

5. **JSONL round-trip** — export DB to JSONL, clear DB, migrate from
   the exported JSONL. Expect identical row count.

6. **Backward compat** — the legacy JSONL file is still readable by the
   current signals dashboard during the transition phase.

## Dependencies

- **SQLite 3.7+** (ubiquitous; macOS bundled, Linux package manager)
- **Python 3.8+** (already required)
- No new external packages (SQLite is stdlib in Python)

## Open Questions

1. **Where does the DB live relative to git?** Options:
   - Committed (binary file in git) — history survives git clone
   - Gitignored (derived from JSONL mirror) — keeps git clean
   - Hybrid: DB gitignored, JSONL committed as the canonical log
   Recommendation: **hybrid** — JSONL stays as the canonical committed
   log until Phase 6, DB is derived and gitignored. This preserves
   git-native review + avoids binary conflicts.

2. **One DB per .intent/ tree, or one DB global?**
   Recommendation: **one per tree** — matches the current JSONL behavior
   and keeps per-repo isolation. Cross-tree queries are a future feature.

3. **Should the CLI block or buffer on emit?**
   Recommendation: **block** — block on fsync for durability guarantees.
   Buffering is a performance optimization that trades durability for
   throughput, which is the wrong trade for signals that must not be lost.

## Lineage

- **INT-009 P0 #2** — the panel-derived architectural hardening backlog
- **SIG-051** — consolidated architecture hardening signal
- **ARB panel 2026-04-09** — "not production-ready" verdict on current persistence
- **Engineering panel 2026-04-09** — same finding, cited as blocking for team pilot
- **DEC-20260409-02 Answer 5d** — measurability-as-prerequisite principle
- **DORA / Accelerate (Forsgren)** — the argument that signals must be
  reliable for the feedback loop to drive improvement
- **Write-Ahead Logging** — SQLite canonical docs on durability
