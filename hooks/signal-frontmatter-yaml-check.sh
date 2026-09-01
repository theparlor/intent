#!/usr/bin/env bash
# signal-frontmatter-yaml-check.sh
#
# PreToolUse hook — authoring-time YAML gate for signal frontmatter.
#
# Inspects Write/Edit tool calls targeting `*/.intent/signals/*.md`. If the
# resulting file's frontmatter block would not parse as a YAML mapping, the
# write is blocked with the exact parse error. This is the fleet-wide
# upstream control for the failure class landed 2026-09-01 in fieldbook
# (PRs #4/#5): an unquoted plain scalar containing a colon-space made two
# signal files' frontmatter unparseable, so the signalbox collector counted
# them in errors[] and could not read their status for weeks.
#
# Layering: this hook gates authoring time on any hooked surface (fleet);
# fieldbook's tests/test_signal_frontmatter.py gates merge time (that repo);
# the signalbox collector-signals errors[] remains the scan-time catch-net
# for surfaces running without the hook fabric (Cowork, chat).
#
# Edit calls are validated by reconstruction: read the on-disk file, apply
# the old_string -> new_string replacement, validate the result. If the file
# cannot be read or old_string is absent, fail open (the Edit itself will
# error anyway).
#
# Fixtures exemption (SIG-2026-07-19-fixtures-exemption-ruled, same rule as
# closure-discipline-signal-check.sh): exempt ONLY when the path contains a
# fixtures directory segment AND the content carries an explicit
# inert-test-data marker. Exemption use is logged, never silent.
#
# Install: chmod +x and symlink to ~/.claude/hooks/
# Register: PreToolUse entry in ~/.claude/settings.json, matcher "Write|Edit"
#
# Bypass: SIGNAL_FRONTMATTER_YAML_BYPASSED=1 (logged)
# Audit log: ~/.claude/audit/signal-frontmatter-yaml-detections.log
#
# Created: 2026-09-01

set -u

AUDIT_LOG="$HOME/.claude/audit/signal-frontmatter-yaml-detections.log"
mkdir -p "$(dirname "$AUDIT_LOG")" 2>/dev/null || true

if [ "${SIGNAL_FRONTMATTER_YAML_BYPASSED:-0}" = "1" ]; then
  echo "[bypassed]" >> "$AUDIT_LOG"
  exit 0
fi

INPUT=$(cat)

VERDICT=$(printf '%s' "$INPUT" | python3 -c '
import json, re, sys

def out(tag, detail=""):
    print(json.dumps({"tag": tag, "detail": detail}))
    sys.exit(0)

try:
    raw = json.loads(sys.stdin.read() or "{}")
    tn = raw.get("tool_name", "")
    ti = raw.get("tool_input", {}) or {}
    fp = ti.get("file_path", "") or ""

    if tn not in ("Write", "Edit"):
        out("OK")
    if not re.search(r"/\.?intent/signals/[^/]+\.md$", fp):
        out("OK")

    # Fixtures exemption: fixtures path segment AND inert marker in content.
    comps = [c for c in fp.split("/") if c]
    has_fixtures = False
    for i, c in enumerate(comps):
        if c in ("fixtures", "__fixtures__"):
            has_fixtures = True
            break
        if c == "tests" and i + 1 < len(comps) and comps[i + 1] == "fixtures":
            has_fixtures = True
            break
    marker_src = (ti.get("content", "") or "") + (ti.get("new_string", "") or "")
    markers = ("inert-test-data", "inert fixture", "deliberately-malformed test fixture")
    if has_fixtures and any(m in marker_src.lower() for m in markers):
        out("FIXTURE-EXEMPT")

    # Reconstruct the post-write content.
    if tn == "Write":
        content = ti.get("content", "")
        if not isinstance(content, str) or not content:
            out("OK")
    else:
        old = ti.get("old_string", "")
        new = ti.get("new_string", "")
        if not isinstance(old, str) or not old:
            out("OK")
        try:
            with open(fp, encoding="utf-8") as f:
                current = f.read()
        except OSError:
            out("OK")
        if old not in current:
            out("OK")
        if ti.get("replace_all"):
            content = current.replace(old, new)
        else:
            content = current.replace(old, new, 1)

    lines = content.split("\n")
    if not lines or lines[0].strip() != "---":
        # No frontmatter block: not this gate\x27s concern; contract tests
        # and the collector own frontmatter-presence enforcement.
        out("OK")
    close = None
    for i, line in enumerate(lines[1:], start=1):
        if line.strip() == "---":
            close = i
            break
    if close is None:
        out("BLOCK", "opening frontmatter fence (---) is never closed")

    block = "\n".join(lines[1:close])
    try:
        import yaml
    except ImportError:
        out("OK")  # fail open if runtime lacks pyyaml
    try:
        parsed = yaml.safe_load(block)
    except yaml.YAMLError as exc:
        out("BLOCK", "frontmatter is not valid YAML: " + str(exc).replace("\n", " ")[:400])
    if not isinstance(parsed, dict):
        out("BLOCK", "frontmatter parsed to " + type(parsed).__name__ + ", expected a mapping")
    out("OK")
except SystemExit:
    raise
except Exception:
    print(json.dumps({"tag": "OK", "detail": "fail-open"}))
')

TAG=$(printf '%s' "$VERDICT" | python3 -c 'import json,sys; print(json.loads(sys.stdin.read() or "{}").get("tag","OK"))' 2>/dev/null || echo OK)
DETAIL=$(printf '%s' "$VERDICT" | python3 -c 'import json,sys; print(json.loads(sys.stdin.read() or "{}").get("detail",""))' 2>/dev/null || echo "")
TIMESTAMP=$(date -u +%Y-%m-%dT%H:%M:%SZ)
FILE_PATH=$(printf '%s' "$INPUT" | python3 -c 'import json,sys; print((json.loads(sys.stdin.read() or "{}").get("tool_input") or {}).get("file_path",""))' 2>/dev/null || echo "")

case "$TAG" in
  FIXTURE-EXEMPT)
    echo "[$TIMESTAMP] FIXTURE-EXEMPT file=$FILE_PATH" >> "$AUDIT_LOG"
    exit 0
    ;;
  BLOCK)
    echo "[$TIMESTAMP] CAUGHT file=$FILE_PATH detail=$DETAIL" >> "$AUDIT_LOG"
    REASON="SIGNAL-FRONTMATTER YAML GATE: this write would leave the signal file's frontmatter unreadable by every downstream consumer (signalbox collector, status greps, closure audits). Problem: ${DETAIL}. Most common cause: an unquoted value containing colon-space, e.g. a catch_mechanism or upstream_control_path sentence. Fix: convert the offending value to a folded block scalar ('field: >-' then the text indented two spaces) or quote it. Bypass for legitimate cases: SIGNAL_FRONTMATTER_YAML_BYPASSED=1 (logged)."
    printf '%s' "$REASON" | python3 -c 'import json,sys; print(json.dumps({"decision":"block","reason":sys.stdin.read()}))'
    exit 0
    ;;
  *)
    exit 0
    ;;
esac
