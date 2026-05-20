---
title: "File-native, git-tracked, OTel-compatible — no lock-in"
id: DEC-INTENT-004
type: decision-atom
created: 2026-03-28
date_inferred: false
scope: Core/frameworks/intent — storage and observability architecture
status: ratified
ratified_at: 2026-03-28
ratified_by: "brien (Cowork session 2026-03-28; 4-gate pass: reversible / local / precedent / no info gap)"
gate_check:
  reversible: pass
  local: pass
  precedent: pass
  info_gap: pass
upstream_control_path: "Core/frameworks/intent/CLAUDE.md §Key Decisions #4; spec/signal-trust-framework.md; events schema"
catch_mechanism: "All artifacts are markdown + YAML frontmatter + JSONL events — format drift is lint-detectable"
pipeline_survival: "File format is the artifact; survives any tool change"
source: "Cowork session 2026-03-28"
---

# Decision: File-native, git-tracked, OTel-compatible — no lock-in

> Ratified 2026-03-28. All 4 autonomy-grant gates pass.

## Context

Intent needed an artifact storage strategy. SaaS platforms create lock-in and require always-on infrastructure. The methodology should be adoptable by any team without external dependencies.

## Decision

All Intent artifacts are file-native (markdown + YAML frontmatter), git-tracked, and event-compatible with OpenTelemetry conventions. No proprietary formats. No required external services.

## Scope

Governs all `.intent/` artifact formats, event schema, and CLI tool output. Does not constrain hosted-mode extensions (which can layer on top).

## Alternatives Not Taken

| Alternative | Why not chosen | Reversibility if revisited |
|-------------|----------------|---------------------------|
| Database-backed storage | Lock-in; requires always-on service; poor git diff | L2 — migration effort |
| SaaS platform | Vendor dependency; blocks air-gapped adoption | L2 |
| JSON-only (no markdown) | Loses human readability; bad for git review | L4 |

## Reversibility

L4 — format is the artifact. Can add hosted-mode backend without replacing file layer.

## Ratification Action

CLI tools generate markdown + YAML frontmatter. Events emit to `events.jsonl` (OTel-compatible schema). Repo structure mirrors the methodology.
