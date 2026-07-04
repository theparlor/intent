---
title: Autonomy Posture Check — Layer 4.2 (PreSubmitResponse positive-execution check)
id: SPEC-INTENT-AUTONOMY-POSTURE-CHECK-LAYER-4.2-001
updated: 2026-05-26
related:
  - Core/frameworks/intent/spec/autonomy-grant-enforcement.md
  - Core/frameworks/intent/hooks/autonomy-grant-stop-check.sh
  - Core/frameworks/intent/tests/test_autonomy_grant_stop_hook_check4.sh
depth_score: 4
depth_signals:
  file_size_kb: 11.4
  content_chars: 10645
  entity_count: 0
  slide_count: 0
  sheet_count: 0
  topic_count: 0
  has_summary: 0
vocab_density: 0.09
status: draft
scope: framework
date: 2026-05-26
author: intent framework — autonomous continuation during dentist-break 2026-05-26
source_signal: "Workspaces/.intent/signals/SIG-2026-05-26-autonomy-grant-drift-recurrence-in-session.md §\"Layer 4.2 — structural posture check (deferred, follow-up signal)\""
ratification_dependencies:
  - Brien-confirmation on matcher scope (over-blocking risk on legitimate forecasting)
  - calibration period (start in warn-only mode, promote to block-mode after telemetry shows zero false-positive rate)
---
# Autonomy Posture Check — Layer 4.2 (positive-execution posture)

> Status: DRAFT. Design + scaffold are L4; live activation requires Brien sign-off on matcher scope.

## §1 Problem statement

Layer 4 of the autonomy-grant enforcement hook stack (currently 4 CHECKs in `autonomy-grant-stop-check.sh`) operates by **regex-matching forbidden phrases** in the response tail:

| CHECK | Pattern | Year |
|---|---|---|
| 1 | bare-choice multi-option question without recommendation marker | 2026-04-28 |
| 2 | soft-queue "Say go and I X" / "unless you'd like" | 2026-05-13 |
| 3 | L0-on-push framing "Not pushed. Run git push from..." | 2026-05-20 |
| 4 | conditional-queue "unless you redirect" / "I'll X next unless" | 2026-05-26 |

Each new regex variant has been authored in response to a NEW linguistic drift that slipped past prior CHECKs. The pattern is robust to layer-by-layer regex additions because the underlying drift mechanism (caution-bias toward asking for confirmation) generates new linguistic variants faster than regex can keep up.

**The closure path for the pattern CLASS is structural, not lexical.** Layer 4.2 is the structural mechanism.

## §2 Architecture

### §2.1 Core idea — positive-execution posture check

Instead of matching forbidden phrases, Layer 4.2 verifies a positive property: **when the response describes a "next L4 action" and the 4 gates pass for it, the action MUST have been executed within the same turn.**

Pseudocode:

```
On Stop event:
  1. Extract last assistant message text + tool-use blocks within the same turn
  2. Detect "next-action claims" in text (regex on imperative + verb phrases)
  3. For each next-action claim N:
     a. Estimate 4-gate result for N (cheap heuristic)
     b. If 4 gates pass AND no tool-use block in same turn corresponds to N → block
     c. If 4 gates fail OR tool-use corresponds → pass
  4. Emit telemetry + (block | silent)
```

The novel piece is **(3.b)**: the cross-reference between claimed-next-action and actual tool-call execution in the SAME turn.

### §2.2 Next-action claim detection

Imperative + verb-phrase regex (case-insensitive, anchored in last paragraph):

```
NEXT_ACTION_RE = (
    "(I[''']?ll|will|going to|next (move|step|L4|action)) "
    "(write|run|build|execute|deploy|do|start|draft|capture|file|commit|push|"
    "extract|apply|configure|register|wire) "
    "[a-z][a-z0-9_./-]*"
)
```

Matches: "I'll write X", "will run X", "going to draft X", "next L4 move: extract X".

### §2.3 4-gate heuristic estimator

The full 4-gate check (reversible / local blast / precedent / no info gap) requires semantic understanding. For Layer 4.2, a CHEAP heuristic suffices because the goal is "did the assistant have evidence to act and not?", not "should the assistant act?":

```
gates_pass(N, response_text) =
  reversible    := N path starts with workspaces-local OR mentions .intent/ or signal OR git operation in solo repo
  local_blast   := N path NOT in (Slack, email, calendar, money, external) AND NOT mentions "cross-human"
  precedent     := response_text contains "L4" OR cite of autonomy grant OR similar action was just executed in this turn
  no_info_gap   := response does NOT contain "TBD" / "needs Brien" / "Brien decides" within 3 lines of N
  return reversible AND local_blast AND precedent AND no_info_gap
```

