# Opportunity Solution Tree Template — Torres Format

> Teresa Torres' Opportunity Solution Tree (OST) is the canonical format for turning interview signals into actionable opportunity maps. Source: Continuous Discovery Habits (2021).

## The structure

```
                    [DESIRED OUTCOME]
                           |
        +------------------+------------------+
        |                  |                  |
   [Opportunity 1]    [Opportunity 2]    [Opportunity 3]
        |                  |                  |
    +-------+          +-------+          +-------+
    |       |          |       |          |       |
 [Sub-Op] [Sub-Op]  [Sub-Op] [Sub-Op]  [Sub-Op] [Sub-Op]
    |       |          |       |          |       |
  [Sol]   [Sol]      [Sol]   [Sol]      [Sol]   [Sol]
    |       |          |       |          |       |
 [Test]  [Test]     [Test]  [Test]     [Test]  [Test]
```

## Key principles (from Torres)

1. **Outcome first, not output.** The root of the tree is the outcome you want to drive, not the product you want to ship.
2. **Opportunities come from interviews.** Every opportunity is grounded in at least one verbatim quote from a discovery interview.
3. **Solutions come AFTER opportunities.** Do not populate solutions until opportunities are validated. Most methodology failures come from jumping to solutions.
4. **Assumption tests, not experiments.** Each solution has a set of assumptions that must be true. Test the assumptions, not the solution.
5. **The tree is living.** It grows, prunes, and reshapes as new interviews come in.

## Template

```markdown
---
id: DOM-spec-pain-OST
version: 0.1-wave1-draft
status: draft
source: external-discovery-wave-1 (10 interviews)
owner: brien
created: 2026-04-XX
updated: 2026-04-XX
panel_reviewed: false
---

# Spec Pain Opportunity Solution Tree

## Desired outcome

[ONE sentence. Measurable. Outcome, not output.]

Example (but validate with interviews before committing):
> Senior engineers using AI dev tools daily cut their spec-to-working-code rework rate by 50% within 30 days of adoption.

**Why this outcome:**
- [Why this matters to the participant (from their words, not ours)]
- [How it maps to something the org would fund]
- [What changes in the world if this outcome is achieved]

**How to measure:**
- [Specific measurable signal]
- [Baseline from interviews]
- [Target timeframe]

## Opportunity space

### Opportunity 1: [Short name — written in the participant's language, not ours]

**Quote that surfaced it:**
> "[Verbatim from interview]"
> — [Participant slug]

**Participants who described a version of this:**
- [Slug 1]: "[their version]"
- [Slug 2]: "[their version]"
- [Slug 3]: "[their version]"

**How they describe the pain:**
[One paragraph in participants' collective voice]

**Current workarounds:**
- [What they do instead]
- [What they've built themselves]
- [What they've bought]

**Size signal:**
- Frequency: [daily/weekly/monthly]
- Hours lost: [per occurrence]
- People affected: [team-wide or individual]

**Sub-opportunities:**

#### 1a. [Sub-opportunity]

[Description, grounded in quotes]

#### 1b. [Sub-opportunity]

[Description]

**Candidate solutions (from interviews OR brainstormed):**

##### Solution 1a.i: [solution name]

- **Source:** [interview quote OR brainstorm]
- **Assumptions that must be true:**
  1. [Assumption 1]
  2. [Assumption 2]
  3. [Assumption 3]
- **Assumption tests:**
  1. [How we'd test assumption 1 — cheapest/fastest possible]
  2. [How we'd test assumption 2]
  3. [How we'd test assumption 3]
- **What we'd learn from the tests:** [expected outcomes]

### Opportunity 2: [next opportunity]

[Same structure]

### Opportunity 3: [next]

[Same structure]

## Opportunity prioritization

Score each opportunity on:

| Opportunity | Frequency | Severity | Reach | Willingness | Our differentiation | Priority |
|-------------|-----------|----------|-------|-------------|---------------------|----------|
| Opportunity 1 | | | | | | |
| Opportunity 2 | | | | | | |
| Opportunity 3 | | | | | | |

- **Frequency:** how often the pain occurs (1-5)
- **Severity:** how bad the pain is when it occurs (1-5)
- **Reach:** how many participants described it (1-5)
- **Willingness:** how strongly they indicated willingness to change tools/workflows (1-5)
- **Our differentiation:** how much does Intent (or its components) uniquely address this vs. alternatives (1-5)
- **Priority:** weighted average (or judgment call)

**Top 3 opportunities to pursue:**
1. [Rank 1]
2. [Rank 2]
3. [Rank 3]

## Opportunities NOT being pursued (and why)

[Explicitly list opportunities from interviews we are choosing NOT to work on, and why. This is strategy per Rumelt: "strategy is choosing what not to do."]

- **Opportunity X:** [description]
  - Why not: [reason — too small / outside scope / already solved by X / etc.]

## What this tree tells us about Intent

### Hypothesis held

- [Parts of Intent's original hypothesis that this discovery supports]

### Hypothesis changed

- [Parts that need to be revised]
- [What the new version says]

### Hypothesis killed

- [Parts that discovery invalidated]
- [What we stop claiming]

## Assumption test backlog

From the solutions above, the assumption tests we need to run next:

1. [Test 1 — what, how, by when]
2. [Test 2]
3. [Test 3]
4. [Test 4]
5. [Test 5]

These become intents in `.intent/intents/` with links back to this tree.

## Next wave of interviews

Based on what this wave revealed, wave 2 should:
- Target [which population]
- Focus on [which opportunity]
- Ask [which questions differently]
- Avoid [what we did wrong this wave]

## Panel review

Before publishing, run:
```
panel-review target=DOM-spec-pain-OST panels=discovery,product,strategy depth=thorough
```

The panel should ask:
- Are the opportunities actually distinct, or are they the same pain in different words?
- Did we jump to solutions before validating opportunities?
- Is the root outcome measurable and compelling?
- Are the assumption tests actually cheap and fast, or are they "build the whole thing and see"?

## Lineage

- **Opportunity Solution Tree** — Teresa Torres, *Continuous Discovery Habits* (2021)
- **Story Mapping** — Jeff Patton, *User Story Mapping* (2014)
- **Jobs to Be Done** — Clayton Christensen
- **Design Thinking** — IDEO / Stanford d.school
- **Lean Startup** — Eric Ries (hypothesis testing, MVP, pivot)
```
