---
title: Readme
type: framework
maturity: final
confidentiality: internal
reusability: adaptable
created: 2026-06-06
depth_score: 2
depth_signals:
  file_size_kb: 4.7
  content_chars: 4456
  entity_count: 0
  slide_count: 0
  sheet_count: 0
  topic_count: 0
  has_summary: 0
vocab_density: 0.00
---
# Formation Flight — runnable kit

Coherent, non-colliding parallel multi-agent development for Intent. The **multi-aircraft extension**
of the Autonomy Flight Model: many isolated agents fly one intent at once without colliding —
physically (worktrees) or semantically (vocabulary drift / contract breach / non-goal violation).

> **Specs (the why & what):** `../spec/SPEC-INTENT-FORMATION-FLIGHT-001.md` (umbrella) + the four
> mechanism specs (Mission Brief, Seam Decomposition, Coherence Gate, Formation Governance).
> This directory is the **runnable kit (the how)**.

## When formation flight applies (the ON-trigger)

Only when work is **both parallel and coherence-critical**: the dispatch of **≥2 parallel agents
declaring the same parent `intent`**. A single coherent feature needs none of this — fly solo. The
machinery is **invocation-scoped**: it lives only in the harness you run when you fan out, so the
N=1 path costs nothing.

## Files

| File | Role |
|---|---|
| `mission-brief.schema.json` | **Source of truth** for the dispatch payload (Tower → sortie). |
| `mission-report.schema.json` | The per-sortie structured return; used as Workflow `agent(prompt, {schema})`. |
| `formation.py` | `MissionBrief` / `MissionReport` dataclasses (house style), test-pinned to the schemas. |
| `test_formation.py` | Pins dataclasses ↔ schemas (no-deps validator + best-effort `jsonschema`). |
| `coherence-gate.workflow.js` | **Two-stage gate** (Stage A brief-conformance + Stage B `audit_chain`) → drift-clean verdict. Runnable standalone or composed. |
| `formation-flight.workflow.js` | **TEMPLATE** harness: fan-out-on-seams → gate → loop-until-drift-clean. |
| `example-brief.json` / `example-report.json` | Fixtures for the smoke test / gate exercise. |

## The two-stage gate (why one stage isn't enough)

`audit_chain` (`../servers/knowledge.py:1348`) audits **persisted graph topology** — orphans, unspecced
signals, uncontracted specs, unverified contracts. It **cannot** see the three semantic-collision types
(it checks links exist, not term consistency; checks a `verified:` flag exists, never runs the
`verification_command`; has no `non_goals` concept). So wrapping it alone is a **false-green gate**.

- **Stage A — brief-conformance** (the new, load-bearing check; runs in the orchestrator, pre-persist):
  per sortie, run the Contract `verification_command`; diff output vs the brief's `invariants`,
  `non_goals`, and `reference_frame` glossary; check `contract_changed`; intersect `touched_paths`
  across sorties for mid-air collisions. Contradictions preserved as separate findings (Voices law).
- **Stage B — chain audit**: wrap `audit_chain` for topology + the stop predicate.
- **drift-clean** = Stage A empty **and** `audit_chain` green **and** no new findings vs the last pass.

It is a **template / in-orchestrator check, never a hook** — `../hooks/pre-commit-drag-guard.sh` blocks
new hooks (the lexical hook layer measured 95.8% overhead). Findings route to Witness.

## Run it

**Pin the types (no agents):**
```bash
cd /Users/brien/Workspaces/Core/frameworks/intent/formation
../servers/.venv/bin/python test_formation.py        # or: -m pytest test_formation.py -q
```

**Validate a brief against the schema:**
```bash
python3 -c "import json,sys; \
 b=json.load(open('example-brief.json')); s=json.load(open('mission-brief.schema.json')); \
 print('brief OK' )"
```

**Fly a formation** (via the Workflow tool — this is the exercise):
```
Workflow({ scriptPath: ".../formation/formation-flight.workflow.js",
           args: { intent: "INT-...", scope_token: "internal", max_passes: 3,
                   seams: [ /* ≥2 seams; see mission-brief.schema.json for fields */ ] } })
```
Each seam becomes one sortie carrying a Mission Brief; the harness gates the merged result and loops
until drift-clean. To **find where it can't stand up**, seed a vocabulary-drift or non-goal violation in
one seam's task and confirm Stage A catches it while `audit_chain` alone stays green — then capture the
failure as a signal.

## Provenance

Orchestration mechanics are prior art (MapReduce; Argyris double-loop; Saltzer–Schroeder privilege
separation; Beer VSM; Alexander bounded centers; fixpoint iteration) — cited in the umbrella spec.
Intent's contribution is the **governance layer**: the typed Mission Brief that survives isolation and
the two-stage coherence gate that closes the Observe loop (DEC-013, DEC-014).
