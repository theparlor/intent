#!/usr/bin/env python3
"""Test harness for response-lint-stop-check.sh. Runs the hook under a throwaway HOME
so real audit logs are untouched. Asserts each rule + the consolidation behavior."""
import json, os, subprocess, tempfile, sys

HOOK = "/Users/brien/Workspaces/Core/frameworks/intent/hooks/response-lint-stop-check.sh"
TMP = tempfile.mkdtemp(prefix="lint-test-")
FAKE_HOME = os.path.join(TMP, "home")
os.makedirs(os.path.join(FAKE_HOME, ".claude", "audit"), exist_ok=True)
MODEL_LOG = os.path.join(FAKE_HOME, ".claude", "audit", "model-effort-detections.log")

CLEAN_FILLER = ("The audit runs a check and records the outcome in plain words. " * 16)  # ~990 chars, clean
MODEL_LINE = "Model: Opus 4.8 . Effort: high\n\n"

def run(last_text, stop_active=False):
    tpath = os.path.join(TMP, "t.jsonl")
    with open(tpath, "w") as f:
        f.write(json.dumps({"type": "user", "message": {"content": "hi"}}) + "\n")
        f.write(json.dumps({"type": "assistant",
                            "message": {"content": [{"type": "text", "text": last_text}]}}) + "\n")
    hook_input = json.dumps({"transcript_path": tpath, "session_id": "test",
                             "stop_hook_active": stop_active})
    env = dict(os.environ); env["HOME"] = FAKE_HOME
    p = subprocess.run(["bash", HOOK], input=hook_input, env=env,
                       capture_output=True, text=True)
    return p.stdout.strip()

def model_log_count():
    if not os.path.exists(MODEL_LOG):
        return 0
    return sum(1 for _ in open(MODEL_LOG))

results = []
def check(name, cond):
    results.append((name, cond))
    print(("PASS " if cond else "FAIL ") + name)

# T1: clean substantive w/ model line -> no block
out = run(MODEL_LINE + CLEAN_FILLER)
check("T1 clean+model -> no block", out == "")

# T2: em-dash -> block DASH-GLYPH
out = run("This has an em dash — right here, and it is not allowed.")
check("T2 emdash -> DASH-GLYPH block", "DASH-GLYPH DRIFT" in out)

# T3: backtick-wrapped workspace path -> block LINK-FORMAT
out = run("See `/Users/brien/Workspaces/Core/foo.md` for the detail you want.")
check("T3 backtick path -> LINK-FORMAT block", "LINK-FORMAT DRIFT" in out)

# T4: BOTH em-dash and backtick path -> ONE block object containing BOTH reasons
out = run("Fix `/Users/brien/Workspaces/Core/foo.md` — then re-run the check.")
one_json = False
try:
    obj = json.loads(out); one_json = obj.get("decision") == "block"
except Exception:
    one_json = False
check("T4 both -> single block obj", one_json)
check("T4 both -> contains DASH-GLYPH", "DASH-GLYPH DRIFT" in out)
check("T4 both -> contains LINK-FORMAT", "LINK-FORMAT DRIFT" in out)

# T5: send-ready content w/o assertion audit -> block PRE-SEND
out = run("This note is ready to send to the client. Just paste it over to them.")
check("T5 send no-audit -> PRE-SEND block", "PRE-SEND ASSERTION DRIFT" in out)

# T5b: send-ready WITH an assertion-audit marker -> NOT blocked (suppressed)
out = run("This note is ready to send to the client. assertion-audit: every claim sourced below.")
check("T5b send + audit marker -> no presend block", "PRE-SEND ASSERTION DRIFT" not in out)

# T6: substantive, NO model line, clean -> no block BUT one model-effort WARN logged
before = model_log_count()
out = run(CLEAN_FILLER)
after = model_log_count()
check("T6 substantive no-model -> no block", out == "")
check("T6 substantive no-model -> WARN logged", after == before + 1)

# T7: short, no model line -> no block AND no WARN (below length threshold)
before = model_log_count()
out = run("Quick clean note, nothing to see here.")
after = model_log_count()
check("T7 short no-model -> no block", out == "")
check("T7 short no-model -> no WARN", after == before)

# T8: recursion guard (stop_hook_active) -> no output even with an em-dash present
out = run("has an em dash — here", stop_active=True)
check("T8 recursion guard -> no output", out == "")

# T9: code-fence exemption -> backtick path INSIDE a fence does NOT block link-format
out = run(MODEL_LINE + "Example only:\n```\nsee `/Users/brien/Workspaces/x.md`\n```\nCarry on with the plan.")
check("T9 fenced path -> no LINK-FORMAT block", "LINK-FORMAT DRIFT" not in out)

# T9b: same path OUTSIDE a fence DOES block (control for T9)
out = run("see `/Users/brien/Workspaces/x.md` inline in prose here")
check("T9b inline path -> LINK-FORMAT block", "LINK-FORMAT DRIFT" in out)

# T10: em-dash INSIDE a fence STILL blocks (emdash has no fence exemption, by design)
out = run("```\ncode with an em dash — inside\n```")
check("T10 fenced emdash -> still blocks", "DASH-GLYPH DRIFT" in out)

# --- multi-line-message hardening (2026-07-18): one response splits across multiple
# --- assistant JSONL lines sharing a message.id; lint the joined final-message text.
def run_split(items, stop_active=False):
    # items: list of (block_type, text); each becomes its own JSONL assistant line,
    # all sharing ONE message.id (id="MSGSPLIT1").
    tpath = os.path.join(TMP, "t.jsonl")
    with open(tpath, "w") as f:
        f.write(json.dumps({"type": "user", "message": {"content": "hi"}}) + "\n")
        for bt, tx in items:
            if bt == "text":
                block = {"type": "text", "text": tx}
            else:
                block = {"type": "tool_use", "id": "tool_x", "name": "X", "input": {}}
            f.write(json.dumps({"type": "assistant",
                                "message": {"id": "MSGSPLIT1", "content": [block]}}) + "\n")
    hook_input = json.dumps({"transcript_path": tpath, "session_id": "test",
                             "stop_hook_active": stop_active})
    env = dict(os.environ); env["HOME"] = FAKE_HOME
    p = subprocess.run(["bash", HOOK], input=hook_input, env=env,
                       capture_output=True, text=True)
    return p.stdout.strip()

# T11: em-dash in the FIRST text block of a split final response -> caught (was missed)
out = run_split([("text", "clean intro with an em dash — here"), ("text", "more clean text after")])
check("T11 glyph in earlier split-block -> caught", "DASH-GLYPH DRIFT" in out)

# T11b: final block is tool_use (no text) but an earlier same-id text block has a bad path -> caught
out = run_split([("text", "see `/Users/brien/Workspaces/x.md` inline"), ("tool_use", "")])
check("T11b bad path before trailing tool_use -> caught", "LINK-FORMAT DRIFT" in out)

print()
passed = sum(1 for _, c in results if c)
total = len(results)
print("RESULT: %d/%d passed" % (passed, total))
sys.exit(0 if passed == total else 1)
