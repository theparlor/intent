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
#
# Updated: 2026-07-19: precision patch. The 2026-07-08..07-18 warn-only
#   calibration window against the widened recall grammar (9c0e6bf) logged 14
#   would-block fires; a full-population manual read (WINDOW-CLOSE READ,
#   Core/products/_intake/2026-07-19-decision-surfaces-retrofit/
#   layer42-calibration-promote-retire.md) classified 3 as true positive, 10
#   as false positive, 1 as an ambiguous swing case. The false positives
#   trace to legitimate-gate misclassification, not the pronoun/stopword
#   mechanism the grammar already fixed. §2.3b below adds a fifth gate that
#   discriminates five named false-positive categories plus one general
#   discriminator (recommendation-with-reveal / already-autonomous framing)
#   found necessary during fixture testing to fully clear the confirmed set.
#   Fixtures: hooks/tests/fixtures/layer42/ (14 real firings, verbatim).
#   Test: hooks/tests/test_layer42_precision.py. Mode is UNCHANGED: still
#   warn-only, still never emits a block decision. This is precision
#   refinement of the detector, not a promotion.

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

# --- §2.2c Deferred-claim grammar (2026-07-03 recall widening) --------------
# NEXT_ACTION_RE only catches the FORWARD-declarative claim shape ("I'll run X").
# The lexical Stop-hook's true-positive corpus (autonomy-grant-stop-detections.log,
# 231 genuine catches) is dominated by three OTHER constructions that NEXT_ACTION_RE
# never matched. Recall against that corpus was 17/231 (7.4%) matched-at-all, and
# only 4/231 (1.7%) survived the §2.2b stopword filter as would-block-eligible
# (SIG-2026-07-03-layer42-recall-unmeasured.md). Widening to these three closed
# grammatical classes raises recall to 178/231 (77.1%). Each class below is a CLOSED
# grammatical construction (a finite syntactic frame keyed on a small fixed token
# set), NOT an open-ended phrase catalogue, so it does not reproduce the
# CHECK-1-through-7 whack-a-mole that motivated lexical-layer-freeze.yaml. The
# standing reviewer objection to the lexical layer ("phrase lists never converge")
# does not apply: you cannot invent a new pronoun, a new subordinating conjunction,
# or a new first-/second-person interrogative-offer opener the way you can invent a
# new way to phrase a hedge sentence. The set of go-signal idioms and question
# frames is bounded by grammar, not by phrasing creativity.
#
# Each new hit yields a SYNTHETIC match tuple shaped exactly like NEXT_ACTION_RE's
# findall() output (4 groups, action-target at index [3]) so it flows unchanged
# through §2.2b stopword filtering, §2.4 tool_use cross-reference, and §2.3 4-gate
# logic below. The target is a CLASS MARKER ("OFFER"/"TRIGGER"/"COND"), not a concrete
# noun, because these constructions defer an action named elsewhere (or offered, not
# yet named). A class marker is intentionally NOT in STOPWORD_TARGETS (it is a real
# deferral, unlike an anaphoric pronoun) and intentionally will not substring-match a
# tool_use blob (a genuine deferral has no same-turn execution), so it correctly
# reaches the 4-gate estimator, which is where would-block eligibility is decided.
#
# CLASS A, interrogative offer (marker "OFFER"). The assistant asks Brien whether to
#   act instead of acting. Ground truth (2026-05-04): "Want me to draft a TSD ticket to
#   Omar requesting the OAuth scope grant, or is the current ticket-queue model the
#   intended steady state?"  Closure: a fixed set of 1st/2nd-person offer openers
#   ("want me to", "should I", "shall I", "would you like me to"). The optional leading
#   "w?" tolerates the logged/truncated "ant me to ..." tail shape.
#   2026-07-03 adversarial-verify trim: the original draft also carried a bare
#   "want (?:me )?to" branch, which collapses to the open bigram "want to" and fired
#   advice-shaped (33/123 telemetry hits: "you might want to review", "teams want to
#   walk in"). Load-bearing test: removing it changed 231-corpus recall by ZERO
#   (178 -> 178). Deleted as the sole open-list leak; only the closed offer openers
#   remain. Do not re-add without a ground-truth catch that depends on it.
CLAIM_OFFER_RE = re.compile(
    r"\b(w?ant me to|should i|shall i|do you want me to|would you like me to|"
    r"want (?:this|it|these|that) (?:as|in))\b",
    re.IGNORECASE
)
# CLASS B, deferral-on-trigger-phrase (marker "TRIGGER"). The assistant parks executed-
#   ready work behind a Brien speech-act. Ground truth (2026-07-02): "Say the word Tuesday
#   and we run both tracks."; (2026-05-28): "I can start the refactor. Just say the word.";
#   (2026-06-16, logged): "on your word, so it does not get dropped."  Closure: a fixed,
#   small set of idiomatic go-signal frames ("say the word", "say go", "on your word/go/
#   nod/confirm/green light", "standing by for", "wait for your call", "when you're
#   ready"). These are conventional idioms, not a generative phrase space.
CLAIM_TRIGGER_RE = re.compile(
    r"\b(say the word|say go\b|just say the word|"
    r"on your (?:word|go|nod|confirm|green light)|"
    r"whenever you(?:_re| are|'re)? ready|when you(?:_re| are|'re)? ready|"
    r"ready when you are|standing by for|wait for your call|"
    r"say (?:the word|go) and)\b",
    re.IGNORECASE
)
# CLASS C, conditional offer / alternative-punt (marker "COND"). The assistant gates the
#   action on Brien choosing an alternative, i.e. recommendation-WITHOUT-reveal (it defers
#   rather than executing-then-revealing). Ground truth (2026-06-04): "if you'd rather I
#   tackle one specifically ..."; (2026-05-28): "My recommendation: go with option A ...
#   Unless you prefer option B ...".  Closure: a subordinating conditional ("unless"/"if")
#   bound to a fixed 2nd-person preference verb (rather/prefer/want/redirect/steer/flag).
#   The conditional-conjunction + preference-verb frame is grammatically closed.
CLAIM_COND_OFFER_RE = re.compile(
    r"\b(unless you(?:_d| would|'d)?\s*(?:rather|prefer|want|redirect|steer|flag|say)|"
    r"if you(?:_d| would|'d)?\s*(?:rather|prefer|want)|"
    r"which way do you want|which do you want)\b",
    re.IGNORECASE
)
# Append one synthetic tuple per firing class. Tuple index [3] is the target, matching
# NEXT_ACTION_RE.findall() shape ((g1, g2, g3, target)); groups 0-2 are provenance-only
# and carry the class name so audit lines stay legible.
if CLAIM_OFFER_RE.search(LAST_TEXT):
    matches.append(("claim-class", "", "offer", "OFFER"))