False-positive rate: TBD via calibration period. Initial telemetry mode is warn-only.

### §2.4 Same-turn tool-use cross-reference

The hook receives the transcript including tool-use blocks. Layer 4.2 must:

1. Extract all tool-use blocks AFTER the last assistant text message (or in the same message)
2. Check if any tool-use targets a file/path that matches the next-action claim
3. Match score:
   - **Strong**: tool-use file_path contains a substring of N (e.g., N = "apply_lambda_settings.py" → tool-use Write to `.../apply_lambda_settings.py`)
   - **Weak**: tool-use is in same product/framework dir as N's implied scope
   - **None**: no related tool-use → block-eligible

A weak match passes; only "none" triggers the block.

## §3 Implementation sketch

```bash
# Hook file: Core/frameworks/intent/hooks/autonomy-posture-check-layer-4.2.sh
# Registration: PostStop hook (after autonomy-grant-stop-check.sh CHECK 1-4)
# OR: integrated into autonomy-grant-stop-check.sh as CHECK 5

# Hooks 1-4 are LEXICAL (catch forbidden phrases).
# Hook 4.2 is STRUCTURAL (verify positive-execution property).

# The hook reads the transcript (same input shape as autonomy-grant-stop-check.sh
# Stop hook), but in addition to extracting LAST_TEXT, it extracts the tool-use
# blocks within the same assistant message OR within the prior N assistant messages
# (since execution typically happens in the SAME turn as the description).

# Pseudocode (Python embedded in bash, like the existing hook):

python3 <<'PY'
import json, sys, re, os
TRANSCRIPT_PATH = os.environ.get("TRANSCRIPT_PATH")
LAST_TEXT = ""
LAST_TOOLS = []

# Parse transcript JSONL
with open(TRANSCRIPT_PATH) as f:
    last_assistant = None
    for line in f:
        line = line.strip()
        if not line: continue
        try: obj = json.loads(line)
        except: continue
        if obj.get("type") == "assistant":
            last_assistant = obj

if not last_assistant:
    sys.exit(0)

msg = last_assistant.get("message", {})
content = msg.get("content", [])
for block in content:
    if isinstance(block, dict):
        if block.get("type") == "text":
            LAST_TEXT += block.get("text", "") + "\n"
        elif block.get("type") == "tool_use":
            LAST_TOOLS.append(block)

# Detect next-action claims
NEXT_ACTION_RE = re.compile(
    r"(I'?ll|will|going to|next (move|step|L4|action)) "
    r"(write|run|build|execute|deploy|do|start|draft|capture|file|commit|push|"
    r"extract|apply|configure|register|wire) "
    r"([a-zA-Z][a-zA-Z0-9_./-]*)",
    re.IGNORECASE
)
matches = NEXT_ACTION_RE.findall(LAST_TEXT)
if not matches:
    sys.exit(0)

# For each next-action, check if any tool-use corresponds
unmatched = []
for m in matches:
    action_target = m[3]  # the noun
    matched = False
    for tool in LAST_TOOLS:
        ti = tool.get("input", {})
        tool_target = (ti.get("file_path", "") + " " +
                       ti.get("command", "") + " " +
                       ti.get("prompt", ""))
        if action_target.lower() in tool_target.lower():
            matched = True
            break
    if not matched:
        # Apply 4-gate heuristic — if gates pass and no tool-use, this is a violation
        gates_pass_heuristic = (
            # reversible: workspaces-local hints
            ("workspaces" in LAST_TEXT.lower() or ".intent" in LAST_TEXT.lower() or "signal" in LAST_TEXT.lower()) and
            # no cross-human:
            ("slack" not in LAST_TEXT.lower()[:500] and "email" not in LAST_TEXT.lower()[:500]) and
            # precedent (L4 referenced):
            ("L4" in LAST_TEXT or "L4-" in LAST_TEXT or "autonomy" in LAST_TEXT.lower()) and
            # no info gap:
            ("TBD" not in LAST_TEXT[-1000:] and "Brien decides" not in LAST_TEXT[-1000:])
        )
        if gates_pass_heuristic:
            unmatched.append(action_target)

if unmatched:
    print(json.dumps({
        "decision": "block",
        "reason": ("AUTONOMY-GRANT DRIFT (Layer 4.2 — positive-execution posture check): "
                   "your response describes the next L4 action(s) " + str(unmatched) +
                   " AND the 4-gate heuristic passes for them AND no tool-use in this turn "
                   "corresponds to them. Per the AUTONOMY GRANT POSTURE anchor: if 4 gates pass, "
                   "EXECUTE in this same turn. Do not queue. Do not describe-then-stop. "
                   "Execute the action now, OR surface the specific failing gate that blocks "
                   "execution (info gap, cross-human comms, L0 external system).")
    }))
    sys.exit(0)

sys.exit(0)
PY
```

