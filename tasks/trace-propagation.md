# Task: Add trace_id propagation to event system

> Handoff spec for Claude Code terminal. Updates models.py and all three MCP servers to propagate trace context through the signal → intent → spec → contract chain.

## Context

Every event in Intent carries `trace_id`, `span_id`, and `parent_id` fields — but they're always null. This task makes them real. When a signal promotes to an intent, the intent's UUID becomes the trace_id that flows through every downstream event. This is the prerequisite for connecting to any OTel backend.

Read `spec/observability-stack.md` for the full architecture. This task implements the "Trace Identity Model" section.

## The Rule

**An Intent is a Trace. Everything under it is a Span.**

- Signals start as orphans (`trace_id: null`)
- When signals promote → intent, intent gets a UUID trace_id
- All signals in the promoted cluster get backfill events linking them to the trace
- Specs created under an intent inherit its trace_id
- Contracts under a spec inherit the trace_id, with parent_id = spec's span_id

## Changes Required

### 1. `servers/models.py` — Update `make_event()`

Current:
```python
def make_event(event_type: str, actor: str, ref: str, data: dict = None, source: str = "mcp") -> str:
    return json.dumps({
        "event": event_type,
        "timestamp": datetime.utcnow().isoformat(),
        "actor": actor,
        "ref": ref,
        "data": data or {},
        "source": source,
    })
```

New:
```python
def make_event(event_type: str, actor: str, ref: str, data: dict = None, source: str = "mcp",
               trace_id: str = None, span_id: str = None, parent_id: str = None) -> str:
    """Create a JSONL-formatted OTel-compatible event with trace context."""
    return json.dumps({
        "version": "0.2.0",
        "event": event_type,
        "timestamp": datetime.utcnow().isoformat(),
        "trace_id": trace_id,
        "span_id": span_id or ref,
        "parent_id": parent_id,
        "actor": actor,
        "ref": ref,
        "data": data or {},
        "source": source,
    })
```

Changes:
- Add `trace_id`, `span_id`, `parent_id` parameters (all default None)
- `span_id` defaults to `ref` for backwards compatibility
- Bump version to `0.2.0` to reflect trace context support
- Include `version` field (was missing from current implementation)

### 2. Add `generate_trace_id()` utility

In `models.py`, add:
```python
import uuid

def generate_trace_id() -> str:
    """Generate a UUID v4 trace ID for an Intent."""
    return str(uuid.uuid4())
```

### 3. Add trace context store

In `models.py`, add a simple lookup class:
```python
class TraceContext:
    """Maps Intent IDs and Spec IDs to their trace context."""

    def __init__(self):
        self._intents: dict[str, str] = {}   # intent_id → trace_id
        self._specs: dict[str, tuple[str, str]] = {}  # spec_id → (trace_id, parent_span_id)

    def register_intent(self, intent_id: str) -> str:
        """Create or retrieve trace_id for an intent."""
        if intent_id not in self._intents:
            self._intents[intent_id] = generate_trace_id()
        return self._intents[intent_id]

    def get_intent_trace(self, intent_id: str) -> str | None:
        return self._intents.get(intent_id)

    def register_spec(self, spec_id: str, intent_id: str) -> tuple[str, str]:
        """Register a spec under an intent. Returns (trace_id, parent_id)."""
        trace_id = self.get_intent_trace(intent_id)
        if trace_id:
            self._specs[spec_id] = (trace_id, intent_id)
        return trace_id, intent_id

    def get_spec_trace(self, spec_id: str) -> tuple[str | None, str | None]:
        """Returns (trace_id, parent_id) for a spec."""
        return self._specs.get(spec_id, (None, None))
```

### 4. `servers/notice.py` — Propagate on promote

When `promote_to_intent` is called:
1. Generate trace_id via `TraceContext.register_intent(intent_id)`
2. Emit `signal.promoted` event with the new trace_id
3. For each signal in the cluster, emit a `signal.updated` event with the trace_id (backfill)

Find the promote tool function and update it to:
```python
trace_ctx = TraceContext()  # module-level instance

# In promote_to_intent:
trace_id = trace_ctx.register_intent(intent_id)
# Emit promotion event with trace context
event = make_event("signal.promoted", author, cluster_or_signal_id,
                   data={"intent_id": intent_id, "signals": signal_ids},
                   source="mcp", trace_id=trace_id, span_id=intent_id)
# Backfill cluster signals
for sig_id in signal_ids:
    backfill = make_event("signal.updated", "system", sig_id,
                          data={"trace_linked": True, "intent_id": intent_id},
                          source="mcp", trace_id=trace_id, span_id=sig_id,
                          parent_id=intent_id)
```

