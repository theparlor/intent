# Intent: Developer Operating System

Intent is a three-layer personal development OS for autonomous operations: **notice** → **spec** → **execute** → **observe**.

## What Is Intent?

Intent captures observations (signals) as they happen, structures them for action, and tracks autonomous execution.
It sits between personal dev tools (IDE, Cowork) and team/infrastructure automation.

### Three Product Shapes

1. **Developer OS** (Personal) — notice/spec loop inside IDE/Cowork
2. **Team Foundation** (Team) — shared spec library, signal feed, trust dashboard
3. **Autonomous Platform** (Infrastructure) — multi-agent orchestration, L2-L4 execution
4. **Commercial Service** (Market) — SaaS for complex work management

## Core Concepts

### Signals

Observations about work. Examples:
- OTel spans showing contract failures
- Team discussion about process bottleneck
- PR comment suggesting refactoring
- Agent trace discovering inefficiency

**Signal Lifecycle**: `captured` → `active` → `dismissed` or `promoted`

**Trust Levels** (autonomy boundaries):
- **L0** — Noisy idea; human review needed (trust < 0.3)
- **L1** — Reviewed pattern; confirmed but not actionable (trust 0.3-0.5)
- **L2** — High-confidence signal; may trigger conditional actions (trust 0.5-0.7)
- **L3** — Autonomous action trigger (trust 0.7-0.9)
- **L4** — System behavior modification (trust > 0.9)

### Work Ontology

Work is organized in three nested units:

1. **Contract** — Business agreement with vendor/customer (SLA, scope, renewal)
2. **Process** — Workflow running within or across contracts (vendor onboarding, invoice cycle)
3. **Tool** — System executing process (Salesforce, Jira, payment platform)

Each unit has a **schema** defining fields, states, and transitions.

### Intent (The Noun)

A specification for action. Intents have:
- Trigger condition (when to act)
- Policy (what to do)
- Scope (contract/process/tool)
- Boundaries (autonomy level, approval gates)

Example:
```yaml
name: Escalate Contract Renewals
trigger:
  signal: "Contract expires in < 30 days"
action:
  notify: account-owner
  create-task: "Schedule renewal discussion"
  duedate: now + 20 days
scope: contract
autonomy_level: L1  # Human approval before execution
```

## Command-Line Interface

### Signal Management

#### Capture a signal

```bash
# Simple: title only
intent-signal "OTel traces show 40% of contracts fail on first pass"

# Full: with body, source, confidence, trust, author
intent-signal "Title here" \
  --body "Longer description" \
  --source pr-review \
  --author brien \
  --confidence 0.8 \
  --trust 0.6
```

#### Review signals

```bash
# Interactive triage (pending)
intent-signal review

# Review specific signal
intent-signal review SIG-003
```

#### Dismiss a signal

```bash
intent-signal dismiss SIG-003 --reason "Duplicate of SIG-001"
```

#### Cluster signals

```bash
intent-signal cluster SIG-003,SIG-005 --name "Bootstrap tooling"
```

#### Promote signal to intent

```bash
intent-signal promote SIG-003
```

#### List signals

```bash
# List active signals (default)
intent-signal list

# Filter by status
intent-signal list --status captured
intent-signal list --status all
```

#### Show signal details

```bash
intent-signal show SIG-003
```

## File Structure

```
.intent/
  signals/
    2026-03-28-work-ontology.md           # Signal: Work is organized into contract/process/tool
    2026-03-28-conversation-as-signal.md # Signal: Conversations should feed notice layer
    2026-03-28-otel-for-work.md          # Signal: OTel spans map to work units
    2026-03-28-three-dimensions.md       # Signal: Work classified on 3 orthogonal dimensions
    2026-03-28-units-need-schemas.md     # Signal: Work units need schemas
    2026-03-29-ari-pattern-tickets-as-bot-specs.md         # Signal: Ari's team uses tickets as bot specs
    2026-03-29-autonomous-signal-processing-trust-levels.md # Signal: Autonomous ops need L0-L4 trust framework
    2026-03-29-bootstrap-gap-description-vs-enabler.md     # Signal: Bootstrap gap is description infrastructure
    2026-03-29-ceremony-wall-sprint-3.md                   # Signal: Agile ceremonies are overhead
    2026-03-29-four-products-not-one.md                    # Signal: Intent has 4 product shapes
    2026-03-29-multi-machine-cloud-always-on-requirement.md # Signal: Cloud processing must be always-on
    2026-03-29-multi-surface-capture-requirement.md        # Signal: Signals from conversation, OTel, Slack, PRs, traces
    2026-03-29-signals-die-in-context-switch.md            # Signal: Signals must be captured immediately
  templates/
    signal.md                            # Template for new signals
    intent.md                            # Template for new intents (pending)
  schemas/                               # Work unit schemas (planned)
    contract.schema.yaml
    process.schema.yaml
    tool.schema.yaml

bin/
  intent-signal        # Signal management CLI
  intent               # Main CLI (planned)

VERSION              # Current version: 2026.03.29-0.6.0
CHANGELOG.md         # Release notes
CLAUDE.md            # This file
```

## Status

### Completed (v0.6.0)
- [x] Signal template with trust framework fields
- [x] intent-signal CLI with capture, review, dismiss, cluster, promote, list, show
- [x] 13 founding signals scored and clustered
- [x] Signal frontmatter normalized (timestamp, numeric confidence, author, cluster, autonomy_level)
- [x] CLAUDE.md documentation updated
- [x] VERSION bumped to 0.6.0

### In Progress / Planned
- [ ] Intent template and intent-intent CLI subcommands
- [ ] Schema definitions for contract, process, tool
- [ ] Trust scorer (evaluates signal against criteria)
- [ ] Team Foundation layer (shared spec library, signal feed)
- [ ] Autonomous Platform (multi-agent execution, L2-L4)
- [ ] Web dashboard (signal feed, trust metrics, intent status)
- [ ] Integration with Cowork (signal capture from conversation)
- [ ] Integration with OTel (span-to-signal mapping)
- [ ] Integration with Slack (signal reactions, discussion capture)

## Roadmap

### Phase 1: Developer OS (Current)
Personal notice→spec loop. Developer uses intent-signal to capture observations, reviews them as signals, promotes high-trust signals to intents.

### Phase 2: Team Foundation
Shared spec library. Team members see signal feed, vote on trust, collaborate on specs. Dashboard shows team signal health.

### Phase 3: Autonomous Platform
Multi-agent orchestration. Intents execute at L2-L3 autonomy with approval gates. Agents observe execution and generate new signals.

### Phase 4: Commercial Service
SaaS offering. Customers use Intent to manage complex work across vendors/processes/tools. White-label dashboard and integrations.

## References

- **Signal Framework**: `.intent/signals/` — Foundational observations that shaped Intent
- **Work Ontology**: Signal SIG-002 — Contract, process, tool structure
- **Trust Levels**: Signal SIG-001 — L0-L4 autonomy boundaries
- **OTel Mapping**: Signal SIG-004 — How observability feeds signals
