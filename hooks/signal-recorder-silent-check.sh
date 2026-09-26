#!/usr/bin/python3
# signal-recorder-silent-check.sh
#
# PreToolUse hook (registered on Write|Edit in ~/.claude/settings.json; the Bash branch
# below is kept for any matcher that adds Bash). Witness mandatory-recorder check for
# WS-DDR-098: a product that declares autonomy settings must report what it does to
# Witness. The file keeps its .sh name because settings.json and ~/.claude/hooks point at
# it; it is Python, run by the system interpreter in its shebang (no venv needed).
#
# What it checks (rebuilt 2026-09-25, QMT-01M3D8KVWP66F2SH5X0TAV4E0B):
#   1. The tool call's file path (file_path, path, notebook_path, or for Bash the first
#      absolute path in the command that exists) is walked up to the nearest folder that
#      holds a .intent/ directory: the product.
#   2. Engagement products (Work/<kind>/Engagements/<Client>/...) are exempt.
#   3. Only products whose .intent/INTENT.md declares lambda_settings: or
#      autonomy_grants: at column 0 are checked.
#   3b. A product that declares no actions of its own, with a named reason
#      ("witness_actions: none (<reason>)" at column 0 in INTENT.md, a content or
#      methodology repo), is skipped: detection no-actions-declared. A bare "none"
#      with no reason is not a declaration (WS-DDR-150 backfill, QMT-01M3F5JYA4643ANV7GPPRJDPZR).
#   4. The product's Witness names: INTENT.md may declare
#          witness_source_system: fieldbook
#          witness_source_system: [signalbox, exchange]
#      or a block list of "- name" lines. Absent that, the name is the product's
#      directory name, with a session-kit worktree suffix removed ("intent-wt-<task>"
#      reads as "intent"). Witness's intent-events adapter uses the same default when it
#      ingests Core/**/.intent/events/events*.jsonl, so a product that writes its own
#      events file is found under its directory name with no declaration.
#   5. The names are looked up, ignoring case, in the Witness source index
#      ($HOME/.claude/state/witness-source-index.json, built by
#      hooks/witness_source_index.py from the Witness events store). The index keys each
#      event by event.product, else source_system. No event in 30 days under any of the
#      names means the product is silent.
#   6. Field lint (WS-DDR-150, added 2026-09-26, QMT-01M3F5JWBR8XPK9YGB7HTMCBNP). For an
#      active product the index also says, per name, how many of its rule-bound events in
#      the last 30 days miss a minimum field (ts with timezone, product, event, caller,
#      machine, outcome, duration_ms, run_id; redaction_level on engagement events) and
#      which field is missing most often. When more than half miss a field, the session
#      is told once, in one sentence that names that field and points at emit.py.
#      Legacy events (screenpipe, cc-native, entire-io, and anything a Witness stream
#      adapter carried, marked by attributes.adapter) are counted by the builder and
#      shown by its --report, but never produce this note. The rule for telling them
#      apart is written out in witness_source_index.py under "Field lint".
#   The hook never scans the Witness store. When the index is missing or more than 24
#   hours old it starts the builder detached (at most one kick an hour, stamp file next
#   to the index) and does not wait for it.
#
# Its own events (WS-DDR-150): every fire, except a bypassed one, reports itself to
# Witness through emit.py as product intent, event hook.fire, caller
# hook:signal-recorder-silent-check, with the detection, the product's directory name as
# target (a hash plus redaction_level client-confidential for an engagement path), the
# session id and its duration. Fail-open: when emit.py is absent (a machine without
# Witness) nothing is said; a failed emit prints one line to stderr (the debug log) and
# the check's result stands. Costs about 11 ms of the latency budget.
#
# Telemetry detections (one JSONL row per call, $HOME/.claude/logs/signal-recorder-silent.jsonl):
#   no-context, engagement-exempt, no-lambda-declaration      skip, as before
#   no-actions-declared   the product names why it has no actions (step 3b); skip
#   recorder-active       a Witness event within 30 days (was: a SIG-*.md within 30 days)
#                         and its rule-bound events mostly carry the minimum fields
#                         (lint_* fields in the row when the index has field lint)
#   nonconformant-events  active, but more than half of its rule-bound events miss a
#                         minimum field (outcome warn, or warn-suppressed once told)
#   silent-recorder       no Witness event within 30 days (outcome warn, or
#                         warn-suppressed when this session was already told)
#   witness-index-missing / witness-index-malformed           no verdict possible; builder kicked
#   hook-error            an internal error; logged, the call proceeds
#
# Output channel: JSON on stdout, hookSpecificOutput.additionalContext, which Claude Code
# adds to the model's context before the tool runs, plus a one-line systemMessage for the
# person. Checked 2026-09-25 on Claude Code 2.1.282 two ways: the hooks reference
# (code.claude.com/docs/en/hooks, PreToolUse decision control: additionalContext is
# "added to Claude's context before the tool call executes"; exit 0 stderr "goes to the
# debug log only, Claude never sees it") and a headless probe in which the model reported
# the additionalContext token and neither the stderr nor the systemMessage token. The old
# stderr warning therefore reached nobody. The note goes out once per session per
# product: state in $HOME/.claude/state/signal-recorder-silent-warned.json keyed by the
# hook input's session_id, entries pruned after 7 days.
#
# Posture: WARN-ONLY. Never blocks, always exits 0; any internal error fails open.
# Bypass: SIGNAL_RECORDER_SILENT_BYPASSED=1 (inert: no telemetry, no note, no Witness event)
# Audit log: $HOME/.claude/audit/signal-recorder-silent-detections.log (silent verdicts)
# Test: /usr/bin/python3 hooks/tests/test_signal_recorder_silent_check.py
#
# Spec: Workspaces/.context/DECISIONS.md WS-DDR-098, amended in part by WS-DDR-150
# Signals: .intent/signals/SIG-2026-05-26-flight-model-ingestion.md (origin);
#   Workspaces/.intent/signals/SIG-WITNESS-COVERAGE-GAP-AND-DEAD-RECORDER-HOOK-2026-09-25.md
# Created 2026-05-26; path lookup fixed 2026-09-25 (ecb2e60); Witness measure 2026-09-25.

