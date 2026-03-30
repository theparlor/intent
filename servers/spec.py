"""
Intent Spec Server — The Spec Phase of the Loop
=================================================
Shapes signals into agent-ready specifications. Specs are contracts,
not stories — verifiable assertions that an AI agent can execute against.
Clear specs mean agents work autonomously; vague specs mean expensive
human intervention.

Aligns to: Spec schema, Contract schema, Atom schema
Storage:   spec/SPEC-NNN-slug.md, spec/contracts/CON-NNN.md
Events:    spec.created, spec.approved, contract.verified, contract.failed

Deploy: fastmcp.cloud or `fastmcp run servers/spec.py`
"""

from fastmcp import FastMCP
from models import (
    SpecStatus, ContractType, ContractStatus, ContractSeverity,
    spec_frontmatter, contract_frontmatter, make_event,
)
import json
from datetime import datetime

mcp = FastMCP(
    "intent-spec",
    instructions="""You are the Spec agent for the Intent system.

    Your job is to transform intents (problems worth solving) into
    agent-ready specifications with verifiable contracts.

    Specs follow the Intent schema:
    - Problem statement grounded in signal evidence
    - Solution description
    - Contracts (verifiable assertions in 4 types: interface, behavior, quality, integration)
    - Acceptance criteria
    - Out of scope
    - Dependencies and test scenarios

    A spec is agent-ready when:
    - completeness_score >= 0.8
    - All contracts have verification_method != 'manual'
    - No ambiguous acceptance criteria

    Contracts are the smallest testable unit — like assertions in code,
    but for any kind of work. Every contract must be precise enough
    that you can write a test for it.
    """,
)

_specs: dict[str, dict] = {}
_contracts: dict[str, dict] = {}
_events: list[str] = []
_next_spec = 1
_next_contract = 1


@mcp.tool()
def create_spec(
    title: str,
    intent_id: str,
    product: str,
    author: str,
    problem_statement: str,
    solution_description: str,
    acceptance_criteria: list[str],
    out_of_scope: list[str] | None = None,
    dependencies: list[str] | None = None,
    test_scenarios: list[str] | None = None,
    version: str = "1.0",
) -> str:
    """Create a specification from an intent.

    A spec is intent made executable. It's the contract between the person
    shaping work and the agent (or person) building it. Good specs are
    verifiable — you can test whether they've been fulfilled.

    Args:
        title: What this spec delivers
        intent_id: Parent intent ID (INT-NNN)
        product: Product boundary (notice, spec, execute, observe)
        author: Who wrote the spec
        problem_statement: The problem, grounded in signal evidence
        solution_description: How we'll solve it
        acceptance_criteria: Testable criteria for completion
        out_of_scope: Explicitly excluded items
        dependencies: What this spec depends on
        test_scenarios: How we'll verify the spec is fulfilled
        version: Semantic version (e.g., "1.0")

    Returns:
        JSON with spec data, frontmatter, completeness assessment, and event.
    """
    global _next_spec
    spec_id = f"SPEC-{_next_spec:03d}"
    _next_spec += 1

    # Assess completeness
    completeness = _assess_completeness(
        problem_statement, solution_description,
        acceptance_criteria, out_of_scope, dependencies, test_scenarios,
    )

    spec = {
        "id": spec_id,
        "title": title,
        "version": version,
        "status": "draft",
        "intent": intent_id,
        "product": product,
        "author": author,
        "contracts": [],
        "atoms": [],
        "completeness_score": completeness,
        "agent_ready": completeness >= 0.8,
        "problem_statement": problem_statement,
        "solution_description": solution_description,
        "acceptance_criteria": acceptance_criteria,
        "out_of_scope": out_of_scope or [],
        "dependencies": dependencies or [],
        "test_scenarios": test_scenarios or [],
        "created_at": datetime.utcnow().isoformat(),
    }

    _specs[spec_id] = spec

    frontmatter = spec_frontmatter(spec_id, title, intent_id, product, author, version)
    event = make_event("spec.created", author, spec_id, {
        "intent": intent_id, "completeness": completeness,
    })
    _events.append(event)

    return json.dumps({
        "spec": spec,
        "frontmatter": frontmatter,
        "completeness_assessment": {
            "score": completeness,
            "agent_ready": completeness >= 0.8,
            "gaps": _identify_gaps(spec),
        },
        "event": json.loads(event),
    }, indent=2)


