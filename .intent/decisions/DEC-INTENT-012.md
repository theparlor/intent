---
title: "Origin tracking on all knowledge artifacts — human | agent | synthetic"
id: DEC-INTENT-012
type: decision-atom
created: 2026-04-05
date_inferred: false
scope: Core/frameworks/intent — knowledge artifact provenance
status: ratified
ratified_at: 2026-04-05
ratified_by: "brien (2026-04-05; 4-gate pass: reversible / local / precedent / no info gap)"
gate_check:
  reversible: pass
  local: pass
  precedent: pass
  info_gap: pass
upstream_control_path: "Core/frameworks/intent/CLAUDE.md §Key Decisions #12; knowledge-engine/AGENTS.md schema; knowledge/ file templates"
catch_mechanism: "knowledge/ templates include origin: field; lint flags artifacts without origin tag"
pipeline_survival: "Frontmatter field survives all render cycles; lint enforces presence"
source: "2026-04-05; Ango (contamination mitigation)"
---

# Decision: Origin tracking on all knowledge artifacts — human | agent | synthetic

> Ratified 2026-04-05. All 4 autonomy-grant gates pass.

## Context

As AI agents compile and update knowledge artifacts, contamination risk grows — agent-synthesized content can displace human-observed evidence without a trace. Origin tracking enables contamination auditing: which claims are grounded in human observation vs. agent synthesis vs. synthetic generation.

## Decision

Every knowledge artifact carries an `origin:` field with one of three values: `human` (directly from human observation/interview), `agent` (LLM-compiled from source material), or `synthetic` (generated without primary sources). This field is required in all `knowledge/` artifacts.

## Scope

Governs all `knowledge/` artifacts (personas, journeys, DDRs, themes, domain models, design rationale). Does not govern `.intent/` work artifacts (signals, specs, etc.) which have different provenance needs.

## Alternatives Not Taken

| Alternative | Why not chosen | Reversibility if revisited |
|-------------|----------------|---------------------------|
| No origin tracking | Contamination undetectable at scale | L3 — retroactive tagging needed |
| Binary human/agent (no synthetic) | Loses signal on speculative artifacts | L4 |
| Confidence score instead | Doesn't capture provenance type, only certainty level | L3 |

## Reversibility

L4 — adding/changing origin field values is a template update + lint rule update.

## Ratification Action

`origin:` field added to all `knowledge/` templates. Lint detects missing origin fields. Three valid values: `human`, `agent`, `synthetic`. Cited from Ango's contamination mitigation research.
