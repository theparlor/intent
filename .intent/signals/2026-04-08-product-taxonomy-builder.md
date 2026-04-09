---
title: "Digital Product Taxonomy Builder — KE capability"
severity: medium
detected: 2026-04-08
status: active
source: brainstorming session — persona browser + product dashboard design
---

## Observation

While building the "Products Built with Intent" dashboard tab, we manually scanned and curated the product taxonomy for The Parlor's portfolio. This produced a `products-taxonomy.yaml` with product lines, products, capabilities, composability flows, and a GTM product (Knowledge Farm).

The process was: scan existing artifacts → identify product boundaries → classify type (domain/platform/standalone/GTM) → map provides/consumes relationships → formalize as data.

This is a Knowledge Engine capability — Research + Infer + Assess applied to a product landscape.

## Opportunity

Build a KE capability that automates product taxonomy scanning:
- **Input:** A codebase, documentation set, or organizational artifact collection
- **Output:** A `products-taxonomy.yaml` with product lines, products, types, status, provides/consumes flows
- **Value:** Any consulting engagement could produce a product taxonomy as a deliverable. Clients with sprawling product portfolios need this clarity.

## Implication

This connects to the Knowledge Farm GTM concept — a product taxonomy is one of the artifacts that lives in a client's Knowledge Farm instance.
