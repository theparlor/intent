#!/usr/bin/env bash
# response-lint-stop-check.sh
#
# Stop hook -- consolidated response linter. Replaces three separate Stop-hook
# spawns (emdash-stop-check.sh, link-format-stop-check.sh, presend-assertion-check.sh)
# with ONE process that reads the transcript ONCE and runs all response-text rules
# over the extracted last-assistant message. Adds a fourth rule (model-effort
# recommendation) in WARN-ONLY mode.
#
# Why consolidate (2026-07-18, Brien-approved):
#   RUNNING  -- the three predecessors each spawned a python process and each
#               re-parsed the full transcript JSONL to pull the same last message.
#               One parse now serves every rule.
#   DOING    -- one combined block report instead of three separate ones, so every
#               text-lint violation surfaces together in a single pass instead of
#               ping-ponging fix -> resubmit -> next-hook-fires.
#
# Rules (jurisdiction is disjoint; each owns exactly one concern):
#   1. emdash        (BLOCK)      banned dash/arrow/ellipsis glyphs   [feedback_no_emdashes]
#   2. link-format   (BLOCK)      non-clickable local path forms      [feedback_link_format]
#   3. presend       (BLOCK)      client send-ready content w/o assertion audit
#   4. model-effort  (WARN-ONLY)  substantive turn missing a Model/Effort recommendation line
#
# The three BLOCK rules preserve their predecessors' regexes (triggers), audit-log
# paths, and per-rule bypass env vars verbatim, so enforcement is byte-identical.
# Reason strings are verbatim for emdash and link-format; the presend reason text is
# de-dashed per Brien's no-glyph rule (triggers unchanged, so enforcement is unaffected).
# model-effort is warn-only during calibration: it appends to its audit log and never
# blocks. Promotion to BLOCK happens later, after Brien reviews the miss-rate -- same
# warn-first calibration pattern the Layer-4.2 posture check used.
#
# Per-rule bypass:   EMDASH_BYPASSED=1 | LINK_FORMAT_BYPASSED=1 | PRESEND_ASSERTION_BYPASSED=1 | MODEL_EFFORT_BYPASSED=1
# Global bypass:     RESPONSE_LINT_BYPASSED=1
# Audit logs:        ~/.claude/audit/{emdash,link-format,presend-assertion,model-effort}-detections.log
#
# Fails OPEN on any error so a script bug can never permanently block responses.

set -u

[ "${RESPONSE_LINT_BYPASSED:-0}" = "1" ] && exit 0

INPUT=$(cat)

LINT_HOOK_INPUT="$INPUT" python3 - <<'PY'
import json, sys, re, os, datetime

def fail_open():
    sys.exit(0)

try:
    d = json.loads(os.environ.get("LINT_HOOK_INPUT", "") or "{}")
except Exception:
    fail_open()

# Recursion guard
if d.get("stop_hook_active"):
    sys.exit(0)

tpath = d.get("transcript_path") or ""
sid = d.get("session_id", "unknown")
if not tpath or not os.path.exists(tpath):
    sys.exit(0)

# ---- ONE parse: extract the FULL final-response text (fail open on any error) ----
# A single visible response splits across multiple assistant JSONL lines that
# SHARE one message.id (thinking / text / tool_use each on their own line), and
# a turn can end with a tool_use line carrying no text. Reading only the last
# object therefore misses text in earlier chunks of the same response, or gets
# nothing (hardening review 2026-07-18, finding 1). Fix: join every text block
# belonging to the final message.id. Falls back to the last object's text when
# no id is present. Residual (documented, follow-up): text emitted in an EARLIER
# message.id of the same turn, before a tool call, is not joined.
assistants = []
try:
    with open(tpath) as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                o = json.loads(line)
            except Exception:
                continue
            if o.get("type") == "assistant":
                assistants.append(o)
except Exception:
    sys.exit(0)
if not assistants:
    sys.exit(0)

