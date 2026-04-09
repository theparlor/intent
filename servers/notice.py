"""
Intent Notice Server — The Notice Phase of the Loop
=====================================================
Captures signals, enriches with trust scoring, clusters related signals,
and promotes clusters to intents. This is the "upstream" that Intent
argues is the real bottleneck when AI collapses implementation cost.

Aligns to: Signal schema, Signal Amplification spec, Event types
Storage:   .intent/signals/YYYY-MM-DD-slug.md (frontmatter + body)
Events:    signal.created, signal.updated, signal.dismissed,
           signal.clustered, signal.promoted

Deploy: fastmcp.cloud or `fastmcp run servers/notice.py`
"""

from fastmcp import FastMCP
from models import (
    SignalSource, SignalStatus, AutonomyLevel,
    compute_trust, trust_to_autonomy, compute_amplification,
    compute_effective_trust, signal_frontmatter, make_event,
    REFERENCE_WEIGHTS, TraceContext,
)
from id_gen import generate_id
import json
from datetime import datetime

mcp = FastMCP(
    "intent-notice",
    instructions="""You are the Notice agent for the Intent system.
    Your domain is the upstream signal layer — the part Intent argues
    is the real bottleneck when AI collapses implementation cost.

    You capture signals, compute trust scores, determine autonomy levels,
    cluster related signals, and promote clusters to intents.

    Every signal you create must have:
    - Clear, specific content (not vague summaries)
    - A source attribution (cli, mcp, slack, conversation, pr-review, agent-trace)
    - Trust factors scored for the trust formula
    - At minimum a confidence score

    Signal lifecycle: captured → active → clustered → promoted | dismissed
    Trust formula: clarity×0.30 + (1/blast_radius)×0.20 + reversibility×0.20
                   + testability×0.20 + precedent×0.10
    """,
)

# In-memory store — replace with .intent/signals/ file I/O for production
_signals: dict[str, dict] = {}
_events: list[str] = []  # JSONL event log
_trace_ctx = TraceContext()


def _gen_id():
    # ULID-based per SIG-022 — globally unique, no coordination required.
    # Replaces the legacy sequential counter that broke across MCP server
    # restarts and concurrent writers.
    return generate_id("SIG")


@mcp.tool()
def create_signal(
    content: str,
    source: str = "conversation",
    author: str = "human",
    confidence: float = 0.7,
    clarity: float = 0.5,
    blast_radius: float = 0.3,
    reversibility: float = 0.7,
    testability: float = 0.5,
    precedent: float = 0.3,
    cluster: str | None = None,
    related_intents: list[str] | None = None,
    parent_signal: str | None = None,
) -> str:
    """Capture a new signal — the atomic unit of the Notice layer.

    A signal is a structured observation worth tracking. It gets trust-scored
    and assigned an autonomy level that determines how much agent freedom
    any downstream action gets.

    Args:
        content: What was observed. Be specific, not vague.
        source: One of: cli, mcp, slack, conversation, pr-review, agent-trace
        author: Who captured this signal
        confidence: 0.0-1.0 — how confident the capturer is this matters
        clarity: 0.0-1.0 — how well-defined is the observation?
        blast_radius: 0.0-1.0 — how much damage if wrong? (high = lower trust)
        reversibility: 0.0-1.0 — can the action be undone?
        testability: 0.0-1.0 — can we verify accuracy before acting?
        precedent: 0.0-1.0 — have similar signals been acted on before?
        cluster: Optional cluster name if grouping with related signals
        related_intents: Optional list of intent IDs this relates to
        parent_signal: Optional SIG-ID if this refines another signal

    Returns:
        JSON with signal data, trust score, autonomy level, and frontmatter.
    """
    sig_id = _gen_id()
    trust = compute_trust(clarity, blast_radius, reversibility, testability, precedent)
    autonomy = trust_to_autonomy(trust)

    signal = {
        "id": sig_id,
        "timestamp": datetime.utcnow().isoformat(),
        "source": source,
        "confidence": confidence,
        "trust": trust,
        "autonomy_level": autonomy.value,
        "status": "captured",
        "cluster": cluster,
        "author": author,
        "related_intents": related_intents or [],
        "parent_signal": parent_signal,
        "content": content,
        "trust_factors": {
            "clarity": clarity,
            "blast_radius": blast_radius,
            "reversibility": reversibility,
            "testability": testability,
            "precedent": precedent,
        },
        "amplification": {
            "referenced_by": [],
            "reference_count": 0,
            "amplification_score": 0.0,
            "effective_trust": trust,
        },
    }

    _signals[sig_id] = signal

    # Emit event
    event = make_event("signal.created", author, sig_id, {
        "source": source, "trust": trust, "autonomy_level": autonomy.value,
    })
    _events.append(event)

    # Generate the markdown frontmatter for .intent/signals/ storage
    frontmatter = signal_frontmatter(
        sig_id, source, confidence, trust, author,
        cluster, related_intents, parent_signal,
    )

    return json.dumps({
        "signal": signal,
        "frontmatter": frontmatter,
        "event": json.loads(event),
    }, indent=2)


