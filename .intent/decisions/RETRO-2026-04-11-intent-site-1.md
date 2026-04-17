---
decision_id: RETRO-2026-04-11-intent-site-1
title: "Intent Site Synced to v1.0 Architecture"
date: 2026-04-11
status: accepted
source: retroactive-extraction
---

## Context

The Intent marketing/documentation site had fallen behind the product's architectural evolution. Multiple decisions (D7-D12), the three-layer architecture, Knowledge Engine separation, fourth MCP server, spec-shaping protocol, and federated KB had all been implemented in the product repo but not propagated to the site.

## Decision

Executed a comprehensive site sync to v1.0 architecture:

- **10 HTML pages updated** to reflect current architecture and terminology
- **5 governance docs updated** to align with product repo state
- **All 10 site contracts pass** — verified programmatically
- Three-layer architecture, Knowledge Engine separation, fourth MCP server, spec-shaping protocol, and federated KB all propagated to site content
- Decisions D7-D12 incorporated into relevant site pages
- `content-map.md` updated with 51+ new traceability entries linking site content to source-of-truth documents in the product repo

## Consequences

- Site now accurately represents the product as built
- Content-map.md provides full traceability from every site claim to its source document
- Future site updates have a clear baseline to diff against
