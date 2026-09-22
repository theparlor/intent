#!/usr/bin/env python3
"""Test harness for session-end.sh's signals_captured evidence ladder.

The old writer treated every signal file whose mtime fell inside the last
60 minutes as "captured" by whichever session happened to be stopping —
a coincidence of the clock, not attribution. This suite pins the narrowed
behavior: signals_captured now requires evidence (frontmatter naming the
session, a Write/Edit tool_use in the session's own transcript, or a
commit on the cwd's current branch), while the old broad mtime sweep is
kept, unmodified, under signals_seen so nothing is lost.

Run: python3 tests/test_session_end_signals_captured.py
"""
import json
import os
import shutil
import subprocess
import sys
import tempfile
import uuid

HOOK = os.environ.get(
    "SESSION_END_HOOK_PATH",
    os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "session-end.sh"),
)

fails = []


def check(desc, cond, detail=""):
    ok = bool(cond)
    print(f"  {'PASS' if ok else 'FAIL'}  {desc}")
    if not ok:
        fails.append(f"{desc} {detail}".strip())


def make_root(tmp):
    """A fresh git repo with .intent/signals/ — the writer's find_intent_root anchor."""
    root = tempfile.mkdtemp(prefix="root-", dir=tmp)
    os.makedirs(os.path.join(root, ".intent", "signals"))
    os.makedirs(os.path.join(root, ".intent", "events"))
    subprocess.run(["git", "init", "-q", root], check=True)
    subprocess.run(["git", "-C", root, "config", "user.email", "test@example.com"], check=True)
    subprocess.run(["git", "-C", root, "config", "user.name", "Test"], check=True)
    # An initial commit so HEAD/branch resolution works.
    readme = os.path.join(root, "README.md")
    with open(readme, "w") as f:
        f.write("root\n")
    subprocess.run(["git", "-C", root, "add", "README.md"], check=True)
    subprocess.run(["git", "-C", root, "commit", "-q", "-m", "init"], check=True)
    return root


def write_signal(root, name, frontmatter_session=None, extra="body"):
    path = os.path.join(root, ".intent", "signals", name)
    fm_lines = ["---", "type: signal", f"id: {name}"]
    if frontmatter_session:
        fm_lines.append(f"session: {frontmatter_session}")
    fm_lines.append("---")
    with open(path, "w") as f:
        f.write("\n".join(fm_lines) + f"\n\n# {name}\n\n{extra}\n")
    return path


def write_transcript(tmp, writes):
    """writes: list of (tool_name, file_path) -> a transcript.jsonl with one
    assistant message carrying one tool_use block per entry."""
    path = os.path.join(tmp, f"transcript-{uuid.uuid4()}.jsonl")
    content = []
    for tool_name, file_path in writes:
        content.append({
            "type": "tool_use",
            "id": f"toolu_{uuid.uuid4().hex[:8]}",
            "name": tool_name,
            "input": {"file_path": file_path},
        })
    line = {"type": "assistant", "message": {"content": content}}
    with open(path, "w") as f:
        f.write(json.dumps(line) + "\n")
    return path


def run_hook(root, session_id, transcript_path=None, extra_env=None):
    payload = {"session_id": session_id}
    if transcript_path:
        payload["transcript_path"] = transcript_path
    env = dict(os.environ)
    env["INTENT_SESSION_END_ROOT"] = root
    # Fixed machine id: the hook writes events.<machine-id>.jsonl (P4 shard).
    env["INTENT_SESSION_END_MACHINE"] = "test"
    env.pop("CLAUDE_SESSION_ID", None)
    if extra_env:
        env.update(extra_env)
    p = subprocess.run(
        ["bash", HOOK], input=json.dumps(payload), env=env,
        capture_output=True, text=True, timeout=30,
    )
    return p


def last_event(root):
    events_path = os.path.join(root, ".intent", "events", "events.test.jsonl")
    with open(events_path) as f:
        lines = [l for l in f.read().splitlines() if l.strip()]
    return json.loads(lines[-1])


def all_events(root):
    events_path = os.path.join(root, ".intent", "events", "events.test.jsonl")
    with open(events_path) as f:
        return [json.loads(l) for l in f.read().splitlines() if l.strip()]