import json
import os
import sys
import time

BYPASS = "SIGNAL_RECORDER_SILENT_BYPASSED"
STALE_DAYS = 30
DAY_S = 86400
WARN_TTL = 7 * DAY_S
REFRESH_EVERY_S = 24 * 3600
KICK_EVERY_S = 3600

HOME = os.environ.get("HOME") or os.path.expanduser("~")
AUDIT_LOG = os.path.join(HOME, ".claude", "audit", "signal-recorder-silent-detections.log")
TELEMETRY_LOG = os.path.join(HOME, ".claude", "logs", "signal-recorder-silent.jsonl")
WARN_STATE = os.path.join(HOME, ".claude", "state", "signal-recorder-silent-warned.json")
HOOK_DIR = os.path.dirname(os.path.realpath(__file__))
BUILDER = os.path.join(HOOK_DIR, "witness_source_index.py")
HOOK_NAME = "signal-recorder-silent-check"
_VERDICTS = ("recorder-active", "silent-recorder", "nonconformant-events")
_EMIT_SUPPLIES = ("ts", "product", "event", "caller", "machine", "outcome", "run_id")
FIRE = {}  # the last telemetry row of this fire, reported to Witness when the fire ends
SESSION = {"id": ""}  # the hook input's session_id, for the same report


def _now_iso(now):
    return time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime(now))


def _append(path, line):
    try:
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "a", encoding="utf-8") as fh:
            fh.write(line + "\n")
    except Exception:
        pass


def _telemetry(now, **row):
    out = {"ts": _now_iso(now)}
    out.update(row)
    FIRE.clear()
    FIRE.update(out)
    _append(TELEMETRY_LOG, json.dumps(out, separators=(",", ":")))


_SCOPE_ROOTS = (("Core", "products"), ("Core", "frameworks"), ("Home",))


