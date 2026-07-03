#!/usr/bin/env bash
# autonomy-posture-check-layer-4.2.sh
#
# Stop hook — Layer 4.2 of autonomy-grant enforcement (STRUCTURAL detector).
#
# WARN-ONLY MODE. This hook NEVER emits a block decision. It always lets the
# response pass (exit 0, no {"decision":"block"} output). When it detects a
# case it WOULD have blocked in block-mode, it logs that fact to telemetry and
# to a human-readable detections log. Promotion to block-mode is a separate,
# Brien-gated event after the 14-day calibration window shows FP rate < 5%.
#
# WHAT IT CHECKS (positive-execution posture, per spec §2.2-§2.4 and §3):
#   Instead of matching forbidden phrases (the lexical CHECKs 1-7 in
#   autonomy-grant-stop-check.sh, now frozen per lexical-layer-freeze.yaml),
#   Layer 4.2 verifies a POSITIVE property: when the response describes a
#   "next L4 action" AND the 4-gate heuristic passes for it, the action MUST
#   have been executed within the same turn (a corresponding tool_use block).
#
#   The "would-block" case is:
#     next-action claim (NEXT_ACTION_RE) detected in last assistant text
#     AND the cheap 4-gate heuristic (§2.3) passes
#     AND NO tool_use block in the same turn corresponds to the claim (§2.4)
#
# WHY STRUCTURAL: each new lexical CHECK was a reaction to a NEW linguistic
# drift variant. Caution-bias generates variants faster than regex catches
# them (spec §1). The convergent closure is structural — verify the property,
# don't enumerate the phrasings.
#
# Spec:    Core/frameworks/intent/spec/autonomy-posture-check-layer-4.2-DRAFT.md
# Freeze:  Core/frameworks/intent/hooks/lexical-layer-freeze.yaml (successor_path)
# Mirror:  Core/frameworks/intent/hooks/autonomy-grant-stop-check.sh (conventions)
#
# Install: chmod +x and symlink to ~/.claude/hooks/ (parent wires settings.json)
# Register: add Stop entry to ~/.claude/settings.json (matcher "*")
#
# Bypass:     AUTONOMY_POSTURE_L42_BYPASSED=1  (exit early, silent)
# Telemetry:  ~/.claude/logs/autonomy-posture-layer42.jsonl (one line per Stop)
# Detections: ~/.claude/audit/autonomy-posture-layer42-detections.log (would-block only)
#
# Created: 2026-05-29 — warn-only scaffold per road-readiness rollout replacing
#   the frozen lexical layer with the structural successor (Layer 4.2).

set -u

AUDIT_LOG="$HOME/.claude/audit/autonomy-posture-layer42-detections.log"
TELEMETRY_LOG="$HOME/.claude/logs/autonomy-posture-layer42.jsonl"
mkdir -p "$(dirname "$AUDIT_LOG")" 2>/dev/null || true
mkdir -p "$(dirname "$TELEMETRY_LOG")" 2>/dev/null || true

# Bypass
if [ "${AUTONOMY_POSTURE_L42_BYPASSED:-0}" = "1" ]; then
  exit 0
fi

# Read input JSON from stdin
INPUT=$(cat)

# Parse input defensively (fail open). Single-line space-separated output.
# Mirrors autonomy-grant-stop-check.sh exactly.
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

# No transcript → exit gracefully (fail open)
if [ "$TRANSCRIPT_PATH" = "NONE" ] || [ ! -f "$TRANSCRIPT_PATH" ]; then
  exit 0
fi

