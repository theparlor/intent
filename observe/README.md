---
title: Readme
type: framework
maturity: final
confidentiality: shareable
reusability: universal
domains:
  - consulting-operations
created: 2026-03-31
depth_score: 2
depth_signals:
  file_size_kb: 2.6
  content_chars: 2228
  entity_count: 0
  slide_count: 0
  sheet_count: 0
  topic_count: 1
  has_summary: 0
vocab_density: 0.90
---
# Intent Observe — Observability Infrastructure

OTel-native distributed tracing for the Intent loop. Connects the event system to Grafana via OpenTelemetry Collector.

## Quick Start

### 1. Install adapter dependencies

```bash
cd observe/adapters
pip install -r requirements.txt
```

### 2. Run the OTel Collector

Download the [OTel Collector binary](https://opentelemetry.io/docs/collector/installation/) for your platform, then:

```bash
otelcol-contrib --config observe/otel-collector-config.yaml
```

### 3. Run the File Tail Adapter

```bash
# One-shot: process all existing events
python observe/adapters/file-tail.py --once

# Daemon: continuously tail new events
python observe/adapters/file-tail.py
```

## Configuration

| Variable | Default | Description |
|----------|---------|-------------|
| `OTEL_EXPORTER_OTLP_ENDPOINT` | `localhost:4317` | Collector gRPC endpoint |
| `INTENT_EVENTS_FILE` | `.intent/events/events.jsonl` | Path to event log |
| `INTENT_CHECKPOINT_FILE` | `.tail-checkpoint` | Byte offset checkpoint |
| `INTENT_ENV` | `local` | Deployment environment label |

## Grafana Cloud Setup

1. Create a free account at [grafana.com](https://grafana.com)
2. Go to Connections > Add new connection > OpenTelemetry
3. Copy the OTLP endpoint and generate an API token
4. Update `otel-collector-config.yaml`: uncomment the `otlphttp/grafana` exporter and add your endpoint/token
5. Import `grafana/dashboards/intent-observe.json` via Dashboards > Import

## Architecture

```
CLI/MCP/GitHub -> events.jsonl -> File Tail Adapter -> OTel Collector -> Grafana Cloud
                                                                        (Tempo + Mimir + Loki)
```

See `spec/observability-stack.md` for the full architecture specification.

## Directory Structure

```
observe/
├── adapters/
│   ├── file-tail.py          <- events.jsonl -> OTLP adapter
│   └── requirements.txt      <- Python dependencies
├── grafana/
│   ├── dashboards/
│   │   └── intent-observe.json  <- Dashboard definition
│   └── provisioning/
│       └── datasources.yaml     <- Data source config (Phase 2)
├── otel-collector-config.yaml   <- Collector pipeline config
└── README.md                    <- This file
```
