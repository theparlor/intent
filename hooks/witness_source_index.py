#!/usr/bin/python3
"""witness_source_index.py: a small daily index of Witness events per product.

Why it exists
-------------
The WS-DDR-098 recorder hook (hooks/signal-recorder-silent-check.sh) has to say whether
a product has sent any event to Witness in the last 30 days. It runs before every Write
and Edit, so it cannot read the Witness store (about 1.3 GB of JSONL, 60 to 240 MB a
day). This builder reads the store out of band, at most once a day, and writes a small
JSON index the hook reads in a millisecond.

What it reads
-------------
Every *.jsonl file in the Witness events store, by default
$HOME/Workspaces/Core/products/witness/farm/events-store (override WITNESS_EVENTS_STORE).
Each line is one envelope: {"event_id", "ingested_at", "source_system", "event": {"ts",
"product", "event", "attributes", "source": {"system"}}}.

Product identity is read from event.product, falling back to source_system when an event
carries no product. source_system names the ingest channel, not the product: the
intent-events adapter carries every product's .intent/events file under source_system
"intent" and sets event.product from that file's declared_source, and the Signalbox
Exchange adapter carries both "signalbox" and "exchange" under "signalbox-exchange".
Matching on source_system would make the Intent framework look active on behalf of every
other product, so the hook matches names against the product key only. The index keeps a
per-source_system table too, for reading.

Activity time is event.ts, falling back to ingested_at when ts is missing, unparseable,
or more than a day after ingestion. Backfilled events (Loom records from May, Gauntlet
sessions from June, ingested on 2026-09-25) therefore count at the time the product
acted, not the time Witness caught up.

How it builds
-------------
Incrementally. A state file remembers, per store file, the byte offset read so far, a
hash of the first 4 KB already read, and that file's per-product totals and per-day counts. A run
reads only bytes appended since the last run and files it has not seen; a file that
shrank or whose head changed is re-read from zero. The first run reads the whole store
(all history, so "last event" is known even for products silent for months).

Runs hold an exclusive non-blocking lock; a second run while one is going exits 0 at
once. Without --force a run exits 0 when the index is less than 24 hours old, so the
hook can kick it freely and it still builds at most once a day.

Files (all outside git; override the index path with WITNESS_SOURCE_INDEX):
  index  $HOME/.claude/state/witness-source-index.json        (what the hook reads)
  state  $HOME/.claude/state/witness-source-index.json.state  (builder bookkeeping)
  lock   $HOME/.claude/state/witness-source-index.json.lock
  kick   $HOME/.claude/state/witness-source-index.json.kick   (hook's hourly kick stamp)
  log    $HOME/.claude/logs/witness-source-index.log

Usage
-----
  /usr/bin/python3 witness_source_index.py            # build if older than 24 h
  /usr/bin/python3 witness_source_index.py --force    # build now
  /usr/bin/python3 witness_source_index.py --report [ROOT ...] [--json]
      # two tables, read from the index only. First, every product under ROOT (default:
      # Core/products and Core/frameworks in $HOME/Workspaces) that declares
      # lambda_settings or autonomy_grants, with the names checked, last Witness event,
      # 30-day count and verdict. Second, field conformance (WS-DDR-150) for every name
      # in the index with events in the last 30 days, rule-bound and legacy apart, and
      # whether a session editing that product would be told.

Product names (the witness_source_system key)
---------------------------------------------
A product's .intent/INTENT.md may declare which Witness names are its own:

  witness_source_system: fieldbook
  witness_source_system: [signalbox, exchange]
  witness_source_system:
    - signalbox
    - exchange

When absent, the name is the product's directory name, with a session-kit worktree
suffix removed ("intent-wt-2026-09-25-task" reads as "intent") and a Claude desktop
worktree read as the repo that holds it. Matching ignores case.

No actions of its own (the witness_actions key)
-----------------------------------------------
WS-DDR-150 asks every product that acts to report its actions. A product with nothing
that acts (a content or methodology repo: markdown only, no scripts, hooks, jobs or
servers) says so, with a named reason, at column 0 in .intent/INTENT.md:

  witness_actions: none (content repo, markdown only, no scripts hooks jobs or servers)

The reason in parentheses is required; a bare "witness_actions: none" is not a
declaration and the product stays silent until someone names why. The report shows such
a product as "no-actions" with its reason instead of "silent", and the hook skips it
(telemetry detection no-actions-declared). Events still win: a product that declares no
actions but has Witness events in the window reads as active.

Field lint (WS-DDR-150, added 2026-09-26, QMT-01M3F5JWBR8XPK9YGB7HTMCBNP)
-----------------------------------------------------------------------
WS-DDR-150 says every event carries a minimum set of fields. While it reads each line
the builder also checks it against that set, and keeps per product and per day how many
events it saw, how many miss at least one field, and how often each field is missing.
The index then carries, per product, a lint_30d block over the same 30 days as
count_30d, split into two classes (below), each with events, nonconformant, missing
(field: count) and most_missing. The fields:

  ts              a timestamp with an explicit timezone (Z or +hh:mm); null, missing
                  or zone-less times fail
  product, event  event.product and event.event, non-empty (the event's own field,
                  not the source_system fallback the index uses for identity)
  caller, machine, outcome, duration_ms, run_id
                  present and non-empty in event.attributes
  redaction_level only for engagement work: when any top-level attribute string names
                  a path under Work/<kind>/Engagements/, the event must carry
                  redaction_level: client-confidential

Presence is checked, not values (emit.py already refuses a bad outcome). redaction_level
is the exception, because a wrong value on client work is the leak decision point 5 of
the rule guards against.

OTLP-shaped events (Fieldbook, Conduit, Witness's own spans) are read the way the rule's
decision surface maps them: span name is the event, service.name or a product span
attribute is the product, span and resource attributes are the rest, and four
span-native fields count as their equivalents because every span carries them:
startTimeUnixNano for ts (epoch nanoseconds are absolute), start and end times for
duration_ms, a 32-hex traceId for run_id, a set status.code (not UNSET) for outcome.
host.name stands in for machine.

Legacy versus rule-bound. Each event is put in one of two classes from the event itself,
so there is no list of products to keep current:

  legacy      source_system is screenpipe, cc-native or entire-io (capture channels that
              record other programs' activity in those tools' own formats: screen
              frames, Claude transcripts, Entire traces), or the event carries
              attributes.adapter (Witness's stream adapters, intent-events-jsonl,
              loom-records, signalbox-events and exchange-events, stamp it on every line
              they translate from a product's older log, which never had these fields;
              the emit.py path, ingest_jsonl, never stamps it)
  rule-bound  everything else: events a program wrote itself, through emit.py and the
              watcher, Quartermaster's audit push, Fieldbook's emitter, Witness's own
              linker and watcher, or OTLP spans

--report prints both classes. Only rule-bound events can raise the hook's session note:
a product with no rule-bound event in the window is never told about fields. One
consequence: a product that reports only by appending lines to its .intent/events file
arrives through the intent-events adapter, so it is legacy and never linted; emit.py is
the rule's path, and the hook's notes say so.

The state file carries lint_version. A state without it (written before the lint) is
set aside, so the first build after an upgrade re-reads the whole store once; later
builds stay incremental.

Its own events
--------------
Every build run (built, fresh, locked, no store, error) reports itself to Witness through
emit.py as product intent, event job.run, job witness-source-index, with its counts: this
is the lint pass's own event. The caller is WITNESS_CALLER when set (the hook sets
hook:signal-recorder-silent-check when it starts a build), else manual:<user>. Emitting
is fail-open: when emit.py is absent (a machine without Witness) nothing is said; when it
fails, one line goes to stderr and the build's result stands. WITNESS_EMIT overrides the
emit.py path; WITNESS_INBOX (read by emit.py) redirects the inbox, which the tests use.
--report is a read and emits nothing.

The hook imports the small pure functions below (names, lookup, timestamps, lint,
emit_action); keep this module's top-level imports light, because every Write and Edit
pays for them.
"""
from __future__ import annotations

