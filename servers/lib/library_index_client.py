"""
library-index client — composition seam for substrate exposure
(per substrate-exposure-architecture.md §Q4).

Phase 2 (this module):
    Calls library-index-mcp's BM25 ranking surface directly via Python
    import (Option A — direct in-process import of the ranking functions
    from `Core/products/library-index-mcp/server.py`).

    Rationale for Option A over B/C:
      - Option B (in-process MCP stdio client) would require spawning a
        subprocess from inside an MCP server — a known pain point.
      - Option C (HTTP dial-in) requires library-index-mcp to expose an
        HTTP transport, which it only does on demand (--transport http).
      - Option A reuses the exact same BM25 logic (`_build_bm25_index` +
        inline BM25Okapi stdlib fallback) without a subprocess.  The
        architectural "MCP composition" commitment holds at the *user-side*
        — both servers run independently and any user-side client can call
        either; for intent-knowledge → library-index-mcp INTERNAL use, a
        Python import is the pragmatic and correct choice.

    Import path:
        `Core/products/library-index-mcp/server.py` — resolved relative to
        `LIBRARY_INDEX_MCP_ROOT` env var, else hardcoded Workspaces default.
        Import is deferred to query-time; failure falls back to Phase 1
        word-hit scorer so the server never goes dark.

Contract (unchanged):
    query(text, k) → list of {path, chunk, score, entity_id}

`path`       — absolute path (or catalog-relative) to the matched asset
`chunk`      — content_excerpt from sidecar, else topics string, else path
`score`      — BM25 score (Phase 2) or word_hits * 0.3 + depth_score * 0.7 (fallback)
`entity_id`  — first entity in the asset's entities list, if any

The MCP server applies classification enforcement AFTER library-index
returns results — this client does not filter by scope.
"""
from __future__ import annotations

import importlib.util
import json
import os
import re
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Optional


# ─── Resolved path to library-index-mcp server.py ─────────────────────────
# Override via LIBRARY_INDEX_MCP_ROOT env var (useful in tests).
_DEFAULT_LI_MCP_PATH = (
    Path.home() / "Workspaces" / "Core" / "products" / "library-index-mcp" / "server.py"
)
_LI_MCP_SERVER_PATH: Optional[Path] = None


def _resolve_li_mcp_path() -> Optional[Path]:
    """Resolve the library-index-mcp server.py path, honouring the env override."""
    global _LI_MCP_SERVER_PATH
    if _LI_MCP_SERVER_PATH is not None:
        return _LI_MCP_SERVER_PATH

    env_root = os.environ.get("LIBRARY_INDEX_MCP_ROOT")
    if env_root:
        p = Path(env_root) / "server.py"
    else:
        p = _DEFAULT_LI_MCP_PATH

    _LI_MCP_SERVER_PATH = p if p.is_file() else None
    return _LI_MCP_SERVER_PATH


# ─── Module-level import cache for library-index-mcp internals ─────────────
_li_mcp_module = None
_li_mcp_import_error: Optional[str] = None


