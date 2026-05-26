#!/usr/bin/env bash
# spec-age-lint.sh
#
# Spec-age lint — identifies `.intent/specs/*.md` files with
# `status: approved` or `status: ratified` that have no corresponding
# code in `src/` or `bin/`, and have been stale for more than
# SPEC_AGE_THRESHOLD_DAYS (default 30).
#
# Emits one signal per stale spec to `.intent/signals/`.
#
# Usage:
#   spec-age-lint.sh [--threshold N]   # override default 30-day threshold
#   spec-age-lint.sh --dry-run         # print stale specs without emitting signals
#
# Addresses: Upgrade Plan 2026-05-20, Track B, Item B3
# Gap: "spec-vs-implementation gap accumulation — specs that age without
# triggering IDD execute loops"
#
# Install:
#   chmod +x hooks/spec-age-lint.sh
#   # Run manually or via scheduled task; NOT a realtime hook
#   # (volume-based, not per-turn)
#
# Created: 2026-05-20

set -euo pipefail

THRESHOLD_DAYS="${SPEC_AGE_THRESHOLD_DAYS:-30}"
DRY_RUN=0
INTENT_ROOT=""

# Parse args
for arg in "$@"; do
  case "$arg" in
    --threshold) THRESHOLD_DAYS="${2:-30}"; shift ;;
    --threshold=*) THRESHOLD_DAYS="${arg#*=}" ;;
    --dry-run) DRY_RUN=1 ;;
  esac
done

# Find intent root (walk up from CWD)
find_intent_root() {
  local dir="$PWD"
  while [ "$dir" != "/" ]; do
    if [ -d "$dir/.intent" ]; then
      echo "$dir"
      return 0
    fi
    dir="$(dirname "$dir")"
  done
  return 1
}

INTENT_ROOT=$(find_intent_root 2>/dev/null) || {
  echo "spec-age-lint: no .intent/ directory found in $PWD or ancestors. Run from an intent repo." >&2
  exit 0
}

SPECS_DIR="$INTENT_ROOT/.intent/specs"
SIGNALS_DIR="$INTENT_ROOT/.intent/signals"
SRC_DIR="$INTENT_ROOT/src"
BIN_DIR="$INTENT_ROOT/bin"

[ -d "$SPECS_DIR" ] || { echo "spec-age-lint: $SPECS_DIR not found"; exit 0; }

STALE_COUNT=0
EMITTED_COUNT=0
NOW=$(date +%s)
THRESHOLD_SECS=$(( THRESHOLD_DAYS * 86400 ))

for spec_file in "$SPECS_DIR"/*.md; do
  [ -f "$spec_file" ] || continue

  # Check status field
  status=$(grep -m1 '^status:' "$spec_file" 2>/dev/null | awk '{print $2}' | tr -d "'" | tr -d '"')
  case "$status" in
    approved|ratified) ;;
    *) continue ;;
  esac

  # Check age
  file_mtime=$(stat -f %m "$spec_file" 2>/dev/null || stat -c %Y "$spec_file" 2>/dev/null)
  age_secs=$(( NOW - file_mtime ))
  if [ "$age_secs" -lt "$THRESHOLD_SECS" ]; then
    continue
  fi

  # Derive a slug from spec ID (first `id:` field, else filename)
  spec_id=$(grep -m1 '^id:' "$spec_file" 2>/dev/null | awk '{print $2}' | tr -d "'" | tr -d '"')
  spec_slug=$(basename "$spec_file" .md)
  [ -n "$spec_id" ] && spec_slug="$spec_id"

  # Check for corresponding implementation: src/ or bin/
  # Heuristic: any file in src/ or bin/ whose name contains a normalized slug fragment
  slug_fragment=$(echo "$spec_slug" | sed 's/^SPEC-[0-9]*-//' | tr '[:upper:]' '[:lower:]' | tr '-' '_')
  has_impl=0
  if find "$SRC_DIR" "$BIN_DIR" -type f 2>/dev/null | grep -qi "$slug_fragment" 2>/dev/null; then
    has_impl=1
  fi

  [ "$has_impl" = "1" ] && continue

  # Stale spec with no implementation
  STALE_COUNT=$(( STALE_COUNT + 1 ))
  age_days=$(( age_secs / 86400 ))
  title=$(grep -m1 '^title:' "$spec_file" 2>/dev/null | sed 's/^title:[ ]*//' | tr -d "'" | tr -d '"')
  [ -z "$title" ] && title="$spec_slug"

  if [ "$DRY_RUN" = "1" ]; then
    echo "STALE ($age_days days): $spec_slug — $title"
    continue
  fi

  # Emit signal
  today=$(date +%Y-%m-%d)
  signal_file="$SIGNALS_DIR/SIG-SPEC-AGE-${spec_slug}-${today}.md"

  # Skip if signal already exists for this spec today
  [ -f "$signal_file" ] && continue

  cat > "$signal_file" << SIGNAL_EOF
---
id: SIG-SPEC-AGE-${spec_slug}-${today}
title: Spec-age alert — ${title} (${age_days} days since last edit, no implementation found)
type: signal
status: captured
confidence: 0.80
trust: 0.75
autonomy_level: L4
source: spec-age-lint
date: '${today}'
upstream_control_path: SIG-SPEC-AGE-${spec_slug}-${today}.md — triggers IDD Execute loop for this spec
catch_mechanism: IDD Execute loop with DoR/DoD gates; spec-age-lint re-runs to verify implementation landed
pipeline_survival: spec-age-lint.sh runs periodically; will re-emit if spec remains unimplemented after threshold
---

# Spec-Age Alert: ${title}

## What Was Noticed

Spec \`${spec_slug}\` has status \`${status}\` and was last modified **${age_days} days ago**
(threshold: ${THRESHOLD_DAYS} days). No corresponding implementation was found in \`src/\` or \`bin/\`.

This spec has been approved/ratified but has not triggered an IDD Execute loop.

## Spec File
\`${spec_file}\`

## Action
Open a dedicated IDD Execute session for this spec. Read the spec in full, write DoR + DoD,
then implement. Use \`spawn-prompts/idd-build-execute.md\` with this signal as the Notice source.

## Do Not Implement Inline
The spec may require architectural review before implementation begins. Open an IDD loop.
SIGNAL_EOF

  EMITTED_COUNT=$(( EMITTED_COUNT + 1 ))
  echo "spec-age-lint: emitted signal for stale spec: $spec_slug ($age_days days)"
done

if [ "$DRY_RUN" = "0" ]; then
  echo "spec-age-lint: $STALE_COUNT stale specs found, $EMITTED_COUNT signals emitted"
fi
