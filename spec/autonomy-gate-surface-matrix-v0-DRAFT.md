---
title: Autonomy Gate Surface Matrix — execution surfaces × modes × deterministic preconditions
id: SPEC-INTENT-AUTONOMY-SURFACE-MATRIX-001
status: draft
scope: framework
plane: bridge
date: 2026-05-26
updated: 2026-05-26
author: "intent framework (elevated from prior-Claude v0.1 via ingestion 2026-05-26)"
source_artifact: Core/frameworks/intent/raw/competitors/2026-05-25-prior-claude-source-artifacts.md (Artifact 3)
sibling: SPEC-INTENT-AUTONOMY-FLIGHT-MODEL-001
related:
  - Core/frameworks/intent/spec/autonomy-flight-model-v1-DRAFT.md
  - Core/frameworks/intent/spec/autonomy-grant-enforcement.md
  - Core/frameworks/methodology-library/meta/signal-scoring.md
  - .intent/signals/SIG-2026-05-26-flight-model-ingestion.md
relates_to: [trust-formula, contract, L0-L4, hooks]
ratification_dependencies:
  - flight-model v1 ratification (this matrix' floor values assume forward-fit λ from flight model)
  - surface-coverage audit (Claude-in-Chrome, MCP fabric, plugin-list inventory all need to be mapped to a row)
---

# Autonomy Gate Surface Matrix (v0 DRAFT)

> Status: DRAFT. Companion to SPEC-INTENT-AUTONOMY-FLIGHT-MODEL-001.
> Flight model = HOW the gate computes (forces, λ, envelope).
> This matrix = WHERE the gate applies (surface × mode → autonomy floor + deterministic precondition).
> These are SIBLING specs and must ratify together.

## §1 How to read this matrix

- **Autonomy floor (contained)** assumes the listed containment posture is in place. Strip the containment and drop one or two levels — containment is the lever that *buys* autonomy without lowering the harm bar.
- **Deterministic precondition (hook)** is the *law* layer: it fires regardless of the trust score. Trust governs the ceiling (how much autonomy you grant); the hook governs the floor (what is forbidden until a precondition holds). A failed hook blocks the action even at L4.
- Every surface splits into **read vs. mutate** — the gate behaves very differently across that line, and collapsing them is the most common design error.
- Today's v1 trust formula has *no value term and no detection-latency term*. Until v2 (flight model) lands, treat these floors as a caution-biased baseline to be loosened deliberately via shadow-autonomy calibration, not as settled safe limits.

## §2 The matrix

| #    | Surface    | Mode                                 | Inherent blast radius | Containment posture (the lever)                          | Autonomy floor (contained) | Deterministic precondition (hook)                            |
| ---- | ---------- | ------------------------------------ | --------------------- | -------------------------------------------------------- | -------------------------- | ------------------------------------------------------------ |
| 1    | Filesystem | read                                 | low                   | path allowlist, no symlink escape                        | L1                         | path ∈ allowlist; resolved real-path stays inside root       |
| 2    | Filesystem | write / edit                         | medium                | workspace sandbox; all targets git-tracked               | L2                         | inside workspace root; file is git-tracked (recoverable); not matching protected globs (`.env`, `**/secrets/**`, CI config) |
| 3    | Repo / git | read / clone                         | low                   | read-only token                                          | L1                         | token scope is read-only                                     |
| 4    | Repo / git | commit to branch                     | low–med               | feature branch only, never protected                     | L2                         | target branch ∉ protected set; no `--force`; commit signed   |
| 5    | Repo / git | push / open PR                       | medium                | PR + required review + CI gate                           | L3                         | targets a PR, not direct-to-main; merge blocked until CI green + human approve |
| 6    | Terminal   | read / inspect                       | low                   | non-mutating command class                               | L1                         | command ∈ read-only allowlist (`ls`, `cat`, `git status`, …) |
| 7    | Terminal   | mutate (install / build / exec / rm) | high                  | ephemeral/disposable container + snapshot                | L3                         | running in disposable env; rollback point exists; command ∉ denylist (`rm -rf /`, `curl … \| sh`, credential reads) |
| 8    | Database   | read                                 | low–med               | read replica + row/column scoping                        | L2                         | connection uses read-only role/replica; query has `LIMIT`; restricted columns require explicit grant |
| 9    | Database   | write / migrate                      | high                  | transaction + dry-run plan + fresh backup; staging first | L3 (L4 only with gate)     | wrapped in transaction w/ rollback; migration has a down-migration; backup age < N min; applied to staging before prod |
| 10   | Browser    | navigate / read (public)             | low                   | no stored credentials attached                           | L2                         | no authenticated session bound; destination ∈ domain allowlist |
| 11   | Browser    | authenticated action                 | high                  | non-prod tenant / sandbox account                        | L3                         | acting against non-prod tenant **or** explicit per-action human confirm; destructive/financial endpoints require L4 + human |
| 12   | Network    | outbound egress                      | medium (exfil)        | egress proxy + domain allowlist                          | L2                         | destination ∈ allowlist; payload scanned for secrets/PII before send |

## §3 Brien-specific overrides observed in practice

These deviate from the matrix above because Brien's autonomy grants are not generic — they are scoped to his specific actor model (solo + theparlor + 1099 + Workspaces-local). The matrix is the *generic* floor; Brien's `CLAUDE.md` autonomy grants are the actual operating point.

| Surface | Mode | Generic floor | Brien-observed | Why |
|---|---|---|---|---|
| Repo / git | commit | L2 | **L4** | theparlor solo repos — feedback_commit_autonomy memory (2026-05-19) — public-domain material, git-reversible, solo user population |
| Repo / git | push | L3 | **L4** in solo-owned repos | same — recalibrated 2026-05-19 from earlier L0-on-push framing |
| Filesystem | write | L2 | **L4** within Workspaces | autonomy-grant per CLAUDE.md "File creation within Workspaces: L4" |
| Slack / Email / Calendar (cross-human) | any mutate | L2 | **L0** | autonomy-grant per CLAUDE.md "Cross-human communication: L0" — the boundary is whether another human gets notified or has to act |

The pattern: solo-blast-radius surfaces get L4 grants; cross-human-notification surfaces stay L0. The matrix needs an explicit `actor_population` containment field to model this — added as §6 ratification dependency.

## §4 Missing facets this matrix exposes (feed back into the flight-model spec)

1. **Strategic value / upside** — the accelerator. Lets high-value work earn *investment in containment* rather than only earn more brakes. Without it the gate operationalizes caution, not strategy. (Addressed in flight-model §1.)
2. **Detection latency** — distinct from reversibility. "How fast will we know it broke" deserves its own term; a reversible-but-silent failure beats an irreversible-but-loud one in danger, not safety. (Addressed in flight-model §2 Lift composition.)
3. **Containment posture as input** — blast radius should be the *contained* radius, since containment is engineerable. Reward the posture; don't penalize the raw task. (Addressed in flight-model §5.)
4. **Actor competence / earned trust** — accrue trust to the *actor*, not just the task, so agents can graduate (Cagan's earned autonomy). (Addressed via the §3 actor-scoped overrides; needs formalization as the `actor` dimension in the deterministic decision step of flight-model §4.)
5. **Uncertainty / variance** — carry the spread, not just the mean. Route high-variance to a cheap probe (ephemeral wiki), not to default human escalation. (Addressed in flight-model §10 — panel composition produces variance.)

## §5 Find-the-ledge protocol (calibration, not nerve)

- **Shadow autonomy:** run the agent at *floor + 1*, dry-run/proposal-capture only; log the would-be action via Witness; diff against human-approved ground truth. Promote the floor only after agreement on safe-calls crosses threshold. This is the OVS drift-monitor calibration pattern generalized.
- **Reversibility as budget:** treat snapshots / transactions / flags / undo logs as spend that moves the ledge outward — manufacture reversibility, don't merely score it.
- **Spend saved caution on Observe:** every second shaved off time-to-detect earns a notch of looseness at the gate. Loose gate + tight loop > tight gate + loose loop. (Brien has the tight loop already — Witness + drift-monitor + closure-discipline + autonomy-grant-stop-check; the gate is currently the slow side.)

## §6 Surface-coverage audit dependencies (must clear before status → accepted)

The 12 rows above are starter coverage. The full surface inventory must add:

1. **Claude-in-Chrome MCP** (`mcp__claude-in-chrome__*`) — browser-control row. The current Row 10/11 is generic browser; needs CIC-specific containment (tabs context, no auto-submit on forms, link-suspicion rule from CLAUDE.md).
2. **Computer-use MCP** — desktop-control row. Needs tier-specific rows (read tier / click tier / full tier per the SessionStart computer-use instructions).
3. **All MCP fabric surfaces from the deferred-tools list** — Slack, Gmail, Calendar, GitHub, Jira, Notion, Linear, Asana, Atlassian, Google Workspace, etc. Each needs read/mutate rows + cross-human-notification flag.
4. **Plugin-list shopping-cart surfaces** (per the Reddit "9 plugins" analysis) — Context7, GitHub MCP, Playwright, Filesystem MCP, Sequential Thinking, Browser Tools, Database MCP, Terminal, Memory Plugins. Most map to existing rows; verify coverage.
5. **Witness ports** (`ingest_otlp`, `ingest_jsonl`, `tag_source_system`, `query`, `signal_emit`, `lineage`). Read vs mutate split per port.

## §7 What this spec is NOT

- This matrix is not a substitute for the deterministic preconditions implemented in hooks. The hooks ARE the precondition layer. This matrix documents what each hook should check; the hook code (`Core/frameworks/intent/hooks/`) is the source of truth.
- This matrix is not a replacement for v1 trust-formula scoring. It is the surface-level floor that the flight model's autonomy-band computation must respect.
- This matrix is not engagement-scoped. Engagement-specific overrides (e.g., Subaru Premium Jira surfaces) live in `Work/.../Engagements/[Client]/glossary.md` or engagement-specific spec.
