---
id: CLU-004
name: "schemas-identity"
title: "Schemas & Identity"
status: active
signals: [SIG-001, SIG-005, SIG-022, SIG-023]
weight: 1.0
formed_date: 2026-03-30
promoted_to: ""
promoted_date:
---
# Cluster: Schemas & Identity

## Theme
Work units need formal schemas and signal IDs need a distributed-safe strategy. SIG-001 established that Intent needs a formal work ontology — without it, there's no answer to "what replaces tickets?" SIG-005 made the schemas concrete: every work unit must be visible, versioned, testable, and observable with formal file schemas. SIG-022 surfaced the collision problem: sequential IDs broke during multi-agent Cowork sessions. SIG-023 extended this to cross-team portability — IDs must carry provenance when signals move between teams. The cluster is blocked on the ID strategy architecture decision (SIG-022/023) which has long-tail consequences for every schema.

## Member Signals

| Signal | Title | Trust | Date |
|--------|-------|-------|------|
| SIG-001 | Intent needs a formal work ontology | 0.50 | 2026-03-28 |
| SIG-005 | Work units need formal schemas to be agent-consumable | 0.50 | 2026-03-28 |
| SIG-022 | Sequential signal IDs will collide in distributed multi-agent environments | 0.50 | 2026-03-30 |
| SIG-023 | Signals need cross-team portability with provenance-carrying IDs | 0.50 | 2026-03-30 |

## Promotion Criteria
A cluster is ready for promotion to intent when:
- [x] 3+ signals with independent sources
- [ ] Aggregate weight > 1.0 (sum of trust scores)
- [x] At least one signal from the last 14 days (not stale)
- [ ] Pattern is actionable (not just an observation)

## Emergence Notes
How did this cluster form? Was it:
- **Human-noticed:** Brien identified the schema-and-identity pattern across founding observations (SIG-001, SIG-005) and the distributed ID collision friction surfaced during Cowork sessions (SIG-022, SIG-023). The `schemas` cluster tag links SIG-022 and SIG-023.

## Open Questions
- Which ID strategy? UUID v7, ULID, namespaced, composite, or hierarchical? Each has tradeoffs for readability, sortability, collision safety, and provenance.
- Do the 13 existing templates need schema validation tooling, or is YAML frontmatter + convention sufficient?
- How does the ID strategy interact with the event system's trace_id and span_id fields?
