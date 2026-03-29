---
id: SIG-014
timestamp: 2026-03-29T22:20:00Z
source: conversation
author: brien
confidence: 0.95
trust: 0.45
autonomy_level: L2
status: active
cluster: bootstrap-tooling
parent_signal:
related_intents: [signal-capture, autonomous-execution]
---
# Agent context limits cause content drift during multi-file pushes

During v0.6.0 development, delegating a multi-file GitHub push to a sub-agent resulted in every file being rewritten with fabricated content. The agent replaced the 617-line CLI with a 211-line simplified version, swapped signal IDs between files, rewrote all signal body text, and reported success. Root causes:

1. **Payload size exceeds tool limits.** The 18-file push payload was ~69KB / 23K tokens — beyond the Read tool's 10K token limit and too large for reliable agent context handling.
2. **Agent content drift.** When an agent can't fit all source content in context, it generates plausible-looking replacements rather than failing explicitly. The output looks correct at a glance but is semantically wrong.
3. **No verification in the push path.** The push succeeded at the API level (files were created/updated) but there was no content hash check or diff verification after the push.
4. **Recovery cost is high.** Manual recovery required reading each file from GitHub, comparing against source, and pushing corrections in small batches. For 18 files, this consumed significant session context.

## Implications for Intent's Autonomous Execution

This is a concrete instance of why the trust framework and autonomy levels exist. A push operation should have been L3 (agent executes, human monitors) but the tooling didn't support verification. The system needs:

- **Content hash verification** after every push (compare SHA of intended vs actual)
- **Batch size limits** in the agent handoff protocol (max N files per push, based on total token count)
- **Explicit failure mode** — agents should error rather than fabricate when content exceeds context
- **Disambiguation signal generation** — when an agent can't complete a task faithfully, it should emit a signal explaining what it couldn't do, rather than producing plausible-looking wrong output

## Trust Factors

- Clarity: 0.9 (problem is well-observed and reproducible)
- Blast radius: 0.4 (affects all multi-file operations, not just signals)
- Reversibility: 0.6 (recoverable via git history, but costly)
- Testability: 0.5 (can write verification checks, but root cause is in agent behavior)
- Precedent: 0.2 (first time this specific failure mode was observed)
