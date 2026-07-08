"""
Tests for port_resolver.py, the fallback-on-conflict port resolution shared
by the Intent MCP servers (notice/spec/observe/knowledge).

Origin: SIG-035-intent-mcp-servers-hardcode-ports.md flagged that the
resolver and its server wiring were committed (2026-05-19) but had no
committed regression test, so fallback-on-conflict, env-override,
malformed-config, and range-exhaustion behavior had no catch mechanism.
This file is that catch mechanism.

Strategy:
  - Each test occupies a real localhost socket to force a collision, then
    asserts resolve_port() steps past it, exactly the scenario the module's
    docstring describes (second instance / orphaned process / dev+prod
    collision on one host).
  - Environment variables are cleared and restored per test via monkeypatch
    so INTENT_MCP_HOST / INTENT_MCP_PORT_FALLBACK_COUNT / a per-server
    port_env do not leak between tests or from the ambient environment.
"""
from __future__ import annotations

import socket
import sys
from pathlib import Path

import pytest

HERE = Path(__file__).resolve().parent
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))

import port_resolver  # noqa: E402


PORT_ENV = "INTENT_TEST_PORT_RESOLVER_PORT"


@pytest.fixture(autouse=True)
def clean_env(monkeypatch):
    """Ensure no ambient env var leaks into a test's expected default."""
    for name in (port_resolver.HOST_ENV, port_resolver.FALLBACK_COUNT_ENV, PORT_ENV):
        monkeypatch.delenv(name, raising=False)


def _free_port() -> int:
    """Ask the OS for a currently-unused port."""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(("127.0.0.1", 0))
        return s.getsockname()[1]


def test_binds_preferred_port_when_free():
    preferred = _free_port()
    host, port = port_resolver.resolve_port(
        "test-server", preferred, port_env=PORT_ENV
    )
    assert port == preferred
    assert host == port_resolver.DEFAULT_HOST


def test_falls_back_when_preferred_port_occupied():
    preferred = _free_port()
    # Occupy the preferred port for the duration of the resolve call.
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as occupier:
        occupier.bind(("127.0.0.1", preferred))
        occupier.listen(1)
        host, port = port_resolver.resolve_port(
            "test-server", preferred, port_env=PORT_ENV
        )
        assert port != preferred
        assert preferred < port <= preferred + port_resolver.DEFAULT_FALLBACK_COUNT


def test_env_override_of_preferred_port(monkeypatch):
    default_port = _free_port()
    override_port = _free_port()
    monkeypatch.setenv(PORT_ENV, str(override_port))
    host, port = port_resolver.resolve_port(
        "test-server", default_port, port_env=PORT_ENV
    )
    assert port == override_port


def test_malformed_port_env_raises_config_error(monkeypatch):
    monkeypatch.setenv(PORT_ENV, "not-a-port")
    with pytest.raises(port_resolver.PortConfigError):
        port_resolver.resolve_port("test-server", _free_port(), port_env=PORT_ENV)


def test_malformed_fallback_count_raises_config_error(monkeypatch):
    monkeypatch.setenv(port_resolver.FALLBACK_COUNT_ENV, "not-a-count")
    with pytest.raises(port_resolver.PortConfigError):
        port_resolver.resolve_port("test-server", _free_port(), port_env=PORT_ENV)


def test_negative_fallback_count_raises_config_error(monkeypatch):
    monkeypatch.setenv(port_resolver.FALLBACK_COUNT_ENV, "-1")
    with pytest.raises(port_resolver.PortConfigError):
        port_resolver.resolve_port("test-server", _free_port(), port_env=PORT_ENV)


def test_range_exhaustion_raises_no_available_port_error(monkeypatch):
    preferred = _free_port()
    monkeypatch.setenv(port_resolver.FALLBACK_COUNT_ENV, "2")
    sockets = []
    try:
        # Occupy preferred, preferred+1, preferred+2 (the full candidate range).
        for offset in range(3):
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.bind(("127.0.0.1", preferred + offset))
            s.listen(1)
            sockets.append(s)
        with pytest.raises(port_resolver.NoAvailablePortError):
            port_resolver.resolve_port(
                "test-server", preferred, port_env=PORT_ENV
            )
    finally:
        for s in sockets:
            s.close()


def test_custom_host_env_is_honored(monkeypatch):
    monkeypatch.setenv(port_resolver.HOST_ENV, "127.0.0.1")
    preferred = _free_port()
    host, port = port_resolver.resolve_port(
        "test-server", preferred, port_env=PORT_ENV
    )
    assert host == "127.0.0.1"
    assert port == preferred