# ---------------------------------------------------------------------------
# Structural analysis — embedded python3 (like the existing hook).
#
# Emits a single line of space-separated fields on stdout for the bash layer
# to consume, plus pre-formatted JSON/audit payloads on dedicated markers.
# The python NEVER prints a block decision — warn-only is enforced here AND in
# the bash layer (which only ever appends logs and exits 0).
#
# Output protocol (one line each, prefixed):
#   RESULT <would_block> <gates_pass> <has_tool_use>
#   NEXTACTIONS <json-array>
#   TAIL <json-string>
#
# Fail-open: any exception → print nothing → bash treats as silent pass.
# ---------------------------------------------------------------------------
ANALYSIS=$(python3 - "$TRANSCRIPT_PATH" <<'PY' 2>/dev/null
import json, sys, re

def emit_silent():
    # Print a well-formed "nothing detected" result so the bash layer can log
    # baseline telemetry even when there's no next-action claim.
    print("RESULT 0 0 0")
    print("NEXTACTIONS []")
    print("TAIL \"\"")
    sys.exit(0)

try:
    path = sys.argv[1]
except Exception:
    emit_silent()

# --- Parse transcript JSONL: find the LAST assistant message ----------------
last_assistant = None
try:
    with open(path) as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                obj = json.loads(line)
            except Exception:
                continue
            if obj.get("type") == "assistant":
                last_assistant = obj
except Exception:
    emit_silent()

if not last_assistant:
    emit_silent()

# --- Extract text + tool_use from the last assistant message ----------------
# Per spec §3 reference implementation: LAST_TEXT from text blocks, LAST_TOOLS
# from tool_use blocks of the last assistant message.
LAST_TEXT = ""
LAST_TOOLS = []

def harvest(msg):
    txt = ""
    tools = []
    content = msg.get("content", [])
    if isinstance(content, str):
        txt += content + "\n"
    elif isinstance(content, list):
        for block in content:
            if isinstance(block, dict):
                if block.get("type") == "text":
                    txt += block.get("text", "") + "\n"
                elif block.get("type") == "tool_use":
                    tools.append(block)
    return txt, tools

try:
    msg = last_assistant.get("message", {}) or {}
    LAST_TEXT, LAST_TOOLS = harvest(msg)
except Exception:
    emit_silent()

# Same-turn tool_use augmentation (spec §2.4 step 1: "AFTER the last assistant
# text message (or in the same message) ... or within the prior N assistant
# messages, since execution typically happens in the SAME turn"). The §3
# reference impl only reads the last message; we additionally collect tool_use
# blocks from a short trailing window of assistant messages so that the common
# pattern (tool_use in one assistant turn, then a final text-only summary turn)
# is still credited as same-turn execution. This is a documented deviation that
# REDUCES would-block false positives; it never adds them.
TURN_TOOLS = list(LAST_TOOLS)
try:
    WINDOW = 6  # trailing assistant messages to scan for same-turn tool_use
    assistant_msgs = []
    with open(path) as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                obj = json.loads(line)
            except Exception:
                continue
            if obj.get("type") == "assistant":
                assistant_msgs.append(obj)
    for obj in assistant_msgs[-WINDOW:]:
        _, t = harvest(obj.get("message", {}) or {})
        TURN_TOOLS.extend(t)
except Exception:
    # If the window scan fails, fall back to LAST_TOOLS only — still fail-open.
    TURN_TOOLS = list(LAST_TOOLS)

if not LAST_TEXT:
    emit_silent()

# --- §2.2 Next-action claim detection ---------------------------------------
NEXT_ACTION_RE = re.compile(
    r"(I'?ll|will|going to|next (move|step|L4|action)) "
    r"(write|run|build|execute|deploy|do|start|draft|capture|file|commit|push|"
    r"extract|apply|configure|register|wire) "
    r"([a-zA-Z][a-zA-Z0-9_./-]*)",
    re.IGNORECASE
)
matches = NEXT_ACTION_RE.findall(LAST_TEXT)

# --- §2.2b Grammatical-class exclusion (closed class, not a growing phrase list) ---
# The extractor grabs a single word after the verb ("I'll run TARGET"). When the
# grammatical object is a pronoun/quantifier/preposition/determiner ("that", "each",
# "all", "with"), the regex still matches, but there is no concrete noun to
# tool-use-cross-reference — the real referent is elsewhere in the sentence (anaphora)
# or the construction is a compliant recommendation-with-reveal, not a deferred action.
# Closed grammatical class, not an enumerated phrase list: adding a word here does not
# reproduce the CHECK-1-through-7 whack-a-mole (root cause: lexical-layer-freeze.yaml),
# because pronouns/quantifiers/prepositions/determiners are a fixed, small part-of-speech
# set, not an open-ended catalogue of ways to phrase hedging.
# Provenance: SIG-2026-06-12-layer42-calibration-review.md + SIG-2026-06-28-flight-model-
# 30day-ratification-readiness.md identified 8 of 9 historical fires as this class
# ("each","that"x3,"all","with"x2,"those."); re-verified against the live jsonl log on
# 2026-07-03 (Core/frameworks/intent/spec/2026-07-03-autonomy-grant-pause-drift-audit.md).
# NOT COVERED: a real noun target (e.g. "team-configs") is NOT filtered here — it stays
# a would-block candidate. Whether that class is a true or false positive is a Gate-4
# semantic question (does the surrounding sentence read as recommendation-with-reveal?),
# which gate_no_info_gap below does not yet detect. That gap is open, not silently
# patched — see the audit doc §2 root cause 3 and §7 Phase 2.
STOPWORD_TARGETS = {
    # pronouns
    "it", "this", "that", "these", "those", "them", "they", "he", "she", "we", "you", "i",
    # quantifiers / determiners
    "each", "all", "any", "some", "none", "both", "either", "neither", "other", "another",
    "the", "a", "an",
    # prepositions
    "with", "without", "for", "from", "to", "of", "in", "on", "at", "by", "as", "into", "onto",
    # conjunctions
    "and", "or", "but", "if", "so", "then",
}

# Full-text sample (bounded only against pathological input, not a fixed analysis
# window) for telemetry/audit. 2026-07-03: was LAST_TEXT[-200:]. Cross-model review
# (SIG-2026-07-03-layer42-recall-unmeasured.md) found the 200-char tail is a lossy
# summary that discards claim-bearing text earlier in the message, and that 194/231
# of the session transcripts backing this hook's sibling audit log have already
# rotated off disk, meaning a truncated log line is often the ONLY surviving record.
# session_id is a durable pointer only as long as transcripts are retained; this repo
# has already lost 84% of them within weeks. Log full text here so retrospective
# recall/precision analysis never depends on transcript survival.
tail_raw = LAST_TEXT[-8000:].replace("\n", " ").replace("\r", " ")
tail_json = json.dumps(tail_raw)

if not matches:
    # No next-action claim → silent (but still emit baseline telemetry).
    print("RESULT 0 0 %d" % (1 if TURN_TOOLS else 0))
    print("NEXTACTIONS []")
    print("TAIL %s" % tail_json)
    sys.exit(0)

# --- §2.4 Same-turn tool_use cross-reference --------------------------------
# Strong match: a tool_use input field (file_path / command / prompt / others)
# contains a substring of the next-action target N.
# Weak match: tool exists targeting the same implied scope. We approximate the
# weak tier by also testing the action TARGET token against all stringy values
# of the tool input. A weak match passes; only "none" is would-block-eligible.
def tool_input_blob(tool):
    ti = tool.get("input", {}) or {}
    parts = []
    if isinstance(ti, dict):
        for v in ti.values():
            if isinstance(v, str):
                parts.append(v)
            else:
                try:
                    parts.append(json.dumps(v))
                except Exception:
                    pass
    elif isinstance(ti, str):
        parts.append(ti)
    return " ".join(parts).lower()

tool_blobs = [tool_input_blob(t) for t in TURN_TOOLS]

unmatched_targets = []
for m in matches:
    action_target = m[3]  # the noun captured by the final group
    if not action_target:
        continue
    # Strip a bare sentence-final period ("those." -> "those"). Does not affect
    # real file-extension targets like "config.yaml", which do not end in ".".
    at = action_target.rstrip(".").lower()
    if at in STOPWORD_TARGETS:
        # Grammatical function word, not a concrete deferred-action target.
        # See §2.2b above. Not tool-use-cross-referenced; not would-block-eligible.
        continue
    matched = False
    for blob in tool_blobs:
        if at and at in blob:
            matched = True
            break
    if not matched:
        unmatched_targets.append(action_target)

has_tool_use = 1 if TURN_TOOLS else 0

# If every claim has a corresponding tool_use → executed, not queued → pass.
if not unmatched_targets:
    # next-action present, but all executed this turn
    na_json = json.dumps([m[3] for m in matches])
    print("RESULT 0 0 %d" % has_tool_use)
    print("NEXTACTIONS %s" % na_json)
    print("TAIL %s" % tail_json)
    sys.exit(0)

# --- §2.3 4-gate heuristic estimator (cheap) --------------------------------
# Only the unmatched claims are candidates. The heuristic asks: did the
# assistant have evidence to act (and not)? Mirrors the spec §3 gate sketch.
low = LAST_TEXT.lower()
head500 = low[:500]
tail1000 = LAST_TEXT[-1000:]

gate_reversible = (
    "workspaces" in low or ".intent" in low or "signal" in low or
    "git " in low or "commit" in low or "theparlor/" in low
)
gate_local_blast = not (
    "slack" in head500 or "email" in head500 or "calendar" in head500 or
    "cross-human" in low
)
gate_precedent = (
    "L4" in LAST_TEXT or "L4-" in LAST_TEXT or "autonomy" in low
)
gate_no_info_gap = not (
    "TBD" in tail1000 or "needs Brien" in tail1000 or
    "Brien decides" in tail1000 or "Brien needs to decide" in tail1000
)

gates_pass = 1 if (gate_reversible and gate_local_blast and gate_precedent and gate_no_info_gap) else 0

# would_block in block-mode == (unmatched next-action claim) AND (gates pass)
# AND (no corresponding tool_use). The "no corresponding tool_use" is already
# encoded by the target being in unmatched_targets.
would_block = 1 if (unmatched_targets and gates_pass == 1) else 0

nextactions_json = json.dumps(unmatched_targets if would_block else [m[3] for m in matches])
print("RESULT %d %d %d" % (would_block, gates_pass, has_tool_use))
print("NEXTACTIONS %s" % nextactions_json)
print("TAIL %s" % tail_json)
sys.exit(0)
PY
)

