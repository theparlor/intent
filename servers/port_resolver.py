"""
Port resolver — preferred port with configurable fallback range.

Shared by the Intent MCP servers (notice/spec/observe) so a second
instance, an orphaned process, or a dev+prod collision on one host does
not produce a hard "address already in use" boot failure. Each process
late-binds the first available port from `preferred + fallbacks` and the
caller logs the port it actually bound.

Pattern ported from the merged upstream fix in
taylorwilsdon/google_workspace_mcp#768 (clean-room reimplementation).

Configuration (environment):
- INTENT_MCP_HOST                   bind host        (default 0.0.0.0)
- INTENT_MCP_PORT_FALLBACK_COUNT    extra ports tried (default 4)
- <port_env> (e.g. INTENT_NOTICE_PORT)  per-server override of the preferred port

Note: there is an unavoidable TOCTOU window between probing a port and
the server actually binding it. Probing collapses that window to
near-zero in practice; it does not eliminate it.
"""

from __future__ import annotations

import logging
import os
import socket

logger = logging.getLogger("intent.port_resolver")

HOST_ENV = "INTENT_MCP_HOST"
FALLBACK_COUNT_ENV = "INTENT_MCP_PORT_FALLBACK_COUNT"
DEFAULT_HOST = "0.0.0.0"
DEFAULT_FALLBACK_COUNT = 4
_PROBE_TIMEOUT_SECONDS = 0.25


class PortConfigError(ValueError):
    """Raised when port-related environment configuration is invalid."""


class NoAvailablePortError(RuntimeError):
    """Raised when no candidate port in the resolved range is bindable."""


def _read_int_env(name: str, default: int, *, minimum: int) -> int:
    raw = os.environ.get(name)
    if raw is None or raw.strip() == "":
        return default
    try:
        value = int(raw)
    except ValueError as exc:
        raise PortConfigError(
            f"{name}={raw!r} is not a valid integer"
        ) from exc
    if value < minimum:
        raise PortConfigError(
            f"{name}={value} is below the minimum of {minimum}"
        )
    return value


def _candidate_ports(preferred: int, fallback_count: int) -> list[int]:
    """Preferred port first, then `fallback_count` sequential ports."""
    return [preferred + offset for offset in range(fallback_count + 1)]


def _is_available(host: str, port: int) -> bool:
    """Two-stage probe: loopback connect check, then a real bind attempt."""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as probe:
        probe.settimeout(_PROBE_TIMEOUT_SECONDS)
        if probe.connect_ex(("127.0.0.1", port)) == 0:
            # Something is already accepting connections here.
            return False

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as binder:
        try:
            binder.bind((host, port))
        except OSError:
            return False
    return True


def resolve_port(
    server_name: str,
    default_port: int,
    *,
    port_env: str,
) -> tuple[str, int]:
    """Resolve the (host, port) the given server should bind.

    Reads the preferred port from ``port_env`` (falling back to
    ``default_port``), the host from ``INTENT_MCP_HOST``, and the number
    of fallback ports from ``INTENT_MCP_PORT_FALLBACK_COUNT``. Returns
    the first available ``(host, port)`` pair.

    Raises:
        PortConfigError: if any env var is malformed.
        NoAvailablePortError: if no candidate port is bindable.
    """
    host = os.environ.get(HOST_ENV) or DEFAULT_HOST
    preferred = _read_int_env(port_env, default_port, minimum=1)
    fallback_count = _read_int_env(
        FALLBACK_COUNT_ENV, DEFAULT_FALLBACK_COUNT, minimum=0
    )

    candidates = _candidate_ports(preferred, fallback_count)
    for port in candidates:
        if _is_available(host, port):
            if port != preferred:
                logger.warning(
                    "%s: preferred port %d unavailable; bound fallback %d",
                    server_name,
                    preferred,
                    port,
                )
            else:
                logger.info("%s: bound preferred port %d", server_name, port)
            return host, port

    raise NoAvailablePortError(
        f"{server_name}: no available port in {candidates} "
        f"(host {host}); set {port_env} or "
        f"{FALLBACK_COUNT_ENV} to widen the range"
    )
