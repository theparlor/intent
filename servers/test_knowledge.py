"""
Tests for the substrate-exposure verbs on the intent-knowledge MCP server.

Strategy:
  - Each test sets `knowledge.ROOT` to a fresh tmp_path containing a
    synthetic .intent/ tree with classification.yaml, signals, specs,
    decisions.
  - We exercise the underlying tool callables (each `@mcp.tool()` wraps
    the function; we call the unwrapped function via `.fn` attribute or
    by direct module access).
  - library-index is exercised by both stub-raise and fallback path.
"""
from __future__ import annotations

import json
import os
import sys
from pathlib import Path

import pytest


HERE = Path(__file__).resolve().parent
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))


# ─── Fixtures ───────────────────────────────────────────────────

@pytest.fixture
def synthetic_repo(tmp_path: Path) -> Path:
    """
    Build a small repo tree:

        tmp/
          .intent/
            classification.yaml        (tier: internal)
            signals/
              2026-05-26-internal-sig.md  (SIG-INTERNAL-001)
              2026-05-26-public-sig.md    (SIG-PUBLIC-001, tier=public)
            specs/
              SPEC-100.md
            decisions/
              DEC-200.md
            events/events.jsonl
          knowledge/
            decisions/
              DDR-300.md (declared confidential under sub-product)
          spec/
            decision-log.md (contains ### DEC-201:)
          Core/engagements/alpha/
            .intent/classification.yaml (tier: confidential:alpha)
            signals/
              2026-05-26-alpha-secret.md (SIG-ALPHA-001)
    """
    # Root classification
    intent_dir = tmp_path / ".intent"
    (intent_dir / "signals").mkdir(parents=True)
    (intent_dir / "specs").mkdir(parents=True)
    (intent_dir / "decisions").mkdir(parents=True)
    (intent_dir / "events").mkdir(parents=True)
    (intent_dir / "classification.yaml").write_text(
        "tier: internal\ndeclared_at: 2026-05-26\ndeclared_by: brien\nnotes: \"\"\n"
    )

    # Internal signal
    (intent_dir / "signals" / "2026-05-26-internal-sig.md").write_text(
        "---\n"
        "id: SIG-INTERNAL-001\n"
        "timestamp: 2026-05-26T10:00:00Z\n"
        "source: cli\n"
        "status: active\n"
        "related_intents:\n"
        "  - INT-100\n"
        "---\n"
        "# Internal signal about knowledge\n\n"
        "This is the internal substrate query test fixture.\n"
    )

    # Public signal — same root, but per-file tier set via sibling directory
    # For simplicity, public-tier files live under a sub-product that has its
    # own classification.yaml.
    public_dir = tmp_path / "public-product" / ".intent"
    (public_dir / "signals").mkdir(parents=True)
    (public_dir / "classification.yaml").write_text(
        "tier: public\ndeclared_at: 2026-05-26\ndeclared_by: brien\nnotes: \"\"\n"
    )
    (public_dir / "signals" / "2026-05-26-public-sig.md").write_text(
        "---\n"
        "id: SIG-PUBLIC-001\n"
        "timestamp: 2026-05-26T10:00:00Z\n"
        "source: cli\n"
        "status: active\n"
        "---\n"
        "# Public marketing-safe signal\n"
    )

    # Spec
    (intent_dir / "specs" / "SPEC-100.md").write_text(
        "---\n"
        "id: SPEC-100\n"
        "title: Test spec\n"
        "status: draft\n"
        "---\n"
        "# Test Spec\n\nBody.\n"
    )

    # Decision
    (intent_dir / "decisions" / "DEC-200.md").write_text(
        "---\n"
        "id: DEC-200\n"
        "title: Test decision\n"
        "status: filed\n"
        "supersedes:\n"
        "  - DEC-199\n"
        "---\n"
        "# Test Decision\n\nBody.\n"
    )

    # decision-log.md sentinel
    (tmp_path / "spec").mkdir(parents=True)
    (tmp_path / "spec" / "decision-log.md").write_text(
        "# Log\n\n### DEC-201: Sample decision\n\nBody.\n"
    )

    # Confidential engagement
    eng_dir = tmp_path / "Core" / "engagements" / "alpha" / ".intent"
    (eng_dir / "signals").mkdir(parents=True)
    (eng_dir / "classification.yaml").write_text(
        "tier: confidential:alpha\ndeclared_at: 2026-05-26\ndeclared_by: brien\nnotes: \"\"\n"
    )
    (eng_dir / "signals" / "2026-05-26-alpha-secret.md").write_text(
        "---\n"
        "id: SIG-ALPHA-001\n"
        "timestamp: 2026-05-26T10:00:00Z\n"
        "source: cli\n"
        "status: active\n"
        "caused_by:\n"
        "  - SIG-INTERNAL-001\n"
        "---\n"
        "# Alpha-confidential signal — should not leak to internal scope\n"
    )

    # Empty events.jsonl
    (intent_dir / "events" / "events.jsonl").write_text("")

    return tmp_path


