---
title: "Name the product 'Intent'"
id: DEC-INTENT-001
type: decision-atom
created: 2026-03-28
date_inferred: false
scope: Core/frameworks/intent — product naming
status: ratified
ratified_at: 2026-03-28
ratified_by: "brien (Cowork session 2026-03-28; 4-gate pass: reversible / local / precedent / no info gap)"
gate_check:
  reversible: pass
  local: pass
  precedent: pass
  info_gap: pass
upstream_control_path: "Core/frameworks/intent/CLAUDE.md §Key Decisions #1; README.md; all repo references"
catch_mechanism: "Naming appears in every file header, repo name, and README — drift is immediately visible"
pipeline_survival: "Encoded in repo name (theparlor/intent) and all documentation; survives render cycles"
source: "Cowork session 2026-03-28"
---

# Decision: Name the product "Intent"

> Ratified 2026-03-28. All 4 autonomy-grant gates pass.

## Context

Working name throughout initial development was "Dev OS." This sounded like DevOps infrastructure tooling and confused positioning. A name was needed that IS the thing — not a metaphor for it.

## Decision

Use the single word "Intent" as the product name. The name describes exactly what the layer produces: the crystallized why behind what teams are building.

## Scope

All product naming: repo name, documentation, marketing site, CLI tools, MCP server names, signal files.

## Alternatives Not Taken

| Alternative | Why not chosen | Reversibility if revisited |
|-------------|----------------|---------------------------|
| Dev OS | Confused with DevOps infrastructure tooling | L4 — file renames + repo rename |
| Frame | Too generic, no semantic anchor | L4 |
| Premise | Abstract, doesn't name the output | L4 |
| Lucid | Generic SaaS name, no differentiation | L4 |
| Upstream | Directional metaphor, not the thing itself | L4 |
| Intent Operating Flow | Verbose, acronym (IOF) weak | L4 |

## Reversibility

L4 — requires comprehensive rename across repo, files, and site. Done once in 2026-03-28 session (68KB JSX file pushed, CLI cleanup script run). High friction but technically reversible.

## Ratification Action

Triggered comprehensive rename: repo name, file names, file contents, memory files, cross-references. All "Dev OS" references replaced.
