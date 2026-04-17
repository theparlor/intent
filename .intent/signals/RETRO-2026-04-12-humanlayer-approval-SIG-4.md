---
id: RETRO-2026-04-12-humanlayer-approval-SIG-4
type: signal
category: pattern-opportunity
severity: low
source: session-analysis
detected: 2026-04-12
topic: humanlayer-approval
---

# Approve-With-Modification Pattern Missing

## Signal

HumanLayer's `updatedInput` field allows reviewers to modify the proposed action payload before approving. Brien already does this conversationally ("change X, then send") but the original draft and the modified version are not captured as a diff. This delta is training data for improving future L0 drafts.

## Evidence

- HumanLayer MCP response: `{ "behavior": "allow", "updatedInput": { ... } }`
- Brien's current workflow: verbal correction → Claude regenerates → Brien approves
- No structured capture of original vs. modified payload exists

## Implication

Without capturing the modification delta, the system can't learn which types of L0 actions Brien consistently edits. Pattern detection would enable proactive template improvement.

## Recommended Action

IntentApproval entity should store both `original_payload` and `approved_payload` when Brien modifies before approving.