@pytest.fixture
def knowledge_module(synthetic_repo: Path, monkeypatch):
    """Import the knowledge server module rebased on the synthetic repo."""
    monkeypatch.chdir(synthetic_repo)
    # Point catalog at a missing file so the library-index client falls
    # back to repo_keyword_fallback against the synthetic substrate.
    # Tests that want to exercise the catalog path (re-)set this explicitly.
    monkeypatch.setenv("INTENT_KNOWLEDGE_CATALOG", str(synthetic_repo / "no-catalog.json"))
    # Drop any cached module so module-level ROOT recomputes against tmp.
    for mod in ("knowledge", "lib.classification", "lib.lineage", "lib.library_index_client"):
        if mod in sys.modules:
            del sys.modules[mod]
    import knowledge  # noqa: F401
    # Re-point ROOT explicitly so child files use the fixture path.
    knowledge.ROOT = str(synthetic_repo)
    knowledge.KNOWLEDGE_DIR = str(synthetic_repo / "knowledge")
    knowledge.RAW_DIR = str(synthetic_repo / "raw")
    knowledge.INDEX_FILE = str(synthetic_repo / "knowledge" / "_index.md")
    knowledge.LOG_FILE = str(synthetic_repo / "knowledge" / "log.md")
    knowledge.EVENTS_FILE = str(synthetic_repo / ".intent" / "events" / "events.jsonl")
    (synthetic_repo / "knowledge").mkdir(exist_ok=True)
    (synthetic_repo / "knowledge" / "_index.md").write_text("# Index\n")
    (synthetic_repo / "knowledge" / "log.md").write_text("")
    return knowledge


def _call(tool_callable, **kwargs):
    """Call a FastMCP-wrapped tool — unwrap to .fn if present."""
    fn = getattr(tool_callable, "fn", tool_callable)
    return fn(**kwargs)


# ─── Classification module unit tests ───────────────────────────

def test_classification_default_when_missing(tmp_path):
    from lib.classification import ClassificationResolver
    resolver = ClassificationResolver(repo_root=tmp_path)
    cls = resolver.resolve(tmp_path / "foo.md")
    assert cls.tier == "internal"
    assert cls.source_path is None


def test_classification_walks_up_to_find_yaml(tmp_path):
    from lib.classification import ClassificationResolver
    (tmp_path / ".intent").mkdir()
    (tmp_path / ".intent" / "classification.yaml").write_text("tier: public\n")
    nested = tmp_path / "subdir" / "deeper" / "file.md"
    nested.parent.mkdir(parents=True)
    nested.write_text("hi")
    resolver = ClassificationResolver(repo_root=tmp_path)
    cls = resolver.resolve(nested)
    assert cls.tier == "public"


