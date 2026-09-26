#!/usr/bin/python3
"""Test harness for signal-recorder-silent-check.sh (WS-DDR-098 companion hook).

Two regressions under test.

1. 2026-05-26 to 2026-09-25: the path lookup read as
   (file_path or path or command.split()[1]) if command else None, so every Edit and Write
   resolved to None. 30,953 telemetry rows, all no-context/skip; the hook never evaluated a
   product. The seven original cases pin the detection matrix.
2. Until 2026-09-25 (QMT-01M3D8KVWP66F2SH5X0TAV4E0B) the hook measured signal-file recency,
   not Witness events, and warned on stderr, which Claude Code sends to the debug log only.
   The added cases pin the Witness-index measure, declared names, the once-per-session
   additionalContext note, index failure modes, the detached refresh and latency.

Expectation change from the seven-case version: "warned" used to mean WS-DDR-098 on stderr;
it now means the recorder-check note inside hookSpecificOutput.additionalContext on stdout
(since 2026-09-26 the note cites WS-DDR-150, which amended WS-DDR-098). The
detection values keep their names; "recorder-active" and "silent-recorder" now come from the
Witness index instead of SIG-*.md mtimes (the SIG fixtures are kept, and one added case
proves a fresh SIG file no longer counts).

3. 2026-09-26 (QMT-01M3F5JWBR8XPK9YGB7HTMCBNP, WS-DDR-150): the index carries field lint per
   product. Cases 23 to 31 pin the once-per-session field note for an active product whose
   rule-bound events mostly miss a minimum field, the quiet paths (mostly conformant, legacy
   only, no lint in the index), merging across declared names, the silent note's emit.py
   pointer, the hook.fire event every fire emits through emit.py, that an emit failure never
   changes the check, and a remedy that fits what is missing. Case 20 now times 21 runs with
   the emit on. Case 19's fixture event carries attributes.adapter, as every real event on
   the intent channel does (the intent-events adapter stamps it); without it the event read
   as a nonconformant rule-bound one and drew the new note.

Everything runs under a temp dir with a fake HOME, so the real telemetry, audit log, dedupe
state and index are never touched. The emit cases point WITNESS_EMIT at the real emit.py and
WITNESS_INBOX at a temp dir, so nothing reaches the real Witness inbox.

Run: /usr/bin/python3 hooks/tests/test_signal_recorder_silent_check.py   (or under pytest)
"""
import json
import os
import shutil
import statistics
import subprocess
import sys
import tempfile
import time

HERE = os.path.dirname(os.path.abspath(__file__))
HOOK = os.path.join(HERE, "..", "signal-recorder-silent-check.sh")
sys.path.insert(0, os.path.join(HERE, ".."))
import witness_source_index as wsi  # noqa: E402

DAY = 86400
LATENCY_BUDGET_MS = 100
LATENCY_RUNS = 21
_EMIT_ENV = ("WITNESS_EMIT", "WITNESS_INBOX", "WITNESS_CALLER", "WITNESS_RUN_ID", "WITNESS_ROOT")


def real_emit_py():
    """The Witness emit.py beside this repo (Core/products/witness/src), else under $HOME."""
    for cand in (os.path.join(HERE, "..", "..", "..", "..", "products", "witness", "src", "emit.py"),
                 os.path.join(os.path.expanduser("~"), "Workspaces", "Core", "products", "witness", "src", "emit.py")):
        if os.path.isfile(cand):
            return os.path.normpath(cand)
    raise AssertionError("Witness emit.py not found; the emit cases need Core/products/witness/src/emit.py")

TMP = FAKE_HOME = TELEMETRY = INDEX = STORE = None
P = {}


