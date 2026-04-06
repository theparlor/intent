---
title: Grafana Dashboard
type: framework
maturity: final
confidentiality: shareable
reusability: universal
domains:
  - consulting-operations
created: 2026-03-31
depth_score: 3
depth_signals:
  file_size_kb: 5.1
  content_chars: 4907
  entity_count: 0
  slide_count: 0
  sheet_count: 0
  topic_count: 1
  has_summary: 0
vocab_density: 0.00
---
# Task: Create Grafana dashboard definition for Intent Observe

> Handoff spec for Claude Code terminal. Creates a Grafana dashboard JSON that can be imported into Grafana Cloud or self-hosted Grafana.

## Context

The Intent Observe dashboard is the visual surface of the observe layer. It answers: "What's happening in the system right now, and where should I look next?" Read `spec/observability-stack.md` for the full panel layout.

## Prerequisites

- OTel Collector and File Tail Adapter running (tasks/file-tail-adapter.md)
- Grafana instance with Tempo data source configured

## What to Build

### `observe/grafana/dashboards/intent-observe.json`

A Grafana dashboard JSON definition with these panels:

#### Row 1: Summary Stats (4 stat panels)
- **Active Signals** — Count of signals with status=active
- **Active Intents** — Count of intents with status!=complete
- **Specs In Progress** — Count of specs with status=executing or approved
- **Contract Results** — Pass/fail ratio of contract.verified vs contract.failed events

#### Row 2: Cycle Time (bar gauge panel)
- Signal → Intent median and p95
- Intent → Spec median and p95
- Spec → Complete median and p95

Computed from timestamp deltas between lifecycle events sharing a trace_id.

#### Row 3: Trust Distribution (bar chart)
- X axis: autonomy levels (L0, L1, L2, L3, L4)
- Y axis: count of active signals at each level
- Color: persona colors (L0=red, L1=amber, L2=blue, L3=green, L4=emerald)

#### Row 4: Event Stream (table panel)
- Live tail of recent events
- Columns: timestamp, event_type, ref, source, actor
- Sorted by timestamp descending
- Clickable ref links to trace explorer

#### Row 5: Trace Explorer (trace list panel)
- List of active traces (intents) with span count and duration
- Expandable to show waterfall view of all spans in a trace
- Uses Tempo's native trace search

### Dashboard Variables

- `$timeRange` — Standard Grafana time picker
- `$source` — Filter by event source (all, cli, mcp, github-action, etc.)
- `$autonomy` — Filter by autonomy level (L0-L4)

### Data Source Queries

For Tempo traces:
```
{ resource.service.name = "intent" }
```

For metrics (if Mimir/Prometheus configured):
```promql
# Active signals
sum(intent_signals_active)

# Cycle time
histogram_quantile(0.5, rate(intent_cycle_time_signal_to_intent_bucket[7d]))

# Contract pass rate
sum(rate(intent_contracts_total{result="pass"}[7d])) /
sum(rate(intent_contracts_total[7d]))
```

For log queries (if Loki configured):
```logql
{service_name="intent"} | json | event_type =~ "signal.*|spec.*|contract.*"
```

### Implementation Notes

- Use Grafana's JSON model format (dashboard → panels → targets)
- Set `uid` to `intent-observe` for stable imports
- Set `editable: true` so Brien can customize after import
- Include a `__requires` section for Tempo, Prometheus/Mimir, Loki data sources
- Panels that require Mimir/Loki should have `"datasource": null` fallback with a note

The dashboard should be importable via:
```bash
# Via Grafana API
curl -X POST -H "Content-Type: application/json" \
  -H "Authorization: Bearer $GRAFANA_TOKEN" \
  -d @observe/grafana/dashboards/intent-observe.json \
  $GRAFANA_URL/api/dashboards/db

# Or via Grafana UI: Dashboards → Import → Upload JSON
```

## Verification

```bash
cd ~/Workspaces/Core/frameworks/intent

# 1. Verify JSON is valid
python3 -c "import json; d = json.load(open('observe/grafana/dashboards/intent-observe.json')); print(f'PASS: valid JSON, {len(d.get(\"panels\", d.get(\"dashboard\", {}).get(\"panels\", [])))} panels')"

# 2. Verify required panels exist
python3 -c "
import json
d = json.load(open('observe/grafana/dashboards/intent-observe.json'))
panels = d.get('panels', d.get('dashboard', {}).get('panels', []))
titles = [p.get('title', '') for p in panels]
required = ['Signal', 'Intent', 'Spec', 'Contract', 'Cycle', 'Trust', 'Event', 'Trace']
found = sum(1 for r in required if any(r.lower() in t.lower() for t in titles))
print(f'PASS: {found}/{len(required)} required panel groups found')
assert found >= 5, f'Missing panels: only {found} of {len(required)} found'
"

# 3. Verify dashboard uid
python3 -c "
import json
d = json.load(open('observe/grafana/dashboards/intent-observe.json'))
uid = d.get('uid', d.get('dashboard', {}).get('uid', ''))
assert 'intent' in uid.lower(), f'Expected uid containing intent, got {uid}'
print(f'PASS: dashboard uid = {uid}')
"
```

## Commit

```bash
cd ~/Workspaces/Core/frameworks/intent
git add observe/grafana/
git commit -m "Add Grafana dashboard definition for Intent Observe

Dashboard panels: summary stats, cycle time, trust distribution,
event stream, trace explorer. Importable to Grafana Cloud or
self-hosted. Uses Tempo for traces, Mimir for metrics, Loki for logs.

Ref: spec/observability-stack.md (Grafana Dashboard)

Co-Authored-By: Claude Opus 4.6 <noreply@anthropic.com>"
```
