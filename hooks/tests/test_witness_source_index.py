#!/usr/bin/python3
"""Tests for hooks/witness_source_index.py, the out-of-band Witness index the WS-DDR-098
recorder hook reads (QMT-01M3D8KVWP66F2SH5X0TAV4E0B, 2026-09-25).

Pins: product identity (event.product, else source_system), activity time (event.ts, else
ingested_at, also for future-dated ts), the 30-day window against backfilled events,
incremental reads of appended bytes only, a rewritten file re-read without double
counting, a torn last line held until it completes, the once-a-day refusal, the lock,
a missing store, INTENT.md name parsing, and the --report table.

Added 2026-09-26 (QMT-01M3F5JWBR8XPK9YGB7HTMCBNP, WS-DDR-150), cases 14 to 23: the field
lint of one event (plain and OTLP shapes, the timezone rule, the engagement redaction rule,
legacy versus rule-bound), agreement with what emit.py builds, per-product lint in the
index over the 30-day window, incremental lint, the one full re-read of a state written
before the lint, the conformance table in --report, the job.run event every build emits
through emit.py, and that an emit failure never breaks a build. They use their own store
and HOME; the emit cases point WITNESS_EMIT at the real emit.py and WITNESS_INBOX at a
temp dir, so nothing reaches the real Witness inbox.

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
    for k in ("WITNESS_EMIT", "WITNESS_INBOX", "WITNESS_CALLER", "WITNESS_RUN_ID", "WITNESS_ROOT"):
        env.pop(k, None)
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



def test_12_declared_no_actions_parsing():
    f = wsi.declared_no_actions
    assert f("witness_actions: none (content repo, markdown only)\n") == "content repo, markdown only"
    assert f("---\nx: 1\nwitness_actions: None (methodology repo; no scripts)  # why\n---\n") == \
        "methodology repo; no scripts"
    assert f('witness_actions: "none (quoted reason)"\n') == "quoted reason"
    assert f("witness_actions: none\n") is None          # a reason is required
    assert f("witness_actions: none ()\n") is None       # an empty reason is no reason
    assert f("witness_actions: none (   )\n") is None
    assert f("witness_actions: some (it acts)\n") is None
    assert f("  witness_actions: none (indented is not column 0)\n") is None
    assert f("name: x\n") is None and f("") is None and f(None) is None


def test_13_report_no_actions_verdict():
    root = os.path.join(TMP, "products-na")
    for name, body in (("content", "lambda_settings:\n  a: 1\nwitness_actions: none (content repo, markdown only)\n"),
                       ("bare", "lambda_settings:\n  a: 1\nwitness_actions: none\n"),
                       ("cortege", "lambda_settings:\n  a: 1\nwitness_actions: none (declared but it emits)\n")):
        os.makedirs(os.path.join(root, name, ".intent"))
        with open(os.path.join(root, name, ".intent", "INTENT.md"), "w") as fh:
            fh.write(body)
    env = dict(os.environ, HOME=HOME)
    p = subprocess.run(["/usr/bin/python3", BUILDER, "--report", root, "--json"],
                       capture_output=True, text=True, env=env)
    assert p.returncode == 0, p.stderr
    rows = {r["product"]: r for r in json.loads(p.stdout)["rows"]}
    assert rows["content"]["verdict"] == "no-actions", rows["content"]
    assert rows["content"]["no_actions_reason"] == "content repo, markdown only", rows["content"]
    assert rows["bare"]["verdict"] == "silent" and rows["bare"]["no_actions_reason"] is None, rows["bare"]
    assert rows["cortege"]["verdict"] == "active", rows["cortege"]  # events win over the declaration
    p = subprocess.run(["/usr/bin/python3", BUILDER, "--report", root],
                       capture_output=True, text=True, env=env)
    assert p.returncode == 0, p.stderr
    assert "1 of 3 declaring products silent; 1 declare no actions of their own" in p.stdout, p.stdout
    assert "| no-actions (content repo, markdown only) |" in p.stdout, p.stdout


# ---- added 2026-09-26: field lint and the builder's own events (WS-DDR-150) ----
# These cases use their own store and HOME (L*), so the cases above are untouched.

LTMP = {}
_EMIT_ENV = ("WITNESS_EMIT", "WITNESS_INBOX", "WITNESS_CALLER", "WITNESS_RUN_ID", "WITNESS_ROOT")


def _lsetup():
    if not LTMP:
        base = os.path.join(TMP, "lint")
        LTMP.update(base=base, home=os.path.join(base, "home"), store=os.path.join(base, "store"),
                    root=os.path.join(base, "products"))
        LTMP["index"] = os.path.join(LTMP["home"], ".claude", "state", "witness-source-index.json")
        os.makedirs(LTMP["home"])
        os.makedirs(LTMP["store"])
    return LTMP


def real_emit_py():
    """The Witness emit.py beside this repo (Core/products/witness/src), else under $HOME."""
    for cand in (os.path.join(HERE, "..", "..", "..", "..", "products", "witness", "src", "emit.py"),
                 os.path.join(os.path.expanduser("~"), "Workspaces", "Core", "products", "witness", "src", "emit.py")):
        if os.path.isfile(cand):
            return os.path.normpath(cand)
    raise AssertionError("Witness emit.py not found; the emit cases need Core/products/witness/src/emit.py")


def lrun(*args, env_extra=None):
    L = _lsetup()
    env = dict(os.environ, HOME=L["home"], WITNESS_EVENTS_STORE=L["store"])
    env.pop("WITNESS_SOURCE_INDEX", None)
    for k in _EMIT_ENV:
        env.pop(k, None)
    env.update(env_extra or {})
    return subprocess.run(["/usr/bin/python3", BUILDER, *args], capture_output=True, text=True, env=env)


def lload():
    with open(_lsetup()["index"]) as fh:
        return json.load(fh)


def good(product, ts=None, **attrs):
    a = {"caller": "manual:test", "machine": "m", "outcome": "ok", "duration_ms": 1.5, "run_id": "r1"}
    a.update(attrs)
    return {"ts": ts or iso(time.time() - 60), "level": "info", "product": product,
            "event": product + ".act", "attributes": a}


def bare(product, **attrs):
    return {"ts": iso(time.time() - 120), "level": "error", "product": product,
            "event": "audit.invariant.fired", "attributes": dict({"invariant": "I-X"}, **attrs)}


def otlp(product="fieldbook", span_attrs=None, res_attrs=None, status="STATUS_CODE_OK",
         trace="9c0902c0c3f38b53c1b902fa2775fb68", start="1789333529990539000", end="1789333530018056000"):
    kv = lambda d: [{"key": k, "value": {"stringValue": v}} for k, v in d.items()]
    span = {"traceId": trace, "spanId": "50dda4eb646a4144", "name": product + ".ledger.create",
            "startTimeUnixNano": start, "attributes": kv(dict({"product": product}, **(span_attrs or {}))),
            "status": {"code": status}}
    if end is not None:
        span["endTimeUnixNano"] = end
    return {"resource": {"attributes": kv(dict({"service.name": product}, **(res_attrs or {})))},
            "scopeSpans": [{"scope": {"name": product}, "spans": [span]}]}


def eline(ss, event, ingested=None):
    return json.dumps({"event_id": "EVT-%f" % time.perf_counter(), "ingested_at": ingested or iso(time.time()),
                       "source_system": ss, "event": event}) + "\n"


def test_14_lint_event_plain_fields():
    assert wsi.lint_event(good("witness")) == ("rule", []), wsi.lint_event(good("witness"))
    assert wsi.lint_event(good("x", duration_ms=0))[1] == [], "zero is a duration"
    assert wsi.lint_event(bare("quartermaster"), "quartermaster") == (
        "rule", ["caller", "machine", "outcome", "duration_ms", "run_id"])
    for ts in ("2026-09-25 10:00:00", "2026-09-25T10:00:00", None, "garbage"):
        ev = good("x")
        ev["ts"] = ts
        assert wsi.lint_event(ev)[1] == ["ts"], ts
    for ts in ("2026-09-25T10:00:00Z", "2026-09-25T06:00:00-04:00", "2026-09-25T06:00:00.12+0530"):
        assert wsi.lint_event(good("x", ts=ts))[1] == [], ts
    ev = good("x")
    ev["product"], ev["event"] = "", None
    assert wsi.lint_event(ev)[1] == ["product", "event"]
    eng = "Work/Consulting/Engagements/Acme/notes.md"
    assert wsi.lint_event(good("x", target=eng))[1] == ["redaction_level"]
    assert wsi.lint_event(good("x", target="/h/Workspaces/" + eng, redaction_level="brien-private"))[1] == ["redaction_level"]
    assert wsi.lint_event(good("x", target=eng, redaction_level="client-confidential"))[1] == []
    assert wsi.lint_event(good("x", target="Core/products/witness/src/emit.py"))[1] == []
    assert wsi.lint_event(None) == ("rule", ["ts", "product", "event", "caller", "machine", "outcome",
                                             "duration_ms", "run_id"])


def test_15_emit_py_output_lints_conformant():
    """The shared emit call and this lint agree: what emit.py builds passes, given duration_ms."""
    import importlib.util
    spec = importlib.util.spec_from_file_location("witness_emit_under_test", real_emit_py())
    emit = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(emit)
    ev = emit.build_event("intent", "job.run", caller="manual:test", duration_ms=5)
    assert wsi.lint_event(ev, "intent") == ("rule", []), (ev, wsi.lint_event(ev, "intent"))
    ev = emit.build_event("intent", "job.run")  # emit.py leaves duration_ms to the caller
    assert wsi.lint_event(ev, "intent") == ("rule", ["duration_ms"]), ev


def test_16_lint_event_classes():
    for ss in ("screenpipe", "cc-native", "entire-io", "ScreenPipe"):
        assert wsi.lint_event(good("x"), ss)[0] == "legacy", ss
    for adapter in ("intent-events-jsonl", "loom-records", "signalbox-events", "exchange-events"):
        assert wsi.lint_event(good("x", adapter=adapter), "intent")[0] == "legacy", adapter
    assert wsi.lint_event(bare("quartermaster"), "quartermaster")[0] == "rule"
    assert wsi.lint_event(good("witness"), "witness")[0] == "rule"
    assert wsi.lint_event(otlp(), "fieldbook")[0] == "rule"
    assert wsi.lint_event(otlp(), "entire-io")[0] == "legacy"


def test_17_lint_event_otlp():
    assert wsi.lint_event(otlp(), "fieldbook") == ("rule", ["caller", "machine"])
    ok = otlp(span_attrs={"caller": "launchd:x"}, res_attrs={"host.name": "marcus-aurelius"})
    assert wsi.lint_event(ok)[1] == []
    assert wsi.lint_event(otlp(span_attrs={"caller": "c", "machine": "m"}, status="STATUS_CODE_UNSET"))[1] == ["outcome"]
    assert wsi.lint_event(otlp(span_attrs={"caller": "c", "machine": "m"}, trace="0" * 32))[1] == ["run_id"]
    assert wsi.lint_event(otlp(span_attrs={"caller": "c", "machine": "m"}, end=None))[1] == ["duration_ms"]
    assert wsi.lint_event(otlp(span_attrs={"caller": "c", "machine": "m"}, start="0"))[1] == ["ts", "duration_ms"]
    wrapped = {"resourceSpans": [otlp(span_attrs={"caller": "c", "machine": "m"})]}
    assert wsi.lint_event(wrapped)[1] == [], wsi.lint_event(wrapped)
    assert wsi.most_missing({"machine": 3, "caller": 3}) == "caller"
    assert wsi.most_missing({"run_id": 5, "caller": 3}) == "run_id"
    assert wsi.most_missing({}) is None


def test_18_build_stores_lint_per_product_in_window():
    L = _lsetup()
    now = time.time()
    eng = "Work/Consulting/Engagements/Acme/notes.md"
    lines = (
        [eline("quartermaster", bare("qm")) for _ in range(3)] + [eline("quartermaster", good("qm"))]
        + [eline("emitprod", good("emitprod")) for _ in range(2)]
        + [eline("screenpipe", dict(good("screenpipe"), attributes={"redaction_level": "client-confidential"}))
           for _ in range(2)]
        + [eline("intent", good("adapterprod", adapter="intent-events-jsonl", caller=None)) for _ in range(2)]
        + [eline("intent", good("oldprod", ts=iso(now - 45 * DAY)), ingested=iso(now - 45 * DAY))]
        + [eline("fieldbook", otlp())]
        + [eline("engprod", good("engprod", target=eng)),
           eline("engprod", good("engprod", target=eng, redaction_level="client-confidential"))]
    )
    with open(os.path.join(L["store"], "2026-09-26.jsonl"), "w") as fh:
        fh.writelines(lines)
    p = lrun("--force")
    assert p.returncode == 0 and "index built" in p.stdout, (p.stdout, p.stderr)
    d = lload()
    assert d["lint"]["version"] == wsi.LINT_VERSION and d["lint"]["rule"] == "WS-DDR-150", d["lint"]
    pr = d["products"]
    qm = pr["qm"]["lint_30d"]
    assert qm["rule"] == {"events": 4, "nonconformant": 3, "most_missing": "caller",
                          "missing": {"caller": 3, "machine": 3, "outcome": 3, "duration_ms": 3, "run_id": 3}}, qm
    assert qm["legacy"]["events"] == 0
    assert pr["emitprod"]["lint_30d"]["rule"]["nonconformant"] == 0
    assert pr["screenpipe"]["lint_30d"]["legacy"]["events"] == 2 and pr["screenpipe"]["lint_30d"]["rule"]["events"] == 0
    assert pr["screenpipe"]["lint_30d"]["legacy"]["most_missing"] == "caller"
    ad = pr["adapterprod"]["lint_30d"]
    assert ad["legacy"] == {"events": 2, "nonconformant": 2, "most_missing": "caller", "missing": {"caller": 2}}, ad
    assert pr["oldprod"]["lint_30d"]["rule"]["events"] == 0 and pr["oldprod"]["count_total"] == 1
    assert pr["fieldbook"]["lint_30d"]["rule"]["missing"] == {"caller": 1, "machine": 1}
    en = pr["engprod"]["lint_30d"]["rule"]
    assert (en["events"], en["nonconformant"], en["most_missing"]) == (2, 1, "redaction_level"), en
    assert "lint_30d" not in d["source_systems"]["quartermaster"]


def test_19_lint_is_incremental():
    L = _lsetup()
    extra = eline("quartermaster", good("qm"))
    with open(os.path.join(L["store"], "2026-09-26.jsonl"), "a") as fh:
        fh.write(extra)
    p = lrun("--force")
    assert p.returncode == 0, p.stderr
    d = lload()
    assert d["build"]["bytes_read"] == len(extra.encode()), d["build"]
    assert d["products"]["qm"]["lint_30d"]["rule"]["events"] == 5
    assert d["products"]["qm"]["lint_30d"]["rule"]["nonconformant"] == 3


def test_20_state_from_before_the_lint_is_reread_once():
    L = _lsetup()
    state_path = L["index"] + ".state"
    with open(state_path) as fh:
        state = json.load(fh)
    state.pop("lint_version")
    for rec in state["files"].values():
        for row in rec["products"].values():
            row.pop("lint", None)
    with open(state_path, "w") as fh:
        json.dump(state, fh)
    size = sum(os.path.getsize(os.path.join(L["store"], n)) for n in os.listdir(L["store"]))
    assert lrun("--force").returncode == 0
    d = lload()
    assert d["build"]["bytes_read"] == size, (d["build"], size)
    assert d["products"]["qm"]["lint_30d"]["rule"]["events"] == 5, "re-read once, not doubled"
    assert lrun("--force").returncode == 0
    d = lload()
    assert d["build"]["bytes_read"] == 0 and d["products"]["qm"]["lint_30d"]["rule"]["events"] == 5, d["build"]


def test_21_report_prints_the_conformance_table():
    L = _lsetup()
    for name in ("qm", "emitprod", "adapterprod"):
        os.makedirs(os.path.join(L["root"], name, ".intent"), exist_ok=True)
        with open(os.path.join(L["root"], name, ".intent", "INTENT.md"), "w") as fh:
            fh.write("lambda_settings:\n  a: 1\n")
    p = lrun("--report", L["root"], "--json")
    assert p.returncode == 0, p.stderr
    data = json.loads(p.stdout)
    conf = {c["name"]: c for c in data["conformance"]}
    assert conf["qm"]["session_note"] == "yes, names caller" and conf["qm"]["declared_by"] == "qm", conf["qm"]
    assert conf["emitprod"]["session_note"] == "no: mostly conformant", conf["emitprod"]
    assert conf["adapterprod"]["session_note"] == "no: legacy events only", conf["adapterprod"]
    assert conf["screenpipe"]["session_note"].startswith("no: not a product"), conf["screenpipe"]
    assert "oldprod" not in conf, "no events in the window, no conformance row"
    assert data["lint"]["required"][:3] == ["ts", "product", "event"]
    p = lrun("--report", L["root"])
    assert p.returncode == 0 and "Field conformance" in p.stdout, p.stdout
    assert "| qm | qm | 5 | 3 (60%) | caller | 0 | - | - | yes, names caller |" in p.stdout, p.stdout


def test_22_build_reports_its_run_through_emit_py():
    L = _lsetup()
    inbox = os.path.join(L["base"], "inbox")
    env = {"WITNESS_EMIT": real_emit_py(), "WITNESS_INBOX": inbox,
           "WITNESS_CALLER": "hook:signal-recorder-silent-check"}
    p = lrun("--force", env_extra=env)
    assert p.returncode == 0 and p.stderr == "", p.stderr
    env.pop("WITNESS_CALLER")
    env["USER"] = "tester"
    p = lrun(env_extra=env)  # fresh index: a skipped run, still reported
    assert p.returncode == 0 and "fresh" in p.stdout, p.stdout
    p = lrun("--report", L["root"], env_extra=env)  # a read: reports nothing
    assert p.returncode == 0
    events = []
    for name in sorted(os.listdir(inbox)):
        with open(os.path.join(inbox, name)) as fh:
            events.extend(json.loads(x) for x in fh if x.strip())
    assert len(events) == 2, events
    built, fresh = events
    for ev in events:
        assert ev["product"] == "intent" and ev["event"] == "job.run", ev
        assert ev["attributes"]["job"] == "witness-source-index", ev
        assert wsi.lint_event(ev, "intent") == ("rule", []), wsi.lint_event(ev, "intent")
    a = built["attributes"]
    assert (a["outcome"], a["reason"], a["caller"]) == ("ok", "built", "hook:signal-recorder-silent-check"), a
    assert a["rule_events_30d"] > 0 and a["mostly_nonconformant"] >= 1 and a["events_read"] == 0, a
    b = fresh["attributes"]
    assert (b["outcome"], b["reason"], b["caller"]) == ("skipped", "fresh", "manual:tester"), b


def test_23_emit_failure_never_breaks_the_build():
    L = _lsetup()
    broken = os.path.join(L["base"], "broken_emit.py")
    with open(broken, "w") as fh:
        fh.write("raise RuntimeError('emit module broken on purpose')\n")
    not_a_dir = os.path.join(L["base"], "inbox-is-a-file")
    with open(not_a_dir, "w") as fh:
        fh.write("x\n")
    for env in ({"WITNESS_EMIT": broken}, {"WITNESS_EMIT": real_emit_py(), "WITNESS_INBOX": not_a_dir}):
        before = lload()["built_at_epoch"]
        p = lrun("--force", env_extra=env)
        assert p.returncode == 0 and "index built" in p.stdout, (p.stdout, p.stderr)
        assert "witness-emit: not recorded" in p.stderr, p.stderr
        assert lload()["built_at_epoch"] > before
    p = lrun("--force", env_extra={"WITNESS_EMIT": os.path.join(L["base"], "no-such-emit.py")})
    assert p.returncode == 0 and p.stderr == "", p.stderr


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