def setup_module(_module=None):
    global TMP, FAKE_HOME, TELEMETRY, INDEX, STORE
    TMP = tempfile.mkdtemp(prefix="recorder-silent-test-")
    FAKE_HOME = os.path.join(TMP, "home")
    os.makedirs(FAKE_HOME)
    TELEMETRY = os.path.join(FAKE_HOME, ".claude", "logs", "signal-recorder-silent.jsonl")
    INDEX = os.path.join(FAKE_HOME, ".claude", "state", "witness-source-index.json")
    STORE = os.path.join(TMP, "store")
    os.makedirs(STORE)
    P["silent"] = make_product("silent", declares=True, sig_age_days=60)
    P["active"] = make_product("active", declares=True, sig_age_days=2)
    P["plain"] = make_product("plain", declares=False, sig_age_days=None)
    eng_parent = os.path.join(TMP, "Work", "Consulting", "Engagements")
    os.makedirs(eng_parent)
    P["eng"] = make_product("Client", declares=True, sig_age_days=60, parent=eng_parent)
    P["sigonly"] = make_product("sigonly", declares=True, sig_age_days=1)
    P["never"] = make_product("never", declares=True, sig_age_days=None)
    P["scalar"] = make_product("renamed-dir", declares=True, sig_age_days=None,
                               extra="witness_source_system: fieldbook-x  # reports under another name\n")
    P["flow"] = make_product("flowlist", declares=True, sig_age_days=None,
                             extra="witness_source_system: [alpha-src, 'Beta-Src']\n")
    P["block"] = make_product("blocklist", declares=True, sig_age_days=None,
                              extra="witness_source_system:\n  - gamma-src\n  - \"delta-src\"\nother: 1\n")
    P["wt"] = make_product("wtprod-wt-2026-09-25-some-task", declares=True, sig_age_days=None)
    P["dedupe"] = make_product("dedupe", declares=True, sig_age_days=None)
    P["noact"] = make_product("noact", declares=True, sig_age_days=None,
                              extra="witness_actions: none (content repo, markdown only)\n")
    P["barenone"] = make_product("barenone", declares=True, sig_age_days=None,
                                 extra="witness_actions: none\n")
    P["fieldy"] = make_product("fieldy", declares=True, sig_age_days=None)
    P["tidy"] = make_product("tidy", declares=True, sig_age_days=None)
    P["oldie"] = make_product("oldie", declares=True, sig_age_days=None)
    P["split"] = make_product("splitprod", declares=True, sig_age_days=None,
                              extra="witness_source_system: [split-a, split-b]\n")
    P["slowy"] = make_product("slowy", declares=True, sig_age_days=None)
    P["engy"] = make_product("engy", declares=True, sig_age_days=None)
    P["mixy"] = make_product("mixy", declares=True, sig_age_days=None)
    write_index()


def teardown_module(_module=None):
    shutil.rmtree(TMP, ignore_errors=True)


def make_product(name, declares, sig_age_days, parent=None, extra=""):
    root = os.path.join(parent or TMP, name)
    os.makedirs(os.path.join(root, ".intent", "signals"))
    os.makedirs(os.path.join(root, "src"))
    body = "---\nname: %s\n" % name + ("lambda_settings:\n  default: L2\n" if declares else "title: plain\n") + extra + "---\n"
    with open(os.path.join(root, ".intent", "INTENT.md"), "w") as fh:
        fh.write(body)
    target = os.path.join(root, "src", "thing.py")
    with open(target, "w") as fh:
        fh.write("x = 1\n")
    if sig_age_days is not None:
        sig = os.path.join(root, ".intent", "signals", "SIG-TEST.md")
        with open(sig, "w") as fh:
            fh.write("---\nid: SIG-TEST\n---\n")
        past = time.time() - sig_age_days * DAY
        os.utime(sig, (past, past))
    return root, target


def write_index(built_ago_s=0, raw=None):
    os.makedirs(os.path.dirname(INDEX), exist_ok=True)
    if raw is not None:
        with open(INDEX, "w") as fh:
            fh.write(raw)
        return
    now = time.time()

    def row(days_ago, count, lint=None):
        e = now - days_ago * DAY
        r = {"last_event_epoch": e, "last_event": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime(e)),
             "count_30d": count, "count_total": count + 5, "source_systems": {"x": count + 5}}
        if lint is not None:
            r["lint_30d"] = {k: wsi.lint_block(*lint.get(k, (0, 0, {}))) for k in ("rule", "legacy")}
        return r

    data = {
        "schema": "witness-source-index/1",
        "built_at_epoch": now - built_ago_s,
        "built_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime(now - built_ago_s)),
        "window_days": 30,
        "products": {
            "silent": row(60, 0),
            "active": row(2, 17),
            "client": row(90, 0),
            "fieldbook-x": row(3, 4),
            "beta-src": row(5, 2),
            "alpha-src": row(45, 0),
            "gamma-src": row(40, 0),
            "wtprod": row(1, 9),
            "fieldy": row(1, 10, {"rule": (10, 9, {"caller": 9, "machine": 9, "run_id": 2})}),
            "tidy": row(1, 10, {"rule": (10, 3, {"machine": 3})}),
            "oldie": row(1, 500, {"legacy": (500, 500, {"ts": 500, "caller": 500})}),
            "split-a": row(2, 4, {"rule": (4, 4, {"run_id": 4})}),
            "split-b": row(1, 6, {"rule": (6, 0, {})}),
            "slowy": row(1, 10, {"rule": (10, 8, {"duration_ms": 8})}),
            "engy": row(1, 10, {"rule": (10, 6, {"redaction_level": 6})}),
            "mixy": row(1, 10, {"rule": (10, 10, {"duration_ms": 10, "caller": 9, "run_id": 9})}),
        },
        "source_systems": {},
    }
    with open(INDEX, "w") as fh:
        json.dump(data, fh)