import json
import os
import re
import sys
import time

SCHEMA = "witness-source-index/1"
LINT_VERSION = 1
WINDOW_DAYS = 30
REFRESH_EVERY_S = 24 * 3600
KICK_EVERY_S = 3600
KEEP_DAYS = WINDOW_DAYS + 2
HEAD_BYTES = 4096
DAY_S = 86400

DECLARES_RE = re.compile(r"^(lambda_settings|autonomy_grants):", re.M)
NO_ACTIONS_RE = re.compile(r"^witness_actions:[ \t]*(.*)$", re.M)
_NO_ACTIONS_VALUE = re.compile(r"^none\s*\((.*\S.*)\)\s*(#.*)?$", re.I)
_WT_SUFFIX = re.compile(r"^(.+?)-wt-.+$")
_TS_RE = re.compile(
    r"(\d{4})-(\d{2})-(\d{2})[T ](\d{2}):(\d{2}):(\d{2})(\.\d+)?\s*(Z|z|[+-]\d{2}:?\d{2})?$")

# WS-DDR-150 minimum event (see "Field lint" above).
REQUIRED_FIELDS = ("ts", "product", "event", "caller", "machine", "outcome", "duration_ms", "run_id")
ENGAGEMENT_FIELD = "redaction_level"
FIELD_ORDER = REQUIRED_FIELDS + (ENGAGEMENT_FIELD,)
LEGACY_SOURCE_SYSTEMS = frozenset({"screenpipe", "cc-native", "entire-io"})
MOSTLY = 0.5  # a session is told when more than this share of rule-bound events miss a field
LINT_CLASSES = ("rule", "legacy")
_ENGAGEMENT_RE = re.compile(r"(?:^|/)Work/[^/]+/Engagements/")
_TRACE_RE = re.compile(r"^[0-9a-f]{32}$")
_UNSET_STATUS = (None, "", 0, "0", "STATUS_CODE_UNSET", "UNSET")
EMIT_PRODUCT = "intent"


# ------------------------------------------------------------------ paths

def home() -> str:
    return os.environ.get("HOME") or os.path.expanduser("~")


def store_dir() -> str:
    return os.environ.get("WITNESS_EVENTS_STORE") or os.path.join(
        home(), "Workspaces", "Core", "products", "witness", "farm", "events-store")


