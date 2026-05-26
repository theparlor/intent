#!/usr/bin/env bash
# autonomy-grant-stop-check.sh
#
# Stop hook — Layer 4 of autonomy-grant enforcement (linguistic detector).
#
# Detects two drift patterns and forces revision:
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
# Spec: Core/frameworks/intent/spec/autonomy-grant-enforcement.md (Layer 4)
# Signal: Core/products/org-design-tooling/.intent/signals/SIG-AUTONOMY-DRIFT-POST-STAGE-2026-05-13.md
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

exit 0
