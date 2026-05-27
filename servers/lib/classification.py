"""
Classification enforcement — the load-bearing policy point for substrate
exposure (DEC-010, DEC-011, substrate-exposure-architecture.md §Phase 1).

Every entity in the substrate carries a tier — declared in
`.intent/classification.yaml` at the product root. The MCP server reads
the file on every request, compares against the caller's `scope_token`,
and decides whether to expose, omit, or 404 the entity.

Day 1 enforcement is binary (per Brien's D5-refined close):
  - scope_token matches → expose
  - scope_token does not match → absent (verb-specific)

Phase 2 (deferred) adds shaped-view substitution via per-engagement
`redaction-map.yaml`. This module stays the policy point either way —
shaped-view code reads from the same classification.yaml.

Schema (`<product>/.intent/classification.yaml`):
    tier: public | internal | confidential:<engagement-slug>
    declared_at: YYYY-MM-DD
    declared_by: brien
    notes: ""

Default tier when classification.yaml is absent: `internal`
(per DEC-011 — products without explicit declaration default to internal).

Scope-token semantics:
  - "public"               → matches tier=public only
  - "internal"             → matches tier in {public, internal}
  - "engagement:<slug>"    → matches tier=public, tier=internal,
                              or tier=confidential:<slug> (exact slug)
"""
from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path
from typing import Optional

import yaml


# Default classification when no .intent/classification.yaml is found.
# Per DEC-011: products default to `internal`; engagement-shaped paths
# require explicit declaration (the CLI errors at scaffold time, not here).
DEFAULT_TIER = "internal"

VALID_SCOPE_PREFIXES = ("public", "internal", "engagement:")


@dataclass(frozen=True)
class Classification:
    """Resolved classification for a single substrate path."""
    tier: str                  # "public" | "internal" | "confidential:<slug>"
    declared_at: Optional[str] = None
    declared_by: Optional[str] = None
    notes: str = ""
    source_path: Optional[str] = None  # path to classification.yaml (None = default)

    @property
    def is_confidential(self) -> bool:
        return self.tier.startswith("confidential:")

    @property
    def engagement_slug(self) -> Optional[str]:
        if self.is_confidential:
            return self.tier.split(":", 1)[1]
        return None


class ClassificationError(ValueError):
    """Raised when classification.yaml is malformed."""


class ScopeTokenError(ValueError):
    """Raised when scope_token is malformed."""


def _parse_classification_file(path: Path) -> Classification:
    """Read and validate `<path>/.intent/classification.yaml`."""
    try:
        with open(path) as f:
            data = yaml.safe_load(f) or {}
    except (OSError, yaml.YAMLError) as exc:
        raise ClassificationError(
            f"Failed to read classification.yaml at {path}: {exc}"
        ) from exc

    tier = data.get("tier")
    if not tier or not isinstance(tier, str):
        raise ClassificationError(
            f"classification.yaml at {path} missing or invalid `tier:` field"
        )

    # Validate tier shape
    valid_simple = ("public", "internal")
    if tier not in valid_simple and not tier.startswith("confidential:"):
        raise ClassificationError(
            f"classification.yaml at {path} has invalid tier: {tier!r}. "
            f"Must be one of: public, internal, confidential:<slug>"
        )
    if tier.startswith("confidential:") and len(tier.split(":", 1)[1]) == 0:
        raise ClassificationError(
            f"classification.yaml at {path} has empty engagement slug "
            f"after 'confidential:'"
        )

    return Classification(
        tier=tier,
        declared_at=data.get("declared_at"),
        declared_by=data.get("declared_by"),
        notes=data.get("notes", "") or "",
        source_path=str(path),
    )


class ClassificationResolver:
    """
    Per-request cache for classification.yaml lookups.

    Walks up from a given file path until it finds a `.intent/classification.yaml`,
    caches the result keyed by the *product root* (the dir containing `.intent/`),
    and returns the resolved Classification.

    Cache is request-scoped — instantiate a new resolver per MCP request to avoid
    serving stale data across writes.
    """

    def __init__(self, repo_root: Optional[Path] = None):
        # repo_root caps the upward walk so we don't escape the project.
        # If None, walk until filesystem root.
        self.repo_root = Path(repo_root).resolve() if repo_root else None
        self._cache: dict[str, Classification] = {}

    def resolve(self, entity_path: str | Path) -> Classification:
        """
        Resolve the classification for an entity at `entity_path`.

        Walks upward from `entity_path` until a `.intent/classification.yaml`
        is found, capped by `repo_root` if set. If none found, returns the
        default classification (tier=internal, source_path=None).
        """
        path = Path(entity_path).resolve()
        if path.is_file():
            path = path.parent

        # Walk up looking for .intent/classification.yaml
        for ancestor in [path] + list(path.parents):
            cls_path = ancestor / ".intent" / "classification.yaml"
            cache_key = str(ancestor)
            if cache_key in self._cache:
                return self._cache[cache_key]
            if cls_path.is_file():
                resolved = _parse_classification_file(cls_path)
                self._cache[cache_key] = resolved
                return resolved
            if self.repo_root is not None and ancestor == self.repo_root:
                break

        # No classification.yaml found — return default (internal)
        default = Classification(tier=DEFAULT_TIER, source_path=None)
        return default


def validate_scope_token(scope_token: str) -> str:
    """Validate scope_token shape. Returns normalized token. Raises ScopeTokenError on bad input."""
    if not scope_token or not isinstance(scope_token, str):
        raise ScopeTokenError("scope_token must be a non-empty string")
    if scope_token in ("public", "internal"):
        return scope_token
    if scope_token.startswith("engagement:"):
        slug = scope_token.split(":", 1)[1]
        if not slug:
            raise ScopeTokenError("engagement: scope_token missing engagement slug")
        return scope_token
    raise ScopeTokenError(
        f"Invalid scope_token: {scope_token!r}. "
        f"Must be 'public', 'internal', or 'engagement:<slug>'"
    )


def in_scope(scope_token: str, classification: Classification) -> bool:
    """
    Binary scope check (Day 1 enforcement per substrate-exposure-architecture.md §Phase 1).

    Match rules:
        scope_token="public"            → matches tier=public ONLY
        scope_token="internal"          → matches tier in {public, internal}
        scope_token="engagement:<slug>" → matches tier in {public, internal,
                                            confidential:<slug-exact>}
    """
    scope_token = validate_scope_token(scope_token)
    tier = classification.tier

    if scope_token == "public":
        return tier == "public"

    if scope_token == "internal":
        return tier in ("public", "internal")

    # engagement:<slug>
    requested_slug = scope_token.split(":", 1)[1]
    if tier in ("public", "internal"):
        return True
    if tier.startswith("confidential:"):
        entity_slug = tier.split(":", 1)[1]
        return entity_slug == requested_slug
    return False
