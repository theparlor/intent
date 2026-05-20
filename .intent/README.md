---
title: .intent/ Directory Index
type: index
created: 2026-05-20
---

# .intent/ Directory Index

This directory is Intent's dogfood — the framework uses its own loop to govern its own development.
All work artifacts live here: captured signals, proposed intents, shaped specs, decisions, and events.

## Subdirectory Map

| Directory | Purpose |
|-----------|---------|
| `approvals/` | IntentApproval entities — L0 cross-human action gate. Lifecycle: pending → approved/denied/expired. Schema: `methodology/meta/approval-gate.md`. Template: `approvals/_TEMPLATE.md`. |
| `clusters/` | Signal clusters — groups of related signals identified via pattern analysis. 6 clusters filed (2026-03-30). Template: `templates/cluster.md`. |
| `config/` | Intent config files — `approval-rules.yml` (L0 gate action types), future `config.yml` (local vs hosted mode selector). |
| `decisions/` | Decision log — all architectural and methodology decisions with rationale. Source of truth for "why we chose X". See also `decisions.md` in this directory. |
| `discovery/` | Discovery artifacts — research notes, interview summaries, and early-stage exploration. Pre-signal material that hasn't been processed into formal signals yet. |
| `elevations/` | Elevation grants — time-boxed auto-approve tokens that temporarily elevate an L0 action to L3/L4. Lifecycle: pending → active → expired. Schema: `methodology/meta/approval-gate.md`. Template: `elevations/_TEMPLATE.md`. |
| `events/` | Event log — `events.jsonl` append-only OTel-compatible event stream. 15 event types across Execute and Observe phases. GitHub Action emits on every push. |
| `intents/` | Proposed intents — "what needs to change" statements promoted from signals. Template: `templates/intent.md`. |
| `methodology/` | Methodology modules — cross-cutting governance docs (approval gate, spec-shaping protocol, signal-stream policy). These document the loop's own operating rules. |
| `plans/` | Execution plans — scoped work plans for specific execution windows. Distinct from specs (which define what to build) and intents (which state what needs to change). |
| `signals/` | Captured signals — 130+ signals across 2026-03-28 through 2026-05-20. Mixed naming: legacy `SIG-NNN` sequential, date-slug `YYYY-MM-DD-slug`, and `RETRO-` prefix for retrospectives. ULID migration pending (SPEC-003). |
| `specs/` | Shaped specs — agent-ready specifications that link back to intents and decisions. Template: `templates/spec.md`. Status lifecycle: draft → shaped → approved → ratified. |
| `templates/` | Artifact templates — signal, intent, spec, contract, cluster templates for consistent structure. Knowledge artifact templates live in `../knowledge-engine/templates/`. |

## Key Files (root of .intent/)

| File | Purpose |
|------|---------|
| `INTENT.md` | Project manifest — the top-level intent for this repo. What Intent is trying to do, at the framework level. |
| `decisions.md` | Decision log shortcut — same content as `decisions/` but flat file for quick scanning. |

## Naming Conventions

- **Signals:** prefer ULID format `SIG-{26-char-ulid}.md` per SPEC-003 (2026-04-09). Legacy `SIG-NNN` and `YYYY-MM-DD-slug` names remain valid via backward-compat regex. RETRO signals use `RETRO-{date}-{slug}.md`.
- **Intents:** `INT-{NNN}.md`
- **Specs:** `SPEC-{NNN}-{slug}.md` or `{date}-{slug}.md` for plan-type specs
- **Approvals:** `APR-{NNN}.md`
- **Elevations:** `ELV-{NNN}.md`

## Health Indicators

A healthy `.intent/` has:
- Signals captured within the last 14 days (active notice)
- No signal stuck at `status: captured` for >30 days without triage
- Specs at `status: approved` linked to active execution
- `events.jsonl` updated on every push (GitHub Action health)
- Decisions log current with any recent architectural choices
