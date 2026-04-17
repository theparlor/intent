---
decision_id: RETRO-2026-04-11-plugin-1
title: "Cowork Plugin Architecture: Three Layers with Persona Skills"
date: 2026-04-11
status: accepted
source: retroactive-extraction
---

## Context

Intent's four MCP servers (notice, spec, observe, knowledge) needed to be accessible from Cowork sessions. Two approaches were considered: manual MCP server registration (requiring per-machine config) or a Cowork plugin that bundles everything for portability.

## Decision

Designed a Cowork plugin architecture with three layers:

1. **MCP Servers:** The four Intent MCP servers (notice, spec, observe, knowledge) bundled as plugin connectors. Plugin packaging handles registration and configuration.

2. **Persona Skills:** The four Intent personas (Cagan, Torres, Patton, Seiden, etc.) exposed as invokable advisor skills within Cowork. Each persona skill loads the persona's enriched profile and can provide perspective on product decisions.

3. **Expert Critique / ARB Review:** A composite multi-perspective skill that invokes multiple personas simultaneously to provide architectural review board-style feedback on a proposed decision or design.

Plugin route chosen over manual MCP registration for portability — the plugin can be installed on any machine with a single command and carries its own configuration.

## Consequences

- Intent becomes usable from any Cowork session without manual setup
- Personas are accessible as first-class advisor skills, not just data files
- The ARB review skill demonstrates the compositional potential of multiple personas
- Plugin packaging is the distribution mechanism for the entire Intent toolchain
