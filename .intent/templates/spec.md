---
id: SPEC-XXX
title: ""
status: draft  # draft | review | approved | executing | complete
version: 1

# Provenance
intent: INT-XXX            # parent intent (the why)
author: ""
created_date:
approved_date:
completed_date:

# Ownership topology
product: notice | spec | execute | observe | cross-cutting
capability: ""

# Linked artifacts
contracts:                 # contracts this spec defines
  - CON-XXX
atoms:                     # atoms that have executed against this spec
  - ATOM-XXX
assignee: ""               # current executor (human or agent)

# Agent-readiness
completeness_score:        # computed: 0-100% based on required fields
agent_ready: false         # true when all contracts are binary pass/fail
---

# {title}

## Problem Statement

What problem does this spec solve? Link to the parent intent and
the signals that drove it.

## Solution

Descriptive solution — what the implementation looks like when done.
This section is human-readable context for anyone reviewing the spec.

## Contracts

Each contract is a verifiable assertion. Contracts are defined here
but live as independent artifacts at `.intent/contracts/CON-NNN.md`.

### CON-XXX: {contract title}
- **Type:** interface | behavior | quality | integration
- **Assertion:** Given [context], when [action], then [expected result]
- **Verification:** How to check — command, test, manual inspection

## Acceptance Criteria

The spec is complete when ALL referenced contracts pass verification.

- [ ] Contract CON-XXX: verified
- [ ] Contract CON-XXX: verified
- [ ] Events emitted: spec.approved, spec.executing, spec.completed

## Out of Scope

What this spec explicitly does NOT cover.

## Dependencies

- Spec SPEC-XXX must be complete
- File `path/to/file` must exist

## Test Scenarios

### Happy path
Given... When... Then...

### Edge case
Given... When... Then...

### Failure mode
Given... When... Then...

## Revision History

| Version | Date | Author | Change |
|---------|------|--------|---------|
| 1 | {created_date} | {author} | Initial draft |
