---
id: ELEV-{ULID}
type: elevation
status: active                     # active | expired | revoked
granted_by: brien                  # Only Brien can grant
granted_at: null                   # ISO 8601
expires_at: null                   # ISO 8601
duration_minutes: null             # Convenience field
action_types: []                   # Which L0 types are elevated: slack_message, email, pr_create, etc.
scope: null                        # Optional: restrict to target (channel, repo, recipient)
elevated_to: L3                    # Autonomy level actions are elevated to (default L3)
reason: null                       # Why Brien granted this
approvals_auto_approved: []        # List of APR-{id}s auto-approved via this elevation
trace_id: null                     # OTel trace for provenance
---
# Elevation: {action_types} for {duration_minutes}m

## Scope

{scope description — "all Slack" or "#engineering channel only" or "theparlor/skills-engine PRs"}

## Reason

{Brien's reason for granting — "reviewing PRs for the next hour", "high-tempo Slack session"}

## Auto-Approved Actions

{List populated as actions are auto-approved via this elevation}
