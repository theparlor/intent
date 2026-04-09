"""
Cross-engagement leak test scaffold — SPEC-005.

This file establishes the CI machinery for the cross-engagement leak test
described in INT-009 P0 #3. It does NOT yet enforce isolation — the
fixture tree and query-layer wiring land in the full SPEC-005 ship.

For now this file contains:
  1. Pass-today smoke tests that verify the test harness runs correctly
  2. Placeholder tests marked xfail that describe the intended assertions
  3. A sanity check that the test runner can import the intent tree

When SPEC-005 is fully implemented:
  - Fixtures are created in tests/fixtures/
  - The query layer is identified and wired in
  - The xfail tests become real passes
  - A deliberate-leak test is added to verify the test actually catches leaks

Until then, running this file should produce green output with the
expected-failure tests marked xfail, so CI stays green but the shape of
the work is captured.

Reference: .intent/specs/SPEC-005-cross-engagement-leak-test.md
"""

from __future__ import annotations

import os
import sys
from pathlib import Path

import pytest

# Test fixture tree locations (created during full SPEC-005 ship)
REPO_ROOT = Path(__file__).resolve().parents[1]
FIXTURE_ROOT = REPO_ROOT / "tests" / "fixtures"
FIXTURE_CORE = FIXTURE_ROOT / "core-knowledge"
FIXTURE_ALPHA = FIXTURE_ROOT / "engagement-alpha"
FIXTURE_BETA = FIXTURE_ROOT / "engagement-beta"

# Marker strings — distinctive enough for grep-based leak detection.
# These are fake. Real content lives in fixture files.
CORE_MARKERS = ["CORE_MARKER_X7Q2", "CORE_MARKER_M4K9"]
ALPHA_MARKERS = ["ALPHA_SECRET_XYZ", "ALPHA_CLIENT_QRS"]
BETA_MARKERS = ["BETA_SECRET_PQR", "BETA_CLIENT_MNL"]


# ─── Pass-today smoke tests ──────────────────────────────────────────


def test_repo_root_is_intent() -> None:
    """Sanity: the test harness is running in the intent repo."""
    assert (REPO_ROOT / ".intent").is_dir(), (
        f"Expected .intent/ at {REPO_ROOT}, but it's not there. "
        "This test file must live at tests/ inside an intent tree."
    )


def test_spec_005_exists() -> None:
    """The full leak test spec is tracked in .intent/specs/."""
    spec = REPO_ROOT / ".intent" / "specs" / "SPEC-005-cross-engagement-leak-test.md"
    assert spec.exists(), (
        f"SPEC-005 file missing at {spec}. The leak test scaffold "
        "without the spec is context-free — if you removed the spec, "
        "remove the scaffold too."
    )


def test_id_gen_module_available() -> None:
    """The ULID helper is on the Python path (sanity for future tests)."""
    sys.path.insert(0, str(REPO_ROOT / "servers"))
    try:
        import id_gen  # noqa: F401
        from id_gen import generate_id, is_valid_id

        sig_id = generate_id("SIG")
        assert is_valid_id(sig_id, "SIG"), (
            f"ULID helper produced invalid ID: {sig_id}"
        )
    finally:
        sys.path.pop(0)


# ─── Fixture-dependent tests (xfail until fixtures + query layer ship) ──


@pytest.mark.xfail(
    reason="SPEC-005 fixtures not yet created — see .intent/specs/SPEC-005",
    strict=False,
)
def test_fixture_tree_exists() -> None:
    """Fixture tree must exist for any real assertion to work."""
    assert FIXTURE_CORE.is_dir(), f"Missing {FIXTURE_CORE}"
    assert FIXTURE_ALPHA.is_dir(), f"Missing {FIXTURE_ALPHA}"
    assert FIXTURE_BETA.is_dir(), f"Missing {FIXTURE_BETA}"


@pytest.mark.xfail(
    reason="SPEC-005 query layer not yet wired — see .intent/specs/SPEC-005",
    strict=False,
)
def test_alpha_query_returns_alpha_and_core_not_beta() -> None:
    """Query scoped to 'alpha' returns Alpha + Core, zero Beta."""
    result = _query_knowledge_engine(engagement="alpha")
    _assert_markers_present(result, ALPHA_MARKERS + CORE_MARKERS)
    _assert_markers_absent(result, BETA_MARKERS)


@pytest.mark.xfail(
    reason="SPEC-005 query layer not yet wired — see .intent/specs/SPEC-005",
    strict=False,
)
def test_beta_query_returns_beta_and_core_not_alpha() -> None:
    """Query scoped to 'beta' returns Beta + Core, zero Alpha."""
    result = _query_knowledge_engine(engagement="beta")
    _assert_markers_present(result, BETA_MARKERS + CORE_MARKERS)
    _assert_markers_absent(result, ALPHA_MARKERS)


@pytest.mark.xfail(
    reason="SPEC-005 query layer not yet wired — see .intent/specs/SPEC-005",
    strict=False,
)
def test_unscoped_query_returns_only_core() -> None:
    """Query with no engagement context returns only Core."""
    result = _query_knowledge_engine(engagement=None)
    _assert_markers_present(result, CORE_MARKERS)
    _assert_markers_absent(result, ALPHA_MARKERS)
    _assert_markers_absent(result, BETA_MARKERS)


@pytest.mark.xfail(
    reason="SPEC-005 tool-level redaction not yet wired — see .intent/specs/SPEC-005",
    strict=False,
)
def test_mcp_tool_response_does_not_leak_other_engagement() -> None:
    """MCP tool response payload does not contain other engagement's markers."""
    # Placeholder: invoke the actual MCP knowledge tool with engagement context
    # and assert its serialized response does not contain Beta markers when
    # called with Alpha context.
    raise NotImplementedError("wire to MCP server test harness in SPEC-005 Phase 2")


@pytest.mark.xfail(
    reason="SPEC-005 deliberate-leak canary not yet implemented",
    strict=False,
)
def test_deliberate_leak_is_caught() -> None:
    """Inject a fake leak into a fixture and verify the test catches it.

    This is the 'test the test' meta-assertion — a test suite that has
    never failed provides no evidence the test actually tests anything.
    """
    raise NotImplementedError("injected-leak canary in SPEC-005 Phase 3")


# ─── Helpers (placeholder implementations for Phase 2) ──────────────


def _query_knowledge_engine(engagement: str | None) -> str:
    """Query the Knowledge Engine with an optional engagement context.

    Returns the full response as a string for marker-based assertions.

    Placeholder — will be wired to `servers/knowledge.py` or the
    `intent-knowledge query` CLI in SPEC-005 Phase 2.
    """
    raise NotImplementedError(
        "Query layer wiring deferred to SPEC-005 Phase 2. "
        "See .intent/specs/SPEC-005-cross-engagement-leak-test.md "
        "open question #1 for the entrypoint identification."
    )


def _assert_markers_present(response: str, markers: list[str]) -> None:
    """Assert all markers appear in the response."""
    missing = [m for m in markers if m not in response]
    assert not missing, f"Expected markers missing from response: {missing}"


def _assert_markers_absent(response: str, markers: list[str]) -> None:
    """Assert none of the markers appear in the response (the leak assertion)."""
    leaked = [m for m in markers if m in response]
    assert not leaked, (
        f"LEAK DETECTED — these markers should NOT be in the response: {leaked}. "
        "This is the scenario SPEC-005 is designed to prevent. If you're seeing "
        "this in a real run, the engagement isolation contract is broken."
    )
