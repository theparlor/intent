---
title: Observability Stack
type: framework
maturity: final
confidentiality: shareable
reusability: universal
domains:
  - consulting-operations
created: 2026-03-31
technologies:
  - slack
depth_score: 5
depth_signals:
  file_size_kb: 26.9
  content_chars: 19226
  entity_count: 1
  slide_count: 0
  sheet_count: 0
  topic_count: 1
  has_summary: 0
vocab_density: 0.10
related_entities:
  - {pair: consulting-operations ↔ subaru, count: 836, strength: 0.43}
  - {pair: consulting-operations ↔ automotive-manufacturing, count: 791, strength: 0.409}
  - {pair: consulting-operations ↔ engagement-management, count: 507, strength: 0.262}
  - {pair: consulting-operations ↔ turnberry, count: 472, strength: 0.226}
  - {pair: consulting-operations ↔ foot-locker, count: 256, strength: 0.133}
---
# Observability Stack Specification

> Open-source, OTel-native infrastructure for Intent's Observe layer. Connects the event system to a real distributed tracing backend so work flowing through Notice → Spec → Execute → Observe becomes queryable, visualizable, and alertable.

## Problem

Intent's event system emits 15 OTel-compatible event types through 6 mechanisms — but every event lands in a flat JSONL file with `trace_id: null`. The three MCP servers (notice, spec, observe) maintain isolated in-memory event stores with no cross-server correlation. You can't answer basic observability questions:

- "How long does it take from signal capture to spec approval?"
- "Which intents have stalled — signals promoted but no spec created?"
- "What's the contract pass rate this week?"
- "Show me every work unit that traced from SIG-003 through to deployment."

The event schema is right. The emission mechanisms exist. What's missing is the infrastructure that turns flat events into queryable traces, metrics, and dashboards.

## Design Principles

1. **OTel-native, not OTel-adjacent.** Use OpenTelemetry Collector as the single intake surface. Every source speaks OTLP or gets adapted to OTLP. No proprietary ingest formats.
2. **File-native stays.** `events.jsonl` remains the git-tracked audit log. The observability stack reads from it — it doesn't replace it. Two outputs: git (audit) + backend (query).
3. **Progressive deployment.** Solo practitioner starts with Grafana Cloud free tier. Teams self-host when they outgrow it. Same collector config, different export targets.
4. **No lock-in.** Each layer (collector, trace store, metrics store, log store, dashboard) is independently swappable. Grafana is the recommended default, not a dependency.

## Architecture

```
┌──────────────── SOURCES ────────────────┐
│                                         │
│  CLI tools    MCP servers    GitHub      │
│  (bash)       (Python)       Actions     │
│     │              │            │        │
│     ▼              ▼            ▼        │
│  events.jsonl   in-memory   workflow     │
│  (append)       event list   logs        │
│                                         │
└─────────────────┬───────────────────────┘
                  │
         ┌────────▼────────┐
         │  File Tail      │  ← Reads new lines from events.jsonl
         │  Adapter        │  ← Converts Intent events → OTLP spans
         │  (Python)       │  ← Manages trace_id propagation
         └────────┬────────┘
                  │ OTLP/gRPC
         ┌────────▼────────┐
         │  OTel Collector  │  ← Also receives from:
         │  (otelcol)       │     - GitHub webhook receiver
         │                  │     - MCP server direct export (Phase 2)
         └──┬─────┬─────┬──┘
            │     │     │
     ┌──────▼─┐ ┌▼────┐ ┌▼──────┐
     │ Tempo  │ │Mimir│ │ Loki  │
     │(traces)│ │(met)│ │(logs) │
     └───┬────┘ └──┬──┘ └──┬───┘
         │         │       │
         └────┬────┘───────┘
              │
         ┌────▼─────┐
         │ Grafana  │  ← Unified query surface
         │          │  ← Dashboards, alerts
         └──────────┘
```

### Component Roles

