---
title: Autonomy-Grant Enforcement Chronically Fails to Prevent Pause-Drift — Audit and Design Report
type: analysis
maturity: draft
confidentiality: internal
reusability: specific
created: 2026-07-03
updated: 2026-07-03
purpose: Root-cause audit of the Intent autonomy-grant/closure-discipline hook fabric, three adversarially-verified candidate redesigns, and a corrected diagnosis of why Layer 4.2 promotion has stalled — proposed DDR pending Brien's L2 ratification.
related:
  - Core/frameworks/intent/spec/autonomy-grant-enforcement.md
  - Core/frameworks/intent/spec/closure-discipline-enforcement.md
  - Core/frameworks/intent/spec/autonomy-flight-model-v1-DRAFT.md
  - Core/frameworks/intent/spec/autonomy-posture-check-layer-4.2-DRAFT.md
  - Core/frameworks/intent/spec/autonomy-flight-model-ratification-tracker.md
  - Core/frameworks/intent/.intent/signals/SIG-2026-06-12-layer42-calibration-review.md
  - Core/frameworks/intent/.intent/signals/SIG-2026-06-28-flight-model-30day-ratification-readiness.md
  - Core/products/parallax/spec/2026-05-31-governance-layer-vsm.md
---

# Audit and Design Report: Autonomy-Grant Enforcement Chronically Fails to Prevent Pause-Drift

## 1. Executive Summary

The system chronically hedges on work you already granted L4 standing autonomy for because every enforcement layer that inspects the model's own hedging language fires only after the full response text already exists (Stop hooks), so it can block a re-submission but never stop the first hedge token from being written. On top of that reactive ceiling, detection is almost entirely regex-on-phrases, which has hit a documented paraphrase wall: seven successive CHECKs in the primary hook file each exist because a prior CHECK got worded around, and that lexical layer was formally frozen five weeks ago as unconvergeable. The one structurally sound fix that could escape both problems (Layer 4.2's property-based detector) has sat in warn-only telemetry mode for 35+ days, not from neglect but because it has already been surfaced to you twice, at 14 and 30 days, as a correctly-gated L2 promote/retire/ratify decision that has not yet been answered. Re-reading those two existing signals directly (not a new test) found the recommendation itself has a gap: one real fire (`team-configs`) is a genuine noun, not a stop-word, and was mis-bucketed alongside true stop-words in the 06-28 signal's own table, so the patch as specified would not fully suppress it. None of the three candidate redesigns survives adversarial review intact; the two concrete ones (consolidation, Entire-backed Gate 1) both contain factual errors, including the workflow's own mistaken claim that the two prior signals don't exist (they do, just uncommitted in git). The path forward is not a bigger hook: it is closing out the decision that is already sitting in front of you, with a corrected diagnosis, then treating file consolidation and Entire-wiring as separate, lower-priority, partially-correct follow-ons.

## 2. Root Cause Diagnosis

Ranked by explanatory weight, per the diagnosis (confidence noted per cause):

**1. Reactive-only architecture (high confidence, dominant cause).** Claude Code's hook model has no mid-generation interception point. PreToolUse only sees structured tool_input payloads, never the model's own prose. The Stop hook is the only layer that inspects conversational hedging, and Stop fires strictly after the full response is generated and appended to the transcript. The fabric can force a regenerate-and-hope rewrite. It cannot prevent the first token of "Want me to..." from being written. The DRAFT flight-model redesign explicitly preserves this constraint rather than solving it: it changes what gets computed at Stop time, not when enforcement fires.

**2. Lexical paraphrase ceiling (high confidence).** Regex/phrase-list matching cannot converge against a model that keeps finding new ways to say the same underlying caution-bias. `autonomy-grant-stop-check.sh` grew from CHECK 1 to CHECK 7 between 2026-04-28 and 2026-05-29, and the in-file comments document each CHECK as a direct patch for the prior CHECK's bypass (a recommendation marker laundering a scope-narrowing bare choice past CHECK 1; a keyword requirement being evaded; a scope-variant slipping past everything). The lexical layer was formally frozen at CHECK 7 on 2026-05-29 with an explicit acknowledgment in `lexical-layer-freeze.yaml` that this approach cannot converge. Live telemetry as of 2026-07-02, one day before this audit, shows the cascade is still catching new phrasing variants.