@mcp.tool()
def create_contract(
    spec_id: str,
    title: str,
    contract_type: str,
    assertion: str,
    severity: str = "major",
    verification_method: str = "manual",
    verification_command: str | None = None,
) -> str:
    """Define a verifiable contract for a spec.

    Contracts are the smallest testable unit. They come in four types:
    - interface: API shape, input/output format
    - behavior: What happens when invoked
    - quality: Non-functional requirements
    - integration: Cross-system interaction

    Args:
        spec_id: Parent spec ID (SPEC-NNN)
        title: What this contract asserts
        contract_type: interface | behavior | quality | integration
        assertion: The verifiable assertion in plain language
        severity: critical | major | minor — impact if contract fails
        verification_method: manual | cli-command | test-suite | automated
        verification_command: Command or test to verify (if not manual)

    Returns:
        JSON with contract data, frontmatter, and event.
    """
    global _next_contract
    if spec_id not in _specs:
        return json.dumps({"error": f"Spec {spec_id} not found"})

    con_id = f"CON-{_next_contract:03d}"
    _next_contract += 1

    contract = {
        "id": con_id,
        "title": title,
        "spec": spec_id,
        "status": "defined",
        "type": contract_type,
        "severity": severity,
        "assertion": assertion,
        "verification_method": verification_method,
        "verification_command": verification_command,
        "verified_date": None,
        "verified_by": None,
        "created_at": datetime.utcnow().isoformat(),
    }

    _contracts[con_id] = contract
    _specs[spec_id]["contracts"].append(con_id)

    # Recalculate spec agent-readiness
    _recalculate_agent_readiness(spec_id)

    frontmatter = contract_frontmatter(
        con_id, title, spec_id, contract_type,
        severity, verification_method, verification_command,
    )

    return json.dumps({
        "contract": contract,
        "frontmatter": frontmatter,
        "spec_agent_ready": _specs[spec_id]["agent_ready"],
    }, indent=2)


@mcp.tool()
def verify_contract(
    contract_id: str,
    verified_by: str,
    passed: bool,
    evidence: str = "",
) -> str:
    """Record the result of verifying a contract.

    Args:
        contract_id: Contract to verify (CON-NNN)
        verified_by: Who or what verified it
        passed: Whether the contract assertion holds
        evidence: Evidence supporting the verification result

    Returns:
        JSON with verification result and emitted event.
    """
    if contract_id not in _contracts:
        return json.dumps({"error": f"Contract {contract_id} not found"})

    con = _contracts[contract_id]
    con["status"] = "verified" if passed else "failed"
    con["verified_date"] = datetime.utcnow().isoformat()
    con["verified_by"] = verified_by

    event_type = "contract.verified" if passed else "contract.failed"
    event = make_event(event_type, verified_by, contract_id, {
        "spec": con["spec"],
        "severity": con["severity"],
        "evidence": evidence,
    })
    _events.append(event)

    return json.dumps({
        "contract_id": contract_id,
        "status": con["status"],
        "verified_by": verified_by,
        "event": json.loads(event),
    }, indent=2)


