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


# ─── DEC-012: envelope extensions (D1 sightline · D2 supply_policy ·
#              D3 get_core · D4 audit_chain · preservation_invariant) ───

def test_supply_policy_derives_from_entity_type(knowledge_module):
    k = knowledge_module
    # normative — binding decisions / contracts (always supply)
    assert k._supply_policy({}, entity_id="DEC-200") == "normative"
    assert k._supply_policy({}, entity_id="WS-DDR-099") == "normative"
    assert k._supply_policy({}, entity_id="CON-001") == "normative"
    # provisional — revisable signals / intents / specs
    assert k._supply_policy({}, entity_id="SIG-INTERNAL-001") == "provisional"
    assert k._supply_policy({}, entity_id="INT-100") == "provisional"
    assert k._supply_policy({}, entity_id="SPEC-100") == "provisional"
    # grounded — sourced observation/event (via frontmatter type)
    assert k._supply_policy({"type": "observation"}, entity_id="") == "grounded"
    assert k._supply_policy({"type": "event"}, entity_id="") == "grounded"


def test_supply_policy_frontmatter_override_wins(knowledge_module):
    k = knowledge_module
    # explicit, valid override beats type derivation
    assert k._supply_policy({"supply_policy": "normative"}, entity_id="SIG-1") == "normative"
    assert k._supply_policy({"supply_policy": "grounded"}, entity_id="SIG-1") == "grounded"
    # invalid override is ignored → falls back to type derivation
    assert k._supply_policy({"supply_policy": "bogus"}, entity_id="SIG-1") == "provisional"


def test_supply_policy_unknown_defaults_provisional_never_normative(knowledge_module):
    k = knowledge_module
    assert k._supply_policy({}, entity_id="") == "provisional"
    assert k._supply_policy({}, entity_id="XYZ-9") == "provisional"


def test_sightline_frontmatter_override_wins(knowledge_module):
    k = knowledge_module
    content = "---\nsightline: My one-liner\n---\n# Title\n\nBody text."
    assert k._sightline(content, {"sightline": "My one-liner"}) == "My one-liner"


def test_sightline_falls_back_to_first_prose_line(knowledge_module):
    k = knowledge_module
    content = "---\nid: SIG-1\n---\n# Heading\n\n> a framing blockquote\n\nThe first real prose sentence here."
    sl = k._sightline(content, {"id": "SIG-1"})
    assert "first real prose sentence" in sl
    assert not sl.startswith("#")
    assert not sl.startswith(">")


def test_sightline_falls_back_to_title_when_no_body(knowledge_module):
    k = knowledge_module
    content = "---\nid: SIG-1\n---\n# Just A Title\n"
    assert k._sightline(content, {"id": "SIG-1"}) == "Just A Title"


def test_sightline_is_single_line_and_bounded(knowledge_module):
    k = knowledge_module
    sl = k._sightline("---\n---\n" + ("x" * 300), {})
    assert "\n" not in sl
    assert len(sl) <= 160


def test_get_envelope_carries_sightline_and_supply_policy(knowledge_module):
    r = json.loads(_call(knowledge_module.get,
                         entity_id="SIG-INTERNAL-001", scope_token="internal"))
    e = r["entity"]
    assert e["supply_policy"] == "provisional"   # a signal is revisable
    assert e["sightline"]                        # non-empty one-liner
    assert "\n" not in e["sightline"]


def test_get_decision_supply_policy_is_normative(knowledge_module):
    r = json.loads(_call(knowledge_module.get,
                         entity_id="DEC-200", scope_token="internal"))
    assert r["entity"]["supply_policy"] == "normative"


def test_list_entities_carry_sightline_and_supply_policy(knowledge_module):
    r = json.loads(_call(knowledge_module.list_entities,
                         type="signal", scope_token="internal", limit=20))
    assert r["entities"]
    for e in r["entities"]:
        assert "sightline" in e
        assert e["supply_policy"] == "provisional"   # all fixtures are signals


def test_query_hits_carry_sightline_and_supply_policy(knowledge_module):
    r = json.loads(_call(knowledge_module.query,
                         text="signal", scope_token="internal", k=10))
    assert r["hits"]
    for h in r["hits"]:
        assert "sightline" in h
        assert h["supply_policy"] in ("normative", "grounded", "provisional")


def test_preservation_invariant_get_returns_body_verbatim(knowledge_module, synthetic_repo):
    # A sourced provisional/grounded item MUST round-trip byte-identical — no
    # synthesis-rewrite at the exposure boundary (DEC-012 preservation_invariant).
    path = synthetic_repo / ".intent" / "signals" / "2026-05-26-internal-sig.md"
    raw = path.read_text()
    body_on_disk = raw.split("\n---\n", 1)[1]   # body after closing delimiter
    r = json.loads(_call(knowledge_module.get,
                         entity_id="SIG-INTERNAL-001", scope_token="internal"))
    e = r["entity"]
    assert e["body"].strip() == body_on_disk.strip()       # verbatim round-trip
    assert e["preservation"]["verbatim"] is True
    assert e["preservation"]["applies"] is True            # provisional + sourced (source: cli)


