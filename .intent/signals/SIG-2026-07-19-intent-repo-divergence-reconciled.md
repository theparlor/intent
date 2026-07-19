---
id: SIG-2026-07-19-intent-repo-divergence-reconciled
type: signal
status: captured
severity: high
created: 2026-07-19
target: "Repo-level divergence: main vs origin/main forked at b439d27 (2026-07-02 07:42) and grew to 26 local-only vs 24 remote-only commits with no detection for 17 days"
discovered_during: "2026-07-19 reconciliation session (Brien-directed after the 2026-07-18 session hit the push rejection and parked the work)"
requested_by: brien
---

# Intent repo divergence, 26 local vs 24 remote, reconciled by merge

## What happened

The last local fetch-and-integrate before today was at b439d27 (2026-07-02 07:42).
Later that same day the remote advanced 24 commits (PR merges 6 through 10 by
theparlor, intent-bot event emissions, cloud Claude sessions). From 2026-07-03
through 2026-07-18, local sessions committed 24 more commits (then 2 landing
commits at reconciliation), never fetching, so every local commit was born
unpushable. Nothing surfaced this: the pre-push hook is Entire session-log sync
(fail-open), no sweep checks ahead/behind, and sessions end without a push
attempt in most cases.

## Concrete costs found at reconciliation

1. Both lines minted a DDR-009 (remote: externally-authored-verification, 2026-07-02,
   pushed; local: always-on-hosting-substrate, 2026-07-03, ratified by Brien).
   Local renumbered to DDR-010 at merge. The March signal
   2026-03-30-id-collision-distributed.md predicted exactly this class.
2. The 2026-07-08 local triage-drain audited a stale world: it wrote "confirmed
   neither control has been built" into SIG-2026-06-27 (both controls had been
   built remote-side on 2026-07-02), and equivalent stale findings into
   SIG-2026-06-09 and SIG-2026-06-05. All three triage notes are preserved in
   place with reconciliation annotations.
3. Both sides appended different test classes to tools/test_closure_writeboundary_check.py
   and different arms to the checker itself (local: precision exemptions;
   remote: Control B downstream-fix arm). These composed cleanly at merge; both
   test classes pass against the composed checker.

## Resolution

Single merge commit (no rebase, no history rewrite), 7 textual conflicts
resolved semantically, 3 auto-merged files given reconciliation annotations,
1 status adjudication (three-dimensions: per-file audit evidence beat the batch
incorporated classification). Full analysis:
Core/products/_intake/2026-07-19-intent-repo-reconciliation/analysis.md

## Upstream control (what makes regrowth detectable)

A divergence detector is being added to the governance sweep fabric in this
same session: every nested repo under Core/products/ and Core/frameworks/ plus
the Workspaces root reports ahead/behind vs its remote; stale-ahead (ahead
greater than 0 with last local commit older than 24 hours) or behind greater
than 20 emits a signal file to Workspaces/.intent/signals/, one per repo per
day, idempotent. This signal flips to resolved when that detector is live and
red-green tested.
