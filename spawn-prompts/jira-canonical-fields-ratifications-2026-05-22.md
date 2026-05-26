---
title: Spawn Prompt — Jira canonical-fields ratifications from design-artifact work
id: SPAWN-JIRA-CANONICAL-FIELDS-2026-05-22
type: spawn-prompt
created: 2026-05-22
depth_score: 4
depth_signals:
  file_size_kb: 9.5
  content_chars: 8463
  entity_count: 0
  slide_count: 0
  sheet_count: 0
  topic_count: 0
  has_summary: 0
vocab_density: 0.00
target: jira-migration-canonical-session
status: ready-to-execute
upstream_control_path: Core/frameworks/intent/spawn-prompts/jira-canonical-fields-ratifications-2026-05-22.md (this file)
catch_mechanism: "the canonical files at working/jira-migration/canonical/fields/ are the authoritative landing zone; the design artifacts at deliverables/design-artifacts/pdf-exports/ are the downstream consumer that must stay consistent"
pipeline_survival: "self-contained pasteable artifact; references files by exact path; states what to update and why; lists every ratification so nothing carried in conversation gets lost"
usage: "cat ~/Workspaces/Core/frameworks/intent/spawn-prompts/jira-canonical-fields-ratifications-2026-05-22.md | pbcopy   Then paste into a fresh Claude Code session pointed at the jira-migration canonical area. Pin Sonnet; Opus only if a controlled-values.md edit needs schema-level reasoning."
---
# Ratifications to land in the Jira canonical-fields library

## Why this prompt exists

While building the bug-anatomy and per-team scenarios guides in the design-artifacts track, a few field-level decisions either got clarified for the first time or surfaced as needing explicit codification. Those decisions now live in the design artifacts (PDFs the field will actually read) and must be reflected in the canonical library so the two never drift.

The design artifacts are at:
- `Work/Consulting/Engagements/Subaru/deliverables/design-artifacts/pdf-exports/bug-anatomy.pdf` (2 pages)
- `Work/Consulting/Engagements/Subaru/deliverables/design-artifacts/pdf-exports/bundle-{mtec,snetcm,techshare,scom}.pdf` (9–11 pages each)

The canonical library is at:
- `Work/Consulting/Engagements/Subaru/working/jira-migration/canonical/fields/controlled-values.md` (authoritative field-value definitions)
- `Work/Consulting/Engagements/Subaru/glossary.md` (engagement glossary — pointer to canonical)
- `Work/Consulting/Engagements/Subaru/deliverables/curriculum/Agile Academy/Decision Records - MARS-v-0-3.docx` (Decision Record register)

## Ratification 1 — Work Classification: optional at create, audit-required by close (NOT a Jira gate)

**Decision:** Work Classification is **optional at creation** and **must be populated by close**, but enforcement of "populated by close" is **discipline-and-audit-based, not a Jira workflow gate**.

**Rationale (preserve verbatim in the DR):** If we force people to populate Work Classification at create or via a hard gate, filers who don't understand the taxonomy will pick incorrectly. Wrong values are worse than absent values for a taxonomy field — they corrupt the analytical signal. The audit-by-close model lets an informed party (Engineering at triage or close) classify when they have context, without blocking the filing flow.

**Where to land this:**
1. `controlled-values.md` — Work Classification field section: change the enforcement note from "optional · taxonomy" to "Optional at create. Required to be populated by close, audit-enforced (not a Jira validator)."
2. Add or update a Decision Record (likely DR-XXX, check the register for the next free number) titled something like *"Work Classification enforcement: audit-required by close, not gated"*. Include the rationale verbatim above.
3. `glossary.md` — update the Work Classification entry to mention the audit-by-close model.

**Where the design artifacts already reflect this:** `bug-anatomy.pdf` page 1, callout #2 now reads "Work Classification — optional at create · audit-required by close" (committed as part of this design-track build).

## Ratification 2 — Diagnosis: 8 values with single-line definitions

**Decision:** Diagnosis is a multi-select field on Bug. Optional. Eight controlled values:

| Value | Working definition |
|---|---|
| Regression | used to work, no longer does |
| Design Issue | the original design was flawed |
| Legacy | older code with known constraints |
| Environmental | config, infra, deploy, or data |
| Security | exposure or vulnerability |
| Performance | too slow or too resource-hungry |
| Accessibility | barriers for assistive-tech users |
| Integration | fails at a system boundary |