def _blocks_text(obj):
    c = obj.get("message", {}).get("content", [])
    if isinstance(c, list):
        return "\n".join(b.get("text", "") for b in c
                         if isinstance(b, dict) and b.get("type") == "text")
    if isinstance(c, str):
        return c
    return ""

final_id = assistants[-1].get("message", {}).get("id")
if final_id is not None:
    text = "\n".join(t for t in (_blocks_text(o) for o in assistants
                     if o.get("message", {}).get("id") == final_id) if t)
else:
    text = _blocks_text(assistants[-1])
if not text.strip():
    sys.exit(0)

ts = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
AUDIT_DIR = os.path.expanduser("~/.claude/audit")
try:
    os.makedirs(AUDIT_DIR, exist_ok=True)
except Exception:
    pass

def audit(name, line):
    try:
        with open(os.path.join(AUDIT_DIR, name), "a") as a:
            a.write(line + "\n")
    except Exception:
        pass

blocks = []  # reason strings from BLOCK rules; combined into one block decision

# ---- RULE 1: emdash (BLOCK) ---- verbatim from emdash-stop-check.sh
try:
    if os.environ.get("EMDASH_BYPASSED", "0") != "1":
        GLYPHS = {
            "—": "em-dash", "–": "en-dash", "―": "horizontal-bar",
            "→": "right-arrow", "←": "left-arrow", "↔": "both-arrow",
            "⇒": "double-arrow", "…": "ellipsis",
        }
        found = [name for g, name in GLYPHS.items() if g in text]
        if found:
            audit("emdash-detections.log", "[%s] CAUGHT session=%s glyphs=%s" % (ts, sid, ",".join(found)))
            blocks.append(
                "DASH-GLYPH DRIFT (feedback_no_emdashes): your response contains glyphs Brien's peers read "
                "as an AI tell, which blocks his ability to share this material -- detected: "
                + ", ".join(found) + ". These are banned with no reprieve, in conversation and in every "
                "drafted/shareable artifact (Slack, email, Jira, Confluence, deliverables). Rewrite using "
                "periods, commas, colons, parentheses, the words 'to'/'vs', or a plain hyphen (-) instead. "
                "If you ran a mechanical strip on a file, also fix the resulting comma-splices by hand. "
                "Bypass with EMDASH_BYPASSED=1 ONLY when quoting a source verbatim that must keep the glyph."
            )
except Exception:
    pass

# ---- RULE 2: link-format (BLOCK) ---- verbatim from link-format-stop-check.sh (code fences exempt)
try:
    if os.environ.get("LINK_FORMAT_BYPASSED", "0") != "1":
        prose = re.sub(r"```.*?```", "", text, flags=re.S)
        anchor_local = re.compile(r"\]\(\s*(?!https?://|mailto:|#)([~./]|/Users/|Core/|Work/|Home/)", re.I)
        anchor_ext   = re.compile(r"\]\(\s*(?!https?://|mailto:|#)[^)]*\.(?:md|py|ya?ml|csv|json|sh|html?|xlsx|pdf|docx|txt|png)\s*\)", re.I)
        backtick_abs = re.compile(r"`(?:/Users/brien/Workspaces|~/Workspaces)[^`]*`")
        bare_rel     = re.compile(r"(?:^|\s)(?:Core|Work|Home)/[\w./-]+\.(?:md|py|ya?ml|csv|json|sh|html?|xlsx|pdf|docx)\b")
        tilde_path   = re.compile(r"(?<![\w/])~/[\w.\-/]+")
        hits = []
        if anchor_local.search(prose) or anchor_ext.search(prose):
            hits.append("markdown-anchor-to-local-path")
        if backtick_abs.search(prose):
            hits.append("backtick-wrapped-absolute-path")
        if bare_rel.search(prose):
            hits.append("bare-relative-workspace-path")
        if tilde_path.search(prose):
            hits.append("tilde-shorthand-path-double-nests")
        if hits:
            audit("link-format-detections.log", "[%s] CAUGHT session=%s hits=%s" % (ts, sid, ",".join(hits)))
            blocks.append(
                "LINK-FORMAT DRIFT (feedback_link_format): your response references a local file in a form "
                "that is NOT clickable in Brien's interface -- detected: " + ", ".join(hits) + ". The ONLY "
                "clickable form is a BARE, FULL-ABSOLUTE path starting /Users/brien/Workspaces/... with "
                "nothing around it. Do NOT use the ~/ shorthand (~/Workspaces, ~/.claude): Brien's client "
                "joins it to the project-root CWD and produces a double-nested /Users/brien/Workspaces/~/Workspaces/... "
                "path he cannot open. No markdown anchor [label](...), no backticks, no relative Core/|Work/|Home/ form, "
                "no ~/ shorthand. Rewrite every file reference as a bare /Users/brien/... absolute path "
                "(fenced code-block examples are exempt)."
            )