def run(tool_input, tool="Write", session="s-default", env_extra=None, bypass=False):
    env = dict(os.environ, HOME=FAKE_HOME, WITNESS_INDEX_NO_REFRESH="1", WITNESS_EVENTS_STORE=STORE)
    env.pop("SIGNAL_RECORDER_SILENT_BYPASSED", None)
    env.pop("WITNESS_SOURCE_INDEX", None)
    env.pop("CLAUDE_SESSION_ID", None)
    for k in _EMIT_ENV:
        env.pop(k, None)
    if bypass:
        env["SIGNAL_RECORDER_SILENT_BYPASSED"] = "1"
    env.update(env_extra or {})
    payload = {"tool_name": tool, "tool_input": tool_input}
    if session:
        payload["session_id"] = session
    before = _rows()
    t0 = time.perf_counter()
    p = subprocess.run([HOOK], input=json.dumps(payload), capture_output=True, text=True, env=env)
    ms = (time.perf_counter() - t0) * 1000
    rows = _rows()[len(before):]
    last = json.loads(rows[-1]) if rows else {}
    ctx = ""
    if p.stdout.strip():
        ctx = json.loads(p.stdout)["hookSpecificOutput"]["additionalContext"]
    return {"rc": p.returncode, "stdout": p.stdout, "stderr": p.stderr, "row": last,
            "rows": len(rows), "ctx": ctx, "warned": "[Witness recorder check," in ctx,
            "field_note": "[Witness field check, WS-DDR-150]" in ctx, "ms": ms}


def emit_env(inbox):
    return {"WITNESS_EMIT": real_emit_py(), "WITNESS_INBOX": inbox}


def inbox_events(inbox):
    out = []
    if os.path.isdir(inbox):
        for name in sorted(os.listdir(inbox)):
            with open(os.path.join(inbox, name)) as fh:
                out.extend(json.loads(line) for line in fh if line.strip())
    return out


def _rows():
    if not os.path.exists(TELEMETRY):
        return []
    with open(TELEMETRY) as fh:
        return fh.read().splitlines()


def _check(r, detection, warned):
    assert r["rc"] == 0, r
    assert r["row"].get("detection") == detection, (detection, r["row"], r["stderr"])
    assert r["warned"] == warned, (warned, r["stdout"], r["stderr"])
    assert r["stderr"] == "", r["stderr"]


# ---- the seven original cases (same meaning; warned now means additionalContext) ----

def test_01_write_into_silent_product():
    _check(run({"file_path": P["silent"][1], "content": "y"}, "Write", "s01"), "silent-recorder", True)


def test_02_edit_into_silent_product():
    _check(run({"file_path": P["silent"][1], "old_string": "x", "new_string": "y"}, "Edit", "s02"),
           "silent-recorder", True)


def test_03_bash_naming_path_in_silent_product():
    _check(run({"command": f"python3 -m pytest {P['silent'][1]} -q"}, "Bash", "s03"), "silent-recorder", True)


def test_04_write_into_active_product():
    r = run({"file_path": P["active"][1], "content": "y"}, "Write", "s04")
    _check(r, "recorder-active", False)
    assert r["row"]["count_30d"] == 17 and r["row"]["last_event_days"] == 2, r["row"]


def test_05_no_autonomy_declaration():
    _check(run({"file_path": P["plain"][1], "content": "y"}, "Write", "s05"), "no-lambda-declaration", False)


def test_06_engagement_path_exempt():
    _check(run({"file_path": P["eng"][1], "content": "y"}, "Write", "s06"), "engagement-exempt", False)