@mcp.tool()
def score_trust(
    signal_id: str,
    clarity: float,
    blast_radius: float,
    reversibility: float,
    testability: float,
    precedent: float,
    reasoning: str = "",
) -> str:
    """Rescore a signal's trust factors. Recalculates trust and autonomy level.

    Use when enrichment reveals new information that changes the trust assessment.
    If the new trust crosses an autonomy level boundary, flags for review.

    Args:
        signal_id: Signal to rescore
        clarity: Updated clarity assessment (0.0-1.0)
        blast_radius: Updated blast radius (0.0-1.0)
        reversibility: Updated reversibility (0.0-1.0)
        testability: Updated testability (0.0-1.0)
        precedent: Updated precedent (0.0-1.0)
        reasoning: Why the trust factors changed

    Returns:
        JSON with old/new trust, old/new autonomy, and boundary crossing flag.
    """
    if signal_id not in _signals:
        return json.dumps({"error": f"Signal {signal_id} not found"})

    sig = _signals[signal_id]
    old_trust = sig["trust"]
    old_autonomy = sig["autonomy_level"]

    new_trust = compute_trust(clarity, blast_radius, reversibility, testability, precedent)
    new_autonomy = trust_to_autonomy(new_trust)

    sig["trust"] = new_trust
    sig["autonomy_level"] = new_autonomy.value
    sig["trust_factors"] = {
        "clarity": clarity, "blast_radius": blast_radius,
        "reversibility": reversibility, "testability": testability,
        "precedent": precedent,
    }

    # Recalculate effective trust with amplification
    amp_score = sig["amplification"]["amplification_score"]
    sig["amplification"]["effective_trust"] = compute_effective_trust(new_trust, amp_score)

    # Emit update event
    event = make_event("signal.updated", "intent-notice", signal_id, {
        "field": "trust", "old": old_trust, "new": new_trust,
        "reasoning": reasoning,
    })
    _events.append(event)

    boundary_crossed = old_autonomy != new_autonomy.value

    return json.dumps({
        "signal_id": signal_id,
        "old_trust": old_trust,
        "new_trust": new_trust,
        "old_autonomy": old_autonomy,
        "new_autonomy": new_autonomy.value,
        "boundary_crossed": boundary_crossed,
        "review_flagged": boundary_crossed,
        "reasoning": reasoning,
    }, indent=2)


@mcp.tool()
def cluster_signals(
    signal_ids: list[str],
    cluster_name: str,
    reasoning: str = "",
) -> str:
    """Group related signals into a named cluster.

    Signals that get referenced together reveal emergent problem structure.
    Clustering is the precursor to promotion — when a cluster reaches
    critical mass, it becomes an intent.

    Args:
        signal_ids: List of signal IDs to cluster
        cluster_name: Descriptive name for the cluster
        reasoning: Why these signals belong together

    Returns:
        JSON with cluster summary and updated signals.
    """
    found = []
    missing = []
    for sid in signal_ids:
        if sid in _signals:
            found.append(sid)
        else:
            missing.append(sid)

    for sid in found:
        _signals[sid]["cluster"] = cluster_name
        _signals[sid]["status"] = "clustered"
        event = make_event("signal.clustered", "intent-notice", sid, {
            "cluster": cluster_name,
        })
        _events.append(event)

    return json.dumps({
        "cluster_name": cluster_name,
        "signals_clustered": len(found),
        "signal_ids": found,
        "missing_ids": missing,
        "reasoning": reasoning,
    }, indent=2)


@mcp.tool()
def promote_to_intent(
    signal_ids: list[str],
    intent_title: str,
    problem_statement: str,
    proposed_by: str = "human",
    priority: str = "next",
    product: str = "notice",
) -> str:
    """Promote a cluster of signals to an Intent — a problem worth solving.

    This is the bridge from 'we keep noticing this' to 'let's spec a solution.'
    The intent carries evidence from the signals that spawned it.

    Args:
        signal_ids: Signals being promoted (typically a cluster)
        intent_title: Short description of the problem
        problem_statement: What the problem is, informed by signal evidence
        proposed_by: Who is proposing this intent
        priority: now | next | later
        product: Which Intent product this addresses (notice, spec, execute, observe)

    Returns:
        JSON with the created intent and updated signal statuses.
    """
    intent_id = f"INT-{len([e for e in _events if 'intent.proposed' in e]) + 1:03d}"

    # Generate trace_id for the new intent
    trace_id = _trace_ctx.register_intent(intent_id)

    # Mark signals as promoted and backfill with trace_id
    for sid in signal_ids:
        if sid in _signals:
            _signals[sid]["status"] = "promoted"
            event = make_event("signal.promoted", proposed_by, sid, {
                "intent_title": intent_title, "intent_id": intent_id,
            }, trace_id=trace_id, span_id=sid, parent_id=intent_id)
            _events.append(event)
            # Backfill: link signal to the trace
            backfill = make_event("signal.updated", "system", sid, {
                "trace_linked": True, "intent_id": intent_id,
            }, trace_id=trace_id, span_id=sid, parent_id=intent_id)
            _events.append(backfill)

    intent_event = make_event("intent.proposed", proposed_by, intent_id, {
        "title": intent_title,
        "signals": signal_ids,
        "priority": priority,
        "product": product,
    }, trace_id=trace_id, span_id=intent_id)
    _events.append(intent_event)

    return json.dumps({
        "intent": {
            "id": intent_id,
            "title": intent_title,
            "status": "proposed",
            "proposed_by": proposed_by,
            "signals": signal_ids,
            "priority": priority,
            "product": product,
            "problem_statement": problem_statement,
        },
        "signals_promoted": len(signal_ids),
        "event": json.loads(intent_event),
    }, indent=2)


