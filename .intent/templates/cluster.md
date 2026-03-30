---
id: CLU-XXX
name: ""            # kebab-case identifier (e.g., signal-capture-surfaces)
title: ""           # Human-readable cluster name
status: forming    # forming → active → promoted → dissolved
signals: []        # SIG-XXX IDs in this cluster
weight: 0          # Aggregate signal weight (sum of trust scores)
formed_date: YYYY-MM-DD
promoted_to: ""    # INT-XXX if promoted to intent
promoted_date:
---
# Cluster: [title]

## Theme
What connects these signals? Describe the underlying pattern or friction
in one paragraph. This is the "so what" — why these signals belong together.

## Member Signals

| Signal | Title | Trust | Date |
|--------|-------|-------|------|
| SIG-XXX | ... | 0.XX | YYYY-MM-DD |

## Promotion Criteria
A cluster is ready for promotion to intent when:
- [ ] 3+ signals with independent sources
- [ ] Aggregate weight > 1.0 (sum of trust scores)
- [ ] At least one signal from the last 14 days (not stale)
- [ ] Pattern is actionable (not just an observation)

## Emergence Notes
How did this cluster form? Was it:
- **Auto-detected:** keyword co-occurrence or reference overlap
- **Human-noticed:** someone saw the pattern manually
- **Agent-suggested:** AI flagged the connection

## Open Questions
What don't we know yet about this pattern?
