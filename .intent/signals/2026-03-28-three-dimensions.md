---
id: SIG-005
timestamp: 2026-03-28T14:00:00Z
source: cowork-session
author: brien
confidence: 0.85
trust: 0.6
autonomy_level: L1
status: active
cluster: work-ontology-design
parent_signal:
related_intents: []
---
# Signal: Work can be classified on three independent dimensions: layer, type, scope

## Observation

During ontology sketching, a clean taxonomy emerged:

- **Layer**: code, process, infrastructure
- **Type**: tool-specific, contract-level, workflow-level
- **Scope**: atomic, compound, cross-system

These are orthogonal. A bug fix is *code* layer, *tool-specific* type, *atomic* scope. A refactor might be *code* layer, *contract-level* type, *compound* scope. This gives precise language for describing what broke and where autonomy starts.

## Why It Matters

Without a taxonomy, signals blend together and trust scoring becomes subjective. Clear dimensions let the trust framework ask targeted questions: "Is this a code-layer signal?" → different evidence rules than "Is this a process-layer signal?"

## Trust Factors

- Clarity: Very High — the framework is simple and fits observed work
- Blast radius: Medium — affects how signals are scored and filtered
- Reversibility: High — taxonomy can evolve without breaking existing signals
- Testability: Medium — observable in signal metadata
- Precedent: High — three-axis classification is standard (RACI, risk matrices, etc.)
