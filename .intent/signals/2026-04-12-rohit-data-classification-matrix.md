---
id: SIG-032
title: Knowledge Engine needs field-level data classification matrix (public/internal/confidential/restricted)
timestamp: 2026-04-12T01:00:00Z
source: external-article
author: brien
confidence: 0.7
trust: 0.7
autonomy_level: L1
status: active
cluster: persona-fidelity
referenced_by:
  - "Rohit @rohit4verse, 'How to Build a Production-Grade AI Agent' (Feb 2026), Principles 5 and 7"
---

# SIG-032: Data Classification Matrix for Knowledge Engine

## What was noticed

Rohit's Principles 5 (Knowledge Grounding) and 7 (Memory as Architecture) both prescribe a data classification matrix: public, internal, confidential, restricted — with each level dictating storage requirements, access controls, and encryption standards.

Intent's current model has engagement-level federation boundaries (Core = universal, engagements = bounded instances, inherit down, promote up, never leak sideways). But this is coarse-grained. Within an engagement's knowledge artifacts, individual fields may have different confidentiality levels.

Example: A Subaru persona artifact (PER-001) might have public framework descriptions alongside confidential client-specific observations. The current model treats the entire artifact as engagement-scoped. Rohit's model would classify individual fields.

## Evidence

Rohit: "implement a firm data classification matrix, labeling data as public, internal, confidential, or restricted, which dictates storage requirements and access controls."

Intent's DDR-018 (redaction at tool level) prescribes that the MCP server applies confidentiality projection automatically. But the projection granularity is currently artifact-level, not field-level.

## Implication

When the Knowledge Farm is deployed as a hosted MCP server accessible from mobile, field-level classification becomes important — Brien querying from a phone in public should get different projections than Brien querying from his studio desk. The federation boundary model needs a field-level confidentiality annotation in the knowledge artifact schema.
