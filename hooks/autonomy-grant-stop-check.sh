#!/usr/bin/env bash
# autonomy-grant-stop-check.sh
#
# Stop hook — Layer 4 of autonomy-grant enforcement (linguistic detector).
#
# Detects six drift patterns and forces revision:
#
#   CHECK 1 — Bare-choice-instead-of-recommendation (v1, 2026-04-28)
#     Pattern: response ends with "Want me to A, or B?" / "Should I X or Y?"
#     style multi-option question without any recommendation marker in the body.
#
#   CHECK 2 — Soft-queue framing on pre-authorized continuation (v2, 2026-05-13)
#     Pattern: response references a next stage/synthesis/Task/Phase/Wave by name,
#     dispatches nothing in the same turn, AND tail contains soft-queue phrases
#     ("Say go and I X", "unless you want me to pause", "want me to dispatch?",
#     "shall I proceed?", etc.). Slips past CHECK 1 because a recommendation
#     marker precedes the soft-queue tail.
#
#   CHECK 3 — L0-on-push framing on theparlor/* repos (v3, 2026-05-20)
#     Pattern: response commits to theparlor/* and hands push back to Brien
#     with phrases like "Not pushed. Run git push from <path>..." despite
#     solo-repo L4 push grant.
#
#   CHECK 4 — Conditional-queue framing on pre-authorized continuation (v3, 2026-05-26)
#     Pattern: response describes a next L4 action and ends with veto-offer
#     framing ("unless you redirect", "I'll X next unless", "going to X unless").
#     Recommendation marker preceding the tail does NOT redeem it.
#
#   CHECK 5 — Implicit-queue / standby framing (v4, 2026-05-28)
#     Pattern: response contains implicit-gating phrases that position the
#     model as waiting for Brien's instruction to act on already-authorized
#     L4 work: "ready to execute when you say go", "let me know when",
#     "ready when you are", "say the word", "standing by", "I'll wait for
#     your call", "when you're ready", "next steps depend on...", etc.
#     Caught because they are structurally equivalent to bare-choice even
#     though no question mark appears.
#     Context gate: the phrase must appear without an adjacent "if you have
#     questions" / "if there's anything else" style conversational close
#     (those are acceptable L2 surface closers, not implicit queues).
#
#   CHECK 6 — Trailing-observation-after-proposal (v5, 2026-05-28)
#     Pattern: response delivers diagnosis/recommendation/analysis/artifact
#     and then STOPS at a trailing analytical sentence that comments on the
#     structure, scope, quality, or delta of the work just described —
#     without an execution verb or dispatch in the same turn. The closing
#     sentence reads as a "complete deliverable" when it is structurally
#     equivalent to a hand-off pause. No forbidden keyword from CHECK 5
#     appears; the drift is purely positional.
#     Source incident: "stopped at a closing comment about delta-from-original"
#     (SIG-2026-05-27-pause-drift-cross-reference-sweep-after-prompt-rework).
#     Trigger phrases (last ~400 chars only, conservative):
#       "The biggest [delta/difference/change/shift/gap] [from/with/...]"
#       "The most [interesting/notable/striking/important/significant] [aspect/part/thing]"
#       "Worth noting [that/:]"  / "Notable:" / "Of note:"
#       "One [observation/thing to watch/thing to note] ..."
#       "The key insight here is ..."
#       "It's worth (pointing out|noting|flagging) [that]"
#     Context gate (four stacked):
#       (a) Dispatch gate: HAS_DISPATCH=1 — skip (observation is narrative)
#       (b) Closure-DoD gate: response contains upstream_control_path +
#           catch_mechanism + pipeline_survival — skip (legitimate closure)
#       (c) Recommendation-with-reveal gate: response contains recommendation
#           marker AND "unless you prefer" / "alternatively" — skip (L2 surface)
#       (d) L2-info-gap gate: response contains "info gap:" / "l2 decision" /
#           "brien needs to decide" — skip (legitimate decision surface)
#
# Spec: Core/frameworks/intent/spec/autonomy-grant-enforcement.md (Layer 4)
# Signal: Core/products/org-design-tooling/.intent/signals/SIG-AUTONOMY-DRIFT-POST-STAGE-2026-05-13.md
# Signal: .intent/signals/SIG-2026-05-28-stop-hook-regex-extension-implicit-queue.md
# Signal: Core/frameworks/intent/.intent/signals/SIG-2026-05-28-stop-hook-check-6-trailing-observation.md
#
# Install: chmod +x and symlink to ~/.claude/hooks/
# Register: add Stop entry to ~/.claude/settings.json
#
# Bypass: AUTONOMY_GRANT_STOP_BYPASSED=1
# Audit log: ~/.claude/audit/autonomy-grant-stop-detections.log
# Telemetry: ~/.claude/logs/autonomy-stop-check.jsonl (AM-3 mechanical probe)
#
# Created: 2026-04-28 — promotes Layer 4 from "future iteration" to deployed
#   in response to repeat bare-choice slips on autonomy-grant-enforced sessions.
# Updated: 2026-05-13 — adds CHECK 2 soft-queue detector per
#   SIG-AUTONOMY-DRIFT-POST-STAGE-2026-05-13 §3 Layer 3 + JSONL telemetry.
# Updated: 2026-05-20 — adds CHECK 3 L0-on-push detector per
#   SIG-2026-05-20-l0-on-push-framing-no-hook-catch.md.
# Updated: 2026-05-26 — adds CHECK 4 conditional-queue detector per
#   SIG-2026-05-26-autonomy-grant-drift-recurrence-in-session.md.
# Updated: 2026-05-28 — adds CHECK 5 implicit-queue/standby detector per
#   SIG-2026-05-27-pause-drift-items-3-6-7-8-after-coverage-push.md et al.
# Updated: 2026-05-28 — adds CHECK 6 trailing-observation-after-proposal detector per
#   SIG-2026-05-27-pause-drift-cross-reference-sweep-after-prompt-rework.md.

