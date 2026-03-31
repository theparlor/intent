# Task: Build File Tail Adapter for OTel export

> Handoff spec for Claude Code terminal. Creates a Python adapter that tails events.jsonl and exports spans to an OTel Collector via OTLP/gRPC.

## Context

Intent events live in `.intent/events/events.jsonl`. This adapter reads new events from that file and converts them to OpenTelemetry spans, exporting them to a collector endpoint. It bridges Intent's file-native event system to the OTel ecosystem.

Read `spec/observability-stack.md` for the full architecture. This task implements the "File Tail Adapter" section.

## Prerequisites

- Task `tasks/trace-propagation.md` must be completed first (events need trace_id populated)
- OTel Collector must be running at localhost:4317 (or configurable endpoint)

## What to Build

### `observe/adapters/file-tail.py`

A Python script that:
1. Reads events.jsonl from a configurable path
2. Maintains a checkpoint (byte offset) so it only processes new events
3. Converts each Intent event to an OTel ReadableSpan
4. Exports via OTLP/gRPC to the collector
5. Runs continuously (daemon mode) or one-shot (CI mode)

### Dependencies

Create `observe/adapters/requirements.txt`:
```
opentelemetry-api>=1.20.0
opentelemetry-sdk>=1.20.0
opentelemetry-exporter-otlp-proto-grpc>=1.20.0
```

### Implementation

