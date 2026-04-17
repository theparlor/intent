---
title: Knowledge Engine MCP Query Write-Back Architecture
id: DDR-007
type: decision
created: 2026-04-13
updated: 2026-04-13
status: accepted
confidence: 0.85
origin: agent
persona: PER-001
journey_stage: JRN-001#compile-understanding
sources:
  - raw/research/2026-04-12-rvk7895-llm-knowledge-bases.md
  - raw/research/2026-04-12-rotifer-compile-dont-search-agent-memory.md
  - raw/research/2026-04-12-karpathy-gist-llm-wiki.md
related_decisions:
  - DDR-001
  - DDR-005
related_signals:
  - SIG-033
---
# DDR: Knowledge Engine MCP Query Write-Back Architecture

## Context

Three independent sources converge on the same finding: a knowledge system that only reads and never writes back from queries is "archival," not "evolutionary."

- **rvk7895** implements auto-evolve: after every query, a background opus subagent fires silently, creating/updating wiki articles when the answer contained new knowledge. Constraints: no deleting, no stubs under 100 words, must re-read before modifying.
- **Rotifer Protocol** frames query-as-contribution as a "fundamental architectural property, not a UX convenience. Reading and writing are the same operation."
- **Karpathy** (gist): "good answers can be filed back into the wiki as new pages... your explorations and queries always 'add up' in the knowledge base."

The intent-knowledge MCP server (port 8004, DDR-005 Key Decision 16) currently specifies three operations: ingest, query, lint. The query operation has no write pathway. This is a design-time decision — retrofitting write-back after the MCP tool surface is established is expensive.

## Decision

**Query write-back is a first-class operation in the intent-knowledge MCP, implemented as conditional auto-enrichment with confidence gating.**

The architecture:

### 1. Query Tool Returns Structured Response
The `intent_knowledge_query` MCP tool returns:
```yaml
answer: "synthesized response"
sources: [list of artifacts consulted]
novel_knowledge: true|false  # did the answer synthesize beyond what's in the KB?
enrichment_candidates:
  - artifact: "THM-003"
    action: "append"
    content_summary: "window argument from Power essay"
    confidence: 0.8
```

### 2. Enrichment Executes Conditionally
- If `novel_knowledge: false` → no write-back (query was fully answered from existing artifacts)
- If `novel_knowledge: true` AND enrichment confidence ≥ 0.7 → auto-enrich (L3 autonomy, agent executes)
- If `novel_knowledge: true` AND enrichment confidence < 0.7 → suggest enrichment as a signal (L1 autonomy, human reviews)

### 3. Constraints on Auto-Enrichment
Following rvk7895's validated pattern:
- Never delete existing content
- Never create stub artifacts under 100 words
- Must read the target artifact before modifying (prevents blind appends)
- Append-only to existing artifacts preferred over creating new ones
- Every enrichment logged to `knowledge/log.md` with `[ENRICH]` prefix
- Every enrichment emits an `intent.knowledge.enriched` event to `events.jsonl`

### 4. MCP Tool Surface
The intent-knowledge MCP exposes 5 tools (expanded from 3):

| Tool | Operation | Write? |
|---|---|---|
| `intent_knowledge_ingest` | Process raw source into KB | Yes |
| `intent_knowledge_query` | Query with optional auto-enrichment | Conditional |
| `intent_knowledge_lint` | Health check / structural integrity | Read-only |
| `intent_knowledge_enrich` | Explicit enrichment (file answer back) | Yes |
| `intent_knowledge_status` | KB stats, coverage, freshness | Read-only |

The `enrich` tool is the explicit version of what `query` does conditionally — for cases where Brien or an agent wants to file a specific answer back into the KB.

## Alternatives Considered

1. **Always write-back (rvk7895 pattern verbatim).** Rejected — rvk7895 operates in a personal vault where contamination risk is low. Intent's federated KB has engagement-scoped artifacts where auto-write could leak cross-engagement knowledge. Confidence gating is the safety mechanism.

2. **Never write-back (query is read-only).** Rejected — this is the "archival" pattern three independent sources identify as incomplete. The KB stops compounding from use.

3. **Write-back as separate manual step only.** Partially adopted — the explicit `enrich` tool exists for this. But requiring manual enrichment for every valuable query answer introduces the same maintenance burden Karpathy identified as the problem LLMs solve.

## Consequences

**Positive:**
- KB becomes evolutionary — grows from use, not just from explicit ingestion
- Closes the compile loop: raw→compile→query→enrich→compile (Karpathy's full cycle)
- Confidence gating prevents low-quality auto-enrichment
- Event emission enables overwatch to monitor enrichment quality over time

**Negative:**
- Adds complexity to the query tool (must assess novelty, compute enrichment candidates)
- Risk of enrichment loops (query triggers enrich, enriched content changes future query answers)
- Federation boundary enforcement needed — auto-enrichment must respect engagement scoping (never write Subaru knowledge into Core from a query about ASA)

**Mitigations:**
- Circuit breaker: max 3 auto-enrichments per query session (prevents runaway loops)
- Federation check: enrichment target must match query context scope
- Enrichment log enables retrospective audit

## Validation Criteria

- [ ] A query that synthesizes across 2+ KB artifacts and discovers a new connection auto-files the connection
- [ ] A query answered entirely from existing artifacts does NOT trigger enrichment
- [ ] Auto-enrichment respects federation boundaries (engagement-scoped queries don't enrich Core)
- [ ] Enrichment log entries are parseable and auditable
- [ ] Overwatch can detect enrichment quality degradation over time
