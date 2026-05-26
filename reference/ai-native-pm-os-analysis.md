---
title: Ai Native Pm Os Analysis
type: framework
maturity: final
confidentiality: internal
reusability: adaptable
created: 2026-04-26
technologies:
  - jira
  - amplitude
  - slack
frameworks:
  - double-loop-learning
depth_score: 5
depth_signals:
  file_size_kb: 18.3
  content_chars: 17796
  entity_count: 4
  slide_count: 0
  sheet_count: 0
  topic_count: 0
  has_summary: 0
vocab_density: 0.45
related_entities:
  - {pair: consulting-operations ↔ slack, count: 41, strength: 0.124}
  - {pair: jira ↔ subaru, count: 38, strength: 0.26}
  - {pair: jira ↔ turnberry, count: 33, strength: 0.264}
  - {pair: jira ↔ measurement-metrics, count: 32, strength: 0.224}
  - {pair: consulting-operations ↔ jira, count: 31, strength: 0.087}
---
# AI-Native PM OS — Competitive Analysis & Intent Framework Mapping

**Source:** [github.com/vishalmdi/ai-native-pm-os](https://github.com/vishalmdi/ai-native-pm-os)
**Author:** Vishal Jaiswal (vishalmdi) — AI-Driven Analytics Leader, 15+ yrs, Berlin. Ex-Wayfair. MDI-educated. Analytics/BI background pivoting into AI-native PM education.
**Analyzed:** 2026-04-26
**Analyst:** Brien / Claude (Intent project)

---

## 1. What This Is

A **structured, hands-on course** (11 modules, 63 lessons, ~40–50 hours) that teaches product managers to use Claude Code as an operating system for their daily work. It's not a prompt library — it's a complete curriculum that builds a persistent PM workspace with memory hierarchy, file architecture, slash commands, MCP integrations, and specialized agents.

The course uses a fictional B2B SaaS company called **Meridian** (workflow orchestration platform, $4.2M ARR, Series B) as the running context. Students build real deliverables against Meridian's OKRs, personas, and competitive landscape throughout all 11 modules.

**Delivery mechanism:** The repo itself IS the course. Students clone it, open Claude Code inside it, and the CLAUDE.md turns Claude into an interactive tutor that guides them through lessons via slash commands (`/lesson 3-1`, `/next`, `/complete`, `/progress`). Includes a Python-based progress dashboard on localhost:4242.

---

## 2. Repo Contents Summary

### Module Map

| Module | Title | Key Deliverables | Intent Relevance |
|--------|-------|-----------------|------------------|
| 0 | Setup & Orientation (8 lessons) | Four-folder workspace, CLAUDE.md, mental model, token economics | **High** — workspace architecture pattern |
| 1 | CLAUDE.md Mastery (5 lessons) | Three-level hierarchy (global/project/feature), self-improving CLAUDE.md, team CLAUDE.md | **High** — context engineering as methodology |
| 2 | File & Memory Operations (5 lessons) | Read/write patterns, learning companion, sub-agents, project memory, vault organization | **Medium** — memory persistence patterns |
| 3 | PRDs & Specs (5 lessons) | 5-stage PRD workflow (Seed→Outline→Draft→Critique→Polish), PRD-to-ticket pipeline, versioning | **Critical** — direct mapping to Intent's Spec phase |
| 4 | Data & Analytics (5 lessons) | Narrative analytics, retention/churn analysis, A/B test design with anti-peeking discipline, automated weekly digest | **Medium** — maps to Observe phase |
| 5 | Research & Discovery (5 lessons) | Interview synthesis, support ticket mining, competitive intel, JTBD mapping, discovery memo | **Critical** — direct mapping to Notice phase |
| 6 | Stakeholder & Strategy (5 lessons) | Opportunity sizing, roadmap reasoning, executive narrative, objection simulation, QBR docs | **High** — Spec-to-stakeholder communication |
| 7 | MCP & Tool Integrations (8 lessons) | Jira, Slack, Amplitude, Notion, Google Workspace, custom MCP servers | **High** — validates MCP as the integration layer |
| 8 | Team Workflows (5 lessons) | Shared team CLAUDE.md, decision log, shared context design, knowledge map, vault audit | **Medium** — team-level context patterns |
| 9 | Vibe Coding for PMs (5 lessons) | Build loop (Prompt→Preview→Iterate→Ship), metrics dashboard, research portal, prototypes, Vercel deploy | **Medium** — Execute phase analogue |
| 10 | Capstone (5 lessons) | Choose-your-own capstone (zero-to-one / scale / platform), four mental models, peer review, PM AI principles | **High** — synthesizes operating model |

### Key Non-Module Files

| File | Content | Intent Relevance |
|------|---------|------------------|
| `meridian-company/company-context.md` | Full fictional company context: metrics, personas (Olivia/Marcus/Asha), stakeholders (Dev/Tara/James/Priya/Rohan), competitive landscape, OKRs, roadmap | **Template** — excellent engagement context template |
| `CLAUDE.md` | Course guide with slash command definitions, model map, workspace conventions | **Pattern** — CLAUDE.md as interactive tutor |
| `course-server.py` | Python progress dashboard server | Low |
| `PROJECTS/meridian-os/CLAUDE.md` | Project-level CLAUDE.md for the fictional product | **Template** — project context pattern |
| `templates/supplementary-exercises.md` | Additional exercises | Low |

---

## 3. Intent Framework Mapping

### Where the Two Systems Overlap

The AI-Native PM OS and Intent are solving the **same fundamental problem** — that AI collapses implementation time, making the bottleneck upstream in discovery, specification, and observation — but they attack it from opposite ends:

| Dimension | AI-Native PM OS | Intent |
|-----------|----------------|--------|
| **Starting point** | Individual PM's daily workflow | Team operating model |
| **Unit of work** | Artifacts (PRDs, memos, analyses) | Signals → Intents → Specs → Contracts |
| **Memory model** | CLAUDE.md hierarchy (global/project/feature) | `.intent/` directory + compiled knowledge base |
| **Loop** | Implicit: Research → Draft → Critique → Ship | Explicit: Notice → Spec → Execute → Observe |
| **Agent model** | Ad-hoc sub-agents for parallel tasks | Typed agents with trust levels and autonomy gates |
| **Observation** | Automated weekly digests (push, not pull) | OTel-compatible event system, 15 event types |
| **Governance** | "Context > Prompting" + "Isolate the Work" | Trust scoring + L0-L4 autonomy levels |
| **Target user** | Individual PM learning to operate | Team adopting a methodology |

### Direct Phase Mappings

**Notice ↔ Module 5 (Research & Discovery)**
The course's Module 5 teaches interview synthesis, support ticket mining, competitive intelligence, and JTBD mapping. These are all signal-capture activities. Intent's Notice phase formalizes what Module 5 teaches informally — the difference is that Intent gives signals an identity (SIG-xxx), a lifecycle (captured → enriched → promoted → dismissed), and a trust score. Module 5 treats discovery outputs as files; Intent treats them as first-class entities with metadata.

**Spec ↔ Module 3 (PRDs & Specs)**
The 5-stage PRD workflow (Seed → Outline → Draft → Critique → Polish) is remarkably close to Intent's spec-shaping protocol (△ Shape, ◇ Outcome, ○ Contract, ◉ Readiness). Both use multi-perspective critique. The key difference: Intent's spec-shaping is persona-driven (four typed perspectives), while the course's critique is role-driven (engineer, designer, exec). Intent adds formal contracts and verifiable assertions; the course stays at PRD-level prose.

**Execute ↔ Module 9 (Vibe Coding)**
The "Build Loop" (Prompt → Preview → Iterate → Ship) maps to Intent's Execute phase. The course treats this as a PM superpower (prototyping); Intent treats it as an agent-driven phase with trust-gated execution. Different ambitions, same observation: PMs can now build.

**Observe ↔ Module 4 (Data & Analytics)**
Module 4's automated weekly digest and A/B test discipline map to Intent's Observe phase. Intent goes further with OTel event emission, dashboard visualization, and double-loop learning (observations questioning assumptions, not just optimizing). The course stays at "push analytics to yourself."

### What the Course Has That Intent Doesn't

1. **CLAUDE.md as methodology** — The three-level hierarchy (global/project/feature) is well-articulated. Intent has CLAUDE.md but hasn't codified it as a teachable practice. The course's Module 1 is essentially a missing Intent spec.

2. **Stakeholder communication templates** — Module 6's executive narrative structure (Situation → Opportunity → Evidence → Not Doing → Ask → Cost of Inaction) is a concrete, reusable template Intent doesn't have. The stakeholder persona framing (how to write for the CEO vs. CTO vs. CFO) is consulting-ready.

3. **Anti-style patterns** — The course's `anti-style.md` concept (encoding what Claude should NOT do) is a useful governance pattern. Intent has trust scoring but not negative-constraint files.

4. **Token economics awareness** — Module 0.8 teaches model selection as a financial decision (Haiku for structured work, Sonnet for nuanced, Opus for high-stakes). Intent doesn't address this.

5. **JTBD extraction from existing data** — Module 5.4's workflow for extracting JTBD statements from interview transcripts and support tickets, then mapping them to the roadmap, is a complete methodology. Intent's knowledge engine compiles understanding but doesn't have a specific JTBD extraction pipeline.

6. **A/B test discipline** — Module 4.4's pre-registration + anti-peeking framework is rigorous. Intent's Observe phase has event schemas but not experiment design discipline.

7. **The Meridian company context** — A richly detailed fictional B2B SaaS company with personas, stakeholders, OKRs, competitive landscape, and terminology. This is an excellent template for engagement context documents.

### What Intent Has That the Course Doesn't

1. **Formal work ontology** — Signal → Intent → Spec → Contract → Capability → Feature → Product. The course has artifacts but no lifecycle model.

2. **Trust and autonomy scoring** — L0-L4 autonomy levels, confidence/trust scores, circuit breakers. The course has no governance model for agent autonomy.

3. **Event system** — OTel-compatible, 15+ event types, traceable. The course has no observability infrastructure.

4. **Compiled knowledge base** — The three-layer architecture (raw → knowledge → transformation). The course uses flat files with no compilation step.

5. **Double-loop learning** — Observations that question domain assumptions, not just optimize execution. The course's feedback loop is single-loop (improve the artifact).

6. **Multi-surface signal capture** — 5-tier adapter architecture (MCP, CLI, Slack, GitHub, AI plugins). The course captures through manual prompting only.

7. **Spec contracts** — Verifiable assertions that agents can build against. The course's PRDs are prose, not contracts.

---

## 4. Materials Worth Ingesting

### Priority 1: Adopt or Adapt

| File | What to Extract | Where It Maps in Intent |
|------|----------------|------------------------|
| `meridian-company/company-context.md` | **Engagement context template** — persona format, stakeholder communication preferences, competitive landscape structure, OKR format. Adapt for Subaru/Turnberry. | `knowledge-engine/templates/` — new template: `engagement-context.md` |
| `module-6/6-3-executive-narrative.md` | **Executive one-pager template** (Situation → Opportunity → Evidence → Not Doing → Ask → Cost of Inaction). Board narrative structure. Anti-patterns for exec writing. | `knowledge/design-rationale/` or `.intent/templates/` |
| `module-5/5-4-jtbd-mapping.md` | **JTBD extraction pipeline** — prompt workflow for extracting JTBD from existing research, validation criteria (trigger/motivation/outcome tests), roadmap alignment mapping. | `knowledge-engine/` — enrichment agent pattern |
| `module-3/3-1-prd-from-scratch.md` | **5-stage PRD workflow** and **PRD template**. The Seed→Outline→Draft→Critique→Polish pipeline validates Intent's spec-shaping protocol. The template itself is production-ready. | `spec/` — validate against spec-shaping-protocol.md |

### Priority 2: Reference

| File | What to Extract | Where It Maps |
|------|----------------|---------------|
| `module-1/1-1-claude-md-hierarchy.md` | Three-level CLAUDE.md architecture pattern | Reference for Intent's own CLAUDE.md strategy |
| `module-4/4-4-ab-test-design.md` | Pre-registration + anti-peeking A/B test framework | `observe/` — experiment discipline for Observe phase |
| `module-10/10-3-four-mental-models.md` | "Context > Prompting", "Isolate the Work", "30-Minute Prototype Rule", "Push Don't Pull" | Intent methodology — validate against core principles |
| `module-0/0-7-pm-ai-mental-model.md` | Four-layer mental model (Memory, Context, Tasks, Agents) | Reference for Intent's practitioner onboarding |
| `module-7/7-1-what-is-mcp.md` | PM-focused MCP explanation and connector stack | Reference for Intent's MCP server documentation |
| `module-9/9-1-build-loop.md` | "Build vs. Spec" decision framework | Execute phase — when to prototype vs. when to spec |

### Priority 3: Interesting but Low-Urgency

| File | What to Extract |
|------|----------------|
| `module-10/10-5-pm-ai-principles.md` | Reflection-first principles writing methodology |
| `module-0/0-8-token-economics.md` | Model selection as financial decision |
| `templates/supplementary-exercises.md` | Additional practice patterns |

---

## 5. Author Assessment

**Vishal Jaiswal** (vishalmdi)
- **Background:** AI-Driven Analytics Leader, 15+ years experience scaling data organizations, $50M+ business impact, based in Berlin. MDI (Management Development Institute) educated. Previously at Wayfair.
- **GitHub profile:** 8 public repos, account since 2014. The ai-native-pm-os repo is his most substantial public work.
- **LinkedIn:** [vishal-jaiswal-analytics-leader](https://de.linkedin.com/in/vishal-jaiswal-analytics-leader)
- **Positioning:** Analytics/BI leader who has built an AI-native PM curriculum. His analytics background shows in the data modules (Module 4's A/B test discipline is notably rigorous). The course reflects someone who has managed PMs or worked closely with PM teams, not a career PM per se.

**Assessment:** Vishal is a **competent practitioner-educator** rather than an established thought leader. The course is well-structured and practical — it teaches by building, not by lecturing. His analytics rigor elevates the data/experimentation modules above most PM AI content. However, he's not in the Cagan/Patton/Torres tier of influence. The course is more of a "workshop in a repo" than a published methodology.

**Worth adding to Brien's persona registry?** Not as a primary thought leader. Worth tracking as a peer practitioner building in a similar space. The course itself is more valuable than the author's brand — it's a well-executed instantiation of ideas that Brien is formalizing at a deeper architectural level.

---

## 6. Comparative Positioning

Think of it this way: if Intent is the **architect's blueprint** for how AI-augmented teams should operate, the AI-Native PM OS is the **contractor's field manual** for how an individual PM should set up their tools. They're complementary, not competitive.

| | AI-Native PM OS | Intent |
|---|---|---|
| **Metaphor** | Setting up your workshop | Designing the factory |
| **Audience** | Individual PM wanting to be more effective | Team/org wanting a new operating model |
| **Depth** | Wide (covers everything a PM does) | Deep (formalizes the loop + knowledge layer) |
| **Maturity** | Course (teaching) | Framework (prescribing) |
| **Governance** | Informal ("isolate the work") | Formal (trust scores, autonomy levels, approval gates) |
| **Knowledge model** | Flat files in folders | Compiled knowledge base with cross-references |

The course validates Intent's core thesis from a grassroots direction: PMs are already building these systems ad hoc. Intent provides the architecture that makes them systematic, traceable, and team-scale.

---

## 7. Adoption Recommendations

### Immediate (this week)

1. **Adapt the Meridian company context template** for Brien's engagement contexts. The persona format (day-to-day reality, pain points, goals, hiring trigger, key quote) and the stakeholder communication preferences (how to frame for each executive) are directly applicable to Subaru and Turnberry deliverables.

2. **Add the executive one-pager template** from Module 6.3 to Intent's templates. The Situation → Opportunity → Evidence → Not Doing → Ask → Cost of Inaction structure is tighter than most exec communication frameworks.

### Short-term (this month)

3. **Cross-reference the PRD workflow against Intent's spec-shaping protocol.** The 5-stage workflow (Seed→Outline→Draft→Critique→Polish) and Intent's four-persona interrogation (△◇○◉) are solving the same problem differently. Consider whether the course's approach (role-based critique: engineer/designer/exec) should be offered as an alternative path alongside Intent's persona-based approach.

4. **Extract the JTBD pipeline** from Module 5.4 as a potential Knowledge Engine enrichment agent. The extraction → validation → roadmap-alignment flow is well-designed and could be formalized as a knowledge operation.

### Medium-term (this quarter)

5. **Consider the anti-style.md pattern** as a governance addition to Intent. Negative constraints ("never say X") complement Intent's positive specifications. Could live alongside CLAUDE.md as a counterpart.

6. **Evaluate the course's "Context > Prompting" principle** as an Intent design axiom. Intent already embodies this (the compiled knowledge base IS persistent context), but it's not articulated as a named principle that practitioners can internalize.

---

## 8. Key Quotes Worth Preserving

> "A single prompt produces a generic PRD. It has structure but no soul — no decisions, no trade-offs, no real thinking. A PRD workflow produces a document that survived pressure." — Module 3.1

> "AI commoditizes the artifacts, not the decisions." — Module 10.3

> "If you find yourself spending more than 30 minutes trying to explain an interaction in a spec or PRD, stop writing and start building." — Module 10.3 (The 30-Minute Prototype Rule)

> "The PMs who worry about being replaced defined their value by what they produce — the document, the ticket, the update. The AI-Native PM defines their value by the decisions they force and the velocity they enable for their team." — Module 10.3

> "You are the product thinker. Claude is the builder." — Module 9.1

---

*Analysis complete. This file lives in `reference/` as a knowledge artifact, not an engagement deliverable.*
