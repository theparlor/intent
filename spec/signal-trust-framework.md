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
  file_size_kb: 7.3
  content_chars: 6992
  entity_count: 0
  slide_count: 0
  sheet_count: 0
  topic_count: 1
  has_summary: 0
vocab_density: 0.14
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
