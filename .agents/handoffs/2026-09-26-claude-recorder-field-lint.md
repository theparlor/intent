# Agent handoff: 2026-09-26-recorder-field-lint

- Status: complete
- Provider/agent: claude
- Objective: QMT-01M3F5JWBR8XPK9YGB7HTMCBNP: WS-DDR-150 field lint in the recorder check
- Worktree and branch: `../intent-wt-2026-09-26-recorder-field-lint`, `agent/claude/2026-09-26-recorder-field-lint`
- Base and head commits: base `fc674d8`, rebased onto `a7e1121` (the no-actions declaration, same four files, kept whole); head recorded at merge.
- Owned paths: `hooks/witness_source_index.py`, `hooks/signal-recorder-silent-check.sh`, `hooks/tests/test_witness_source_index.py`, `hooks/tests/test_signal_recorder_silent_check.py`, `ARCHITECTURE.md` (added: its recorder-check section described the old behavior)
- Changed paths: the five owned paths.
- Canonical inputs: `.context/DECISIONS.md` WS-DDR-150; `.intent/plans/DECISION-SURFACE-WITNESS-EMIT-RULE-2026-09-25.md` ("The minimum event, exactly"); `Core/products/witness/src/emit.py`; `Core/products/witness/src/ingest_streams.py` (which adapters stamp `attributes.adapter`).
- Generated outputs: `$HOME/.claude/state/witness-source-index.json` gains `lint` and per-product `lint_30d` (outside git).
- External reads: the Witness events store, read-only.
- External writes: none to git outside this repo; the builder and hook append events to the Witness inbox through emit.py.
- Checks and results: `/usr/bin/python3 hooks/tests/test_witness_source_index.py` 23 passed; `/usr/bin/python3 hooks/tests/test_signal_recorder_silent_check.py` 31 passed; both under pytest, 54 passed; hook latency median 49.6 ms over 21 runs with the emit on; `.agents/bin/portability-check` ok; dry run of the builder on the real store: 1.41 GB, 2,347,723 events, 33.18 s.
- Decisions made: legacy versus rule-bound is read from each event (source_system screenpipe, cc-native or entire-io, or `attributes.adapter` set), no product list; the note fires when more than half of an active product's rule-bound events miss a field; OTLP spans count traceId, start and end times and status.code as run_id, duration_ms and outcome; the remedy in the note depends on whether emit.py-supplied fields are missing; the bypass stays inert (no event).
- Unresolved risks or decisions: emit.py makes `duration_ms` optional although the rule requires it, so an emit.py caller that omits it is linted nonconformant; adapter-carried events are never linted, so a product reporting only through `.intent/events` escapes the lint.
- Safest next action: after landing, `witness_source_index.py --force` once (full re-read, about half a minute), then `--report`.