def test_in_scope_public(tmp_path):
    from lib.classification import Classification, in_scope
    pub = Classification(tier="public")
    internal = Classification(tier="internal")
    conf = Classification(tier="confidential:alpha")
    assert in_scope("public", pub) is True
    assert in_scope("public", internal) is False
    assert in_scope("public", conf) is False


def test_in_scope_internal(tmp_path):
    from lib.classification import Classification, in_scope
    assert in_scope("internal", Classification(tier="public")) is True
    assert in_scope("internal", Classification(tier="internal")) is True
    assert in_scope("internal", Classification(tier="confidential:alpha")) is False


def test_in_scope_engagement(tmp_path):
    from lib.classification import Classification, in_scope
    assert in_scope("engagement:alpha", Classification(tier="public")) is True
    assert in_scope("engagement:alpha", Classification(tier="internal")) is True
    assert in_scope("engagement:alpha", Classification(tier="confidential:alpha")) is True
    assert in_scope("engagement:alpha", Classification(tier="confidential:beta")) is False
    assert in_scope("engagement:beta", Classification(tier="confidential:alpha")) is False


def test_invalid_scope_token():
    from lib.classification import ScopeTokenError, validate_scope_token
    with pytest.raises(ScopeTokenError):
        validate_scope_token("")
    with pytest.raises(ScopeTokenError):
        validate_scope_token("garbage")
    with pytest.raises(ScopeTokenError):
        validate_scope_token("engagement:")


def test_malformed_classification_yaml(tmp_path):
    from lib.classification import ClassificationError, ClassificationResolver
    (tmp_path / ".intent").mkdir()
    (tmp_path / ".intent" / "classification.yaml").write_text("not_tier: oops\n")
    resolver = ClassificationResolver(repo_root=tmp_path)
    with pytest.raises(ClassificationError):
        resolver.resolve(tmp_path / "x.md")


# ─── query verb ─────────────────────────────────────────────────

def test_query_internal_scope_excludes_confidential(knowledge_module):
    result = json.loads(_call(knowledge_module.query,
                              text="signal", scope_token="internal", k=10))
    assert result["verb"] == "query"
    assert result["fallback_used"] is True  # library-index is stubbed
    hit_paths = {h["path"] for h in result["hits"]}
    assert not any("Core/engagements/alpha" in p for p in hit_paths)
    assert result["omitted_out_of_scope"] >= 1


def test_query_engagement_scope_returns_confidential(knowledge_module):
    result = json.loads(_call(knowledge_module.query,
                              text="alpha confidential signal",
                              scope_token="engagement:alpha", k=10))
    hit_paths = {h["path"] for h in result["hits"]}
    assert any("Core/engagements/alpha" in p for p in hit_paths)


def test_query_invalid_scope_token(knowledge_module):
    result = json.loads(_call(knowledge_module.query,
                              text="anything", scope_token="bogus"))
    assert "error" in result


def test_query_k_bound(knowledge_module):
    result = json.loads(_call(knowledge_module.query,
                              text="signal", scope_token="internal", k=999))
    assert result["k"] == 25  # capped at 25


# ─── get verb ───────────────────────────────────────────────────

def test_get_internal_entity(knowledge_module):
    result = json.loads(_call(knowledge_module.get,
                              entity_id="SIG-INTERNAL-001",
                              scope_token="internal"))
    assert result["verb"] == "get"
    assert result["entity"]["id"] == "SIG-INTERNAL-001"
    assert "Internal signal" in result["entity"]["title"]
    assert result["entity"]["tier"] == "internal"
    assert "Internal signal about knowledge" in result["entity"]["body"]


def test_get_out_of_scope_returns_error(knowledge_module):
    result = json.loads(_call(knowledge_module.get,
                              entity_id="SIG-ALPHA-001",
                              scope_token="internal"))
    assert result["error"] == "out_of_scope"


