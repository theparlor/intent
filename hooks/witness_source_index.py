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
  /usr/bin/python3 witness_source_index.py --report [ROOT ...]
      # table of every product under ROOT (default: Core/products and Core/frameworks
      # in $HOME/Workspaces) that declares lambda_settings or autonomy_grants, with the
      # names checked, last Witness event, 30-day count and verdict. Reads the index only.

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

The hook imports the small pure functions below (names, lookup, timestamps); keep this
module's top-level imports light, because every Write and Edit pays for them.
"""
from __future__ import annotations

import json
import os
import re
import sys
import time

SCHEMA = "witness-source-index/1"
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

def parse_ts(value) -> float | None:
    """ISO 8601 text to epoch seconds (UTC when no offset). None when unparseable."""
    if not isinstance(value, str):
        return None
    m = _TS_RE.match(value.strip())
    if not m:
        return None
    import calendar
    y, mo, d, h, mi, s = (int(x) for x in m.groups()[:6])
    try:
        epoch = calendar.timegm((y, mo, d, h, mi, s, 0, 0, 0))
    except (ValueError, OverflowError):
        return None
    if m.group(7):
        epoch += float(m.group(7))
    tz = m.group(8)
    if tz and tz not in ("Z", "z"):
        t = tz[1:].replace(":", "")
        off = int(t[:2]) * 3600 + int(t[2:4]) * 60
        epoch -= off if tz[0] == "+" else -off
    return float(epoch)


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
    """Merge the index rows for names: last event epoch, 30-day count, names that matched."""
    products = index.get("products") or {}
    last, count, matched = None, 0, []
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
    return {"last_event_epoch": last, "count_30d": count, "matched": matched}


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


def _bump(table: dict, key: str, epoch: float | None, day: str | None, via: str | None) -> None:
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
            act = parse_ts(ev.get("ts"))
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
                _bump(products, prod, act, day, ss)
            if ss is not None:
                _bump(systems, ss, act, day, None)
    return offset, events, bad


def _prune_days(rec: dict, oldest_day: str) -> None:
    for table in (rec.get("products", {}), rec.get("systems", {})):
        for row in table.values():
            row["days"] = {d: n for d, n in row.get("days", {}).items() if d >= oldest_day}


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

    def shape(table: dict, with_via: bool) -> dict:
        shaped = {}
        for key, a in sorted(table.items()):
            row = {"last_event": iso(a["last"]), "last_event_epoch": a["last"],
                   "count_30d": a["count_30d"], "count_total": a["total"]}
            if with_via:
                row["source_systems"] = dict(sorted(a["via"].items()))
            shaped[key] = row
        return shaped

    return shape(out["products"], True), shape(out["systems"], False)


def build(force: bool = False, quiet: bool = False) -> int:
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
        return 0
    try:
        if not force:
            current, problem = load_index(idx_path)
            if problem is None and time.time() - current["built_at_epoch"] < REFRESH_EVERY_S:
                say(f"index is fresh (built {current.get('built_at')}); use --force to rebuild")
                return 0
        if not os.path.isdir(store):
            say(f"no Witness store at {store}; index not built")
            _log(f"skip store-absent store={store}")
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
            "products": products,
            "source_systems": systems,
        }
        _atomic_write_json(state_path, {"schema": SCHEMA, "store": store, "files": files})
        _atomic_write_json(idx_path, index)
        _log(f"built products={len(products)} files={len(present)} bytes_read={read_bytes} "
             f"events_read={events} bad={bad} seconds={round(built - t0, 2)}")
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
    if as_json:
        print(json.dumps({"index_built_at": index.get("built_at"), "rows": rows}, indent=2))
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