| Component | Role | Intent Mapping |
|-----------|------|----------------|
| **File Tail Adapter** | Watches `events.jsonl`, converts to OTLP spans | Bridge between file-native and network-native |
| **OTel Collector** | Receives, processes, exports telemetry | Central nervous system |
| **Grafana Tempo** | Trace storage — span hierarchies, waterfall views | "Show me the full journey of INT-003" |
| **Grafana Mimir** | Metrics — counters, gauges, histograms | "Signal capture rate", "Spec cycle time" |
| **Grafana Loki** | Log aggregation — structured log streams | "All events from source=github-action today" |
| **Grafana** | Visualization, alerting, exploration | The Observe dashboard |

## Deployment Phases

### Phase 1: Grafana Cloud Free Tier (Now — Solo Practitioner)

**Analogy:** Renting a furnished apartment. You bring your clothes (events), they provide everything else.

**What you get free:**
- 50GB traces/month (Tempo)
- 50GB logs/month (Loki)
- 10,000 active metrics series (Mimir)
- 14-day retention
- Hosted Grafana with alerting

**What you run locally:**
- File Tail Adapter (Python script, runs on your machine or as a GitHub Action)
- OTel Collector (single binary, ~50MB, config-driven — no Docker required)

**What you DON'T run:**
- No containers. No Docker. No orchestration.
- The collector is a standalone binary (like `git` or `node`)
- The adapter is a Python script

**Always-on webhook:** A Cloudflare Worker (free tier) receives GitHub webhook events and forwards to Grafana Cloud's OTLP endpoint. This gives you real-time GitHub telemetry even when your laptop is closed.

**Cost:** $0. Free tier handles a solo practitioner's volume for months.

**Setup:**
1. Create Grafana Cloud account → get OTLP endpoint + API key
2. Download OTel Collector binary for macOS
3. Configure collector with Grafana Cloud exporter
4. Run File Tail Adapter → feeds collector → feeds Grafana Cloud
5. Deploy Cloudflare Worker for GitHub webhooks (optional but recommended)
6. Import Intent Observe dashboard template

### Phase 2: Docker Compose on Single Machine (Always-On Processing)

**Analogy:** Buying a house with one of everything. Same plumbing, you own it.

**When:** When your laptop going offline during travel breaks the pipeline. Or when you want unlimited retention and full data ownership.

**What you run:**
- Docker Compose: Tempo + Mimir + Loki + Grafana + OTel Collector + File Tail Adapter
- Single machine: $5/month VPS, Raspberry Pi, Mac Mini, or any always-on box
- Same OTel Collector config, just different export targets (localhost instead of Grafana Cloud)

**What changes from Phase 1:**
- Export targets switch from `otlphttp/grafana` to `otlp/tempo` + `prometheusremotewrite/mimir` + `loki`
- Add `docker-compose.yml` (provided in `observe/docker-compose.yml`)
- Dashboard JSON imports to self-hosted Grafana instead of cloud

**What stays the same:**
- Same collector config structure
- Same adapter code
- Same dashboard definitions
- Same trace identity model

### Phase 3: k3s (Multi-Team Scale)

**Analogy:** The apartment complex. Only needed when you have multiple tenants.

**When:** Multiple teams each running `.intent/` in their repos, data volumes exceed single-machine capacity, need autoscaling or multi-node redundancy.

**What changes:**
- Kafka between collector and backends (fan-out for multiple consumers)
- Span sampling strategy (head-based for high-trust work, tail-based for failures)
- Cross-repo trace linking (multiple `.intent/` repos share trace context)
- k3s (lightweight Kubernetes) for orchestration — not full k8s
- Helm charts for each component

**What stays the same:**
- Same OTel Collector config (containerized instead of binary)
- Same adapter code (containerized)
- Same dashboard definitions
- Same trace identity model

**Key principle: Every phase uses the same collector config and the same trace identity model. Only the deployment topology changes.**

## Trace Identity Model

This is the most critical design decision. It determines whether the observability backend shows you disconnected dots or connected work streams.

### The Rule

**An Intent is a Trace. Everything under it is a Span.**

