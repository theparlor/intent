---
id: SIG-031
title: Intent MCP servers lack production-grade contract rigor (typed validation, idempotency, structured errors)
timestamp: 2026-04-12T01:00:00Z
source: external-article
author: brien
confidence: 0.85
trust: 0.85
autonomy_level: L2
status: active
cluster: bootstrap-tooling
referenced_by:
  - "Rohit @rohit4verse, 'How to Build a Production-Grade AI Agent' (Feb 2026), Principle 2"
  - "Dex Horthy, 12 Factor Agents, Factor: Tools are structured output"
---

# SIG-031: Contract Rigor Gap in Intent MCP Servers

## What was noticed

Rohit's Principle 2 ("Contracts Everywhere") establishes a standard for production agent tool design: Pydantic/Zod typed inputs with server-side validation, idempotency keys for retry safety, versioned schemas, and structured error payloads that enable the LLM to self-correct and retry.

Intent's four MCP servers (notice 8001, spec 8002, observe 8003, knowledge 8004) accept inputs but do not currently implement:
- Strict server-side validation before execution
- Structured error responses with field-level detail for LLM retry
- Idempotency keys for write operations (create_signal, create_spec, ingest_event)
- Schema versioning for safe API evolution

## Evidence

Rohit: "the llm does not actually understand your api, it simply pattern matches. strict schemas constrain this pattern matching to safe, mathematically valid operations."

Current Intent MCP tools use Pydantic models for input but lack the error-response contract that closes the retry loop. A malformed create_signal call fails silently or crashes rather than returning a structured payload the agent can parse and fix.

## Implication

Before the Intent MCP servers are deployed as a hosted Knowledge Farm or registered in the Cowork plugin, they need a validation pass against Rohit's Principle 2 standard. This is a prerequisite for trust levels L3-L4 (agent executes with monitoring / full autonomy).

## Triage, 2026-07-08

Disposition: still pending. Grepped Intent's MCP servers for idempotency keys or structured field-level error responses on write operations (create_signal, create_spec, ingest_event); none found. Note this is distinct from CON-009 (INGEST Idempotency), which governs entity-level ingestion semantics, not MCP tool-call retry safety, so that later contract does not close this gap.
