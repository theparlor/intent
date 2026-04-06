---
id: SPEC-002
title: "Workspace Lifecycle Hygiene: triage stale working artifacts"
version: "1.0"
status: draft
intent: INT-004
trust_score: 0.78
autonomy_level: L3
shaped_by: [architect, product, quality, agent]
personas_queried: [PER-006]
decisions_referenced: []
contracts: [CON-WS-001, CON-WS-002, CON-WS-003, CON-WS-004, CON-WS-005]
created: 2026-04-06
---
# SPEC-002: Workspace Lifecycle Hygiene

---

## Intent (Pass 2: ◇ Product Leader)

**Why this matters:** Engagement workspaces accumulate stale drafts, notes, and collaborative docs in working/ directories. The new placement resolver (AGENTS.md) tells files where to GO but not when to LEAVE. Without a hygiene process, working/ becomes a junk drawer. Brien noted during the April 6 design session: "we can separately establish a process to ferret through drafts or prior versions that have gone stale to truly assess if there is any unique material in there for anything not needed as a record of delivery content to client."

**Who benefits:** Brien (primary user), Dean Gabbert (if Fieldbook expense system adopts same structure). Any consultant using the Workspaces engagement model.

**Behavioral change:** Instead of periodic manual archaeology through cluttered directories, Brien runs a skill that presents a triage report. Decision time drops from 30+ minutes of manual inspection to ~5 minutes of reviewing a structured assessment.

**Key outcome:** A triage report per engagement showing: stale artifacts, unique-content flags, safe-to-archive recommendations, and total working/ health score.

---

## Shape (Pass 1: △ Architect)

### Approach

The skill operates in three phases:
1. **SCAN** — Walk working/{drafts,notes,collaborative}/ for each engagement. Collect file metadata (name, size, modified date, age).
2. **DIFF** — For files in working/drafts/, find counterparts in deliverables/ by name similarity or content overlap. Diff to identify unique content in the draft not present in the delivered version.
3. **ASSESS** — Classify each file: STALE (no unique content, >N days old), UNIQUE (has content not in delivered version — keep or promote), ACTIVE (recently modified, skip), ARCHIVE (stale but worth preserving as record).

### Boundaries

- NEVER auto-deletes. Always produces a triage report for Brien's decision.
- Operates on engagement directories only (Work/.../Engagements/[Client]/working/).
- Does NOT touch from-client/ (immutable), deliverables/ (finished), knowledge/ (has its own lint).
- Staleness threshold: configurable, default 14 days since last modification.
- Scope: single engagement (default) or all active engagements (flag).

### Key Decisions Made

- Assessment is advisory, never destructive (Brien decides)
- Diff uses content similarity, not just filename matching (a draft might be renamed before delivery)
- "Unique content" means material in the draft that does NOT appear in any delivered artifact — it was cut, not evolved
- Archive = move to working/archive/ (new subdirectory), not delete

### Decisions for the Agent

- Whether to integrate with Knowledge Engine lint (could surface "this stale note has insights worth compiling into a persona/theme")
- Whether to produce a signal (SIG-*) when working/ exceeds a clutter threshold

### File Layout

```
Core/skills-engine/platforms/claude-code/operations/workspace-hygiene/SKILL.md
```
No additional code files — this is an agent skill (instructions for Claude), not a CLI tool.

---

## Contract (Pass 3: ○ Quality Advocate)

### Acceptance Criteria

Each criterion maps to a workspace hygiene contract:

**AC-1: Scan covers all working subdirectories (CON-WS-001)**
```
Given: an engagement directory with working/ subdirectories
When: workspace-hygiene skill is invoked for that engagement
Then: all three subdirectories (drafts/, notes/, collaborative/) are scanned
  AND every file in those subdirectories appears in the triage report
```

**AC-2: Diff identifies unique content in drafts (CON-WS-002)**
```
Given: a file exists in working/drafts/
When: a counterpart exists in deliverables/ (by name similarity or content overlap)
Then: the diff identifies content present in the draft but absent from the delivered version
  AND that content is flagged as "unique" in the triage report
```

**AC-3: Every file is classified (CON-WS-003)**
```
Given: workspace-hygiene has scanned an engagement's working/ directories
When: the triage report is generated
Then: every file is classified as exactly one of: STALE | UNIQUE | ACTIVE | ARCHIVE
  AND the classification rationale is included for each file
```

**AC-4: No destructive action without approval (CON-WS-004)**
```
Given: workspace-hygiene has produced a triage report
When: the report recommends archiving or removing files
Then: no file is deleted or moved until Brien explicitly approves the action
  AND the report presents recommendations, not executed changes
```

**AC-5: Staleness threshold is configurable (CON-WS-005)**
```
Given: workspace-hygiene is invoked
When: a custom staleness threshold is provided (e.g., 7 days, 30 days)
Then: the threshold overrides the default 14-day value
  AND all staleness classifications use the provided threshold
```

### Failure Modes

| Failure | Impact | Mitigation |
|---------|--------|-----------|
| False positive: marks active working doc as STALE | Brien loses trust in triage accuracy | ACTIVE threshold checks both modification date AND whether Brien has referenced it recently |
| False negative: misses unique content because diff is too coarse | Valuable material gets archived without review | Content-level diff, not just filename match |
| Scope creep: starts triaging from-client/ or knowledge/ | Violates immutability guarantees on protected directories | Hard-coded directory scope (working/ only) |

---

## Agent Notes (Pass 4: ◉ Agent Readiness Assessment)

### Trust Score Breakdown

| Factor | Score | Rationale |
|--------|-------|-----------|
| Clarity of intent | 0.9 | Brien stated the need explicitly |
| Technical feasibility | 0.8 | File scanning + content diff are straightforward |
| Scope containment | 0.85 | Clear boundaries (working/ only) |
| Risk of harm | 0.1 | Advisory only, never destructive |
| Reversibility | 0.95 | Archive is reversible; no deletion |
| **Composite** | **0.78** | **L3: agent executes, Brien reviews output** |

### Required Reads Before Execution

1. `Workspaces/AGENTS.md` (§4 schema, §5 lifecycle rules)
2. Target engagement CONTEXT.md
3. Target engagement deliverables/ listing (for diff targets)

### Ambiguity Flags

| Flag | Resolution | Status |
|------|-----------|--------|
| "Recently referenced" is undefined — should this check git log, session history, or just file modification time? | **Open** | Needs Brien's input |
| Whether working/archive/ should be a new standard subdirectory in the engagement schema | **Open** | Needs Brien's input |

### Events to Emit

| Event | When |
|-------|------|
| `workspace.hygiene.scanned` | When scan completes for an engagement |
| `workspace.hygiene.triage_ready` | When triage report is ready for Brien's review |
