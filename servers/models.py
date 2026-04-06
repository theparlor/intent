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
import os
import uuid


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


# ─── Knowledge Artifact Types ──────────────────────────────

class KnowledgeArtifactType(str, Enum):
    PERSONA = "persona"
    JOURNEY = "journey"
    DECISION = "decision"
    THEME = "theme"
    DOMAIN_MODEL = "domain-model"
    DESIGN_RATIONALE = "rationale"


# ─── OTel-Compatible Event Types (18) ────────────────────────

EVENT_TYPES = {
    "signal.created", "signal.updated", "signal.dismissed",
    "signal.clustered", "signal.promoted",
    "intent.proposed", "intent.accepted", "intent.specced", "intent.completed",
    "spec.created", "spec.approved", "spec.executing", "spec.completed",
    "contract.verified", "contract.failed",
    "knowledge.ingested", "knowledge.queried", "knowledge.linted",
    "system.status",
}


def generate_trace_id() -> str:
    """Generate a UUID v4 trace ID for an Intent."""
    return str(uuid.uuid4())


def make_event(event_type: str, actor: str, ref: str, data: dict = None, source: str = "mcp",
               trace_id: str = None, span_id: str = None, parent_id: str = None) -> str:
    """Create a JSONL-formatted OTel-compatible event with trace context."""
    return json.dumps({
        "version": "0.2.0",
        "event": event_type,
        "timestamp": datetime.utcnow().isoformat(),
        "trace_id": trace_id,
        "span_id": span_id or ref,
        "parent_id": parent_id,
        "actor": actor,
        "ref": ref,
        "data": data or {},
        "source": source,
    })


TRACE_CONTEXT_FILE = "trace-context.json"


class TraceContext:
    """Maps Intent IDs and Spec IDs to their trace context.
    Persists to .intent/trace-context.json for cross-server correlation."""

    def __init__(self, intent_root: str = "."):
        self._path = os.path.join(intent_root, ".intent", TRACE_CONTEXT_FILE)
        self._load()

    def _load(self):
        try:
            with open(self._path) as f:
                data = json.load(f)
                self._intents = data.get("intents", {})
                self._specs = {k: tuple(v) for k, v in data.get("specs", {}).items()}
        except (FileNotFoundError, json.JSONDecodeError):
            self._intents = {}
            self._specs = {}

    def _save(self):
        os.makedirs(os.path.dirname(self._path), exist_ok=True)
        with open(self._path, "w") as f:
            json.dump({
                "intents": self._intents,
                "specs": {k: list(v) for k, v in self._specs.items()},
            }, f, indent=2)

    def register_intent(self, intent_id: str) -> str:
        """Create or retrieve trace_id for an intent."""
        if intent_id not in self._intents:
            self._intents[intent_id] = generate_trace_id()
            self._save()
        return self._intents[intent_id]

    def get_intent_trace(self, intent_id: str) -> str | None:
        return self._intents.get(intent_id)

    def register_spec(self, spec_id: str, intent_id: str) -> tuple[str | None, str]:
        """Register a spec under an intent. Returns (trace_id, parent_id)."""
        trace_id = self.get_intent_trace(intent_id)
        if trace_id:
            self._specs[spec_id] = (trace_id, intent_id)
            self._save()
        return trace_id, intent_id

    def get_spec_trace(self, spec_id: str) -> tuple[str | None, str | None]:
        """Returns (trace_id, parent_id) for a spec."""
        return self._specs.get(spec_id, (None, None))


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
