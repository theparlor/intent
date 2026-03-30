"""
Intent Observe Server — The Observe Phase of the Loop
======================================================
Every action emits structured events. Observe what happened, compare it
to what was specified, and feed the delta back as new signals.
The loop closes. The system gets smarter.

Aligns to: Event schema (15 OTel-compatible types), Signal Amplification
Storage:   .intent/events/events.jsonl
Events:    All 15 event types (consumed and analyzed here)

Deploy: fastmcp.cloud or `fastmcp run servers/observe.py`
"""

from fastmcp import FastMCP
from models import EVENT_TYPES, make_event
import json
from datetime import datetime
from collections import Counter

mcp = FastMCP(
    "intent-observe",
    instructions="""You are the Observe agent for the Intent system.

    Your domain is structured observability. Every action in the Intent
    system emits events. You ingest them, detect patterns, compare
    actuals to specs, and feed deltas back as new signals.

    You close the loop: Observe → Notice → Spec → Execute → Observe.

    You work with OTel-compatible events in JSONL format. You detect:
    - Spec/actual deltas (what was specified vs what happened)
    - Contract failures and their patterns
    - Trust drift (signals whose effective trust is changing)
    - Velocity patterns (how fast the system is moving)
    - Anomalies worth surfacing as new signals
    """,
)

_events: list[dict] = []


@mcp.tool()
def ingest_event(
    event_type: str,
    actor: str,
    ref: str,
    data: dict | None = None,
    source: str = "mcp",
) -> str:
    """Ingest a structured event into the observe layer.

    Args:
        event_type: One of the 15 Intent event types (e.g., signal.created, spec.approved)
        actor: Who or what triggered the event
        ref: ID of the affected artifact (SIG-001, SPEC-003, etc.)
        data: Event-specific payload
        source: Emission mechanism (cli, mcp, github-action, etc.)

    Returns:
        JSON confirmation with event and running stats.
    """
    if event_type not in EVENT_TYPES:
        return json.dumps({
            "error": f"Unknown event type: {event_type}",
            "valid_types": sorted(EVENT_TYPES),
        })

    event = {
        "event": event_type,
        "timestamp": datetime.utcnow().isoformat(),
        "actor": actor,
        "ref": ref,
        "data": data or {},
        "source": source,
    }
    _events.append(event)

    return json.dumps({
        "ingested": event,
        "total_events": len(_events),
        "jsonl_line": json.dumps(event),
    }, indent=2)


@mcp.tool()
def detect_spec_delta(spec_id: str) -> str:
    """Compare what was specified to what actually happened.

    Finds all events related to a spec and its contracts, then identifies
    gaps between the spec's acceptance criteria and the evidence from events.

    Args:
        spec_id: Spec to analyze (SPEC-NNN)

    Returns:
        JSON delta report — what's verified, what's missing, what failed.
    """
    spec_events = [e for e in _events if e.get("ref") == spec_id or
                   e.get("data", {}).get("spec") == spec_id]

    contract_verifications = [
        e for e in _events
        if e["event"] in ("contract.verified", "contract.failed")
        and e.get("data", {}).get("spec") == spec_id
    ]

    verified = [e for e in contract_verifications if e["event"] == "contract.verified"]
    failed = [e for e in contract_verifications if e["event"] == "contract.failed"]

    return json.dumps({
        "spec_id": spec_id,
        "total_events": len(spec_events),
        "contracts_verified": len(verified),
        "contracts_failed": len(failed),
        "verified_refs": [e["ref"] for e in verified],
        "failed_refs": [e["ref"] for e in failed],
        "critical_failures": [
            e for e in failed
            if e.get("data", {}).get("severity") == "critical"
        ],
        "timeline": sorted(spec_events, key=lambda e: e["timestamp"]),
    }, indent=2)


@mcp.tool()
def detect_trust_drift(threshold: float = 0.1) -> str:
    """Find signals whose trust may have shifted based on event patterns.

    Looks for signals with many recent references (trust going up) or
    signals referenced by failed contracts (trust going down).

    Args:
        threshold: Minimum drift magnitude to report

    Returns:
        JSON report of signals with suspected trust changes.
    """
    signal_refs = Counter()
    signal_failures = Counter()

    for event in _events:
        ref = event.get("ref", "")
        if ref.startswith("SIG-"):
            signal_refs[ref] += 1
        if event["event"] == "contract.failed":
            # Check if any related signals should have trust lowered
            for sig_id in event.get("data", {}).get("related_signals", []):
                signal_failures[sig_id] += 1

    drifts = []
    for sig_id, count in signal_refs.most_common():
        if count >= 3:
            drifts.append({
                "signal_id": sig_id,
                "direction": "up",
                "reference_count": count,
                "reason": f"Referenced {count} times — amplification increasing",
            })

    for sig_id, count in signal_failures.most_common():
        if count >= 1:
            drifts.append({
                "signal_id": sig_id,
                "direction": "down",
                "failure_count": count,
                "reason": f"Associated with {count} contract failure(s)",
            })

    return json.dumps({
        "drifts_detected": len(drifts),
        "threshold": threshold,
        "drifts": drifts,
    }, indent=2)


