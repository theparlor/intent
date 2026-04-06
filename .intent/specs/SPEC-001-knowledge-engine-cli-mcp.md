---
id: SPEC-001
title: "Knowledge Engine CLI + MCP Server: ingest, query, lint operations"
version: "1.0"
status: draft
intent: INT-003
trust_score: 0.72
autonomy_level: L3
shaped_by: [architect, product, quality, agent]
personas_queried: [PER-001, PER-002]
decisions_referenced: [DDR-001, DDR-002, DDR-005]
contracts: [CON-KE-001, CON-KE-002, CON-KE-003, CON-KE-004, CON-KE-005, CON-KE-008, CON-KE-009]
created: 2026-04-06
---
# SPEC-001: Knowledge Engine CLI + MCP Server

---

## Intent (Pass 2: ◇ Product Leader)

**Why this matters:** Brien's Knowledge Farm has a complete schema and 16 manually-compiled artifacts, but no executable operations. He can't drop a source into `raw/` and have the system compile it. Every ingest requires a full session with an agent manually writing files. The Knowledge Engine's value proposition — compiled knowledge that compounds — requires operational tooling.

**What outcome:** Brien drops a markdown file into `raw/`, runs a command, and the knowledge base self-organizes. He asks a question and gets a cited answer drawn from compiled knowledge. He runs lint and gets actionable signals about gaps and contradictions. This works against Intent's own dogfood AND against engagement Knowledge Farms (Subaru first).

**Who benefits:**
- [[PER-001-practitioner-architect]] — Brien himself, using the Knowledge Farm to compile consulting domain knowledge
- [[PER-002-solo-knowledge-worker]] — Any practitioner adopting the Karpathy compilation pattern

**Behavioral change (Seiden):** Brien shifts from "manually authoring knowledge artifacts in sessions" to "curating sources and reviewing compiled output." The bottleneck moves from authoring to curation.

---

## Shape (Pass 1: △ Architect)

### Technical Approach

Two interfaces to the same operations, following Intent's existing dual-interface pattern:

**CLI Tool: `bin/intent-knowledge`**
- Bash script following `intent-signal` pattern
- `find_intent_root()` to locate `.intent/` (and from there, `knowledge/` and `raw/`)
- Sequential ID generation for new artifacts
- Event emission to `events.jsonl`
- Subcommands: `ingest`, `query`, `lint`, `status`

**MCP Server: `servers/knowledge.py`**
- FastMCP server on port 8004, following `notice.py` pattern
- Tools: `knowledge_ingest`, `knowledge_query`, `knowledge_lint`, `knowledge_status`
- File-backed (reads/writes `knowledge/` directly), not in-memory
- Separate from intent-notice/spec/observe (DDR-005: Knowledge Engine is separable)

### Boundaries

**In scope:**
- `ingest`: read source from `raw/`, read `knowledge/_index.md`, create/update knowledge artifacts, update cross-refs, update index, append log
- `query`: read index, read relevant artifacts, synthesize cited answer, offer to file as new artifact
- `lint`: scan all artifacts for contradictions, orphans, staleness, coverage gaps, provenance drift; output as suggested signals
- `status`: summary of knowledge base state (artifact counts, avg confidence, last ingest, coverage gaps)

**Out of scope for SPEC-001:**
- Federation (engagement-specific AGENTS.md inheritance) — deferred to SPEC-002
- Retroactive enrichment cascade — deferred to SPEC-003
- Redaction projections — deferred to SPEC-004
- Obsidian bridge / graph visualization — deferred
- Non-markdown source handling (PDFs, images, CSVs) — deferred; log a warning and skip

### Key Decisions Already Made (DDRs)

| Decision | Reference | Implication |
|----------|-----------|-------------|
| Compilation over RAG | DDR-001 | No vector store. Navigate via `_index.md` and summaries. |
| Three-layer architecture | DDR-002 | Knowledge Engine is Layer 1. Independent of but coupled to the loop. |
| Knowledge Engine is separable | DDR-005 | Own MCP server (port 8004), own CLI tool. Not bolted onto intent-notice. |
| New MCP server | Key Decision #16 | `intent-knowledge` on port 8004. |
| New CLI tool | Key Decision #16 | `bin/intent-knowledge` with subcommands. |

### Decisions for the Agent

The agent MAY make these implementation decisions within the boundaries above:
- Internal helper function structure in the CLI script
- MCP tool parameter naming (follow existing convention from notice.py)
- How to detect "new vs existing" artifacts during ingest (match by slug? by ID? by content similarity?)
- Log message formatting within the `[INGEST]`/`[QUERY]`/`[LINT]` prefix convention

### File Layout

```
bin/intent-knowledge              # CLI tool (new)
servers/knowledge.py              # MCP server (new)
servers/models.py                 # Add KnowledgeArtifactType enum, knowledge event types (modify)
```

---

## Contract (Pass 3: ○ Quality Advocate)

### Acceptance Criteria

Each criterion maps to a Knowledge Engine contract:

**AC-1: Ingest produces artifacts (CON-KE-001)**
```
Given: a markdown file exists in raw/research/
When: `intent-knowledge ingest raw/research/file.md` is run
Then: at least one new .md file appears in knowledge/
  AND knowledge/_index.md is updated with the new artifact
  AND knowledge/log.md has a new [INGEST] entry
  AND .intent/events/events.jsonl has a knowledge.ingested event
```

