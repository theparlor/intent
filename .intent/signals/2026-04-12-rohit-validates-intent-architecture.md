---
id: SIG-034
title: Rohit's 10 production agent principles validate Intent's three-layer architecture as a production-grade pattern
timestamp: 2026-04-12T01:00:00Z
source: external-article
author: brien
confidence: 0.8
trust: 0.8
autonomy_level: L2
status: resolved
upstream_control_path: "n/a (informational external-validation signal, no build ask)"
catch_mechanism: "no catch-net required; the signal's content is the deliverable and is preserved in this file"
verification_command: "n/a"
cluster: work-ontology-design
referenced_by:
  - "Rohit @rohit4verse, 'How to Build a Production-Grade AI Agent' (Feb 2026), all 10 principles"
  - "Dex Horthy, 12 Factor Agents"
---

# SIG-034: External Validation of Intent as Production Architecture

## What was noticed

Rohit's 10 principles for production-grade AI agents map cleanly onto Intent's four-phase loop:

**Notice phase** ← Principle 1 (threat model), Principle 4 (context engineering), Principle 5 (knowledge grounding)
**Spec phase** ← Principle 2 (contracts everywhere), Principle 6 (orchestration as control flow)
**Execute phase** ← Principle 3 (secure tool execution, RBAC, sandboxing), Principle 8 (reliability mechanics)
**Observe phase** ← Principle 9 (observability with OpenTelemetry), Principle 10 (evaluations, drift, governance)
**Cross-cutting** ← Principle 7 (memory as architecture) maps to the Knowledge Engine layer

This is the second independent validation of Intent's architecture (the first being Dex Horthy's 12 Factor Agents and harness engineering). Two practitioners from different domains (Rohit from enterprise agent deployment, Dex from infrastructure/context engineering) arrive at patterns that map onto the same loop.

## Evidence

Specific mappings:
- Rohit's "state machine orchestration for business-critical flows" = Intent's Notice→Spec→Execute→Observe loop
- Rohit's "OTel semantic conventions with trace/span hierarchy" = Intent's event system (Intent=Trace, Spec=Span, Contract=Leaf Span)
- Rohit's "human-in-the-loop approval registry" = Intent's L0-L4 trust/autonomy levels
- Rohit's "10:1 compression ratio for context" = Intent's Knowledge Engine compilation-over-retrieval principle
- Rohit's "circuit breakers to terminate runaway loops" = Intent's disambiguation signal pattern (generate a signal asking a better question rather than dead-ending)

## Implication

Intent is not just a team methodology — it's a production architecture pattern that independent practitioners are converging on. This strengthens the case for the Intent site's "The Build" pillar and the technical credibility of the framework. Consider adding Rohit's mapping as a reference in the Intent site's architecture page.

## Triage, 2026-07-08

Disposition: control exists now, informational, no control required. This signal is pure external validation (Rohit's 10 principles mapping onto Intent's four-phase loop); it does not itself request new construction, only suggests "consider adding Rohit's mapping as a reference on the Intent site's architecture page." That specific suggestion was not actioned, but nothing is broken or missing as a result, the signal's substantive content (the mapping itself) is preserved in this file regardless of whether it is cross-posted to the site. Same treatment as batch 1's RETRO-2026-04-12-batch-sweep-SIG-5 (point-in-time validation snapshot, nothing to fix).