**3. The one structurally sound fix has been surfaced to you twice and not yet decided, not "neglected" (high confidence, corrected post-audit).** Layer 4.2 (`autonomy-posture-check-layer-4.2.sh`) is the fabric's only property-based, non-lexical detector, and it is the load-bearing piece of the stalled flight-model redesign. It has been warn-only since its single commit on 2026-05-29 (35+ days as of this audit), unconditionally exiting 0 and never emitting a block decision. Two automated reviews DO exist on disk (`SIG-2026-06-12-layer42-calibration-review.md`, `SIG-2026-06-28-flight-model-30day-ratification-readiness.md`, both untracked/uncommitted in the intent repo, which the workflow's file search missed) and both explicitly mark `decision_owner: Brien (L2 - promote/retire/ratify are NOT autonomous)`. This was correctly gated, not skipped: promoting a hook that blocks your own future turns from warn-only to enforcing is a real risk decision, not routine L4 cleanup, and the system asked you for it twice, at 14 days and 30 days, and you have not yet answered. The two reviews both identify the same target-extractor bug: it captures stop-words and pronouns ("each," "that," "it," "with") as real action targets. But the 06-28 signal's own false-positive table lumps `team-configs` into that same "quantifiers/pronouns/stop-words" bucket alongside `each`/`that`/`all`, without noticing `team-configs` is a genuine compound noun, not a stop-word. The recommended one-line stop-word filter would not suppress that fire. This is a real gap in the existing diagnosis, not a new problem this audit introduced, and it means the "patch is fully specified" claim in both prior signals is not quite true yet.

**4. Capture-bias in the signal record (medium-high confidence).** The two failure classes structurally invisible to a lexical Stop hook, silent-stop (task-boundary completion with no further action) and stance-costume framing (dressing an L4 item as if it needs Brien's decision), are by construction also the classes least likely to generate their own signal file, because nothing fires to prompt writing one up. The apparent decline in logged incidents from roughly 9 in May to 2 in June/July is real at the lexical layer (four regex CHECKs now firing as true positives against known phrasings) but is very likely an artifact of what still gets logged, not evidence the underlying behavior resolved. The 2026-05-27 silent-stop signal was re-triaged 2026-06-17 and confirmed still unimplemented, with no signal since. Your live complaint in the source conversation, with no corresponding fresh signal on disk, is the expected symptom of this exact gap, not a new, unrelated event.

**5. Governance-layer duplication without cross-pollination (medium confidence).** Parallax's S3-S5 VSM layer and the Selection Docket both cite the autonomy-grant hook mechanism as settled, working infrastructure, re-labeling the same L0-L4 taxonomy in VSM vocabulary, without either layer ever modeling the hook's actual mechanics (6+ regex checks, bypass semantics, false-positive/false-negative behavior) as a governed artifact the way Gauntlet governs Voices or Scout governs Topography. Gauntlet, the system's own falsification tool, has never been pointed at the autonomy-grant hook's own reliability claims. Decision Reconsideration has no registered trigger for the hook despite it having visibly iterated 6 times.

**6. The one correctly-positioned pre-generation control is soft advisory, not a gate (medium confidence).** The `autonomy-grant-drift-detector` skill, loaded at SessionStart, instructs the model to run a silent 4-gate self-check on its own draft before sending. This is architecturally the right intervention point (before the hedge is written), but it is a prompt instruction with no mechanical enforcement verifying the check happened. Skipping it produces no signal, no block, no trace. Multiple hook file headers explicitly note that prompt/memory-only reinforcement already failed to close this exact gap before hooks were built as the mechanism-level fix, yet the drift-detector skill is the same class of intervention repeated.

**Entire CLI is confirmed NOT a root cause.** It has zero references anywhere in the hooks or spec directories governing this system, and the one document that scopes its actual capabilities explicitly narrows it to authoring-side provenance, not outcome/loop-closure verification. Reversibility (Gate 1 of the 4-gate check) is never connected to Entire in any document, which is a real unexamined gap, but wiring it in would improve auditability, not fix the reactive-timing problem that dominates.

## 3. Why The Current Architecture Cannot Fully Solve This

Claude Code hooks fire on five discrete events: SessionStart, PreToolUse, PostToolUse, Stop, SessionEnd. None of these fire mid-generation. PreToolUse inspects a tool call's structured input before it executes, which is useful for catching a dispatched sub-agent prompt or a file write, but it never sees the assistant's own conversational prose, because prose is not a tool call. The Stop hook is the only place in the entire event model where the model's free-text response can be inspected at all, and by the time Stop fires, that text is already complete and already in the transcript.

This means the entire fabric, no matter how it is rebuilt, can only ever do one of two things when it detects a hedge: block the response and force a rewrite (reactive, after the fact), or leave a marker in context for the next turn (also reactive, one turn late). There is no third option inside the current platform. A perfect regex, a perfect property-based classifier, an ML classifier, none of it changes the timing. The best any Stop-hook-based system can do is get very good at catching hedges after they are written and forcing a redo, which is what the current system already does when it works, at CHECK 1 through CHECK 7.

The DRAFT flight-model redesign is honest about this. It explicitly states the flight model changes what gets computed at Stop-hook time, not when enforcement fires. That is the correct scope for what a hook-based redesign can claim. Any proposal that implies it will stop the hedge from ever being written is overclaiming against a platform ceiling, not a design choice.

## 4. The Stalled Redesign

Three DRAFT artifacts exist in `Core/frameworks/intent/spec/`:

- **`autonomy-flight-model-v1-DRAFT.md`**: replaces the old monotonically-restrictive weighted-sum caution formula with a coupled Gravity/Thrust/Lift/Drag model. This is real architectural progress: it introduces the fabric's first value term (Thrust), and it names stall (over-caution, proposal-framing on reversible L4 work) as a distinct, detectable failure mode that the old weighted-sum system structurally could not represent. Its own ratification dependencies (D1-D4) are marked satisfied in the tracker, and the wiring (`flight_model.py`) is built and tested (16/16).
- **`autonomy-posture-check-layer-4.2-DRAFT.md`**: the spec twin of the live `autonomy-posture-check-layer-4.2.sh` hook, the fabric's only property-based (not lexical) detector.
- **`autonomy-gate-surface-matrix-v0-DRAFT.md`**: an unstarted scope-expansion (Slack, Jira, computer-use surface coverage), explicitly downstream of flight-model v1 ratification by its own frontmatter.
- **`autonomy-flight-model-ratification-tracker.md`**: the status board tying all three together.

None of this shipped, and correcting the workflow's own miss on this point: it is not that nobody executed a known fix. It is that the fix requires your decision (correctly gated, per the signals' own `decision_owner` field, as L2), you were asked twice, at the 14-day mark (2026-06-12) and the 30-day mark (2026-06-28), and it has not yet been decided either way. The file has one commit, dated 2026-05-29, and is still warn-only 35+ days later. The flight model cannot be honestly ratified because its Drag term depends on Layer 4.2 telemetry that is currently near-zero-precision garbage.

