# Agent handoff: cross-engagement-write-guard

- Status: complete
- Provider/agent: claude
- Objective: PreToolUse guard: warn on cross-engagement repo writes, block other engagements' names in engagement project memory (SIG-0026)
- Worktree and branch: `../intent-wt-2026-09-24-cross-engagement-write-guard`, `agent/claude/2026-09-24-cross-engagement-write-guard`
- Base and head commits: base `4179813`; head recorded at merge.
- Owned paths: `hooks/cross-engagement-write-guard.sh`, `hooks/tests/test_cross_engagement_write_guard.py` (hooks/install.sh dropped from the claim: the primary checkout carries another session's uncommitted edit to it, and touching it here would stop the primary from fast-forwarding; the neighbouring nested-repo guards are registered by hand too)
- Changed paths: `hooks/cross-engagement-write-guard.sh` (new), `hooks/tests/test_cross_engagement_write_guard.py` (new)
- Canonical inputs: every `Work/{Consulting,Advising}/Engagements/<Name>/glossary.md`, the central glossary `memory/glossary.md`, `/usr/share/dict/words`, git user.name. Read at call time, only on a write into an engagement project memory.
- Generated outputs: none tracked. Runtime state `~/.claude/state/cross-engagement-write-guard-warned.json`, log `~/.claude/logs/cross-engagement-write-guard.log` (counts and engagement names only, never the flagged terms).
- External reads: the Subaru and JohnsonControls project memories, read-only, for the real replay in `--selftest`.
- External writes: none
- Checks and results: `python3 hooks/cross-engagement-write-guard.sh --selftest` 53/53, including the real 2026-09-24 replay (blocked on 3 weak Subaru names) and the three repaired JCI memories (0 hits each); pytest on the new test and test_no_hardcoded_home.py, 3 passed; calibration over all 36 existing engagement memory files: 0 would block, 0 advisories.
- Decisions made: rule 2's reference is the memory dir's engagement, not the session's, so filing a lesson into the right engagement's memory from a wrong-folder session (the repair) is allowed; strong/weak term tiers (one weak hit advises, two block); vocabulary sections of glossaries are skipped to keep methodology terms from blocking.
- Unresolved risks or decisions: the guard only sees people and products listed in People or org/team/product sections. JohnsonControls keeps its people inside vocabulary sections, so JCI names leaking into another engagement's memory are not yet caught; a People section in that glossary closes it. Governance record: WS-DDR in the Workspaces root, landed with this.
- Safest next action: after landing, fast-forward the primary checkout, symlink into ~/.claude/hooks, register under the Write|Edit|NotebookEdit|MultiEdit and Bash PreToolUse entries.
