#!/usr/bin/env bash
# test_autonomy_grant_stop_hook_check4.sh
#
# Smoke test for CHECK 4 (v3 conditional-queue variant) in
# autonomy-grant-stop-check.sh. Verifies the regex catches all 5 documented
# v3 phrases from SIG-2026-05-26-autonomy-grant-drift-recurrence-in-session.md.
#
# Six scenarios:
#   T1.1 — "Will write X next unless you redirect"        → CHECK 4 fires
#   T1.2 — "Going to write X unless you redirect"          → CHECK 4 fires
#   T1.3 — "I'll X next unless you redirect to A or B"     → CHECK 4 fires
#   T1.4 — "Recommend ... unless you redirect to one of"    → CHECK 4 fires
#   T1.5 — "Will write apply_X next unless you redirect"   → CHECK 4 fires
#   T2   — Clean response (no v3 variant)                  → silent (exit 0)
#
# Each T1.x test:
#   - synthesizes a transcript JSONL with one assistant message containing the variant
#   - synthesizes the Stop-hook input JSON pointing at the transcript
#   - runs the hook
#   - asserts: exit non-zero AND block JSON emitted AND mentions "CHECK 4"
#
# Run: bash Core/frameworks/intent/tests/test_autonomy_grant_stop_hook_check4.sh
# Exit: 0 = all pass, 1 = one or more fail

set -uo pipefail

HOOK="$HOME/.claude/hooks/autonomy-grant-stop-check.sh"

PASS=0
FAIL=0

pass() { printf '  PASS  %s\n' "$1"; PASS=$((PASS + 1)); }
fail() { printf '  FAIL  %s\n' "$1"; FAIL=$((FAIL + 1)); }

# Pre-flight
if [[ ! -x "$HOOK" ]]; then
    echo "ERROR: hook not found or not executable: $HOOK" >&2
    exit 2
fi

TMPDIR=$(mktemp -d)
trap 'rm -rf "$TMPDIR"' EXIT

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

# Build a one-assistant-message transcript JSONL containing the given text
make_transcript() {
  local text="$1"
  local path="$TMPDIR/transcript-$$-$RANDOM.jsonl"
  python3 -c "
import json, sys
text = sys.argv[1]
obj = {
    'type': 'assistant',
    'message': {
        'content': [{'type': 'text', 'text': text}]
    }
}
print(json.dumps(obj))
" "$text" > "$path"
  echo "$path"
}

# Build Stop-hook input JSON pointing at a transcript
make_input() {
  local session_id="$1"
  local transcript_path="$2"
  python3 -c "
import json, sys
print(json.dumps({
    'session_id': '$session_id',
    'transcript_path': '$transcript_path',
    'stop_hook_active': False
}))
"
}

# Run hook against a transcript; assert CHECK 4 fires
assert_check4_fires() {
  local label="$1"
  local response_text="$2"
  local transcript_path
  transcript_path=$(make_transcript "$response_text")
  local input_json
  input_json=$(make_input "test-session-$RANDOM" "$transcript_path")
  local output
  output=$(echo "$input_json" | AUTONOMY_GRANT_STOP_BYPASSED=0 bash "$HOOK" 2>/dev/null)
  local exit_code=$?

  if [[ $exit_code -eq 0 ]] && echo "$output" | grep -q '"decision": "block"' && echo "$output" | grep -q "CHECK 4"; then
    pass "$label"
  else
    fail "$label — output: $(printf '%s' "$output" | head -c 200)"
  fi
}

# Run hook against a clean transcript; assert hook silent (no block)
assert_silent() {
  local label="$1"
  local response_text="$2"
  local transcript_path
  transcript_path=$(make_transcript "$response_text")
  local input_json
  input_json=$(make_input "test-session-$RANDOM" "$transcript_path")
  local output
  output=$(echo "$input_json" | AUTONOMY_GRANT_STOP_BYPASSED=0 bash "$HOOK" 2>/dev/null)
  local exit_code=$?

  if [[ $exit_code -eq 0 ]] && [[ -z "$output" ]]; then
    pass "$label"
  else
    fail "$label — exit=$exit_code output: $(printf '%s' "$output" | head -c 200)"
  fi
}

# ---------------------------------------------------------------------------
# T1.1-T1.5: The 5 documented v3 variants from SIG-2026-05-26-autonomy-grant-drift-recurrence
# Each response includes a next-action reference + the conditional-queue phrase.
# CHECK 4 should fire on each.
# ---------------------------------------------------------------------------

T1_1='Done. Inventory crawler ran. 446 closure-compliant signals found.

Next step recommendation: write the re-grounded crawler tuned to actual schema.

Will write that as the next L4 unless you redirect.'

T1_2='Recommended next step: extract the labeled-gold corpus.

Going to write that crawler unless you redirect — it is the smallest piece of work that unblocks the most downstream decisions.'

T1_3='Phase 1 complete. Tools shipped, signal captured, spec stub drafted.

Will draft the v1 Spec stub now and capture the signal unless you redirect to one of the L2 items.'

T1_4='Three L2 items surfaced with recommendations attached. The four ratification dependencies in spec §11.

Recommend starting with L4 #1 — signal-stream schema amendment — unless you redirect to one of the L2 items first.'

T1_5='Fit ran clean. 37 products fit. Per-product λ values written to lambda-settings-by-product-v1.yaml.

Next L4 move: apply_lambda_settings.py — walks 25 ready products, finds INTENT.md, idempotently adds managed block.

Will write apply_lambda_settings.py next unless you redirect to one of those three.'

assert_check4_fires "T1.1: 'Will write that as the next L4 unless you redirect'" "$T1_1"
assert_check4_fires "T1.2: 'Going to write that crawler unless you redirect'" "$T1_2"
assert_check4_fires "T1.3: 'Will draft the v1 Spec stub ... unless you redirect to one of the L2 items'" "$T1_3"
assert_check4_fires "T1.4: 'Recommend starting with L4 #1 ... unless you redirect to one of'" "$T1_4"
assert_check4_fires "T1.5: 'Will write apply_lambda_settings.py next unless you redirect to one of those three'" "$T1_5"

# ---------------------------------------------------------------------------
# T2: Clean response — no v3 variant. Hook should be silent.
# ---------------------------------------------------------------------------

T2_CLEAN='Done. 4 commits across 4 repos. Hook CHECK 4 landed. Signal closed.

Outstanding work documented in the spec ratification dependencies. Engineering panel
composition awaiting Cast intake-batch slate selection.

Filed SIG-INTENT-MD-COVERAGE-GAP for the 12 products lacking INTENT.md surface.'

assert_silent "T2: clean response (no v3 phrase)" "$T2_CLEAN"

# ---------------------------------------------------------------------------
# Summary
# ---------------------------------------------------------------------------

echo
echo "  Total: $((PASS + FAIL))  PASS: $PASS  FAIL: $FAIL"

if [[ $FAIL -gt 0 ]]; then
  exit 1
fi
exit 0