TMP = tempfile.mkdtemp(prefix="session-end-signals-test-")

try:
    # ------------------------------------------------------------------
    # Case 1: two overlapping sessions each capture only their own files,
    # via transcript Write evidence (rung 2). Both files share one mtime
    # window, so the OLD mtime-only sweep would have handed both files to
    # both sessions.
    print("Case 1: overlapping sessions, transcript evidence, own files only")
    root1 = make_root(TMP)
    sess_a = str(uuid.uuid4())
    sess_b = str(uuid.uuid4())
    path_a = write_signal(root1, "a-owned-by-sess-a.md")
    path_b = write_signal(root1, "b-owned-by-sess-b.md")
    transcript_a = write_transcript(TMP, [("Write", path_a)])
    transcript_b = write_transcript(TMP, [("Edit", path_b)])

    p_a = run_hook(root1, sess_a, transcript_path=transcript_a)
    check("session A hook exits 0", p_a.returncode == 0, p_a.stderr)
    p_b = run_hook(root1, sess_b, transcript_path=transcript_b)
    check("session B hook exits 0", p_b.returncode == 0, p_b.stderr)

    events1 = all_events(root1)
    check("two events written", len(events1) == 2, str(len(events1)))
    ev_a, ev_b = events1[0], events1[1]
    check("session A captured only its own file",
          ev_a["data"]["signals_captured"] == ["a-owned-by-sess-a.md"],
          str(ev_a["data"]["signals_captured"]))
    check("session B captured only its own file",
          ev_b["data"]["signals_captured"] == ["b-owned-by-sess-b.md"],
          str(ev_b["data"]["signals_captured"]))
    check("session A's signals_seen still includes both files (nothing lost)",
          set(ev_a["data"].get("signals_seen", [])) >= {"a-owned-by-sess-a.md", "b-owned-by-sess-b.md"},
          str(ev_a["data"].get("signals_seen")))

    # ------------------------------------------------------------------
    # Case 2: a file with no evidence at all sits in signals_seen (mtime
    # window) but never in signals_captured.
    print("Case 2: no-evidence file is seen, never captured")
    root2 = make_root(TMP)
    sess_c = str(uuid.uuid4())
    path_c = write_signal(root2, "c-no-evidence.md")
    p_c = run_hook(root2, sess_c)  # no transcript at all
    check("hook exits 0 with no transcript", p_c.returncode == 0, p_c.stderr)
    ev_c = last_event(root2)
    check("no-evidence file NOT in signals_captured",
          "c-no-evidence.md" not in ev_c["data"]["signals_captured"],
          str(ev_c["data"]["signals_captured"]))
    check("no-evidence file IS in signals_seen",
          "c-no-evidence.md" in ev_c["data"].get("signals_seen", []),
          str(ev_c["data"].get("signals_seen")))

    # ------------------------------------------------------------------
    # Case 3: missing/unreadable transcript path -> fail open, hook still
    # exits 0 and writes an event; signals_captured falls back to
    # frontmatter + git evidence only.
    print("Case 3: missing transcript -> fail open, frontmatter evidence still works")
    root3 = make_root(TMP)
    sess_d = str(uuid.uuid4())
    path_d = write_signal(root3, "d-frontmatter-owned.md", frontmatter_session=sess_d)
    bogus_transcript = os.path.join(TMP, "does-not-exist.jsonl")
    p_d = run_hook(root3, sess_d, transcript_path=bogus_transcript)
    check("hook exits 0 with a missing transcript file", p_d.returncode == 0, p_d.stderr)
    ev_d = last_event(root3)
    check("frontmatter-evidenced file captured despite missing transcript",
          "d-frontmatter-owned.md" in ev_d["data"]["signals_captured"],
          str(ev_d["data"]["signals_captured"]))

    # Compound value in frontmatter: "session: <id> (worktree name)" still
    # tokenizes to a match, per the loom PR 9 convention this writer feeds.
    print("Case 3b: compound frontmatter value tokenizes")
    root3b = make_root(TMP)
    sess_e = str(uuid.uuid4())
    path_e = write_signal(root3b, "e-compound-frontmatter.md",
                           frontmatter_session=f"{sess_e} (events-writer)")
    p_e = run_hook(root3b, sess_e)
    check("compound frontmatter value still matches", p_e.returncode == 0, p_e.stderr)
    ev_e = last_event(root3b)
    check("compound-frontmatter file captured",
          "e-compound-frontmatter.md" in ev_e["data"]["signals_captured"],
          str(ev_e["data"]["signals_captured"]))

    # ------------------------------------------------------------------
    # Case 4: a commit on the cwd's current branch touching the signal
    # file counts as evidence (rung 3), even with no frontmatter tag and
    # no transcript at all.
    print("Case 4: branch-commit evidence (rung 3)")
    root4 = make_root(TMP)
    sess_f = str(uuid.uuid4())
    path_f = write_signal(root4, "f-committed-no-frontmatter.md")
    subprocess.run(["git", "-C", root4, "add", ".intent/signals/f-committed-no-frontmatter.md"], check=True)
    subprocess.run(["git", "-C", root4, "commit", "-q", "-m", "signal: f"], check=True)
    p_f = run_hook(root4, sess_f)
    check("hook exits 0 after a real commit", p_f.returncode == 0, p_f.stderr)
    ev_f = last_event(root4)
    check("committed file captured via branch evidence",
          "f-committed-no-frontmatter.md" in ev_f["data"]["signals_captured"],
          str(ev_f["data"]["signals_captured"]))

    # ------------------------------------------------------------------
    print("Case 5: per-machine shard (P4); role and name recorded, never gating")
    root5 = make_root(TMP)
    mj = os.path.join(TMP, "machine.json")
    with open(mj, "w") as f:
        json.dump({"role": "travel", "name": 'Faus"tina\\x', "serial": "ABC123"}, f)
    p_g = run_hook(root5, str(uuid.uuid4()),
                   extra_env={"INTENT_SESSION_END_MACHINE": "Serial-ABC 123",
                              "CLAUDE_MACHINE_JSON": mj})
    check("hook exits 0 with a machine.json present", p_g.returncode == 0, p_g.stderr)
    shard = os.path.join(root5, ".intent", "events", "events.serial-abc-123.jsonl")
    check("machine id is slugged and lowercased into the shard name", os.path.isfile(shard),
          str(os.listdir(os.path.join(root5, ".intent", "events"))))
    with open(shard) as f:
        ev_g = json.loads(f.read().splitlines()[-1])
    check("row is version 0.2.0", ev_g["version"] == "0.2.0", ev_g["version"])
    check("source.machine carries serial, role, escaped name",
          ev_g["source"]["machine"] == {"serial": "serial-abc-123", "role": "travel",
                                        "name": 'Faus"tina\\x'},
          str(ev_g["source"].get("machine")))

    root6 = make_root(TMP)
    env_unset = {"CLAUDE_MACHINE_JSON": os.path.join(TMP, "absent.json")}
    saved = os.environ.pop("INTENT_SESSION_END_MACHINE", None)
    env6 = dict(os.environ)
    env6["INTENT_SESSION_END_ROOT"] = root6
    env6.pop("CLAUDE_SESSION_ID", None)
    env6.update(env_unset)
    p_h = subprocess.run(["bash", HOOK], input=json.dumps({"session_id": str(uuid.uuid4())}),
                         env=env6, capture_output=True, text=True, timeout=30)
    if saved is not None:
        os.environ["INTENT_SESSION_END_MACHINE"] = saved
    names6 = sorted(os.listdir(os.path.join(root6, ".intent", "events")))
    check("unknown role still writes (capture is never gated)", p_h.returncode == 0 and len(names6) == 1,
          str(names6))
    check("default machine id never writes the legacy events.jsonl", "events.jsonl" not in names6,
          str(names6))
    with open(os.path.join(root6, ".intent", "events", names6[0])) as f:
        ev_h = json.loads(f.read().splitlines()[-1])
    check("absent machine.json records role unknown", ev_h["source"]["machine"]["role"] == "unknown",
          str(ev_h["source"]["machine"]))

finally:
    shutil.rmtree(TMP, ignore_errors=True)

print()
if fails:
    print(f"FAILED: {len(fails)} check(s)")
    for f in fails:
        print(f"  - {f}")
    sys.exit(1)
print("ALL PASS")
sys.exit(0)
