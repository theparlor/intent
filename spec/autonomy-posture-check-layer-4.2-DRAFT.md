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

## §4 Calibration protocol

Layer 4.2 starts in WARN-ONLY mode (emit telemetry, do not block) for at least 14 days. During calibration:

1. Telemetry log shows fire rate, false-positive rate (manual review weekly)
2. False-positive examples are categorized:
   - **legitimate forecast** (response describes next action but it requires a NEW session or future user input — not a same-turn obligation)
   - **gate heuristic mismatch** (4-gate heuristic was wrong)
   - **lexical mismatch** (next-action regex caught something that wasn't a real next-action claim)
3. After 14d: if false-positive rate < 5%, promote to BLOCK mode

Promotion gate: Brien-confirmation on telemetry summary + matcher scope.

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