## §3.5 Grammatical-class exclusion (added 2026-07-03)

Two calibration reviews (SIG-2026-06-12-layer42-calibration-review.md at 14 days,
SIG-2026-06-28-flight-model-30day-ratification-readiness.md at 30 days) found the target
extractor (§2.2, `NEXT_ACTION_RE` group 4) captures the single word immediately following
the verb, which is frequently a pronoun/quantifier/preposition ("that", "each", "all",
"with") when the real referent is anaphoric or the construction is a compliant
recommendation-with-reveal, not a deferred action. 8 of 9 historical `would_block=1` fires
through 2026-06-29 were this class.

Fixed in the live hook (`autonomy-posture-check-layer-4.2.sh` §2.2b, 2026-07-03) with a
closed-class exclusion set (pronouns, quantifiers/determiners, prepositions, conjunctions)
plus trailing-punctuation stripping. This is a fixed part-of-speech set, not an open-ended
phrase list — it does not reproduce the CHECK-1-through-7 whack-a-mole pattern the lexical
layer hit (see `lexical-layer-freeze.yaml`).

**Explicitly NOT fixed:** a real noun target is still would-block-eligible even when the
surrounding sentence is a compliant recommendation-with-reveal. The 06-28 signal's own
false-positive table mis-bucketed one such case (`team-configs`, a genuine compound noun)
alongside the pronoun/quantifier fires without flagging that it doesn't fit that pattern.
Re-verified live post-fix (2026-07-03): the `each`-class fires now correctly report
`would_block:0`; a synthetic `team-configs`-shaped fire with gates forced to pass still
correctly reports `would_block:1` — the residual is real and open, not silently patched
away. Closing it requires strengthening `gate_no_info_gap` to detect
recommendation-with-reveal phrasing semantically, which is separate, harder work (see
`Core/frameworks/intent/spec/2026-07-03-autonomy-grant-pause-drift-audit.md` §2 root cause 3
and §7 Phase 2) and is NOT done by this fix.

## §2.2d Deferred-claim grammar: recall widening (added 2026-07-03)

The §2.2 `NEXT_ACTION_RE` and §3.5 stopword exclusion were both authored and calibrated
against a 9-fire would-block sample, i.e. entirely against **precision**. A cross-model
breadth pass (Fable 5, spot-checked by Opus 4.8) measured the missing axis for the first
time: recall against the lexical Stop-hook's own true-positive corpus, the 231 genuine
CHECK1-7 catches in `~/.claude/audit/autonomy-grant-stop-detections.log`. That corpus is
the exact behavior Layer 4.2 exists to structurally replace, so it is the correct recall
ground truth. Full finding: `SIG-2026-07-03-layer42-recall-unmeasured.md`.

**Measured recall of the pre-2026-07-03 grammar (replayed over all 231 tails):**

| Grammar | Caught | Rate | Note |
|---|---|---|---|
| `NEXT_ACTION_RE`, matched at all | 17 / 231 | 7.4% | the signal's headline lower bound |
| `NEXT_ACTION_RE`, non-stopword (would-block-eligible after §3.5) | 4 / 231 | 1.7% | what actually reaches the 4-gate estimator |

A detector at ~2% recall with near-perfect precision on 9 fires has barely fired; a clean
calibration window under that condition is not evidence of readiness (it is evidence of
silence). Before spending another window on the patch-then-window-then-promote sequence, the
claim grammar had to be widened to catch what the lexical layer already catches.

**What was added (live hook §2.2c):** three closed-grammatical-class detectors, run
alongside `NEXT_ACTION_RE` rather than folded into it. Each produces a synthetic match tuple
shaped like `NEXT_ACTION_RE.findall()` output (target at index [3]) carrying a class marker
(`OFFER` / `TRIGGER` / `COND`), so it flows unchanged through §3.5 stopword filtering, §2.4
tool_use cross-reference, and the §2.3 4-gate logic. A class marker is not a stopword (a
deferral is real, unlike an anaphoric pronoun) and will not substring-match a tool_use blob
(a genuine deferral has no same-turn execution), so it correctly reaches the gate estimator.

