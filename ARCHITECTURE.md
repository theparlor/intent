---
title: Architecture
type: framework
maturity: final
confidentiality: shareable
reusability: universal
domains:
  - consulting-operations
created: 2026-04-02
updated: 2026-05-20
depth_score: 4
depth_signals:
  file_size_kb: 17.7
  content_chars: 16972
  entity_count: 0
  slide_count: 0
  sheet_count: 0
  topic_count: 1
  has_summary: 0
vocab_density: 0.18
version: 0.11.0
---
# Intent: Architecture — v0.11.0

## Three-Layer Model

Intent prescribes three layers that work together. Each layer is independently useful; they compose bidirectionally.

| Layer | Purpose | Primary Directories |
|---|---|---|
| **1. Compiled Knowledge Base** | Everything the system knows about the problem domain — compiled once, kept current | `raw/`, `knowledge/` |
| **2. Transformation OS** | The Notice→Spec→Execute→Observe engine. Domain-agnostic. | `.intent/`, `spec/` |
| **3. Software Spec & Code** | Specs, contracts, and running code produced by the loop | `spec/` (generated), `src/` |

**Six bidirectional data flows couple the layers:**
1. Knowledge → Notice: lint surfaces signals (gaps, contradictions, staleness)
2. Notice → Spec (via knowledge): spec authoring queries knowledge base for personas, journeys, DDRs
3. Spec → Execute: trust-gated agents build against specs
4. Execute → Observe: running code emits events
5. **Observe → Knowledge (double-loop):** observations update domain models — questioning assumptions, not just optimizing
6. Observe → Spec corpus (single-loop): spec drift detection, living doc sync

---

## How the Loop Maps to Infrastructure

The Intent loop — Notice → Spec → Execute → Observe — maps to three MCP servers and a set of Claude Code subagents. Each server owns one or more phases.

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

---

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
- `ingest_event` — Accept any of the 26 OTel-compatible event types
- `detect_spec_delta` — Compare specified vs actual for a spec
- `detect_trust_drift` — Find signals with shifting effective trust
- `system_health` — Pipeline health across all four phases
- `suggest_signals_from_events` — **Closes the loop**: observe → notice

### intent-knowledge (Port 8004)
**Phase:** Cross-cutting (Layer 1)
**Domain:** Knowledge base ingestion, query, and lint — extended 2026-05-26 to include cross-surface substrate exposure (DEC-010)
**Tools:** `ingest`, `query`, `lint` (existing per SPEC-001 / DDR-005) + `get`, `list`, `lineage`, `freshness` (substrate-exposure read verbs per DEC-010)
**Note:** Specced; CLI implementation in `bin/intent-knowledge` pending. See Gap 7.1 / track E3 in `.intent/specs/2026-05-20-upgrade-plan.md`. Substrate exposure verbs land per `spec/substrate-exposure-architecture.md` (WS-DDR-099 + DEC-010, 2026-05-26).

---

## CLI Suite (Stable Surface)

The `tools/intent-mcp/server.py` provides **6 tools** consumed by Claude Code, Cowork, and Cursor:

| Tool | Action | Read-only |
|------|--------|-----------|
| `intent_capture_signal` | Capture a signal | No |
| `intent_list_signals` | List recent signals | Yes |
| `intent_get_signal` | Get signal details | Yes |
| `intent_propose_intent` | Propose an intent | No |
| `intent_create_spec` | Create a spec | No |
| `intent_status` | System status overview | Yes |

The `servers/` directory contains a parallel FastMCP-based implementation of all four servers. Migration path from legacy `tools/intent-mcp/server.py` to `servers/` is unspecified; both are currently maintained. See `.intent/specs/2026-05-20-upgrade-plan.md` Gap 11.1.

---

## Schema Alignment

Every tool input/output aligns to the published Intent schemas:

| Schema    | ID Format  | Storage Path                    | MCP Server    |
|-----------|------------|---------------------------------|---------------|
| Signal    | SIG-NNN    | .intent/signals/YYYY-MM-DD-*.md | intent-notice |
| Intent    | INT-NNN    | .intent/intents/INT-NNN-*.md    | intent-notice |
| Spec      | SPEC-NNN   | spec/SPEC-NNN-*.md              | intent-spec   |
| Contract  | CON-NNN    | spec/contracts/CON-NNN.md       | intent-spec   |
| Event     | (JSONL)    | .intent/events/events.jsonl     | intent-observe|

**ID generation:** All new entity IDs use ULID (Crockford base32) via `bin/lib/id_gen.sh`. Legacy `SIG-NNN` sequential IDs remain valid. See SPEC-003.

---

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

---

## 5-Layer Closure-Discipline Enforcement