def index_path() -> str:
    return os.environ.get("WITNESS_SOURCE_INDEX") or os.path.join(
        home(), ".claude", "state", "witness-source-index.json")


def log_path() -> str:
    return os.path.join(home(), ".claude", "logs", "witness-source-index.log")


# ------------------------------------------------------------------ shared with the hook

def _parse_ts(value):
    """(epoch seconds or None, True when the text carries an explicit timezone)."""
    if not isinstance(value, str):
        return None, False
    m = _TS_RE.match(value.strip())
    if not m:
        return None, False
    import calendar
    y, mo, d, h, mi, s = (int(x) for x in m.groups()[:6])
    try:
        epoch = calendar.timegm((y, mo, d, h, mi, s, 0, 0, 0))
    except (ValueError, OverflowError):
        return None, False
    if m.group(7):
        epoch += float(m.group(7))
    tz = m.group(8)
    if tz and tz not in ("Z", "z"):
        t = tz[1:].replace(":", "")
        off = int(t[:2]) * 3600 + int(t[2:4]) * 60
        epoch -= off if tz[0] == "+" else -off
    return float(epoch), bool(tz)


def parse_ts(value) -> float | None:
    """ISO 8601 text to epoch seconds (UTC when no offset). None when unparseable."""
    return _parse_ts(value)[0]


def iso(epoch: float | None) -> str | None:
    if epoch is None:
        return None
    return time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime(epoch))


def declares_autonomy(intent_md_text: str) -> bool:
    return bool(DECLARES_RE.search(intent_md_text or ""))


def _clean_name(raw: str) -> str:
    s = raw.strip()
    if " #" in s:
        s = s.split(" #", 1)[0].strip()
    return s.strip("'\"").strip()


def declared_names(intent_md_text: str) -> list[str]:
    """Names from a witness_source_system: line (scalar, flow list or block list)."""
    lines = (intent_md_text or "").splitlines()
    for i, line in enumerate(lines):
        if not line.startswith("witness_source_system:"):
            continue
        rest = line.split(":", 1)[1].strip()
        if rest.startswith("#"):
            rest = ""
        if rest.startswith("["):
            items = rest.split("]", 1)[0].lstrip("[").split(",")
        elif rest:
            items = [rest]
        else:
            items = []
            for nxt in lines[i + 1:]:
                s = nxt.strip()
                if s.startswith("- "):
                    items.append(s[2:])
                elif s == "" or s.startswith("#"):
                    continue
                else:
                    break
        names = []
        for item in items:
            n = _clean_name(item)
            if n and n not in names:
                names.append(n)
        return names
    return []


def declared_no_actions(intent_md_text: str) -> str | None:
    """The named reason from a 'witness_actions: none (<reason>)' line at column 0, else None.

    None also when the key is absent, its value is not 'none', or the reason is empty:
    only a named reason takes a product off the silent list."""
    m = NO_ACTIONS_RE.search(intent_md_text or "")
    if not m:
        return None
    value = m.group(1).strip()
    if len(value) >= 2 and value[0] == value[-1] and value[0] in "'\"":
        value = value[1:-1].strip()
    v = _NO_ACTIONS_VALUE.match(value)
    if not v:
        return None
    reason = v.group(1).strip()
    return reason or None


def default_name(product_root: str) -> str:
    """Directory name of the product, worktree suffixes read back to the repo name."""
    root = os.path.normpath(product_root)
    marker = os.sep + ".claude" + os.sep + "worktrees" + os.sep
    if marker in root:
        root = root.split(marker, 1)[0]
    base = os.path.basename(root)
    m = _WT_SUFFIX.match(base)
    return m.group(1) if m else base


def product_names(product_root: str, intent_md_text: str) -> tuple[list[str], str]:
    """(names, how) where how is 'declared' or 'default'."""
    names = declared_names(intent_md_text)
    if names:
        return names, "declared"
    return [default_name(product_root)], "default"


def load_index(path: str | None = None):
    """(index, problem). problem is None, 'missing' or 'malformed'."""
    path = path or index_path()
    try:
        with open(path, "r", encoding="utf-8") as fh:
            data = json.load(fh)
    except FileNotFoundError:
        return None, "missing"
    except Exception:
        return None, "malformed"
    if (not isinstance(data, dict) or data.get("schema") != SCHEMA
            or not isinstance(data.get("products"), dict)
            or not isinstance(data.get("built_at_epoch"), (int, float))):
        return None, "malformed"
    return data, None


def lookup(index: dict, names: list[str]) -> dict:
    """Merge the index rows for names: last event epoch, 30-day count, names that matched,
    and the field lint (None when no matched row carries lint_30d, an index built before
    the lint existed)."""
    products = index.get("products") or {}
    last, count, matched, lint = None, 0, [], None
    for n in names:
        row = products.get(n.lower())
        if not isinstance(row, dict):
            continue
        matched.append(n)
        e = row.get("last_event_epoch")
        if isinstance(e, (int, float)) and (last is None or e > last):
            last = float(e)
        c = row.get("count_30d")
        if isinstance(c, int):
            count += c
        block = row.get("lint_30d")
        if isinstance(block, dict):
            if lint is None:
                lint = {k: [0, 0, {}] for k in LINT_CLASSES}
            for klass in LINT_CLASSES:
                b = block.get(klass) if isinstance(block.get(klass), dict) else {}
                acc = lint[klass]
                acc[0] += b.get("events") if isinstance(b.get("events"), int) else 0
                acc[1] += b.get("nonconformant") if isinstance(b.get("nonconformant"), int) else 0
                for f, k in (b.get("missing") or {}).items():
                    if isinstance(k, int):
                        acc[2][f] = acc[2].get(f, 0) + k
    return {"last_event_epoch": last, "count_30d": count, "matched": matched,
            "lint": None if lint is None else {k: lint_block(*v) for k, v in lint.items()}}


