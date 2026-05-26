---
type: industry-analysis
depth_score: 4
depth_signals:
  file_size_kb: 7.6
  content_chars: 7212
  entity_count: 0
  slide_count: 0
  sheet_count: 0
  topic_count: 0
  has_summary: 0
vocab_density: 0.42
source: "https://martinfowler.com/articles/exploring-gen-ai/sdd-3-tools.html"
captured: 2026-04-12
origin: agent
confidence: 0.90
related_signals:
  - SIG-032
extraction_depth: high
author: Birgitta Böckeler (Distinguished Engineer, Thoughtworks)
published: 2025-10-15
---
# Fowler/Böckeler — SDD Tools Survey: Kiro, spec-kit, Tessl

Article: "Understanding Spec-Driven-Development: Kiro, spec-kit, and Tessl"
Author: Birgitta Böckeler (Distinguished Engineer, AI-assisted delivery expert, Thoughtworks)
Published: 15 October 2025

## Three Tools Covered

### Kiro (VS Code-based, AWS-adjacent)
- **Workflow:** Requirements → Design → Tasks (three markdown docs, linear)
- Requirements: user stories ("As a...") with acceptance criteria (GIVEN/WHEN/THEN)
- Design: component architecture, data flow, models, error handling, testing strategy
- Tasks: trace back to requirement numbers; UI to run/review one by one
- Memory bank ("steering"): flexible, default topology is product.md, structure.md, tech.md
- **Validation:** Implicit — human reviews. No checklist or formal validation layer
- **Positioning:** Spec-first only

### spec-kit (GitHub's SDD implementation, CLI-based)
- **Workflow:** Constitution → Specify → Plan → Tasks (cyclical)
- Constitution: immutable rules file — "a very powerful rules file that is heavily used by the workflow"
- Heavy use of checklists inside files to track clarifications, constitution violations, research tasks
- Checklists function as "definitions of done" — but interpreted by AI, no guarantee of adherence
- Creates a branch per spec — signals spec-first despite aspirational spec-anchored language
- One spec = many files (verbose topology)
- **Aspiration:** "Not as static documents, but as living, executable artifacts that evolve with the project"
- **Reality:** branch-per-spec treats specs as living for change request lifetime, not feature lifetime

### Tessl Framework (CLI + MCP server, private beta as of Sept 2025)
- Most ambitious: explicitly aspires to spec-anchored and spec-as-source
- Spec can be primary artifact with `// GENERATED FROM SPEC - DO NOT EDIT` markers
- Currently 1:1 mapping: one spec → one code file. Exploring multi-file for future
- Spec tags: `@generate`, `@test` — directive annotations
- API section in specs: defines interfaces exposed to other parts of codebase
- `tessl document --code ...js` reverse-engineers existing code into a spec
- `tessl build` generates code file from spec
- Abstraction level: low (per-file), which reduces LLM interpretation steps

## Böckeler's Three-Level SDD Taxonomy

1. **Spec-first** — well-developed spec written before AI-assisted coding (all three tools)
2. **Spec-anchored** — spec kept after task complete, used for ongoing feature evolution (aspirational in spec-kit; operational in Tessl)
3. **Spec-as-source** — spec is only human-editable artifact; humans never touch code (Tessl's stated north star)

## Cross-Cutting Patterns

**Memory bank / context document distinction:** All three tools separate global codebase context from task-specific specs. Spec-kit calls it "constitution," Kiro calls it "steering," Tessl has its own equivalent. These are "relevant across all AI coding sessions," whereas specs are task-scoped.

**Spec definition (synthesized):** "A structured, behavior-oriented artifact — or a set of related artifacts — written in natural language that expresses software functionality and serves as guidance to AI coding agents."

## What Works

- Spec-first as general principle: real demand, frequently asked questions in the field
- Kiro's 3-doc model more intuitive than spec-kit's verbose multi-file structure

## What Doesn't Work

- **Problem size mismatch:** Neither Kiro nor spec-kit provides flexible workflows for varying scales. Kiro turned a small bug fix into 4 user stories with 16 acceptance criteria
- **Review burden:** "I'd rather review code than all these markdown files." Spec-kit files were repetitive with each other and existing code
- **False sense of control:** Agents frequently ignored or over-interpreted instructions. Larger context windows don't guarantee adherence
- **Functional/technical separation:** Constant confusion about when to stay functional vs. add technical details. "Poor track record as a profession"
- **Target user ambiguity:** Tools incorporate product analysis, user story definition without stating who should do them
- **Iteration incompatibility:** "The best way for us to stay in control are small, iterative steps, so I'm very skeptical that lots of up-front spec design is a good idea"

## The MDD Warning (Key Structural Insight)

Böckeler draws the parallel to **Model-Driven Development**, not BDD/TDD:

- In MDD, models in UML/DSLs served as specs; code generators turned them into code
- MDD "never took off for business applications — awkward abstraction level, too much overhead"
- LLMs remove MDD's core constraints (no need for parseable spec language or elaborate code generators)
- **But LLMs add non-determinism** — the thing MDD didn't have
- MDD's parseable structure had upsides being lost: tool support for authoring valid, complete, consistent specs

**Her warning:** Spec-as-source, and even spec-anchoring, "might end up with the downsides of both MDD and LLMs: Inflexibility AND non-determinism."

## "Verschlimmbesserung"

German compound word: "making something worse through the attempt to make it better." Her closing warning: elaborate SDD tooling may amplify existing problems rather than solve them.

## Unresolved Questions

1. Real-world applicability for complex brownfield codebases
2. What problem size SDD is actually appropriate for
3. Whether iterative development and spec-driven up-front design are fundamentally incompatible
4. Right abstraction level for specs (per-file, per-feature, per-component)
5. Who the actual target practitioner is
6. No long-term usage reports from anyone using SDD on a real established codebase

## Relevance to Intent's Spec Product

**Intent occupies a unique position in the SDD landscape:**

| Dimension | Kiro/spec-kit/Tessl | Intent |
|---|---|---|
| Validation | Human review between stages, no automation | Trust-gated autonomy — spec IS the trust gate |
| Memory/spec separation | Ambiguous naming | Explicit: context docs (project-level) vs specs (agent-execution) |
| Spec lifecycle | Spec-first through spec-as-source | Spec-governed execution (between spec-first and spec-as-source) |
| Non-determinism | Acknowledged but unaddressed | Observe stage + hypothesis tracking detect/correct over time |
| MDD trap | At risk | Spec-as-contract + trust gates = executable assertion, not generation prompt |
| Problem sizing | One-size-fits-all workflows | Trust scoring adapts workflow to signal complexity |
| Iteration | Tension with up-front design | Continuous loop eliminates the tension — no "up-front" phase |

**Key architectural differentiation:** Intent's specs are contracts agents execute against with humans in the loop via trust gates — not just pre-generation guidance (spec-first) or the sole editable artifact (spec-as-source). This is "spec-governed execution."

**The MDD warning for Intent:** If specs become primary artifact without solving validation/consistency tooling, you get MDD's inflexibility without parsing guarantees. Intent's answer: spec-as-contract + trust gates + observe phase. The spec isn't just a prompt — it's an executable assertion the agent is verified against.
