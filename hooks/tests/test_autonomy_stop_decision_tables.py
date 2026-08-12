#!/usr/bin/env python3
"""Test harness for autonomy-grant-stop-check.sh CHECK 8 (decision-table rows).
Runs the Stop hook under a throwaway HOME so real audit and telemetry logs are
untouched. Pins the existing prose behavior (E cases, CHECKs 1 to 7 unchanged)
and asserts the table matrix (T cases).

Contract under test (engagement backlog row D5, build ordered 2026-08-12):
- Stop hook. stdin = JSON {session_id, transcript_path, stop_hook_active}.
  The hook always exits 0. Blocking = printing {"decision": "block", ...} to
  stdout. Passing = empty stdout.
- CHECK 8 (table layer, structural): a markdown table body row that presents
  a decision or question to the user must carry, IN THAT ROW, either
  (1) a recommendation marker (Recommend / Recommendation: / bold recommend,
      negation-stripped so "no recommendation yet" does not qualify), or
  (2) the D-N154 bucket-three form: the literal phrase
      "No recommendation BY RULE" plus a D-N154 citation
      (two reasoned readings in genuine conflict go to the user side by
      side with no recommendation, BY RULE; the only sanctioned form).
- Decision-row heuristics: a cell that ends a question and carries a decision
  stem (which / should / shall / whether / choose / pick / prefer / approve /
  adopt / or / who decides), or decide/choose/approve/rule-on language
  directed at the user (needs a ruling, decision needed, awaiting approval,
  to be decided, who decides, your call).
- Rows quoting an old decision or reporting a closure are not new asks:
  strikethrough, a closure word with its date in the same cell, or a whole
  status cell that is itself a closure word, all skip.
- Fenced code blocks are stripped before table parsing.
- The block reason names the failing row and BOTH accepted forms.
- Prose responses without tables never reach the analyzer: CHECKs 1 to 7
  behavior is unchanged (the E cases pin it, and they must pass both before
  and after the CHECK 8 change).

Fixtures are modeled on the engagement backlog rows A38/A39 (the sanctioned
bucket-three form) with client-internal specifics genericized; only the
structural form and the D-N154 citation are preserved.
"""
import json, os, subprocess, tempfile, sys

HOOK = "/Users/brien/Workspaces/Core/frameworks/intent/hooks/autonomy-grant-stop-check.sh"
TMP = tempfile.mkdtemp(prefix="stop-table-test-")
FAKE_HOME = os.path.join(TMP, "home")
os.makedirs(FAKE_HOME, exist_ok=True)
AUDIT = os.path.join(FAKE_HOME, ".claude", "audit", "autonomy-grant-stop-detections.log")

_seq = [0]


def run(response_text):
    _seq[0] += 1
    tpath = os.path.join(TMP, "transcript-%d.jsonl" % _seq[0])
    with open(tpath, "w") as fh:
        fh.write(json.dumps({
            "type": "assistant",
            "message": {"content": [{"type": "text", "text": response_text}]},
        }) + "\n")
    payload = json.dumps({"session_id": "t-%d" % _seq[0],
                          "transcript_path": tpath,
                          "stop_hook_active": False})
    env = dict(os.environ)
    env["HOME"] = FAKE_HOME
    env.pop("AUTONOMY_GRANT_STOP_BYPASSED", None)
    p = subprocess.run(["bash", HOOK], input=payload, env=env,
                       capture_output=True, text=True, timeout=90)
    return p.stdout, p.returncode


def blocked(out):
    return '"decision": "block"' in out


def audit_lines():
    if not os.path.exists(AUDIT):
        return []
    with open(AUDIT) as fh:
        return fh.readlines()


results = []


def check(name, cond):
    results.append((name, cond))
    print(("PASS " if cond else "FAIL ") + name)


TABLE_HEAD = "| Id | Item | State | Status |\n|---|---|---|---|\n"

# ---------------------------------------------------------------- E: existing prose behavior (pinned)

# E1: bare-choice question, no recommendation marker anywhere: CHECK 1 blocks
out, rc = run("The migration plan is drafted and both paths are viable. "
              "Want me to execute the dry pass, or go straight to the cutover?")
check("E1 bare-choice prose -> CHECK 1 block", blocked(out) and "CHECK 1" in out and rc == 0)