def test_get_engagement_scope_unlocks_confidential(knowledge_module):
    result = json.loads(_call(knowledge_module.get,
                              entity_id="SIG-ALPHA-001",
                              scope_token="engagement:alpha"))
    assert result["entity"]["id"] == "SIG-ALPHA-001"
    assert result["entity"]["tier"] == "confidential:alpha"


def test_get_invalid_id(knowledge_module):
    result = json.loads(_call(knowledge_module.get,
                              entity_id="not-a-valid-id",
                              scope_token="internal"))
    assert result["error"] == "invalid_id"


def test_get_not_found(knowledge_module):
    result = json.loads(_call(knowledge_module.get,
                              entity_id="SIG-MISSING-999",
                              scope_token="internal"))
    assert result["error"] == "not_found"


def test_get_decision_from_log(knowledge_module):
    # DEC-201 is declared inline in spec/decision-log.md (no individual file).
    result = json.loads(_call(knowledge_module.get,
                              entity_id="DEC-201",
                              scope_token="internal"))
    assert result["entity"]["id"] == "DEC-201"


# ─── list verb ──────────────────────────────────────────────────

def test_list_signals_internal(knowledge_module):
    result = json.loads(_call(knowledge_module.list_entities,
                              type="signal", scope_token="internal", limit=20))
    ids = {e["id"] for e in result["entities"]}
    assert "SIG-INTERNAL-001" in ids
    assert "SIG-PUBLIC-001" in ids
    assert "SIG-ALPHA-001" not in ids


def test_list_signals_public_only(knowledge_module):
    result = json.loads(_call(knowledge_module.list_entities,
                              type="signal", scope_token="public", limit=20))
    ids = {e["id"] for e in result["entities"]}
    assert "SIG-PUBLIC-001" in ids
    assert "SIG-INTERNAL-001" not in ids
    assert "SIG-ALPHA-001" not in ids


def test_list_invalid_type(knowledge_module):
    result = json.loads(_call(knowledge_module.list_entities,
                              type="goober", scope_token="internal"))
    assert result["error"] == "invalid_type"


def test_list_limit_capped(knowledge_module):
    result = json.loads(_call(knowledge_module.list_entities,
                              type="signal", scope_token="internal", limit=9999))
    assert result["limit"] == 50


def test_list_substring_filter(knowledge_module):
    result = json.loads(_call(knowledge_module.list_entities,
                              type="signal", scope_token="internal",
                              filter="public", limit=20))
    ids = {e["id"] for e in result["entities"]}
    assert "SIG-PUBLIC-001" in ids
    assert "SIG-INTERNAL-001" not in ids


# ─── lineage verb ───────────────────────────────────────────────

def test_lineage_traverses_caused_by(knowledge_module):
    # Walking SIG-ALPHA-001 backward with engagement scope → reaches SIG-INTERNAL-001
    result = json.loads(_call(knowledge_module.lineage,
                              signal_id="SIG-ALPHA-001",
                              scope_token="engagement:alpha",
                              depth=3))
    back_ids = {n["id"] for n in result["backward"]}
    assert "SIG-INTERNAL-001" in back_ids


def test_lineage_truncates_at_scope_boundary(knowledge_module):
    # An internal-scope caller asking lineage on SIG-INTERNAL-001 should not
    # see the confidential SIG-ALPHA-001 as a forward step.
    result = json.loads(_call(knowledge_module.lineage,
                              signal_id="SIG-INTERNAL-001",
                              scope_token="internal",
                              depth=3))
    # Confidential entities never appear in chain
    fwd_ids = {n["id"] for n in result["forward"]}
    assert "SIG-ALPHA-001" not in fwd_ids


def test_lineage_root_out_of_scope(knowledge_module):
    result = json.loads(_call(knowledge_module.lineage,
                              signal_id="SIG-ALPHA-001",
                              scope_token="internal"))
    assert result["error"] == "out_of_scope"


def test_lineage_depth_bounded(knowledge_module):
    result = json.loads(_call(knowledge_module.lineage,
                              signal_id="SIG-INTERNAL-001",
                              scope_token="internal", depth=99))
    assert result["max_depth"] == 5