# Fail open: if python produced nothing (exception / crash), exit silently.
if [ -z "$ANALYSIS" ]; then
  exit 0
fi

# ---------------------------------------------------------------------------
# Parse the python analysis output back into bash variables (defensive).
# ---------------------------------------------------------------------------
RESULT_LINE=$(printf '%s\n' "$ANALYSIS" | grep '^RESULT ' | head -n1)
NEXTACTIONS_JSON=$(printf '%s\n' "$ANALYSIS" | sed -n 's/^NEXTACTIONS //p' | head -n1)
TAIL_JSON=$(printf '%s\n' "$ANALYSIS" | sed -n 's/^TAIL //p' | head -n1)

# RESULT <would_block> <gates_pass> <has_tool_use>
WOULD_BLOCK=$(printf '%s' "$RESULT_LINE" | awk '{print $2}')
GATES_PASS=$(printf '%s' "$RESULT_LINE" | awk '{print $3}')
HAS_TOOL_USE=$(printf '%s' "$RESULT_LINE" | awk '{print $4}')

# Defensive defaults if parsing yielded blanks
WOULD_BLOCK="${WOULD_BLOCK:-0}"
GATES_PASS="${GATES_PASS:-0}"
HAS_TOOL_USE="${HAS_TOOL_USE:-0}"
[ -z "$NEXTACTIONS_JSON" ] && NEXTACTIONS_JSON="[]"
[ -z "$TAIL_JSON" ] && TAIL_JSON="\"\""

