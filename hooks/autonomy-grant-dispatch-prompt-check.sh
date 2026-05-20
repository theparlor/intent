#!/usr/bin/env bash
# autonomy-grant-dispatch-prompt-check.sh
#
# PreToolUse hook — fires BEFORE an Agent (subagent) dispatch.
#
# Enforces: dispatch prompts may NOT inject proposal-framing into L4-eligible
# reversible work. Pattern-match catches verbatim variants of the drift vector
# documented in SIG-PROCESS-DRIFT-PR-STYLE-REVIEW-2026-05-19:
#
#   "Brien is the decider — your answers are PROPOSALS, not closures."
#   "Use `status: proposed`, not `status: ratified`."
#   "propose answers" / "for Brien's review" style framing
#
# If the drift pattern is detected WITHOUT an explicit override token, the hook
# blocks the dispatch and demands correction.
#
# Override token (line anywhere in the dispatch prompt):
#   # AUTONOMY-OVERRIDE-PROPOSAL-FRAMING-INTENTIONAL: <one-line-justification>
#
# Spec: Core/frameworks/intent/spec/autonomy-grant-enforcement.md (Layer 5)
# Signal: SIG-PROCESS-DRIFT-PR-STYLE-REVIEW-2026-05-19.md (§ structural-prevention-candidates)
# Sibling: Core/frameworks/intent/hooks/autonomy-grant-stop-check.sh (Stop hook)
#
# Install:
#   chmod +x Core/frameworks/intent/hooks/autonomy-grant-dispatch-prompt-check.sh
#   ln -s "$PWD/Core/frameworks/intent/hooks/autonomy-grant-dispatch-prompt-check.sh" \
#         ~/.claude/hooks/autonomy-grant-dispatch-prompt-check.sh
#
# Register: add to ~/.claude/settings.json under hooks → PreToolUse → matcher "Agent"
#
# Bypass: AUTONOMY_GRANT_DISPATCH_BYPASSED=1 (logged to audit)
# Audit log: ~/.claude/audit/autonomy-grant-dispatch-detections.log
#
# Created: 2026-05-19 — Layer 5 per SIG-PROCESS-DRIFT-PR-STYLE-REVIEW-2026-05-19
#   structural-prevention candidate #1; sibling to Stop hook (Layers 3/4).

set -u

AUDIT_LOG="$HOME/.claude/audit/autonomy-grant-dispatch-detections.log"
mkdir -p "$(dirname "$AUDIT_LOG")" 2>/dev/null || true

# Bypass
if [ "${AUTONOMY_GRANT_DISPATCH_BYPASSED:-0}" = "1" ]; then
  TIMESTAMP=$(date -u +%Y-%m-%dT%H:%M:%SZ)
  echo "[$TIMESTAMP] BYPASS env-flag set" >> "$AUDIT_LOG"
  exit 0
fi

# Read tool input JSON from stdin
INPUT=$(cat)

# Extract session_id, tool_name, and prompt via python3 (robust JSON parsing)
read -r SESSION_ID TOOL_NAME <<< "$(python3 -c "
import json, sys
try:
    d = json.loads(sys.stdin.read() or '{}')
    sid = d.get('session_id', 'unknown')
    tname = d.get('tool_name', '')
    print(sid, tname)
except Exception:
    print('unknown', '')
" <<< "$INPUT")"

