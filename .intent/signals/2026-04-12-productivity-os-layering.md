---
id: SIG-035
title: Intent framework needs explicit layering model for Personal through Enterprise productivity operating systems
timestamp: 2026-04-12T10:00:00Z
source: cowork-session
author: brien
confidence: 0.9
trust: 0.9
autonomy_level: L2
status: resolved
upstream_control_path: "Core/frameworks/intent/spec/SPEC-productivity-os-layers.md (### L1 through ### L6 sections)"
catch_mechanism: "explicit six-layer altitude model with scope, autonomy default, and knowledge architecture defined per layer, closing the L2/L5 gaps this signal named"
verification_command: "grep -n '^### L[0-9]:' /Users/brien/Workspaces/Core/frameworks/intent/spec/SPEC-productivity-os-layers.md"
cluster: architecture
---

# SIG-035: Productivity OS Layering — Personal Through Enterprise

## What was noticed

Intent currently describes itself as a "team operating model for AI-augmented product teams." But the actual work happening in the repo spans at least six distinct organizational altitudes — and Intent's architecture applies differently at each one.

**The layers that already exist, implicitly:**

| Layer | Altitude | What Brien is building here |
|-------|----------|----------------------------|
| L1 | Personal OS | Persona library, Knowledge Farm, Cowork plugin, auto-memory |
| L2 | Independent Builders | Not explicitly addressed — GAP |
| L3 | Team OS | Intent methodology, four-persona spec shaping |
| L4 | Team of Teams | Federation model, team boundaries |
| L5 | Department OS | Not explicitly addressed — GAP |
| L6 | Enterprise OS | Transformation Operating System, Intent site, consulting deliverables |

The three-layer architecture (Knowledge Base → Transformation OS → Software) is **layer-agnostic** — it works at every altitude. But the loop cadence, trust model, persona usage, knowledge architecture, and tooling all change as you move from L1 to L6. That variation is nowhere formalized.

## Evidence from adjacent work

Several existing workstreams are building L1-L2 tooling without a formal model connecting them to L3-L6:

- **Persona library and Knowledge Farm** — L1 personal productivity infrastructure. Brien invokes "what would Teresa say?" as a solo practitioner, not as a team ritual.
- **Cowork plugin (SIG-030)** — L1 mobile/dispatch access to Intent's MCP servers and persona critique skills.
- **Auto-memory and task management** — L1 personal continuity across sessions.
- **AI PM OS course concept** — L1-L2 teaching individual practitioners to run their own operating system.
- **Hermes/Obsidian system** — L1 personal knowledge management that feeds the Knowledge Farm.
- **Dex Horthy's "harness engineering"** — L1-L2 pattern where individuals build personal AI agent harnesses.

Meanwhile, the Intent site and consulting practice target L3-L6 buyers — team leads, product organizations, enterprise transformation sponsors. The gap between "personal AI productivity" and "enterprise transformation operating system" is the product story that connects all of Brien's work into a coherent offering.

## Why this matters

Without an explicit layering model:

1. **Product story is fragmented** — the persona work feels disconnected from the methodology work, even though they're the same architecture at different altitudes.
2. **Consulting positioning is unclear** — clients can't see how Intent scales from one practitioner to their whole organization.
3. **L2 and L5 are invisible gaps** — no one is designing for independent builders (freelancers, open source contributors) or department-level governance.
4. **Cross-layer data flows are undefined** — how does an L1 observation become an L3 team signal? How does L6 governance constrain L3 autonomy?

## Relationship to existing architecture

The three-layer architecture, the loop, trust/autonomy, federation, and the Knowledge Engine all exist. What's missing is the **altitude dimension** — a formal model for how these mechanisms vary across organizational scale. Think of it as the Z-axis that Intent's current X-Y (loop phase × work ontology) doesn't yet account for.

This is analogous to Team Topologies (Pais/Skelton) providing the organizational altitude model for platform engineering — Intent needs its equivalent for AI-augmented product work.

## Triage, 2026-07-08

Disposition: control exists now, verified live. spec/SPEC-productivity-os-layers.md now has fully written sections for all six altitudes this signal named as gaps, including the two it specifically flagged as missing: L2 (Independent Builders, line 181) and L5 (Department OS, line 343), alongside L1/L3/L4/L6. The Z-axis (altitude) model this signal called for is built.
