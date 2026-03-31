# Intent Product — Execution Roadmap

> Master execution plan for terminal Claude. Read this FIRST, before any task spec.
> Phases are sequential. Do NOT skip phases. Do NOT parallelize across phases.

---

## Phase 0: Reconciliation ✅ COMPLETE

Reconcile product-roadmap.md with actual repo state. Update TASKS.md. Remove stale claims.

**Completed 2026-03-30 by Cowork session.**

---

## Phase 1: Trace Propagation — CURRENT

**Task spec:** `tasks/trace-propagation.md`
**Dependency:** None
**Unlocks:** Phase 2 (file tail adapter), Phase 3 (Grafana)

### What to do
1. Read `spec/observability-stack.md` § "Trace Identity Model"
2. Read `tasks/trace-propagation.md` for exact code diffs
3. Update `servers/models.py` — add trace_id, span_id, parent_id to make_event()
4. Update `servers/notice.py` — signal.promoted_to_intent generates trace_id
5. Update `servers/spec.py` — specs inherit trace_id from parent intent
6. Update `servers/observe.py` — events carry trace context through the chain

### Verification

```bash
# models.py has trace fields
grep -c "trace_id" servers/models.py  # expect ≥ 3

# notice.py propagates trace_id on promotion
grep "trace_id" servers/notice.py  # expect in promote_to_intent

# spec.py inherits trace_id
grep "trace_id" servers/spec.py  # expect in create_spec

# observe.py carries trace context
grep "trace_id" servers/observe.py  # expect in ingest_event
```

### Contract
- CON-PROD-001: `make_event()` signature includes trace_id, span_id, parent_id parameters
- CON-PROD-002: `promote_to_intent` generates a UUID trace_id and backfills cluster signals
- CON-PROD-003: `create_spec` inherits trace_id from parent intent
- CON-PROD-004: No event emitted with trace_id=null after promotion (orphan signals before promotion are allowed)

---

## Phase 2: File Tail Adapter

**Task spec:** `tasks/file-tail-adapter.md`
**Dependency:** Phase 1 (trace_id must be populated)
**Unlocks:** Phase 3 (Grafana dashboard)

### What to do
1. Read `tasks/file-tail-adapter.md` for full implementation
2. Create `observe/adapters/file-tail.py` — tails events.jsonl, converts to OTLP spans
3. Create `observe/adapters/requirements.txt` — OTel SDK dependencies
4. Test with: `python observe/adapters/file-tail.py --once --jsonl .intent/events/events.jsonl`

### Verification

```bash
# file exists and is executable
test -f observe/adapters/file-tail.py && echo "EXISTS"

# has OTel imports
grep "opentelemetry" observe/adapters/file-tail.py  # expect sdk, exporter imports

# requirements file exists
test -f observe/adapters/requirements.txt && echo "EXISTS"

# dry-run parse (no collector needed)
python3 -c "
import json
with open('.intent/events/events.jsonl') as f:
    events = [json.loads(line) for line in f if line.strip()]
print(f'{len(events)} events parsed')
"
```

### Contract
- CON-PROD-005: `file-tail.py` accepts --jsonl and --endpoint CLI arguments
- CON-PROD-006: `file-tail.py` maintains a checkpoint file to avoid re-processing events
- CON-PROD-007: Events with trace_id are converted to OTel spans; events without trace_id are converted to standalone spans with a synthetic trace

---

## Phase 3: Grafana Dashboard

**Task spec:** `tasks/grafana-dashboard.md`
**Dependency:** Phase 2 (file tail adapter producing spans)
**Unlocks:** Metrics framework, operational readiness

### What to do
1. Read `tasks/grafana-dashboard.md` for dashboard JSON spec
2. Validate `observe/grafana/` dashboard definitions
3. Verify OTel Collector config at `observe/otel-collector-config.yaml` is internally consistent
4. Document the deployment steps in `observe/README.md`

### Verification

```bash
# Dashboard JSON is valid
python3 -c "
import json, glob
for f in glob.glob('observe/grafana/*.json'):
    json.loads(open(f).read())
    print(f'VALID: {f}')
"

# OTel collector config is valid YAML
python3 -c "
import yaml
with open('observe/otel-collector-config.yaml') as f:
    cfg = yaml.safe_load(f)
    assert 'receivers' in cfg, 'missing receivers'
    assert 'exporters' in cfg, 'missing exporters'
    print('VALID collector config')
"

# README has deployment steps
grep -c "docker\|grafana\|otelcol" observe/README.md  # expect ≥ 3
```

### Contract
- CON-PROD-008: All JSON files in `observe/grafana/` parse without error
- CON-PROD-009: OTel collector config references receivers, processors, and exporters
- CON-PROD-010: `observe/README.md` contains step-by-step deployment instructions

---

## Phase 4: Signal Enrichment

**Dependency:** Phase 1 (trace propagation for event emission)
**Can run in parallel with Phases 2-3** — this is the only parallelizable phase.

### What to do
1. Emit cluster files to `.intent/` for the 6 identified signal clusters (see `spec/product-roadmap.md` § Signal Cluster Analysis)
2. Add `referenced_by` field to `.intent/templates/signal.md`
3. Update `servers/models.py` trust scoring to include reference frequency as amplification factor
4. Backfill `referenced_by` on existing 24 signals where cross-references exist

### Verification

```bash
# Cluster files exist
ls .intent/clusters/ 2>/dev/null | wc -l  # expect ≥ 6

# Signal template has referenced_by
grep "referenced_by" .intent/templates/signal.md  # expect present

# models.py trust scoring includes reference factor
grep "reference\|amplif" servers/models.py  # expect in trust computation

# At least some signals have referenced_by populated
grep -l "referenced_by" .intent/signals/*.md | wc -l  # expect > 0
```

### Contract
- CON-PROD-011: Each signal cluster has a `.intent/clusters/<name>.md` file using the cluster template
- CON-PROD-012: Signal template frontmatter includes `referenced_by: []` field
- CON-PROD-013: Trust score computation in models.py includes a reference frequency factor

---

## Phase 5: Housekeeping

**Dependency:** Phases 1-4 complete

### What to do
1. Bump VERSION to 0.7.0
2. Update CHANGELOG.md with all Phase 1-4 work
3. Verify CLAUDE.md is still accurate after all changes
4. Run `intent-status` CLI tool to confirm it reflects current state

### Verification

```bash
# Version bumped
cat VERSION  # expect 2026.03.30-0.7.0 or similar

# CHANGELOG has entries for this round
grep -c "0.7.0\|trace propagation\|file tail\|signal cluster" CHANGELOG.md  # expect ≥ 3

# intent-status runs without error
bash bin/intent-status 2>&1 | head -5
```

---

## Disambiguation Queue — Surfaces to Brien only

These items CANNOT be resolved by agents. They require human voice, external evidence, or architecture decisions with long-tail consequences. When encountered, generate a disambiguation signal to `.intent/signals/` with `status: blocked` and `trust: 0.1`.

| Item | Why it's blocked | Signal refs |
|------|-----------------|-------------|
| Intent Manifesto | Requires Brien's voice and conviction | — |
| Practitioner interviews | Requires human-to-human interaction | SIG-010 |
| Vocabulary decision ("Notice"/"Execute") | Naming cascades everywhere; requires product judgment | SIG-019 |
| Signal ID strategy | Architecture decision with distributed system implications | SIG-022, SIG-023 |
| Case Study #1 | Requires Brien's introspection + narrative | — |

---

*Created: 2026-03-30 by Cowork session*
*Phase status: Phase 0 COMPLETE, Phase 1 CURRENT*
