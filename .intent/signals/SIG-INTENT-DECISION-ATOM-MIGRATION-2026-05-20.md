---
id: SIG-INTENT-DECISION-ATOM-MIGRATION-2026-05-20
title: "21 Key Decisions migrated to decision atoms (DEC-INTENT-001..021)"
type: signal
status: resolved
confidence: 1.0
trust: 1.0
autonomy_level: L4
source: wave-5-framework-audit
created: 2026-05-20
resolved: 2026-05-20
upstream_control_path: ".intent/decisions/DEC-INTENT-001.md through DEC-INTENT-021.md; CLAUDE.md §Key Decisions cross-reference note"
catch_mechanism: "Future Intent decisions write as atoms first, prose second (or both). Atom template at knowledge-engine/templates/decision-atom.md. Prose in CLAUDE.md §Key Decisions is not deleted — both forms coexist."
pipeline_survival: "yes — all 21 atoms git-tracked in .intent/decisions/; CLAUDE.md cross-reference note links prose to atoms"
---

# Signal: 21 Key Decisions migrated to decision atoms

## Context

Wave 5 framework audit noted: Intent framework had 14 (actual count: 21) Key Decisions in CLAUDE.md as prose, not `.intent/decisions.md` atoms. Not a blocking gap at canonical stage, but canonical form of decisions should eventually migrate to decision atoms for full chainability.

## What Was Done

Converted all 21 prose decisions from `CLAUDE.md §Key Decisions` into individual decision atoms at `.intent/decisions/DEC-INTENT-001.md` through `DEC-INTENT-021.md`.

Each atom includes:
- Full frontmatter (id, type, created, scope, status, ratified_at, ratified_by, gate_check, upstream_control_path, catch_mechanism, pipeline_survival)
- Context, Decision, Scope, Alternatives Not Taken, Reversibility, Ratification Action sections
- [unknown] fields marked explicitly where prose did not record the information

CLAUDE.md §Key Decisions updated with cross-reference note pointing to the atoms. Prose preserved — both forms coexist.

## Atom Index

| ID | Title |
|----|-------|
| DEC-INTENT-001 | Name the product "Intent" |
| DEC-INTENT-002 | Methodology first, tool second |
| DEC-INTENT-003 | Open development — signals, decisions, architecture all public |
| DEC-INTENT-004 | File-native, git-tracked, OTel-compatible — no lock-in |
| DEC-INTENT-005 | Target practitioner-architects first |
| DEC-INTENT-006 | Specs as contracts, not stories |
| DEC-INTENT-007 | Staged GTM — thought leadership → methodology → tooling |
| DEC-INTENT-008 | Four-product framing — Notice, Spec, Execute, Observe are distinct products |
| DEC-INTENT-009 | Three-layer architecture — compiled knowledge base + transformation OS + spec/code |
| DEC-INTENT-010 | Compilation over retrieval — knowledge base compiles understanding once |
| DEC-INTENT-011 | Double-loop learning — Observe updates domain understanding, not just execution |
| DEC-INTENT-012 | Origin tracking on all knowledge artifacts — human | agent | synthetic |
| DEC-INTENT-013 | Federated knowledge base — Core is universal substrate, engagements are bounded instances |
| DEC-INTENT-014 | Two products, not one — Intent (methodology) and Knowledge Engine (product) are distinct |
| DEC-INTENT-015 | Engagement rollout order — Subaru → F&G → ASA → Cargill → Footlocker |
| DEC-INTENT-016 | Knowledge Engine as new MCP server — intent-knowledge on port 8004 |
| DEC-INTENT-017 | Retroactive enrichment is suggested, not automatic cascade |
| DEC-INTENT-018 | Redaction at tool level — MCP server applies confidentiality projection automatically |
| DEC-INTENT-019 | Spec shaping is self-prompting through four personas |
| DEC-INTENT-020 | ULID-based ID generation for all entity IDs |
| DEC-INTENT-021 | 12-factor agent pattern integration — 5 gaps resolved, event catalog expanded |

## [unknown] Count

Fields marked [unknown] in atoms (prose did not specify):
- DEC-INTENT-015: catch_mechanism field — prose recorded rollout order but no mechanism for drift detection

All other atoms had sufficient prose to populate all required fields.

## DoD

- upstream_control_path: `.intent/decisions/DEC-INTENT-001.md` through `DEC-INTENT-021.md` + `CLAUDE.md §Key Decisions` cross-reference note
- catch_mechanism: future Intent decisions write as atoms first, prose second (or both); atom template at `knowledge-engine/templates/decision-atom.md`
- pipeline_survival: yes — atoms git-tracked; CLAUDE.md note links to atoms; prose preserved
