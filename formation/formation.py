"""
Formation Flight — typed dispatch payload (MissionBrief) and per-sortie return (MissionReport).

The SHAPE source of truth is the JSON Schema, not this file:
    formation/mission-brief.schema.json
    formation/mission-report.schema.json
These dataclasses are TEST-PINNED to those schemas (see formation/test_formation.py) to prevent
triple-definition drift (schema vs dataclass vs prose). House style mirrors servers/models.py
(dataclasses + str enums + to_dict frontmatter generators).

Spec: SPEC-INTENT-MISSION-BRIEF-001 / SPEC-INTENT-FORMATION-FLIGHT-001.
"""

from __future__ import annotations

from dataclasses import dataclass, field, asdict
from enum import Enum
from typing import Optional


# ─── Enums (reuse the Intent trust band) ──────────────────────

class TrustGate(str, Enum):
    L0 = "L0"
    L1 = "L1"
    L2 = "L2"
    L3 = "L3"
    L4 = "L4"


class Isolation(str, Enum):
    WORKTREE = "worktree"
    READONLY = "readonly"
    NONE = "none"


# ─── Mission Brief (dispatch payload: Tower -> sortie) ─────────

@dataclass
class ReferenceFrame:
    glossary: dict                              # canonical term -> definition
    canonical_terms: list = field(default_factory=list)
    forbidden_synonyms: dict = field(default_factory=dict)


@dataclass
class VerificationRubric:
    contract: Optional[str] = None
    verification_command: Optional[str] = None


@dataclass
class Lineage:
    trace_id: str
    span_id: str
    parent_id: Optional[str] = None


@dataclass
class MissionBrief:
    # required (per mission-brief.schema.json)
    brief_id: str
    intent: str
    seam_id: str
    interface_contract: str
    reference_frame: ReferenceFrame
    invariants: list
    non_goals: list
    trust_gate: str                            # TrustGate value
    lineage: Lineage
    # optional
    title: Optional[str] = None
    drift_markers: list = field(default_factory=list)
    lambda_: float = 1.0                        # NOTE: 'lambda' is a Python keyword; serialized as "lambda"
    isolation: str = "none"
    model: Optional[str] = None
    verification_rubric: Optional[VerificationRubric] = None

    def to_dict(self) -> dict:
        d = {
            "brief_id": self.brief_id,
            "intent": self.intent,
            "seam_id": self.seam_id,
            "interface_contract": self.interface_contract,
            "reference_frame": asdict(self.reference_frame),
            "invariants": list(self.invariants),
            "non_goals": list(self.non_goals),
            "trust_gate": self.trust_gate,
            "lambda": self.lambda_,             # de-keyword on the way out
            "isolation": self.isolation,
            "lineage": {k: v for k, v in asdict(self.lineage).items()
                        if not (k == "parent_id" and v is None)},
        }
        if self.title is not None:
            d["title"] = self.title
        if self.drift_markers:
            d["drift_markers"] = list(self.drift_markers)
        if self.model is not None:
            d["model"] = self.model
        if self.verification_rubric is not None:
            d["verification_rubric"] = {k: v for k, v in asdict(self.verification_rubric).items()
                                        if v is not None}
        return d


# ─── Mission Report (per-sortie return; the gate checks this vs the brief) ─

@dataclass
class Verification:
    command: str
    ran: bool
    passed: bool
    output: Optional[str] = None


@dataclass
class MissionReport:
    # required (per mission-report.schema.json)
    seam_id: str
    brief_id: str
    touched_paths: list
    verification: Verification
    vocabulary_terms: list
    invariants_selfcheck: list
    non_goals_selfcheck: list
    contract_changed: bool
    # optional
    summary: Optional[str] = None
    outputs: list = field(default_factory=list)
    notes: Optional[str] = None

    def to_dict(self) -> dict:
        d = {
            "seam_id": self.seam_id,
            "brief_id": self.brief_id,
            "touched_paths": list(self.touched_paths),
            "verification": {k: v for k, v in asdict(self.verification).items()
                             if not (k == "output" and v is None)},
            "vocabulary_terms": list(self.vocabulary_terms),
            "invariants_selfcheck": list(self.invariants_selfcheck),
            "non_goals_selfcheck": list(self.non_goals_selfcheck),
            "contract_changed": self.contract_changed,
        }
        if self.summary is not None:
            d["summary"] = self.summary
        if self.outputs:
            d["outputs"] = list(self.outputs)
        if self.notes is not None:
            d["notes"] = self.notes
        return d
