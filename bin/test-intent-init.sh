#!/usr/bin/env bash
#
# test-intent-init.sh — end-to-end harness for bin/intent-init
#
# Builds a temp "Workspaces-like" root, runs intent-init against fake products
# and engagements, asserts the 7 DEC-011 behaviors. Cleans up on exit.
#
# Usage: bin/test-intent-init.sh
# Exit:  0 = all PASS, 1 = any FAIL.

set -u

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
INTENT_INIT="$SCRIPT_DIR/intent-init"
FRAMEWORK_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"

PASS=0
FAIL=0
FAIL_DETAILS=()

note()   { printf '  %s\n' "$*"; }
ok()     { PASS=$((PASS+1)); printf '  PASS  %s\n' "$*"; }
nope()   { FAIL=$((FAIL+1)); FAIL_DETAILS+=("$*"); printf '  FAIL  %s\n' "$*"; }

assert_eq() {
  # assert_eq <label> <expected> <actual>
  if [[ "$2" == "$3" ]]; then ok "$1"; else nope "$1 (expected $2 got $3)"; fi
}

assert_file() {
  if [[ -f "$2" ]]; then ok "$1"; else nope "$1 (missing: $2)"; fi
}

assert_dir() {
  if [[ -d "$2" ]]; then ok "$1"; else nope "$1 (missing: $2)"; fi
}

assert_contains() {
  # assert_contains <label> <substring> <file>
  if grep -qF -- "$2" "$3" 2>/dev/null; then
    ok "$1"
  else
    nope "$1 (missing '$2' in $3)"
  fi
}

assert_not_contains() {
  if grep -qF -- "$2" "$3" 2>/dev/null; then
    nope "$1 (unexpectedly found '$2' in $3)"
  else
    ok "$1"
  fi
}

# Build temp Workspaces root
ROOT="$(mktemp -d -t intent-init-test-XXXXXX)"
trap 'rm -rf "$ROOT"' EXIT

mkdir -p "$ROOT/Core/products" "$ROOT/Core/engagements" "$ROOT/Core/products/witness/.intent"
# Provide a session-end hook so the install step has a real source to copy.
mkdir -p "$ROOT/Core/frameworks/intent/hooks"
cat > "$ROOT/Core/frameworks/intent/hooks/session-end.sh" <<'HOOK'
#!/usr/bin/env bash
# fixture session-end hook for test harness
exit 0
HOOK
chmod +x "$ROOT/Core/frameworks/intent/hooks/session-end.sh"

export INTENT_INIT_ROOT="$ROOT"

printf '\n=== Test 1: internal-tier product (default classification, default federation) ===\n'
OUT="$("$INTENT_INIT" my-product --path Core/products/my-product --dry-run 2>&1)"
RC=$?
assert_eq "exit code 0" "0" "$RC"

PRODUCT_ROOT="$ROOT/Core/products/my-product"
assert_dir   "creates .intent/events"    "$PRODUCT_ROOT/.intent/events"
assert_dir   "creates .intent/signals"   "$PRODUCT_ROOT/.intent/signals"
assert_dir   "creates .intent/intents"   "$PRODUCT_ROOT/.intent/intents"
assert_dir   "creates .intent/specs"     "$PRODUCT_ROOT/.intent/specs"
assert_dir   "creates .entire/"          "$PRODUCT_ROOT/.entire"
assert_file  "writes classification.yaml" "$PRODUCT_ROOT/.intent/classification.yaml"
assert_contains "classification tier = internal" "tier: internal" "$PRODUCT_ROOT/.intent/classification.yaml"
assert_file  "installs session-end hook" "$PRODUCT_ROOT/.claude/hooks/session-end"
[[ -x "$PRODUCT_ROOT/.claude/hooks/session-end" ]] && ok "session-end hook is executable" \
  || nope "session-end hook is not executable"

# Stop-hook registration in .claude/settings.local.json
assert_file  "writes .claude/settings.local.json" "$PRODUCT_ROOT/.claude/settings.local.json"
assert_contains "registers Stop hook" '"Stop"' "$PRODUCT_ROOT/.claude/settings.local.json"
assert_contains "registers session-end command" 'CLAUDE_PROJECT_DIR/.claude/hooks/session-end' "$PRODUCT_ROOT/.claude/settings.local.json"

# Idempotency: re-running should not duplicate the Stop-hook entry
RERUN_OUT="$("$INTENT_INIT" my-product --path Core/products/my-product --classification internal --dry-run 2>&1)"
STOP_COUNT=$(grep -c '"Stop"' "$PRODUCT_ROOT/.claude/settings.local.json")
[[ "$STOP_COUNT" -eq 1 ]] && ok "Stop-hook registration is idempotent (single entry after re-run)" \
  || nope "Stop-hook duplicated on re-run (count=$STOP_COUNT)"
echo "$RERUN_OUT" | grep -q "already registered" && ok "re-run reports 'already registered'" \
  || nope "re-run did not detect existing Stop-hook registration"

assert_file  "appends Core/products/products.json" "$ROOT/Core/products/products.json"
assert_contains "products.json mentions name" '"name": "my-product"' "$ROOT/Core/products/products.json"
assert_contains "products.json carries classification" '"classification": "internal"' "$ROOT/Core/products/products.json"