What IS a real gap, found by re-reading both existing signals directly (not a new adversarial test, the data was already on disk): replaying the recommended patch against all historical `would_block=1` fires (3 at the 14-day mark, growing to 8 at the 30-day mark) shows most match the stop-word/pronoun pattern, but `team-configs`, listed in the 06-28 signal's own FP table, is a real compound noun. The recommended stop-word exclusion list, as specified in both signals, will not suppress that fire. Neither prior signal caught this before recommending the patch as "fully specified." So the two-times-surfaced recommendation is directionally right (promote after a real fix, not before) but the fix itself needs one more pass before it is actually ready to hand you as a yes/no decision.

## 5. Three Candidate Fixes, Evaluated

**`prevention_first`: refuted outright, not a usable design.** Every field in the submitted design was literal placeholder text ("test", `["a"]`, an undated `feasibility_score: 0.5`). There was nothing to adversarially test. The verification pass did the useful work anyway by grounding itself in the real hook file and real telemetry, and surfaced two things worth keeping regardless of what replaces this stub: (a) the `HAS_DISPATCH` gate in the live hook is satisfiable by merely naming a dispatch-sounding word without an actual `tool_use` block, a real narrow gap; (b) any future proposal must state explicitly whether it stays Stop-only (inherits the paraphrase ceiling) or adds a behavior-based PreToolUse check keyed off actual tool_use records instead of prose. **Verdict: not viable as submitted. Re-solicit a concrete design if this path is wanted.**