# ------------------------------------------------------------------ field lint (WS-DDR-150)

def _present(v) -> bool:
    return v is not None and v != "" and v != [] and v != {}


def _names_engagement(attrs: dict) -> bool:
    for v in attrs.values():
        if isinstance(v, str) and "Engagements/" in v and _ENGAGEMENT_RE.search(v):
            return True
    return False


def _nanos(v) -> bool:
    if isinstance(v, bool):
        return False
    if isinstance(v, int):
        return v > 0
    return isinstance(v, str) and v.isdigit() and int(v) > 0


def _otlp_kv(items) -> dict:
    out = {}
    if isinstance(items, list):
        for it in items:
            if isinstance(it, dict) and isinstance(it.get("key"), str):
                val = it.get("value")
                out[it["key"]] = next(iter(val.values())) if isinstance(val, dict) and val else val
    return out


def _lint_otlp(ev: dict) -> list:
    rs = ev
    if isinstance(ev.get("resourceSpans"), list):
        first = ev["resourceSpans"][0] if ev["resourceSpans"] else None
        rs = first if isinstance(first, dict) else {}
    res = rs.get("resource") if isinstance(rs.get("resource"), dict) else {}
    attrs = _otlp_kv(res.get("attributes"))
    service = attrs.get("service.name")
    span = {}
    scopes = rs.get("scopeSpans")
    if isinstance(scopes, list) and scopes and isinstance(scopes[0], dict):
        spans = scopes[0].get("spans")
        if isinstance(spans, list) and spans and isinstance(spans[0], dict):
            span = spans[0]
    attrs.update(_otlp_kv(span.get("attributes")))
    start, end = span.get("startTimeUnixNano"), span.get("endTimeUnixNano")
    status = span.get("status") if isinstance(span.get("status"), dict) else {}
    trace = span.get("traceId")
    missing = []
    if not _nanos(start):
        missing.append("ts")
    if not (_present(attrs.get("product")) or _present(service)):
        missing.append("product")
    if not _present(span.get("name")):
        missing.append("event")
    if not _present(attrs.get("caller")):
        missing.append("caller")
    if not (_present(attrs.get("machine")) or _present(attrs.get("host.name"))):
        missing.append("machine")
    if not (_present(attrs.get("outcome")) or status.get("code") not in _UNSET_STATUS):
        missing.append("outcome")
    if not (_present(attrs.get("duration_ms")) or (_nanos(start) and _nanos(end))):
        missing.append("duration_ms")
    if not (_present(attrs.get("run_id"))
            or (isinstance(trace, str) and _TRACE_RE.match(trace) and trace != "0" * 32)):
        missing.append("run_id")
    if _names_engagement(attrs) and attrs.get(ENGAGEMENT_FIELD) != "client-confidential":
        missing.append(ENGAGEMENT_FIELD)
    return missing


def _lint(ev: dict, source_system, ts_ok: bool) -> tuple:
    otlp = "scopeSpans" in ev or "resourceSpans" in ev
    attrs = ev.get("attributes")
    if not isinstance(attrs, dict):
        attrs = {}
    legacy = source_system in LEGACY_SOURCE_SYSTEMS or (not otlp and _present(attrs.get("adapter")))
    klass = "legacy" if legacy else "rule"
    if otlp:
        return klass, _lint_otlp(ev)
    missing = []
    if not ts_ok:
        missing.append("ts")
    p = ev.get("product")
    if not (isinstance(p, str) and p.strip()):
        missing.append("product")
    e = ev.get("event")
    if not (isinstance(e, str) and e.strip()):
        missing.append("event")
    for f in ("caller", "machine", "outcome", "duration_ms", "run_id"):
        if not _present(attrs.get(f)):
            missing.append(f)
    if _names_engagement(attrs) and attrs.get(ENGAGEMENT_FIELD) != "client-confidential":
        missing.append(ENGAGEMENT_FIELD)
    return klass, missing


def lint_event(ev, source_system=None) -> tuple:
    """(class, missing) for one stored event (the envelope's "event" object). class is
    "rule" or "legacy"; missing lists the WS-DDR-150 minimum fields it lacks, in order."""
    if not isinstance(ev, dict):
        ev = {}
    ss = source_system.strip().lower() if isinstance(source_system, str) else None
    epoch, has_tz = _parse_ts(ev.get("ts"))
    return _lint(ev, ss, epoch is not None and has_tz)


def most_missing(missing: dict):
    """The most often missing field; ties go to the earlier field in the rule's order."""
    best = None
    for f in FIELD_ORDER:
        k = missing.get(f, 0)
        if k and (best is None or k > missing[best]):
            best = f
    return best


