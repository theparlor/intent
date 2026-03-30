---
id: CON-XXX
title: ""
status: defined  # defined | verified | failed | revised
version: 1

# Provenance
spec: SPEC-XXX             # parent spec this contract belongs to
intent: INT-XXX             # grandparent intent for traceability
author: ""
created_date:

# Classification
type: interface | behavior | quality | integration
severity: critical | major | minor

# Verification
verified_date:
verified_by: ""            # human name, agent ID, or "automated"
verification_method: manual | cli-command | test-suite | automated
verification_command: ""   # e.g., "intent-verify CON-XXX" or test command

# Ownership topology
product: notice | spec | execute | observe | cross-cutting
---

# {title}

## Assertion

**Given** [precondition or context]
**When** [action or trigger]
**Then** [expected observable result]

## Verification Method

How to verify this contract passes:

```bash
# Command or steps to verify
```

Expected output or observable result:

## Context

Why this contract exists. What breaks if it fails.
Link to the parent spec for full solution context.

## Contract Types Reference

| Type | Description | Example |
|------|-------------|---------|
| **Interface** | API shape, input/output format | "CLI accepts --format json flag" |
| **Behavior** | What happens when invoked | "Emits signal.created event on capture" |
| **Quality** | Non-functional requirements | "Response time under 200ms" |
| **Integration** | Cross-system interaction | "Event appears in events.jsonl within 5s" |

## Related Contracts

- CON-XXX — {related contract and why}

## Revision History

| Version | Date | Reason |
|---------|------|--------|
| 1 | {created_date} | Initial definition |
