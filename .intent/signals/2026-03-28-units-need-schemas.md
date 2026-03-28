# Signal: Work Units Need Formal Schemas

ID: SIG-005
Date: 2026-03-28
Status: Captured

## Problem

Without schemas, agents can't consume work units reliably. Signals, Intents, Specs need to be parseable by machines, not just readable by humans.

## Insight

Each work unit needs:
1. **File format** (where/how it lives)
2. **Schema** (what fields it has)
3. **State machine** (valid transitions)
4. **Unique ID** (linkable and traceable)
5. **Git tracking** (history and blame)
6. **Self-testing** (validate on commit)

## Example: Signal Schema

**File location**: `.intent/signals/{YYYY-MM-DD}-{slug}.md`

**Format**: YAML front-matter + Markdown body

```yaml
---
id: SIG-001
date: 2026-03-28
source: design_session  # or: customer_feedback, monitoring, code_review
severity: high  # or: medium, low
status: captured  # or: parsed, scheduled, building, shipped
participants: [alice, bob]
related_signals: []
related_intents: []
---
# Signal: User confusion around budget limits

## Observation

[Specific, precise observation]

## Impact

[Why this matters]

## Constraint or Opportunity

[Any limitations or possibilities]
```

**Schema validation** (JSON Schema):
```json
{
  "type": "object",
  "required": ["id", "date", "source", "status"],
  "properties": {
    "id": {"type": "string", "pattern": "^SIG-[0-9]{3,}$"},
    "date": {"type": "string", "format": "date"},
    "source": {"enum": ["design_session", "customer_feedback", "monitoring", "code_review"]},
    "severity": {"enum": ["low", "medium", "high"]},
    "status": {"enum": ["captured", "parsed", "scheduled", "building", "shipped"]},
    "participants": {"type": "array", "items": {"type": "string"}}
  }
}
```

**State machine**:
```
captured -> parsed -> scheduled -> building -> shipped
```

## Example: Spec Schema

**File location**: `.intent/specs/{id}.yaml`

```yaml
id: SPEC-001
intent_id: INT-001
status: draft  # or: review, approved, building, testing, shipped

# Description
title: "Daily budget enforcement with email notification"
description: |
  Users should be able to set a daily spending limit.
  When spending would exceed the limit, block the transaction and send an email.

# Requirements
requirements:
  - id: REQ-001
    text: "Users can set a daily budget via settings page"
    acceptance_criteria:
      - "Budget must be between $0 and $100,000"
      - "Budget persists across sessions"
  - id: REQ-002
    text: "Transactions exceeding budget are blocked"
    acceptance_criteria:
      - "Block is immediate (< 10ms)"
      - "User gets error message"

# Dependencies
contracts:
  - CON-001  # User settings storage
  - CON-002  # Budget enforcement
  - CON-003  # Email service

# Testing
test_coverage_target: 0.90
performance_slo:
  budget_check_latency_p99_ms: 10
  settings_save_latency_p99_ms: 100

# Governance
architecture_review_required: true
approvers: [arch-team]
```

## Why Schemas Matter

1. **Agents can read**: Structured data is machine-consumable
2. **Validation on commit**: Pre-commit hooks check schema compliance
3. **Linking**: UUIDs make specs linkable (spec refers to intent, intent refers to signal)
4. **Observability**: Can query/filter work by status, owner, dependency
5. **Automation**: Can build tooling (e.g., "create a PR for all specs in review")

## Tradeoff: YAML vs. Markdown

- **YAML**: Machine-friendly, agents can parse and modify
- **Markdown**: Human-friendly, easy to read and write

**Solution**: YAML front-matter + Markdown body
- Machines read YAML, humans read body
- Both are version-controlled and linked

## Implementation

1. Define JSON Schema for each unit type (Signal, Intent, Spec, Contract, etc.)
2. Add schema validation to pre-commit hooks
3. Build CLI tool: `intent validate` (checks all files)
4. Add to CI/CD: validation must pass before merge
5. Generate documentation from schemas

## Next Steps

- Write full schemas for all 7 work unit types
- Create validation tooling
- Document examples