# Extract full prompt separately (may contain newlines; handled via python stdout)
PROMPT=$(python3 -c "
import json, sys
try:
    d = json.loads(sys.stdin.read() or '{}')
    prompt = d.get('tool_input', {}).get('prompt', '')
    print(prompt)
except Exception:
    print('')
" <<< "$INPUT" 2>/dev/null)

# Only inspect Agent tool dispatches
if [ "$TOOL_NAME" != "Agent" ]; then
  exit 0
fi

# No prompt → pass (defensive fail-open)
if [ -z "$PROMPT" ]; then
  exit 0
fi

# Override token — any line matching this pattern suppresses the hook
OVERRIDE_TOKEN="AUTONOMY-OVERRIDE-PROPOSAL-FRAMING-INTENTIONAL:"
if echo "$PROMPT" | grep -qF "$OVERRIDE_TOKEN"; then
  TIMESTAMP=$(date -u +%Y-%m-%dT%H:%M:%SZ)
  EXCERPT=$(echo "$PROMPT" | grep -F "$OVERRIDE_TOKEN" | head -1 | cut -c1-200)
  echo "[$TIMESTAMP] OVERRIDE session=$SESSION_ID token='$EXCERPT'" >> "$AUDIT_LOG"
  exit 0
fi

# ---------------------------------------------------------------------------
# Proposal-framing detection
#
# Match ANY of these phrases (case-insensitive) in the dispatch prompt:
#   1. Exact verbatim drift phrase
#   2. status: proposed (with or without backticks/spaces)
#   3. "propose answers" / "propose your answers" / "propose a"
#   4. "for Brien's review" / "for brien review" / "for review by Brien"
#   5. "Brien is the decider"
#   6. "answers are PROPOSALS" / "responses are proposals"
# ---------------------------------------------------------------------------

PROMPT_LOWER=$(printf '%s' "$PROMPT" | tr '[:upper:]' '[:lower:]')

MATCHED=0
MATCHED_PHRASE=""

# Pattern list (lowercase — matched against PROMPT_LOWER)
PATTERNS=(
  "brien is the decider"
  "your answers are proposals"
  "responses are proposals"
  "answers are proposals"
  "status: proposed"
  "status:proposed"
  "\`status: proposed\`"
  "not closures"
  "propose answers"
  "propose your answers"
  "for brien'?s review"
  "for review by brien"
  "brien to review"
  "brien to approve"
  "brien to decide"
  "submit for review"
  "propose .{0,60} not ratif"
  "proposed, not ratified"
  "proposals, not closures"
)

for pat in "${PATTERNS[@]}"; do
  if echo "$PROMPT_LOWER" | grep -qiE "$pat" 2>/dev/null; then
    MATCHED=1
    MATCHED_PHRASE="$pat"
    break
  fi
done

if [ "$MATCHED" = "0" ]; then
  exit 0  # Clean — no proposal-framing detected
fi

# ---------------------------------------------------------------------------
# BLOCK: proposal-framing detected without override token
# ---------------------------------------------------------------------------

TIMESTAMP=$(date -u +%Y-%m-%dT%H:%M:%SZ)
EXCERPT=$(printf '%s' "$PROMPT" | head -c 300 | tr '\n' ' ' | tr '"' "'" | tr '\' '/')

echo "[$TIMESTAMP] CAUGHT session=$SESSION_ID pattern='$MATCHED_PHRASE' excerpt='$EXCERPT'" >> "$AUDIT_LOG"

cat <<EOF
{"decision": "block", "reason": "AUTONOMY-GRANT DRIFT (Layer 5 — dispatch-prompt check): this Agent dispatch prompt injects proposal-framing ('$MATCHED_PHRASE') into subagent work. Pattern origin: SIG-PROCESS-DRIFT-PR-STYLE-REVIEW-2026-05-19 — verbatim drift vector was 'Brien is the decider — your answers are PROPOSALS, not closures. Use status: proposed, not status: ratified.' This converts L4 autonomous work into L0 review-by-Brien work — exactly inverse of the autonomy grant. Correction: (1) run the 4-gate check (reversible? local? precedent? no info gap?); (2) if all 4 pass, rewrite the prompt to instruct the subagent to EXECUTE + SIGNAL with status: ratified; (3) only if a specific gate fails, name that gate explicitly rather than defaulting to proposal-framing. Override if EITHER (a) this is genuinely L0 external work, OR (b) the prompt is meta-instructional content that catalogs the anti-pattern as documented learning (playbook, drift catalog, template showing what NOT to do, post-mortem signal) — add a comment line '# AUTONOMY-OVERRIDE-PROPOSAL-FRAMING-INTENTIONAL: <one-line-justification>' anywhere in the prompt. Spec: Core/frameworks/intent/spec/autonomy-grant-enforcement.md Layer 5."}
EOF

exit 2
