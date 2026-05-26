---
title: Definition of Ready — Template
id: TEMPLATE-DOR
type: template
created: 2026-04-14
updated: 2026-04-14
depth_score: 4
depth_signals:
  file_size_kb: 5.9
  content_chars: 5579
  entity_count: 0
  slide_count: 0
  sheet_count: 0
  topic_count: 0
  has_summary: 0
vocab_density: 0.36
version: 1.00
status: canonical
origin: brien-original
related_signals:
  - SIG-046
related_templates:
  - dod.md
  - dor-dod-library.md
---
# Definition of Ready (DoR) — Template

## What Is a DoR?

A **Definition of Ready** is an **entry gate**: a set of preconditions that must be verified as true before work on a spec, skill, engagement, or task may begin. If any DoR item is unmet, work is explicitly blocked — not deferred, not skipped.

DoR is the answer to: *"Are we ready to start this?"*

It pairs with the Definition of Done (DoD), which asks: *"Are we done?"*

### DoR in the Intent Framework

In the Intent work ontology:

```
Signal → Intent → Spec → Contract → Capability → Feature → Product
                  ↑
              DoR gates the transition INTO Spec execution
              DoD gates the transition OUT of Spec (to Observe)
```

Every spec should declare its DoR inline, and every repeating work type has canonical DoR definitions in `dor-dod-library.md`.

### Why DoR Prevents Costly Failures

Without DoR, teams start work before architectural decisions are locked, before the target repo is identified, before the composition audit is done. This produces:
- Orphaned builds (code written but never committed)
- Reinvented patterns (built a primitive that already existed)
- Abandoned work (started without a deployment plan; never finished)

DoR catches these **at inception, not at delivery**.

---

## DoR Entry Format

Each DoR entry follows this structure:

```yaml
id: DOR-NNN
description: One-sentence statement of the precondition (must be verifiable)
verification_method: How to confirm this condition is met (file check, git command, Brien confirm, etc.)
blocked_if_unmet: true | false  # Almost always true; false only for informational items
owner: agent | brien | both
```

### Field Guidance

| Field | Guidance |
|-------|----------|
| `id` | Sequential within this spec/context: DOR-001, DOR-002, ... |
| `description` | Write as an assertion: "The composition audit has been completed." Not "Do the audit." |
| `verification_method` | Must be checkable by an agent or Brien without ambiguity. Examples: "File `composition-audit.md` exists at skill dir", "git status shows target repo initialized", "Brien has confirmed architecture in session" |
| `blocked_if_unmet` | Default true. Set false only for informational items (e.g., "nice-to-have context"). Informational items NEVER block work. |
| `owner` | Who verifies: `agent` (can be checked mechanically), `brien` (requires human judgment), `both` (agent checks first, Brien confirms) |

---

## Authoring Guidance

### Write conditions, not tasks

DoR items are **states**, not actions.

- BAD: "Run the composition audit"
- GOOD: "Composition audit has been completed and classification decision is recorded"

### Make conditions observable

If the condition can't be checked with a file existence test, a git command, or a direct question, it's too vague.

- BAD: "The team understands the scope"
- GOOD: "INTENT.md at skill directory declares scope and composition strategy"

### Keep the list short

A DoR with 10 items will be ignored. Target 3–6. If you need more, consider whether the work type needs to be broken down first.

### Link to the DoD library

Before writing custom DoR entries, check `dor-dod-library.md`. If a canonical DoR exists for your work type (skill-build, spec-authoring, engagement-kickoff), use it. Only write custom entries for conditions specific to this particular spec.

---

## Template: DoR Block for a Spec

```markdown
## Definition of Ready

Before execution begins on this spec, ALL items below must be verified:

| ID | Condition | Verification | Blocked If Unmet | Owner |
|----|-----------|--------------|------------------|-------|
| DOR-001 | Composition audit completed; build classified as extend/compose/new/don't-build | File `composition-audit.md` exists at skill dir | Yes | agent |
| DOR-002 | Target git repository identified and initialized | `git status` returns valid repo | Yes | agent |
| DOR-003 | Deployment plan documented (where code lands, how it registers) | Declared in spec or INTENT.md | Yes | both |
| DOR-004 | DoD entries for this spec are declared and understood | DoD section present in this spec | Yes | agent |

**Blocked:** Work cannot begin until all `blocked_if_unmet: true` items are confirmed.
```

---

## Example DoR: Spec for a New Skill Build

Context: Brien has asked for a skill that synthesizes Harvest time data into a narrative expense report.

```markdown
## Definition of Ready

| ID | Condition | Verification | Blocked If Unmet | Owner |
|----|-----------|--------------|------------------|-------|
| DOR-001 | Composition audit complete — `expense-narrative` classified vs existing fieldbook skills | `composition-audit-expense-narrative.md` exists | Yes | agent |
| DOR-002 | Target repo identified: `skills-engine` (not a new repo) | Confirmed by agent check of `Core/products/skills-engine/.git` | Yes | agent |
| DOR-003 | Harvest MCP connector confirmed available in session environment | Test call to `harvest_list_time_entries` succeeds | Yes | agent |
| DOR-004 | Deployment plan: skill will live at `skills-engine/platforms/claude-code/financials/expense-narrative/` | Declared above | Yes | agent |
| DOR-005 | DoD for `skill-build` applied (from `dor-dod-library.md`) | DoD section below populated | Yes | agent |
```

---

## Cross-References

- DoD template: `dod.md`
- Canonical library: `dor-dod-library.md`
- Build-intake skill: `Core/products/skills-engine/platforms/claude-code/meta/skill-intake/SKILL.md`
- Intent work ontology: `Core/frameworks/intent/spec/work-ontology.md`