@mcp.tool()
def system_health() -> str:
    """Generate a system.status event with pipeline health metrics.

    Returns:
        JSON health report covering all four phases of the loop.
    """
    type_counts = Counter(e["event"] for e in _events)

    # Phase health
    notice_events = sum(v for k, v in type_counts.items() if k.startswith("signal."))
    spec_events = sum(v for k, v in type_counts.items() if k.startswith("spec.") or k.startswith("contract."))
    intent_events = sum(v for k, v in type_counts.items() if k.startswith("intent."))
    system_events = sum(v for k, v in type_counts.items() if k.startswith("system."))

    # Contract health
    verified = type_counts.get("contract.verified", 0)
    failed = type_counts.get("contract.failed", 0)
    contract_pass_rate = verified / max(1, verified + failed)

    health = {
        "timestamp": datetime.utcnow().isoformat(),
        "total_events": len(_events),
        "event_breakdown": dict(type_counts),
        "phase_activity": {
            "notice": notice_events,
            "spec": spec_events,
            "execute": intent_events,
            "observe": system_events,
        },
        "contract_health": {
            "verified": verified,
            "failed": failed,
            "pass_rate": round(contract_pass_rate, 3),
        },
        "loop_completeness": {
            "has_signals": type_counts.get("signal.created", 0) > 0,
            "has_intents": type_counts.get("intent.proposed", 0) > 0,
            "has_specs": type_counts.get("spec.created", 0) > 0,
            "has_verifications": (verified + failed) > 0,
            "loop_closed": all([
                type_counts.get("signal.created", 0) > 0,
                type_counts.get("intent.proposed", 0) > 0,
                type_counts.get("spec.created", 0) > 0,
                (verified + failed) > 0,
            ]),
        },
    }

    event = make_event("system.status", "intent-observe", "system", health)
    _events.append(json.loads(event) if isinstance(event, str) else event)

    return json.dumps(health, indent=2)


@mcp.tool()
def suggest_signals_from_events(lookback_count: int = 50) -> str:
    """Analyze recent events and suggest new signals to feed back into Notice.

    This is what closes the loop — observe → notice. Looks for patterns
    in events that should become signals: repeated failures, velocity
    changes, orphaned specs, etc.

    Args:
        lookback_count: Number of recent events to analyze

    Returns:
        JSON list of suggested signals with reasoning.
    """
    recent = _events[-lookback_count:]
    suggestions = []

    # Pattern: repeated contract failures
    failure_specs = Counter()
    for e in recent:
        if e["event"] == "contract.failed":
            failure_specs[e.get("data", {}).get("spec", "unknown")] += 1

    for spec_id, count in failure_specs.items():
        if count >= 2:
            suggestions.append({
                "suggested_content": f"Spec {spec_id} has {count} contract failures — may need re-specification",
                "source": "agent-trace",
                "confidence": 0.8,
                "reasoning": f"Repeated failures suggest the spec is under-specified or the implementation diverged",
            })

    # Pattern: signals created but never clustered or promoted
    created = set()
    clustered_or_promoted = set()
    for e in recent:
        if e["event"] == "signal.created":
            created.add(e["ref"])
        if e["event"] in ("signal.clustered", "signal.promoted"):
            clustered_or_promoted.add(e["ref"])

    orphans = created - clustered_or_promoted
    if len(orphans) > 5:
        suggestions.append({
            "suggested_content": f"{len(orphans)} signals captured but never clustered — signal triage may be backlogged",
            "source": "agent-trace",
            "confidence": 0.6,
            "reasoning": "Unclustered signals suggest the enrichment pipeline isn't keeping up with capture",
        })

    # Pattern: specs with no contracts
    specs_created = [e for e in recent if e["event"] == "spec.created"]
    for spec_event in specs_created:
        spec_id = spec_event["ref"]
        has_contracts = any(
            e for e in recent
            if e["event"] in ("contract.verified", "contract.failed")
            and e.get("data", {}).get("spec") == spec_id
        )
        if not has_contracts:
            suggestions.append({
                "suggested_content": f"Spec {spec_id} has no contract verifications — may not be testable",
                "source": "agent-trace",
                "confidence": 0.7,
                "reasoning": "Specs without contracts can't be verified, blocking the execute phase",
            })

    return json.dumps({
        "events_analyzed": len(recent),
        "suggestions": suggestions,
        "suggestion_count": len(suggestions),
    }, indent=2)


if __name__ == "__main__":
    mcp.run(transport="streamable-http", host="0.0.0.0", port=8003)