# ─── freshness verb ─────────────────────────────────────────────

def test_freshness_returns_mtime(knowledge_module, synthetic_repo):
    rel = ".intent/signals/2026-05-26-internal-sig.md"
    result = json.loads(_call(knowledge_module.freshness,
                              path=rel, scope_token="internal"))
    assert result["verb"] == "freshness"
    assert result["path"] == rel
    assert result["size_bytes"] > 0
    assert "T" in result["mtime"]
    assert result["tier"] == "internal"


def test_freshness_out_of_scope(knowledge_module):
    rel = "Core/engagements/alpha/.intent/signals/2026-05-26-alpha-secret.md"
    result = json.loads(_call(knowledge_module.freshness,
                              path=rel, scope_token="internal"))
    assert result["error"] == "out_of_scope"


def test_freshness_path_traversal_blocked(knowledge_module):
    result = json.loads(_call(knowledge_module.freshness,
                              path="../../../etc/passwd",
                              scope_token="internal"))
    assert result["error"] in ("outside_repo", "not_found")


def test_freshness_missing_path(knowledge_module):
    result = json.loads(_call(knowledge_module.freshness,
                              path=".intent/signals/does-not-exist.md",
                              scope_token="internal"))
    assert result["error"] == "not_found"


# ─── library-index client behavior ──────────────────────────────

def test_library_index_client_absent_catalog_raises(tmp_path):
    """When CATALOG.json is missing, the client raises NotImplementedError
    so the MCP server falls back to repo_keyword_fallback."""
    from lib.library_index_client import LibraryIndexClient
    missing = tmp_path / "no-such-catalog.json"
    client = LibraryIndexClient(catalog_path=missing)
    assert client.available is False
    with pytest.raises(NotImplementedError):
        client.query("anything")


def test_library_index_client_with_synthetic_catalog(tmp_path):
    """When CATALOG.json is present, the client returns ranked hits."""
    from lib.library_index_client import LibraryIndexClient
    cat = tmp_path / "CATALOG.json"
    cat.write_text(json.dumps({
        "assets": [
            {
                "path": "/x/a.md",
                "topics": ["substrate", "exposure"],
                "entities": ["SIG-001"],
                "depth_score": 0.8,
                "summary": "Substrate exposure design notes",
            },
            {
                "path": "/x/b.md",
                "topics": ["unrelated"],
                "entities": [],
                "depth_score": 0.1,
                "summary": "About other things",
            },
        ],
    }))
    client = LibraryIndexClient(catalog_path=cat)
    assert client.available is True
    hits = client.query("substrate exposure design", k=5)
    assert len(hits) >= 1
    assert hits[0].path == "/x/a.md"
    assert hits[0].score > 0
    assert hits[0].entity_id == "SIG-001"


def test_repo_keyword_fallback(synthetic_repo):
    from lib.library_index_client import repo_keyword_fallback
    hits = repo_keyword_fallback(synthetic_repo, "internal signal", k=5)
    # Should find at least the internal signal
    assert len(hits) >= 1
    paths = {os.path.basename(h.path) for h in hits}
    assert "2026-05-26-internal-sig.md" in paths


# ─── Server import smoke test ───────────────────────────────────

def test_server_imports_clean():
    """The MCP server module must be importable without side-effects.

    This is the Definition-of-Done's pipeline-survival check —
    `python servers/knowledge.py` must at least import cleanly.
    """
    for mod in ("knowledge", "lib.classification", "lib.lineage", "lib.library_index_client"):
        if mod in sys.modules:
            del sys.modules[mod]
    import knowledge  # noqa: F401
    for name in ("query", "get", "list_entities", "lineage", "freshness",
                 "knowledge_status", "knowledge_ingest", "knowledge_query",
                 "knowledge_lint", "knowledge_dossier"):
        assert hasattr(knowledge, name), f"missing tool: {name}"