TIMESTAMP=$(date -u +%Y-%m-%dT%H:%M:%SZ)

# ---------------------------------------------------------------------------
# Telemetry — one JSON line per Stop event. Mirrors the jsonl style of
# ~/.claude/logs/autonomy-stop-check.jsonl. Always fires (frequency trends).
# ---------------------------------------------------------------------------
printf '{"ts":"%s","session":"%s","would_block":%d,"next_actions":%s,"gates_pass":%d,"has_tool_use":%d,"mode":"warn-only","tail":%s}\n' \
  "$TIMESTAMP" "$SESSION_ID" "$WOULD_BLOCK" "$NEXTACTIONS_JSON" "$GATES_PASS" "$HAS_TOOL_USE" "$TAIL_JSON" \
  >> "$TELEMETRY_LOG" 2>/dev/null || true

# ---------------------------------------------------------------------------
# Human-readable detection log — only when would_block=1. Same shape as
# ~/.claude/audit/autonomy-grant-stop-detections.log:
#   [ts] L42-WOULDBLOCK session=... next=... tail='...'
# ---------------------------------------------------------------------------
if [ "$WOULD_BLOCK" = "1" ]; then
  # Build a sanitized single-quote-safe tail for the audit line (strip the
  # surrounding JSON quotes, collapse newlines, neutralize single quotes).
  AUDIT_TAIL=$(printf '%s' "$TAIL_JSON" | python3 -c "
import sys, json
try:
    s = json.loads(sys.stdin.read())
except Exception:
    s = ''
print(s.replace(chr(10),' ').replace(chr(13),' ').replace(\"'\", '_'))
" 2>/dev/null)
  # Sanitize next-actions for the audit line (single-quote-safe)
  AUDIT_NEXT=$(printf '%s' "$NEXTACTIONS_JSON" | tr '\n' ' ' | tr "'" '_')
  echo "[$TIMESTAMP] L42-WOULDBLOCK session=$SESSION_ID next=$AUDIT_NEXT tail='$AUDIT_TAIL'" >> "$AUDIT_LOG" 2>/dev/null || true
fi

# WARN-ONLY: always pass. Never emit a block decision.
exit 0
