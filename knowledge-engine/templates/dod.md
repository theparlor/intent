---
title: Definition of Done — Template
id: TEMPLATE-DOD
type: template
created: 2026-04-14
updated: 2026-04-14
version: 1.0
status: canonical
origin: brien-original
related_signals:
  - SIG-046
related_templates:
  - dor.md
  - dor-dod-library.md
---

# Definition of Done (DoD) — Template

## What Is a DoD?

A **Definition of Done** is an **exit gate**: a set of postconditions that must be verified as true before work on a spec, skill, engagement, or task may be declared complete. If any DoD item is unmet, the work is **not done** — regardless of what has been written, built, or shipped.

DoD is the answer to: *"Are we actually done?"*

It pairs with the Definition of Ready (DoR), which asks: *"Are we ready to start?"*

### DoD in the Intent Framework

In the Intent work ontology:

```
Signal → Intent → Spec → Contract → Capability → Feature → Product
                                                  ↑
                                          DoD gates the transition
                                          OUT of Execution (to Observe)
```

"Shipped to Workspaces" is not done. "Files written" is not done. Done means: committed, registered, tested, and documented. DoD is the difference between **shipped** and **abandoned**.

### Why DoD Prevents Silent Debt

The most common failure mode: declare something done because it "works," then never commit it, never register it, never test it in composition. Three months later, Brien can't find it, can't use it, can't chain it. It's lost.

DoD closes the gate at the moment it matters: before "complete" is said aloud.

---

## DoD Entry Format

Each DoD entry follows this structure:

```yaml
id: DOD-NNN
description: One-sentence assertion of the postcondition (must be verifiable)
verification_method: How to confirm this condition is met (file check, git command, output test, etc.)
must_be_true_to_close: true | false  # Default true. False only for stretch/aspirational items.
owner: agent | brien | both
```

### Field Guidance

| Field | Guidance |
|-------|----------|
| `id` | Sequential within this spec/context: DOD-001, DOD-002, ... |
| `description` | Write as an assertion in past tense or present state: "Code is committed to git." Not "Commit the code." |
| `verification_method` | Must be checkable without ambiguity. Examples: "git log shows commit", "skill name appears in registry SKILL.md files", "CONTEXT.md exists at skill dir", "Brien can invoke skill by trigger phrase in new session" |
| `must_be_true_to_close` | Default true. Set false for aspirational goals that improve quality but don't gate completion. Never use false to avoid hard verification. |
| `owner` | Who verifies: `agent` (mechanical check), `brien` (human review), `both` (agent checks mechanically, Brien confirms quality) |

---

## Authoring Guidance

### The gate is the gate

If something is listed as `must_be_true_to_close: true`, it CANNOT be overridden by saying "close enough" or "I'll do it later." If Brien approves a close without verifying, that's a governance failure to be captured as a signal — not a reason to soften the DoD.

### Write postconditions, not tasks

- BAD: "Commit the code to git"
- GOOD: "Code is committed to a managed git repo with a descriptive commit message"

### Separate "it exists" from "it works"

Two different conditions, both required:
1. "SKILL.md exists at the correct path" (structural)
2. "Skill activates on trigger phrase in a new session" (functional)

Don't collapse these into one item.

### Use the library first

Before writing custom DoD entries, check `dor-dod-library.md`. Canonical DoD exists for skill-build, spec-authoring, engagement-kickoff, persona-enrichment, and critique-panel. Start from the canonical; add only what's specific to this work.

---

## Template: DoD Block for a Spec

```markdown
## Definition of Done

Work on this spec is complete ONLY when ALL items below are verified:

| ID | Condition | Verification | Must Be True | Owner |
|----|-----------|--------------|--------------|-------|
| DOD-001 | Code/files committed to managed git repo | `git log` shows commit with file paths | Yes | agent |
| DOD-002 | Skill discoverable in registry | Skill name appears in `skills-engine` SKILL.md registry | Yes | agent |
| DOD-003 | CONTEXT.md present at skill directory | File exists at skill path | Yes | agent |
| DOD-004 | Memory updated if load-bearing | Memory file exists or n/a declared explicitly | Yes | both |
| DOD-005 | At least one composition scenario tested | Test output documented or test session noted | Yes | agent |
| DOD-006 | Signal captured if process-changing | Signal filed in `.intent/signals/` or n/a declared | Yes | agent |

**Blocked:** "Complete" cannot be declared until all `must_be_true_to_close: true` items are verified.
```

---

## Example DoD: Skill Build for `expense-narrative`

```markdown
## Definition of Done

| ID | Condition | Verification | Must Be True | Owner |
|----|-----------|--------------|--------------|-------|
| DOD-001 | `expense-narrative/SKILL.md` committed to `skills-engine` repo | `git show HEAD -- platforms/claude-code/financials/expense-narrative/SKILL.md` | Yes | agent |
| DOD-002 | Skill registered: appears in skills registry scan | Glob `**/financials/expense-narrative/SKILL.md` returns file | Yes | agent |
| DOD-003 | `CONTEXT.md` present at `financials/` category level | File exists | Yes | agent |
| DOD-004 | Memory file `project_fieldbook.md` updated with new skill reference | File updated with expense-narrative entry | Yes | agent |
| DOD-005 | Composition test: skill invoked with mock Harvest data, output is narrative | Test session transcript or output snippet | Yes | both |
| DOD-006 | Signal captured: SIG-NNN filed if skill changes Brien's expense workflow | Signal file exists at `.intent/signals/` | Yes | agent |
```

---

## Relationship to Contracts

DoD works alongside spec contracts (CON-NNN) but is distinct:

| | Contracts (CON-NNN) | Definition of Done (DOD-NNN) |
|---|---|---|
| **What they assert** | Invariants the output must satisfy | Postconditions for the work to be "complete" |
| **Scope** | Behavior / quality of the artifact | Deployment / registration / documentation state |
| **Verification** | Can be checked against the artifact | Checked against the system state (git, registry, memory) |
| **Failure mode** | Artifact doesn't meet spec | Artifact exists but is orphaned, unregistered, or undocumented |

Use both. Contracts test the **what**; DoD tests the **where it landed**.

---

## Cross-References

- DoR template: `dor.md`
- Canonical library: `dor-dod-library.md`
- Build-intake skill: `Core/products/skills-engine/platforms/claude-code/meta/skill-intake/SKILL.md`
- Intent work ontology: `Core/frameworks/intent/spec/work-ontology.md`
