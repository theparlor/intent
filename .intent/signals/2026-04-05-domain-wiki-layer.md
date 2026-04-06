---
id: SIG-025
timestamp: 2026-04-05T14:30:00Z
source: conversation
confidence: 0.9
trust: 0.7
autonomy_level: L2
status: active
cluster: methodology-adoption
author: brien
related_intents: []
referenced_by: []
parent_signal:
---
# Karpathy's LLM Knowledge Base pattern should become Intent's Layer 1

Andrej Karpathy's April 2, 2026 tweet (25K+ likes) describes using LLMs as knowledge compilers: raw sources → self-organizing markdown wiki → lint/query operations. His system (raw/, wiki/, AGENTS.md schema) maps structurally to Intent across five dimensions: storage mechanism, ingestion/curation, topic-centering, method-vs-content separation, and compounding feedback loops.

**The critical distinction Brien identified:** Karpathy builds a knowledge artifact (output = understanding). Intent builds a generative engine (output = running software). Karpathy's loop terminates at understanding. Intent's loop terminates at deployment.

**The architectural decision:** Absorb Karpathy's pattern as Layer 1 of a three-layer system:
- Layer 1: Domain Knowledge Base (Karpathy pattern adapted for product artifacts — personas, journeys, DDRs, themes)
- Layer 2: Transformation Operating System (Intent's notice→spec→execute→observe loop)
- Layer 3: Software Specification & Code (the generative output)

All three layers are fully bidirectionally coupled through six data flows. Flow 5 (observe → domain knowledge base) enables Argyris double-loop learning — questioning assumptions, not just optimizing execution.

**Grounded in:** Torres (OST), Patton (story mapping), Cagan (product model), Seiden (outcomes), Herbig (impact mapping), Beer (VSM), Argyris (double-loop), Boyd (OODA), Alexander (pattern languages).

**Sources:** reference/karpathy-synthesis/

## Trust Factors

- Clarity: 0.9 — Architecture fully specified with file system, data flows, templates, traceability chain
- Blast radius: 0.4 — Additive (new directories, new schema file), but touches CLAUDE.md, TASKS.md, and future MCP servers
- Reversibility: 0.8 — New directories can be removed, knowledge-engine/AGENTS.md can be deleted, no existing files modified destructively
- Testability: 0.7 — Can be validated by running first ingest against dogfood data
- Precedent: 0.6 — Karpathy's pattern proven at 100 articles / 400K words; Intent's adaptation is novel
