---
type: signal
date: 2026-04-15
origin: pawel-huryn 2026-04-14 newsletter + intent-orchestrator architecture review
severity: medium
scope: intent-framework-methodology
tags:
  - orchestration-choice
  - explicit-graph
  - single-call-agent
  - pipeline-design
  - methodology
related_mental_models:
  - agent-as-callable-component
  - intent-orchestrator
---
# Signal: Orchestration Choice as a First-Class Design Decision

## Observation

The Intent framework currently has one orchestration pattern baked in: **explicit skill chains executed by `intent-orchestrator`**. Each chain is a directed graph of skills with defined data flow, observable at each node, resumable mid-chain.

Huryn's Agent SDK pattern (2026-04-14) presents an alternative orchestration model: **single-function agent call** where the agent's internal reasoning handles flow control. Simple orchestration and guardrails live in hooks or business logic around the call, not in a node-by-node graph.

These are not interchangeable. Each has distinct trade-offs. The framework currently does not name this choice — which means pipeline designers pick implicitly, usually defaulting to explicit-graph because it's the documented pattern.

## The Trade-Off Matrix

| Dimension | Explicit Graph (intent-orchestrator) | Single-Call Agent (Huryn's SDK pattern) |
|---|---|---|
| Observability | HIGH — every step logged with inputs/outputs | LOW — internal reasoning is a single span |
| Resumability | HIGH — pause and resume mid-chain | LOW — query() is atomic |
| Flexibility | LOW — graph is fixed at design time | HIGH — agent adapts per invocation |
| Debugging | EASY — step isolation, deterministic replay | HARDER — reasoning trace needed, non-deterministic |
| Cost predictability | HIGH — per-step budgets and caching | LOW — agent iterates as needed up to maxTurns |
| Complexity on simple tasks | OVERHEAD — forcing graph structure on a 2-step task | LOW — one function call |
| Complexity on complex tasks | WELL-SUITED — graphs scale cleanly | BOTTLENECK — single context, single model |

## The Heuristic (Proposed)

**Use explicit graph when:**
- Pipeline is batch / offline (time-to-complete measured in minutes to hours)
- Observability matters (audit requirements, client deliverable traceability)
- Resumability matters (long-running, interruption-tolerant)
- Cost must be predictable (fixed-budget engagements, token-cap enforcement)
- Steps involve distinct competencies that benefit from different models (Sonnet for one step, Opus for another)

Examples: **Cortège fetch fabric, Opus synthesizer, multi-persona research**, engagement-kickoff workflows, declutter pipelines.

**Use single-call agent when:**
- Pipeline is request-response (time-to-complete measured in seconds to 1 minute)
- Flexibility matters (input space is open-ended, agent needs to decide tool sequence)
- End-user cares about answer quality more than process traceability
- Cost envelope is small enough that bounded iteration is tolerable
- Pipeline fits naturally inside a single Claude context window

Examples: **on-demand persona voice generation** (skills-engine renders → SDK agent responds with brand-aligned copy), **interactive Q&A against a corpus**, contextual lookups inside an app.

**Mixed / nested:** Complex pipelines often benefit from explicit-graph at the top layer with single-call agents as leaves. The intent-orchestrator runs the graph; each node may be either a skill (current model) or a callable-component agent (new model).

## Implications for Intent Framework Evolution

1. **Methodology module addition.** `Core/frameworks/intent/methodology/orchestration-choice.md` — articulates the heuristic above, provides decision tree, lists worked examples from Brien's current pipelines.

2. **Skill frontmatter field.** Skills should declare their preferred orchestration mode — `orchestration: explicit-graph | single-call | either`. Skills that support either mode ship with both renderings (see companion signal on `agent-sdk` rendering target).

3. **DoR/DoD extension.** Definition of Ready for a pipeline build should include: "Orchestration mode chosen and justified against heuristic." Definition of Done should include: "Observability and resumability requirements traced to orchestration choice."

4. **Signal capture extension.** Post-implementation signals should evaluate: did the chosen orchestration mode hold? If the pipeline was rebuilt later with the other mode, what triggered the switch? This feeds a lessons-learned loop.

## Why This Matters Beyond the Pawel Ingestion

Brien's composable architecture has been building toward the callable-component pattern without explicitly naming the orchestration-mode choice. This is why Huryn's newsletter triggered Brien's self-assessment: "is this giving it a name, or modifying our thinking?"

**It's giving it a name for the composable pattern; it's modifying our thinking about orchestration.** The Intent framework has assumed explicit-graph as the default. Huryn's pattern shows this is a choice, not a given. Making the choice explicit unlocks:
- Simpler pipelines that don't need the graph overhead
- Better packaging (SDK-callable targets — see skills-engine signal)
- Clearer architectural decisions that future engineers can audit

## Recommended Actions

1. Draft `methodology/orchestration-choice.md` in the Intent framework knowledge library
2. Add orchestration-mode frontmatter field to skills-engine SKILL.md template
3. Backfill the field on existing skills with `orchestration: explicit-graph` as safe default (migration signal, not per-skill individual audits)
4. Add the orchestration-choice question to the DoR checklist template at `Core/frameworks/intent/knowledge-engine/templates/dor-dod-library.md`

## Timing

- Not blocking anything urgent
- Should precede the `agent-sdk` rendering target implementation (skills-engine signal) — orchestration choice is the methodology layer; SDK rendering is the implementation layer
- Target window: late April / early May 2026

## Cross-Reference

- Companion signals: `Core/personas/.intent/signals/2026-04-15-pipeline-components-as-callable-agents.md`, `Core/products/skills-engine/.intent/signals/2026-04-15-agent-sdk-as-new-rendering-target.md`
- Source: Pawel Huryn newsletter 2026-04-14 (`Core/personas/corpus/pawel-huryn/newsletter-2026-04-14-claude-agent-sdk-production-agent.md`)
- Related mental models: `intent-orchestrator` (Brien), `agent-as-callable-component` (Huryn)