| Class | Marker | Closed construction (why it is not a phrase list) | Ground-truth example from the corpus |
|---|---|---|---|
| A. interrogative offer | `OFFER` | fixed set of 1st/2nd-person offer openers (`want me to`, `should I`, `shall I`, `would you like me to`). You cannot coin a new interrogative-offer opener the way you can coin a new hedge sentence | 2026-05-04: "Want me to draft a TSD ticket to Omar requesting the OAuth scope grant, or is the current ticket-queue model the intended steady state?" |
| B. deferral-on-trigger-phrase | `TRIGGER` | fixed set of idiomatic go-signal frames (`say the word`, `say go`, `on your word/go/nod/confirm/green light`, `standing by for`, `wait for your call`, `when you're ready`). Conventional idioms, a bounded set | 2026-07-02: "Say the word Tuesday and we run both tracks." |
| C. conditional offer / alternative-punt | `COND` | subordinating conditional (`unless`/`if`) bound to a fixed 2nd-person preference verb (`rather`/`prefer`/`want`/`redirect`/`steer`/`flag`). Recommendation-WITHOUT-reveal; the conjunction+verb frame is grammatically closed | 2026-06-04: "if you'd rather I tackle one specifically ..." |

This is the standing lexical-layer-freeze objection ("phrase lists never converge") answered
directly: these three classes are bounded by grammar (pronoun sets, subordinating
conjunctions, interrogative-offer frames, go-signal idioms), not by phrasing creativity, so
they do not reproduce the CHECK-1-through-7 whack-a-mole (`lexical-layer-freeze.yaml`).

**Adversarial-verify trim (2026-07-03, same day):** the independent verify pass refuted one
branch of the original Class A draft: a bare `want (?:me )?to` alternative that collapses to
the open bigram "want to" and fired advice-shaped in telemetry (33/123 OFFER hits were
"you might want to review"-class text, not deferrals). Load-bearing test: deleting it changed
231-corpus recall by ZERO (178 to 178); no ground-truth catch depended on it. It was removed
before the calibration window opened, leaving only the closed offer openers in the table
above. Rule going forward: a new Class A branch requires a ground-truth catch that depends on
it. Window read-protocol note (also from the verify pass): would-block ELIGIBILITY on stored
tails widens roughly 16 to ~310 of 1757 telemetry rows, but full-path would_block was 0 to 5
on stored 200-char tails because gate_precedent fails most; the concurrent telemetry-tail
unbounding means the live rate will run higher than that stored-tail estimate, and the next
calibration read must not treat the 5-row figure as the expected fire rate.

**Measured recall after the widening (same 231 tails):**

| Grammar | Caught | Rate |
|---|---|---|
| `NEXT_ACTION_RE` + §2.2c classes A/B/C | **178 / 231** | **77.1%** |

**Residual misses (53), bucketed honestly. Some are structurally unreachable by ANY text regex over the tail:**

| Bucket | Count | Reachable by a text regex? |
|---|---|---|
| trailing-observation closure (CHECK6 class: closure + "one observation / worth noting", NO offer or question in the tail) | 23 | No in the tail. Either a compliant executed turn (correct non-catch) or the offer sat earlier in the message and the 200-char telemetry tail truncated it away (the lossy-tail artifact documented in SIG-2026-07-03 addendum; the tail widening to unbounded fixes this going forward, but the 194/231 already-rotated transcripts can never be re-measured) |
| clean status report / handoff (no offer-verb, no trailing question in tail) | 27 | No. Same tail-truncation / clean-closure split as above |
| URL / citation dump (trailing link lines) | 2 | No. Telemetry noise, not a hedge; catching would be a false positive |
| info-question close ("Who's your pick to win this season?") | 1 | Yes but MUST NOT. A conversational info-question, not an L4 deferral; catching it would be a false positive |

The honest floor: **silent-stop is structurally unreachable.** A turn that finishes work,
says nothing about a next action, and simply stops (no offer, no trigger, no conditional, no
declarative claim) leaves no text for any regex to match. That failure mode is out of scope
for a text detector by construction and is named here rather than chased. It is exactly the
class the §2.4 tool_use cross-reference and the positive-execution posture (not the claim
grammar) are meant to reason about.