```
TRACE: INT-003 "Build Slack signal bot"
│
├── SPAN: SIG-006 "Teams want signal capture from chat"
│     └── event: signal.created (source: conversation)
│
├── SPAN: SIG-008 "Slack reactions as signal triggers"
│     └── event: signal.created (source: pr-review)
│
├── SPAN: SIG-006+SIG-008 cluster
│     └── event: signal.clustered
│     └── event: signal.promoted → creates INT-003
│
├── SPAN: SPEC-004 "Slack Signal Capture Bot"
│     ├── event: spec.created (parent: INT-003)
│     ├── event: spec.approved
│     │
│     ├── SPAN: CON-012 "Bot responds to emoji reaction"
│     │     ├── event: contract.started
│     │     ├── event: contract.assertion.passed
│     │     └── event: contract.completed
│     │
│     └── SPAN: CON-013 "Signal has source=slack"
│           ├── event: contract.started
│           └── event: contract.assertion.failed (!)
│
└── SPAN: observation
      └── event: observation.written (delta detected: CON-013 failed)
      └── event: signal.created → NEW signal from observation
```

### Trace ID Assignment Rules

| Moment | What happens to trace_id |
|--------|--------------------------|
| Signal created (no intent yet) | `trace_id = null` — signal is an orphan observation |
| Signals clustered | Cluster gets a provisional trace_id: `cluster-{uuid}` |
| Cluster promoted → Intent | Intent ID becomes the trace_id. All member signals are **backfilled** with this trace_id |
| Spec created under Intent | Inherits `trace_id` from parent Intent. `parent_id` = Intent span_id |
| Contract created under Spec | Inherits `trace_id` from parent Spec. `parent_id` = Spec span_id |
| Contract execution events | Inherit `trace_id` and `parent_id` from the contract |
| Observation creates new signal | New signal is an orphan (new trace begins if it promotes) |

### Backfill Mechanism

When signals promote to an intent, the adapter must:
1. Generate a trace_id for the new Intent (UUID v4)
2. Emit the `signal.promoted` event with the new trace_id
3. Emit **retroactive span updates** for each signal in the cluster, linking them to the new trace_id
4. The JSONL file gets the events appended (immutable log — no rewriting old events)
5. The trace backend receives the full span hierarchy

This means traces "grow backwards" — signals exist before their trace does. This is fine. Tempo and Jaeger both support receiving spans in any order and assembling the hierarchy at query time.

### Implementation: `make_event()` Changes

Current signature:
```python
def make_event(event_type, actor, ref, data=None, source="mcp") -> str
```

New signature:
```python
def make_event(event_type, actor, ref, data=None, source="mcp",
               trace_id=None, span_id=None, parent_id=None) -> str
```

The caller is responsible for passing trace context. The MCP servers maintain a lookup:
- `notice.py`: When promoting, generates trace_id and stores `{intent_id: trace_id}`
- `spec.py`: When creating spec under intent, looks up intent's trace_id
- `observe.py`: When ingesting events, correlates by trace_id

## Source Adapters

### 1. File Tail Adapter (Primary)

A Python script that:
1. Watches `events.jsonl` for new lines (using file offset checkpoint)
2. Parses each JSON line
3. Maps Intent event fields to OTel span fields:
   - `event.trace_id` → OTel `trace_id` (generate if null for orphan signals)
   - `event.span_id` → OTel `span_id`
   - `event.parent_id` → OTel `parent_span_id`
   - `event.event` → Span name
   - `event.timestamp` → Span start time (point event = start == end)
   - `event.source` → Span attribute `intent.source`
   - `event.data.*` → Span attributes `intent.data.*`
4. Exports via OTLP/gRPC to collector

```python
# Adapter pseudocode
from opentelemetry.sdk.trace.export import BatchSpanExporter
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter

exporter = OTLPSpanExporter(endpoint="localhost:4317")

def convert_event_to_span(event: dict) -> ReadableSpan:
    return ReadableSpan(
        name=event["event"],
        context=SpanContext(
            trace_id=to_otel_id(event.get("trace_id") or generate_orphan_id()),
            span_id=to_otel_id(event.get("span_id") or event.get("ref")),
        ),
        parent=SpanContext(trace_id=..., span_id=to_otel_id(event.get("parent_id")))
            if event.get("parent_id") else None,
        start_time=parse_iso(event["timestamp"]),
        end_time=parse_iso(event["timestamp"]),
        attributes={
            "intent.event_type": event["event"],
            "intent.source": event.get("source", "unknown"),
            "intent.actor": event.get("actor", "unknown"),
            "intent.ref": event.get("ref", ""),
            **{f"intent.data.{k}": str(v) for k, v in event.get("data", {}).items()},
        },
    )
```