Every resolved signal or task must carry three triad keys before claiming `status: resolved`. The 5-layer enforcement architecture catches drift at every phase:

| Layer | Mechanism | Hook |
|---|---|---|
| 1. Spec | `spec/closure-discipline-enforcement.md` — policy definition | — |
| 2. SessionStart | Injects closure posture before first response | `closure-discipline-check.sh` |
| 3. Memory | `feedback_closure_discipline.md` + `reference_signal_closure_policy.md` | — |
| 4. Stop hook | Scans response text for completion claims without upstream-control mention | `closure-discipline-stop-check.sh` |
| 5. PreToolUse | Blocks signal-file writes with `status: resolved` missing triad keys | `closure-discipline-signal-check.sh` |

**Triad keys required for `status: resolved`:**
- `upstream_control_path:` — what governs this domain going forward
- `catch_mechanism:` — what fires if the pattern regresses
- `pipeline_survival:` — what makes this survive across builds and sessions

**Process Drift Catalog:** `learnings/process-drift-catalog.md` — canonical catalog covering Family 2 closure drifts (2.1 resolved-without-triad, 2.2 symptom-patch, 2.3 table-form, 2.4 complete-at-mechanical-step).

---

## 5-Layer Autonomy-Grant Enforcement

Prevents conversion of L4-eligible work into L0 proposals. Parallel architecture to closure-discipline enforcement.

| Layer | Mechanism | Hook |
|---|---|---|
| 1. Spec | `spec/autonomy-grant-enforcement.md` — policy definition | — |
| 2. SessionStart | Injects autonomy posture anchor before first response | `autonomy-grant-check.sh` |
| 3. Memory | `feedback_autonomy_grant_drift_pattern.md` + CLAUDE.md behavioral rules | — |
| 4. Stop hook | Scans response endings for bare-choice and soft-queue patterns | `autonomy-grant-stop-check.sh` |
| 5. Dispatch-prompt pre-flight | Scans Agent/spawn_task dispatch prompts for proposal-framing injection | `autonomy-grant-dispatch-prompt-check.sh` |

**Override token:** `# AUTONOMY-OVERRIDE-PROPOSAL-FRAMING-INTENTIONAL: <justification>` in dispatch prompt suppresses Layer 5 for genuine L0 items.

**Process Drift Catalog:** Family 1 entries (1.1–1.7) cover autonomy drifts including the new `1.7 — Artificial-gate-architecture drift` (inventing L0 sign-offs at design time rather than response time).

---

## Hook Infrastructure (8 Governance Hooks)

All hooks live in `hooks/`. Registered in `~/.claude/settings.json`.

| Hook | Trigger | Purpose |
|---|---|---|
| `autonomy-grant-check.sh` | SessionStart | Autonomy posture banner |
| `autonomy-grant-stop-check.sh` | Stop | Bare-choice + soft-queue detection |
| `autonomy-grant-dispatch-prompt-check.sh` | PreToolUse (Agent/spawn_task) | Proposal-framing injection block |
| `closure-discipline-check.sh` | SessionStart | Closure posture banner |
| `closure-discipline-stop-check.sh` | Stop | Completion-claim detection + table-cell scanner |
| `closure-discipline-signal-check.sh` | PreToolUse (Write/Edit) | Resolved-without-triad block |
| `overwatch-staleness-check.sh` | SessionStart | Overwatch journal staleness banner (>7d warn, >14d load-bearing) |
| `spec-age-lint.sh` | Configurable | Approved/ratified specs with no corresponding implementation after N days |

`install.sh` — registers all hooks into `~/.claude/settings.json`.

---

## Spawn-Prompts Library (8 Prompts)

Reusable handoff prompts for common governance and build operations. All live in `spawn-prompts/`.

| Prompt | Purpose |
|---|---|
| `autonomy-grant-correction.md` | Corrective posture restoration when drift accumulates |
| `closure-discipline-audit.md` | Full audit for closure-discipline debt across a product |
| `cowork-idd-with-panel-critique.md` | Cowork-targeted IDD execution + panel critique integration |
| `framework-self-audit.md` | Targeted Intent-framework-only audit (lighter than overnight) |
| `idd-audit-product.md` | Product-level IDD compliance audit |
| `idd-build-execute.md` | IDD build execution from a ratified spec |
| `overnight-exhaustive-upgrade.md` | Multi-phase overnight orchestrator; runs exhaustive audits across full Workspaces topology |
| `process-drift-audit.md` | Drift pattern audit against the catalog |

---

## IDD Build Discipline

Intent prescribes IDD (Intent-Driven Development) as the build pattern for all non-trivial work. Canonical playbook: `learnings/idd-playbook.md`.

**7-stage loop:** Notice → DoR gate → Spec → DoD gate → Execute → Observe → DoR gate (next loop)