**`consolidation`: right priority order, wrong on two checkable claims, one of which I corrected post-audit.** The design proposes three moves: execute the Layer 4.2 fix, merge duplicate lexical-check files (`autonomy-grant-stop-check.sh` + `closure-discipline-stop-check.sh`, and the two SessionStart primers), and give each stalled DRAFT an explicit disposition (ratify Layer 4.2, hold the flight model pending a real Drag reading, demote the gate-surface matrix to backlog). The workflow's adversarial pass flagged the cited 06-12/06-28 signals as not existing on disk; that check was wrong, both files exist, they are just untracked in the intent repo's git working tree, which a git-history-based search would miss. Correcting the workflow's error: the design's fire count (11) doesn't match the signals' own numbers (3 at 14 days, 8 at 30 days, both fully accounted for in-file), and the `team-configs` gap is real but was already latent in the existing 06-28 signal's own FP table, not a new discovery. Separately, the design's Stop-array arithmetic (9 hooks down to ~6) only accounts for 3 of the 9 live Stop entries, silently omitting `link-format-stop-check.sh`, `presend-assertion-check.sh`, `engagement-signal-cadence-check.sh`, and `forge-signal-cadence-stop-check.sh`, all the same architecturally-reactive, regex-based shape and undiagnosed instances of root cause 2 sitting outside the proposed scope. Separately, the design's own claim that Layer 4.2 is "property-based, non-lexical" is weakened by the fact that its `gate_no_info_gap` heuristic is itself a shallow substring scan ("TBD" in tail, "Brien decides" in tail), reproducing the exact gaming surface it claims to escape. What did verify cleanly: the sunset-train block counts (CHECK5=100, CHECK4=36, CHECK7=32, CHECK6=26, CHECK1=25, CHECK2=5 vs. claimed 7, CHECK3=1) are close to the design's figures and the file-disposition logic for the three DRAFT specs is coherent and honest about the reactive-timing ceiling it does not attempt to close. **Verdict: the diagnosis-to-priority-order (fix Layer 4.2 first) is right, and it is right because you already asked for it twice and it is still open, not because it was overlooked; the specific patch and its promotion timeline are not ready to execute as written.**

**`tooling_leverage`: refuted on multiple factual claims about the Entire CLI, and its core mechanism reproduces the failure mode it claims to fix.** The design proposes replacing Layer 4.2's lexical `gate_reversible` keyword match with a real state check against `entire status`, on the theory that checkpoint existence is a structural fact, not a judgment call. Adversarial verification, run directly against the live CLI, found: `entire status --json` does not exist (only `--detailed`); `entire status` with no arguments returns a global, machine-wide active-session listing, not per-repo checkpoint state, so extracting "is this repo/session checkpointed" requires a second layer of text-parsing bolted onto a design whose entire premise is "stop parsing text"; the proposed external-side-effect tool classifier (matching tool names against literal substrings like "slack," "gmail/send") fails silently on real tool names in this session, e.g. `create_draft` (a genuine Gmail-drafting action) contains no matching substring and would be misclassified as fully local; and the design's proposed source-of-truth reuse (`native-connector-precedence-map.json`) does not have the coverage or shape needed for this purpose, covering only Gmail/Calendar/Drive with free-text notes, not a machine-checkable tool registry. The design is honest and accurate about its own limits (it correctly states it does not fix the reactive-timing root cause and that Layer 4.2 remains inert until promoted), but its central mechanism claim, "no paraphrase to evade a check that inspects which tool functions were actually called," is false as specified: it is a hand-maintained keyword list on tool names instead of on prose, the same failure class relocated. **Verdict: the SessionStart/skill-text prose changes are low-risk and roughly sound; the Layer 4.2 mechanism rewrite is not usable as specified.**

All three designs were adversarially verified and refuted in whole or in load-bearing part. None ships as-is.

## 6. Recommendation

**Fix Layer 4.2's target extractor for real, using all historical fires as the test set (8 as of the 06-28 signal, re-pull the current count since it's now 2026-07-03), then bring the promote/retire/ratify decision back to you as a clean yes/no, not a re-ask of the same open question.** One-line why: this is not a new task, it is the same decision two prior signals already asked you for and you have not yet answered; the reason to act now rather than defer again is that the diagnosis itself needed one more correction (the `team-configs` gap) before the yes/no you're being asked is actually trustworthy.

This is not a bare choice between the three candidate designs; none of them is ready to execute wholesale. The right move is to take the correctly-diagnosed priority order from the `consolidation` design (fix Layer 4.2 first, dispose of each DRAFT explicitly, do not blanket-ratify), throw out its specific stop-word patch and 3-5 day promotion timeline (both falsified), and defer the `tooling_leverage` design's Entire-wiring and the broader file-merge (Move 2) as separate, lower-priority follow-ons that should not gate the Layer 4.2 fix. Do not pursue `prevention_first` further unless a concrete mechanism is specified; the placeholder gave nothing to build on.