def test_preservation_invariant_marker_on_every_get(knowledge_module):
    # A normative decision: body still never paraphrased; 'applies' is False
    # (not a sourced grounded/provisional item) but verbatim holds.
    r = json.loads(_call(knowledge_module.get,
                         entity_id="DEC-200", scope_token="internal"))
    e = r["entity"]
    assert e["preservation"]["verbatim"] is True
    assert e["preservation"]["applies"] is False


def test_get_core_returns_bounded_shaped_items(knowledge_module):
    r = json.loads(_call(knowledge_module.get_core, scope_token="internal"))
    assert r["verb"] == "get_core"
    assert r["items"]
    for it in r["items"]:
        assert {"id", "sightline", "supply_policy"} <= set(it)
        assert "body" not in it              # standing core never dumps full bodies
        assert it["id"]                       # canonical entities only
    assert r["token_estimate"] <= 1000        # bounded (default budget)
    assert r["bounded"] is True


def test_get_core_excludes_out_of_scope(knowledge_module):
    r = json.loads(_call(knowledge_module.get_core, scope_token="internal"))
    ids = {it["id"] for it in r["items"]}
    assert "SIG-ALPHA-001" not in ids         # confidential never in internal core


def test_get_core_normative_before_provisional(knowledge_module):
    r = json.loads(_call(knowledge_module.get_core, scope_token="internal"))
    policies = [it["supply_policy"] for it in r["items"]]
    if "normative" in policies and "provisional" in policies:
        assert policies.index("normative") < policies.index("provisional")


def test_audit_chain_returns_color_and_counts(knowledge_module):
    r = json.loads(_call(knowledge_module.audit_chain, scope_token="internal"))
    assert r["verb"] == "audit_chain"
    assert r["color"] in ("green", "amber", "red")
    for key in ("unspecced_signals", "uncontracted_specs",
                "unverified_contracts", "orphans"):
        assert key in r["counts"] and isinstance(r["counts"][key], int)
    assert isinstance(r["findings"], list)


def test_audit_chain_color_reflects_findings(knowledge_module):
    r = json.loads(_call(knowledge_module.audit_chain, scope_token="internal"))
    total = sum(r["counts"].values())
    if total == 0:
        assert r["color"] == "green"
    else:
        assert r["color"] in ("amber", "red")


def test_audit_chain_excludes_out_of_scope(knowledge_module):
    r = json.loads(_call(knowledge_module.audit_chain, scope_token="internal"))
    ids = {f.get("id") for f in r["findings"]}
    assert "SIG-ALPHA-001" not in ids        # confidential never audited in internal scope


def test_audit_chain_intentional_orphan_opt_out(knowledge_module, synthetic_repo):
    # Mark the lone public signal intentional → it must not be an orphan finding.
    p = (synthetic_repo / "public-product" / ".intent" / "signals"
         / "2026-05-26-public-sig.md")
    p.write_text(p.read_text().replace(
        "status: active\n", "status: active\nintentional: true\n"))
    r = json.loads(_call(knowledge_module.audit_chain, scope_token="public"))
    orphan_ids = {f["id"] for f in r["findings"] if f["kind"] == "orphan"}
    assert "SIG-PUBLIC-001" not in orphan_ids


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


# ─── Phase 2: BM25 via library-index-mcp import ─────────────────

