"""
id_gen.py — ULID generation for Intent Python servers and tools

Purpose: Replace sequential ID generators (SIG-001, INT-042, etc.) with
globally-unique, timestamp-ordered IDs that don't require coordination
between concurrent writers.

Addresses: SIG-022 (sequential signal IDs will collide in distributed
multi-agent environments), INT-009 P0 #1.

Format: {PREFIX}-{ULID} where ULID is 26 Crockford base32 chars
  10 chars: 48-bit timestamp (ms since epoch)
  16 chars: 80-bit randomness from os.urandom

Backward compatibility: legacy SIG-NNN / INT-NNN / SPEC-NNN IDs remain
valid and parseable via MATCH_ID_PATTERN.

Ship history:
  2026-04-09 — initial ship (SPEC-sig-022-ulid-migration)

No external dependencies — uses stdlib only (os.urandom, time, re).
"""

from __future__ import annotations

import os
import re
import time
from typing import Iterable

# Crockford base32 — excludes I, L, O, U to avoid visual ambiguity
ALPHABET = "0123456789ABCDEFGHJKMNPQRSTVWXYZ"

# Regex for matching both legacy sequential IDs and new ULID IDs.
# Use {prefix} named group match if you need to parse the prefix separately.
MATCH_ID_PATTERN = re.compile(
    r"^(?P<prefix>[A-Z]+)-(?P<id>[0-9]{3}|[0-9A-Z]{26})$"
)


def generate_ulid() -> str:
    """Generate a 26-character Crockford base32 ULID.

    10 chars of timestamp + 16 chars of randomness. Timestamp-sortable.
    Collision-free for all practical purposes (80 bits of entropy per ms).
    """
    ts_ms = int(time.time() * 1000)

    # Encode timestamp as 10 base32 chars (big-endian)
    ts_chars = ""
    n = ts_ms
    for _ in range(10):
        ts_chars = ALPHABET[n % 32] + ts_chars
        n //= 32

    # 80 bits of randomness
    rand_int = int.from_bytes(os.urandom(10), "big")
    rand_chars = ""
    for _ in range(16):
        rand_chars = ALPHABET[rand_int % 32] + rand_chars
        rand_int //= 32

    return ts_chars + rand_chars


def generate_id(prefix: str) -> str:
    """Generate a prefixed ULID.

    >>> generate_id("SIG")
    'SIG-01JR8XYZABCDEFGHJKMNPQR'
    """
    if not prefix or not prefix.isupper():
        raise ValueError(
            f"prefix must be an uppercase string (e.g., 'SIG', 'INT', 'SPEC'), got: {prefix!r}"
        )
    return f"{prefix}-{generate_ulid()}"


def is_valid_id(id_str: str, prefix: str | None = None) -> bool:
    """Check if a string matches the ID format (legacy or ULID).

    If prefix is provided, also validates that the ID has that prefix.
    """
    match = MATCH_ID_PATTERN.match(id_str)
    if not match:
        return False
    if prefix is not None and match.group("prefix") != prefix:
        return False
    return True


def parse_id(id_str: str) -> tuple[str, str] | None:
    """Parse an ID into (prefix, id_body). Returns None if invalid.

    >>> parse_id("SIG-042")
    ('SIG', '042')
    >>> parse_id("INT-01JR8XYZABCDEFGHJKMNPQR")
    ('INT', '01JR8XYZABCDEFGHJKMNPQR')
    >>> parse_id("not-an-id")
    None
    """
    match = MATCH_ID_PATTERN.match(id_str)
    if not match:
        return None
    return (match.group("prefix"), match.group("id"))


def is_legacy_id(id_str: str) -> bool:
    """Return True if the ID is in legacy sequential format (SIG-NNN)."""
    parsed = parse_id(id_str)
    if parsed is None:
        return False
    return len(parsed[1]) == 3 and parsed[1].isdigit()


def sort_ids(ids: Iterable[str]) -> list[str]:
    """Sort IDs chronologically.

    Legacy IDs sort before ULID IDs (legacy is always "older" by convention).
    Within each category, legacy IDs sort numerically and ULIDs sort
    lexicographically (which is timestamp-ordered by design).
    """
    legacy = []
    ulid = []
    for id_str in ids:
        if is_legacy_id(id_str):
            legacy.append(id_str)
        else:
            ulid.append(id_str)
    # Legacy: sort by numeric body
    legacy.sort(key=lambda x: int(parse_id(x)[1]) if parse_id(x) else 0)
    # ULID: lexicographic = timestamp-ordered
    ulid.sort()
    return legacy + ulid


# Module-level self-test
if __name__ == "__main__":
    # Smoke test — verify generation works and format is valid
    for prefix in ("SIG", "INT", "SPEC", "CON", "DEC"):
        new_id = generate_id(prefix)
        assert is_valid_id(new_id, prefix), f"Generated invalid ID: {new_id}"
        parsed = parse_id(new_id)
        assert parsed is not None
        assert parsed[0] == prefix
        assert len(parsed[1]) == 26
        print(f"✓ {new_id}")

    # Verify legacy IDs still parse
    for legacy in ("SIG-001", "INT-042", "SPEC-007"):
        assert is_valid_id(legacy), f"Legacy ID rejected: {legacy}"
        assert is_legacy_id(legacy), f"Legacy ID not flagged as legacy: {legacy}"
        print(f"✓ legacy: {legacy}")

    # Verify invalid IDs reject
    for bad in ("SIG-foo", "sig-042", "SIG-", "foo", ""):
        assert not is_valid_id(bad), f"Invalid ID accepted: {bad!r}"
        print(f"✓ rejected: {bad!r}")

    # Verify sort order
    mixed = [
        "SIG-042",
        "SIG-01JR8XYZABCDEFGHJKMNPQR",
        "SIG-001",
        "SIG-01JR9ZZZABCDEFGHJKMNPQR",
    ]
    sorted_mixed = sort_ids(mixed)
    assert sorted_mixed[0] == "SIG-001"
    assert sorted_mixed[1] == "SIG-042"
    assert sorted_mixed[2] == "SIG-01JR8XYZABCDEFGHJKMNPQR"
    assert sorted_mixed[3] == "SIG-01JR9ZZZABCDEFGHJKMNPQR"
    print("✓ sort order: legacy first, ULID second, chronological within each")

    print("\nAll self-tests passed.")
