---
id: RETRO-2026-04-12-humanlayer-approval-DEC-6
type: decision
source: session-analysis
decided: 2026-04-12
topic: humanlayer-approval
status: decided
---

# Formalize Auto-Accept Rules as Executable Config

## Context

Brien's L0-L4 autonomy levels are documented in CLAUDE.md as prose. HumanLayer has programmatic bypass rules (`isEditTool()`, `DangerouslySkipPermissions`). The gap: Intent's autonomy levels should be executable, not just instructional.

## Decision

Define auto-accept rules as structured config that maps action types to autonomy levels. L4 actions auto-approve with audit comment. L0 actions always require human. L2 actions require human above threshold. This makes CLAUDE.md governance machine-readable.

## Alternatives Considered

1. **Keep prose-only governance** — rejected; not auditable, not composable
2. **Binary approve/deny per tool** — rejected; too coarse, doesn't capture the L0-L4 gradient

## Consequences

- Requires auto-accept rules config (YAML or similar)
- Gate skill reads config to determine whether to block or auto-approve
- CLAUDE.md prose governance becomes the human-readable documentation of the executable config
- Config is the source of truth; CLAUDE.md is the explanation
