---
id: SIG-KE-CLI-IDD-TRIGGER-2026-05-20
title: IDD trigger — bin/intent-knowledge CLI implementation (SPEC-001, 44 days since spec)
type: signal
status: resolved
upstream_control_path: "bin/intent-knowledge (ingest, query, lint subcommands)"
catch_mechanism: "shared find_intent_root() + emit_event() wiring matches the other three Intent CLI tools; event emission on every subcommand invocation"
verification_command: 'grep -n "cmd_ingest\|cmd_query\|cmd_lint\|emit_event" /Users/brien/Workspaces/Core/frameworks/intent/bin/intent-knowledge'
confidence: 0.90
trust: 0.85
autonomy_level: L4
source: framework-self-audit-2026-05-20
date: '2026-05-20'
upstream_control_path: SIG-KE-CLI-IDD-TRIGGER-2026-05-20.md (this file) — triggers a dedicated IDD Execute loop for bin/intent-knowledge; the IDD loop is the upstream control
catch_mechanism: IDD loop will have its own DoR + DoD gates that prevent incomplete implementation from being declared resolved
pipeline_survival: git-tracked; overwatch sweeps will surface this as active Notice until Execute loop closes it
---

# IDD Trigger: bin/intent-knowledge CLI

## What Was Noticed

`bin/intent-knowledge` (the Knowledge Engine CLI with `ingest`, `query`, `lint` subcommands) was specced in SPEC-001 on 2026-04-06. As of 2026-05-20, the `bin/` directory contains only the four main Intent CLI tools (`intent-signal`, `intent-intent`, `intent-spec`, `intent-status`). The `intent-knowledge` binary does not exist.

Gap age: **44 days** since spec was written with no corresponding implementation.

## Why It Matters

Without `bin/intent-knowledge`:
- Flow 1 (lint → Notice signals) is unexecutable
- Flow 2 (spec authoring queries knowledge base) is manual
- Flow 5 (Observe → Knowledge updates) cannot be invoked via CLI
- The Knowledge Engine as a standalone product is unusable from the terminal

This is not a signal about whether to build it — SPEC-001 is ratified. This is a Notice that the Execute loop has not opened, and no IDD trigger existed before this signal.

## IDD Loop Spec

**Notice:** This signal.
**Intent:** `bin/intent-knowledge` operational with `ingest`, `query`, `lint` subcommands.
**Spec:** SPEC-001 (`knowledge-engine/spec/` — KE operations, federation, enrichment, redaction, boundary). Read before writing code.
**DoR gates before Execute:**
- [ ] SPEC-001 re-read in full (it may have drifted since April)
- [ ] `knowledge-engine/AGENTS.md` re-read (schema constraints)
- [ ] `bin/lib/id_gen.sh` reviewed (ULID generation for artifact IDs)
- [ ] DoD written and approved

**DoD gates (proposed):**
- [ ] `ingest`: drop file in `raw/` → compiles to knowledge artifact in `knowledge/` → appends to `_index.md` + `log.md` → emits event
- [ ] `query`: takes question arg → reads `_index.md` → synthesizes answer with `[[citations]]` → optional `--file` to save as knowledge artifact
- [ ] `lint`: checks for contradictions, orphans, stale claims, missing cross-refs → outputs signal-ready findings
- [ ] All three subcommands share `find_intent_root()` and ULID-based ID generation
- [ ] Tests against Intent's own `knowledge/` directory (dogfood)
- [ ] Event emission to `events.jsonl` per subcommand operation

## Do Not Implement Inline

This signal is a Notice, not an Execute authorization. The Execute loop requires its own spec review, DoR confirmation, and DoD. Open a dedicated IDD session using `spawn-prompts/idd-build-execute.md` with this signal as the Notice source.

## Triage, 2026-07-08

Disposition: control exists now, verified live. bin/intent-knowledge exists (478 lines) with exactly the three subcommands this signal's DoD specified: ingest, query, lint. It shares find_intent_root() with the other CLI tools, emits events to events.jsonl via emit_event() (knowledge.ingested, knowledge.queried, knowledge.linted, confirmed by grep), and the ingest path documents a dossier subtype in addition to the base research/raw ingest path. The gap this signal named, "the Knowledge Engine as a standalone product is unusable from the terminal," is closed.