# E2: same question preceded by a recommendation marker: passes
out, rc = run("Recommendation: execute the dry pass first, because the rollback window is short. "
              "Want me to execute the dry pass, or go straight to the cutover?")
check("E2 bare-choice with recommendation -> pass", not blocked(out) and rc == 0)

# E3: plain informative prose: passes
out, rc = run("The corpus pull finished. Three files changed and the page map "
              "regenerated. The counts match the manifest.")
check("E3 plain prose -> pass", not blocked(out) and rc == 0)

# E4: conditional-queue tail: CHECK 4 blocks
out, rc = run("Recommendation: land the fix now. I will draft the follow-up spec "
              "next unless you redirect.")
check("E4 conditional-queue tail -> CHECK 4 block", blocked(out) and "CHECK 4" in out)

# E5: standby framing: CHECK 5 blocks
out, rc = run("The build is green and the artifact is staged. Standing by for "
              "your ruling on the last item.")
check("E5 standby framing -> CHECK 5 block", blocked(out) and "CHECK 5" in out)

# ---------------------------------------------------------------- T: decision-table layer (CHECK 8)

A38_ROW = ("| A38 | Dual governance: which registry is authoritative for the dual-bound pages? "
           "| **No recommendation BY RULE (D-N154 bucket three): two reasoned readings, side by side.** "
           "Reading 1: the corpus page map is authoritative and local edits re-land in corpus sources "
           "before any regen. Reading 2: the local generators are authoritative and hold the later "
           "content. Until ruled, no regeneration runs (charter tripwire) | opened 2026-08-12 (slice 1) |")

A39_ROW = ("| A39 | Links page authored by another party: touch or leave? "
           "| **No recommendation BY RULE (D-N154 bucket three).** Reading 1: another party authored it, "
           "leave it and review separately. Reading 2: it is corpus-bound and missing a row, so leaving "
           "it means the corpus asserts a stale page. Both in the triage file | opened 2026-08-12 (slice 1) |")

BARE_ROW = ("| A40 | Who decides the registry of record for the dual-bound pages? "
            "| open question, two registries in play | opened 2026-08-12 |")

REC_ROW = ("| A41 | Which site hosts the first wave: Premium or Standard? "
           "| **Recommend: Premium.** It is the site the space already lives on, unless you prefer "
           "Standard because of licensing | open |")

# T1: bucket-three row modeled on A38 -> pass
out, rc = run("Slice 2 findings are below.\n\n" + TABLE_HEAD + A38_ROW + "\n")
check("T1 A38-modeled bucket-three row -> pass", not blocked(out) and rc == 0)

# T2: bucket-three row modeled on A39 (question-mark via 'touch or leave?') -> pass
out, rc = run("One page remains in triage.\n\n" + TABLE_HEAD + A39_ROW + "\n")
check("T2 A39-modeled bucket-three row -> pass", not blocked(out) and rc == 0)

# T3: bare who-decides row with neither form -> CHECK 8 block naming the row and both forms
out, rc = run("Slice 2 findings are below. One governance row is still open.\n\n"
              + TABLE_HEAD + BARE_ROW + "\n")
check("T3 bare who-decides row -> CHECK 8 block", blocked(out) and "CHECK 8" in out and rc == 0)
check("T3 reason names the failing row", "A40" in out)
check("T3 reason names the recommendation form", "Recommend" in out)
check("T3 reason names the bucket-three form",
      "No recommendation BY RULE" in out and "D-N154" in out)
def _valid_block_json(text):
    try:
        return json.loads(text).get("decision") == "block"
    except Exception:
        return False


check("T3 block JSON is valid", _valid_block_json(out))
check("T3 audit log records CHECK8-CAUGHT", any("CHECK8-CAUGHT" in l for l in audit_lines()))

# T4: decision row carrying a recommendation marker -> pass
out, rc = run("The wave 1 target is settled below.\n\n" + TABLE_HEAD + REC_ROW + "\n")
check("T4 recommendation-marker row -> pass", not blocked(out) and rc == 0)

# T5: closed rows only (strikethrough plus closure word with date) -> pass
out, rc = run("Closures from this morning:\n\n" + TABLE_HEAD
              + "| A38 | ~~Dual governance of the dual-bound pages~~ | **RULED 2026-08-12, landed as a register row: "
                "sequence, not either-or.** One-time pull of live edits into the corpus | closed 2026-08-12 |\n"
              + "| A39 | ~~Links page: touch or leave?~~ | **RULED 2026-08-12: absorb and take over.** "
                "The page joins the corpus | closed 2026-08-12 |\n")