def _get_li_mcp_module():
    """
    Import library-index-mcp server.py as a Python module (deferred, cached).

    Returns the module on success, None on any import failure.  The import
    failure message is stored in _li_mcp_import_error for status reporting.
    """
    global _li_mcp_module, _li_mcp_import_error
    if _li_mcp_module is not None:
        return _li_mcp_module
    if _li_mcp_import_error is not None:
        return None  # already tried and failed

    server_path = _resolve_li_mcp_path()
    if server_path is None:
        _li_mcp_import_error = (
            "library-index-mcp server.py not found at expected path; "
            "set LIBRARY_INDEX_MCP_ROOT to override"
        )
        return None

    try:
        spec = importlib.util.spec_from_file_location(
            "library_index_mcp_server", str(server_path)
        )
        if spec is None or spec.loader is None:
            _li_mcp_import_error = f"importlib could not build spec from {server_path}"
            return None
        module = importlib.util.module_from_spec(spec)
        # Prevent the module from registering MCP tools at import time by
        # inserting it into sys.modules BEFORE exec_module so that any
        # top-level import guards pass.
        sys.modules["library_index_mcp_server"] = module
        spec.loader.exec_module(module)  # type: ignore[attr-defined]
        _li_mcp_module = module
        return module
    except Exception as exc:
        _li_mcp_import_error = f"import failed: {exc}"
        return None


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
    Phase 2 client: BM25-ranked retrieval via direct Python import of
    library-index-mcp's `_build_bm25_index` ranking surface.

    Fallback chain (in order):
        1. BM25 via library-index-mcp import (Phase 2 — primary)
        2. Word-hit * 0.3 + depth_score * 0.7 over CATALOG.json (Phase 1 scorer)
        3. NotImplementedError raised → caller falls back to repo_keyword_fallback()

    Behavior modes:
        - library-index-mcp importable + catalog present → BM25 results
        - library-index-mcp not importable + catalog present → Phase 1 word-hit
        - catalog absent / unreadable → raise NotImplementedError

    `available` property: True if catalog_path file exists (either path works).
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

    # ─── Phase 2: BM25 via library-index-mcp ─────────────────────────

    def _search_via_bm25(self, text: str, k: int, catalog: dict) -> list[LibraryIndexHit]:
        """
        Use library-index-mcp's `_build_bm25_index` to score and rank assets.

        Raises ImportError (caught by caller) when the module is not importable.
        Raises ValueError when BM25 index build fails.
        """
        module = _get_li_mcp_module()
        if module is None:
            raise ImportError(
                _li_mcp_import_error or "library-index-mcp module unavailable"
            )

        build_fn = getattr(module, "_build_bm25_index", None)
        resolve_sidecar_fn = getattr(module, "_resolve_sidecar_path", None)
        if build_fn is None:
            raise ImportError("_build_bm25_index not found in library-index-mcp module")

        # Override the module's CATALOG_PATH so it reads the same file we loaded.
        # (The module-level _load_catalog is not called here — we pass our own
        # already-loaded catalog dict directly.)
        bm25, paths = build_fn(catalog)

        query_tokens = text.lower().split()
        scores = bm25.get_scores(query_tokens)

        assets_by_path = {a["path"]: a for a in catalog.get("assets", [])}

        scored = sorted(
            ((scores[i], paths[i]) for i in range(len(paths))),
            key=lambda x: x[0],
            reverse=True,
        )

        hits: list[LibraryIndexHit] = []
        for score, path in scored:
            if len(hits) >= k:
                break
            asset = assets_by_path.get(path, {})

            # Load excerpt from sidecar (mirrors library-index-mcp logic)
            excerpt = ""
            if resolve_sidecar_fn is not None:
                sidecar_path = resolve_sidecar_fn(path)
                if sidecar_path and sidecar_path.exists():
                    try:
                        import yaml as _yaml
                        with open(sidecar_path) as f:
                            sc = _yaml.safe_load(f) or {}
                        raw_excerpt = (
                            sc.get("content_excerpt") or sc.get("summary") or ""
                        )
                        excerpt = raw_excerpt[:500]
                    except Exception:
                        pass

            if not excerpt:
                # Fallback: topics list as excerpt (same as library-index-mcp)
                excerpt = "; ".join(asset.get("topics", []))[:500]
            if not excerpt:
                excerpt = path

            entities = asset.get("entities") or []
            entity_id = entities[0] if entities else None

            hits.append(LibraryIndexHit(
                path=path,
                chunk=excerpt,
                score=float(score),
                entity_id=str(entity_id) if entity_id else None,
            ))

        return hits

    # ─── Phase 1 fallback: word-hit scorer ───────────────────────────

    def _search_via_wordhit(self, text: str, k: int, catalog: dict) -> list[LibraryIndexHit]:
        """
        Phase 1 depth-sorted keyword scoring over CATALOG.json.
        Used when library-index-mcp is not importable.
        """
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

    # ─── Public interface ─────────────────────────────────────────────

    def query(self, text: str, k: int = 10) -> list[LibraryIndexHit]:
        """
        Return up to `k` ranked hits for `text`.

        Phase 2 primary path: BM25 scoring via library-index-mcp import.
        Phase 1 fallback: word-hit * 0.3 + depth_score * 0.7 (when import fails).
        Raises NotImplementedError when CATALOG.json is unavailable (caller
        falls back to repo_keyword_fallback()).
        """
        if not self.available:
            raise NotImplementedError(
                f"CATALOG.json not present at {self.catalog_path}; falling back. "
                f"See spec/library-index-composition-investigation-2026-05-26.md."
            )

        catalog = self._load_catalog()

        # Phase 2: BM25 via library-index-mcp
        try:
            return self._search_via_bm25(text, k, catalog)
        except Exception:
            pass

        # Phase 1 fallback: word-hit scorer (no library-index-mcp dependency)
        return self._search_via_wordhit(text, k, catalog)

    def status(self) -> str:
        """
        Report which path is active for diagnostics / library_index_status field.

        Returns a human-readable status string used by knowledge.py's query verb.
        """
        if not self.available:
            return "unavailable — CATALOG.json not found"

        module = _get_li_mcp_module()
        if module is not None:
            return (
                "bm25 — library-index-mcp import active; "
                "ranked by BM25Okapi (rank_bm25 or stdlib fallback)"
            )
        err = _li_mcp_import_error or "unknown import error"
        return (
            f"phase1-wordhit — library-index-mcp not importable ({err}); "
            f"using word_hits * 0.3 + depth_score * 0.7"
        )


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

    Intentionally coarse — the BM25 composition replaces this for
    CATALOG.json assets; this covers .intent/ substrate files that
    library-index-mcp doesn't index.
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