### 2. GitHub Webhook Receiver

An OTel Collector receiver that accepts GitHub webhook payloads and maps them to spans:

| GitHub Event | Intent Event | Span Attributes |
|-------------|-------------|----------------|
| `push` to `.intent/signals/*` | `signal.created` | file, author, sha |
| `push` to `.intent/intents/*` | `intent.proposed` | file, author, sha |
| `push` to `.intent/specs/*` | `spec.written` | file, author, sha |
| `workflow_run.completed` | `system.health` | workflow, status, duration |
| `issues.opened` (label=freshness) | `observation.written` | issue_number, drift_count |

Receiver config (OTel Collector):
```yaml
receivers:
  webhookevent/github:
    endpoint: 0.0.0.0:8088
    path: /github
    health_path: /health
```

### 3. MCP Server Direct Export (Phase 2)

Add OpenTelemetry Python SDK to the MCP servers so they export spans directly:

```python
# In notice.py, spec.py, observe.py
from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter

provider = TracerProvider()
provider.add_span_processor(BatchSpanProcessor(OTLPSpanExporter()))
trace.set_tracer_provider(provider)
tracer = trace.get_tracer("intent.notice")

# When creating a signal:
with tracer.start_as_current_span("signal.created") as span:
    span.set_attribute("intent.signal_id", sig_id)
    span.set_attribute("intent.source", source)
    span.set_attribute("intent.confidence", confidence)
    span.set_attribute("intent.trust", trust)
    # ... create signal as before
```

This replaces the File Tail Adapter for MCP-sourced events. The adapter remains for CLI and GitHub Action events.

### 4. Entire.io Session Bridge (Phase 2)

Entire.io is the execution observability layer. It records full Claude Code session traces — every file read, edit, command, and test — and produces the `trace.completed` event that makes agent work visible to the Observe layer.

| Entire.io Output | Intent Event | What It Captures |
|-----------------|-------------|-----------------|
| Session recording | `trace.completed` | Full execution trace: files, commands, durations |
| File change log | (attribute on trace span) | Blast radius — what files were touched |
| Command log | (attribute on trace span) | What shell commands were run |
| Session metadata | span attributes | Duration, exit code, agent model, token usage |

Entire.io's `.entire/` directory in each repo holds the raw session data. The adapter reads completed sessions and emits them as OTel spans to the collector.

```
.entire/sessions/
├── 2026-03-30T10-42-00.json   ← raw session trace
├── 2026-03-30T14-15-00.json
└── ...
```

Each session maps to an Intent trace when the session was invoked with a spec reference. The adapter looks up the spec's trace_id via TraceContext and parents the execution spans under it.

### 5. Claude Code Session Adapter (Phase 2)

Claude Code terminal sessions produce execution traces. An adapter wraps session output:

| Claude Code Event | Intent Event | What It Captures |
|------------------|-------------|-----------------|
| Session start (with spec ref) | `contract.started` | Which spec/contract being executed |
| File written/edited | (attribute on parent span) | Blast radius indicator |
| Test passed | `contract.assertion.passed` | Evidence of verification |
| Test failed | `contract.assertion.failed` | Failure detail |
| Session end | `contract.completed` | Duration, file count, test results |

Implementation: A wrapper script around Claude Code that emits OTLP spans:
```bash
#!/bin/bash
# intent-execute: wraps claude-code with OTel instrumentation
TRACE_ID=$(lookup_trace_for_spec "$SPEC_ID")
otel-cli span start --trace-id "$TRACE_ID" --name "contract.started"
claude-code "$@"
EXIT_CODE=$?
otel-cli span end --status "$([[ $EXIT_CODE -eq 0 ]] && echo ok || echo error)"
```

## Metrics Model

Beyond traces, Intent needs gauges and counters for the Observe dashboard.

### Counters (Monotonically Increasing)

| Metric | Description | Labels |
|--------|-------------|--------|
| `intent.signals.total` | Total signals captured | source, status |
| `intent.specs.total` | Total specs created | status, product |
| `intent.contracts.total` | Total contracts verified | result (pass/fail) |
| `intent.events.total` | Total events emitted | event_type, source |

