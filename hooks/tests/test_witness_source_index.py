#!/usr/bin/python3
"""Tests for hooks/witness_source_index.py, the out-of-band Witness index the WS-DDR-098
recorder hook reads (QMT-01M3D8KVWP66F2SH5X0TAV4E0B, 2026-09-25).

Pins: product identity (event.product, else source_system), activity time (event.ts, else
ingested_at, also for future-dated ts), the 30-day window against backfilled events,
incremental reads of appended bytes only, a rewritten file re-read without double
counting, a torn last line held until it completes, the once-a-day refusal, the lock,
a missing store, INTENT.md name parsing, and the --report table.

Temp store, temp HOME, subprocess runs of the builder: nothing real is read or written.

Run: /usr/bin/python3 hooks/tests/test_witness_source_index.py   (or under pytest)
"""
import fcntl
import json
import os
import shutil
import subprocess
import sys
import tempfile
import time

HERE = os.path.dirname(os.path.abspath(__file__))
BUILDER = os.path.join(HERE, "..", "witness_source_index.py")
sys.path.insert(0, os.path.join(HERE, ".."))
import witness_source_index as wsi  # noqa: E402

DAY = 86400
TMP = HOME = STORE = INDEX = None


def setup_module(_module=None):
    global TMP, HOME, STORE, INDEX
    TMP = tempfile.mkdtemp(prefix="witness-index-test-")
    HOME = os.path.join(TMP, "home")
    STORE = os.path.join(TMP, "store")
    os.makedirs(HOME)
    os.makedirs(STORE)
    INDEX = os.path.join(HOME, ".claude", "state", "witness-source-index.json")


def teardown_module(_module=None):
    shutil.rmtree(TMP, ignore_errors=True)


def iso(epoch):
    return time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime(epoch))


def env_line(ss, product=None, ts=None, ingested=None, **extra):
    now = time.time()
    ev = {"level": "info", "event": "x"}
    if product is not None:
        ev["product"] = product
    ev["ts"] = ts
    d = {"event_id": "EVT-%f" % time.perf_counter(), "ingested_at": ingested or iso(now),
         "source_system": ss, "event": ev}
    d.update(extra)
    return json.dumps(d) + "\n"


def build(*args, store=None):
    env = dict(os.environ, HOME=HOME, WITNESS_EVENTS_STORE=store or STORE)
    env.pop("WITNESS_SOURCE_INDEX", None)
    p = subprocess.run(["/usr/bin/python3", BUILDER, *args], capture_output=True, text=True, env=env)
    assert p.returncode == 0, (p.stdout, p.stderr)
    return p.stdout


def load():
    with open(INDEX) as fh:
        return json.load(fh)


def test_01_identity_time_and_window():
    now = time.time()
    lines = [
        env_line("witness", "witness", iso(now - 3600)),
        env_line("intent", "Gauntlet", iso(now - 100 * DAY), ingested=iso(now - 3600)),   # backfill
        env_line("intent", "cortege", iso(now - 2 * DAY)),
        env_line("signalbox-exchange", "exchange", iso(now - 5 * DAY)),
        env_line("witness-self", None, None, ingested=iso(now - 7200)),                    # no product, no ts
        env_line("loom", "loom", iso(now + 10 * DAY), ingested=iso(now - 60)),             # future ts
        env_line("loom", "loom", "not a time", ingested=iso(now - 2 * DAY)),
        "{broken json\n",
        "\n",
    ]
    with open(os.path.join(STORE, "2026-09-24.jsonl"), "w") as fh:
        fh.writelines(lines)
    out = build("--force")
    assert "index built" in out, out
    d = load()
    pr = d["products"]
    assert d["schema"] == "witness-source-index/1" and d["build"]["unparseable_lines"] == 1, d["build"]
    assert pr["gauntlet"]["count_30d"] == 0 and pr["gauntlet"]["count_total"] == 1, pr["gauntlet"]
    assert abs(pr["gauntlet"]["last_event_epoch"] - (now - 100 * DAY)) < 2, pr["gauntlet"]
    assert pr["gauntlet"]["source_systems"] == {"intent": 1}, pr["gauntlet"]
    assert pr["cortege"]["count_30d"] == 1
    assert pr["exchange"]["source_systems"] == {"signalbox-exchange": 1}
    assert "witness-self" in pr and pr["witness-self"]["count_30d"] == 1, pr
    assert pr["loom"]["count_30d"] == 2 and pr["loom"]["last_event_epoch"] < now + 5, pr["loom"]
    assert d["source_systems"]["intent"]["count_30d"] == 1 and d["source_systems"]["intent"]["count_total"] == 2
    assert "intent" not in pr, "source_system must not stand in for the product"


def test_02_once_a_day_refusal_and_force():
    before = load()["built_at_epoch"]
    out = build()
    assert "fresh" in out and load()["built_at_epoch"] == before, out
    time.sleep(0.05)
    build("--force")
    assert load()["built_at_epoch"] > before


def test_03_incremental_reads_only_appended_bytes():
    path = os.path.join(STORE, "2026-09-24.jsonl")
    extra = env_line("intent", "cortege", iso(time.time() - 60))
    with open(path, "a") as fh:
        fh.write(extra)
    build("--force")
    d = load()
    assert d["build"]["bytes_read"] == len(extra.encode()), d["build"]
    assert d["products"]["cortege"]["count_30d"] == 2, d["products"]["cortege"]


