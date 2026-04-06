---
id: INT-004
title: "Workspace Lifecycle Hygiene: triage stale working artifacts across engagements"
status: accepted
proposed_by: brien
proposed_date: 2026-04-06T14:00:00Z
accepted_date: 2026-04-06T14:00:00Z
signals: [SIG-031]
specs: [SPEC-002]
owner: brien
priority: next
product: workspace-operations
---

# Workspace Lifecycle Hygiene

## Problem
Engagement workspaces accumulate stale content in working/ directories (drafts, notes, collaborative docs) with no systematic review process. The placement resolver (AGENTS.md) governs where files GO but not when files LEAVE. Without hygiene, working/ becomes a junk drawer within weeks.

## Desired Outcome
A periodic skill that scans engagement working/ directories, identifies stale artifacts, diffs drafts against delivered versions, flags unique vs. redundant content, and presents a triage assessment for Brien's decision. Never auto-deletes — always presents for human judgment.

## Scope
- Covers: working/drafts/, working/notes/, working/collaborative/
- Engagement-scoped: runs per-engagement or across all active engagements
- Connects to: AGENTS.md lifecycle rules (§5), Knowledge Engine lint (staleness detection)
- Does NOT cover: from-client/ (immutable), deliverables/ (finished), knowledge/ (separate lint)

## Success Criteria
Brien opens a session, runs workspace-hygiene, gets a clear "here's what's stale, here's what has unique content, here's what's safe to archive" report. Decision takes 5 minutes, not 30.
