---
signal_id: RETRO-2026-04-30-closure-discipline-SIG-1
title: Two-layer drift in same response — symptom-patch escalation followed by bare-choice escalation
severity: high
detected: 2026-04-30
status: resolved
source: retroactive-extraction
trust_score: 0.75
autonomy: L2
upstream_control_path: "Core/frameworks/intent/hooks/autonomy-grant-stop-check.sh (CHECK 1 through CHECK 7, frozen 2026-05-29 per lexical-layer-freeze.yaml) + ~/.claude/audit/autonomy-grant-stop-detections.log"
catch_mechanism: "the Stop hook fires on every assistant turn (not just session-end) and runs 7+ distinct CHECK patterns in one invocation, directly answering this signal's ask for compound-drift coverage; continuously-updated audit log (93KB, last entry 2026-07-08) gives the investigation-log capability this signal asked for"
verification_command: "wc -l /Users/brien/.claude/audit/autonomy-grant-stop-detections.log && grep -c '^# Pattern:' Core/frameworks/intent/hooks/autonomy-grant-stop-check.sh"
---
# Two-layer drift in same response — symptom-patch escalation followed by bare-choice escalation

## Observation
When asked to assess the recurring symptom-patch-disguised-as-resolution drift, the response itself drifted twice:

1. Layer-1 drift: presented a known-precedent solution (parallel-to-autonomy-grant hook) AND optionally a "lighter weight" alternative (upstream-controls-table-as-discipline)
2. Layer-2 drift: ended with a bare-choice question — "Should I draft the hook spec + bash script... Or is the upstream-controls-table-as-discipline the lighter-weight starting point you'd prefer?"

The autonomy-grant Stop hook should have caught Layer-2 drift (bare-choice without recommendation marker). Either:
- The hook didn't fire (possible: the response had recommendation markers in body, just not in the closing question)
- The hook fired but wasn't visible to the operator
- The hook only catches certain bare-choice phrasings and missed this one
- The hook only fires on Stop event, not on user-message-arrival

## Context
This was during the closure-discipline mechanism design conversation. The L4 answer was: design + critique with panels + execute fully + communicate along the way — not present-options-to-Brien. Brien explicitly named the second-layer drift in his next message: "you presented a known previously approved solution and optionally a lesser solution. The L4 answer is to design implement and critique or assess the solution with our panels and execute it fully..."

## Implication
The autonomy-grant hook's bare-choice detector has at least one gap. The phrasing "Should I X or is Y the lighter-weight starting point you'd prefer?" matches the BARE_CHOICE_RE pattern but the response body may have contained recommendation markers (this needs verification by reading the audit log at `~/.claude/audit/autonomy-grant-stop-detections.log`).

Investigation actions:
1. Check if the autonomy-grant Stop hook fired on that response (audit log)
2. If it didn't fire, identify which markers tipped REC_MATCH=1 inappropriately
3. If it did fire, identify why the operator didn't see the block decision

Broader pattern: two-layer drift is harder to catch than single-layer drift. The model can drift on dimension A (symptom-patch instead of upstream-fix), recover when prompted, but then drift on dimension B (bare-choice instead of execute) in the recovery response. Hooks need to consider compound drift, not just single-pattern drift.

Possible upstream control: each behavioral hook should run on EVERY assistant response, not just session-end. The current Stop hook only fires when the model says "I'm done" — it should also fire on responses that include question-marks AND aren't pure task-clarification.

## Triage, 2026-07-08

Disposition: control exists now, verified live. Claude Code's Stop hook fires at the end of every assistant turn (not only on an explicit "I'm done" claim), which is the "every response" coverage this signal asked for. `hooks/autonomy-grant-stop-check.sh` has grown to CHECK 1 through CHECK 7 (formally frozen 2026-05-29 per `lexical-layer-freeze.yaml`) plus a companion `closure-discipline-stop-check.sh`, each targeting a different drift shape in the same invocation, directly addressing "hooks need to consider compound drift, not just single-pattern drift." The audit log at `~/.claude/audit/autonomy-grant-stop-detections.log` is continuously written (93KB, entries through 2026-07-08), giving the specific investigation capability this signal's Implication asked for (checking whether a hook fired, and on what basis). The specific historical incident this signal describes cannot be re-diagnosed (no timestamp/session ID given), but the infrastructure gap it identified is closed.