### Gauges (Current State)

| Metric | Description | Labels |
|--------|-------------|--------|
| `intent.signals.active` | Currently active signals | cluster |
| `intent.signals.trust_avg` | Average trust score of active signals | — |
| `intent.pipeline.depth` | Signals awaiting promotion | — |
| `intent.specs.in_progress` | Specs currently executing | product |

### Histograms (Distributions)

| Metric | Description | Buckets |
|--------|-------------|---------|
| `intent.cycle_time.signal_to_intent` | Duration from signal → intent promotion | 1h, 4h, 1d, 3d, 7d, 14d |
| `intent.cycle_time.intent_to_spec` | Duration from intent → spec approval | 1h, 4h, 1d, 3d, 7d, 14d |
| `intent.cycle_time.spec_to_complete` | Duration from spec → contract completion | 1h, 4h, 1d, 3d, 7d |
| `intent.trust_score` | Distribution of trust scores | 0.1, 0.2, 0.4, 0.6, 0.85, 1.0 |

### Metrics Emission

The File Tail Adapter computes metrics by maintaining in-memory state derived from events:
- Count events by type → counters
- Track open signals/specs → gauges
- Compute timestamps between lifecycle events → histograms

Export via Prometheus remote-write to Mimir (or Grafana Cloud).

## OTel Collector Configuration

```yaml
# otel-collector-config.yaml
receivers:
  otlp:
    protocols:
      grpc:
        endpoint: 0.0.0.0:4317
      http:
        endpoint: 0.0.0.0:4318

  # GitHub webhook receiver (Phase 2)
  # webhookevent/github:
  #   endpoint: 0.0.0.0:8088

processors:
  batch:
    timeout: 5s
    send_batch_size: 256

  attributes/intent:
    actions:
      - key: service.name
        value: "intent"
        action: upsert
      - key: deployment.environment
        value: "local"
        action: upsert

  # Filter out system.health noise during development
  filter/dev:
    spans:
      exclude:
        match_type: strict
        attributes:
          - key: intent.event_type
            value: "system.status"

exporters:
  # Phase 1: Grafana Cloud
  otlphttp/grafana:
    endpoint: https://otlp-gateway-prod-us-central-0.grafana.net/otlp
    headers:
      Authorization: "Basic ${GRAFANA_CLOUD_TOKEN}"

  # Phase 2: Self-hosted
  # otlp/tempo:
  #   endpoint: tempo:4317
  #   tls:
  #     insecure: true
  # prometheusremotewrite:
  #   endpoint: http://mimir:9009/api/v1/push
  # loki:
  #   endpoint: http://loki:3100/loki/api/v1/push

  # Debug: log to console during development
  debug:
    verbosity: detailed

service:
  pipelines:
    traces:
      receivers: [otlp]
      processors: [batch, attributes/intent]
      exporters: [otlphttp/grafana, debug]
    # metrics:
    #   receivers: [otlp]
    #   processors: [batch]
    #   exporters: [otlphttp/grafana]
    # logs:
    #   receivers: [otlp]
    #   processors: [batch]
    #   exporters: [otlphttp/grafana]
```

## Grafana Dashboard: Intent Observe

### Panel Layout

