#!/usr/bin/env python3
"""Red-green precision test for autonomy-posture-check-layer-4.2.sh
(2026-07-19 false-positive-category patch). Runs the hook against each of the
14 real in-window firings (2026-07-08..07-18), preserved verbatim as inert
fixtures in fixtures/layer42/, under a throwaway HOME so real telemetry/audit
logs are untouched. Harness follows test_response_lint.py's precedent (fake
HOME + subprocess + JSONL transcript construction).

Ground truth: WINDOW-CLOSE READ in Core/products/_intake/
2026-07-19-decision-surfaces-retrofit/layer42-calibration-promote-retire.md.

  - 3 confirmed true positives MUST fire (would_block == 1).
  - 10 confirmed false positives MUST NOT fire (would_block == 0).
  - 1 swing case (firing-06) may go either way; this test asserts its
    POST-PATCH behavior explicitly with a comment, rather than silently
    accepting whichever way it happens to fall.

The hook remains WARN-ONLY throughout (it never prints a block decision to
stdout); this harness reads the throwaway telemetry JSONL it writes under
FAKE_HOME to recover the would_block value per session, since that is the
only channel Layer 4.2 uses to report its verdict.
"""
import json, os, subprocess, tempfile, sys

HOOK = "/Users/brien/Workspaces/Core/frameworks/intent/hooks/autonomy-posture-check-layer-4.2.sh"
FIXTURES_DIR = "/Users/brien/Workspaces/Core/frameworks/intent/hooks/tests/fixtures/layer42"
TMP = tempfile.mkdtemp(prefix="l42-precision-test-")
FAKE_HOME = os.path.join(TMP, "home")
os.makedirs(os.path.join(FAKE_HOME, ".claude", "audit"), exist_ok=True)
os.makedirs(os.path.join(FAKE_HOME, ".claude", "logs"), exist_ok=True)
TELEMETRY_LOG = os.path.join(FAKE_HOME, ".claude", "logs", "autonomy-posture-layer42.jsonl")


def load_fixture(fname):
    path = os.path.join(FIXTURES_DIR, fname)
    with open(path, encoding="utf-8") as f:
        content = f.read()
    header, sep, body = content.partition("\n---\n")
    assert sep, f"{fname}: missing '---' header/body separator"
    assert "inert-test-data" in header, f"{fname}: missing inert-test-data marker"
    return body


def run(session_id, text, stop_active=False):
    tpath = os.path.join(TMP, session_id + ".jsonl")
    with open(tpath, "w", encoding="utf-8") as f:
        f.write(json.dumps({"type": "user", "message": {"content": "hi"}}) + "\n")
        f.write(json.dumps({"type": "assistant",
                            "message": {"content": [{"type": "text", "text": text}]}}) + "\n")
    hook_input = json.dumps({"transcript_path": tpath, "session_id": session_id,
                             "stop_hook_active": stop_active})
    env = dict(os.environ); env["HOME"] = FAKE_HOME
    p = subprocess.run(["bash", HOOK], input=hook_input, env=env,
                       capture_output=True, text=True)
    return p


def would_block_for(session_id):
    """Read the throwaway telemetry log and return the would_block value
    logged for this session_id (last matching line, defensive against reruns)."""
    if not os.path.exists(TELEMETRY_LOG):
        return None
    val = None
    with open(TELEMETRY_LOG, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                d = json.loads(line)
            except Exception:
                continue
            if d.get("session") == session_id:
                val = d.get("would_block")
    return val


results = []
def check(name, cond):
    results.append((name, cond))
    print(("PASS " if cond else "FAIL ") + name)


# --- 3 confirmed true positives: MUST fire (would_block == 1) --------------
TRUE_POSITIVES = [
    ("firing-01-tp-overwatch-l4-eligible-offer.txt", "tp1-overwatch"),
    ("firing-04-tp-bare-either-or-no-recommendation.txt", "tp2-bare-either-or"),
    ("firing-07-tp-want-me-to-action-and-fix.txt", "tp3-want-me-to-action"),
]
for fname, sid in TRUE_POSITIVES:
    text = load_fixture(fname)
    run(sid, text)
    wb = would_block_for(sid)
    check(f"TP {fname} -> would_block=1 (got {wb})", wb == 1)

# --- 10 confirmed false positives: MUST NOT fire (would_block == 0) --------
# One line each: which of the five named categories (or the additional
# recommendation-with-reveal / already-autonomous discriminator, see hook
# comments) suppresses this fixture.
FALSE_POSITIVES = [
    ("firing-02-fp-scout-recommendation-with-reveal.txt", "fp1-scout"),
    ("firing-03-fp-digest-recommendation-with-reveal.txt", "fp2-digest"),
    ("firing-05-fp-fable-window-budget.txt", "fp3-fable-window"),
    ("firing-08-fp-self-quotation-of-trigger-phrase.txt", "fp4-self-quote"),
    ("firing-09-fp-pending-decisions-recommendation-with-reveal.txt", "fp5-pending-decisions"),
    ("firing-10-fp-oauth-reauth.txt", "fp6-oauth"),
    ("firing-11-fp-prod-write-l0.txt", "fp7-prod-write-l0"),
    ("firing-12-fp-nothing-required-fully-autonomous.txt", "fp8-nothing-required"),
    ("firing-13-fp-fable-budget-launch.txt", "fp9-fable-budget-launch"),
    ("firing-14-fp-fable-budget-and-enforcement-change.txt", "fp10-fable-and-enforcement"),
]
for fname, sid in FALSE_POSITIVES:
    text = load_fixture(fname)
    run(sid, text)
    wb = would_block_for(sid)
    check(f"FP {fname} -> would_block=0 (got {wb})", wb == 0)

# --- 1 swing case: assert current (post-patch) behavior explicitly ---------
# firing-06 (2026-07-10T18:36:45Z) is genuinely ambiguous per the window-close
# read: "Say the word is the wrong framing here... unless you object, add it"
# reads as either compliant recommendation-with-reveal or residual soft
# drift. THIS IS THE SWING CASE. This patch resolves it toward NOT
# would-block, for two independent reasons found in the fixture text: (1) it
# contains an explicit stated recommendation ("I recommend folding the
# Zitron re-extract into Task A now") -- the same recommendation-with-reveal
# signal that legitimately suppresses firing-02/03/09 above; (2) it contains
# Fable-window language ("your Fable window closes in about 3 days"),
# matching category 3. That is a defensible, documented resolution consistent
# with how the rest of the corpus was treated, not a silent default -- it is
# asserted explicitly here so any future change to this behavior shows up as
# a visible test diff, never a quiet regression.
text = load_fixture("firing-06-swing-ambiguous.txt")
run("swing-case", text)
wb = would_block_for("swing-case")
check(f"SWING firing-06 -> would_block=0 post-patch (got {wb}), asserted not guessed", wb == 0)

print()
passed = sum(1 for _, c in results if c)
total = len(results)
print("RESULT: %d/%d passed" % (passed, total))
sys.exit(0 if passed == total else 1)