except Exception:
    pass

# ---- RULE 3: presend assertion audit (BLOCK) ---- verbatim from presend-assertion-check.sh
try:
    if os.environ.get("PRESEND_ASSERTION_BYPASSED", "0") != "1":
        lower = text.lower()
        SEND_RE = r"(paste-ready|paste ready|ready to send|send-ready|send ready|ready to paste|send (this|that|it) (to|over)|send the (reply|message|email|note)|for you to send|you can send (this|that|it)|then send (this|that|it)|drop (this|that) to|reply (for|to) (greg|dean|kevin|natalie|the client|him|her|them)|message (for|to) (greg|dean|the client))"
        AUDIT_RE = r"(assertion[- ]audit|pre-?send (assertion|audit|check)|per[- ]claim source|claim[- ]by[- ]claim|each (factual |load-bearing )?claim (is |was )?sourced|claims sourced|sourced each (claim|assertion)|source-?audited|verified note —|verified note \(|✓ sourced|sources verified before)"
        if re.search(SEND_RE, lower) and not re.search(AUDIT_RE, lower):
            audit("presend-assertion-detections.log", "[%s] CAUGHT-PRESEND session=%s" % (ts, sid))
            blocks.append(
                "PRE-SEND ASSERTION DRIFT: this response presents client-facing send-ready content "
                "(a reply/message to be sent to another human) but shows no pre-send assertion audit. "
                "Before client-facing assertions leave the building, run the audit: enumerate every "
                "load-bearing factual claim in the draft and, for EACH, state its basis: verified (with the "
                "file/ticket/source you actually checked), inferred (and label it as inference), or unknown "
                "(and either cut it or turn it into a question). Any claim drawn from NOT-finding something "
                "(absence) is not verified, flag it. Then revise unsourced assertions to be sourced or hedged, "
                "add a short 'assertion-audit' / 'verified note' line, and re-present. Origin: "
                "SIG-2026-06-04-assert-from-inference-drift. Bypass with PRESEND_ASSERTION_BYPASSED=1 only if "
                "the content carries no factual claims."
            )
except Exception:
    pass

# ---- RULE 4: model-effort recommendation (WARN-ONLY) ----
# Convention (2026-07-18): substantive turns open with a "Model: X . Effort: Y" line, plus a
# "FABLE-SUITED, fallback ..." callout when the Fable rubric fires. This rule only LOGS a miss;
# it never blocks. The substantive-length threshold and marker regex are deliberately rough --
# warn-only exists to gather the miss-rate so the heuristic can be tuned before any promotion.
try:
    if os.environ.get("MODEL_EFFORT_BYPASSED", "0") != "1":
        substantive = len(text) >= 800
        head = text[:400]
        has_model_line = bool(re.search(r"(?i)\bmodel:\s*\S", head) and
                              re.search(r"(?i)\beffort\b", head))
        has_fable_flag = bool(re.search(r"(?i)fable-suited", text))
        if substantive and not has_model_line and not has_fable_flag:
            audit("model-effort-detections.log",
                  "[%s] WARN-MISS session=%s len=%d (substantive response opened without a Model/Effort recommendation line)" % (ts, sid, len(text)))
except Exception:
    pass

if blocks:
    print(json.dumps({"decision": "block", "reason": "\n\n".join(blocks)}))
sys.exit(0)
PY
exit 0
