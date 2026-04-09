---
title: Workspace Hygiene — Contracts
type: contracts
created: 2026-04-06
summary: "Verifiable assertions for the workspace-hygiene skill. Each contract is testable — it either passes or fails."
depth_score: 3
depth_signals:
  file_size_kb: 3.5
  content_chars: 3333
  entity_count: 0
  slide_count: 0
  sheet_count: 0
  topic_count: 0
  has_summary: 1
vocab_density: 0.31
domain: workspace-operations
spec: SPEC-002
---
# Workspace Hygiene — Contracts

> Every contract is a verifiable assertion. Run these to check if the workspace-hygiene skill is working correctly. Contracts reference the spec they verify. CON-WS-* prefix (WS = Workspaces domain, distinct from CON-KE-* Knowledge Engine domain).

---

## CON-WS-001: Working Directory Coverage
**Spec:** SPEC-002 §Shape — three subdirectories

**Assertion:** The workspace-hygiene skill scans all three working/ subdirectories: drafts/, notes/, and collaborative/. No subdirectory is silently skipped.

**Verification:** After running the skill on a test engagement, verify that the triage report contains sections for all three subdirectories, even if empty.

**Status:** Testable after skill creation

---

## CON-WS-002: Unique Content Detection
**Spec:** SPEC-002 §Shape — diff phase

**Assertion:** For every file in working/drafts/ that has a counterpart in deliverables/, the skill identifies content present in the draft but absent from the delivered version. "Unique content" means text blocks, sections, or data that were cut during the draft→deliverable transition.

**Verification:** Create a test draft with 3 sections. Create a delivered version with only 2 of those sections. Run the skill. Verify the triage report flags the missing section as unique content.

**Status:** Testable after skill creation

---

## CON-WS-003: Triage Classification
**Spec:** SPEC-002 §Contract — acceptance criteria

**Assertion:** Every file in working/ receives exactly one classification: STALE (no unique content, older than threshold), UNIQUE (has content not in delivered version), ACTIVE (modified within threshold), or ARCHIVE (stale but preserving as record of process). No file is left unclassified.

**Verification:** Run the skill on an engagement with mixed file ages. Verify every file appears in the triage report with one classification.

**Status:** Testable after skill creation

---

## CON-WS-004: Non-Destructive Operation
**Spec:** SPEC-002 §Contract — failure modes

**Assertion:** The workspace-hygiene skill NEVER deletes, moves, or modifies any file without Brien's explicit approval in the triage output. The skill produces a report. Brien acts on the report. The skill does not act on its own recommendations.

**Verification:** Run the skill. Verify that no file system changes occur. Verify the output is a report, not a set of completed actions.

**Status:** Testable after skill creation — most critical contract

---

## CON-WS-005: Configurable Staleness Threshold
**Spec:** SPEC-002 §Shape — staleness threshold

**Assertion:** The staleness threshold (default: 14 days since last modification) is configurable per invocation. Setting a different threshold changes which files are classified as STALE vs ACTIVE.

**Verification:** Run the skill with threshold=7 and threshold=30 on the same engagement. Verify that the STALE/ACTIVE classifications change appropriately.

**Status:** Testable after skill creation

---

*Workspace Hygiene Contracts v1.0 — 2026-04-06*
*5 contracts. All testable after skill creation.*
