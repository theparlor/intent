---
title: Signal Trust Framework
type: framework
maturity: final
confidentiality: shareable
reusability: universal
domains:
  - consulting-operations
created: 2026-03-31
depth_score: 4
depth_signals:
  file_size_kb: 9.4
  content_chars: 9221
  entity_count: 0
  slide_count: 0
  sheet_count: 0
  topic_count: 1
  has_summary: 0
vocab_density: 0.11
---
# Signal Trust & Autonomous Execution Framework

> How Intent decides what can self-execute and what needs a human.

## The Problem

Signals enter the system at varying levels of clarity and risk. Today, every signal requires human triage. This doesn't scale — and more importantly, it wastes human attention on signals that agents could resolve autonomously. The goal is: **work every signal as far along as it can go**, and only involve humans when their judgment actually matters.

## Trust Model

Every signal gets two scores:

### Confidence (existing)
How likely is this signal to be real and worth acting on?
- Range: 0.0 – 1.0
- Set by: Source adapter (initial), enrichment agents (refined)
- Factors: source reliability, corroboration from other signals, recency, specificity

### Trust Score (new)
How confidently can an agent resolve this without human input?
- Range: 0.0 – 1.0
- Set by: Trust scoring agent (computed from signal properties)
- Factors:
  - **Clarity** — Is the problem unambiguous? Can you write a failing test from the description alone?
  - **Blast radius** — How many files/services/users are affected by the fix?
  - **Reversibility** — Can the change be rolled back if wrong?
  - **Contract testability** — Can success be verified programmatically?
  - **Precedent** — Have similar signals been resolved successfully before?

### Trust Score Computation

```
trust = (clarity × 0.30) + (1/blast_radius × 0.20) + (reversibility × 0.20) + (testability × 0.20) + (precedent × 0.10)
```

Each factor is 0.0–1.0. The weights reflect that clarity is most important (ambiguity is the top reason agents fail), followed by risk factors, with precedent as a tiebreaker.

## Autonomy Levels

| Level | Name | Trust Range | Human Role | Signal Types |
|-------|------|-------------|------------|--------------|
| L0 | Human drives | < 0.2 | Full control | Strategic decisions, ambiguous observations |
| L1 | Agent assists | 0.2 – 0.4 | Decides, agent enriches | Feature requests, UX friction, process gaps |
| L2 | Agent decides, human approves | 0.4 – 0.6 | Reviews & approves | Performance issues, dependency updates, config drift |
| L3 | Agent executes, human monitors | 0.6 – 0.85 | Observes after the fact | Bug fixes, test failures, lint violations, doc gaps |
| L4 | Full autonomy | ≥ 0.85 | Circuit breaker only | Typos, formatting, dependency patches, known patterns |

### Builder-Configurable Thresholds

Teams configure their own autonomy thresholds in `.intent/config.yml`:

```yaml
autonomy:
  thresholds:
    L1: 0.2    # below this: human drives
    L2: 0.4    # below this: agent assists only
    L3: 0.6    # below this: agent needs approval
    L4: 0.85   # above this: full autonomy
  
  circuit_breakers:
    max_files_changed: 5          # auto-stop if agent touches > N files
    max_blast_radius: "service"   # file | module | service | system
    require_tests: true           # agent must include tests for L3+
    require_rollback_plan: true   # L4 changes must be revertable
  
  allowed_auto_actions:
    - fix_lint
    - fix_test_failure
    - update_dependency_patch
    - fix_typo
    - update_docs
  
  require_human:
    - schema_migration
    - api_breaking_change
    - security_related
    - new_service
    - cost_increase
```

## Signal Lifecycle (Extended)

```
captured → enriched → scored → classified → routed
                                              ├─ L0: → human_queue (signal stays, human triages)
                                              ├─ L1: → enriched_queue (agent adds context, human decides)
                                              ├─ L2: → approval_queue (agent drafts intent+spec, human approves)
                                              ├─ L3: → execution_queue (agent runs full loop, posts to observe)
                                              └─ L4: → auto_queue (agent runs + deploys, circuit breakers active)
```

At any point, if an agent encounters ambiguity it can't resolve, it generates a **disambiguation signal**:

```
original_signal (ambiguous, trust=0.3)
  └─ disambiguation_signal (asks: "did you mean X or Y?")
       └─ human responds → enriched_signal (trust=0.8) → re-enters pipeline
```

This is the recursive loop. The system never dead-ends — it either resolves or asks a better question.

## Signal Enrichment Pipeline

Enrichment is a chain of agents, each adding properties:

