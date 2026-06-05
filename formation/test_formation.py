"""
Pins the MissionBrief / MissionReport dataclasses (formation.py) to the JSON Schemas
(mission-brief.schema.json / mission-report.schema.json) so the two definitions cannot drift.

Dependency-free: ships a tiny JSON-Schema-subset validator (object/array/enum/type +
required + additionalProperties:false), and ALSO runs the real `jsonschema` validator if it
is installed (best-effort, for extra rigor).

Run:  cd formation && ../servers/.venv/bin/python -m pytest test_formation.py -q
   or: ../servers/.venv/bin/python test_formation.py     (also works via system python3)
"""

import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

from formation import (  # noqa: E402
    MissionBrief, MissionReport, ReferenceFrame, VerificationRubric, Lineage, Verification,
    TrustGate, Isolation,
)

BRIEF_SCHEMA = json.load(open(os.path.join(HERE, "mission-brief.schema.json")))
REPORT_SCHEMA = json.load(open(os.path.join(HERE, "mission-report.schema.json")))


# ─── tiny JSON-Schema-subset validator (no deps) ──────────────

def _check_type(value, t):
    if isinstance(t, list):
        return any(_check_type(value, x) for x in t)
    return {
        "object": lambda v: isinstance(v, dict),
        "array": lambda v: isinstance(v, list),
        "string": lambda v: isinstance(v, str),
        "boolean": lambda v: isinstance(v, bool),
        "number": lambda v: isinstance(v, (int, float)) and not isinstance(v, bool),
        "integer": lambda v: isinstance(v, int) and not isinstance(v, bool),
        "null": lambda v: v is None,
    }.get(t, lambda v: True)(value)


def validate(inst, schema, path="$"):
    t = schema.get("type")
    if t is not None:
        assert _check_type(inst, t), f"{path}: expected type {t}, got {type(inst).__name__}"
    if "enum" in schema:
        assert inst in schema["enum"], f"{path}: {inst!r} not in enum {schema['enum']}"
    if schema.get("type") == "object" and isinstance(inst, dict):
        props = schema.get("properties", {})
        for r in schema.get("required", []):
            assert r in inst, f"{path}: missing required key '{r}'"
        ap = schema.get("additionalProperties")
        if ap is False:
            extra = set(inst) - set(props)
            assert not extra, f"{path}: unexpected keys {sorted(extra)} (additionalProperties:false)"
        for k, v in inst.items():
            if k in props:
                validate(v, props[k], f"{path}.{k}")
            elif isinstance(ap, dict):
                validate(v, ap, f"{path}.{k}")
    if schema.get("type") == "array" and isinstance(inst, list):
        items = schema.get("items")
        if items:
            for i, el in enumerate(inst):
                validate(el, items, f"{path}[{i}]")


def _maybe_jsonschema(inst, schema):
    try:
        import jsonschema  # type: ignore
    except Exception:
        return  # not installed — the subset validator already ran
    jsonschema.validate(inst, schema)


# ─── fixtures ─────────────────────────────────────────────────

def _a_brief() -> MissionBrief:
    return MissionBrief(
        brief_id="MB-s1-p1", intent="INT-x", seam_id="s1", interface_contract="CON-x",
        reference_frame=ReferenceFrame(glossary={"sortie": "one agent, one seam"},
                                       canonical_terms=["sortie"],
                                       forbidden_synonyms={"sortie": ["mission"]}),
        invariants=["schema is source of truth"], non_goals=["do not touch the gate"],
        trust_gate=TrustGate.L4.value,
        lineage=Lineage(trace_id="formation-INT-x", span_id="s1-p1", parent_id="formation-INT-x"),
        title="seam 1", drift_markers=["new field"], lambda_=1.8,
        isolation=Isolation.WORKTREE.value, model="opus",
        verification_rubric=VerificationRubric(contract="CON-x", verification_command="true"),
    )


def _a_report() -> MissionReport:
    return MissionReport(
        seam_id="s1", brief_id="MB-s1-p1", touched_paths=["a.py"],
        verification=Verification(command="true", ran=True, passed=True, output="ok"),
        vocabulary_terms=["sortie"],
        invariants_selfcheck=[{"invariant": "schema is source of truth", "held": True}],
        non_goals_selfcheck=[{"non_goal": "do not touch the gate", "respected": True}],
        contract_changed=False, summary="did the thing", outputs=[{"path": "a.py"}], notes="",
    )


# ─── tests ────────────────────────────────────────────────────

def test_brief_dataclass_conforms():
    d = _a_brief().to_dict()
    validate(d, BRIEF_SCHEMA)
    _maybe_jsonschema(d, BRIEF_SCHEMA)


def test_report_dataclass_conforms():
    d = _a_report().to_dict()
    validate(d, REPORT_SCHEMA)
    _maybe_jsonschema(d, REPORT_SCHEMA)


def test_example_brief_conforms():
    d = json.load(open(os.path.join(HERE, "example-brief.json")))
    validate(d, BRIEF_SCHEMA)
    _maybe_jsonschema(d, BRIEF_SCHEMA)


def test_example_report_conforms():
    d = json.load(open(os.path.join(HERE, "example-report.json")))
    validate(d, REPORT_SCHEMA)
    _maybe_jsonschema(d, REPORT_SCHEMA)


def test_lambda_serialized_as_keyword():
    d = _a_brief().to_dict()
    assert "lambda" in d and "lambda_" not in d, "lambda must serialize as JSON key 'lambda'"


def test_missing_required_is_caught():
    d = _a_brief().to_dict()
    del d["non_goals"]
    try:
        validate(d, BRIEF_SCHEMA)
    except AssertionError:
        return
    raise AssertionError("validator failed to catch a missing required key")


if __name__ == "__main__":
    tests = [v for k, v in sorted(globals().items()) if k.startswith("test_") and callable(v)]
    failed = 0
    for t in tests:
        try:
            t()
            print(f"PASS {t.__name__}")
        except Exception as e:  # noqa: BLE001
            failed += 1
            print(f"FAIL {t.__name__}: {e}")
    print(f"\n{len(tests) - failed}/{len(tests)} passed")
    sys.exit(1 if failed else 0)
