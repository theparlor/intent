# Agent handoff: xeng-guard-name-precision

- Status: complete
- Provider/agent: claude
- Objective: keep the cross-engagement write guard precise as engagement glossaries grow (Brien, 2026-09-25: glossaries and lists of humans always grow), and give glossary changes a catch-net.
- Worktree and branch: `../intent-wt-2026-09-25-xeng-guard-name-precision`, `agent/claude/2026-09-25-xeng-guard-name-precision`
- Base and head commits: base recorded by the kit; head recorded at merge.
- Owned paths: `hooks/cross-engagement-write-guard.sh`
- Changed paths: `hooks/cross-engagement-write-guard.sh`
- Canonical inputs: the JCI glossary People widening (about 200 people, JohnsonControls repo, same day); WS-DDR-148; SIG-0026 in the JohnsonControls repo.
- Generated outputs: none
- External reads: none
- External writes: none
- Checks and results: `--selftest` 70/70 (was 54), including the real 2026-09-24 replay, which still blocks. Stress over every engagement's own markdown with the widened JCI glossary: would-block files fell from Subaru 10, FidelityGuaranty 15, OptumCareWellMed 15, Turnberry 37 (old rules) to 1, 2, 2, 17; Turnberry's remainder is mostly true JCI references in channel notes.
- Decisions made: (1) a first-name or surname term counts only as its own person: a capitalized word right after it, or a common given name or non-dictionary word before a surname, marks a different person; (2) first names corroborate and never convict alone: a block needs a strong hit or two weak hits with at least one that is not a first name; (3) `box` and `dropbox` join the public tool list; (4) new `--collisions [NAME]` mode as the catch-net for glossary changes.
- Unresolved risks or decisions: surname-alone stays strong, so a standalone citation of a common surname (an author, another engagement's person missing from its own glossary) still blocks; the remedy is that engagement's glossary growing. WS-DDR-148 amendment is recorded in the Workspaces root DECISIONS.md by the same session.
- Safest next action: run `python3 hooks/cross-engagement-write-guard.sh --collisions <Engagement>` before landing any glossary that adds people.