def test_07_bash_with_no_path():
    _check(run({"command": "ls"}, "Bash", "s07"), "no-context", False)


# ---- added 2026-09-25 ----

def test_08_fresh_signal_file_no_longer_counts():
    r = run({"file_path": P["sigonly"][1], "content": "y"}, "Write", "s08")
    _check(r, "silent-recorder", True)
    assert "Last event: never" in r["ctx"], r["ctx"]


def test_09_index_present_and_silent_never_seen():
    r = run({"file_path": P["never"][1], "content": "y"}, "Write", "s09")
    _check(r, "silent-recorder", True)
    assert r["row"]["last_event_days"] is None and r["row"]["names"] == ["never"], r["row"]
    out = json.loads(r["stdout"])
    assert out["hookSpecificOutput"]["hookEventName"] == "PreToolUse"
    assert "permissionDecision" not in out["hookSpecificOutput"], out
    assert "never" in out.get("systemMessage", ""), out


def test_10_index_present_and_active_old_event_is_silent():
    # "silent" has an event 60 days old: present in the index, still silent.
    r = run({"file_path": P["silent"][1], "content": "y"}, "Write", "s10")
    _check(r, "silent-recorder", True)
    assert r["row"]["last_event_days"] == 60, r["row"]


def test_11_declared_scalar_name():
    r = run({"file_path": P["scalar"][1], "content": "y"}, "Write", "s11")
    _check(r, "recorder-active", False)
    assert r["row"]["names"] == ["fieldbook-x"] and r["row"]["names_from"] == "declared", r["row"]


def test_12_declared_flow_list_any_active_name_counts_ignoring_case():
    r = run({"file_path": P["flow"][1], "content": "y"}, "Write", "s12")
    _check(r, "recorder-active", False)
    assert r["row"]["names"] == ["alpha-src", "Beta-Src"], r["row"]
    assert r["row"]["last_event_days"] == 5 and r["row"]["count_30d"] == 2, r["row"]


def test_13_declared_block_list_all_quiet_is_silent():
    r = run({"file_path": P["block"][1], "content": "y"}, "Write", "s13")
    _check(r, "silent-recorder", True)
    assert r["row"]["names"] == ["gamma-src", "delta-src"], r["row"]
    assert "gamma-src, delta-src" in r["ctx"], r["ctx"]


def test_14_worktree_suffix_reads_as_repo_name():
    r = run({"file_path": P["wt"][1], "content": "y"}, "Write", "s14")
    _check(r, "recorder-active", False)
    assert r["row"]["names"] == ["wtprod"], r["row"]


def test_15_once_per_session_per_product():
    first = run({"file_path": P["dedupe"][1], "content": "y"}, "Write", "s15")
    second = run({"file_path": P["dedupe"][1], "content": "z"}, "Edit", "s15")
    other_product = run({"file_path": P["never"][1], "content": "y"}, "Write", "s15")
    new_session = run({"file_path": P["dedupe"][1], "content": "y"}, "Write", "s15-b")
    _check(first, "silent-recorder", True)
    _check(second, "silent-recorder", False)
    assert second["row"]["outcome"] == "warn-suppressed" and second["stdout"] == "", second
    _check(other_product, "silent-recorder", True)
    _check(new_session, "silent-recorder", True)


def test_16_index_missing_degrades_cleanly():
    os.rename(INDEX, INDEX + ".aside")
    try:
        r = run({"file_path": P["silent"][1], "content": "y"}, "Write", "s16")
        _check(r, "witness-index-missing", False)
        assert r["stdout"] == "" and r["row"]["refresh_kicked"] is False, r
    finally:
        os.rename(INDEX + ".aside", INDEX)


def test_17_malformed_index_degrades_cleanly():
    saved = open(INDEX).read()
    try:
        for raw in ("{not json", json.dumps({"schema": "something-else", "products": {}}), "[]"):
            write_index(raw=raw)
            r = run({"file_path": P["silent"][1], "content": "y"}, "Write", "s17")
            _check(r, "witness-index-malformed", False)
    finally:
        write_index(raw=saved)


def test_18_bypass_writes_nothing():
    r = run({"file_path": P["silent"][1], "content": "y"}, "Write", "s18", bypass=True)
    assert r["rc"] == 0 and r["rows"] == 0 and r["stdout"] == "", r


