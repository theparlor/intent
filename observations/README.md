---
title: Readme
type: framework
maturity: final
confidentiality: shareable
reusability: universal
domains:
  - consulting-operations
created: 2026-04-06
depth_score: 2
depth_signals:
  file_size_kb: 1.2
  content_chars: 878
  entity_count: 0
  slide_count: 0
  sheet_count: 0
  topic_count: 1
  has_summary: 0
vocab_density: 1.14
---
# Observations

> Runtime feedback from executed specs. This directory captures what actually happened when code ran, users interacted, and systems behaved — the empirical evidence that feeds back into both the compiled knowledge base (Flow 5, double-loop) and the spec corpus (Flow 6, single-loop).

## Subdirectories

- `metrics/` — Performance data, usage analytics, behavioral measurements
- `incidents/` — Error reports, anomalies, unexpected behaviors

## Rules

1. **Structured.** Each observation file uses YAML frontmatter with `observed_at`, `source`, `related_specs`, `related_knowledge_artifacts`.
2. **Linked.** Every observation must reference the spec(s) it validates or contradicts.
3. **Actionable.** Observations that contradict domain knowledge base assumptions trigger Flow 5 updates. Observations that confirm or refine specs trigger Flow 6 updates.
