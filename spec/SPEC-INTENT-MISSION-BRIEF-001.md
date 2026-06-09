---
title: Mission Brief — the Formation Flight dispatch payload
id: SPEC-INTENT-MISSION-BRIEF-001
type: spec
created: 2026-06-05
updated: 2026-06-05
related:
  - servers/models.py (Contract, make_event, TraceContext — the carriers this composes with)
  - "servers/knowledge.py (get_core :1259 — sources the standing-core slice of reference_frame)"
  - spec/SPEC-substrate-exposure-envelope-extensions-DRAFT.md (the OTHER, read-direction envelope — sibling, not this)
  - spec/autonomy-flight-model-v1-DRAFT.md (§16 λ-scoping — trust_gate/lambda source)
  - hooks/autonomy-grant-dispatch-prompt-check.sh (the dispatch-prompt sibling this complements)
depth_score: 4
depth_signals:
  file_size_kb: 7.5
  content_chars: 6639
  entity_count: 0
  slide_count: 0
  sheet_count: 0
  topic_count: 0
  has_summary: 0
vocab_density: 0.00
status: draft
plane: bridge
author: intent framework (formation-flight build)
parent: SPEC-INTENT-FORMATION-FLIGHT-001
schema: formation/mission-brief.schema.json
return_schema: formation/mission-report.schema.json
---
# Mission Brief

> One sentence: the typed coherence contract an orchestrator (Tower) hands DOWN to each parallel agent
> (a sortie) before it flies its seam — so the system's intent, vocabulary, and "don't do X" constraints
> survive the agent's isolation instead of evaporating at turn 47.

**Status:** `draft` · **Created:** 2026-06-05 · **Schema (source of truth):** `formation/mission-brief.schema.json`

---

## 1. Intent

### What I noticed
A spawned subagent is, by design, ignorant of the system's intent. The dispatch prompt carries the task;
it does **not** reliably carry the invariants, the canonical vocabulary, or the explicit non-goals. There
is a hook for the *negative* case (`autonomy-grant-dispatch-prompt-check.sh` blocks proposal-framing
injection, F13) — but nothing carries the *positive* coherence contract into the agent's context.

### Why it matters now
Two envelopes already exist in Intent and **neither is a dispatch payload**: the **flight envelope** (the
safe operating region, flight-model §4) and the **substrate-exposure envelope** (the knowledge-server
RETURN payload — `sightline`/`supply_policy`, read-direction, pull). Formation Flight needs a *third*,
**dispatch-direction** object (Tower → sortie, push). Three of its fields — `non_goals`, `drift_markers`,
`reference_frame` glossary — have **no carrier anywhere in the existing ontology**.

### Desired outcome
Every fan-out agent receives one Mission Brief. The orchestrator can construct it, the agent is forced to
report against it (via the Mission Report return schema), and the coherence gate can check conformance —
all from one typed object that travels into isolation.

---

## 2. Shape

### Approach
A typed object, JSON-Schema-defined (`formation/mission-brief.schema.json` is the **single source of
truth**; the `MissionBrief` dataclass in `formation/formation.py` is test-pinned to it — no parallel
hand-maintained definition). The orchestrator builds one brief per seam and serializes it into that
sortie's `agent()` prompt. The sortie returns a **Mission Report** (`formation/mission-report.schema.json`)
used as the Workflow `agent(prompt, {schema})` StructuredOutput.

### Two-plane placement
The Mission Brief is **ephemeral coordination state** — it belongs to *neither* plane of the two-plane
model (`models.py:5-9`). It is dispatch-direction, a sibling to the dispatch prompt, not to a Spec.
Forcing its fields into Spec frontmatter would pollute a persistent-plane artifact with per-dispatch
ephemera and break the two-plane separation DEC-013 names as core differentiation. So: **new type, not a
field on an existing one** — but it **composes by reference** with existing carriers wherever one exists.

### Fields — new vs. reference (don't re-encode paid substrate)

