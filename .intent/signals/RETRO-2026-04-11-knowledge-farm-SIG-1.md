---
signal_id: RETRO-2026-04-11-knowledge-farm-SIG-1
title: "Mobile Access Gap: Knowledge Farm Is Desktop-Only Without VPS"
date: 2026-04-11
severity: medium
status: open
source: retroactive-extraction
---

## Signal

The Knowledge Farm (compiled persona knowledge, engagement data, research artifacts) is currently accessible only from desktop Cowork sessions via local MCP servers. Brien frequently wants to query persona perspectives from mobile Claude chat — this is currently impossible.

The $10/month VPS solution was designed in this session but not yet implemented. Until it is, the entire persona system is desktop-locked.

## Impact

Reduces the effective utility of the persona investment. A persona that can only be consulted when sitting at the desk is significantly less useful than one available anytime. Brien's consulting work happens across contexts — client sites, commutes, quick evening questions.

## Recommended Action

VPS deployment is the next infrastructure priority after Wave 1 extension enrichment completes. The architecture is designed (bearer token auth, federation boundaries, audit logging via observe layer). What remains is implementation and deployment.

## Triage, 2026-07-08

Disposition: still pending. Same finding as 2026-04-11-cowork-plugin-persona-access.md: the $10/month VPS deployment this signal calls the next infrastructure priority was never implemented. The persona system remains desktop/Cowork-session-bound; no hosted MCP server is reachable from mobile Claude chat today.