```python
#!/usr/bin/env python3
"""
Intent File Tail Adapter
Tails .intent/events/events.jsonl and exports OTel spans to a collector.

Usage:
  # Daemon mode (watches for new events)
  python file-tail.py --events-file ../../.intent/events/events.jsonl

  # One-shot mode (process all unprocessed events and exit)
  python file-tail.py --events-file ../../.intent/events/events.jsonl --once

  # Custom endpoint
  python file-tail.py --endpoint otel-collector:4317

Environment variables:
  OTEL_EXPORTER_OTLP_ENDPOINT — Collector endpoint (default: localhost:4317)
  INTENT_EVENTS_FILE — Path to events.jsonl
  INTENT_CHECKPOINT_FILE — Path to checkpoint file (default: .tail-checkpoint)
"""

import argparse
import json
import os
import sys
import time
import uuid
from datetime import datetime, timezone
from pathlib import Path

from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider, ReadableSpan
from opentelemetry.sdk.trace.export import BatchSpanExporter, SimpleSpanExporter
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from opentelemetry.sdk.resources import Resource
from opentelemetry.trace import StatusCode


def setup_exporter(endpoint: str, insecure: bool = True) -> TracerProvider:
    """Configure OTel tracer provider with OTLP exporter."""
    resource = Resource.create({
        "service.name": "intent",
        "service.version": "0.2.0",
        "deployment.environment": os.environ.get("INTENT_ENV", "local"),
    })
    provider = TracerProvider(resource=resource)
    exporter = OTLPSpanExporter(endpoint=endpoint, insecure=insecure)
    provider.add_span_processor(BatchSpanExporter(exporter))
    trace.set_tracer_provider(provider)
    return provider


def load_checkpoint(checkpoint_path: str) -> int:
    """Load the last processed byte offset."""
    try:
        with open(checkpoint_path) as f:
            return int(f.read().strip())
    except (FileNotFoundError, ValueError):
        return 0


def save_checkpoint(checkpoint_path: str, offset: int):
    """Save the current byte offset."""
    with open(checkpoint_path, "w") as f:
        f.write(str(offset))


def to_otel_trace_id(intent_trace_id: str | None) -> int:
    """Convert Intent trace_id (UUID string) to OTel 128-bit trace ID."""
    if not intent_trace_id:
        # Generate a random trace ID for orphan events
        return uuid.uuid4().int & ((1 << 128) - 1)
    try:
        return uuid.UUID(intent_trace_id).int
    except ValueError:
        # If it's not a UUID, hash it
        return int(uuid.uuid5(uuid.NAMESPACE_DNS, intent_trace_id).int) & ((1 << 128) - 1)


def to_otel_span_id(intent_span_id: str | None) -> int:
    """Convert Intent span_id (e.g., SIG-003) to OTel 64-bit span ID."""
    if not intent_span_id:
        return uuid.uuid4().int & ((1 << 64) - 1)
    return int(uuid.uuid5(uuid.NAMESPACE_DNS, intent_span_id).int) & ((1 << 64) - 1)


def parse_timestamp(ts: str) -> int:
    """Parse ISO 8601 timestamp to nanoseconds since epoch."""
    dt = datetime.fromisoformat(ts.replace("Z", "+00:00"))
    return int(dt.timestamp() * 1e9)


def convert_event(event: dict, tracer) -> None:
    """Convert an Intent event to an OTel span and export it."""
    event_type = event.get("event", "unknown")
    timestamp = event.get("timestamp", datetime.utcnow().isoformat())

    # Build attributes from event data
    attributes = {
        "intent.event_type": event_type,
        "intent.source": event.get("source", "unknown"),
        "intent.ref": event.get("ref", ""),
        "intent.version": event.get("version", "0.1.0"),
    }

    # Add actor if present
    if event.get("actor"):
        attributes["intent.actor"] = event["actor"]

    # Flatten data dict into attributes
    for k, v in event.get("data", {}).items():
        if isinstance(v, (str, int, float, bool)):
            attributes[f"intent.data.{k}"] = v
        elif isinstance(v, list):
            attributes[f"intent.data.{k}"] = json.dumps(v)

    # Create span (point event: start == end)
    with tracer.start_as_current_span(
        name=event_type,
        attributes=attributes,
    ) as span:
        # Set span status based on event type
        if "failed" in event_type:
            span.set_status(StatusCode.ERROR, f"{event_type}")
        else:
            span.set_status(StatusCode.OK)


def process_events(events_file: str, checkpoint_path: str, tracer, once: bool = False):
    """Main loop: tail events file and export new events."""
    offset = load_checkpoint(checkpoint_path)

    while True:
        try:
            file_size = os.path.getsize(events_file)
        except FileNotFoundError:
            if once:
                print(f"Events file not found: {events_file}")
                return
            time.sleep(5)
            continue

        if file_size < offset:
            # File was truncated or rotated
            print(f"File appears truncated (size {file_size} < offset {offset}), resetting")
            offset = 0

        if file_size > offset:
            with open(events_file, "r") as f:
                f.seek(offset)
                new_lines = f.readlines()
                new_offset = f.tell()

            count = 0
            for line in new_lines:
                line = line.strip()
                if not line:
                    continue
                try:
                    event = json.loads(line)
                    convert_event(event, tracer)
                    count += 1
                except json.JSONDecodeError as e:
                    print(f"Skipping malformed event: {e}")

            if count > 0:
                print(f"Exported {count} events (offset {offset} → {new_offset})")

            offset = new_offset
            save_checkpoint(checkpoint_path, offset)

        if once:
            return

        time.sleep(2)


def main():
    parser = argparse.ArgumentParser(description="Intent File Tail Adapter")
    parser.add_argument("--events-file", default=os.environ.get("INTENT_EVENTS_FILE", ".intent/events/events.jsonl"))
    parser.add_argument("--endpoint", default=os.environ.get("OTEL_EXPORTER_OTLP_ENDPOINT", "localhost:4317"))
    parser.add_argument("--checkpoint", default=os.environ.get("INTENT_CHECKPOINT_FILE", ".tail-checkpoint"))
    parser.add_argument("--once", action="store_true", help="Process all unprocessed events and exit")
    parser.add_argument("--insecure", action="store_true", default=True, help="Use insecure gRPC connection")
    args = parser.parse_args()

    print(f"Intent File Tail Adapter")
    print(f"  Events: {args.events_file}")
    print(f"  Endpoint: {args.endpoint}")
    print(f"  Mode: {'one-shot' if args.once else 'daemon'}")

    provider = setup_exporter(args.endpoint, args.insecure)
    tracer = trace.get_tracer("intent.adapter.file-tail", "0.2.0")

    try:
        process_events(args.events_file, args.checkpoint, tracer, args.once)
    except KeyboardInterrupt:
        print("\nShutting down...")
    finally:
        provider.shutdown()


if __name__ == "__main__":
    main()
```

