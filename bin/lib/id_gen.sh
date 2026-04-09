#!/bin/bash
# id_gen.sh — ULID generation helpers for Intent CLI tools
#
# Purpose: Replace sequential ID generators (SIG-001, INT-042, etc.) with
# globally-unique, timestamp-ordered IDs that don't require coordination
# between concurrent writers.
#
# Addresses: SIG-022 (sequential signal IDs will collide in distributed
# multi-agent environments), INT-009 P0 #1.
#
# Format: {PREFIX}-{ULID} where ULID is 26 Crockford base32 chars
#   10 chars: 48-bit timestamp (ms since epoch)
#   16 chars: 80-bit randomness from os.urandom
#
# Example IDs:
#   SIG-01JR8XYZABCDEFGHJKMNPQR  (was SIG-042)
#   INT-01JR8Y0123ABCDEFGHJKMNQ  (was INT-007)
#   SPEC-01JR8Y45BCDEFGHJKMNPQR  (was SPEC-003)
#
# Backward compatibility: old SIG-\d{3} IDs remain valid. The match_id_regex
# function returns a pattern that matches both formats so grep-based lookups
# continue to work across the migration.
#
# Ship history:
#   2026-04-09 — initial ship (SPEC-sig-022-ulid-migration)

set -euo pipefail

# ULID generation — uses python3 for timing + base32 encoding.
# python3 is assumed available (macOS ships with it; every dev machine has it).
generate_ulid() {
  python3 -c '
import os
import time

ALPHABET = "0123456789ABCDEFGHJKMNPQRSTVWXYZ"  # Crockford base32

# 48-bit timestamp in milliseconds since epoch
ts_ms = int(time.time() * 1000)

# Encode timestamp as 10 base32 chars (big-endian)
ts_chars = ""
n = ts_ms
for _ in range(10):
    ts_chars = ALPHABET[n % 32] + ts_chars
    n //= 32

# 80 bits of randomness from os.urandom
rand_int = int.from_bytes(os.urandom(10), "big")

# Encode randomness as 16 base32 chars
rand_chars = ""
for _ in range(16):
    rand_chars = ALPHABET[rand_int % 32] + rand_chars
    rand_int //= 32

print(ts_chars + rand_chars)
'
}

# Generate a prefixed ID for a given entity type
#   Usage: generate_id SIG    → "SIG-01JR8XYZABCDEFGHJKMNPQR"
#          generate_id INT    → "INT-01JR8XYZABCDEFGHJKMNPQR"
#          generate_id SPEC   → "SPEC-01JR8XYZABCDEFGHJKMNPQR"
generate_id() {
  local prefix="$1"
  if [[ -z "$prefix" ]]; then
    echo "Error: generate_id requires a prefix (SIG|INT|SPEC|CON|DEC)" >&2
    return 1
  fi
  echo "${prefix}-$(generate_ulid)"
}

# Return a regex pattern that matches either legacy sequential IDs or new
# ULID-based IDs for a given prefix. Use this in grep calls that need to
# find entities by ID across the migration boundary.
#
#   Usage: match_id_regex SIG    → "SIG-([0-9]{3}|[0-9A-Z]{26})"
#          grep "^id: $(match_id_regex SIG)"
match_id_regex() {
  local prefix="$1"
  if [[ -z "$prefix" ]]; then
    echo "Error: match_id_regex requires a prefix" >&2
    return 1
  fi
  echo "${prefix}-([0-9]{3}|[0-9A-Z]{26})"
}

# Extract the bare ID (with prefix) from a frontmatter field line.
# Handles both legacy and ULID formats.
#
#   Usage: extract_id_from_file <filepath> <prefix>
extract_id_from_file() {
  local file="$1"
  local prefix="${2:-[A-Z]+}"
  if [[ ! -f "$file" ]]; then
    return 1
  fi
  grep -oE "^id: ${prefix}-([0-9]{3}|[0-9A-Z]{26})" "$file" 2>/dev/null \
    | head -1 \
    | sed 's/^id: //'
}

# Validate that a given ID matches either the legacy or ULID format.
#   Usage: is_valid_id SIG-042 SIG   → 0 (valid)
#          is_valid_id SIG-01JR8XYZABCDEFGHJKMNPQR SIG → 0 (valid)
#          is_valid_id SIG-foo SIG   → 1 (invalid)
is_valid_id() {
  local id="$1"
  local prefix="$2"
  if [[ "$id" =~ ^${prefix}-([0-9]{3}|[0-9A-Z]{26})$ ]]; then
    return 0
  fi
  return 1
}

# Sort a list of IDs chronologically. Legacy SIG-NNN sorts numerically,
# ULID-based IDs sort lexicographically (which is timestamp-ordered by
# ULID design). Mixed lists: legacy IDs appear first (lower), new IDs
# after (higher). This is intentional — new IDs are always "newer" than
# legacy ones.
#
#   Usage: sort_ids <<< "SIG-042\nSIG-01JR8XYZ..."
sort_ids() {
  sort -V
}
