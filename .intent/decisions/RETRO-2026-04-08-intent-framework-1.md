---
decision_id: RETRO-2026-04-08-intent-framework-1
title: Knowledge graph can be the product OR trigger autonomous investigation — two modes, one governance model
date: 2026-04-05
status: accepted
source: retroactive-extraction
session_date: 2026-04-08
---
# Two Modes of Knowledge Graph Operation

## Context
Brien described a critical distinction: "we learn about things and sometimes the knowledge graph is the product. other times we learn about things, unearth unmet needs or gaps or opportunities and the signals are enough to trigger an autonomous investigation, progression, hypothesis, and experimentation."

## Decision
The system supports both modes through a single governance model:
- **Mode 1 (Knowledge as product):** Brien expresses intent → system executes skill chain → delivers compiled intelligence. The graphs serve Brien.
- **Mode 2 (Knowledge as trigger):** System detects signal → scores risk → acts within autonomy level → brings Brien the finding. The graphs serve themselves, with Brien governing boundaries.

Both modes use the same signal scoring formula, same depth guarantees, same attribution chain. The difference is who initiates (Brien vs. system) and where the human-in-loop checkpoint falls.

## Alternatives Considered
- **Mode 1 only (demand-driven)** — system only acts when Brien asks. Rejected: creates the "primary engagement has thinnest graph" problem where Brien's direct knowledge substitutes for compiled intelligence.
- **Mode 2 only (fully autonomous)** — system investigates everything it notices. Rejected: unbounded budget consumption, noise generation.
- **Two modes, one model (chosen)** — the scoring model governs both. Mode 1 executions score high naturally (Brien's explicit intent = signal strength 1.0). Mode 2 must earn autonomy through the formula.

## Consequences
- The signal detector must run both explicitly (/lint) and implicitly (during context resolution)
- Every autonomous investigation produces an artifact Brien can review — the system never acts without a record
- Precedent accumulates across both modes — a Mode 1 execution builds precedent for Mode 2 autonomy on the same pattern