Key posture rules:
- DoR gate: spec must carry `assess_agent_readiness` L3+ score before Execute starts
- DoD gate: Observe stage must verify outcomes against contracts before closing
- Signal-zero is not evidence of correctness — verify the mechanism, not the count

Cross-product applicability: `learnings/idd-cross-product-applicability.md` maps IDD across Cast, Forge, Voices, Loom, Topography, Throughline, and Fieldbook.

---

## Process Drift Catalog

`learnings/process-drift-catalog.md` — 4 families, 17 entries as of v0.11.0.

| Family | Entries | Hooked |
|---|---|---|
| 1. Autonomy-Grant Drifts | 1.1–1.7 | Yes (Layers 1, 4, 5) |
| 2. Closure-Discipline Drifts | 2.1–2.4 | Yes (Layers 1, 4, 5) |
| 3. Honesty/Over-Claim Drifts | 3.1–3.5 | No (catalog + memory) |
| 4. Process/Coordination Drifts | 4.1–4.7 | Partial (4.7 hooked via overwatch-staleness-check.sh) |

**v0.11.0 additions:**
- `1.7 — Artificial-gate-architecture drift`: inventing L0 sign-offs at design time for algorithmically-verifiable work
- `4.7 — Governance-skill-without-trigger`: periodic governance operations with no hook, no scheduled task, no staleness alarm — caught by `overwatch-staleness-check.sh`

---

## State Philosophy

Intent is a **stateful system composed of stateless agent invocations.** This resolves the apparent tension between Intent's distributed state model and the stateless-reducer pattern common in agent architectures.

### The Resolution

| Layer | State Model | Why |
|-------|-------------|-----|
| **System** (knowledge base, signals, events) | Stateful — compiled knowledge, entity lifecycles, signal amplification persist across sessions | The system accumulates understanding over time. DDR-001's compilation model is permanently pre-computed context. |
| **Agent invocation** (single skill/contract execution) | Stateless — the context resolver assembles everything the agent needs into a single context window | Each agent call is a pure function: context in → actions + events out. No hidden state between calls. |
| **Bridge** (context resolver) | The context resolver is the bridge — it projects system state into agent-invocation state | Pre-fetches compiled knowledge, active signals, relevant specs, and checkpoint data into a unified context per invocation. |

### Implications

- **Replay:** Any agent invocation can be replayed by reconstructing its context window from the event log + knowledge base at that point in time.
- **Fork:** Agent executions can be forked by copying the context window and diverging. The system-level state (knowledge base) remains shared.
- **Recovery:** When an agent pauses (`execution.paused`), it serializes a checkpoint. Resumption reconstructs context from checkpoint + any new events since pause. The agent itself stores nothing.
- **Observability:** Because agents are stateless, their entire decision-making context is captured in the input. Combined with the output events, every agent action is fully explainable.

### What This Means for Builders

When building a new MCP tool or skill: your tool receives a context window (the input) and produces events + artifacts (the output). It does NOT maintain state between calls. If it needs to "remember" something, it emits an event or writes to the knowledge base — the context resolver picks it up on the next invocation.

---

## Deployment (Free Tier)

| Server         | FastMCP Cloud URL                          | Alt: Cloudflare |
|---------------|--------------------------------------------| --------------- |
| intent-notice | https://intent-notice.fastmcp.cloud/mcp   | Workers         |
| intent-spec   | https://intent-spec.fastmcp.cloud/mcp     | Workers         |
| intent-observe| https://intent-observe.fastmcp.cloud/mcp  | Workers         |

**Total cost: $0/month** on FastMCP Cloud free tier or Cloudflare Workers (100K req/day).

---

## Cross-Product References

Intent composes with or is used by the following Core products:

| Product | Relationship | Location |
|---|---|---|
| **Cast** | Persona registry feeds Intent's spec-shaping personas; Cast uses Intent's `.intent/` dogfood pattern | `Core/products/cast/` |
| **Forge** | Renders Intent skills (governance hooks, spawn prompts) as deployable Claude Code skills | `Core/products/forge/` |
| **Voices** | Critique pipeline for Intent specs; dissent-preservation law governs review | `Core/products/voices/` |
| **Loom** | Cross-session coordination substrate; sibling at Awareness position | `Core/products/loom/` |
| **Topography** | Planning pipeline position; composes with Loom at COMPACT seam | `Core/products/topography/` |
| **Throughline** | Vision-thread artifact; decision-to-vision traceability | `Core/products/throughline/` |
| **Fieldbook** | Expense lifecycle system; uses Intent loop for its own development | `Core/products/fieldbook/` |
| **Coherence Engineering** | Intent is the reference implementation of the coherence engineering discipline | `Core/frameworks/coherence-engineering/` |

---

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
