---
id: SIG-RECORDER-FIELD-LINT-2026-09-26
title: "The recorder check now lints Witness events for the WS-DDR-150 minimum fields; the busiest producers miss them on every event, and four gaps stay upstream"
type: signal
kind: gap
status: symptom-repaired, upstream-pending
severity: medium
confidence: high
created: 2026-09-26
discovered_by: "queue task QMT-01M3F5JWBR8XPK9YGB7HTMCBNP, a Claude session on Aurelius (hub), enforcement item 7 of WS-DDR-150"
scope: WS-DDR-150 minimum event; the recorder check (hooks/signal-recorder-silent-check.sh and hooks/witness_source_index.py)
affects:
  - Core/frameworks/intent/hooks/signal-recorder-silent-check.sh
  - Core/frameworks/intent/hooks/witness_source_index.py
  - Core/products/witness/src/emit.py
  - Core/products/witness/src/ingest_streams.py
related:
  - .context/DECISIONS.md (WS-DDR-150)
  - .intent/plans/DECISION-SURFACE-WITNESS-EMIT-RULE-2026-09-25.md
  - Core/frameworks/intent/.intent/signals/SIG-RECORDER-HOOK-MEASURES-WITNESS-2026-09-25.md
upstream_control_path: "Detection is controlled: Core/frameworks/intent/hooks/witness_source_index.py lints every Witness event against the WS-DDR-150 minimum and keeps per-product counts; hooks/signal-recorder-silent-check.sh tells a session once when an active product's rule-bound events mostly miss a field. Four things stay upstream. (1) Core/products/witness/src/emit.py makes duration_ms optional although the rule requires it, so a caller that omits it emits a nonconformant event (the WS-DDR-150 ratification event did). (2) The hook speaks only to products whose INTENT.md declares lambda_settings or autonomy_grants (the WS-DDR-098 gate, hooks/signal-recorder-silent-check.sh step 3), so quartermaster (18 of 18 events missing fields), speech-suite (139 of 139) and witness-self never reach a session although WS-DDR-150 covers everything that acts. (3) Events a Witness stream adapter carries (Core/products/witness/src/ingest_streams.py) are classed legacy and never linted, so a product that reports only through its .intent/events file escapes the lint. (4) The producers themselves: Witness's own linker (175,527 events in 30 days, every one missing caller, machine, outcome, duration_ms and run_id) and Fieldbook's spans (1,939, missing caller and machine) are backfill items under WS-DDR-150 decision point 7."
catch_mechanism: "hooks/tests/test_witness_source_index.py (23 cases, 10 new: the lint of one event, plain and OTLP, timezone and engagement rules, legacy versus rule-bound, agreement with emit.py, per-product counts in the window, incremental lint, the one full re-read of an old state, the conformance table, the builder's own job.run event, emit failure) and hooks/tests/test_signal_recorder_silent_check.py (31 cases, 9 new: the field note, quiet paths, merging across names, the silent note's emit.py pointer, the hook.fire event every fire emits, emit failure, a remedy that fits what is missing). /usr/bin/python3 hooks/witness_source_index.py --report prints the conformance table, rule-bound and legacy apart, and which products a session would be told about. Every hook fire and every build emits a Witness event (intent hook.fire, intent job.run), so a check that stops running shows up as those events stopping."
verification_command: "cd ~/Workspaces/Core/frameworks/intent && /usr/bin/python3 hooks/tests/test_witness_source_index.py && /usr/bin/python3 hooks/tests/test_signal_recorder_silent_check.py && /usr/bin/python3 hooks/witness_source_index.py --report | sed -n '/Field conformance/,$p'"
---

# The recorder check now reads what each event says, not only that it arrived

## What changed

WS-DDR-150, ratified by Brien on 2026-09-26, says every event carries a minimum set of fields: when (with timezone), which product, what action, who asked, which machine, the result, how long it took, and a run id. Until today the recorder check only asked whether a product had sent Witness anything in 30 days. Now, while it builds its daily index, it also checks each event for those fields and keeps, per product, how many events it saw, how many miss a field, and which field is missing most often.

When someone edits a product that is reporting, but most of whose events miss a field, the model is told once per session in one sentence, for example: "Most of witness's events in Witness over the last 30 days (175527 of 175527) lack fields the rule requires, most often duration_ms, so have witness report through Core/products/witness/src/emit.py, which supplies every required field when given duration_ms." The edit is never blocked.

Older sources that predate the rule are counted but never nag. Screen capture (screenpipe), Claude transcripts (cc-native), Entire traces (entire-io), and anything Witness's stream adapters translate from an older log (every such event carries an `adapter` attribute) are shown in the report as legacy.

The check and its index builder now report their own runs to Witness through emit.py, so they follow the rule they enforce.

## What it shows (index built 2026-09-26T15:59:06Z)

| Witness name | rule-bound events, 30 days | missing a field | most often missing | a session is told |
|---|---|---|---|---|
| witness | 175,527 | 100% | duration_ms (caller on all but one) | yes |
| fieldbook | 1,939 | 100% | caller | yes |
| speech-suite | 139 | 100% | caller | no, does not declare autonomy settings |
| quartermaster | 18 | 100% | caller | no, does not declare autonomy settings |
| conduit | 6 | 33% | caller | no, mostly conformant |
| digital-declutter, parallax, library-index-mcp, lodestone, model-call, reference-substrate | 1 to 3 each | 0% | none | no |

Legacy, last 30 days: screenpipe 895,289, cc-native 314,383, entire-io 145,625, loom 9,213, signalbox 6,749, workspaces 3,254 and smaller; all miss the fields except jev (22 adapter-carried events, all conformant).

## What is left, and why it is not fixed here

1. **emit.py leaves duration_ms to the caller.** The rule requires it; emit.py accepts an event without it. The one Witness event written at ratification lacks it. The fix belongs in Witness (a default, or a warning), not in this check.
2. **The hook only speaks to products that declare autonomy settings.** That gate is WS-DDR-098's. WS-DDR-150 covers everything that acts, so Quartermaster and the speech suite, which miss the fields on every event, never produce a note. Widening the gate is a governance change, not a hook fix.
3. **Adapter-carried events are never linted.** This keeps the old logs quiet, as intended. But a product that reports only by appending to its `.intent/events` file also arrives through an adapter and is never linted. Both notes now point at emit.py, and the jev events show that an adapter carries the fields through when the source line has them.
4. **The producers.** Witness's linker and Fieldbook's spans are the bulk of the nonconformant events. They come up to the rule under WS-DDR-150's backfill list, or when next touched; the check now tells whoever touches them.

## By the record

- Landed: intent commit 8669665 (squash of the session branch agent/claude/2026-09-26-recorder-field-lint), on top of a7e1121 (the no-actions declaration, same four files, kept whole).
- Tests on the primary after landing: test_witness_source_index.py 23 passed; test_signal_recorder_silent_check.py 31 passed; both under pytest, 54 passed.
- Hook latency, median of 21 runs through ~/.claude/hooks with a copy of the real index and the emit on: 44.6 ms (field note), 43.4 ms (active, legacy only), 44.3 ms (silent), 42.2 ms (no context). Budget 100 ms.
- First build after the upgrade: full re-read, 1,407,717,584 bytes, 2,347,748 events, 31.3 s; later builds stay incremental.
- Witness events from the real runs, in Core/products/witness/farm/events-store/2026-09-26.jsonl: intent job.run run_id d90f94c68a3d4b0588ba0a8aa427e343 and intent hook.fire session qmt-01m3f5jwbr8x-verify.