def test_04_torn_last_line_waits_for_its_newline():
    path = os.path.join(STORE, "2026-09-24.jsonl")
    line = env_line("intent", "cortege", iso(time.time() - 30))
    with open(path, "a") as fh:
        fh.write(line[:-20])
    build("--force")
    assert load()["products"]["cortege"]["count_30d"] == 2
    with open(path, "a") as fh:
        fh.write(line[-20:])
    build("--force")
    assert load()["products"]["cortege"]["count_30d"] == 3


def test_05_rewritten_file_is_reread_without_double_counting():
    path = os.path.join(STORE, "2026-09-24.jsonl")
    with open(path, "w") as fh:
        fh.write(env_line("intent", "cortege", iso(time.time() - 60)))
    build("--force")
    d = load()
    assert d["products"]["cortege"]["count_total"] == 1 and d["build"]["files_rescanned"] == 1, d
    assert "gauntlet" not in d["products"], d["products"].keys()


def test_06_lock_held_means_no_build():
    lock = open(INDEX + ".lock", "a")
    fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
    try:
        before = load()["built_at_epoch"]
        out = build("--force")
        assert "lock" in out and load()["built_at_epoch"] == before, out
    finally:
        fcntl.flock(lock, fcntl.LOCK_UN)
        lock.close()


def test_07_missing_store_builds_nothing():
    saved = INDEX + ".saved"
    os.rename(INDEX, saved)
    try:
        out = build("--force", store=os.path.join(TMP, "no-such-store"))
        assert "no Witness store" in out and not os.path.exists(INDEX), out
    finally:
        os.rename(saved, INDEX)


def test_08_declared_names_parsing():
    cases = [
        ("witness_source_system: fieldbook\n", ["fieldbook"]),
        ("witness_source_system: \"fieldbook\"  # quoted\n", ["fieldbook"]),
        ("witness_source_system: [signalbox, 'exchange']\n", ["signalbox", "exchange"]),
        ("witness_source_system:\n  - signalbox\n  - exchange\nnext: 1\n", ["signalbox", "exchange"]),
        ("witness_source_system:\n\n  - a\n---\n", ["a"]),
        ("name: x\n", []),
        ("  witness_source_system: nested-is-not-top-level\n", []),
    ]
    for text, want in cases:
        assert wsi.declared_names(text) == want, (text, wsi.declared_names(text))


def test_09_default_names():
    j = os.path.join
    assert wsi.default_name(j(TMP, "Core", "products", "cast")) == "cast"
    assert wsi.default_name(j(TMP, "Core", "frameworks", "intent-wt-2026-09-25-recorder-hook")) == "intent"
    assert wsi.default_name(j(TMP, "Core", "products", "witness", ".claude", "worktrees", "brave-x")) == "witness"
    names, how = wsi.product_names(j(TMP, "p"), "witness_source_system: [a, b]\n")
    assert (names, how) == (["a", "b"], "declared")


def test_10_parse_ts_variants():
    base = wsi.parse_ts("2026-09-25T10:00:00Z")
    assert base == wsi.parse_ts("2026-09-25T10:00:00+00:00") == wsi.parse_ts("2026-09-25T06:00:00-04:00")
    assert abs(wsi.parse_ts("2026-09-25T10:00:00.469609+00:00") - base - 0.469609) < 1e-6
    assert wsi.parse_ts("2026-09-25 10:00:00") == base
    assert wsi.parse_ts(None) is None and wsi.parse_ts("garbage") is None


def test_11_report_table():
    root = os.path.join(TMP, "products")
    for name, body in (("cortege", "lambda_settings:\n  a: 1\n"),
                       ("quiet", "autonomy_grants:\n  a: 1\n"),
                       ("undeclared", "name: x\n"),
                       ("quiet-wt-2026-09-25-x", "lambda_settings:\n  a: 1\n")):
        os.makedirs(os.path.join(root, name, ".intent"))
        with open(os.path.join(root, name, ".intent", "INTENT.md"), "w") as fh:
            fh.write(body)
    env = dict(os.environ, HOME=HOME)
    p = subprocess.run(["/usr/bin/python3", BUILDER, "--report", root, "--json"],
                       capture_output=True, text=True, env=env)
    assert p.returncode == 0, p.stderr
    rows = {r["product"]: r for r in json.loads(p.stdout)["rows"]}
    assert set(rows) == {"cortege", "quiet"}, rows.keys()
    assert rows["cortege"]["verdict"] == "active" and rows["quiet"]["verdict"] == "silent", rows


def main():
    setup_module()
    tests = [(n, f) for n, f in sorted(globals().items()) if n.startswith("test_") and callable(f)]
    failures = 0
    try:
        for name, fn in tests:
            try:
                fn()
                print(f"PASS  {name}")
            except Exception as e:  # an error is a failure too, never an aborted run
                failures += 1
                print(f"FAIL  {name}: {type(e).__name__}: {str(e)[:600]}")
    finally:
        teardown_module()
    print(f"\n{len(tests) - failures} passed, {failures} failed")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
