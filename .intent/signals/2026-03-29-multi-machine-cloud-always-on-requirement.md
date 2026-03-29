---
id: SIG-013
timestamp: 2026-03-29T23:00:00Z
source: conversation
author: brien
confidence: 0.95
trust: 0.25
autonomy_level: L1
status: active
cluster: autonomous-infrastructure
parent_signal:
related_intents: [deployment-topology, autonomous-execution]
---
# Multi-machine cloud requirement: can’t rely on local laptop being always connected

Brien’s primary machine travels with him — goes on planes, gets closed in a bag, loses internet. Signal processing agents can’t run on a machine that goes offline unpredictably.

This creates a hard requirement: **the agent processing layer must run somewhere always-on.** Options:

1. **GitHub-native:** Signals committed to repo trigger GitHub Actions that run enrichment/processing agents. Always available, no infrastructure to manage.
2. **Cloud service:** Hosted Intent service that agents connect to via API. More capability but more to build.
3. **Secondary machine:** Brien has a second machine he could dedicate, but it lacks his organizational skills, library index, and file sync.

The multi-machine problem also surfaces a **file sync requirement**: Brien’s library organizational skills need to work across machines, likely via GitHub-based sync or a shared storage layer.

## Implication for Architecture

The signal capture → enrichment → routing → execution pipeline must be decomposable:
- **Capture** can happen anywhere (Cowork, iOS, web browser, CLI)
- **Processing** must happen somewhere always-on (GitHub Actions or cloud)
- **Execution** happens in Claude Code sessions (can be on any machine with repo access)
- **Observe** must be accessible from any device (web dashboard)

This reinforces the config-driven deployment model from SIG-012: same tools, different backends, configurable per-machine.