**AC-2: All artifacts have valid frontmatter (CON-KE-002)**
```
Given: ingest has been run
When: any knowledge artifact is inspected
Then: it has YAML frontmatter with: id, type, confidence, origin, created, updated
  AND confidence is between 0.0 and 1.0
  AND origin is one of: human, agent, synthetic
```

**AC-3: Cross-references resolve (CON-KE-003)**
```
Given: ingest has created artifacts with [[wikilinks]]
When: all wikilinks are extracted and checked
Then: every wikilink target has a corresponding .md file in knowledge/
```

**AC-4: Index reflects state (CON-KE-004)**
```
Given: ingest has run
When: knowledge/_index.md artifact_count is compared to actual file count
Then: they match
```

**AC-5: Query returns cited answer**
```
Given: knowledge base has been populated by ingest
When: `intent-knowledge query "what personas exist?"` is run
Then: the response references specific knowledge artifacts by ID
  AND includes [[wikilinks]] or file paths to sources
```

**AC-6: Lint produces actionable findings**
```
Given: knowledge base has been populated
When: `intent-knowledge lint` is run
Then: output lists findings by category (contradictions, orphans, stale, gaps, provenance)
  AND each finding identifies the specific artifact(s) involved
  AND findings can be piped to signal creation
```

**AC-7: CLI follows existing pattern**
```
Given: intent-knowledge CLI is installed in bin/
When: run with no arguments
Then: shows usage help consistent with intent-signal pattern
  AND finds .intent/ by walking up from $PWD
  AND emits events to .intent/events/events.jsonl
```

**AC-8: MCP server is functional**
```
Given: servers/knowledge.py exists
When: `fastmcp run servers/knowledge.py` is started
Then: server starts on port 8004
  AND knowledge_ingest, knowledge_query, knowledge_lint, knowledge_status tools are available
  AND tools read/write knowledge/ directory (file-backed, not in-memory)
```

### Failure Modes

| Failure | Impact | Mitigation |
|---------|--------|-----------|
| Ingest creates duplicate artifacts for same source | Knowledge base bloated, confidence inflated | Match by source path in frontmatter before creating |
| Wikilinks point to non-existent artifacts | Broken navigation, lint false positives | Validate links during ingest before writing |
| Index drifts from actual state | Stale navigation, wrong artifact counts | Regenerate index from directory scan, not incremental updates |
| Log.md edited instead of appended | Audit trail broken | Append-only enforcement in the write function |

---

## Agent Notes (Pass 4: ◉ Agent Readiness Assessment)

### Trust Score Breakdown

| Factor | Score | Rationale |
|--------|-------|-----------|
| Clarity | 0.85 | Spec is detailed. Acceptance criteria are testable. Boundaries clear. |
| Blast radius | 0.4 | Creates new files (bin/, servers/), modifies models.py. Medium. |
| Reversibility | 0.8 | New files can be deleted. models.py changes are additive. |
| Testability | 0.8 | 8 acceptance criteria, all verifiable via CLI/file inspection. |
| Precedent | 0.7 | Follows exact patterns from intent-signal CLI and notice.py server. |
| **Computed trust** | **0.72** | **L3: Agent executes, human monitors** |

### Required Reads Before Execution

1. `bin/intent-signal` — Full CLI pattern (done, read above)
2. `servers/notice.py` — Full MCP server pattern (done, read above)
3. `servers/models.py` — Shared models, enums, event types (done, read above)
4. `knowledge-engine/AGENTS.md` — Schema, artifact types, operations (done, loaded)
5. `knowledge-engine/spec/operations.md` — Ingest/query/lint process (done, loaded)
6. `knowledge-engine/spec/contracts.md` — Contracts to satisfy (done, loaded)

### Ambiguity Flags

| Flag | Resolution | Status |
|------|-----------|--------|
| How to detect duplicate artifacts during ingest | Match by `sources:` field in frontmatter — if source path already listed, update instead of create | **Resolved in spec** |
| Should query be interactive (offer to file) or output-only | CLI: output-only with `--file` flag to create artifact. MCP: return answer with `should_file: true/false` suggestion. | **Resolved in spec** |
| How to handle non-markdown raw sources | Log warning, skip. Note in output. Defer to SPEC-002+. | **Resolved in spec** |
| Event types for knowledge operations | Add to models.py: `knowledge.ingested`, `knowledge.queried`, `knowledge.linted` | **Resolved in spec** |

### Recommended Execution Approach

1. **Start with models.py** — add KnowledgeArtifactType enum and 3 event types
2. **Build CLI first** (`bin/intent-knowledge`) — easier to test, follows proven pattern
3. **Test CLI against Intent's own knowledge base** — validate AC-1 through AC-7
4. **Build MCP server** (`servers/knowledge.py`) — same operations, different interface
5. **Test MCP server** — validate AC-8

### Events to Emit

| Event | When |
|-------|------|
| `knowledge.ingested` | After successful ingest (data: source path, artifacts created/updated) |
| `knowledge.queried` | After query (data: question, artifacts referenced) |
| `knowledge.linted` | After lint (data: findings count by category) |