| Field | Kind | Carrier / meaning |
|---|---|---|
| `reference_frame` (glossary, canonical_terms, forbidden_synonyms) | **NEW** | The shared datum. Seed cheaply from `get_core` (`knowledge.py:1259`). Root anchor against vocabulary drift. |
| `invariants` | **NEW** | Must-remain-true constraints. Checked by gate Stage A. |
| `non_goals` | **NEW** | Explicit out-of-scope. No existing carrier — this is why `audit_chain` alone cannot see non-goal violations. |
| `drift_markers` | **NEW** | Per-seam drift definition; feeds the loop stop condition. |
| `intent` | ref | Parent `INT-…` (shared frame anchor + ON-trigger key). |
| `interface_contract` | ref | `CON-…`, the frozen seam (Work-Ontology L4, `ContractType.INTERFACE`). |
| `verification_rubric.verification_command` | ref | The Contract's existing `verification_command` (`models.py:291`). The gate RUNS it. |
| `trust_gate` / `lambda` | ref | Intent trust band (`trust_to_autonomy`) + per-product λ (`autonomy-flight-model §16`). |
| `isolation` / `model` | ref | Assigned by the governance matrix from `trust_gate × lambda`. |
| `lineage` (trace_id/span_id/parent_id) | ref | `make_event`/`TraceContext` (`models.py:178,198`). Observe-loop closure. |

### Boundaries
**In:** the typed brief + its return (Mission Report); construction-by-reference; serialization into a
dispatch prompt.
**Out:** a new datastore (the brief is ephemeral, not persisted as a first-class entity); a new lineage
scheme (reuse `make_event`); any change to the substrate-exposure (read) envelope.

### Key decisions (already made — do not revisit)
- JSON Schema is the source of truth; the dataclass is generated-conformant / test-pinned.
- Mission Brief is dispatch-direction and ephemeral; it is NOT a Spec/Contract field.
- `interface_contract`, `lambda`, `lineage`, `verification_command` compose **by reference**, never copy.
- Name = "Mission Brief" (grep-clean; "dispatch"/"flight"/"envelope" overloaded). "Clearance" noted as
  the civil-ATC alternative in DEC-014.

### Open questions
- Should `reference_frame.glossary` be inlined or referenced by a `get_core` call id? (Default: inline a
  bounded slice so the brief is self-contained in isolation.)

### Prior art (read before building)
- `formation/mission-brief.schema.json`, `formation/mission-report.schema.json`
- `servers/models.py` (Contract types, `make_event`, `TraceContext`)
- `spec/SPEC-substrate-exposure-envelope-extensions-DRAFT.md` (the read-direction envelope — the sibling)

---

## 3. Contract

### Done when
- [ ] `formation/mission-brief.schema.json` validates a hand-written example brief.
- [ ] The `MissionBrief` dataclass round-trips through the schema (test in `formation/test_formation.py`).
- [ ] A constructed brief embeds cleanly in an `agent()` prompt and the sortie returns a schema-valid
      Mission Report.
- [ ] Every reference field resolves to a real artifact (`INT-…`, `CON-…`, a product λ, a trace id).

### Smoke test
```
python3 -c "import json,jsonschema; jsonschema.validate(json.load(open('formation/example-brief.json')), json.load(open('formation/mission-brief.schema.json')))"
```

### Failure modes to watch
- **Triple-definition drift** (schema vs dataclass vs prose). Mitigation: schema is source of truth; the
  dataclass test is the catch-net.
- **Brief bloat** — if the brief becomes a tax to author, formation dies of friction. Keep it the
  shortest object that keeps a sortie coherent.
- **`non_goals` omitted** — the most common and most expensive omission; it is the field with no other
  home, so dropping it means the gate cannot catch non-goal violation.

### Observability
Each brief carries `lineage`; the sortie's events (`make_event`) and Mission Report flow to Witness. The
coherence gate's findings reference `brief_id`/`seam_id`.
