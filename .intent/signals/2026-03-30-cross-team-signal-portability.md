---
id: SIG-023
title: Signals need cross-team portability with provenance-carrying IDs
type: insight
source: conversation
source_context: Brien identified need to pass signals between teams
date: 2026-03-30
status: resolved
cluster: schemas
autonomy_level: L1
tags: [ids, teams, portability, provenance, schema]
upstream_control_path: "CLAUDE.md 'Owner: Brien, solo practitioner'; DEC-INTENT-020 (ULID adoption)"
catch_mechanism: "Overtaken by events: Intent crystallized as a solo-practitioner tool rather than a cross-team product, so the provenance-carrying-ID need this signal anticipated never materialized; the collision-avoidance half of the same root problem (SIG-022) was resolved by ULID adoption"
verification_command: "grep -n 'solo practitioner' /Users/brien/Workspaces/Core/frameworks/intent/CLAUDE.md"
---

# SIG-023: Signals need cross-team portability with provenance-carrying IDs

## Observation

Brien identified that signals need to be passable between teams. When Team A notices something that affects Team B's product, the signal needs to travel with its full context — who generated it, which intent it relates to, and the signal itself.

This means IDs can't just be unique — they need to be **self-describing**.

## The Jira Comparison

Jira uses `{PROJECT}-{NNN}` (e.g., MARS-42). This is better than bare numbers because it carries project scope, but:

- Single numbering queue per project creates a bottleneck
- No indication of who created it or when
- Moving a ticket between projects changes its identity
- No hierarchical relationship expressed in the ID

## What a Portable Signal ID Needs

A signal ID that crosses team boundaries should answer:
1. **Who generated it?** — Team or agent origin
2. **What intent does it relate to?** — Parent context (if any)
3. **What is it?** — The signal itself
4. **When?** — Temporal ordering without needing to parse metadata

## Design Principle

The ID should be like a **return address on an envelope** — enough information to route it back to its origin and understand its context without opening it.

## Relates To

- SIG-022 (ID collision in distributed environments, same root problem)
- Work Ontology v2 ownership topology (Product to Capability to Team)
- OTel trace propagation pattern (trace ID flows through all children)

## Triage, 2026-07-08

Disposition: overtaken by events. Intent never grew into a multi-team product; CLAUDE.md is explicit that the owner is "Brien, solo practitioner." The cross-team, provenance-carrying-ID design problem this signal raised has no user to serve. Its sibling problem, ID collision under concurrent writers, was real and got solved (SIG-022, DEC-INTENT-020, ULID adoption); that is the part of "same root problem" that mattered in practice.