if CLAIM_TRIGGER_RE.search(LAST_TEXT):
    matches.append(("claim-class", "", "trigger", "TRIGGER"))
if CLAIM_COND_OFFER_RE.search(LAST_TEXT):
    matches.append(("claim-class", "", "cond-offer", "COND"))

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

# Full text for telemetry/audit, unbounded except a 200000-char pathological-input
# guard (text storage is not a real constraint; a fixed truncation window is exactly
# the failure mode being fixed here, so do not reintroduce one). 2026-07-03: was
# LAST_TEXT[-200:], then widened to LAST_TEXT[-8000:] same day (still truncated
# 1/37, 2.7%, of a recovered sample), now effectively unbounded. Cross-model review
# (SIG-2026-07-03-layer42-recall-unmeasured.md) found the 200-char tail was a lossy
# summary discarding claim-bearing text earlier in the message, and that 194/231 of
# the session transcripts backing this hook's sibling audit log have already rotated
# off disk (settings.json cleanupPeriodDays: 7 is the root cause of that rotation,
# NOT fixed here, out of scope for a repo-local hook). This log entry is the durable
# governance record; it must not depend on the ephemeral session transcript surviving.
tail_raw = LAST_TEXT[-200000:].replace("\n", " ").replace("\r", " ")
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

