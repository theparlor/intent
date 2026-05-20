---
title: "Redaction at tool level — MCP server applies confidentiality projection automatically"
id: DEC-INTENT-018
type: decision-atom
created: 2026-04-06
date_inferred: false
scope: Core/frameworks/intent — confidentiality enforcement architecture
status: ratified
ratified_at: 2026-04-06
ratified_by: "brien (2026-04-06; 4-gate pass: reversible / local / precedent / no info gap)"
gate_check:
  reversible: pass
  local: pass
  precedent: pass
  info_gap: pass
upstream_control_path: "Core/frameworks/intent/CLAUDE.md §Key Decisions #18; knowledge-engine/spec/redaction.md"
catch_mechanism: "MCP server applies projection at response time; confidentiality flag in artifact frontmatter; redaction spec defines projection rules"
pipeline_survival: "Server-level enforcement survives any client change; redaction is applied at MCP response boundary"
source: "2026-04-06"
---

# Decision: Redaction at tool level — MCP server applies confidentiality projection automatically

> Ratified 2026-04-06. All 4 autonomy-grant gates pass.

## Context

Brien's Knowledge Farm contains engagement-specific knowledge that is confidential (NDA-governed). When agents query the knowledge base, the response must not leak confidential content to contexts where it doesn't belong. Requiring Brien to manually flag confidentiality on every query is fragile.

## Decision

The MCP server (`intent-knowledge`) applies confidentiality projection automatically at response time, based on the engagement context of the requesting session. Brien doesn't need to remember to apply confidentiality flags on individual queries — the tool enforces it.

## Scope

Governs all Knowledge Engine MCP server responses. Defined in `knowledge-engine/spec/redaction.md`.

## Alternatives Not Taken

| Alternative | Why not chosen | Reversibility if revisited |
|-------------|----------------|---------------------------|
| Brien manually flags each query | Fragile; human error introduces leak risk | L3 — revert to client-side |
| Confidentiality at storage level (encrypted per engagement) | Higher complexity; blocks legitimate cross-engagement synthesis | L2 |
| No redaction (public knowledge only in KE) | Defeats the purpose of engagement-specific knowledge | L2 |

## Reversibility

L3 — server-level enforcement is the only wired path. Removing it would require client-side confidentiality enforcement and Brien awareness training.

## Ratification Action

`knowledge-engine/spec/redaction.md` defines projection rules. MCP server applies projection at response boundary based on engagement context. Confidentiality flag in artifact frontmatter drives projection decisions.