def _tree_product_root(path):
    """The product folder a path sits in, read from its place in the tree (WS-DDR-150 scope).

    Core/products/<name>, Core/frameworks/<name> and Home/<name> are products whether or
    not they carry a .intent/ directory. Names starting with "_" or "." (the intake area,
    hidden folders) are not products. Returns "" when the path is not under one of them.
    """
    parts = os.path.normpath(os.path.abspath(path)).split(os.sep)
    for i in range(len(parts) - 1, -1, -1):
        for root in _SCOPE_ROOTS:
            n = len(root)
            if tuple(parts[i:i + n]) == root and len(parts) > i + n:
                name = parts[i + n]
                if name and not name.startswith(("_", ".")) and len(parts) > i + n + 1:
                    return os.sep.join(parts[:i + n + 1]) or os.sep
    return ""


def _resolve_product(tool_input):
    """(product_dir, in_rule_scope) for the tool's target path.

    A path under Core/products, Core/frameworks or Home resolves to its product folder and
    is in scope of WS-DDR-150 (everything built). Anything else falls back to the nearest
    ancestor holding a .intent/ directory, gated as before on an autonomy declaration.
    """
    if not isinstance(tool_input, dict):
        return "", False
    path = tool_input.get("file_path") or tool_input.get("path") or tool_input.get("notebook_path")
    if not path and isinstance(tool_input.get("command"), str):
        for tok in tool_input["command"].split():
            tok = tok.strip("'\"")
            if tok.startswith("/") and os.path.exists(tok):
                path = tok
                break
    if not isinstance(path, str) or not path or not os.path.exists(path):
        return "", False
    tree_root = _tree_product_root(path)
    if tree_root:
        return tree_root, True
    cur = os.path.dirname(os.path.abspath(path))
    while cur and cur != "/":
        if os.path.isdir(os.path.join(cur, ".intent")):
            return cur, False
        cur = os.path.dirname(cur)
    return "", False


def _is_engagement(work_dir):
    parts = work_dir.split(os.sep)
    for i, p in enumerate(parts):
        if p == "Work" and len(parts) > i + 2 and parts[i + 2] == "Engagements":
            return True
    return False


def _kick_refresh(index_path, now):
    """Start the index builder detached, at most once an hour. Never waits."""
    if os.environ.get("WITNESS_INDEX_NO_REFRESH") == "1" or not os.path.isfile(BUILDER):
        return False
    stamp = index_path + ".kick"
    try:
        if now - os.path.getmtime(stamp) < KICK_EVERY_S:
            return False
    except OSError:
        pass
    try:
        os.makedirs(os.path.dirname(stamp), exist_ok=True)
        with open(stamp, "a"):
            pass
        os.utime(stamp, (now, now))
        import subprocess
        env = dict(os.environ, WITNESS_CALLER=f"hook:{HOOK_NAME}")
        subprocess.Popen([sys.executable, BUILDER, "--quiet"], stdin=subprocess.DEVNULL,
                         stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
                         close_fds=True, start_new_session=True, env=env)
        return True
    except Exception:
        return False


def _already_warned(session_id, work_dir, now):
    """True when this session was already told about work_dir; records it otherwise."""
    if not session_id:
        return False
    try:
        with open(WARN_STATE, "r", encoding="utf-8") as fh:
            state = json.load(fh)
        if not isinstance(state, dict):
            state = {}
    except Exception:
        state = {}
    state = {s: v for s, v in state.items()
             if isinstance(v, dict) and any(isinstance(t, (int, float)) and now - t < WARN_TTL
                                            for t in v.values())}
    seen = state.setdefault(session_id, {})
    if work_dir in seen:
        return True
    seen[work_dir] = now
    try:
        os.makedirs(os.path.dirname(WARN_STATE), exist_ok=True)
        tmp = f"{WARN_STATE}.tmp.{os.getpid()}"
        with open(tmp, "w", encoding="utf-8") as fh:
            json.dump(state, fh)
        os.replace(tmp, WARN_STATE)
    except Exception:
        pass
    return False