set -u

AUDIT_LOG="$HOME/.claude/audit/autonomy-grant-stop-detections.log"
TELEMETRY_LOG="$HOME/.claude/logs/autonomy-stop-check.jsonl"
mkdir -p "$(dirname "$AUDIT_LOG")" 2>/dev/null || true
mkdir -p "$(dirname "$TELEMETRY_LOG")" 2>/dev/null || true

# Bypass
if [ "${AUTONOMY_GRANT_STOP_BYPASSED:-0}" = "1" ]; then
  exit 0
fi

# Read input JSON from stdin
INPUT=$(cat)

# Parse input defensively (fail open). Single-line space-separated output.
read -r SESSION_ID TRANSCRIPT_PATH STOP_ACTIVE <<< "$(python3 -c "
import json, sys
try:
    d = json.loads(sys.stdin.read() or '{}')
    sid = d.get('session_id', 'unknown')
    tpath = d.get('transcript_path', '') or 'NONE'
    sactive = d.get('stop_hook_active', False)
    # Replace any whitespace in path (defensive)
    tpath = tpath.replace(' ', '\\\\ ')
    print(sid, tpath, 'true' if sactive else 'false')
except Exception:
    print('unknown', 'NONE', 'false')
" <<< "$INPUT")"

# Recursion guard — if Stop hook already fired this cycle, exit
if [ "$STOP_ACTIVE" = "true" ]; then
  exit 0
fi

# No transcript → exit gracefully
if [ "$TRANSCRIPT_PATH" = "NONE" ] || [ ! -f "$TRANSCRIPT_PATH" ]; then
  exit 0
fi

