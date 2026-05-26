---
id: SIG-035
title: Security posture reframe — redaction is narrow export-layer, not the model; 4-layer stance (at-rest + access control + audit/signal + export redaction)
date: 2026-04-21
status: open
category: architecture
severity: high
related:
  - Core/reference/SHARING_AND_REDACTION_SCHEMA.md (2026-03-25 draft, redaction-only, never implemented)
  - CLAUDE.md Autonomy Grants (external communication L0 — access-control analog)
  - SIG-034 (entire.io partial landing — parallel rigor gap)
  - SIG-036 (audit-catchnet symptom — same upstream discipline root)
  - memory/feedback_audit_vs_writethrough.md (canonical — advisory ≠ enforced)
---

# SIG-035 — Security posture reframe (4-layer stance)

## Origin

During the 2026-04-21 Intent rigor audit kickoff, Brien flagged: *"we do need some form of redaction and protection for all knowledge farms including any queries we run against them."*

Initial agent framing: redaction-first — add sharing-tier enforcement, redact at query time, gate exports. Brien **reframed** directly:

> "we might be missing a point if we redact a knowledge farm that we intend to use for a client we will end up losing value when it is likely our better move is to understand, define and implement a security posture even if it just encrypt disk at rest and keep it locked. if we expose a knowledge farm we need to consider what our credentials, rights, access and permissions stance and model will be"

## The misframe being corrected

`Core/reference/SHARING_AND_REDACTION_SCHEMA.md` (2026-03-25 draft) treats **redaction as the primary protection model** — sharing_tier taxonomy (open/internal/confidential/restricted), 4 redaction actions, 5 audience profiles, dual-pattern enforcement (extraction-time + display-time).

**Never implemented.** No classifier, no `redacted_export.py`, no `AUDIENCES.yml`. The schema itself is the only artifact — a draft that hasn't been executed against.

Beyond implementation status: **redaction at query time destroys the value** for the intended consumer. If a client engagement needs a knowledge farm, redacting content on the query path makes the farm useless *for the engagement it exists to serve*. Redaction belongs in the **export path** (content leaving the trust boundary), not the query path.

## The reframe: 4-layer security posture

| Layer | Concern | Current state | Primary gap? |
|---|---|---|---|
| **A. At-rest encryption** | Disk-level protection of stored material | FileVault likely on (verify); macOS Keychain + SSH keys for credentials | No — baseline exists |
| **B. Access control** | Credentials, rights, permissions — who/what may read each farm under which engagement | Implicit, no declared model | **Yes.** Primary gap — cross-engagement bleed, agent exfiltration paths undefined |
| **C. Audit + signal** | What queries ran, by whom/what, against which farm; query log feeds content-discovery signal (per Brien's original insight) | Essentially none | **Yes.** Primary gap — Brien's own signal-driving use case unsupported |
| **D. Export redaction** | Narrow: content leaving trust boundary (client deliverable, external share) | SHARING_AND_REDACTION_SCHEMA.md draft | Narrow — Layer D only, was previously misframed as universal |

**Layer B and C are the real gaps.** Layer D is narrow. Layer A is baseline hygiene (verify and patch).

## Sub-project #6 phase decomposition

Accepted sequencing: **(a) → (c) → (d) → (b)**.

| Phase | Work | Why this order |
|---|---|---|
| **(a) Understand** | Asset inventory of knowledge farms; threat model; use-case enumeration; current-posture audit (FileVault, Keychain, existing access surface) | Load-bearing — Brien's own language was "understand, define, implement." Skipping risks 10x over/under-sizing. |
| **(c) Access model** | Credentials / rights / permissions / who-can-read-which-farm model | Addresses the two live risks (cross-engagement bleed, agent exfiltration) |
| **(d) Audit + signal layer** | Query-log capture surface; content-discovery signal pipeline | Depends on (c) to define actors; is the layer Brien wants instrumented |
| **(b) At-rest supplemental** | Per-farm supplemental encryption *above* FileVault if threat model demands | Defense-in-depth; threat-model-derived; last because A is already non-zero |

## Program context: 6-sub-project sequencing

Accepted full sequencing for the rigor audit program:

1. **#6 Security Posture Phase (a) Understand** — this sub-project, first, before exposing more knowledge farms
2. **#5 entire.io install + propagate** (D-scope: Core + frameworks) — per SIG-034
3. **#2 Coding-practices propagation** — DoR/DoD, audit-vs-writethrough, sibling-over-parent-child, decisioning discipline, quality-baseline inviolability, aliasing first-class
4. **#1 Intent framework rigor audit** — with current practices in hand (from #2) and clean observability (from #5)
5. **#3 + #4 parallel** — Witness forensics/event-tagging/drift pipeline (per SIG-WITNESS-001); Dashboards (Grafana Intent Observe + Witness forensics surface)

## Why #6 is first

Knowledge farms (Cast registry, library-index, corpus material) are already valuable internal state; they will gain value as more is added — *including content that is engagement-confidential*. Every addition without a posture compounds the gap. The right move is to answer the posture question before the next ingestion wave, not after.

## Follow-up

- Design doc: `Core/frameworks/intent/spec/2026-04-21-rigor-audit-program-design.md` (program overview + sub-project #6 Phase (a) detail)
- Downstream: the Intent-ification queue (13 Core frameworks missing `.intent/`) should be triaged through this posture lens — some are substrate, some are products, some may need engagement-scoping
- `SHARING_AND_REDACTION_SCHEMA.md` retained as Layer D input; de-promoted from "universal model"