@mcp.tool()
def assess_agent_readiness(spec_id: str) -> str:
    """Evaluate whether a spec is ready for agent execution.

    A spec is agent-ready when:
    - completeness_score >= 0.8
    - All contracts have non-manual verification methods
    - Acceptance criteria are unambiguous

    Args:
        spec_id: Spec to assess

    Returns:
        JSON readiness report with specific blockers.
    """
    if spec_id not in _specs:
        return json.dumps({"error": f"Spec {spec_id} not found"})

    spec = _specs[spec_id]
    blockers = []
    warnings = []

    # Completeness
    if spec["completeness_score"] < 0.8:
        blockers.append({
            "type": "low_completeness",
            "detail": f"Score {spec['completeness_score']} < 0.8 threshold",
            "gaps": _identify_gaps(spec),
        })

    # Contract verification methods
    manual_contracts = []
    for con_id in spec["contracts"]:
        con = _contracts.get(con_id, {})
        if con.get("verification_method") == "manual":
            manual_contracts.append(con_id)
    if manual_contracts:
        blockers.append({
            "type": "manual_contracts",
            "detail": f"{len(manual_contracts)} contracts require manual verification",
            "contracts": manual_contracts,
        })

    # No contracts at all
    if not spec["contracts"]:
        blockers.append({
            "type": "no_contracts",
            "detail": "Spec has no contracts defined — nothing to verify",
        })

    # Acceptance criteria quality
    for i, criterion in enumerate(spec.get("acceptance_criteria", [])):
        if len(criterion) < 20:
            warnings.append(f"Criterion {i+1} may be too terse to be testable")

    is_ready = len(blockers) == 0
    spec["agent_ready"] = is_ready

    return json.dumps({
        "spec_id": spec_id,
        "agent_ready": is_ready,
        "completeness_score": spec["completeness_score"],
        "blockers": blockers,
        "warnings": warnings,
        "contracts_total": len(spec["contracts"]),
        "contracts_verified": len([
            c for c in spec["contracts"]
            if _contracts.get(c, {}).get("status") == "verified"
        ]),
    }, indent=2)


@mcp.tool()
def get_spec(spec_id: str) -> str:
    """Retrieve a spec by ID."""
    if spec_id in _specs:
        return json.dumps(_specs[spec_id], indent=2)
    return json.dumps({"error": f"Spec {spec_id} not found"})


@mcp.tool()
def list_specs(
    status: str | None = None,
    product: str | None = None,
    agent_ready_only: bool = False,
) -> str:
    """List specs with optional filters."""
    results = []
    for spec in _specs.values():
        if status and spec["status"] != status:
            continue
        if product and spec["product"] != product:
            continue
        if agent_ready_only and not spec["agent_ready"]:
            continue
        results.append(spec)
    return json.dumps({"count": len(results), "specs": results}, indent=2)


# ─── Internal helpers ─────────────────────────────────────────

def _assess_completeness(problem, solution, criteria, out_of_scope, deps, tests):
    score = 0.0
    if len(problem) >= 50:
        score += 0.20
    elif len(problem) >= 20:
        score += 0.10
    if len(solution) >= 50:
        score += 0.20
    elif len(solution) >= 20:
        score += 0.10
    if len(criteria) >= 3:
        score += 0.25
    elif len(criteria) >= 1:
        score += 0.10
    if out_of_scope:
        score += 0.10
    if deps is not None:
        score += 0.05
    if tests and len(tests) >= 1:
        score += 0.20
    elif tests:
        score += 0.10
    return round(min(1.0, score), 2)


def _identify_gaps(spec):
    gaps = []
    if len(spec.get("problem_statement", "")) < 50:
        gaps.append("Problem statement needs more detail")
    if len(spec.get("acceptance_criteria", [])) < 3:
        gaps.append("Need at least 3 acceptance criteria")
    if not spec.get("out_of_scope"):
        gaps.append("No out-of-scope items defined")
    if not spec.get("test_scenarios"):
        gaps.append("No test scenarios defined")
    if not spec.get("contracts"):
        gaps.append("No contracts defined")
    return gaps


def _recalculate_agent_readiness(spec_id):
    spec = _specs.get(spec_id)
    if not spec:
        return
    manual = any(
        _contracts.get(c, {}).get("verification_method") == "manual"
        for c in spec["contracts"]
    )
    spec["agent_ready"] = spec["completeness_score"] >= 0.8 and not manual and len(spec["contracts"]) > 0


if __name__ == "__main__":
    mcp.run(transport="streamable-http", host="0.0.0.0", port=8002)