```
┌─────────────────────────────────────────────────────┐
│  INTENT OBSERVE DASHBOARD                            │
├──────────┬──────────┬──────────┬────────────────────┤
│ Signals  │ Intents  │ Specs    │ Contracts          │
│   24     │    5     │    3     │  Pass: 12 Fail: 1  │
│ active   │ active   │ in prog  │                    │
├──────────┴──────────┴──────────┴────────────────────┤
│                                                      │
│  CYCLE TIME (histogram)                              │
│  Signal→Intent: median 2.1d │ p95 6.3d              │
│  Intent→Spec:   median 1.4d │ p95 4.8d              │
│  Spec→Complete:  median 0.8d │ p95 2.1d              │
│                                                      │
├──────────────────────────────────────────────────────┤
│                                                      │
│  TRUST DISTRIBUTION (heatmap)                        │
│  L0 ██░░░░░░░░ 3                                    │
│  L1 ████░░░░░░ 5                                    │
│  L2 ██████░░░░ 8                                    │
│  L3 ████████░░ 6                                    │
│  L4 ██░░░░░░░░ 2                                    │
│                                                      │
├──────────────────────────────────────────────────────┤
│                                                      │
│  EVENT STREAM (live log)                             │
│  10:42 signal.created   SIG-025  source=mcp          │
│  10:38 contract.passed  CON-014  spec=SPEC-003       │
│  10:35 spec.approved    SPEC-004 intent=INT-005      │
│                                                      │
├──────────────────────────────────────────────────────┤
│                                                      │
│  TRACE EXPLORER                                      │
│  ▸ INT-003 "Slack signal bot"      4 spans  2.1d     │
│  ▸ INT-005 "Trust scoring agent"   7 spans  0.8d     │
│  ▸ Orphan signals (no intent yet)  6 spans           │
│                                                      │
└──────────────────────────────────────────────────────┘
```

### Alert Rules

| Alert | Condition | Severity |
|-------|-----------|----------|
| Stale intent | Intent has no new events in 7 days | Warning |
| Contract failure | `contract.assertion.failed` event | Critical |
| Volume surge | > 20 signals in 24h | Warning |
| Trust drift | Average trust drops > 0.1 in 7 days | Info |
| Pipeline stall | No events of any type in 48h | Warning |

## File Structure (New Files)

```
intent/
├── observe/                          ← Observability infrastructure
│   ├── otel-collector-config.yaml    ← Collector pipeline config
│   ├── docker-compose.yml            ← Self-hosted stack (Phase 2)
│   ├── grafana/
│   │   ├── dashboards/
│   │   │   └── intent-observe.json   ← Dashboard definition
│   │   └── provisioning/
│   │       └── datasources.yaml      ← Tempo + Mimir + Loki sources
│   ├── adapters/
│   │   ├── file-tail.py              ← events.jsonl → OTLP adapter
│   │   ├── github-webhook.py         ← GitHub events → OTLP (Phase 2)
│   │   └── requirements.txt          ← opentelemetry-sdk, etc.
│   └── README.md                     ← Setup and operation guide
├── servers/
│   └── models.py                     ← Updated make_event() with trace context
└── spec/
    └── observability-stack.md        ← THIS FILE
```

## Implementation Order

1. **Update `make_event()` in models.py** — Add trace_id, span_id, parent_id parameters
2. **Update MCP servers** — Pass trace context when creating signals, specs, contracts
3. **Build File Tail Adapter** — Python script: tail events.jsonl → OTLP export
4. **Deploy OTel Collector** — Local binary with Grafana Cloud export config
5. **Create Grafana Cloud account** — Get OTLP endpoint + configure dashboards
6. **Build Intent Observe dashboard** — Import panel definitions
7. **Add metrics emission** — Counters, gauges, histograms from adapter state
8. **GitHub webhook receiver** — OTel Collector receives GitHub events directly
9. **Claude Code wrapper** — `intent-execute` script emits execution spans
10. **Self-hosted option** — Docker Compose for teams wanting data control

## Trust Assessment

This spec at L2 autonomy:
- **Confidence: 0.80** — OTel is well-documented; Grafana stack is mature
- **Trust: 0.55** — Infrastructure work has configuration complexity; Grafana Cloud setup requires Brien's credentials
- **Blast radius: Low** — Observability is additive. Existing file-native events continue regardless
- **Reversibility: High** — Can disable collector and adapter with no impact on event capture

## Dependencies

- `opentelemetry-sdk` (Python) — For adapter and MCP server instrumentation
- `opentelemetry-exporter-otlp` — OTLP export
- `otelcol-contrib` binary — OTel Collector with webhook receiver
- Grafana Cloud account (free tier) — Or self-hosted Docker stack

## Semantic Versioning Note

This spec represents the **Phase 1 → Phase 2** evolution described in SIG-017 (OTel deployment spectrum) and the "Phase 6: OTel upgrade" described in the Event Catalog spec. It replaces the generic "migrate from JSONL to full OTel collector" guidance with a concrete, deployable architecture.