def _handle(raw, now):
    try:
        payload = json.loads(raw or "{}")
    except Exception:
        payload = {}
    if not isinstance(payload, dict):
        payload = {}
    session_id = payload.get("session_id") or os.environ.get("CLAUDE_SESSION_ID") or ""
    SESSION["id"] = session_id
    work_dir, in_scope = _resolve_product(payload.get("tool_input"))
    if not work_dir:
        _telemetry(now, work_dir="", detection="no-context", outcome="skip")
        return 0
    if _is_engagement(work_dir):
        _telemetry(now, work_dir=work_dir, detection="engagement-exempt", outcome="skip")
        return 0
    try:
        with open(os.path.join(work_dir, ".intent", "INTENT.md"), "r", encoding="utf-8",
                  errors="replace") as fh:
            intent_md = fh.read()
    except OSError:
        intent_md = ""

    sys.path.insert(0, HOOK_DIR)
    import witness_source_index as wsi

    declares = wsi.declares_autonomy(intent_md)
    if not declares and not in_scope:
        _telemetry(now, work_dir=work_dir, detection="no-lambda-declaration", outcome="skip")
        return 0
    no_actions = wsi.declared_no_actions(intent_md) if hasattr(wsi, "declared_no_actions") else None
    if no_actions:
        _telemetry(now, work_dir=work_dir, detection="no-actions-declared", outcome="skip",
                   reason=no_actions[:200])
        return 0
    names, names_from = wsi.product_names(work_dir, intent_md)
    index_path = wsi.index_path()
    index, problem = wsi.load_index(index_path)
    if problem:
        kicked = _kick_refresh(index_path, now)
        _telemetry(now, work_dir=work_dir, detection=f"witness-index-{problem}", outcome="skip",
                   names=names, refresh_kicked=kicked)
        return 0
    index_age_h = round((now - index["built_at_epoch"]) / 3600, 1)
    kicked = _kick_refresh(index_path, now) if index_age_h * 3600 > REFRESH_EVERY_S else False
    hit = wsi.lookup(index, names)
    last = hit["last_event_epoch"]
    last_days = None if last is None else max(0, int((now - last) // DAY_S))
    base = dict(work_dir=work_dir, names=names, names_from=names_from, last_event_days=last_days,
                count_30d=hit["count_30d"], index_age_h=index_age_h, refresh_kicked=kicked)
    lint = hit.get("lint")
    rule = (lint or {}).get("rule") or {}
    if lint is not None:
        base.update(lint_events=rule.get("events"), lint_nonconformant=rule.get("nonconformant"),
                    lint_most_missing=rule.get("most_missing"),
                    lint_legacy_events=((lint.get("legacy") or {}).get("events")))
    if last is not None and now - last <= STALE_DAYS * DAY_S:
        if not wsi.mostly_nonconformant(rule):
            _telemetry(now, detection="recorder-active", outcome="skip", **base)
            return 0
        # Active, but most of what it reports lacks the minimum fields (WS-DDR-150).
        if _already_warned(session_id, work_dir + "#fields", now):
            _telemetry(now, detection="nonconformant-events", outcome="warn-suppressed", **base)
            return 0
        _telemetry(now, detection="nonconformant-events", outcome="warn", **base)
        product = os.path.basename(work_dir)
        field = rule.get("most_missing") or "caller"
        emit_py = wsi.emit_path()
        # emit.py supplies ts, product, event, caller, machine, outcome and run_id itself;
        # duration_ms and redaction_level come from the caller. A product missing any field
        # emit.py supplies is not using it yet, so the remedy is emit.py; one already using
        # it is told which argument to pass.
        missing = rule.get("missing") or {}
        if any(missing.get(f) for f in _EMIT_SUPPLIES):
            how = f"so have {product} report through {emit_py}, which supplies every required field when given duration_ms"
        elif field == "redaction_level":
            how = f"so have {product} pass redaction_level client-confidential to {emit_py} for engagement work"
        elif field == "duration_ms":
            how = f"so have {product} pass duration_ms to {emit_py} with each action"
        else:
            how = f"so have {product} report through {emit_py}, which supplies every required field when given duration_ms"
        context = (
            f"[Witness field check, WS-DDR-150] Most of {product}'s events in Witness over the last "
            f"{STALE_DAYS} days ({rule.get('nonconformant')} of {rule.get('events')}) lack fields the rule "
            f"requires, most often {field}, {how}."
        )
        user_line = (f"Witness field check: most of {product}'s recent Witness events lack {field} "
                     f"(WS-DDR-150); report through emit.py.")
        print(json.dumps({"hookSpecificOutput": {"hookEventName": "PreToolUse", "additionalContext": context},
                          "systemMessage": user_line}))
        return 0

    last_txt = "never" if last is None else f"{wsi.iso(last)}, {last_days} days ago"
    _append(AUDIT_LOG, f"[{_now_iso(now)}] SILENT-RECORDER work_dir={work_dir} names={','.join(names)} "
                       f"last_event={last_txt.replace(' ', '_')} declares_lambda={1 if declares else 0}")
    if _already_warned(session_id, work_dir, now):
        _telemetry(now, detection="silent-recorder", outcome="warn-suppressed", **base)
        return 0
    _telemetry(now, detection="silent-recorder", outcome="warn", **base)
    product = os.path.basename(work_dir)
    how = "declared in INTENT.md" if names_from == "declared" else "the directory name, no witness_source_system declared"
    context = (
        f"[Witness recorder check, WS-DDR-150] {product} ({work_dir}) "
        f"{'declares autonomy settings in .intent/INTENT.md' if declares else 'is a product, and everything built reports its actions to Witness'}, "
        f"but Witness holds no event from it in the last {STALE_DAYS} days. "
        f"Names checked: {', '.join(names)} ({how}). Last event: {last_txt}. "
        f"Index built {index.get('built_at')} from the Witness store. "
        f"Everything built reports its actions to Witness (WS-DDR-150). If this session changes what "
        f"{product} does, have it report each action through the shared emit call, {wsi.emit_path()}, "
        f"under the name {names[0]}, passing duration_ms; emit.py then gives every event the minimum fields "
        f"the rule requires, which lines appended to .intent/events files do not. If it already reports "
        f"under another name, "
        f"declare witness_source_system: in its INTENT.md. If it has no actions of its own (a content "
        f"or methodology repo), declare witness_actions: none (<named reason>) there instead. Warn-only: the tool call proceeds, and this "
        f"note appears once per session per product."
    )
    user_line = (f"Witness recorder check: {product} sent Witness no event in {STALE_DAYS} days "
                 f"(last: {last_txt}); WS-DDR-150 asks every product to report its actions.")
    print(json.dumps({"hookSpecificOutput": {"hookEventName": "PreToolUse", "additionalContext": context},
                      "systemMessage": user_line}))
    return 0


def _emit_fire(session_id, started):
    """Report this fire to Witness: one hook.fire event through emit.py. Never raises."""
    try:
        if HOOK_DIR not in sys.path:
            sys.path.insert(0, HOOK_DIR)
        import witness_source_index as wsi
        detection = FIRE.get("detection") or "unknown"
        outcome = "error" if detection == "hook-error" else ("ok" if detection in _VERDICTS else "skipped")
        fields = {"hook": HOOK_NAME, "detection": detection, "told_session": FIRE.get("outcome") == "warn"}
        if session_id:
            fields["session"] = session_id
        work_dir = FIRE.get("work_dir") or ""
        if work_dir and _is_engagement(work_dir):
            import hashlib
            fields["target"] = "sha256:" + hashlib.sha256(work_dir.encode("utf-8")).hexdigest()[:16]
            fields["redaction_level"] = "client-confidential"
        elif work_dir:
            fields["target"] = os.path.basename(work_dir)
        for k in ("count_30d", "lint_events", "lint_nonconformant", "lint_most_missing"):
            if FIRE.get(k) is not None:
                fields[k] = FIRE[k]
        wsi.emit_action("hook.fire", caller=f"hook:{HOOK_NAME}", outcome=outcome,
                        duration_ms=(time.perf_counter() - started) * 1000, **fields)
    except Exception:
        pass


def main():
    if os.environ.get(BYPASS) == "1":
        return 0
    started = time.perf_counter()
    now = time.time()
    try:
        raw = sys.stdin.read()
    except Exception:
        raw = ""
    try:
        return _handle(raw, now)
    except Exception as e:  # a recorder check must never wedge a write
        _telemetry(now, detection="hook-error", outcome="skip", error=f"{type(e).__name__}: {e}"[:300])
        return 0
    finally:
        _emit_fire(SESSION["id"], started)


if __name__ == "__main__":
    sys.exit(main())