def test_19_stale_index_kicks_a_detached_rebuild():
    """Index two days old: the hook answers from it at once and starts the builder, which
    rebuilds from the fixture store; a second call inside the hour does not kick again."""
    saved = open(INDEX).read()
    with open(os.path.join(STORE, "2026-09-25.jsonl"), "w") as fh:
        ts = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime(time.time() - 3600))
        fh.write(json.dumps({"event_id": "EVT-1", "ingested_at": ts, "source_system": "intent",
                             "event": {"ts": ts, "product": "silent", "event": "x",
                                       "attributes": {"adapter": "intent-events-jsonl"}}}) + "\n")
    try:
        write_index(built_ago_s=2 * DAY)
        r = run({"file_path": P["silent"][1], "content": "y"}, "Write", "s19",
                env_extra={"WITNESS_INDEX_NO_REFRESH": "0"})
        _check(r, "silent-recorder", True)
        assert r["row"]["refresh_kicked"] is True and r["row"]["index_age_h"] >= 47, r["row"]
        deadline = time.time() + 20
        rebuilt = None
        while time.time() < deadline:
            try:
                d = json.load(open(INDEX))
                if d.get("built_at_epoch", 0) > time.time() - 600:
                    rebuilt = d
                    break
            except Exception:
                pass
            time.sleep(0.2)
        assert rebuilt is not None, "builder did not rebuild the index within 20 s"
        assert rebuilt["products"]["silent"]["count_30d"] == 1, rebuilt["products"]
        r2 = run({"file_path": P["silent"][1], "content": "y"}, "Write", "s19-b",
                 env_extra={"WITNESS_INDEX_NO_REFRESH": "0"})
        _check(r2, "recorder-active", False)
        assert r2["row"]["refresh_kicked"] is False, r2["row"]
    finally:
        os.remove(os.path.join(STORE, "2026-09-25.jsonl"))
        for suffix in (".state", ".kick"):
            if os.path.exists(INDEX + suffix):
                os.remove(INDEX + suffix)
        write_index(raw=saved)


def test_20_latency_under_budget():
    """21 full-path runs: index read, lookup, field lint, the note, and the hook.fire emit."""
    inbox = os.path.join(TMP, "inbox-latency")
    times = []
    for i in range(LATENCY_RUNS):
        r = run({"file_path": P["fieldy"][1], "content": "y"}, "Write", f"s20-{i}", env_extra=emit_env(inbox))
        assert r["rc"] == 0 and r["row"].get("detection") == "nonconformant-events", r
        times.append(r["ms"])
    med = statistics.median(times)
    print(f"      latency: median {med:.1f} ms, max {max(times):.1f} ms over {len(times)} full-path runs "
          f"with the Witness emit on (budget {LATENCY_BUDGET_MS} ms for the whole hook)")
    assert len(inbox_events(inbox)) == LATENCY_RUNS, "one hook.fire event per run"
    assert med < LATENCY_BUDGET_MS, times



def test_21_no_actions_declared_with_reason_is_skipped():
    r = run({"file_path": P["noact"][1], "content": "y"}, "Write", "s21")
    _check(r, "no-actions-declared", False)
    assert r["row"]["outcome"] == "skip" and r["row"]["reason"] == "content repo, markdown only", r["row"]
    assert r["stdout"] == "", r["stdout"]


def test_22_bare_none_without_reason_still_warns():
    r = run({"file_path": P["barenone"][1], "content": "y"}, "Write", "s22")
    _check(r, "silent-recorder", True)
    assert "witness_actions: none (<named reason>)" in r["ctx"], r["ctx"]


# ---- added 2026-09-26: field lint (WS-DDR-150) ----

def test_23_mostly_nonconformant_active_product_is_told_once_naming_the_field():
    first = run({"file_path": P["fieldy"][1], "content": "y"}, "Write", "s23")
    _check(first, "nonconformant-events", False)
    assert first["field_note"] and first["row"]["outcome"] == "warn", first
    ctx = first["ctx"]
    assert "9 of 10" in ctx and "most often caller" in ctx and "emit.py" in ctx, ctx
    assert ". " not in ctx and ctx.endswith("when given duration_ms."), "one plain sentence: " + ctx
    assert "caller" in json.loads(first["stdout"])["systemMessage"], first["stdout"]
    assert first["row"]["lint_events"] == 10 and first["row"]["lint_nonconformant"] == 9, first["row"]
    assert first["row"]["lint_most_missing"] == "caller", first["row"]
    again = run({"file_path": P["fieldy"][1], "content": "z"}, "Edit", "s23")
    _check(again, "nonconformant-events", False)
    assert again["row"]["outcome"] == "warn-suppressed" and again["stdout"] == "", again
    other = run({"file_path": P["fieldy"][1], "content": "y"}, "Write", "s23-b")
    assert other["field_note"], other


