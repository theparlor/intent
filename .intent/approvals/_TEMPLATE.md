---
id: APR-{ULID}
type: approval
status: pending                    # pending | approved | denied | expired
action_type: null                  # slack_message | email | pr_create | pr_comment | issue_comment | calendar_change
action_target: null                # Channel, recipient, repo/PR#, calendar event
originating_skill: null            # Which skill produced this action
originating_intent: null           # INT-NNN if traceable
session_id: null                   # Current session identifier
requested_at: null                 # ISO 8601
decided_at: null                   # ISO 8601 (set on approve/deny)
decided_by: null                   # brien | auto:elevation-{id} | ttl_expiry
ttl_seconds: null                  # From approval-rules.yml by action_type
expires_at: null                   # requested_at + ttl_seconds
modification_detected: false       # true if approved_payload differs from original_payload
denial_comment: null               # Required on deny
elevation_id: null                 # If auto-approved via elevation
trace_id: null                     # OTel trace for provenance
linked_expired_id: null            # If this is a revalidation of an expired approval
---
# Approval: {action_type} → {action_target}

## Why

{One-sentence explanation of why this action was produced}

## Original Payload

```json
{original_payload}
```

## Approved Payload

```json
{approved_payload — same as original if no modifications}
```

## If Denied

{Consequence of not sending — what the originating skill will do instead}

## If Modified

{What Brien could change without breaking the flow}

## Decision

{Brien's comment — required on deny, optional on approve}
