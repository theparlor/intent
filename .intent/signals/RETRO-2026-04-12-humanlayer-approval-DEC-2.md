---
id: RETRO-2026-04-12-humanlayer-approval-DEC-2
type: decision
source: session-analysis
decided: 2026-04-12
topic: humanlayer-approval
status: decided
---

# Adopt Approve-With-Modification (updatedInput) Pattern

## Context

HumanLayer's MCP response includes `updatedInput` — the reviewer can modify the proposed action before approving. Brien already does this conversationally but the delta between original and modified payload is lost.

## Decision

IntentApproval entity stores both `original_payload` and `approved_payload`. When Brien modifies before approving, both versions are captured. The delta is training data for improving future L0 action drafts.

## Alternatives Considered

1. **Approve/deny only** — rejected; loses the modification signal
2. **Store only final version** — rejected; can't detect patterns in what Brien consistently edits

## Consequences

- Slightly larger approval records (two payloads)
- Enables "Brien always shortens Slack messages to client X" pattern detection
- Future: template improvement recommendations based on modification patterns