@mcp.tool()
def add_reference(
    signal_id: str,
    reference_type: str,
    referenced_by: str,
) -> str:
    """Record a reference to a signal, updating its amplification score.

    Reference weights: signal=0.15, conversation=0.10, commit=0.05,
    intent/spec=0.20. References decay with 7-day half-life.

    Args:
        signal_id: Signal being referenced
        reference_type: One of: signal, conversation, commit, intent, spec
        referenced_by: ID of the artifact referencing this signal

    Returns:
        JSON with updated amplification and effective trust.
    """
    if signal_id not in _signals:
        return json.dumps({"error": f"Signal {signal_id} not found"})

    sig = _signals[signal_id]
    amp = sig["amplification"]

    amp["referenced_by"].append(referenced_by)
    amp["reference_count"] += 1

    # Recompute amplification from all references
    refs = [{"type": reference_type, "timestamp": datetime.utcnow().isoformat()}]
    # In production, store all references with timestamps
    new_amp = compute_amplification(refs)
    amp["amplification_score"] = round(amp["amplification_score"] + new_amp, 4)
    amp["effective_trust"] = compute_effective_trust(sig["trust"], amp["amplification_score"])
    amp["last_referenced"] = datetime.utcnow().isoformat()

    # Check if effective trust crosses autonomy boundary
    old_autonomy = sig["autonomy_level"]
    new_autonomy = trust_to_autonomy(amp["effective_trust"]).value
    boundary_crossed = old_autonomy != new_autonomy

    return json.dumps({
        "signal_id": signal_id,
        "reference_type": reference_type,
        "weight": REFERENCE_WEIGHTS.get(reference_type, 0.05),
        "amplification_score": amp["amplification_score"],
        "effective_trust": amp["effective_trust"],
        "base_trust": sig["trust"],
        "boundary_crossed": boundary_crossed,
        "review_flagged": boundary_crossed,
    }, indent=2)


@mcp.tool()
def list_signals(
    status: str | None = None,
    cluster: str | None = None,
    min_trust: float = 0.0,
    limit: int = 25,
) -> str:
    """Query signals with optional filters.

    Args:
        status: Filter by lifecycle status (captured, active, clustered, promoted, dismissed)
        cluster: Filter by cluster name
        min_trust: Minimum trust score threshold
        limit: Max results

    Returns:
        JSON array of matching signals.
    """
    results = []
    for sig in _signals.values():
        if status and sig["status"] != status:
            continue
        if cluster and sig.get("cluster") != cluster:
            continue
        effective = sig["amplification"]["effective_trust"]
        if effective < min_trust:
            continue
        results.append(sig)
        if len(results) >= limit:
            break

    return json.dumps({"count": len(results), "signals": results}, indent=2)


@mcp.tool()
def get_signal(signal_id: str) -> str:
    """Retrieve a single signal by ID.

    Args:
        signal_id: e.g. SIG-001

    Returns:
        Full signal JSON or error.
    """
    if signal_id in _signals:
        return json.dumps(_signals[signal_id], indent=2)
    return json.dumps({"error": f"Signal {signal_id} not found"})


@mcp.tool()
def dismiss_signal(signal_id: str, reason: str = "") -> str:
    """Dismiss a signal — mark it as no longer relevant.

    Args:
        signal_id: Signal to dismiss
        reason: Why it's being dismissed

    Returns:
        Confirmation with event.
    """
    if signal_id not in _signals:
        return json.dumps({"error": f"Signal {signal_id} not found"})

    _signals[signal_id]["status"] = "dismissed"
    event = make_event("signal.dismissed", "human", signal_id, {"reason": reason})
    _events.append(event)

    return json.dumps({
        "signal_id": signal_id,
        "status": "dismissed",
        "reason": reason,
    }, indent=2)


@mcp.tool()
def get_events(limit: int = 50) -> str:
    """Get recent events from the event log.

    Args:
        limit: Number of recent events to return

    Returns:
        JSON array of recent events (newest first).
    """
    recent = _events[-limit:]
    recent.reverse()
    return json.dumps([json.loads(e) for e in recent], indent=2)


if __name__ == "__main__":
    mcp.run(transport="streamable-http", host="0.0.0.0", port=8001)