def lint_block(events: int, bad: int, missing: dict) -> dict:
    ordered = {f: missing[f] for f in FIELD_ORDER if missing.get(f)}
    for f in sorted(missing):
        if f not in ordered and missing[f]:
            ordered[f] = missing[f]
    return {"events": events, "nonconformant": bad, "missing": ordered, "most_missing": most_missing(ordered)}


def mostly_nonconformant(block) -> bool:
    """True when more than half of a lint block's events miss a field."""
    if not isinstance(block, dict):
        return False
    n, bad = block.get("events"), block.get("nonconformant")
    return isinstance(n, int) and isinstance(bad, int) and n > 0 and bad / n > MOSTLY


# ------------------------------------------------------------------ its own events (WS-DDR-150)

_EMIT_MOD = None


def emit_path() -> str:
    return os.environ.get("WITNESS_EMIT") or os.path.join(
        home(), "Workspaces", "Core", "products", "witness", "src", "emit.py")


def default_caller() -> str:
    return os.environ.get("WITNESS_CALLER") or "manual:" + (os.environ.get("USER") or "unknown")


def emit_action(event: str, **fields) -> bool:
    """Report one action of this tool to Witness through emit.py, as product intent.
    Never raises. Quiet when emit.py is absent; one stderr line when it is present but
    cannot be loaded (emit.py prints its own line when a write fails)."""
    global _EMIT_MOD
    try:
        if _EMIT_MOD is None:
            path = emit_path()
            if not os.path.isfile(path):
                return False
            import importlib.util
            spec = importlib.util.spec_from_file_location("witness_emit", path)
            mod = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(mod)
            _EMIT_MOD = mod
        return bool(_EMIT_MOD.emit(EMIT_PRODUCT, event, **fields))
    except (Exception, SystemExit) as exc:
        try:
            print(f"witness-emit: not recorded ({type(exc).__name__}: {exc})", file=sys.stderr)
        except Exception:
            pass
        return False


# ------------------------------------------------------------------ builder

def _log(msg: str) -> None:
    try:
        os.makedirs(os.path.dirname(log_path()), exist_ok=True)
        with open(log_path(), "a", encoding="utf-8") as fh:
            fh.write(f"{iso(time.time())} {msg}\n")
    except Exception:
        pass


def _atomic_write_json(path: str, data) -> None:
    os.makedirs(os.path.dirname(path), exist_ok=True)
    tmp = f"{path}.tmp.{os.getpid()}"
    with open(tmp, "w", encoding="utf-8") as fh:
        json.dump(data, fh, separators=(",", ":"), sort_keys=True)
    os.replace(tmp, path)


def _head_hash(path: str, length: int) -> str:
    """Hash of the first length bytes: the part of the file already read, up to 4 KB."""
    import hashlib
    with open(path, "rb") as fh:
        return hashlib.sha1(fh.read(length)).hexdigest()


def _bump(table: dict, key: str, epoch: float | None, day: str | None, via: str | None,
          lint: tuple | None = None) -> None:
    row = table.get(key)
    if row is None:
        row = table[key] = {"last": None, "total": 0, "days": {}, "via": {}}
    row["total"] += 1
    if epoch is not None:
        if row["last"] is None or epoch > row["last"]:
            row["last"] = epoch
        if day is not None:
            row["days"][day] = row["days"].get(day, 0) + 1
    if via is not None:
        row["via"][via] = row["via"].get(via, 0) + 1
    if lint is not None and day is not None:
        klass, missing = lint
        per_day = row.setdefault("lint", {}).setdefault(klass, {})
        d = per_day.get(day)
        if d is None:
            d = per_day[day] = {"n": 0, "bad": 0, "miss": {}}
        d["n"] += 1
        if missing:
            d["bad"] += 1
            m = d["miss"]
            for f in missing:
                m[f] = m.get(f, 0) + 1