Unless you'd prefer to greenlight the full consolidation plan (file merges included) in one pass, in which case the sequencing risk is that Move 2's regex-preservation-under-merge (39KB+11KB of dense bash/embedded-python patterns copied by hand) is real transcription risk on a governance-critical file that runs on every response, and should not be bundled with the Layer 4.2 fix in the same change.

## 7. Concrete Action Plan

**Phase 1: Correct the Layer 4.2 diagnosis (today, hours-scale).**
1. Read `/Users/brien/.claude/logs/autonomy-posture-layer42.jsonl` in full and manually classify all `would_block=1` fires (currently 9, not 11) into stop-word/pronoun-pattern fires vs. genuine-noun fires like `team-configs`.
2. For the genuine-noun class, determine the actual shared property (if any) that distinguishes a false positive from a real catch, rather than assuming stop-word exclusion covers everything. This may require a different classifier axis entirely (e.g., whether the extracted target resolves to an actual file/entity reference vs. a generic word).
3. Update `Core/frameworks/intent/hooks/autonomy-posture-check-layer-4.2.sh` (the `NEXT_ACTION_RE` match-processing block, embedded Python, around the target-capture logic) and its spec twin `Core/frameworks/intent/spec/autonomy-posture-check-layer-4.2-DRAFT.md` together, so they do not drift again.
4. Do not write a new signal claiming this is fixed until Step 2's classifier has been replayed against all 9 fires with zero unexplained residual, not just the 6 that fit the original hypothesis.

**Phase 2: Re-calibrate with a real window, not a rushed one.**
5. Run a genuine re-calibration window against fresh traffic. Given the diagnosis already shows the first fix attempt was under-characterized, do not compress this to 3-5 days on the assumption the bug is fully understood; use whatever window (likely 7-10 days) is needed to see the fire rate on a corrected extractor, and manually eyeball every fire.
6. Only after that window closes clean (or with fires that are genuine catches, not noise) should Layer 4.2 be flipped from warn-only to block mode. This requires editing the hardcoded `exit 0` / WARN-ONLY block at the end of the script to conditionally emit a real block decision, gated behind an env toggle you flip off deliberately, not silently.

**Phase 3: Dispose of each stalled DRAFT explicitly, per the consolidation design's Move 3 logic (which verified as sound).**
7. `autonomy-posture-check-layer-4.2-DRAFT.md`: ratify (`status: draft` to `status: accepted`) only after Phase 2 closes clean.
8. `autonomy-flight-model-v1-DRAFT.md`: re-run `flight_model.py` once Layer 4.2 is producing real Drag signal. Ratify in the same session as the re-run if the reading clears STALL; if it does not, write a fresh, specific signal naming the binding constraint (likely Thrust/strategic_value calibration) rather than letting a third dead-letter recommendation accumulate.
9. `autonomy-gate-surface-matrix-v0-DRAFT.md`: add `status: draft-blocked` and `blocked_on: autonomy-flight-model-v1-DRAFT.md ratification` to its frontmatter now, independent of Phases 1-2, so it stops reading as abandoned.
10. `autonomy-flight-model-ratification-tracker.md`: update in place as each step above lands; it already has the right shape.

**Phase 4: Defer, do not bundle, the following (separate sessions, lower priority).**
11. File consolidation (merging `autonomy-grant-stop-check.sh` + `closure-discipline-stop-check.sh`, and the two SessionStart primers) is legitimate cleanup but should not touch the same change as Phase 1-2, given the regex-preservation risk on a governance-critical file. If pursued, diff detection behavior against 30 days of transcript samples before deleting either original, and also inventory the four undiagnosed Stop-array entries the consolidation design missed (`link-format-stop-check.sh`, `presend-assertion-check.sh`, `engagement-signal-cadence-check.sh`, `forge-signal-cadence-stop-check.sh`) so the "collapse duplicate machinery" goal is not silently partial.
12. Entire-CLI wiring into Gate 1 needs a from-scratch design, not the one adversarially refuted here. Any future version must resolve per-repo/per-session checkpoint state without relying on a nonexistent `--json` flag or a global session listing, and must not reintroduce a hand-maintained keyword list for external-side-effect tool classification without a real machine-checkable source of truth (the existing `native-connector-precedence-map.json` does not have the right shape or coverage).
13. Set up the scheduled re-check the consolidation design proposed in its Move 3 (7-day cadence via `mcp__scheduled-tasks`, re-running telemetry checks and auto-emitting a signal, not an auto-action, when a promote/retire condition is newly met), but only after Phase 2 proves the underlying metric is trustworthy. A scheduled task that re-checks a broken metric just automates the neglect pattern faster.
14. Open a signal (not a fix) for the paraphrase-ceiling problem on the four undiagnosed Stop-array hooks named in Step 11, since they are the same architectural shape as the already-frozen lexical layer and are not currently governed by `lexical-layer-freeze.yaml`'s cap discipline.
15. Open a signal proposing a Gauntlet disconfirmation pass against the autonomy-grant hook mechanism itself, since root cause 5 names this as a real, never-executed gap, and this audit is itself evidence of why that gap matters (two of three candidate designs contained falsifiable claims that went unchecked until adversarially tested here).

