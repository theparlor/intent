# Agent handoff: guard-citation-surnames

- Status: complete
- Provider/agent: claude
- Objective: Guard: author citations (Womack & Jones (1996), Jones (OpenClaw 2026)) no longer read as glossary people; fonts join PUBLIC
- Worktree and branch: `../intent-wt-2026-09-25-guard-citation-surnames`, `agent/claude/2026-09-25-guard-citation-surnames`
- Base and head commits: base `63baa8b`; head recorded at merge.
- Owned paths: `hooks/cross-engagement-write-guard.sh`
- Changed paths: `hooks/cross-engagement-write-guard.sh` (header rule text, `FONTS` joined into `PUBLIC`, `_HYPHEN_PREV` and the citation regexes, new `_other_author` and `_cited`, `_same_person` extended; 19 new selftest checks and one fixture person)
- Canonical inputs: every engagement `glossary.md`, read at run time; the OptumCareWellMed People table (that repo's commit 92cb43c) raised the collision
- Generated outputs: none
- External reads: none
- External writes: none
- Checks and results: `--selftest` 89/89 (was 70/70), the real 2026-09-24 replay still blocks; `hooks/tests/test_cross_engagement_write_guard.py` passes; each new rule was switched off in a scratch copy and its cases failed (citation 7, hyphen 3, fonts 2, partner guard 2). `--collisions OptumCareWellMed`: would-block JohnsonControls 1 to 0, Turnberry 3 to 0, all others 0. `--collisions` (every glossary): would-block 80 to 77, advisory 138 to 114 (totals corrected after landing: the first figures were a hand tally). The per-file diff against main removes exactly 4 "Jones" hits (3 author citations plus "Avery Worthing-Jones") and 26 "Montserrat" hits (all the Turnberry brand font), and adds none.
- Decisions made: citations and compound names are recognized in `_same_person` (surnames only, never after the person's own given name); a common-surname list was not added, because it would lower recall on every genuine standalone surname and the measured residual after the citation rule is zero; typeface names join `PUBLIC`, so a person who shares one keeps the full name and surname as terms. Recorded as the second 2026-09-25 amendment to WS-DDR-148 in `Workspaces/.context/DECISIONS.md`.
- Unresolved risks or decisions: a bare surname pair in prose ("pair with Womack and Jones") now reads as co-authors when the partner is not one of the same engagement's people; a year closing a parenthetical ("(owner: Jones, OpenClaw 2026)") reads as a citation. Both are narrow and documented in the header.
- Safest next action: none required. Rerun `--collisions <Name>` before landing any glossary that adds people.
