# Signal: Work Ontology Replacement

ID: SIG-001
Date: 2026-03-28
Status: Captured

## Problem

Agile's ticket-based model treats work as discrete human labor units ("story points", "estimates"). This is misaligned with AI-augmented teams where agents consume specs as structured input, not narrative stories.

## Key Insight

The atomic unit of work shifts from "human labor" to **"declarative state description"**.

## Proposed Hierarchy

A seven-level ontology replaces the ticket:

1. **Signal**: Raw observation or request (unstructured)
   - Source: Design sessions, user feedback, monitoring
   - Channel: Conversation transcripts, GitHub issues, monitoring alerts

2. **Intent**: Declarative goal or outcome (what we want)
   - Parsed from signals
   - Orthogonal to time and implementation
   - Example: "Users should be able to set a daily budget"

3. **Spec**: Detailed requirements and constraints (how to achieve it)
   - Business logic, edge cases, acceptance criteria
   - Agents consume this as program input
   - Example: "Budget must prevent purchases over limit, with email notification on violation"

4. **Contract**: Interface and guarantees (the boundary)
   - Input types, output types, error handling
   - Enables parallelization
   - Example: Input: {userId, dailyBudgetUSD}, Output: {success: boolean, newBudget: object}

5. **Capability**: Atomic skill or subsystem (can be built by agent, human, or hybrid)
   - Self-contained, tested independently
   - Maps 1:1 to a contract

6. **Feature**: Composed capability for users (user-visible behavior)
   - One or more capabilities composed together
   - Has acceptance tests, telemetry

7. **Product**: Integrated system for market
   - Collection of features, versioning, release notes

## Why This Matters for Intent

- **Agents as first-class workers**: Agents read specs, not stories. Specs are executable specifications.
- **Parallelization**: Contracts define clear boundaries, enabling work to be parallelized without human coordination.
- **Observability**: Each unit has metadata: creation time, author, status, tests, telemetry.
- **Traceability**: Link from Product -> Feature -> Capability -> Contract -> Spec -> Intent -> Signal.

## Implementation

Each work unit lives in git:
- Signals: `.intent/signals/` (markdown)
- Intents: `.intent/intents/` (YAML)
- Specs: `.intent/specs/` (YAML + markdown)
- Contracts: `.intent/contracts/` (TypeScript interfaces or JSON Schema)
- Capabilities: Git branches / PR model
- Features: Tags + release notes
- Product: Version tags + CHANGELOG

## Next Steps

1. Define formal schemas for each unit
2. Create tooling to convert Signals -> Intents -> Specs
3. Integrate with CI/CD for automated testing at Contract level
4. Build dashboard to visualize the hierarchy