1. **Source Adapter** — Captures raw signal, sets initial confidence
2. **Dedup Agent** — Checks for existing similar signals, links or merges
3. **Context Agent** — Adds related files, recent commits, related signals
4. **Trust Scorer** — Computes trust score from signal properties
5. **Classifier** — Assigns autonomy level based on trust score + config thresholds
6. **Router** — Sends to appropriate queue (human, approval, execution, auto)

Each agent in the chain:
- Reads the signal
- Adds/modifies properties in the frontmatter
- Emits an enrichment event to events.jsonl
- Passes to next agent

## Event Types (New)

| Event | Emitted When |
|-------|--------------|
| `signal.enriched` | An enrichment agent adds context |
| `signal.scored` | Trust score computed |
| `signal.classified` | Autonomy level assigned |
| `signal.routed` | Signal sent to queue |
| `signal.disambiguated` | Human clarified an ambiguous signal |
| `signal.auto_promoted` | Agent auto-promoted signal to intent (L3/L4) |
| `signal.auto_specced` | Agent auto-generated spec from signal (L3/L4) |
| `signal.auto_executed` | Agent completed execution without human (L4) |
| `signal.circuit_break` | Auto-execution stopped by circuit breaker |

## Human Contact as Agent Capability

The trust model above defines **governance gates** — when an agent MUST involve a human. This section defines the inverse: when an agent CHOOSES to involve a human.

### The `request_human_input` Signal Type

Any agent at any trust level can emit a `request_human_input` signal. This is not a governance constraint — it's a strategic tool. The agent recognizes that human judgment would improve the outcome and proactively asks.

```yaml
# Signal frontmatter for request_human_input
id: SIG-NNN
type: request_human_input
timestamp: 2026-04-13T10:00:00Z
source: agent
trust: 0.0                    # Trust is irrelevant — this is a request, not an execution
status: awaiting_response
requester_spec: SPEC-NNN      # What spec the agent is executing
urgency: blocking | informational | deferred
question: "Plain language question"
context: "What the agent knows and why it's asking"
options: ["Option A", "Option B"]
timeout_seconds: 3600
fallback_action: "What agent does if no response"
```

### How It Differs from Governance Gates

| Dimension | Governance Gate (L0-L2) | Strategic Request |
|-----------|------------------------|-------------------|
| **Trigger** | Trust score below threshold | Agent judgment |
| **Mandatory?** | Yes — agent cannot proceed | No — agent could proceed but chooses not to |
| **Trust level** | Only fires at L0-L2 | Fires at ANY level, including L4 |
| **Purpose** | Risk mitigation | Quality improvement |
| **Response required?** | Yes — blocks execution | Configurable — can timeout to fallback |

### Routing

`request_human_input` signals route through the same channels as other signals (Slack, CLI, MCP) but with urgency-aware priority:
- **blocking:** Immediate notification, agent pauses (emits `execution.paused`)
- **informational:** Normal notification, agent continues with best-guess approach
- **deferred:** Batched with other signals for next human review cycle

### Integration with Disambiguation

The existing disambiguation loop (`disambiguation_signal`) is a special case of `request_human_input` where the question is specifically "did you mean X or Y?" The new signal type generalizes this — any question, not just disambiguation.

## Open Questions

1. **Where does enrichment run?** Local agents (Claude Code sessions) or hosted service? The config-driven deployment model means both should be possible.
2. **How do we handle conflicting signals?** Two signals that point in opposite directions — does the system detect this?
3. **What's the feedback loop?** When an L3/L4 execution fails, does the trust model learn? (Adaptive trust scoring.)
4. **Multi-repo signals?** A signal in repo A might be best resolved in repo B. Cross-repo routing.
5. **Team trust calibration?** Different team members may have different trust tolerances. Per-user overrides?

## Implementation Priority

**Now:**
- Add `trust` and `autonomy_level` fields to signal schema/template
- Add `status` field lifecycle: captured → active → clustered → promoted → dismissed
- Signal management CLI: `intent-signal review`, `dismiss`, `cluster`, `promote`
- Signal dashboard (HTML) showing lifecycle, clusters, trust scores ✓ DONE

**Next:**
- Trust scoring agent (first enrichment agent)
- Config file schema (`.intent/config.yml`)
- Approval queue workflow (L2 signals present to human for approval)
- Disambiguation signal generation

**Later:**
- Full enrichment pipeline (all 6 agents)
- Adaptive trust scoring (learns from outcomes)
- Cross-repo signal routing
- Hosted deployment mode
