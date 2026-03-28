# Signal: Three Orthogonal Governance Dimensions

ID: SIG-004
Date: 2026-03-28
Status: Captured

## Problem

Agile conflates three separate concerns:
1. What should we build? (discovery)
2. When should we build it? (scheduling)
3. How should we build it? (governance)

Mixing these makes teams rigid. Changing one dimension breaks the others.

## Insight

These three dimensions are **orthogonal**. They should be separate, with clear interfaces.

## Three Dimensions

### 1. Right Things (Discovery)

**Question**: What should we build?

**Flow**:
1. **Input**: Signals (raw observations, user requests)
2. **Parse**: Extract Intents (declarative goals)
3. **Prioritize**: Sort by impact, effort, risk
4. **Output**: Roadmap (ordered list of Intents)

**Tools**: User research, design sessions, monitoring, customer interviews

**Metric**: Intent quality (clarity, testability, impact estimation)

### 2. Right Time (Parallelization)

**Question**: When can we build it in parallel?

**Flow**:
1. **Input**: Specs (detailed requirements)
2. **Analyze**: Build dependency graph
   - What specs block other specs?
   - Where are the critical paths?
3. **Schedule**: Use DAG solver to parallelize
4. **Output**: Work streams (teams can work in parallel)

**Tools**: Dependency analysis, work partitioning, resource leveling

**Metric**: Parallelization ratio (how much work happens in parallel vs. sequential)

### 3. Right Way (Governance)

**Question**: How do we build it correctly?

**Flow**:
1. **Input**: Contracts (interface specs, guarantees)
2. **Enforce**: Quality gates
   - Design review (does this meet the intent?)
   - Code review (does this meet the spec?)
   - Test coverage (are all edge cases covered?)
   - Performance budgets (are we within SLAs?)
3. **Output**: Tested capabilities, merged to main

**Tools**: Reviews, CI/CD, monitoring, rollback procedures

**Metric**: Quality (test pass rate, deployment success rate, mean time to recovery)

## How They Interact

- **Right Things** feeds work into the system
- **Right Time** schedules it without dependencies
- **Right Way** ensures it's built correctly

Each dimension is independent:
- You can change discovery (new signals) without changing governance
- You can improve parallelization without changing specs
- You can add quality gates without blocking discovery

## Encoding in the Spec

Each spec includes metadata for all three dimensions:

```yaml
Id: SPEC-001
Intent: "Users should set daily budgets"

# Right Things
DiscoverySource: SIG-001  # Links back to the signal
Impact: "Reduces overspending by 30% (estimated)"
Priority: P0

# Right Time
Dependencies: [CON-003, CON-004]  # Blocks these contracts
EstimatedDuration: 3 days
CriticalPath: true

# Right Way
ArchitectureReview: Required
TestCoverage: >= 90%
SLOLatency: < 100ms p99
```

## Benefits

- **Separation of concerns**: Change one dimension without affecting others
- **Team autonomy**: Teams own different dimensions
- **Observability**: Each dimension has clear metrics
- **Scaling**: As team grows, dimensions don't conflict