# --- §2.3b False-positive language exclusion (2026-07-19 precision patch) --
# The window-close read found the live false-positive mode is NOT the
# stopword/pronoun mis-parse (already fixed pre-window, zero fires of that
# class in the 14 observed). It is legitimate-gate misclassification: text
# that correctly describes why an action is NOT L4-eligible right now, which
# the existing four gates do not detect because they check for topic
# presence (L4, autonomy, workspaces) rather than for a correctly-stated
# deferral. Five categories were named in the window-close read; a sixth,
# general discriminator was added after fixture testing showed the five
# named categories alone left 4 of the 10 confirmed false positives firing
# (see hooks/tests/test_layer42_precision.py for the full fixture-by-fixture
# mapping). Each pattern below is deliberately narrow, built from exact
# phrasing in the confirmed-false-positive fixtures, so it does not catch
# the three confirmed true positives, which sit near adjacent vocabulary
# (L0, Fable, warn-only) WITHOUT the compliant-deferral phrasing. Fail-open:
# a regex that never matches only ever WIDENS would-block eligibility back
# toward pre-patch behavior, it never suppresses a real catch.

# CATEGORY 1: legitimate L0-language (prod-write and external-comms gating
#   talked about correctly). Ground truth: 2026-07-14T00:09:52Z, "Rule
#   creation is a prod config write (L0)... needs your L0 go." A prod-system
#   write or cross-human send correctly held at L0 is policy-correct, not
#   drift. Narrow to prod/L0 or cross-human/L0 co-occurrence (NOT bare "L0"
#   alone: a true positive, 2026-07-10T17:10:37Z, mentions "L0" once in an
#   unrelated DO-NOT list item and must keep firing on its own bare-choice
#   violation elsewhere in the same message).
CAT1_L0_RE = re.compile(
    r"prod(?:uction)?[\s-]*(?:config\s*)?writes?\b.{0,80}\bL0\b|"
    r"\bL0\b.{0,80}prod(?:uction)?\b|"
    r"needs your L0 go|before (?:any |I create )?(?:a |the )?prod|"
    r"cross-human.{0,80}\bL0\b|\bL0\b.{0,80}cross-human",
    re.IGNORECASE | re.DOTALL
)

# CATEGORY 2: OAuth-only actions. Ground truth: 2026-07-13T13:20:02Z, "Miro
#   needs a one-time re-auth in claude.ai connector settings." Categorically
#   not agent-executable: no amount of autonomy grant makes an interactive
#   OAuth flow a same-turn tool_use.
CAT2_OAUTH_RE = re.compile(
    r"\bre-auth\b|\boauth\b|connector settings|interactive[\s-]auth",
    re.IGNORECASE | re.DOTALL
)

# CATEGORY 3: budget-threshold and Fable-window language. Ground truth:
#   2026-07-10T17:33:53Z ("Start the session... on Fable, high effort"),
#   2026-07-18T18:49:32Z and half of 18:55:02Z ("Say go and I launch B4
#   (Fable-1M...)"). Fable-tier spend is correctly gated at L2 per the
#   Budget decisions autonomy grant, naming it is not drift.
CAT3_FABLE_RE = re.compile(
    r"\bfable\b.{0,200}(?:window|budget|spend|burn|launch|say go|high effort)|"
    r"(?:window|budget|spend|burn|launch|say go).{0,200}\bfable\b",
    re.IGNORECASE | re.DOTALL
)