## 8. What This Means For Parallax

The diagnosis names a real integration gap, and it is worth stating plainly rather than deferring it into the file-level plan above, because it is a different kind of problem: a citation problem, not an implementation problem.

Parallax's governance-layer VSM mapping (`Core/products/parallax/spec/2026-05-31-governance-layer-vsm.md`) re-labels the same L0-L4 autonomy taxonomy in S3-S5 vocabulary and names the Stop hook "the strongest algedonic act." The Selection Docket reuses the 4-gate doctrine as a boundary condition. Both treat the hook mechanism as settled, reliable infrastructure. Neither has ever modeled the hook's actual mechanics (the regex cascade, its bypass semantics, its false-positive and false-negative behavior) as a governed artifact in its own right, the way Gauntlet governs Voices' output or Scout governs Topography's scoring. This audit is itself the first time anything in the ecosystem has adversarially tested the hook's reliability claims, and it found real problems in the very designs meant to fix it.

Two concrete follow-ons for Parallax, separate from the hook-fix work above:

- The VSM document's characterization of the Stop hook as the strongest algedonic signal should be revised to note it is a reactive-only signal with a documented paraphrase ceiling and an inert (warn-only) structural detector, not an unqualified strength claim. This is a small edit but it changes what downstream governance reasoning is allowed to assume.
- Decision Reconsideration has no registered trigger for the autonomy-grant hook despite 7 documented iterations of its primary detection file. Given this audit found two of three proposed fixes contained falsified claims, a `reconsider_when` trigger tied to Layer 4.2's promotion event (Phase 2, Step 6 above) would give Parallax's own reconsideration machinery a natural hook into this specific, currently-ungoverned artifact.

Neither of these blocks the Phase 1-3 work above. They are governance hygiene that should happen once the underlying hook is actually trustworthy, not before.

## 9. Proposed DDR Stub

