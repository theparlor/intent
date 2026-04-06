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
  file_size_kb: 1.1
  content_chars: 963
  entity_count: 0
  slide_count: 0
  sheet_count: 0
  topic_count: 1
  has_summary: 0
vocab_density: 1.04
---
# Raw Sources

> Immutable source material. Files placed here are NEVER modified by the LLM. They are read during ingest operations and referenced by wiki artifacts.

## Subdirectories

- `research/` — Interview transcripts, surveys, user research
- `analytics/` — Exported reports, dashboards, usage data
- `competitors/` — Competitor analyses, market research
- `support/` — Ticket exports, session recordings, bug reports

## Rules

1. **Immutability.** Once a file is placed here, its content is frozen. If you need to correct or annotate, create a new file referencing the original.
2. **Naming.** Use descriptive filenames: `YYYY-MM-DD-source-description.md` (e.g., `2026-04-01-user-interview-p14.md`)
3. **Format.** Prefer markdown. Non-markdown files (PDFs, images, CSVs) are acceptable — the LLM will read what it can and note what it can't.
4. **Provenance.** Each file should include a brief header noting its origin (who, when, how collected).