### 5. `servers/spec.py` — Inherit trace from intent

When `create_spec` is called with an `intent_id`:
1. Look up trace_id via `TraceContext.get_intent_trace(intent_id)`
2. Register spec via `TraceContext.register_spec(spec_id, intent_id)`
3. Emit `spec.created` with trace_id and parent_id=intent_id

When `create_contract` is called with a `spec_id`:
1. Look up (trace_id, parent_id) via `TraceContext.get_spec_trace(spec_id)`
2. Emit `contract.verified`/`contract.failed` with trace_id and parent_id=spec_id

### 6. `servers/observe.py` — Correlate by trace

When `ingest_event` receives events, index them by trace_id for correlation:
```python
_traces: dict[str, list[dict]] = {}  # trace_id → [events]

def ingest(event: dict):
    _events.append(event)
    tid = event.get("trace_id")
    if tid:
        _traces.setdefault(tid, []).append(event)
```

Update `detect_spec_delta` and `detect_trust_drift` to query by trace_id when available.

### 7. Share TraceContext across servers

Since the three servers run as separate processes, they can't share an in-memory TraceContext. Two options:

**Option A (Recommended for Phase 1):** Persist trace context to `.intent/trace-context.json`:
```json
{
  "intents": {"INT-003": "550e8400-e29b-41d4-a716-446655440000"},
  "specs": {"SPEC-004": ["550e8400-e29b-41d4-a716-446655440000", "INT-003"]}
}
```
Each server reads this file on startup and writes to it when creating new trace contexts.

**Option B (Phase 2):** OTel Collector provides trace context correlation. Servers export spans; the collector handles parent-child assembly.

Implement Option A for now. Add file read/write to TraceContext class:
```python
TRACE_CONTEXT_PATH = ".intent/trace-context.json"

class TraceContext:
    def __init__(self, intent_root: str = "."):
        self._path = os.path.join(intent_root, TRACE_CONTEXT_PATH)
        self._load()

    def _load(self):
        try:
            with open(self._path) as f:
                data = json.load(f)
                self._intents = data.get("intents", {})
                self._specs = {k: tuple(v) for k, v in data.get("specs", {}).items()}
        except (FileNotFoundError, json.JSONDecodeError):
            self._intents = {}
            self._specs = {}

    def _save(self):
        with open(self._path, "w") as f:
            json.dump({"intents": self._intents, "specs": {k: list(v) for k, v in self._specs.items()}}, f, indent=2)
```

## Verification

```bash
cd ~/Workspaces/Core/frameworks/intent

# 1. Verify models.py has updated make_event signature
python3 -c "from servers.models import make_event; e = make_event('signal.created', 'test', 'SIG-001', trace_id='abc', span_id='SIG-001'); import json; d = json.loads(e); assert d['trace_id'] == 'abc' and d['span_id'] == 'SIG-001' and d['version'] == '0.2.0'; print('PASS: make_event trace context')"

# 2. Verify TraceContext works
python3 -c "from servers.models import TraceContext; tc = TraceContext(); tid = tc.register_intent('INT-001'); assert tid is not None and len(tid) == 36; print(f'PASS: trace_id generated: {tid}')"

# 3. Verify generate_trace_id returns valid UUID
python3 -c "from servers.models import generate_trace_id; import uuid; tid = generate_trace_id(); uuid.UUID(tid); print(f'PASS: valid UUID: {tid}')"

# 4. Verify backward compatibility (no trace context = null fields)
python3 -c "from servers.models import make_event; import json; e = json.loads(make_event('signal.created', 'test', 'SIG-001')); assert e['trace_id'] is None and e['parent_id'] is None; print('PASS: backward compatible')"

# 5. Run existing signal tools to ensure nothing breaks
./bin/intent-status
echo $?  # Should be 0
```

## Commit

```bash
cd ~/Workspaces/Core/frameworks/intent
git add servers/models.py servers/notice.py servers/spec.py servers/observe.py
git add .intent/trace-context.json 2>/dev/null || true
git commit -m "Add trace_id propagation to event system

Updated make_event() with trace_id, span_id, parent_id parameters.
Added TraceContext class for cross-server trace correlation.
Notice server links signals to intents on promotion.
Spec server inherits trace context from parent intent.
Observe server indexes events by trace_id for correlation.

Event version bumped to 0.2.0.

Ref: spec/observability-stack.md (Trace Identity Model)

Co-Authored-By: Claude Opus 4.6 <noreply@anthropic.com>"
```