def _scan(path: str, start: int, rec: dict, oldest_day: str) -> tuple[int, int, int]:
    """Read complete lines from start; fold them into rec. Returns (new_offset, events, bad).

    A last line with no newline is left for the next run while the file is still being
    written (modified in the last hour), and read as complete once the file has settled."""
    products, systems = rec["products"], rec["systems"]
    try:
        settled = time.time() - os.path.getmtime(path) > 3600
    except OSError:
        settled = False
    day_cache: dict[int, str] = {}
    events = bad = 0
    offset = start
    with open(path, "rb") as fh:
        fh.seek(start)
        for line in fh:
            if not line.endswith(b"\n") and not settled:
                break  # a line still being written; read it next run
            offset += len(line)
            if not line.strip():
                continue
            try:
                env = json.loads(line)
            except Exception:
                bad += 1
                continue
            if not isinstance(env, dict):
                bad += 1
                continue
            events += 1
            ev = env.get("event") if isinstance(env.get("event"), dict) else {}
            ss = env.get("source_system")
            ss = ss.strip().lower() if isinstance(ss, str) and ss.strip() else None
            prod = ev.get("product")
            prod = prod.strip().lower() if isinstance(prod, str) and prod.strip() else ss
            ing = parse_ts(env.get("ingested_at"))
            act, has_tz = _parse_ts(ev.get("ts"))
            lint = _lint(ev, ss, act is not None and has_tz)
            if act is None or (ing is not None and act > ing + DAY_S):
                act = ing
            day = None
            if act is not None:
                dn = int(act // DAY_S)
                day = day_cache.get(dn)
                if day is None:
                    day = day_cache[dn] = time.strftime("%Y-%m-%d", time.gmtime(dn * DAY_S))
                if day < oldest_day:
                    day = None
            if prod is not None:
                _bump(products, prod, act, day, ss, lint)
            if ss is not None:
                _bump(systems, ss, act, day, None)
    return offset, events, bad


def _prune_days(rec: dict, oldest_day: str) -> None:
    for table in (rec.get("products", {}), rec.get("systems", {})):
        for row in table.values():
            row["days"] = {d: n for d, n in row.get("days", {}).items() if d >= oldest_day}
            lint = row.get("lint")
            if lint:
                for klass in list(lint):
                    lint[klass] = {d: v for d, v in lint[klass].items() if d >= oldest_day}


def _aggregate(files: dict, window_start_day: str) -> tuple[dict, dict]:
    out = {"products": {}, "systems": {}}
    for rec in files.values():
        for kind in ("products", "systems"):
            for key, row in rec.get(kind, {}).items():
                agg = out[kind].setdefault(key, {"last": None, "total": 0, "count_30d": 0, "via": {}})
                agg["total"] += row.get("total", 0)
                last = row.get("last")
                if last is not None and (agg["last"] is None or last > agg["last"]):
                    agg["last"] = last
                agg["count_30d"] += sum(n for d, n in row.get("days", {}).items() if d >= window_start_day)
                for v, n in row.get("via", {}).items():
                    agg["via"][v] = agg["via"].get(v, 0) + n
                if kind == "products":
                    lint = agg.setdefault("lint", {k: [0, 0, {}] for k in LINT_CLASSES})
                    for klass, days in (row.get("lint") or {}).items():
                        acc = lint.setdefault(klass, [0, 0, {}])
                        for d, v in days.items():
                            if d < window_start_day:
                                continue
                            acc[0] += v["n"]
                            acc[1] += v["bad"]
                            for f, k in v["miss"].items():
                                acc[2][f] = acc[2].get(f, 0) + k

    def shape(table: dict, with_via: bool) -> dict:
        shaped = {}
        for key, a in sorted(table.items()):
            row = {"last_event": iso(a["last"]), "last_event_epoch": a["last"],
                   "count_30d": a["count_30d"], "count_total": a["total"]}
            if with_via:
                row["source_systems"] = dict(sorted(a["via"].items()))
                lint = a.get("lint") or {k: [0, 0, {}] for k in LINT_CLASSES}
                row["lint_30d"] = {k: lint_block(*lint.get(k, [0, 0, {}])) for k in LINT_CLASSES}
            shaped[key] = row
        return shaped

    return shape(out["products"], True), shape(out["systems"], False)


def build(force: bool = False, quiet: bool = False) -> int:
    """Build the index (see the module docstring), then report the run to Witness."""
    t0 = time.time()
    result = {"outcome": "error", "reason": "exception"}
    try:
        return _build(force, quiet, result)
    finally:
        fields = {k: v for k, v in result.items() if k != "outcome"}
        emit_action("job.run", caller=default_caller(), outcome=result["outcome"],
                    duration_ms=(time.time() - t0) * 1000, target="witness-source-index",
                    job="witness-source-index", force=bool(force), **fields)


def _build(force: bool, quiet: bool, result: dict) -> int:
    idx_path, store = index_path(), store_dir()
    say = (lambda m: None) if quiet else (lambda m: print(m))
    os.makedirs(os.path.dirname(idx_path), exist_ok=True)
    import fcntl
    lock_fh = open(idx_path + ".lock", "a")
    try:
        fcntl.flock(lock_fh, fcntl.LOCK_EX | fcntl.LOCK_NB)
    except OSError:
        say("another build holds the lock; nothing to do")
        _log("skip locked")
        result.update(outcome="skipped", reason="locked")
        return 0
    try:
        if not force:
            current, problem = load_index(idx_path)
            if problem is None and time.time() - current["built_at_epoch"] < REFRESH_EVERY_S:
                say(f"index is fresh (built {current.get('built_at')}); use --force to rebuild")
                result.update(outcome="skipped", reason="fresh")
                return 0
        if not os.path.isdir(store):
            say(f"no Witness store at {store}; index not built")
            _log(f"skip store-absent store={store}")
            result.update(outcome="skipped", reason="store-absent")
            return 0
        t0 = time.time()
        now = t0
        oldest_day = time.strftime("%Y-%m-%d", time.gmtime(now - KEEP_DAYS * DAY_S))
        window_day = time.strftime("%Y-%m-%d", time.gmtime(now - WINDOW_DAYS * DAY_S))
        state_path = idx_path + ".state"
        try:
            with open(state_path, "r", encoding="utf-8") as fh:
                state = json.load(fh)
            if not isinstance(state, dict) or state.get("schema") != SCHEMA or state.get("store") != store:
                state = None
        except Exception:
            state = None
        full_reread = state is not None and state.get("lint_version") != LINT_VERSION
        if full_reread:
            state = None  # written before the field lint: read the whole store once
        files = (state or {}).get("files") or {}
        present = sorted(n for n in os.listdir(store) if n.endswith(".jsonl"))
        files = {n: r for n, r in files.items() if n in present}
        read_bytes = events = bad = rescanned = 0
        for name in present:
            path = os.path.join(store, name)
            try:
                size = os.path.getsize(path)
                rec = files.get(name)
                if rec is not None:
                    head_len = min(HEAD_BYTES, rec.get("offset", 0))
                    if (size < rec.get("offset", 0) or rec.get("head_len") != head_len
                            or rec.get("head") != _head_hash(path, head_len)):
                        rescanned += 1
                        rec = None
                if rec is None:
                    rec = {"offset": 0, "products": {}, "systems": {}}
                if size > rec["offset"]:
                    start = rec["offset"]
                    rec["offset"], n_ev, n_bad = _scan(path, start, rec, oldest_day)
                    read_bytes += rec["offset"] - start
                    events += n_ev
                    bad += n_bad
                rec["head_len"] = min(HEAD_BYTES, rec["offset"])
                rec["head"] = _head_hash(path, rec["head_len"])
            except OSError:
                continue
            _prune_days(rec, oldest_day)
            files[name] = rec
        products, systems = _aggregate(files, window_day)
        rule_events = sum(p["lint_30d"]["rule"]["events"] for p in products.values())
        rule_bad = sum(p["lint_30d"]["rule"]["nonconformant"] for p in products.values())
        mostly_bad = sorted(k for k, p in products.items() if mostly_nonconformant(p["lint_30d"]["rule"]))
        built = time.time()
        index = {
            "schema": SCHEMA,
            "built_at": iso(built),
            "built_at_epoch": built,
            "store": store,
            "window_days": WINDOW_DAYS,
            "identity": "event.product, else source_system; lower-cased",
            "activity_time": "event.ts, else ingested_at (also when ts is over a day past ingestion)",
            "store_files": len(present),
            "build": {"seconds": round(built - t0, 2), "bytes_read": read_bytes,
                      "events_read": events, "unparseable_lines": bad, "files_rescanned": rescanned},
            "lint": {
                "rule": "WS-DDR-150",
                "version": LINT_VERSION,
                "window_days": WINDOW_DAYS,
                "required": list(REQUIRED_FIELDS),
                "engagement": "redaction_level: client-confidential when an attribute names a path "
                              "under Work/<kind>/Engagements/",
                "legacy": "source_system screenpipe, cc-native or entire-io, or attributes.adapter "
                          "set; counted and reported, never a session note",
                "mostly": MOSTLY,
            },
            "products": products,
            "source_systems": systems,
        }
        _atomic_write_json(state_path, {"schema": SCHEMA, "lint_version": LINT_VERSION,
                                        "store": store, "files": files})
        _atomic_write_json(idx_path, index)
        _log(f"built products={len(products)} files={len(present)} bytes_read={read_bytes} "
             f"events_read={events} bad={bad} seconds={round(built - t0, 2)} full_reread={full_reread} "
             f"rule_events_30d={rule_events} rule_nonconformant_30d={rule_bad}")
        result.update(outcome="ok", reason="built", products=len(products), store_files=len(present),
                      bytes_read=read_bytes, events_read=events, unparseable_lines=bad,
                      files_rescanned=rescanned, full_reread=full_reread,
                      rule_events_30d=rule_events, rule_nonconformant_30d=rule_bad,
                      mostly_nonconformant=len(mostly_bad))
        say(f"index built: {len(products)} products, {len(present)} store files, "
            f"{read_bytes} bytes read, {events} events read in {round(built - t0, 2)} s, written to {idx_path}")
        return 0
    finally:
        try:
            fcntl.flock(lock_fh, fcntl.LOCK_UN)
            lock_fh.close()
        except Exception:
            pass


# ------------------------------------------------------------------ report

def _declaring_products(roots: list[str]) -> list[str]:
    found = []
    for root in roots:
        if os.path.isfile(os.path.join(root, ".intent", "INTENT.md")):
            candidates = [root]
        else:
            try:
                candidates = [os.path.join(root, n) for n in sorted(os.listdir(root))]
            except OSError:
                continue
        for c in candidates:
            base = os.path.basename(c)
            if base.startswith(("_", ".")) or "-wt-" in base:
                continue
            md = os.path.join(c, ".intent", "INTENT.md")
            try:
                with open(md, "r", encoding="utf-8", errors="replace") as fh:
                    text = fh.read()
            except OSError:
                continue
            if declares_autonomy(text):
                found.append(c)
    return found


def conformance_rows(index: dict, declaring: list[dict]) -> list[dict]:
    """One row per Witness name with events in the window: its rule-bound and legacy lint,
    the declaring product that owns the name (if any), and what the hook would tell a
    session editing that product."""
    owners: dict = {}
    for r in declaring:
        for n in r["names"]:
            owners.setdefault(n.lower(), r)
    out = []
    for key, prow in sorted((index.get("products") or {}).items()):
        block = prow.get("lint_30d") if isinstance(prow, dict) else None
        if not isinstance(block, dict):
            continue
        rule = block.get("rule") or {}
        legacy = block.get("legacy") or {}
        if not (rule.get("events") or legacy.get("events")):
            continue
        owner = owners.get(key)
        if owner is None:
            note = "no: not a product that declares autonomy settings"
        elif owner.get("no_actions_reason"):
            note = "no: declares no actions of its own"
        else:
            merged = (lookup(index, owner["names"]).get("lint") or {}).get("rule") or {}
            if not merged.get("events"):
                note = "no: legacy events only"
            elif mostly_nonconformant(merged):
                note = f"yes, names {merged.get('most_missing')}"
            else:
                note = "no: mostly conformant"
        out.append({"name": key, "declared_by": owner["product"] if owner else None,
                    "rule": rule, "legacy": legacy, "session_note": note})
    out.sort(key=lambda r: (-(r["rule"].get("events") or 0), -(r["legacy"].get("events") or 0), r["name"]))
    return out


def _share(block: dict) -> str:
    n, bad = block.get("events") or 0, block.get("nonconformant") or 0
    return f"{bad} ({round(100 * bad / n)}%)" if n else "-"


def report(roots: list[str], as_json: bool = False) -> int:
    index, problem = load_index()
    if problem:
        print(f"index {problem} at {index_path()}; build it with --force first", file=sys.stderr)
        return 2
    if not roots:
        ws = os.path.join(home(), "Workspaces", "Core")
        roots = [os.path.join(ws, "products"), os.path.join(ws, "frameworks")]
    now = time.time()
    rows = []
    for root in _declaring_products(roots):
        with open(os.path.join(root, ".intent", "INTENT.md"), "r", encoding="utf-8", errors="replace") as fh:
            text = fh.read()
        names, how = product_names(root, text)
        no_actions = declared_no_actions(text)
        hit = lookup(index, names)
        last = hit["last_event_epoch"]
        silent = last is None or now - last > WINDOW_DAYS * DAY_S
        verdict = "active" if not silent else ("no-actions" if no_actions else "silent")
        rows.append({"product": os.path.basename(root), "root": root, "names": names, "names_from": how,
                     "last_event": iso(last), "count_30d": hit["count_30d"],
                     "verdict": verdict, "no_actions_reason": no_actions})
    order = {"silent": 0, "no-actions": 1, "active": 2}
    rows.sort(key=lambda r: (order.get(r["verdict"], 3), r["product"]))
    conf = conformance_rows(index, rows)
    if as_json:
        print(json.dumps({"index_built_at": index.get("built_at"), "rows": rows,
                          "lint": index.get("lint"), "conformance": conf}, indent=2))
        return 0
    print(f"Witness index built {index.get('built_at')}; window {WINDOW_DAYS} days; "
          f"{sum(r['verdict'] == 'silent' for r in rows)} of {len(rows)} declaring products silent; "
          f"{sum(r['verdict'] == 'no-actions' for r in rows)} declare no actions of their own\n")
    print("| product | names checked | last Witness event | 30-day count | verdict |")
    print("|---|---|---|---|---|")
    for r in rows:
        names = ", ".join(r["names"]) + (" (declared)" if r["names_from"] == "declared" else "")
        verdict = r["verdict"]
        if verdict == "no-actions":
            verdict = f"no-actions ({r['no_actions_reason']})"
        print(f"| {r['product']} | {names} | {r['last_event'] or 'never'} | {r['count_30d']} | {verdict} |")
    print()
    if not isinstance(index.get("lint"), dict):
        print("Field conformance: this index predates the field lint; rebuild it with --force.")
        return 0
    print(f"Field conformance to the WS-DDR-150 minimum event, last {WINDOW_DAYS} days. Required: ts with "
          f"timezone, product, event, caller, machine, outcome, duration_ms, run_id, and redaction_level: "
          f"client-confidential on engagement events. Rule-bound events are ones a program wrote itself; "
          f"legacy events come from capture channels (screenpipe, cc-native, entire-io) or a Witness stream "
          f"adapter, are counted here, and never raise a session note.\n")
    print("| Witness name | declaring product | rule-bound events | missing a field | most often missing "
          "| legacy events | missing a field | most often missing | session note |")
    print("|---|---|---|---|---|---|---|---|---|")
    for c in conf:
        ru, le = c["rule"], c["legacy"]
        print(f"| {c['name']} | {c['declared_by'] or '-'} | {ru.get('events') or 0} | {_share(ru)} | "
              f"{ru.get('most_missing') or '-'} | {le.get('events') or 0} | {_share(le)} | "
              f"{le.get('most_missing') or '-'} | {c['session_note']} |")
    return 0


def main(argv: list[str]) -> int:
    if "--report" in argv:
        rest = [a for a in argv[argv.index("--report") + 1:] if not a.startswith("--")]
        return report(rest, as_json="--json" in argv)
    try:
        return build(force="--force" in argv, quiet="--quiet" in argv)
    except Exception as e:  # a background kick must never leave a traceback anywhere but the log
        _log(f"error {type(e).__name__}: {e}")
        if "--quiet" not in argv:
            raise
        return 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