def test_31_the_remedy_fits_what_is_missing():
    """emit.py supplies everything but duration_ms and redaction_level. A product already on
    emit.py is told the argument to pass; one missing a field emit.py supplies is told to use
    emit.py, even when duration_ms is the single most missing field (Witness's own linker on
    2026-09-26: duration_ms missing on every event, caller on all but one)."""
    cases = (("slowy", "most often duration_ms", "pass duration_ms to"),
             ("engy", "most often redaction_level", "pass redaction_level client-confidential to"),
             ("mixy", "most often duration_ms", "report through"))
    for name, most, remedy in cases:
        r = run({"file_path": P[name][1], "content": "y"}, "Write", "s31")
        _check(r, "nonconformant-events", False)
        assert most in r["ctx"] and remedy in r["ctx"] and "emit.py" in r["ctx"], (name, r["ctx"])
        assert ". " not in r["ctx"], r["ctx"]


def test_24_mostly_conformant_active_product_stays_quiet():
    r = run({"file_path": P["tidy"][1], "content": "y"}, "Write", "s24")
    _check(r, "recorder-active", False)
    assert r["stdout"] == "" and r["row"]["lint_events"] == 10 and r["row"]["lint_nonconformant"] == 3, r


def test_25_legacy_only_events_never_nag():
    r = run({"file_path": P["oldie"][1], "content": "y"}, "Write", "s25")
    _check(r, "recorder-active", False)
    assert r["stdout"] == "", r
    assert r["row"]["lint_events"] == 0 and r["row"]["lint_legacy_events"] == 500, r["row"]


def test_26_lint_merges_across_declared_names():
    # split-a: 4 of 4 miss run_id; split-b: 6 of 6 carry every field. Merged 4 of 10 is not "mostly".
    r = run({"file_path": P["split"][1], "content": "y"}, "Write", "s26")
    _check(r, "recorder-active", False)
    assert r["row"]["lint_events"] == 10 and r["row"]["lint_nonconformant"] == 4, r["row"]
    assert r["row"]["lint_most_missing"] == "run_id", r["row"]


def test_27_index_without_lint_stays_quiet():
    r = run({"file_path": P["active"][1], "content": "y"}, "Write", "s27")
    _check(r, "recorder-active", False)
    assert "lint_events" not in r["row"], r["row"]


def test_28_silent_note_points_at_emit_py():
    r = run({"file_path": P["never"][1], "content": "y"}, "Write", "s28")
    _check(r, "silent-recorder", True)
    assert "emit.py" in r["ctx"] and "WS-DDR-150" in r["ctx"] and "under the name never" in r["ctx"], r["ctx"]


def test_29_every_fire_emits_one_conformant_hook_fire_event():
    inbox = os.path.join(TMP, "inbox-29")
    env = emit_env(inbox)
    fires = [
        (run({"file_path": P["never"][1], "content": "y"}, "Write", "s29", env_extra=env), "silent-recorder", "ok"),
        (run({"file_path": P["active"][1], "content": "y"}, "Write", "s29", env_extra=env), "recorder-active", "ok"),
        (run({"command": "ls"}, "Bash", "s29", env_extra=env), "no-context", "skipped"),
        (run({"file_path": P["eng"][1], "content": "y"}, "Write", "s29", env_extra=env), "engagement-exempt", "skipped"),
    ]
    events = inbox_events(inbox)
    assert len(events) == len(fires), events
    for (r, detection, outcome), ev in zip(fires, events):
        assert r["rc"] == 0 and r["stderr"] == "", r
        assert ev["product"] == "intent" and ev["event"] == "hook.fire", ev
        a = ev["attributes"]
        assert a["detection"] == detection and a["outcome"] == outcome, (detection, a)
        assert a["caller"] == "hook:signal-recorder-silent-check" and a["session"] == "s29", a
        assert isinstance(a["duration_ms"], (int, float)) and a["machine"] and a["run_id"], a
        assert wsi.lint_event(ev, "intent") == ("rule", []), wsi.lint_event(ev, "intent")
    assert events[0]["attributes"]["told_session"] is True and events[0]["attributes"]["target"] == "never"
    eng = events[3]
    assert eng["attributes"]["target"].startswith("sha256:"), eng
    assert eng["attributes"]["redaction_level"] == "client-confidential", eng
    assert "Client" not in json.dumps(eng) and "Engagements" not in json.dumps(eng), eng
    assert "target" not in events[2]["attributes"], events[2]