```
## WS-DDR-XXX: Autonomy-grant Layer 4.2 promotion gated on corrected diagnosis, not prior stop-word patch

**Context:**
The Intent-framework autonomy-grant enforcement fabric (Core/frameworks/intent/hooks/) chronically
fails to prevent pause/proposal-framing on work already granted L4 standing autonomy. Root cause
analysis (2026-07-03 audit) found this is dominantly a platform-architecture ceiling (Stop hooks fire
only after full response generation, so detection is inherently reactive) compounded by a lexical
regex cascade that cannot converge against paraphrase (7 CHECKs added 2026-04-28 to 2026-05-29, each
patching the prior CHECK's bypass). The one structurally sound fix, Layer 4.2's property-based
detector, has been warn-only since its single 2026-05-29 commit (35+ days) and has already been
surfaced to Brien twice for the promote/retire/ratify decision, correctly gated as L2
(SIG-2026-06-12-layer42-calibration-review.md, SIG-2026-06-28-flight-model-30day-ratification-readiness.md,
both on disk, currently uncommitted in the intent repo), with neither decision taken yet. Both prior
signals recommend the same one-line stop-word-exclusion patch for the target-extractor bug. Direct
review of the 06-28 signal's own false-positive table found that recommendation is not quite
complete: it lists `team-configs` among the false positives it attributes to the stop-word/pronoun
pattern, but `team-configs` is a genuine compound noun, not a stop-word, and will not be suppressed
by the fix as specified.

**Decision:**
Layer 4.2 promotion from warn-only to block mode is gated on a corrected target-extractor diagnosis
that accounts for ALL historical fires (not just the stop-word-pattern subset), followed by a
re-calibration window sized to the actual uncertainty (not a compressed 3-5 day window assumed
sufficient by the now-falsified prior diagnosis). The three stalled DRAFT specs
(autonomy-flight-model-v1-DRAFT.md, autonomy-gate-surface-matrix-v0-DRAFT.md,
autonomy-posture-check-layer-4.2-DRAFT.md) each receive an explicit status disposition rather than a
blanket ratify-or-abandon: Layer 4.2 spec ratifies on clean re-calibration; flight-model v1 ratifies
or gets a fresh stall-diagnosis signal once real Drag telemetry exists; gate-surface matrix is marked
draft-blocked pending flight-model v1. File consolidation (merging duplicate lexical Stop-hook files)
and Entire-CLI wiring into Gate 1 are deferred to separate follow-on work, not bundled into this fix,
given their own adversarially-identified defects (undiagnosed Stop-array entries omitted from the
consolidation's scope; nonexistent entire status --json flag and tool-name-substring gaming surface
in the Entire-wiring proposal).

**Alternatives considered:**
1. Execute the originally-proposed stop-word patch and promote on the timeline the 06-28 signal
   suggested. Rejected: direct review of that signal's own FP table found the patch incomplete
   against live telemetry (team-configs fire), and rushing promotion on an incomplete fix risks a
   live false block on real work, which is a worse outcome than staying warn-only one more cycle.
2. Wire Entire CLI into Gate 1 as the mechanism to replace lexical gate_reversible (the tooling_leverage
   design). Rejected for this DDR's scope: multiple factual claims about the Entire CLI's status
   command and a proposed tool-name classifier were falsified on direct testing; needs a from-scratch
   design, not adoption as specified.
3. Full file consolidation of all Stop-hook lexical checks in the same pass as the Layer 4.2 fix (the
   consolidation design's Move 2). Rejected for sequencing: bundling a regex-preservation-risk file
   merge with a governance-critical bug fix on the same change increases blast radius on a system that
   runs on every response; consolidation is legitimate but should be its own change, and should also
   cover the four Stop-array hooks (link-format, presend-assertion, engagement-signal-cadence,
   forge-signal-cadence) the original proposal omitted.
4. Leave Layer 4.2 in warn-only mode indefinitely and accept the reactive lexical layer as the
   permanent enforcement mechanism. Rejected: this is the status quo that produced the chronic
   complaint this audit was commissioned to address; abandoning the one structural, non-lexical
   detector concedes the paraphrase-ceiling problem is unsolvable when it is only unexecuted.

**Consequences:**
Layer 4.2 remains inert (telemetry-only, no enforcement effect) for longer than the previously-assumed
3-5 day timeline, because the corrected diagnosis requires re-characterizing all 9 fires before a
patch can be trusted. The flight-model redesign's ratification remains blocked until Layer 4.2
produces trustworthy Drag telemetry, meaning the fabric's only escape from the lexical arms race stays
theoretical for at least one more calibration cycle. The reactive-timing root cause (Stop hooks fire
after generation) is explicitly out of scope for this DDR and will not be resolved by it; this remains
a platform ceiling, not a design defect, and should not be re-litigated inside this decision.

**Validation criteria:**
Layer 4.2 promotion to block mode is validated when: (a) all historical would_block=1 fires (8 as of
the 06-28 signal, re-pull the current count before patching since 5 days of additional traffic have
since accrued) have been individually classified and the extractor fix demonstrably suppresses the
false-positive class while preserving the genuine-catch class, with the classification method
documented, not assumed, and specifically covering non-stop-word genuine-noun fires like
`team-configs` that the 06-12/06-28 signals' own FP tables mis-bucketed; (b)
a re-calibration window of sufficient length (minimum 7 days of live traffic) shows a residual
false-positive rate the model itself would characterize as acceptable for block-mode enforcement,
not just "lower than before"; (c) the promotion event is recorded in
autonomy-flight-model-ratification-tracker.md with the corrected diagnosis method cited, so a future
review can distinguish this fix from the two prior warn-only reviews' incomplete FP classification.
Flight-model v1
ratification is validated when a post-Layer-4.2-promotion flight_model.py run shows Thrust clearing
Drag on real (not assumed) telemetry, or, failing that, a fresh signal names the specific binding
constraint rather than leaving the finding unrecorded.
```