---
id: SIG-RECORDER-HOOK-MEASURES-WITNESS-2026-09-25
title: "The WS-DDR-098 recorder hook now measures Witness events and tells the model; 18 of the 22 products it watches have sent Witness nothing in 30 days"
type: signal
kind: gap
status: symptom-repaired, upstream-pending
severity: high
confidence: high
created: 2026-09-25
discovered_by: "queue task QMT-01M3D8KVWP66F2SH5X0TAV4E0B, a Claude session on Aurelius (hub), building upstream item 4 of the Workspaces signal SIG-WITNESS-COVERAGE-GAP-AND-DEAD-RECORDER-HOOK-2026-09-25"
scope: WS-DDR-098 recorder check; Witness coverage of the products that declare autonomy settings
affects:
  - /Users/brien/Workspaces/Core/frameworks/intent/hooks/signal-recorder-silent-check.sh
  - /Users/brien/Workspaces/Core/frameworks/intent/hooks/witness_source_index.py
  - /Users/brien/Workspaces/Core/frameworks/intent/ARCHITECTURE.md
related:
  - /Users/brien/Workspaces/.intent/signals/SIG-WITNESS-COVERAGE-GAP-AND-DEAD-RECORDER-HOOK-2026-09-25.md
  - /Users/brien/Workspaces/.context/DECISIONS.md
upstream_control_path: "Detection is controlled: /Users/brien/Workspaces/Core/frameworks/intent/hooks/signal-recorder-silent-check.sh reads a daily Witness index built by hooks/witness_source_index.py and puts a once-per-session note in the model's context (hookSpecificOutput.additionalContext). Emission is NOT controlled: 18 declaring products still send Witness no events, no written rule yet requires every build to emit (the draft WS-DDR in Workspaces commit 9785b726 is the candidate), the hook is registered on Write|Edit only so Bash-driven changes are unchecked, and Faustina and Legatus have no Witness store, so there the check records witness-index-missing and says nothing."
catch_mechanism: "hooks/tests/test_signal_recorder_silent_check.py (20 cases: the 7 original, plus Witness-index verdicts, declared names, dedupe, missing and malformed index, detached rebuild, latency) and hooks/tests/test_witness_source_index.py (11 cases). The prior hook fails 15 of the 20. Every hook call writes a telemetry row whose detection field says which branch ran, so a hook that stops evaluating shows up as a run of no-context or witness-index-missing rows. /usr/bin/python3 hooks/witness_source_index.py --report prints the silent list on demand."
verification_command: "cd /Users/brien/Workspaces/Core/frameworks/intent && /usr/bin/python3 hooks/tests/test_signal_recorder_silent_check.py && /usr/bin/python3 hooks/tests/test_witness_source_index.py && /usr/bin/python3 hooks/witness_source_index.py --report"
---

# The recorder check now looks at Witness, and most watched products are silent

## What changed

Brien's rule is that anything we build reports what it does through Witness. WS-DDR-098 ships one hook to watch that, for products whose `.intent/INTENT.md` declares `lambda_settings:` or `autonomy_grants:`. Until today the hook asked a different question: had the product written a signal markdown file in 30 days? It also warned on stderr, which Claude Code sends to its debug log, so neither the model nor Brien ever saw a warning.

Now the hook asks Witness. A small index, rebuilt at most once a day from the Witness events store, lists every product Witness has heard from, when it last did, and how often in the last 30 days. A product that declares autonomy settings and has no Witness event in 30 days is silent, and the model is told once per session, in its own context, before the edit runs. The edit is never blocked.

## What the new measure shows (index built 2026-09-26T01:16:32Z)

18 of the 22 declaring products are silent. The old measure passed 16 of them; 12 of those 16 are silent by the Witness measure.

| product | names checked | last Witness event | 30-day count | old signal-file measure |
|---|---|---|---|---|
| cast | cast | never | 0 | passed |
| conduit | conduit | 2026-06-05T19:26:01Z | 0 | flagged |
| cortege | cortege | 2026-07-22T16:34:14Z | 0 | passed |
| digital-declutter | digital-declutter | never | 0 | flagged |
| forge | forge | never | 0 | passed |
| intent-site | intent-site | never | 0 | flagged |
| investment | investment | never | 0 | passed |
| library-index-mcp | library-index-mcp | 2026-05-13T20:00:00Z | 0 | flagged |
| measurement | measurement | never | 0 | passed |
| methodology-library | methodology-library | never | 0 | flagged |
| operating-model | operating-model | never | 0 | passed |
| org-design-tooling | org-design-tooling | never | 0 | passed |
| parallax | parallax | never | 0 | passed |
| patterns | patterns | never | 0 | passed |
| product-academy | product-academy | never | 0 | passed |
| reference-substrate | reference-substrate | never | 0 | flagged |
| studio-control | studio-control | never | 0 | passed |
| transformation | transformation | never | 0 | passed |

Active: fieldbook (last 2026-09-13, 1,939 events, all from one drain, so it goes silent on 2026-10-13 unless it emits again), intent (2026-09-24, 6), library-index (2026-09-25, 86), witness (2026-09-26, 142,671).

## Still upstream

1. **The 18 products do not emit.** The hook names the gap each time someone edits one of them; it cannot make them emit. The cheapest path for most is appending event lines to the product's own `.intent/events/events.jsonl`, which Witness ingests daily at 06:00 under the directory name.
2. **The rule is not written.** The draft WS-DDR in Workspaces commit 9785b726 ("everything we build reports its actions to Witness") is the candidate control.
3. **Write and Edit only.** `~/.claude/settings.json` registers the hook on `Write|Edit`; the hook's Bash branch never runs. Adding Bash would catch scripted changes, at about 33 ms per Bash call.
4. **Other machines.** The Witness store lives on Aurelius (hub). On Faustina (traveler) and Legatus (client ambassador) the builder finds no store, writes no index, and the hook records `witness-index-missing` without a note.
5. **Doc count.** README.md still says "8 governance hooks"; ARCHITECTURE.md no longer carries a count.

## By the record

- Queue task: QMT-01M3D8KVWP66F2SH5X0TAV4E0B.
- Channel evidence: code.claude.com/docs/en/hooks, PreToolUse decision control (additionalContext is "added to Claude's context before the tool call executes"; exit 0 stderr goes to the debug log only), and a headless probe on Claude Code 2.1.282 with `--setting-sources project`, in which the model reported the additionalContext token and neither the stderr token nor the systemMessage token.
- Identity field: `event.product`, else `source_system`. `source_system` is the ingest channel (`intent` carries every product's `.intent/events`), so matching it would make the Intent framework look active on everyone's behalf.
- Latency on Aurelius, median of 21 runs: new hook 33.3 ms (silent product), 32.4 ms (active), 30.3 ms (no context); prior hook 71.5, 67.3 and 50.5 ms.
- First full build: 1,350,552,759 bytes, 2,253,207 events, 23.9 s. An incremental run with nothing new: 0.03 s.