def test_30_emit_failure_never_breaks_the_hook():
    broken = os.path.join(TMP, "broken_emit.py")
    with open(broken, "w") as fh:
        fh.write("raise RuntimeError('emit module broken on purpose')\n")
    not_a_dir = os.path.join(TMP, "inbox-is-a-file")
    with open(not_a_dir, "w") as fh:
        fh.write("x\n")
    for i, env in enumerate(({"WITNESS_EMIT": broken}, {"WITNESS_EMIT": real_emit_py(), "WITNESS_INBOX": not_a_dir})):
        r = run({"file_path": P["never"][1], "content": "y"}, "Write", f"s30-{i}", env_extra=env)
        assert r["rc"] == 0 and r["row"]["detection"] == "silent-recorder" and r["warned"], r
        json.loads(r["stdout"])  # the note is intact: stdout is still one JSON object
        assert "witness-emit: not recorded" in r["stderr"], r["stderr"]
    r = run({"file_path": P["never"][1], "content": "y"}, "Write", "s30-absent",
            env_extra={"WITNESS_EMIT": os.path.join(TMP, "no-such-emit.py")})
    assert r["rc"] == 0 and r["stderr"] == "" and r["warned"], r


def _tree_file(*parts, intent=None):
    """A file at TMP/<parts...>/src/thing.py; optional .intent/INTENT.md body at TMP/<parts...>."""
    root = os.path.join(TMP, *parts)
    os.makedirs(os.path.join(root, "src"), exist_ok=True)
    if intent is not None:
        os.makedirs(os.path.join(root, ".intent"), exist_ok=True)
        with open(os.path.join(root, ".intent", "INTENT.md"), "w") as fh:
            fh.write(intent)
    target = os.path.join(root, "src", "thing.py")
    with open(target, "w") as fh:
        fh.write("x = 1\n")
    return root, target


# ---- WS-DDR-150 scope: every product under Core/products, Core/frameworks, Home ----

def test_32_undeclared_product_without_intent_dir_is_in_scope():
    write_index()
    _, target = _tree_file("Core", "products", "scopedprod")
    r = run({"file_path": target, "content": "y"}, "Write", "s32")
    _check(r, "silent-recorder", True)
    out = json.loads(r["stdout"])
    ctx = out["hookSpecificOutput"]["additionalContext"]
    assert "WS-DDR-150" in ctx and "is a product" in ctx and "declares autonomy" not in ctx, ctx
    assert r["row"]["names"] == ["scopedprod"], r["row"]


def test_33_sibling_worktree_path_reads_as_the_product():
    write_index()
    _, target = _tree_file("Core", "products", "scopedwt-wt-2026-09-26-task")
    r = run({"file_path": target, "content": "y"}, "Write", "s33")
    _check(r, "silent-recorder", True)
    assert r["row"]["names"] == ["scopedwt"], r["row"]


def test_34_intake_package_keeps_the_declaration_gate():
    write_index()
    _, target = _tree_file("Core", "products", "_intake", "2026-09-26-pkg", intent="---\ntitle: plain\n---\n")
    _check(run({"file_path": target, "content": "y"}, "Write", "s34"), "no-lambda-declaration", False)


def test_35_home_product_is_in_scope():
    write_index()
    _, target = _tree_file("Home", "someroom", intent="---\ntitle: a room\n---\n")
    _check(run({"file_path": target, "content": "y"}, "Write", "s35"), "silent-recorder", True)


def test_36_in_scope_product_declaring_no_actions_is_skipped():
    write_index()
    _, target = _tree_file("Core", "frameworks", "contentonly",
                           intent="---\ntitle: c\n---\nwitness_actions: none (content repo, no scripts)\n")
    _check(run({"file_path": target, "content": "y"}, "Write", "s36"), "no-actions-declared", False)


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