check("T5 closed rows -> pass", not blocked(out) and rc == 0)

# T6: row quoting an old ratified decision -> pass (closure word with date in the same cell)
out, rc = run("For context, the governing row reads:\n\n"
              + "| Id | Decision | Stamp | Where |\n|---|---|---|---|\n"
              + "| D-N154 | Canon over recency: which register wins on conflict? "
                "| ratified 2026-08-12 (adoptive) | the register |\n")
check("T6 quoted ratified decision -> pass", not blocked(out) and rc == 0)

# T7: "No recommendation" WITHOUT the BY RULE form -> block (negation does not count as a marker)
out, rc = run("Open governance items:\n\n" + TABLE_HEAD
              + "| A42 | Which registry is authoritative for the split pages? "
                "| No recommendation yet, two readings in play | open |\n")
check("T7 bare 'no recommendation yet' -> CHECK 8 block", blocked(out) and "CHECK 8" in out)

# T8: bucket-three phrase without a D-N154 citation -> block (citation is required)
out, rc = run("Open governance items:\n\n" + TABLE_HEAD
              + "| A43 | Which registry is authoritative for the split pages? "
                "| No recommendation BY RULE, two readings side by side | open |\n")
check("T8 by-rule phrase without citation -> CHECK 8 block", blocked(out) and "CHECK 8" in out)

# T9: informational FAQ table (question marks, no decision stems) -> pass
out, rc = run("Quick glossary:\n\n"
              + "| Question | Answer |\n|---|---|\n"
              + "| What does OCM mean? | Organizational Change Management |\n"
              + "| Where does the digest land? | In the daily folder |\n")
check("T9 informational FAQ table -> pass", not blocked(out) and rc == 0)

# T10: two bare decision rows -> block names the first and counts the rest
out, rc = run("Open items:\n\n" + TABLE_HEAD
              + BARE_ROW + "\n"
              + "| A44 | Keep or drop the staging mirror? | needs a ruling | open |\n")
check("T10 multi-offender block names first row", blocked(out) and "A40" in out)
check("T10 multi-offender block counts the rest", "1 more row" in out)

# T11: mixed table (closed + bucket-three + recommended) -> pass
out, rc = run("Board state:\n\n" + TABLE_HEAD
              + "| A38 | ~~Dual governance~~ | RULED 2026-08-12, landed | closed 2026-08-12 |\n"
              + A39_ROW + "\n"
              + REC_ROW + "\n")
check("T11 mixed compliant table -> pass", not blocked(out) and rc == 0)

# T12: verb-only ask (no question mark): "needs a ruling" -> block
out, rc = run("Remaining state:\n\n" + TABLE_HEAD
              + "| R1 | Registry of record | needs a ruling before any regen | open |\n")
check("T12 needs-a-ruling row -> CHECK 8 block", blocked(out) and "CHECK 8" in out)

# T13: prose CHECK still wins first on a response that trips both layers
out, rc = run("Open items:\n\n" + TABLE_HEAD + BARE_ROW + "\n\n"
              "Want me to close it out, or leave the row for the next session?")
check("T13 prose CHECK 1 fires before CHECK 8", blocked(out) and "CHECK 1" in out and "CHECK 8" not in out)

# T14: table-looking rows inside a fenced code block -> pass (fences stripped)
out, rc = run("Here is the raw script output:\n\n"
              "```\n| A99 | Who decides the fallback path? | open |\n```\n\n"
              "The scan completed with no findings.")
check("T14 fenced pseudo-table -> pass", not blocked(out) and rc == 0)

# T15: bucket-three form present but split across ROWS (phrase in one, citation in another) -> block
out, rc = run("Open items:\n\n" + TABLE_HEAD
              + "| A45 | Which generator wins for the shared pages? | No recommendation BY RULE, see next row | open |\n"
              + "| A46 | Context | The D-N154 method governs the reconciliation, decided path pending | open |\n")
check("T15 phrase and citation in different rows -> CHECK 8 block", blocked(out) and "CHECK 8" in out)

failures = [n for n, c in results if not c]
print("\n%d/%d passed" % (len(results) - len(failures), len(results)))
sys.exit(1 if failures else 0)
