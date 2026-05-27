"""
library-index client — composition seam for substrate exposure
(per substrate-exposure-architecture.md §Q4).

Per `spec/library-index-composition-investigation-2026-05-26.md` (Agent 3):
    library-index has no BM25+vector retrieval surface today. The
    investigation recommends Port A extension (`library_search_ranked`
    in library-index-mcp, half-day) as the future state.

This module implements the **Phase 1 client** documented in the
investigation: a depth-sorted keyword match over
`~/Workspaces/CATALOG.json` (faceted asset metadata + topics +
entities + depth scores). It produces ranked results without needing
library-index-mcp to be running.

Contract (unchanged):
    query(text, k) → list of {path, chunk, score, entity_id}

`path`       — absolute path to the file the asset entry references
`chunk`      — `summary` field if present, else the path (CATALOG.json
                does not carry full content)
`score`      — `word_hits * 0.3 + depth_score * 0.7` (per investigation)
`entity_id`  — first entity in the asset's entities list, if any

The MCP server is responsible for applying classification enforcement
AFTER library-index returns results — the client itself does not filter
by scope. (Phase 2 will add classification metadata to library-index
entries so filtering can happen at retrieval.)

Phase 2 path (when Port A is extended):
    Replace `_search_via_catalog()` with a call to
    `library_search_ranked(query, k)` — same return shape.
"""
from __future__ import annotations

import json
import os
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Optional


@dataclass
class LibraryIndexHit:
    """One result from a library-index query."""
    path: str
    chunk: str
    score: float
    entity_id: Optional[str] = None

    def to_dict(self) -> dict:
        return {
            "path": self.path,
            "chunk": self.chunk,
            "score": self.score,
            "entity_id": self.entity_id,
        }


class LibraryIndexClient:
    """
    Phase 1 client per Agent 3's investigation report.

    Reads ~/Workspaces/CATALOG.json directly (no MCP hop) and ranks
    assets by `word_hits * 0.3 + depth_score * 0.7`. Returns up to `k`
    hits in the agreed contract shape.

    Behavior modes:
        - CATALOG.json present + readable → ranked results
        - CATALOG.json absent / unreadable → raise NotImplementedError so
          the caller falls back to repo_keyword_fallback()

    Phase 2 (Port A extension):
        Replace `_search_via_catalog()` with the `library_search_ranked`
        MCP call documented in the investigation report.
    """

    DEFAULT_CATALOG_PATH = Path.home() / "Workspaces" / "CATALOG.json"

    def __init__(self, repo_root: Optional[Path] = None,
                 catalog_path: Optional[Path] = None):
        self.repo_root = Path(repo_root).resolve() if repo_root else None
        self.catalog_path = Path(catalog_path) if catalog_path else self.DEFAULT_CATALOG_PATH
        self._catalog_cache: Optional[dict] = None
        self.available = self.catalog_path.is_file()

    def _load_catalog(self) -> dict:
        if self._catalog_cache is None:
            try:
                with open(self.catalog_path) as f:
                    self._catalog_cache = json.load(f)
            except (OSError, json.JSONDecodeError) as exc:
                raise NotImplementedError(
                    f"CATALOG.json unavailable at {self.catalog_path}: {exc}. "
                    f"See spec/library-index-composition-investigation-2026-05-26.md."
                ) from exc
        return self._catalog_cache

    def query(self, text: str, k: int = 10) -> list[LibraryIndexHit]:
        """
        Return up to `k` ranked hits for `text`.

        Phase 1: depth-sorted keyword scoring over CATALOG.json
        (per Agent 3 investigation §"The client interface intent-knowledge
        should implement").

        Phase 2: real BM25+vector via library_search_ranked.
        """
        if not self.available:
            raise NotImplementedError(
                f"CATALOG.json not present at {self.catalog_path}; falling back. "
                f"See spec/library-index-composition-investigation-2026-05-26.md."
            )

        catalog = self._load_catalog()
        keywords = [w.lower() for w in re.findall(r"\w{4,}", text)]
        if not keywords:
            return []

        hits: list[LibraryIndexHit] = []
        for asset in catalog.get("assets", []):
            searchable = " ".join([
                asset.get("path", "") or "",
                " ".join(asset.get("topics", []) or []),
                " ".join(str(e) for e in (asset.get("entities", []) or [])),
            ]).lower()
            word_hits = sum(1 for kw in keywords if kw in searchable)
            if word_hits == 0:
                continue
            depth_score = float(asset.get("depth_score", 0) or 0)
            score = word_hits * 0.3 + depth_score * 0.7
            path = asset.get("path", "") or ""
            chunk = asset.get("summary") or path
            entities = asset.get("entities") or []
            entity_id = entities[0] if entities else None
            hits.append(LibraryIndexHit(
                path=path,
                chunk=str(chunk),
                score=score,
                entity_id=str(entity_id) if entity_id else None,
            ))

        hits.sort(key=lambda h: h.score, reverse=True)
        return hits[:k]


# ─── Fallback repo-walker (used when library-index is unavailable) ─────

ENTITY_ID_PATTERN = re.compile(
    r"^id:\s*(SIG|INT|SPEC|CON|DEC|WS-DDR)-[A-Z0-9-]+",
    re.IGNORECASE | re.MULTILINE,
)


def repo_keyword_fallback(
    repo_root: Path,
    text: str,
    k: int = 10,
) -> list[LibraryIndexHit]:
    """
    Fallback query implementation when library-index is unavailable.

    Walks every `.intent/{signals,intents,specs,decisions,contracts}/`
    tree under `repo_root` (multi-product substrate), plus the top-level
    `spec/` and `knowledge/decisions/`. Scores files by keyword frequency
    and returns top-`k` hits with the first ~500 chars of the matched
    file as the chunk.

    Intentionally coarse — the BM25+vector composition replaces this
    once Agent 3's wire-up lands.
    """
    repo_root = Path(repo_root).resolve()
    keywords = [w.lower() for w in re.findall(r"\w{4,}", text)]
    if not keywords:
        return []

    candidate_paths: list[Path] = []
    seen: set[str] = set()

    entity_subdirs = ("signals", "intents", "specs", "decisions", "contracts")
    for intent_dir in repo_root.rglob(".intent"):
        if not intent_dir.is_dir():
            continue
        for sub in entity_subdirs:
            base = intent_dir / sub
            if not base.is_dir():
                continue
            for path in base.rglob("*.md"):
                key = str(path)
                if key in seen:
                    continue
                seen.add(key)
                candidate_paths.append(path)

    # Extra roots: top-level spec/ and knowledge/
    for sub in ("spec", "knowledge"):
        base = repo_root / sub
        if not base.is_dir():
            continue
        for path in base.rglob("*.md"):
            key = str(path)
            if key in seen:
                continue
            seen.add(key)
            candidate_paths.append(path)

    hits: list[tuple[float, LibraryIndexHit]] = []
    for path in candidate_paths:
        try:
            with open(path) as f:
                content = f.read()
        except OSError:
            continue
        lower = content.lower()
        score = sum(lower.count(kw) for kw in keywords)
        if score == 0:
            continue
        eid_match = ENTITY_ID_PATTERN.search(content)
        eid = eid_match.group(0).split(":", 1)[1].strip().upper() if eid_match else None
        chunk = content[:500]
        hits.append((float(score), LibraryIndexHit(
            path=str(path),
            chunk=chunk,
            score=float(score),
            entity_id=eid,
        )))

    hits.sort(key=lambda x: -x[0])
    return [h for _, h in hits[:k]]