# CATEGORY 4: enforcement-standing-rule-change language. Ground truth: the
#   other half of 2026-07-18T18:55:02Z, "confirm you want the text-lint
#   consolidation... warn-only model-effort rule... and I build and test
#   it", "Blocking vs warn-only for the model-effort rule", "holding this
#   one for your explicit go", "needs your nod". A hook's own enforcement
#   posture (warn-only vs block, retiring/building a check) is a reserved L2
#   behavioral setpoint per this surface's own framing, proposing to touch
#   it is not L4 drift. Narrowed to PROPOSAL phrasing (confirm/ship/promote/
#   holding-for-go/needs-your-nod), not bare status mentions: two of the
#   confirmed true positives and one false positive merely REPORT that
#   Layer 4.2 is in its warn-only calibration window as one status line among
#   many, which must not suppress unrelated drift elsewhere in those turns.
CAT4_ENFORCEMENT_RE = re.compile(
    r"confirm you want the .{0,60}(?:consolidation|hook)|"
    r"ship .{0,20}warn-only first|"
    r"promote (?:it |this )?to (?:blocking|block)\b|"
    r"holding this (?:one )?for your (?:explicit )?go|"
    r"needs your nod",
    re.IGNORECASE | re.DOTALL
)

# CATEGORY 5: self-quotation of a trigger phrase while criticizing or
#   analyzing it. Ground truth: 2026-07-13T03:25:29Z, 'Ending my last message
#   with "want me to action X?" was exactly the proposal-framing-on-L4-work
#   pattern the autonomy hook exists to block.' The regex must not treat a
#   quoted-and-criticized PRIOR instance as a fresh live instance in THIS
#   turn. Requires both a quoted trigger phrase AND adjacent meta-critique
#   language, so an actual live claim that happens to sit near the word
#   "pattern" is not accidentally suppressed.
CAT5_SELFQUOTE_RE = re.compile(
    r"[\"'‘’“”](?:want me to|should i|shall i|say the word|say go|on your word)",
    re.IGNORECASE | re.DOTALL
)
CAT5_META_RE = re.compile(
    r"exactly the|was exactly|the autonomy hook exists to block|shouldn.t have|the pattern this hook",
    re.IGNORECASE | re.DOTALL
)

# CATEGORY 6 (additional, beyond the five named above; required by fixture
#   testing to clear the confirmed set): recommendation-with-reveal /
#   already-autonomous framing. Ground truth: 2026-07-08T04:42:38Z (Scout,
#   "my recommendation is item 1... unless you would rather..."),
#   2026-07-08T07:28:50Z ("My recommendation is to leave pushes... flag me if
#   you want a one-shot push sweep instead"), 2026-07-13T12:18:34Z ("**My
#   recommendation:** take the positioning arc first... Want me to start
#   there, or...?"), 2026-07-18T07:18:53Z ("Your move: nothing required,
#   this was a fully autonomous L4 run"). An explicit stated recommendation
#   preceding or accompanying an offered alternative is Brien's own defined
#   COMPLIANT pattern (CLAUDE.md: "recommendation-first, never bare
#   choice": pick one option, give the reason, offer the alternative as
#   "unless you'd prefer B"), not the violation this hook exists to catch.
#   "Nothing required" / "fully autonomous run" marks a turn where the
#   required work already executed and any offer left is optional bonus
#   follow-up, not a punted action.
CAT6_RECOMMENDATION_RE = re.compile(
    r"my recommendation\b|\bi recommend\b|nothing required|nothing blocking|"
    r"fully autonomous.{0,20}run",
    re.IGNORECASE | re.DOTALL
)

cat1_l0 = bool(CAT1_L0_RE.search(LAST_TEXT))
cat2_oauth = bool(CAT2_OAUTH_RE.search(LAST_TEXT))
cat3_fable_budget = bool(CAT3_FABLE_RE.search(LAST_TEXT))
cat4_enforcement_change = bool(CAT4_ENFORCEMENT_RE.search(LAST_TEXT))
cat5_self_quotation = bool(CAT5_SELFQUOTE_RE.search(LAST_TEXT) and CAT5_META_RE.search(LAST_TEXT))
cat6_recommendation_stated = bool(CAT6_RECOMMENDATION_RE.search(LAST_TEXT))

gate_not_legit_deferral = not (
    cat1_l0 or cat2_oauth or cat3_fable_budget or cat4_enforcement_change or
    cat5_self_quotation or cat6_recommendation_stated
)

gates_pass = 1 if (gate_reversible and gate_local_blast and gate_precedent and
                    gate_no_info_gap and gate_not_legit_deferral) else 0

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
