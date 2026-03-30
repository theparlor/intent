"""
Intent: Shared data models aligned to the Intent schema specification.
Reference: https://theparlor.github.io/intent/schemas.html

Two-plane architecture:
  Ephemeral Flow:  Signal → Intent → Atom → Event → Trace
  Persistent:      Spec, Contract (bridge between planes)
  Structure:       Product → Capability → Team
"""

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Optional
import json
import math


# ─── Enums ────────────────────────────────────────────────────

class SignalSource(str, Enum):
    CLI = "cli"
    MCP = "mcp"
    SLACK = "slack"
    CONVERSATION = "conversation"
    PR_REVIEW = "pr-review"
    AGENT_TRACE = "agent-trace"

class SignalStatus(str, Enum):
    CAPTURED = "captured"
    ACTIVE = "active"
    CLUSTERED = "clustered"
    PROMOTED = "promoted"
    DISMISSED = "dismissed"

class AutonomyLevel(str, Enum):
    L0 = "L0"
    L1 = "L1"
    L2 = "L2"
    L3 = "L3"
    L4 = "L4"

class IntentStatus(str, Enum):
    PROPOSED = "proposed"
    ACCEPTED = "accepted"
    SPECCED = "specced"
    EXECUTING = "executing"
    COMPLETE = "complete"
    ARCHIVED = "archived"

class SpecStatus(str, Enum):
    DRAFT = "draft"
    REVIEW = "review"
    APPROVED = "approved"
    EXECUTING = "executing"
    COMPLETE = "complete"

class ContractType(str, Enum):
    INTERFACE = "interface"
    BEHAVIOR = "behavior"
    QUALITY = "quality"
    INTEGRATION = "integration"

class ContractStatus(str, Enum):
    DEFINED = "defined"
    VERIFIED = "verified"
    FAILED = "failed"
    REVISED = "revised"

class ContractSeverity(str, Enum):
    CRITICAL = "critical"
    MAJOR = "major"
    MINOR = "minor"

class AtomStatus(str, Enum):
    PLANNED = "planned"
    IN_PROGRESS = "in-progress"
    COMPLETE = "complete"
    FAILED = "failed"
    BLOCKED = "blocked"


# ─── Trust Scoring (from Intent schema spec) ─────────────────

def compute_trust(
    clarity: float,
    blast_radius: float,
    reversibility: float,
    testability: float,
    precedent: float,
) -> float:
    """
    trust = clarity * 0.30 + (1/blast_radius) * 0.20 +
            reversibility * 0.20 + testability * 0.20 + precedent * 0.10
    All inputs 0.0-1.0. blast_radius is inverted (high blast = low trust).
    """
    inverse_blast = 1.0 - blast_radius
    raw = (
        clarity * 0.30
        + inverse_blast * 0.20
        + reversibility * 0.20
        + testability * 0.20
        + precedent * 0.10
    )
    return round(max(0.0, min(1.0, raw)), 3)


def trust_to_autonomy(trust: float) -> AutonomyLevel:
    if trust < 0.2:
        return AutonomyLevel.L0
    elif trust < 0.4:
        return AutonomyLevel.L1
    elif trust < 0.6:
        return AutonomyLevel.L2
    elif trust < 0.85:
        return AutonomyLevel.L3
    else:
        return AutonomyLevel.L4


# ─── Signal Amplification ────────────────────────────────────

REFERENCE_WEIGHTS = {
    "signal": 0.15,
    "conversation": 0.10,
    "commit": 0.05,
    "intent": 0.20,
    "spec": 0.20,
}
HALF_LIFE_DAYS = 7

def compute_amplification(references: list[dict], now: datetime = None) -> float:
    now = now or datetime.utcnow()
    score = 0.0
    for ref in references:
        weight = REFERENCE_WEIGHTS.get(ref.get("type", ""), 0.05)
        ref_time = datetime.fromisoformat(ref["timestamp"])
        days_ago = (now - ref_time).total_seconds() / 86400
        decay = math.pow(0.5, days_ago / HALF_LIFE_DAYS)
        score += weight * decay
    return round(score, 4)

def compute_effective_trust(base_trust: float, amplification: float) -> float:
    return round(min(1.0, base_trust + amplification), 3)


# ─── OTel-Compatible Event Types (15) ────────────────────────

EVENT_TYPES = {
    "signal.created", "signal.updated", "signal.dismissed",
    "signal.clustered", "signal.promoted",
    "intent.proposed", "intent.accepted", "intent.specced", "intent.completed",
    "spec.created", "spec.approved", "spec.executing", "spec.completed",
    "contract.verified", "contract.failed",
    "system.status",
}


def make_event(event_type: str, actor: str, ref: str, data: dict = None, source: str = "mcp") -> str:
    """Create a JSONL-formatted OTel-compatible event."""
    return json.dumps({
        "event": event_type,
        "timestamp": datetime.utcnow().isoformat(),
        "actor": actor,
        "ref": ref,
        "data": data or {},
        "source": source,
    })


# ─── Frontmatter Generators ──────────────────────────────────

def signal_frontmatter(sig_id, source, confidence, trust, author,
                       cluster=None, related_intents=None, parent_signal=None):
    autonomy = trust_to_autonomy(trust)
    lines = [
        "---",
        f"id: {sig_id}",
        f"timestamp: {datetime.utcnow().isoformat()}",
        f"source: {source}",
        f"confidence: {confidence}",
        f"trust: {trust}",
        f"autonomy_level: {autonomy.value}",
        f"status: captured",
        f"author: {author}",
    ]
    if cluster:
        lines.append(f"cluster: {cluster}")
    if related_intents:
        lines.append(f"related_intents: [{', '.join(related_intents)}]")
    if parent_signal:
        lines.append(f"parent_signal: {parent_signal}")
    lines.append("---")
    return "\n".join(lines)


def spec_frontmatter(spec_id, title, intent_id, product, author, version="1.0"):
    return "\n".join([
        "---",
        f"id: {spec_id}",
        f"title: {title}",
        f"version: {version}",
        f"status: draft",
        f"intent: {intent_id}",
        f"product: {product}",
        f"author: {author}",
        f"contracts: []",
        f"atoms: []",
        f"completeness_score: 0.0",
        f"agent_ready: false",
        "---",
    ])


def contract_frontmatter(con_id, title, spec_id, contract_type,
                          severity="major", verification_method="manual",
                          verification_command=None):
    lines = [
        "---",
        f"id: {con_id}",
        f"title: {title}",
        f"spec: {spec_id}",
        f"status: defined",
        f"type: {contract_type}",
        f"severity: {severity}",
        f"verification_method: {verification_method}",
    ]
    if verification_command:
        lines.append(f"verification_command: {verification_command}")
    lines.append("---")
    return "\n".join(lines)
