---
title: Architecture
type: framework
maturity: final
confidentiality: shareable
reusability: universal
domains:
  - consulting-operations
created: 2026-03-31
depth_score: 4
depth_signals:
  file_size_kb: 6.5
  content_chars: 5664
  entity_count: 0
  slide_count: 0
  sheet_count: 0
  topic_count: 1
  has_summary: 0
vocab_density: 0.35
---
# Intent: Multi-Agent MCP Architecture

## How This Maps to the Loop

The Intent loop — Notice → Spec → Execute → Observe — maps to three
MCP servers and a set of Claude Code subagents. Each server owns one
or more phases. Each subagent connects to the relevant server(s).

```
┌─────────────────────────────────────────────────────────────────┐
│                                                                 │
│   ╔═══════════╗    ╔═══════════╗    ╔═══════════╗              │
│   ║  NOTICE   ║───▶║   SPEC    ║───▶║  OBSERVE  ║              │
│   ║  Server   ║    ║  Server   ║    ║  Server   ║              │
│   ╚═════╤═════╝    ╚═════╤═════╝    ╚═════╤═════╝              │
│         │                │                │                     │
│    Signals          Specs & Contracts    Events                 │
│    Intents          Agent-Readiness     Deltas                  │
│    Trust Scoring    Contract Verify     Health                  │
│    Amplification                       Loop-back signals        │
│    Clustering                                                   │
│    Promotion                                    │               │
│         │                                       │               │
│         ◀───────────────────────────────────────┘               │
│              observe → notice (loop closes)                     │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

## MCP Servers

### intent-notice (Port 8001)
**Phase:** Notice  
**Domain:** Signal lifecycle from capture through promotion to intent  
**Tools:**
- `create_signal` — Capture with trust scoring + autonomy level
- `score_trust` — Rescore trust factors, detect autonomy boundary crossings  
- `cluster_signals` — Group related signals by emergent theme
- `promote_to_intent` — Promote cluster to INT-NNN (problem worth solving)
- `add_reference` — Track signal amplification (7-day half-life decay)
- `dismiss_signal` — Remove from active pipeline
- `list_signals` / `get_signal` — Query with filters
- `get_events` — Read the notice-phase event stream

### intent-spec (Port 8002)
**Phase:** Spec  
**Domain:** Specifications, contracts, agent-readiness assessment  
**Tools:**
- `create_spec` — Generate spec from intent with completeness scoring
- `create_contract` — Define verifiable assertion (interface|behavior|quality|integration)
- `verify_contract` — Record verification result, emit event
- `assess_agent_readiness` — Check if spec meets L3/L4 execution threshold
- `list_specs` / `get_spec` — Query with filters

### intent-observe (Port 8003)
**Phase:** Observe  
**Domain:** Event ingestion, delta detection, loop closure  
**Tools:**
- `ingest_event` — Accept any of the 15 OTel-compatible event types
- `detect_spec_delta` — Compare specified vs actual for a spec
- `detect_trust_drift` — Find signals with shifting effective trust
- `system_health` — Pipeline health across all four phases
- `suggest_signals_from_events` — **Closes the loop**: observe → notice

## Schema Alignment

Every tool input/output aligns to the published Intent schemas:

| Schema    | ID Format  | Storage Path                    | MCP Server    |
|-----------|------------|---------------------------------|---------------|
| Signal    | SIG-NNN    | .intent/signals/YYYY-MM-DD-*.md | intent-notice |
| Intent    | INT-NNN    | .intent/intents/INT-NNN-*.md    | intent-notice |
| Spec      | SPEC-NNN   | spec/SPEC-NNN-*.md              | intent-spec   |
| Contract  | CON-NNN    | spec/contracts/CON-NNN.md       | intent-spec   |
| Event     | (JSONL)    | .intent/events/events.jsonl     | intent-observe|

## Trust & Autonomy

Computed per the Intent trust formula:

```
trust = clarity × 0.30 + (1/blast_radius) × 0.20 + 
        reversibility × 0.20 + testability × 0.20 + precedent × 0.10
```

| Level | Trust Range | Agent Behavior                          |
|-------|-------------|----------------------------------------|
| L0    | < 0.2       | Agent only records. Human drives all.  |
| L1    | 0.2 – 0.4   | Agent suggests. Human decides.         |
| L2    | 0.4 – 0.6   | Agent proposes and awaits approval.    |
| L3    | 0.6 – 0.85  | Agent executes with human monitoring.  |
| L4    | ≥ 0.85      | Full autonomy, circuit breakers only.  |

## Deployment (Free Tier)

| Server         | FastMCP Cloud URL                          | Alt: Cloudflare |
|---------------|--------------------------------------------| --------------- |
| intent-notice | https://intent-notice.fastmcp.cloud/mcp   | Workers         |
| intent-spec   | https://intent-spec.fastmcp.cloud/mcp     | Workers         |
| intent-observe| https://intent-observe.fastmcp.cloud/mcp  | Workers         |

**Total cost: $0/month** on FastMCP Cloud free tier or Cloudflare Workers (100K req/day).

## Phased Rollout

**Phase 1 — Walking Skeleton:** Notice + Spec servers only.  
Capture signals, promote to intents, write specs with contracts.  
Minimum viable loop: signal → intent → spec.

**Phase 2 — Close the Loop:** Add Observe server.  
Event ingestion, delta detection, suggest-signals-from-events.  
Full loop: notice → spec → execute → observe → notice.

**Phase 3 — Agent Teams:** Add Claude Code subagents + coordinator.  
Parallel execution with trust-gated autonomy levels.  
Model mixing: Haiku for capture, Sonnet for spec, Opus for review.

**Phase 4 — Persistence:** Replace in-memory stores with Git-backed storage.  
Each signal/spec/contract writes to .intent/ directory structure.  
Events append to events.jsonl. Full audit trail in git history.