def test_library_index_client_bm25_returns_hits(tmp_path, monkeypatch):
    """
    Phase 2 primary path: when library-index-mcp is importable, query()
    returns BM25-ranked results (score is float from BM25Okapi.get_scores).

    Strategy: point LIBRARY_INDEX_MCP_ROOT at a minimal synthetic server.py
    that exposes `_build_bm25_index` with the same inline BM25Okapi stdlib
    implementation as the real server (no rank_bm25 package required).
    """
    import lib.library_index_client as lic_mod

    # Reset module-level import cache so each test is isolated
    lic_mod._li_mcp_module = None
    lic_mod._li_mcp_import_error = None
    lic_mod._LI_MCP_SERVER_PATH = None

    # Write a minimal server.py that only exposes _build_bm25_index
    fake_server = tmp_path / "server.py"
    fake_server.write_text(
        """
import math
from collections import Counter

_bm25_index_cache = {}

class BM25Okapi:
    def __init__(self, corpus, k1=1.5, b=0.75):
        self.k1 = k1
        self.b = b
        self.corpus = corpus
        self.N = len(corpus)
        self.avgdl = sum(len(d) for d in corpus) / max(self.N, 1)
        self.df = Counter()
        self.tf = []
        for doc in corpus:
            freq = Counter(doc)
            self.tf.append(freq)
            for term in set(doc):
                self.df[term] += 1
        self.idf = {}
        for term, freq in self.df.items():
            self.idf[term] = math.log((self.N - freq + 0.5) / (freq + 0.5) + 1)

    def get_scores(self, query_tokens):
        scores = [0.0] * self.N
        for token in query_tokens:
            idf = self.idf.get(token, 0.0)
            for i, freq in enumerate(self.tf):
                tf = freq.get(token, 0)
                dl = len(self.corpus[i])
                denom = tf + self.k1 * (1 - self.b + self.b * dl / max(self.avgdl, 1))
                scores[i] += idf * (tf * (self.k1 + 1)) / max(denom, 1e-10)
        return scores


def _resolve_sidecar_path(asset_path):
    return None  # no sidecars in test


def _build_bm25_index(catalog):
    key = id(catalog)
    if key in _bm25_index_cache:
        return _bm25_index_cache[key]
    assets = catalog.get("assets", [])
    corpus_tokens = []
    paths = []
    for asset in assets:
        path = asset.get("path", "")
        paths.append(path)
        topics_text = " ".join(asset.get("topics", []))
        entities_text = " ".join(str(e) for e in asset.get("entities", []))
        full_text = f"{topics_text} {entities_text} {path}"
        corpus_tokens.append(full_text.lower().split())
    index = BM25Okapi(corpus_tokens)
    _bm25_index_cache[key] = (index, paths)
    return _bm25_index_cache[key]
"""
    )

    monkeypatch.setenv("LIBRARY_INDEX_MCP_ROOT", str(tmp_path))

    # Build a catalog with two assets; relevance should rank a.md higher
    cat = tmp_path / "CATALOG.json"
    cat.write_text(json.dumps({
        "assets": [
            {
                "path": "/ws/a.md",
                "topics": ["substrate", "exposure", "bm25"],
                "entities": ["SIG-BM25-001"],
                "depth_score": 0.9,
            },
            {
                "path": "/ws/b.md",
                "topics": ["unrelated", "noise"],
                "entities": [],
                "depth_score": 0.1,
            },
        ],
    }))

    from lib.library_index_client import LibraryIndexClient

    client = LibraryIndexClient(catalog_path=cat)
    hits = client.query("substrate exposure bm25", k=5)

    assert len(hits) >= 1, "BM25 path should return at least one hit"
    assert hits[0].path == "/ws/a.md", (
        f"BM25 should rank the relevant doc first, got {hits[0].path}"
    )
    # Score must be a BM25 float > 0, NOT a word_hits * 0.3 + depth * 0.7 composite
    assert hits[0].score > 0.0, "BM25 score must be positive"
    assert hits[0].entity_id == "SIG-BM25-001"

    # Cleanup cached module so other tests are not affected
    lic_mod._li_mcp_module = None
    lic_mod._li_mcp_import_error = None
    lic_mod._LI_MCP_SERVER_PATH = None
    if "library_index_mcp_server" in sys.modules:
        del sys.modules["library_index_mcp_server"]


def test_library_index_client_bm25_fallback_when_import_fails(tmp_path, monkeypatch):
    """
    When library-index-mcp is not importable (LIBRARY_INDEX_MCP_ROOT points
    at a non-existent path), query() falls back to the Phase 1 word-hit scorer
    and still returns ranked hits from CATALOG.json.
    """
    import lib.library_index_client as lic_mod

    # Reset module-level import cache
    lic_mod._li_mcp_module = None
    lic_mod._li_mcp_import_error = None
    lic_mod._LI_MCP_SERVER_PATH = None

    # Point at a directory with no server.py → import must fail
    empty_dir = tmp_path / "empty"
    empty_dir.mkdir()
    monkeypatch.setenv("LIBRARY_INDEX_MCP_ROOT", str(empty_dir))

    cat = tmp_path / "CATALOG.json"
    cat.write_text(json.dumps({
        "assets": [
            {
                "path": "/ws/fallback.md",
                "topics": ["fallback", "wordhit"],
                "entities": ["SIG-FALLBACK-001"],
                "depth_score": 0.7,
                "summary": "Phase 1 fallback doc",
            },
            {
                "path": "/ws/other.md",
                "topics": ["noise"],
                "entities": [],
                "depth_score": 0.0,
                "summary": "Unrelated",
            },
        ],
    }))

    from lib.library_index_client import LibraryIndexClient

    client = LibraryIndexClient(catalog_path=cat)
    hits = client.query("fallback wordhit", k=5)

    assert len(hits) >= 1, "Phase 1 fallback must return hits when import fails"
    assert hits[0].path == "/ws/fallback.md", (
        f"Word-hit scorer should rank fallback.md first, got {hits[0].path}"
    )
    # Phase 1 score formula: word_hits * 0.3 + depth_score * 0.7
    # fallback.md: 2 keyword hits in topics, depth=0.7 → score ≥ 2*0.3 + 0.7*0.7 = 1.09
    assert hits[0].score > 0.0

    # status() should report the import failure
    status = client.status()
    assert "wordhit" in status or "not importable" in status or "not found" in status

    # Cleanup
    lic_mod._li_mcp_module = None
    lic_mod._li_mcp_import_error = None
    lic_mod._LI_MCP_SERVER_PATH = None


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
                 "get_core", "audit_chain",
                 "knowledge_status", "knowledge_ingest", "knowledge_query",
                 "knowledge_lint", "knowledge_dossier"):
        assert hasattr(knowledge, name), f"missing tool: {name}"