**Status:** Already encoded in `controlled-values.md` per the 2026-05-18 field-enforcement ratification. The definitions above are the short-form definitions used in the field-definitions page of the team scenarios guides. Confirm `controlled-values.md` matches these working definitions, or extend `controlled-values.md` to include them as the user-facing short form.

## Ratification 3 — Impact (I1–I4) and Urgency (U1–U4) — draft definitions used in artifacts

**Status: DRAFT for canonical adoption.** The design artifacts ship working definitions for I1–I4 and U1–U4 because the team needed *some* anchor text to learn the model. These definitions may or may not match what the SOA-IT Baseline ratifies. If the canonical has stricter or different definitions, the design artifacts should be updated to match — flag any divergence in your response.

**Impact (single-select, one of four):**
- I1 — Critical: service down, data loss, blocks many users
- I2 — High: core feature broken for some users
- I3 — Medium: workaround exists, minor impact
- I4 — Low: cosmetic or minor inconvenience

**Urgency (single-select, one of four):**
- U1 — Immediate: must act now
- U2 — High: fix this sprint
- U3 — Medium: next sprint
- U4 — Low: backlog, address eventually

**Where to land this:** Confirm/adjust against `controlled-values.md`. If the canonical doesn't yet have value-level descriptions for I1–I4 and U1–U4, propose adopting (or refining) these as the working short-form definitions.

## Ratification 4 — Field role-attribution (who fills in what)

This is already in the design artifacts and should be confirmed in the canonical:

- **Impact and Urgency are input opinions.** Recorded by whoever finds the Bug. Engineering validates and may refine at triage. They are NOT Engineering-only.
- **Priority is Engineering's synthesis** from Impact + Urgency + sequencing. Not a 1-to-1 mapping from Urgency.
- **Disposition is gate-required.** Set on the To Do → working-state transition. Single-select.
- **Diagnosis fills in during work.** Multi-select, optional, but recommended.
- **Reporter is auto-set.** No one chooses it.

Cross-check against `controlled-values.md` and the DR register. If any of these are still ambiguous in the canonical, propose tightening.

## Ratification 5 — Reporter is informed of resolution at Done

**Decision:** The Reporter is **notified of resolution** when the Bug reaches Done. They confirm the behavior is resolved. This was added to the orientation grid in the scenarios guides — previously the Reporter row was empty after To Do, which under-represented the closure loop.

**Where to land this:** This is more a workflow-behavior decision than a field-value decision. Probably belongs in a DR or in the lifecycle documentation. Not a `controlled-values.md` change. Just make sure the lifecycle docs reflect that "Reporter notified at Done" is part of the model.

## Deliverables expected from this Jira-canonical session

1. **`controlled-values.md` updated** with the Work Classification enforcement clarification (Ratification 1).
2. **One or more Decision Records added or updated** in the register, especially for Work Classification audit-enforcement (Ratification 1) and the Reporter-notified-at-Done behavior (Ratification 5).
3. **Glossary updated** if Work Classification's entry doesn't reflect the audit-by-close model.
4. **Divergence report** — any place where the design artifacts state something inconsistent with the canonical. List exact file paths and the specific text that diverges. The design artifacts will be updated to match the canonical (not the other way around).
5. **Confirmation of I1–I4 / U1–U4 working definitions** — either adopt them as the canonical short-form, or supply the existing canonical definitions so the design artifacts can be updated.

## Open questions for the operator (Brien)

(These are honest L0 — only Brien can answer.)

- Should the I1–I4 / U1–U4 working definitions be promoted to canonical, or do you want SOA-IT to weigh in first?
- Is "audit-required by close" the right language, or do you prefer "expected by close, audit-reviewed"? (The artifacts currently use "audit-required by close.")
- Does the Reporter-notified-at-Done need a DR, or is it implicit in the workflow doctrine?

## Closure-DoD for the canonical-session

upstream_control_path: this spawn prompt; the canonical files at `working/jira-migration/canonical/fields/` are the authoritative landing zone

catch_mechanism: the divergence report (deliverable #4) is the catch-net — if any drift between canonical and design artifacts is missed, it surfaces there

pipeline_survival: every ratification is named, sourced, and routed to a specific file; the design artifacts that depend on these ratifications are listed at the top of this prompt so the canonical session can verify consistency

---

*Prepared by the design-artifacts session, 2026-05-22. Generated alongside the bug-anatomy v12 build and the four team scenarios guides. The design artifacts now show Work Classification as "optional at create · audit-required by close" — the canonical needs to match.*
