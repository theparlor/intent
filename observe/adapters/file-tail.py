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
  OTEL_EXPORTER_OTLP_ENDPOINT  Collector endpoint (default: localhost:4317)
  INTENT_EVENTS_FILE           Path to events.jsonl
  INTENT_CHECKPOINT_FILE       Path to checkpoint file (default: .tail-checkpoint)
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
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanExporter
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from opentelemetry.sdk.resources import Resource
from opentelemetry.trace import SpanContext, SpanKind, NonRecordingSpan, TraceFlags
from opentelemetry.context import Context


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
        return uuid.uuid4().int & ((1 << 128) - 1)
    try:
        return uuid.UUID(intent_trace_id).int & ((1 << 128) - 1)
    except ValueError:
        return uuid.uuid5(uuid.NAMESPACE_DNS, intent_trace_id).int & ((1 << 128) - 1)


def to_otel_span_id(intent_span_id: str | None) -> int:
    """Convert Intent span_id (e.g., SIG-003) to OTel 64-bit span ID."""
    if not intent_span_id:
        return uuid.uuid4().int & ((1 << 64) - 1)
    return uuid.uuid5(uuid.NAMESPACE_DNS, intent_span_id).int & ((1 << 64) - 1)


def parse_timestamp(ts: str) -> int:
    """Parse ISO 8601 timestamp to nanoseconds since epoch."""
    dt = datetime.fromisoformat(ts.replace("Z", "+00:00"))
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)
    return int(dt.timestamp() * 1e9)


def convert_event(event: dict, tracer) -> None:
    """Convert an Intent event to an OTel span and export it."""
    event_type = event.get("event", "unknown")
    timestamp = event.get("timestamp", datetime.utcnow().isoformat())

    attributes = {
        "intent.event_type": event_type,
        "intent.source": event.get("source", "unknown"),
        "intent.ref": event.get("ref", ""),
        "intent.version": event.get("version", "0.1.0"),
    }

    if event.get("actor"):
        attributes["intent.actor"] = event["actor"]

    for k, v in event.get("data", {}).items():
        if isinstance(v, (str, int, float, bool)):
            attributes[f"intent.data.{k}"] = v
        elif isinstance(v, list):
            attributes[f"intent.data.{k}"] = json.dumps(v)

    # Build parent context if trace_id is present
    otel_trace_id = to_otel_trace_id(event.get("trace_id"))
    parent_span_id = to_otel_span_id(event.get("parent_id")) if event.get("parent_id") else None

    if parent_span_id:
        parent_ctx = SpanContext(
            trace_id=otel_trace_id,
            span_id=parent_span_id,
            is_remote=True,
            trace_flags=TraceFlags(0x01),
        )
        context = trace.set_span_in_context(NonRecordingSpan(parent_ctx))
    else:
        context = None

    with tracer.start_as_current_span(
        name=event_type,
        kind=SpanKind.INTERNAL,
        attributes=attributes,
        context=context,
    ) as span:
        if "failed" in event_type:
            span.set_status(trace.StatusCode.ERROR, event_type)
        else:
            span.set_status(trace.StatusCode.OK)


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
                print(f"Exported {count} events (offset {offset} -> {new_offset})")

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
