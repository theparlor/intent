---
title: Traceability Matrix
type: traceability
depth_score: 2
depth_signals:
  file_size_kb: 2.3
  content_chars: 2039
  entity_count: 0
  slide_count: 0
  sheet_count: 0
  topic_count: 0
  has_summary: 0
vocab_density: 0.49
maintained_by: agent
last_compiled: 2026-04-05
---
# Traceability Matrix

> Cross-artifact link matrix. Every row traces from raw source material through compiled domain artifacts to specifications and code. Maintained automatically during ingest and lint operations.

## Chain Format

```
Raw Source → Persona → Journey Step → Pain Point → DDR → Spec → Contract → Code
```

## Active Chains

> **Note:** Engagement-scoped chains (Subaru) live in Work/Consulting/Engagements/Subaru/knowledge/. Core chains trace methodology only.

### Chain 1: Specification Quality Problem

```
raw/research/2026-03-28-intent-methodology-v1.md
  → PER-001-practitioner-architect (PP-002: specs too ambiguous for agents)
  → JRN-001-adopt-intent#notice-the-gap
  → DDR-002-three-layer-architecture
  → (no spec yet)
```

### Chain 2: Domain Knowledge Compilation

```
raw/research/2026-04-02-karpathy-llm-knowledge-bases.md
raw/research/2026-04-05-three-layer-architecture-formalized.md
  → PER-001-practitioner-architect (PP-003: no systematic way to compile domain knowledge)
  → PER-002-solo-knowledge-worker (PP-002: RAG re-derives, doesn't compile)
  → JRN-001-adopt-intent#compile-understanding
  → JRN-002-build-knowledge-base#build-critical-mass
  → DDR-001-compilation-over-rag
  → (no spec yet)
```

### Chain 3: Feedback Loop Closure

```
raw/research/2026-04-05-three-layer-architecture-formalized.md
  → PER-001-practitioner-architect (PP-004: observations don't feed back to domain understanding)
  → JRN-001-adopt-intent#observe-learn
  → DDR-003-bidirectional-coupling
  → (no spec yet — requires Flow 5 implementation)
```

## Coverage Gaps

| Gap | Severity | Action |
|-----|----------|--------|
| No specs linked to any DDR yet | Medium | DDRs are accepted but no specs have been written against them |
| No observations directory populated | Expected | System is pre-deployment; observations will come when code runs |
| PER-002 has no pain point addressed by a DDR for PP-003 (no packaged product) | Low | This is Intent's GTM problem, not a knowledge base gap |
| JRN-001 Stage: Scaffold has no DDR | Low | Scaffold experience is underspecified; needs user research |

---

_Last compiled: 2026-04-05_