**Important:** The implementation above is illustrative. Read it, understand the pattern, then write the actual file. The OTel SDK's span creation API may require adjustments — for instance, you may need to use `tracer.start_span()` with explicit context to set trace_id and parent_id from the event rather than generating new ones. Consult the OpenTelemetry Python SDK docs for `SpanContext` and `NonRecordingSpan` patterns to inject existing trace/span IDs.

### OTel Collector Config

Create `observe/otel-collector-config.yaml`:

```yaml
receivers:
  otlp:
    protocols:
      grpc:
        endpoint: 0.0.0.0:4317
      http:
        endpoint: 0.0.0.0:4318

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

exporters:
  debug:
    verbosity: detailed

  # Uncomment and configure for Grafana Cloud:
  # otlphttp/grafana:
  #   endpoint: ${GRAFANA_OTLP_ENDPOINT}
  #   headers:
  #     Authorization: "Basic ${GRAFANA_CLOUD_TOKEN}"

service:
  pipelines:
    traces:
      receivers: [otlp]
      processors: [batch, attributes/intent]
      exporters: [debug]
```

### Directory Structure

```
observe/
├── adapters/
│   ├── file-tail.py
│   └── requirements.txt
├── otel-collector-config.yaml
└── README.md
```

### README.md

Create `observe/README.md` with:
- Quick start (install deps, run collector, run adapter)
- Configuration options (environment variables)
- Grafana Cloud setup instructions (placeholder for Brien to fill in after account creation)

## Verification

```bash
cd ~/Workspaces/Core/frameworks/intent

# 1. Verify adapter file exists and is valid Python
python3 -c "import ast; ast.parse(open('observe/adapters/file-tail.py').read()); print('PASS: valid Python')"

# 2. Verify requirements.txt has correct deps
grep -q 'opentelemetry-sdk' observe/adapters/requirements.txt && echo "PASS: SDK dep present" || echo "FAIL"
grep -q 'opentelemetry-exporter-otlp' observe/adapters/requirements.txt && echo "PASS: exporter dep present" || echo "FAIL"

# 3. Verify collector config is valid YAML
python3 -c "import yaml; yaml.safe_load(open('observe/otel-collector-config.yaml')); print('PASS: valid YAML')" 2>/dev/null || python3 -c "
import json
# Fallback: just check it's parseable
with open('observe/otel-collector-config.yaml') as f:
    content = f.read()
    assert 'receivers:' in content and 'exporters:' in content
    print('PASS: collector config has required sections')
"

# 4. Install deps and verify imports work
cd observe/adapters
pip install -r requirements.txt --break-system-packages 2>/dev/null
python3 -c "from opentelemetry import trace; from opentelemetry.sdk.trace import TracerProvider; print('PASS: OTel SDK imports work')"

# 5. Test one-shot mode against existing events (will fail to connect to collector — that's OK)
# This validates the file-reading logic, not the export
cd ~/Workspaces/Core/frameworks/intent
python3 observe/adapters/file-tail.py --events-file .intent/events/events.jsonl --once --endpoint localhost:4317 2>&1 | head -5
echo "NOTE: Connection refused is expected if collector is not running"
```

## Commit

```bash
cd ~/Workspaces/Core/frameworks/intent
git add observe/
git commit -m "Add OTel file tail adapter and collector config

New observe/ directory with:
- adapters/file-tail.py: tails events.jsonl, exports OTel spans
- otel-collector-config.yaml: collector pipeline for local + Grafana Cloud
- README.md: setup and operation guide

Supports daemon mode (continuous) and one-shot (CI).
Checkpoint-based offset tracking for exactly-once processing.

Ref: spec/observability-stack.md (File Tail Adapter)

Co-Authored-By: Claude Opus 4.6 <noreply@anthropic.com>"
```
