---
id: ATOM-XXX
title: ""
status: draft  # draft | arb-reviewed | executing | complete | closed

# Work stream references
parent_intent: INT-XXX
spec: SPEC-XXX           # the spec this atom executes against
contracts:               # contracts to verify on completion
  - CON-XXX

# Ownership topology
product: notice | spec | execute | observe | cross-cutting
capability: ""           # which capability within the product

# Execution metadata
priority: now | next | later
size: S | M | L          # S = single session, M = 2-3 sessions, L = multi-day
assignee: ""             # human name or "agent"
autonomy_level: L0 | L1 | L2 | L3 | L4
trust_score: 0.0

# ARB review
arb_verdict: pending | approved | approved-with-concerns | blocked | needs-info
arb_date:
arb_conditions: []

# Lifecycle
created_date:
started_date:
completed_date:
closed_date:
---

# {title}

## Execution Context

What this atom accomplishes in a single pass through the work stream.
The atom references (does not contain) the spec and contracts below.

## Spec Reference

Spec: [{spec}](.intent/specs/{spec}-slug.md)

Brief summary of the spec's current state and what this atom addresses.

## Contracts to Verify

| Contract | Type | Status | Assertion |
|----------|------|--------|-----------|
| CON-XXX  | behavior | pending | Given X, when Y, then Z |

## Dependencies

- [ ] Dependency 1
- [ ] Dependency 2

## Files to Modify

- `path/to/file.ext`

## Acceptance Criteria

This atom is complete when:
- [ ] All referenced contracts pass verification
- [ ] Events emitted for execution start/complete
- [ ] Spec status updated to reflect progress

## ARB Review

### △ Practitioner-Architect
Assessment:

### ◇ Product Leader
Assessment:

### ○ Quality Advocate
Assessment:

### ◉ AI Agent
Assessment:

### ⚡ Claude Code Lens
Assessment:

## Execution Log

<!-- Append entries as the atom progresses -->

## Outcome

What happened in this pass. What persists (spec updates, contract verifications).
What signals emerged for the next cycle.
