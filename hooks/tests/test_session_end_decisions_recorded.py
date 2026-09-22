#!/usr/bin/env python3
"""Test harness for session-end.sh's decisions_recorded evidence ladder.

decisions_recorded used to be the mtime sweep verbatim: every
.intent/decisions/*.md file changed in the last 60 minutes, whoever wrote
it. That is the same coincidence-of-the-clock failure mode signals_captured
had before the loom PR 9 fix (test_session_end_signals_captured.py). This
suite pins the narrowed behavior for decisions: decisions_recorded now
requires evidence via the SAME shared evidence_ladder_captured() helper
(frontmatter naming the session, a Write/Edit tool_use in the session's own
transcript, or a commit on the cwd's current branch), while the old broad
mtime sweep is kept, unmodified, under decisions_seen so nothing is lost.

Run: python3 hooks/tests/test_session_end_decisions_recorded.py
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
    """A fresh git repo with .intent/decisions/ (the writer's find_intent_root anchor)."""
    root = tempfile.mkdtemp(prefix="root-", dir=tmp)
    os.makedirs(os.path.join(root, ".intent", "decisions"))
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


def write_decision(root, name, frontmatter_session=None, extra="body"):
    path = os.path.join(root, ".intent", "decisions", name)
    fm_lines = ["---", "type: decision", f"id: {name}"]
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


TMP = tempfile.mkdtemp(prefix="session-end-decisions-test-")

try:
    # ------------------------------------------------------------------
    # Case 1: two overlapping sessions each capture only their own
    # decision files, via transcript Write evidence (rung 2). Both files
    # share one mtime window, so the OLD mtime-only sweep would have
    # handed both files to both sessions.
    print("Case 1: overlapping sessions, transcript evidence, own files only")
    root1 = make_root(TMP)
    sess_a = str(uuid.uuid4())
    sess_b = str(uuid.uuid4())
    path_a = write_decision(root1, "a-owned-by-sess-a.md")
    path_b = write_decision(root1, "b-owned-by-sess-b.md")
    transcript_a = write_transcript(TMP, [("Write", path_a)])
    transcript_b = write_transcript(TMP, [("Edit", path_b)])

    p_a = run_hook(root1, sess_a, transcript_path=transcript_a)
    check("session A hook exits 0", p_a.returncode == 0, p_a.stderr)
    p_b = run_hook(root1, sess_b, transcript_path=transcript_b)
    check("session B hook exits 0", p_b.returncode == 0, p_b.stderr)

    events1 = all_events(root1)
    check("two events written", len(events1) == 2, str(len(events1)))
    ev_a, ev_b = events1[0], events1[1]
    check("session A recorded only its own file",
          ev_a["data"]["decisions_recorded"] == ["a-owned-by-sess-a.md"],
          str(ev_a["data"]["decisions_recorded"]))
    check("session B recorded only its own file",
          ev_b["data"]["decisions_recorded"] == ["b-owned-by-sess-b.md"],
          str(ev_b["data"]["decisions_recorded"]))
    check("session A's decisions_seen still includes both files (nothing lost)",
          set(ev_a["data"].get("decisions_seen", [])) >= {"a-owned-by-sess-a.md", "b-owned-by-sess-b.md"},
          str(ev_a["data"].get("decisions_seen")))

    # ------------------------------------------------------------------
    # Case 2: a file with no evidence at all sits in decisions_seen (mtime
    # window) but never in decisions_recorded.
    print("Case 2: no-evidence file is seen, never recorded")
    root2 = make_root(TMP)
    sess_c = str(uuid.uuid4())
    path_c = write_decision(root2, "c-no-evidence.md")
    p_c = run_hook(root2, sess_c)  # no transcript at all
    check("hook exits 0 with no transcript", p_c.returncode == 0, p_c.stderr)
    ev_c = last_event(root2)
    check("no-evidence file NOT in decisions_recorded",
          "c-no-evidence.md" not in ev_c["data"]["decisions_recorded"],
          str(ev_c["data"]["decisions_recorded"]))
    check("no-evidence file IS in decisions_seen",
          "c-no-evidence.md" in ev_c["data"].get("decisions_seen", []),
          str(ev_c["data"].get("decisions_seen")))

    # ------------------------------------------------------------------
    # Case 3: missing/unreadable transcript path -> fail open, hook still
    # exits 0 and writes an event; decisions_recorded falls back to
    # frontmatter + git evidence only.
    print("Case 3: missing transcript -> fail open, frontmatter evidence still works")
    root3 = make_root(TMP)
    sess_d = str(uuid.uuid4())
    path_d = write_decision(root3, "d-frontmatter-owned.md", frontmatter_session=sess_d)
    bogus_transcript = os.path.join(TMP, "does-not-exist.jsonl")
    p_d = run_hook(root3, sess_d, transcript_path=bogus_transcript)
    check("hook exits 0 with a missing transcript file", p_d.returncode == 0, p_d.stderr)
    ev_d = last_event(root3)
    check("frontmatter-evidenced file recorded despite missing transcript",
          "d-frontmatter-owned.md" in ev_d["data"]["decisions_recorded"],
          str(ev_d["data"]["decisions_recorded"]))

    # Compound value in frontmatter: "session: <id> (worktree name)" still
    # tokenizes to a match, per the loom PR 9 convention this writer feeds.
    print("Case 3b: compound frontmatter value tokenizes")
    root3b = make_root(TMP)
    sess_e = str(uuid.uuid4())
    path_e = write_decision(root3b, "e-compound-frontmatter.md",
                             frontmatter_session=f"{sess_e} (events-writer)")
    p_e = run_hook(root3b, sess_e)
    check("compound frontmatter value still matches", p_e.returncode == 0, p_e.stderr)
    ev_e = last_event(root3b)
    check("compound-frontmatter file recorded",
          "e-compound-frontmatter.md" in ev_e["data"]["decisions_recorded"],
          str(ev_e["data"]["decisions_recorded"]))

    # ------------------------------------------------------------------
    # Case 4: a commit on the cwd's current branch touching the decision
    # file counts as evidence (rung 3), even with no frontmatter tag and
    # no transcript at all.
    print("Case 4: branch-commit evidence (rung 3)")
    root4 = make_root(TMP)
    sess_f = str(uuid.uuid4())
    path_f = write_decision(root4, "f-committed-no-frontmatter.md")
    subprocess.run(["git", "-C", root4, "add", ".intent/decisions/f-committed-no-frontmatter.md"], check=True)
    subprocess.run(["git", "-C", root4, "commit", "-q", "-m", "decision: f"], check=True)
    p_f = run_hook(root4, sess_f)
    check("hook exits 0 after a real commit", p_f.returncode == 0, p_f.stderr)
    ev_f = last_event(root4)
    check("committed file recorded via branch evidence",
          "f-committed-no-frontmatter.md" in ev_f["data"]["decisions_recorded"],
          str(ev_f["data"]["decisions_recorded"]))

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