# Extract last assistant message text (concatenate all text blocks)
LAST_TEXT=$(python3 -c "
import json, sys
try:
    path = sys.argv[1]
    last_assistant = None
    with open(path) as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                obj = json.loads(line)
            except Exception:
                continue
            if obj.get('type') == 'assistant':
                last_assistant = obj
    if not last_assistant:
        sys.exit(0)
    msg = last_assistant.get('message', {})
    content = msg.get('content', [])
    if isinstance(content, str):
        print(content)
    elif isinstance(content, list):
        texts = []
        for block in content:
            if isinstance(block, dict) and block.get('type') == 'text':
                texts.append(block.get('text', ''))
        print('\n'.join(texts))
except Exception:
    sys.exit(0)
" "$TRANSCRIPT_PATH" 2>/dev/null)

# No text extracted → exit
if [ -z "$LAST_TEXT" ]; then
  exit 0
fi

# Last paragraph approximation — last 1000 chars
LAST_PARA=$(printf '%s' "$LAST_TEXT" | tail -c 1000)

# Lowercase for case-insensitive matching
LOWER_PARA=$(printf '%s' "$LAST_PARA" | tr '[:upper:]' '[:lower:]')
LOWER_FULL=$(printf '%s' "$LAST_TEXT" | tr '[:upper:]' '[:lower:]')

# ---------------------------------------------------------------------------
# CHECK 1: Bare-choice-without-recommendation (v1 — 2026-04-28)
# ---------------------------------------------------------------------------

# Bare-choice pattern: multi-option deferral question near end
BARE_CHOICE_RE='(want me to|should i|should we|do you want me to|would you like me to|do you want to|want to|shall i)\s+[^?]{3,200}\bor\b\s+[^?]{3,200}\?'

# Recommendation markers — presence of ANY signals committed POV in the response.
# Inclusive list to keep false-positive rate low for v0.
RECOMMENDATION_RE="(i recommend|my recommendation|i'?d recommend|recommend(ation)?:|my pick|i'?d lean|my read|bottom line|tl;dr|lead recommendation|i'?d go with|i'?d choose|going with|going to (write|run|build|execute|deploy|do|start)|my call|i'?ll (do|run|write|start|build|skip|defer|deploy|execute)|let'?s (go|do|run|start|build|skip|defer|execute)|\*\*recommend|^recommend|recommend\.|locking in|committing to|the (right|cleanest|sharpest) (move|cut|call|path) is|the answer (is|here is)|going (with|for) (the |a |\*\*)|pick (a|one|the)|first (move|step|pass) is|priority (one|here) is|should be (the |a )|i'?d say|my take|the move (is|here)|i lean|leaning (toward|to)|i'?m going (with|to))"

BARE_MATCH=0
if echo "$LOWER_PARA" | grep -qiE "$BARE_CHOICE_RE"; then
  BARE_MATCH=1
fi

REC_MATCH=0
if echo "$LOWER_FULL" | grep -qiE "$RECOMMENDATION_RE"; then
  REC_MATCH=1
fi

# ---------------------------------------------------------------------------
# CHECK 2: Soft-queue framing on pre-authorized continuation (v2 — 2026-05-13)
#
# Detects the recommendation-marker-glove variant: a recommendation precedes
# the response so CHECK 1 passes, but the tail still queues L4-eligible work
# awaiting approval. Pattern origin: SIG-AUTONOMY-DRIFT-POST-STAGE-2026-05-13.
#
# Three sub-patterns per §3 Layer 3 of the signal:
#   variant 1: "Say [go/yes/proceed] and I [verb]"
#   variant 2: "unless you('d like| want)"
#   variant 3: "want/shall me/I (dispatch|proceed|launch|continue)?"
#
# Context gate: also require reference to next-stage work AND absence of
# any Agent tool-call dispatch in the same turn. The context gate keeps
# false-positive rate low on legitimate "here is what I just did" summaries.
# ---------------------------------------------------------------------------

FOUND_SOFT_QUEUE=0

# Variant 1: "Say 'go' and I ..." / "Tell me 'go' and I ..."
if echo "$LAST_PARA" | grep -iE '\b(Say|Tell me) ["'"'"']?(go|yes|proceed)["'"'"']?\s+and I\b' >/dev/null 2>&1; then
  FOUND_SOFT_QUEUE=1
fi

# Variant 2: "unless you'd like" / "unless you want"
if echo "$LAST_PARA" | grep -iE '\bunless you('"'"'d like| want)\b' >/dev/null 2>&1; then
  FOUND_SOFT_QUEUE=1
fi

# Variant 3: "want me to dispatch?" / "shall I proceed?" / "want me to continue?" etc.
if echo "$LAST_PARA" | grep -iE '\b(want|shall) (me to|I) (dispatch|proceed|launch|continue)\?' >/dev/null 2>&1; then
  FOUND_SOFT_QUEUE=1
fi

# Context gate: soft-queue only fires when response references a named next stage
# (Task X.Y / Phase X.Y / Wave Xy / "synthesis" / "next stage")
# AND the response contains no dispatched agent call marker
NEXT_STAGE_RE='(task [0-9]+\.[0-9]+|phase [0-9]+\.[0-9]+|wave [0-9]+[a-z]?|next stage|synthesis|next wave|next phase)'
DISPATCH_RE='(dispatching|launching [0-9]+ sub-?agent|agent\(|model:)'

HAS_NEXT_STAGE=0
if echo "$LOWER_FULL" | grep -qiE "$NEXT_STAGE_RE"; then
  HAS_NEXT_STAGE=1
fi

HAS_DISPATCH=0
if echo "$LOWER_FULL" | grep -qiE "$DISPATCH_RE"; then
  HAS_DISPATCH=1
fi

# Soft-queue fires only when: soft-queue phrase present + next-stage reference + no dispatch
SOFT_QUEUE_TRIGGER=0
if [ "$FOUND_SOFT_QUEUE" = "1" ] && [ "$HAS_NEXT_STAGE" = "1" ] && [ "$HAS_DISPATCH" = "0" ]; then
  SOFT_QUEUE_TRIGGER=1
fi

# ---------------------------------------------------------------------------
# Emit JSONL telemetry (AM-3 mechanical probe) — fires on every hook execution
# so frequency trends are observable, not just caught events.
# ---------------------------------------------------------------------------

TIMESTAMP=$(date -u +%Y-%m-%dT%H:%M:%SZ)
TAIL_SAMPLE=$(printf '%s' "$LAST_PARA" | tail -c 200 | tr '\n' ' ' | tr '"' "'" | tr '\' '/')

printf '{"ts":"%s","session":"%s","bare_match":%d,"rec_match":%d,"soft_queue_found":%d,"next_stage":%d,"dispatch":%d,"soft_queue_trigger":%d,"tail":"%s"}\n' \
  "$TIMESTAMP" "$SESSION_ID" "$BARE_MATCH" "$REC_MATCH" \
  "$FOUND_SOFT_QUEUE" "$HAS_NEXT_STAGE" "$HAS_DISPATCH" "$SOFT_QUEUE_TRIGGER" \
  "$TAIL_SAMPLE" >> "$TELEMETRY_LOG" 2>/dev/null || true
# Note: implicit_queue fields are emitted via a separate telemetry append in CHECK 5

# ---------------------------------------------------------------------------
# Block decisions
# ---------------------------------------------------------------------------

# CHECK 1 block: bare-choice present AND no recommendation marker anywhere
if [ "$BARE_MATCH" = "1" ] && [ "$REC_MATCH" = "0" ]; then
  echo "[$TIMESTAMP] CHECK1-CAUGHT session=$SESSION_ID tail='$(printf '%s' "$LAST_PARA" | tail -c 300 | tr '\n' ' ' | tr "'" '_')'" >> "$AUDIT_LOG"

  cat <<'EOF'
{"decision": "block", "reason": "AUTONOMY-GRANT DRIFT (Layer 4 / CHECK 1): your response ends with a bare-choice question (e.g., 'Want me to A, or B?') with no recommendation marker anywhere in the response body. Per decisioning-discipline rule 6 (recommendation-with-reveal, not bare choice) and the autonomy-grant 4-gate check: pick one option as your recommendation with a 1-line why, THEN offer the alternative as 'unless you would prefer B because...'. Revise the response: lead with a recommendation, present the alternative as a reveal, close with a single clear next step rather than a question. If the 4-gate check passes for either option, just execute it and signal."}
EOF
  exit 0
fi

# CHECK 2 block: soft-queue framing on pre-authorized continuation
if [ "$SOFT_QUEUE_TRIGGER" = "1" ]; then
  echo "[$TIMESTAMP] CHECK2-CAUGHT session=$SESSION_ID soft_queue_found=1 next_stage=1 dispatch=0 tail='$(printf '%s' "$LAST_PARA" | tail -c 300 | tr '\n' ' ' | tr "'" '_')'" >> "$AUDIT_LOG"

  cat <<'EOF'
{"decision": "block", "reason": "AUTONOMY-GRANT DRIFT (Layer 4 / CHECK 2 — soft-queue on pre-authorized continuation): your response references a next stage/synthesis/Task/Wave by name, dispatches nothing, and ends with a soft-queue phrase ('Say go and I X', 'unless you want me to pause', 'want me to dispatch?', 'shall I proceed?', etc.). The recommendation marker preceding this tail does NOT redeem it — this is architecturally equivalent to bare-choice on pre-authorized work. 4-gate check: if the next stage is reversible, Workspaces-local, has precedent in this session, and has no info gap — EXECUTE it in this same turn. Do not queue. Do not ask. Dispatch the next stage now or surface the specific L0 gate that blocks execution (external comms, money, NDA boundary)."}
EOF
  exit 0
fi

# ---------------------------------------------------------------------------
# CHECK 3: L0-on-push framing on theparlor/* repos (v3 — 2026-05-20)
#
# Push to theparlor/* solo repos is L4 (reversible via revert/reset, solo user
# population, public-domain material, git reversibility). Handing the push
# back to Brien with phrases like "Not pushed. Run git push from <path> when
# you want it on <remote>." is the same drift class as CHECK 1 but at the
# git-push layer.
#
# Context gate: only fires when the response body contains evidence of a git
# commit to a theparlor/* remote AND no git push followed. If the response
# already pushed (contains "Pushed to" / "git push" executed), passes clean.
#
# Spec: SIG-2026-05-20-l0-on-push-framing-no-hook-catch.md
# Source: feedback_commit_autonomy.md §5 literal forbidden phrases
# ---------------------------------------------------------------------------

# L0-on-push forbidden phrases (literal variants from feedback_commit_autonomy.md §5)
PUSH_HANDOFF_RE='(not pushed[.;]|run.*git push.*from|commit (landed|complete)[;.].*push when|i.?ll commit only|push when you.?re ready|push it (yourself|manually)|push (to remote|to origin) when you want)'

# Context gate: did the response mention a theparlor/* commit?
THEPARLOR_COMMIT_RE='(theparlor/|git commit|committed to.*theparlor|pushed.*theparlor|git log|co-authored-by)'

HAS_THEPARLOR_COMMIT=0
if echo "$LOWER_FULL" | grep -qiE "$THEPARLOR_COMMIT_RE"; then
  HAS_THEPARLOR_COMMIT=1
fi

PUSH_HANDOFF_MATCH=0
if [ "$HAS_THEPARLOR_COMMIT" = "1" ]; then
  if echo "$LOWER_FULL" | grep -qiE "$PUSH_HANDOFF_RE"; then
    PUSH_HANDOFF_MATCH=1
  fi
fi

if [ "$PUSH_HANDOFF_MATCH" = "1" ]; then
  echo "[$TIMESTAMP] CHECK3-CAUGHT session=$SESSION_ID push_handoff=1 theparlor_commit=1 tail='$(printf '%s' "$LAST_PARA" | tail -c 300 | tr '\n' ' ' | tr "'" '_')'" >> "$AUDIT_LOG"

  cat <<'EOF'
{"decision": "block", "reason": "AUTONOMY-GRANT DRIFT (Layer 4 / CHECK 3 — L0-on-push framing on theparlor/* repo): your response hands the git push back to Brien with language like 'Not pushed. Run git push from <path> when you want it on <remote>.' Per feedback_commit_autonomy.md and the commit-autonomy grant: push to theparlor/* solo repos is L4 (reversible via git revert, solo user population, public-domain material, git-tracked history). 4-gate: reversible=yes, local=yes, precedent=yes, no-info-gap=yes → EXECUTE the push. Forbidden patterns (from §5): 'Not pushed. Run git push from X when you want it on Y.', 'Commit landed; push when you're ready.', 'I'll commit only since you said commit, not push.', any sentence handing the push back to Brien on a theparlor/* repo. Execute: cd <repo path> && git push. Exception (genuine L0 that blocks): force-push to main, repo with active reviewers waiting, or Brien explicitly said commit-only."}
EOF
  exit 0
fi

# ---------------------------------------------------------------------------
# CHECK 4: Conditional-queue framing on pre-authorized continuation (v3 — 2026-05-26)
#
# Slips past CHECK 1 (a recommendation marker precedes the queue) and past
# CHECK 2 (the phrasing is forward-looking, not soft-queue). Pattern observed
# 5+ times in a single session (flight-model ingestion, 2026-05-26):
#   "Will write X next unless you redirect."
#   "Going to write X unless you redirect."
#   "Will draft X unless you redirect to A or B."
#   "Recommend starting with #1 unless you redirect to one of the L2 items."
#   "Will write apply_lambda_settings.py next unless you redirect to one of those three."
#
# Spec: SIG-2026-05-26-autonomy-grant-drift-recurrence-in-session.md
# ---------------------------------------------------------------------------

# v3 conditional-queue phrases (case-insensitive, anchored in last paragraph)
COND_QUEUE_RE='(unless (you )?(redirect|tell me otherwise|stop me|say otherwise|prefer|want|need|push back)|unless (redirected|told otherwise|stopped)|i.?ll [a-z]+ [^.]*? unless|going to [a-z]+ [^.]*? unless|will [a-z]+ [^.]*? unless you)'

COND_QUEUE_MATCH=0
if echo "$LAST_PARA" | grep -qiE "$COND_QUEUE_RE"; then
  COND_QUEUE_MATCH=1
fi

# Context gate (relaxed 2026-05-26 after T1.4 smoke-test miss):
# The conditional-queue phrase itself is the reliable signal. The earlier
# context-gate using NEXT_L4_RE required specific "will write / next L4"
# keywords that the "Recommend starting with L4 #N ... unless you redirect"
# variant didn't contain, so T1.4 slipped past CHECK 4.
#
# Relaxed approach: fire on COND_QUEUE_MATCH alone, gated only by absence
# of a dispatch in the same turn (the dispatch gate is the genuine
# false-positive filter — if you actually executed/dispatched, the
# conditional-queue framing is a description of what you did, not a queue).
#
# Additional gate (added 2026-05-28): recommendation-with-reveal exemption.
# "Unless you prefer B because [reason]" is the REQUIRED recommendation-with-
# reveal form per decisioning-discipline rule 6. It is not a conditional queue.
# Distinguish by requiring a recommendation marker AND the "unless you prefer"
# appearing as a reveal in a recommendation-with-reveal structure.
# Pattern: REC_MATCH + "unless you.?d? prefer" — the "prefer" variant of
# "unless" is the recommendation-reveal form; "redirect/tell me/stop me/say
# otherwise" variants are the conditional-queue form.
C4_REC_REVEAL_RE='unless you.?d? prefer'
C4_HAS_REC_REVEAL=0
if [ "$REC_MATCH" = "1" ]; then
  if echo "$LOWER_FULL" | grep -qiE "$C4_REC_REVEAL_RE"; then
    C4_HAS_REC_REVEAL=1
  fi
fi

COND_QUEUE_TRIGGER=0
if [ "$COND_QUEUE_MATCH" = "1" ] && [ "$HAS_DISPATCH" = "0" ] && [ "$C4_HAS_REC_REVEAL" = "0" ]; then
  COND_QUEUE_TRIGGER=1
fi

if [ "$COND_QUEUE_TRIGGER" = "1" ]; then
  echo "[$TIMESTAMP] CHECK4-CAUGHT session=$SESSION_ID cond_queue=1 next_l4=1 dispatch=0 tail='$(printf '%s' "$LAST_PARA" | tail -c 300 | tr '\n' ' ' | tr "'" '_')'" >> "$AUDIT_LOG"

  cat <<'EOF'
{"decision": "block", "reason": "AUTONOMY-GRANT DRIFT (Layer 4 / CHECK 4 — conditional-queue framing on pre-authorized continuation, v3): your response describes a next L4 action AND ends with conditional-queue phrasing ('unless you redirect', 'I'll X next unless', 'going to X unless'). A recommendation marker preceding this tail does NOT redeem it — this is architecturally equivalent to bare-choice on pre-authorized work, just dressed up as a recommendation-with-veto. Pattern documented in SIG-2026-05-26-autonomy-grant-drift-recurrence-in-session.md. 4-gate check: if the next action is reversible, Workspaces-local, has precedent, and has no info gap — EXECUTE it in this same turn. Do not queue. Do not ask. Do not offer a veto. Dispatch the next L4 work now, or surface the specific L0 gate that blocks execution (external comms, money, NDA boundary, force-push-to-main, or reviewers-waiting)."}
EOF
  exit 0
fi

# ---------------------------------------------------------------------------
# CHECK 5: Implicit-queue / standby framing (v4 — 2026-05-28)
#
# Slips past CHECK 1-4 because it contains no explicit question mark, no
# "want me to", no "unless you redirect" — it simply positions the model
# as *waiting* for Brien's word before acting on already-authorized L4 work.
#
# Canonical forbidden phrases (from feedback_pause_drift_meta_signal_on_nudge
# §Forbidden phrasings and SIG-2026-05-27-* signals):
#   "ready to execute when you say go"
#   "ready when you are" / "ready when ready"
#   "let me know when"
#   "say the word"
#   "standing by"
#   "I'll wait for your call"
#   "let me know if you want me to"  (with action verb — see false-positive gate)
#   "when you're ready"
#   "next steps depend on"           (when framing L4-eligible continuation)
#
# False-positive gate: conversational closers that are acceptable at L2+
# surfaces ("let me know if you have any questions", "if there's anything
# else I can help with") are distinguished by the presence of "questions" /
# "anything else" / "if I missed" / "help" WITHOUT an action verb after
# "let me know". The gate strips those before testing the queue phrases.
#
# The dispatch gate from CHECKs 2/4 applies here too: if the response
# already dispatched a concrete action, standby phrasing is contextual
# narrative, not queuing.
#
# Spec: SIG-2026-05-28-stop-hook-regex-extension-implicit-queue.md
# Sources: 4x SIG-2026-05-27-pause-drift-* signals
# ---------------------------------------------------------------------------

# Core implicit-queue phrases (gated by dispatch + false-positive filter below)
IMPLICIT_QUEUE_RE='(ready to (execute|proceed|start|run|go|begin|dispatch) when (you say (go|the word)|you.?re ready|ready)|ready when you.?re ready|ready when you are|ready when ready|let me know when (you.?re ready|you are ready|you want|you need|to proceed|to start|you.?d like)|say the word|standing by (for|to|—|and |until|when)|i.?ll wait (for your|for you|for brien|until you)|waiting (for your|for you|for brien|until you) (go-ahead|say|word|signal|call|input|direction|okay|ok\b|approval)|next steps depend on (your|brien|the decision|what you|whether you|if you|you)|(let me know|tell me) if you want me to [a-z]|(let me know|tell me) when you.?re ready to proceed|(when you.?re ready|whenever you.?re ready|when you are ready)[,.]?\s*(i.?ll|we.?ll|just|go ahead|proceed|start|run|begin|execute|dispatch))'

# False-positive exclusion: acceptable L2 conversational close forms.
# "let me know if you have any questions", "if there's anything else",
# "let me know if you'd like me to elaborate", etc. are NOT implicit queues.
FP_ACCEPTABLE_CLOSE_RE='(let me know if (you have|there.?s|you.?d like (me to )?elaborate|you need (anything|more)|i (missed|can clarify|can help))|if there.?s anything (else|more)|any questions|anything else i can (help|do|clarify|address))'

# Check: does the last paragraph contain an implicit-queue phrase?
IMPLICIT_QUEUE_MATCH=0
if echo "$LOWER_PARA" | grep -qiE "$IMPLICIT_QUEUE_RE"; then
  IMPLICIT_QUEUE_MATCH=1
fi

# Apply false-positive gate: if the only match of IMPLICIT_QUEUE_RE is inside
# a sentence that also contains an acceptable conversational close, suppress.
# Strategy: check the LOWER_PARA for the acceptable-close pattern; if both
# the queue phrase and the close phrase appear in close proximity (same
# ~200-char window), treat as false positive.
#
# Note: "let me know if you have any questions" style closers contain
# "let me know" which is also in IMPLICIT_QUEUE_RE — but they always pair
# with "questions" / "anything else" / "if you need". The FP gate ensures
# those legitimate L2 closers are not blocked.
FP_SUPPRESSED=0
if [ "$IMPLICIT_QUEUE_MATCH" = "1" ]; then
  # Check: does the para ONLY match because of a benign close phrase?
  # Remove benign close phrases, then re-check.
  STRIPPED_PARA=$(printf '%s' "$LOWER_PARA" | sed -E \
    -e 's/let me know if you have[^.!?]*/[STRIPPED]/g' \
    -e 's/if there.s anything else[^.!?]*/[STRIPPED]/g' \
    -e 's/anything else i can[^.!?]*/[STRIPPED]/g' \
    -e 's/any questions[^.!?]*/[STRIPPED]/g' \
    -e 's/if i (missed|can clarify|can help)[^.!?]*/[STRIPPED]/g' \
    -e 's/let me know if you.d like[^.!?]*/[STRIPPED]/g' \
    -e 's/let me know if you need (anything|more)[^.!?]*/[STRIPPED]/g' \
  )
  # If the queue pattern no longer matches after stripping, it was a false positive
  if ! echo "$STRIPPED_PARA" | grep -qiE "$IMPLICIT_QUEUE_RE"; then
    FP_SUPPRESSED=1
  fi
fi

IMPLICIT_QUEUE_TRIGGER=0
if [ "$IMPLICIT_QUEUE_MATCH" = "1" ] && [ "$FP_SUPPRESSED" != "1" ] && [ "$HAS_DISPATCH" = "0" ]; then
  IMPLICIT_QUEUE_TRIGGER=1
fi

# CHECK 5 telemetry append (implicit_queue fields)
printf '{"ts":"%s","session":"%s","check":"5","implicit_queue_match":%d,"fp_suppressed":%d,"dispatch":%d,"trigger":%d,"tail":"%s"}\n' \
  "$TIMESTAMP" "$SESSION_ID" "$IMPLICIT_QUEUE_MATCH" "$FP_SUPPRESSED" "$HAS_DISPATCH" "$IMPLICIT_QUEUE_TRIGGER" \
  "$TAIL_SAMPLE" >> "$TELEMETRY_LOG" 2>/dev/null || true

if [ "$IMPLICIT_QUEUE_TRIGGER" = "1" ]; then
  echo "[$TIMESTAMP] CHECK5-CAUGHT session=$SESSION_ID implicit_queue=1 fp_suppressed=0 dispatch=0 tail='$(printf '%s' "$LAST_PARA" | tail -c 300 | tr '\n' ' ' | tr "'" '_')'" >> "$AUDIT_LOG"

  cat <<'EOF'
{"decision": "block", "reason": "AUTONOMY-GRANT DRIFT (Layer 4 / CHECK 5 — implicit-queue / standby framing, v4): your response contains a phrase that positions you as waiting for Brien's word before acting on already-authorized L4 work. Caught patterns include: 'ready to execute when you say go', 'let me know when', 'ready when you are', 'say the word', 'standing by', 'I'll wait for your call', 'let me know if you want me to [verb]', 'when you're ready', 'next steps depend on...'. These are structurally equivalent to bare-choice queuing even without a question mark. Documented in SIG-2026-05-27-pause-drift-* (4 incidents 2026-05-27) and SIG-2026-05-28-stop-hook-regex-extension-implicit-queue.md. 4-gate check: if the next action is reversible, Workspaces-local, has precedent, and has no info gap — EXECUTE it in this same turn. Do not standby. Do not wait. Do not frame yourself as ready-but-paused. Dispatch now, or name the specific L0 gate blocking execution (external comms to another human, money movement, NDA boundary, force-push-to-main)."}
EOF
  exit 0
fi

# ---------------------------------------------------------------------------
# CHECK 6: Trailing-observation-after-proposal (v5 — 2026-05-28)
#
# Catches the "deliver a polished proposal/recommendation then stop at a
# closing analytical sentence" drift class. The closing sentence makes the
# response feel complete when execution is the actual next step.
#
# Incident source: SIG-2026-05-27-pause-drift-cross-reference-sweep-after-
# prompt-rework — "stopped at a closing comment about delta-from-original"
# ("The biggest delta from the original prompt is that it bypasses Cortège.")
# No forbidden keyword from CHECK 5 appeared; drift was purely positional.
#
# Trigger phrases (anchored to LAST_TAIL — last 400 chars):
#   "the biggest (delta|difference|change|shift|gap) (from|with|between|compared)"
#   "the most (interesting|notable|striking|important|significant) (aspect|part|thing|point)"
#   "worth noting (that|:)"  /  "notable:"  /  "of note:"
#   "one (observation|thing to watch|thing to note|thing worth noting)"
#   "the key insight (here |is )"
#   "it.s worth (pointing out|noting|flagging)"
#
# CONSERVATIVE design: anchor is last 400 chars, not 1000. False-positive rate
# is the primary risk. Four stacked gates reduce noise aggressively.
#
# Four false-positive gates (ANY gate pass = CHECK 6 suppressed):
#   (a) Dispatch gate: HAS_DISPATCH=1 (concrete action dispatched this turn)
#   (b) Closure-DoD gate: response contains the three-assertion closure framing
#       (upstream_control_path + catch_mechanism + pipeline_survival)
#   (c) Recommendation-with-reveal gate: RECOMMENDATION_RE matched AND tail
#       contains "unless you prefer" / "unless you'd prefer" / "alternatively"
#       — indicates an active L2 decision surface, not a trailing observation
#   (d) L2-info-gap gate: response contains "info gap:" / "l2 decision" /
#       "brien needs to decide" / "l2 item" — legitimate decision surfacing
#
# Spec: SIG-2026-05-28-stop-hook-check-6-trailing-observation.md
# ---------------------------------------------------------------------------

# Tight anchor: last 400 chars (more conservative than CHECK 5's 1000)
LAST_TAIL=$(printf '%s' "$LAST_TEXT" | tail -c 400)
LOWER_TAIL=$(printf '%s' "$LAST_TAIL" | tr '[:upper:]' '[:lower:]')

# Trailing-observation trigger phrases
# Note: "notable:" and "of note:" do NOT require ^ (start-of-line) — they can
# appear mid-paragraph as sentence starters. "worth noting" followed immediately
# by ":" (no space) is handled by "worth noting[: ]" pattern.
TRAILING_OBS_RE='(the biggest (delta|difference|change|shift|gap) (from|with|between|compared to)|the most (interesting|notable|striking|important|significant) (aspect|part|thing|point|piece)|worth noting[: ]|worth noting that|notable:|of note:|one (observation|thing to watch|thing to note|thing worth noting)|the key insight (here |is )|it.s worth (pointing out|noting|flagging))'

TRAILING_OBS_MATCH=0
if echo "$LOWER_TAIL" | grep -qiE "$TRAILING_OBS_RE"; then
  TRAILING_OBS_MATCH=1
fi

# Gate (b): Closure-DoD gate — all three closure assertions present in full text
CLOSURE_DOD_RE='upstream_control_path:'
CLOSURE_CATCH_RE='catch_mechanism:'
CLOSURE_SURVIVAL_RE='pipeline_survival:'

HAS_CLOSURE_DOD=0
if echo "$LOWER_FULL" | grep -qiE "$CLOSURE_DOD_RE" && \
   echo "$LOWER_FULL" | grep -qiE "$CLOSURE_CATCH_RE" && \
   echo "$LOWER_FULL" | grep -qiE "$CLOSURE_SURVIVAL_RE"; then
  HAS_CLOSURE_DOD=1
fi

# Gate (c): Recommendation-with-reveal gate
# Recommendation marker already computed as REC_MATCH.
# Check for the "reveal" half: "unless you prefer" / "alternatively" in the full text.
REC_REVEAL_RE='(unless you.?d? prefer|unless you would prefer|alternatively[,.])'

HAS_REC_REVEAL=0
if [ "$REC_MATCH" = "1" ]; then
  if echo "$LOWER_FULL" | grep -qiE "$REC_REVEAL_RE"; then
    HAS_REC_REVEAL=1
  fi
fi

# Gate (d): L2-info-gap gate
L2_INFOGAP_RE='(info gap:|l2 decision|brien needs to decide|l2 item[^s])'

HAS_L2_INFOGAP=0
if echo "$LOWER_FULL" | grep -qiE "$L2_INFOGAP_RE"; then
  HAS_L2_INFOGAP=1
fi

# CHECK 6 fires only when: trailing-obs match AND none of the four gates pass
TRAILING_OBS_TRIGGER=0
if [ "$TRAILING_OBS_MATCH" = "1" ] && \
   [ "$HAS_DISPATCH" = "0" ] && \
   [ "$HAS_CLOSURE_DOD" = "0" ] && \
   [ "$HAS_REC_REVEAL" = "0" ] && \
   [ "$HAS_L2_INFOGAP" = "0" ]; then
  TRAILING_OBS_TRIGGER=1
fi

# CHECK 6 telemetry
printf '{"ts":"%s","session":"%s","check":"6","trailing_obs_match":%d,"dispatch":%d,"closure_dod":%d,"rec_reveal":%d,"l2_infogap":%d,"trigger":%d,"tail":"%s"}\n' \
  "$TIMESTAMP" "$SESSION_ID" "$TRAILING_OBS_MATCH" "$HAS_DISPATCH" "$HAS_CLOSURE_DOD" "$HAS_REC_REVEAL" "$HAS_L2_INFOGAP" "$TRAILING_OBS_TRIGGER" \
  "$(printf '%s' "$LAST_TAIL" | tail -c 200 | tr '\n' ' ' | tr '"' "'" | tr '\' '/')" >> "$TELEMETRY_LOG" 2>/dev/null || true

if [ "$TRAILING_OBS_TRIGGER" = "1" ]; then
  echo "[$TIMESTAMP] CHECK6-CAUGHT session=$SESSION_ID trailing_obs=1 dispatch=0 closure_dod=0 rec_reveal=0 l2_infogap=0 tail='$(printf '%s' "$LAST_TAIL" | tail -c 300 | tr '\n' ' ' | tr "'" '_')'" >> "$AUDIT_LOG"

  cat <<'EOF'
{"decision": "block", "reason": "AUTONOMY-GRANT DRIFT (Layer 4 / CHECK 6 — trailing-observation-after-proposal, v5): your response delivered a diagnosis/recommendation/analysis/artifact and stopped at a trailing analytical sentence (e.g., 'The biggest delta from the original...', 'Worth noting:', 'The most interesting aspect...', 'The key insight here is...'). This is the same drift class as bare-choice on pre-authorized work — just in dress-clothes. The closing observation makes the response feel complete when execution is the actual next step. Source incident: SIG-2026-05-27-pause-drift-cross-reference-sweep-after-prompt-rework. Fix: if the 4-gate check passes for the next action (reversible, local, precedented, no-info-gap), EXECUTE it in this same turn. Closing observations are only legitimate when (a) a concrete action was dispatched in this turn, (b) you have closure-DoD assertions (upstream_control_path / catch_mechanism / pipeline_survival), (c) you are actively surfacing an L2 decision with recommendation-and-reveal, or (d) you have named an explicit info gap. If none of those apply — dispatch."}
EOF
  exit 0
fi

exit 0