**Precision guard (unchanged verdicts on the historical fires).** Replayed against the 9
would-block=1 telemetry rows: the 8 stopword-class fires (`each`, `that`×3, `all`, `with`×2,
`those.`) still route through the §3.5 stopword path on their old-regex target and are
untouched by the new classes; the genuine `team-configs` residual (§3.5) stays would-block-
eligible and open: the widening neither resurfaces the suppressed 8 nor masks the one real
residual. Separately, several of those same tails DO carry a genuine CLASS B/C construction
(e.g. "on your word", "if you'd rather I tackle one"): that is not a regression but the
recall win: the old grammar could only see their stopword target and suppressed it, while the
new grammar sees the actual deferral. End-to-end hook runs (real stdin JSON, real telemetry
sink, then cleaned): a compliant executed-action turn logs `would_block=0 has_tool_use=1`; a
genuine "say the word" hedge turn (invisible to the old grammar) logs `would_block=1
next_actions=['TRIGGER']`; an empty turn logs `would_block=0 next_actions=[]`; exit 0 in all
three. Syntax gates: `bash -n` on the hook and `ast.parse` on the embedded python block both
pass.

**What this does NOT change** (same discipline as §3.5): the hook stays warn-only (widening
detection is calibration-safe by construction: it can only add would-block *observations*, it
cannot block); the §3.5 stopword exclusions, the 4-gate heuristic, and all promotion machinery
are untouched. Promotion to block-mode remains Brien's L2 call. What this fixes is the
diagnosis, not the readiness: it makes the next calibration window measure a detector that
actually fires, so a clean read would mean precision, not silence. Per §4, a fresh window
against this widened grammar is required before promotion is re-evaluated.

## §4 Calibration protocol

Layer 4.2 starts in WARN-ONLY mode (emit telemetry, do not block) for at least 14 days. During calibration:

1. Telemetry log shows fire rate, false-positive rate (manual review weekly)
2. False-positive examples are categorized:
   - **legitimate forecast** (response describes next action but it requires a NEW session or future user input — not a same-turn obligation)
   - **gate heuristic mismatch** (4-gate heuristic was wrong)
   - **lexical mismatch** (next-action regex caught something that wasn't a real next-action claim) — see §3.5, fixed 2026-07-03 for the pronoun/quantifier/preposition subclass
3. After 14d: if false-positive rate < 5%, promote to BLOCK mode. As of the 30-day review (2026-06-28) the numeric trigger was met but precision was 0% (all 8 fires were the §3.5 false-positive class); a fresh re-calibration window against the corrected extractor is required before re-evaluating promotion — see the 2026-07-03 audit doc §7 Phase 2 for the sizing rationale (do not compress to 3-5 days).

Promotion gate: Brien-confirmation on telemetry summary + matcher scope. Unchanged by the 2026-07-03 extractor fix — that fix corrects the diagnosis, it does not itself authorize promotion.

## §5 Cross-references

- **Layer 1**: feedback memory + SessionStart anchor (current — `AUTONOMY GRANT POSTURE`)
- **Layer 2**: closure-discipline spec (current)
- **Layer 3**: autonomy-grant-drift-detector skill (current)
- **Layer 4**: autonomy-grant-stop-check.sh CHECKs 1-4 (current — LEXICAL)
- **Layer 4.2**: this spec — STRUCTURAL posture check (new)
- **Layer 5**: autonomy-grant-dispatch-prompt-check.sh PreToolUse (current — sub-agent dispatch)

Layer 4.2 sits BETWEEN Layer 4 (lexical Stop-hook) and Layer 5 (PreToolUse for dispatch). It runs at Stop time like Layer 4 but checks a positive property rather than a forbidden pattern.

## §6 Open design questions (for ratification review)

1. **Match score weighting**: how strictly should we cross-reference next-action targets to tool-use blocks? Loose match catches over-eagerness; strict match misses legitimate same-turn execution that's described differently than executed.
2. **Calibration period length**: 14 days is a starting point. Should be telemetry-driven (extend if fire rate is noisy).
3. **Forbidden-phrase fallback**: if Layer 4.2 is too noisy and gets disabled, do we keep the CHECK 4 regex as a stop-gap, or rely entirely on Layer 4.2 once it's stable? Recommended: keep CHECKs 1-4 as belt-and-suspenders.
4. **Subagent boundary**: when the response includes Agent tool-use that dispatches the action to a sub-agent, does that count as execution or queuing? Current sketch counts it as execution (the action moves off the current actor's plate). Brien-input needed.

## §7 What this spec is NOT

- This is not a replacement for CHECKs 1-4 (the lexical hooks remain operational).
- This is not a guarantee that the pattern class is fully closed — only that it adds STRUCTURAL evidence that complements the lexical detectors.
- This is not the live decision-compute layer of the flight model (that's a separate work track).
