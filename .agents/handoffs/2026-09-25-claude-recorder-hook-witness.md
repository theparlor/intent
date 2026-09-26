# Agent handoff: recorder-hook-witness

- Status: complete
- Provider/agent: claude
- Objective: the WS-DDR-098 recorder hook measures Witness events instead of signal-file recency, and its warning reaches the model (queue task QMT-01M3D8KVWP66F2SH5X0TAV4E0B)
- Worktree and branch: `../intent-wt-2026-09-25-recorder-hook-witness`, `agent/claude/2026-09-25-recorder-hook-witness`
- Base and head commits: base `ecb2e60`; head recorded at merge.
- Owned paths: `hooks/signal-recorder-silent-check.sh`, `hooks/tests/test_signal_recorder_silent_check.py`, `hooks/witness_source_index.py`, `hooks/tests/test_witness_source_index.py`, `ARCHITECTURE.md`, `.intent/signals/SIG-RECORDER-HOOK-MEASURES-WITNESS-2026-09-25.md`
- Changed paths: the six owned paths above, plus this handoff and the task file
- Canonical inputs: the Witness events store (Core/products/witness/farm/events-store/*.jsonl, read only); the Witness intent-events adapter's naming rule (src/ingest_streams.py, read only)
- Generated outputs: `$HOME/.claude/state/witness-source-index.json` and its `.state` file, outside git
- External reads: code.claude.com/docs/en/hooks (PreToolUse decision control)
- External writes: none
- Checks and results: hooks/tests/test_signal_recorder_silent_check.py 20 passed (the prior hook fails 15 of them); hooks/tests/test_witness_source_index.py 11 passed; test_no_hardcoded_home 1 passed; hook median 33 ms against 71 ms before
- Decisions made: product identity is event.product, else source_system (source_system "intent" carries every product's events); the hook is Python under its .sh name, like cross-engagement-write-guard.sh; a missing or malformed index records a detection and shows nothing
- Unresolved risks or decisions: 18 of 22 declaring products emit nothing to Witness; the hook runs on Write|Edit only; Faustina and Legatus have no store. All in the signal.
- Safest next action: the draft WS-DDR "everything we build reports its actions to Witness", then per-product emission starting with the products edited most often
