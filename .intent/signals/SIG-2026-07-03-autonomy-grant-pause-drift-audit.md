---
id: SIG-2026-07-03-autonomy-grant-pause-drift-audit
created: 2026-07-03
type: road-readiness-audit
status: captured
severity: medium
confidence: 0.85
trust: 0.7
review_class: cross-system-root-cause-audit
road_ready_gate: true
decision_owner: Brien (L2 — Layer 4.2 promote/retire/ratify remains his call, unchanged by this audit)
parent_signal: SIG-2026-06-28-flight-model-30day-ratification-readiness
related:
  - Core/frameworks/intent/spec/2026-07-03-autonomy-grant-pause-drift-audit.md
  - Core/frameworks/intent/hooks/autonomy-posture-check-layer-4.2.sh
  - Core/frameworks/intent/hooks/autonomy-grant-stop-check.sh
  - Core/frameworks/intent/hooks/lexical-layer-freeze.yaml
  - Core/frameworks/intent/spec/autonomy-flight-model-ratification-tracker.md
  - .intent/signals/SIG-2026-06-12-layer42-calibration-review.md
  - .intent/signals/SIG-2026-06-28-flight-model-30day-ratification-readiness.md
---

# Root-cause audit: chronic autonomy-grant pause-drift, and a correction to two prior signals

## What happened

Brien commissioned a full audit of the Intent autonomy-grant/closure-discipline hook fabric after
hitting live pause-drift with no fresh signal on disk for the incident. A 15-agent workflow (5 parallel
research tracks, adversarially-verified root-cause diagnosis, 3 candidate redesigns each stress-tested
against Claude Code's real hook constraints) produced `Core/frameworks/intent/spec/2026-07-03-autonomy-grant-pause-drift-audit.md`.

## Headline findings

1. **The enforcement fabric is architecturally reactive-only.** Claude Code hooks fire on five discrete
   events (SessionStart/PreToolUse/PostToolUse/Stop/SessionEnd); none intercept mid-generation prose.
   The Stop hook can only catch a hedge after the full response is written and force a rewrite. This is
   a platform ceiling, not a design defect in this system specifically.
2. **The lexical regex layer cannot converge.** `autonomy-grant-stop-check.sh` grew CHECK 1→7 between
   2026-04-28 and 2026-05-29, each patching the prior CHECK's bypass; formally frozen 2026-05-29 per
   `lexical-layer-freeze.yaml` as unconvergeable. Still catching new phrasing as of 2026-07-02.
3. **Correction to this audit's own workflow: the 06-12 and 06-28 Layer 4.2 calibration signals DO
   exist on disk** (untracked/uncommitted in this repo's git working tree, which is why the workflow's
   file-existence check missed them). Both correctly gate the promote/retire/ratify decision as
   Brien's L2 call and both are still open — this is a pending decision, not neglected work.
4. **A real gap in those two existing signals, found on direct re-read, not a new test:** the 06-28
   signal's own false-positive table lists `team-configs` among fires attributed to the
   stop-word/pronoun extractor bug, but `team-configs` is a genuine compound noun, not a stop-word. The
   recommended one-line patch, as specified in both prior signals, will not suppress that fire. The
   patch needs one more pass before the promote decision it's gating is actually trustworthy.
5. **Two of three candidate redesigns generated during this audit contained falsified claims** on
   adversarial verification (a nonexistent `entire status --json` flag; a tool-name-substring
   classifier that silently misclassifies `create_draft` as local-only; Stop-array arithmetic that
   omits 4 of 9 live hooks). None of the three ships as-is. Full detail in the audit doc.
6. **Parallax's governance-layer-vsm.md cites the Stop hook as "the strongest algedonic act"** without
   ever having pressure-tested that claim — this audit is the first adversarial test of the hook's
   reliability anywhere in the ecosystem, and it found real problems.

## Recommendation (surfaced, not executed — Brien's L2 call, same as the two prior signals)

Re-classify all current `would_block=1` fires in `autonomy-posture-layer42.jsonl` (9 as of this audit,
was 8 at the 06-28 signal), specifically checking for non-stop-word genuine-noun fires like
`team-configs` that the existing FP tables mis-bucketed, before treating the stop-word patch as ready
to promote-and-block on. Full phased plan (4 phases, 15 steps) in the audit doc §7.

## Why this is `status: captured`, not `resolved`

Per closure-discipline: no upstream control has shipped. Nothing was fixed. This signal documents an
audit finding and a correction to prior signals' completeness, and hands the same still-open L2
decision back to Brien with a corrected diagnosis. `catch_mechanism`: the audit doc's validation
criteria (§9) define what "actually promotable" looks like; no automated catch-net exists yet for
re-verifying FP-table completeness before a promote recommendation ships, which is itself a gap worth
a future signal if this pattern (a recommendation shipping with an uncaught classification gap)
recurs.