assert_file  "appends Witness registered-products.yaml" "$ROOT/Core/products/witness/.intent/registered-products.yaml"
assert_contains "witness registry mentions product" "product: my-product" "$ROOT/Core/products/witness/.intent/registered-products.yaml"
assert_contains "witness registry tags classification" "classification: internal" "$ROOT/Core/products/witness/.intent/registered-products.yaml"
assert_contains "witness registry sources entire-io" "type: entire-io" "$ROOT/Core/products/witness/.intent/registered-products.yaml"
assert_contains "witness registry sources intent-events" "type: intent-events" "$ROOT/Core/products/witness/.intent/registered-products.yaml"

echo "$OUT" | grep -q "Federation: ON" && ok "echo says Federation: ON" \
  || nope "echo missing 'Federation: ON' (got: $(echo "$OUT" | tail -1))"

printf '\n=== Test 2: confidential engagement (federation deferred) ===\n'
OUT="$("$INTENT_INIT" subaru-q3-2026 --path Core/engagements/subaru-q3-2026 \
       --classification confidential:subaru --dry-run 2>&1)"
RC=$?
assert_eq "exit code 0" "0" "$RC"

ENG_ROOT="$ROOT/Core/engagements/subaru-q3-2026"
assert_file "engagement classification.yaml" "$ENG_ROOT/.intent/classification.yaml"
assert_contains "engagement tier value" "tier: confidential:subaru" "$ENG_ROOT/.intent/classification.yaml"
assert_file "engagements.json written" "$ROOT/Core/engagements/engagements.json"
assert_contains "engagements.json mentions name" '"name": "subaru-q3-2026"' "$ROOT/Core/engagements/engagements.json"

# Witness registry must NOT carry this engagement
if grep -q "product: subaru-q3-2026" "$ROOT/Core/products/witness/.intent/registered-products.yaml" 2>/dev/null; then
  nope "engagement should not appear in Witness registry"
else
  ok "engagement absent from Witness registry (federation deferred)"
fi
echo "$OUT" | grep -q "Federation: DEFERRED" && ok "echo says Federation: DEFERRED" \
  || nope "echo missing 'Federation: DEFERRED'"

printf '\n=== Test 3: engagement path without --classification rejected ===\n'
OUT="$("$INTENT_INIT" no-class-engagement --path Core/engagements/no-class-engagement --dry-run 2>&1)"
RC=$?
assert_eq "exit code 1 on missing classification" "1" "$RC"
echo "$OUT" | grep -qi "engagement-shaped path" && ok "error message names engagement-shaped path" \
  || nope "error did not mention engagement-shaped path"

printf '\n=== Test 4: idempotent re-run on same product ===\n'
OUT="$("$INTENT_INIT" my-product --path Core/products/my-product --dry-run 2>&1)"
RC=$?
assert_eq "second run exits 0" "0" "$RC"
echo "$OUT" | grep -q "already present" && ok "re-run reports already-present state" \
  || nope "re-run did not surface idempotency"

# Confirm registries still single-entry
PRODUCT_COUNT="$(python3 -c "import json; print(sum(1 for e in json.load(open('$ROOT/Core/products/products.json')) if e['name']=='my-product'))")"
assert_eq "products.json has exactly 1 entry for my-product" "1" "$PRODUCT_COUNT"
WITNESS_COUNT="$(grep -c "product: my-product" "$ROOT/Core/products/witness/.intent/registered-products.yaml")"
assert_eq "witness registry has exactly 1 entry for my-product" "1" "$WITNESS_COUNT"

printf '\n=== Test 5: tier mismatch on re-run is refused ===\n'
OUT="$("$INTENT_INIT" my-product --path Core/products/my-product --classification public --dry-run 2>&1)"
RC=$?
assert_eq "tier mismatch exits 1" "1" "$RC"
echo "$OUT" | grep -qi "refusing to overwrite" && ok "tier mismatch surfaces refusal" \
  || nope "tier mismatch error not surfaced"

printf '\n=== Test 6: invalid classification value rejected ===\n'
OUT="$("$INTENT_INIT" bad-tier --path Core/products/bad-tier --classification top-secret --dry-run 2>&1)"
RC=$?
assert_eq "invalid classification exits 1" "1" "$RC"
echo "$OUT" | grep -qi "not one of" && ok "invalid classification message clear" \
  || nope "invalid classification message missing"

printf '\n=== Test 7: public-tier product still federates ===\n'
OUT="$("$INTENT_INIT" open-product --path Core/products/open-product --classification public --dry-run 2>&1)"
RC=$?
assert_eq "exit code 0" "0" "$RC"
assert_contains "public classification recorded" "tier: public" "$ROOT/Core/products/open-product/.intent/classification.yaml"
assert_contains "public product in Witness registry" "product: open-product" "$ROOT/Core/products/witness/.intent/registered-products.yaml"
echo "$OUT" | grep -q "Federation: ON" && ok "public tier federates Day 1" \
  || nope "public tier did not federate"

printf '\n=========================================\n'
printf 'Result: %d PASS / %d FAIL\n' "$PASS" "$FAIL"
if (( FAIL > 0 )); then
  printf '\nFailures:\n'
  for d in "${FAIL_DETAILS[@]}"; do printf '  - %s\n' "$d"; done
  exit 1
fi
exit 0
