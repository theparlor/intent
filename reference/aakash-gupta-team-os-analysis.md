---
title: Aakash Gupta / Hannah Stulberg — Team OS Analysis
type: external-pattern-analysis
thought_leaders:
  - matthew-skelton
  - manuel-pais
frameworks:
  - team-topologies
depth_score: 5
depth_signals:
  file_size_kb: 17.6
  content_chars: 16451
  entity_count: 3
  slide_count: 0
  sheet_count: 0
  topic_count: 0
  has_summary: 0
vocab_density: 0.36
related_entities:
  - {pair: manuel-pais ↔ matthew-skelton, count: 266, strength: 0.635}
  - {pair: manuel-pais ↔ team-topologies, count: 232, strength: 0.856}
  - {pair: matthew-skelton ↔ team-topologies, count: 232, strength: 0.555}
  - {pair: matthew-skelton ↔ mik-kersten, count: 198, strength: 0.407}
  - {pair: matthew-skelton ↔ richard-rumelt, count: 162, strength: 0.338}
source_type: substack-note + github-repo + podcast
source_urls:
  - "https://substack.com/@aakashgupta/note/c-240536298"
  - "https://github.com/in-the-weeds-hannah-stulberg/team-os-example-repo"
  - "https://substack.com/@hannahstulberg/note/c-244346568"
author_primary: Hannah Stulberg (DoorDash PM, ex-Google APM)
author_secondary: Aakash Gupta (Product Growth newsletter, amplifier/interviewer)
date_published: 2026-04-09
date_analyzed: 2026-05-08
related_signals:
  - SIG-038
related_specs:
  - SPEC-productivity-os-layers
related_intents:
  - INT-015
---
# Aakash Gupta / Hannah Stulberg — Team OS Analysis

> "Scaling isn't about making yourself faster — it's about making your team better."

## 1. Article Summary

Aakash Gupta's Substack note (Apr 9, 2026) profiles Hannah Stulberg, a DoorDash PM and ex-Google APM with 1,500+ hours in Claude Code, who built what she calls a "Team OS" — a shared GitHub repository that serves as the knowledge substrate for her entire cross-functional team (~20 people). Aakash amplifies and frames the concept; Hannah is the practitioner and architect.

### What Team OS Is

Team OS is a shared GitHub repo structured so that any team member — PM, designer, data scientist, engineer, strategy lead — can start a Claude Code session and have the agent already understand the team's full context. The repo replaces the PM as the team's context bottleneck.

### The 7-Part Architecture

Hannah describes a concrete, implementable structure:

1. **Root CLAUDE.md** (under 500 tokens) — Doc index, team roster with Slack IDs and GitHub handles. Acts as the routing table for the entire system.
2. **Nested CLAUDE.md files** in every major folder — Navigation indexes only, ~3% of context window per query. Not content — pointers.
3. **Folder ownership by function** — PM owns product/, data scientist owns analytics/, strategy owns customer calls. Clear provenance.
4. **Analytics layer** — Metric definitions, SQL queries, dashboard links. Loaded progressively by depth (not all at once).
5. **Shared skills** — Customer call summaries, PR creation, weekly synthesis. Everyone runs the same agent tools.
6. **Verified playbooks** — Recurring analyses (funnel drop-off, churn investigation) as repeatable agent workflows. Same steps your analyst would follow.
7. **Launch gate** — No feature ships until its metrics, queries, schemas, dashboards, and playbooks are checked into the repo. Knowledge becomes a deployment prerequisite.

### The Example Repo (Forge)

Hannah published a complete example repo (`in-the-weeds-hannah-stulberg/team-os-example-repo`) modeling a fictional 10-person product team at "Forge," an AI prototyping startup. Structure:

```
team-os-example-repo/
├── .claude/                    # Agent configuration
├── CLAUDE.md                   # Root: team roster, Slack channels, DM groups, doc index
├── product-development/
│   ├── feature-index.yaml      # Master lookup — every feature → all artifacts
│   ├── product/
│   │   ├── CLAUDE.md           # Product context, pillars, segments, competitive landscape
│   │   ├── PRDs/CLAUDE.md
│   │   ├── customers/CLAUDE.md # Customer calls, account context, feature requests
│   │   ├── competitive-research/CLAUDE.md
│   │   ├── strategy/CLAUDE.md  # Roadmaps, vision, business context
│   │   ├── launch-emails/CLAUDE.md
│   │   ├── sales-enablement/CLAUDE.md
│   │   ├── processes/CLAUDE.md
│   │   ├── product-context/CLAUDE.md
│   │   └── meetings/CLAUDE.md
│   ├── analytics/CLAUDE.md     # Metrics glossary, data sources, common queries
│   └── engineering/CLAUDE.md   # Engineering plans, RFCs, bug investigations
└── team/                       # Onboarding guide and team resources
```

### Key Framing

Hannah's punchline: she went from being the team's bottleneck to building the system that made the bottleneck disappear. The barrier to starting is "psychological" — the terminal feels scary for about an hour, then it feels normal. She and Carl Vellotti are now running a $200 Maven workshop ("How to Build Your Team OS") on May 10, 2026.

---

## 2. Intent Productivity Stack Mapping

### Where Team OS Sits: Solidly L3, with L2 Aspirations

Hannah's Team OS maps cleanly to **L3 (Team OS)** in Intent's Productivity Stack layer model (SPEC-productivity-os-layers.md). The alignment is striking:

| Intent L3 Dimension | Hannah's Team OS | Alignment |
|---------------------|-----------------|-----------|
| **Scope** | ~20 people, cross-functional (PM, design, analytics, eng, strategy) | **Match** — Intent says 3-8 for core trio, but Hannah scales to 20 through folder ownership. This is worth noting. |
| **Knowledge Architecture** | Shared GitHub repo as compiled knowledge base. CLAUDE.md hierarchy as the routing layer. | **Strong match** — This IS Intent's Layer 1 (Compiled Knowledge Base) implemented at team scope. Feature-index.yaml is a manually-maintained version of Intent's `_index.md`. |
| **Loop cadence** | Implicit daily (standups, weekly synthesis skill). No formal loop language. | **Partial match** — Hannah has the cadence but doesn't name the phases. No explicit Notice→Spec→Execute→Observe. |
| **Trust/autonomy** | Implicit — shared skills are pre-verified, launch gate enforces quality. No trust scoring. | **Gap** — No formal autonomy levels. Everyone can run everything. The launch gate is a binary governance mechanism, not a graduated trust model. |
| **Personas** | No persona concept. Function-based ownership (PM, analyst, engineer). | **Gap** — Intent's four personas (△◇○◉) are absent. Hannah organizes by org-chart function, not by cognitive role. |
| **Observability** | Not addressed. No event system, no signal capture, no metrics on the system itself. | **Major gap** — The Team OS has no observe layer. Hannah doesn't track how the system is used, which queries succeed, which playbooks fail. |
| **Tools** | Claude Code, GitHub, Slack, Google Docs, call transcript importers. | **Match** — Same tool surface as Intent's L3 tools list. |

### What Hannah Gets That Intent Should Learn From

1. **The CLAUDE.md hierarchy as a routing layer is brilliantly minimal.** Intent's `.intent/` structure is richer but also heavier. Hannah proves that under-500-token root files with pure navigation indexes are sufficient for a team of 20. Intent should adopt the "3% context per query" design principle.

2. **Folder ownership by function is a lightweight governance model.** Intent uses personas (△◇○◉) for cognitive diversity in spec shaping, but Hannah uses org-chart ownership for content accountability. Both are needed — Intent should consider adding a `steward` field to knowledge artifacts.

3. **The launch gate is a brilliant forcing function.** No feature ships without its knowledge artifacts checked in. This turns knowledge compilation from a "nice to have" into a deployment prerequisite. Intent should name this pattern and adopt it for L3 deployments.

4. **Progressive loading by depth** — The analytics layer loads metric definitions first, then SQL queries, then dashboard links, scaling context usage to the depth of the question. Intent's persona loading doesn't do this yet.

5. **The "psychological barrier" framing** — Hannah names the real adoption blocker: the terminal feels scary. This is the L1→L3 transition problem. Intent's site and course should address this directly.

### What Intent Has That Team OS Doesn't

1. **The loop.** Hannah's system is a knowledge base, not an operating model. It answers "what does the team know?" but not "how does the team decide what to work on next?" Intent's Notice→Spec→Execute→Observe is the process layer that sits atop Team OS's knowledge layer.

2. **Trust and autonomy.** Hannah's system is flat — anyone can run anything. Intent's L0-L4 autonomy levels with trust scoring are necessary when the blast radius of agent actions grows beyond the team (L4+).

3. **Signal capture.** Team OS has no mechanism for surfacing what the team is noticing. Insights stay locked in individual conversations until someone manually writes them down. Intent's signal system makes noticing a first-class operation.

4. **Observability on the system itself.** Hannah can't answer "is the Team OS working?" There's no event log, no metrics on agent success rates, no tracking of which playbooks get used. Intent's observe layer is precisely this.

5. **Compilation over retrieval.** Hannah's system organizes raw context (PRDs, call transcripts, metrics definitions) for agent access. Intent's Knowledge Engine compiles understanding — personas, journeys, decision records — from that raw material. The compilation step is what makes knowledge compounding rather than linear.

6. **Cross-layer flows.** Team OS is a single altitude. Intent shows how signals flow up, governance flows down, and knowledge flows laterally across organizational layers.

---

## 3. Signals Extracted for Intent

### Signal 1: L3 Scope Extends Beyond the Product Trio (Validation + Challenge)

Hannah runs Team OS with ~20 people across 5 functions (PM, design, eng, analytics, strategy/ops). Intent's L3 definition says "3-8 people" — the Cagan product trio. Hannah's evidence suggests L3 can scale further than Intent specifies IF the knowledge architecture is well-structured (CLAUDE.md hierarchy + folder ownership). The boundary between L3 and L4 may be defined not by headcount but by whether the team shares a single knowledge base or requires federation.

**Implication:** Revise L3 scope from "3-8" to "up to ~20 with shared repo" and define the L3→L4 boundary as "when a single repo can no longer hold the team's context."

### Signal 2: "Launch Gate" Pattern — Knowledge as Deployment Prerequisite

Hannah's rule: no feature ships until metrics, queries, schemas, dashboards, and playbooks are checked into the Team OS repo. This is a governance pattern Intent should name and formalize. It's the L3 equivalent of Intent's trust-gated execution — but applied to knowledge completeness rather than signal trust.

**Implication:** Add a "knowledge gate" concept to Intent's L3 definition. Before a spec moves to Execute, its knowledge artifacts must exist. Before Execute produces output, the output's observability artifacts must exist.

### Signal 3: Team OS Validates "Compilation Over Retrieval" From the Bottom Up

Hannah's system is retrieval-oriented — agents retrieve raw PRDs, call transcripts, and metric definitions on demand. She doesn't compile personas or decision records from that raw material. But the success of her approach (team of 20 self-serving) proves the value of structured context even WITHOUT compilation. Intent's compilation layer adds compounding value on top — this is a differentiation story worth telling.

**Implication:** Position Intent's compilation step as the "Level 2" of the Team OS concept. Hannah solved "everyone can find what they need." Intent solves "the system understands what it all means."

### Signal 4: The "AI Changed the Ratios" Thesis (Leah Tharin Adjacent)

Hannah's core narrative is bottleneck elimination — the PM was the team's context bottleneck, and the Team OS removed it. This directly validates Leah Tharin's argument that AI changes team ratios. When context is embedded in a repo rather than a person, you need fewer PMs per engineer. Intent should cite Hannah's experience alongside Tharin's thesis.

**Implication:** Cross-reference Hannah's Team OS with Tharin's ratio-change argument in Intent's positioning. Both support the same conclusion: the PM role shifts from context-holder to system-builder.

### Signal 5: Aakash Gupta as Amplification Channel (Not Originator)

The "Team OS" concept originated with Hannah Stulberg, not Aakash Gupta. Aakash's role is amplifier and interviewer — his newsletter audience (~500K+) gave the concept reach. This is an important distinction for attribution. Brien's existing persona file for Aakash should note his role as a distribution channel for practitioner-originated patterns, not just his own frameworks.

### Signal 6: Maven Workshop as Market Validation

Hannah and Carl Vellotti are running a $200, 3-hour Maven workshop on "How to Build Your Team OS" (May 10, 2026). The fact that this sold enough to run — at $200 for a 3-hour session, with "no technical background required" — validates that Team OS is a product category, not just a blog post. This is the same market Intent's AI PM OS course targets.

**Implication:** Monitor this workshop for competitive intelligence. Hannah's workshop teaches the L3 knowledge layer. Intent's course should teach L1-L3 with the full loop — Notice through Observe — as the differentiator.

---

## 4. Vocabulary Worth Adopting

| Hannah's Term | Intent Equivalent | Recommendation |
|--------------|-------------------|----------------|
| **Team OS** | L3: Team OS (already used!) | **Keep.** Intent already uses "Team OS" for L3. Hannah's usage validates the term in the wild. |
| **Shared repo as team brain** | Compiled Knowledge Base at team scope | **Adopt selectively.** "Team brain" is more accessible than "compiled knowledge base" for L3 pitches. |
| **CLAUDE.md hierarchy** | `.intent/` + `knowledge/_index.md` | **Note as implementation pattern.** Intent's structure is richer but could learn from the minimalism. |
| **Folder ownership** | Knowledge artifact stewardship | **Adopt.** Add `steward: <function>` to knowledge artifact frontmatter. |
| **Launch gate** | Knowledge gate / readiness gate | **Adopt and formalize.** Name this as a first-class L3 governance pattern. |
| **Progressive loading by depth** | (not in Intent) | **Adopt.** Design persona and knowledge loading to respect context budgets, loading progressively. |
| **Verified playbooks** | Shared skills / agent workflows | **Note.** "Verified playbook" is a good accessible term for agent workflows that have been tested. |
| **Context bottleneck** | (implicit in Intent's thesis) | **Adopt as framing.** "The PM is the team's context bottleneck" is a powerful hook for Intent's L3 story. |

---

## 5. Should This Update SPEC-productivity-os-layers.md?

**Yes, in three specific places:**

1. **L3 scope definition.** Change from "3-8 people" to "up to ~20 with shared knowledge base" and define the L3→L4 boundary as "when a single knowledge base can no longer hold the team's context" (requiring federation).

2. **L3 tools/infrastructure.** Add "CLAUDE.md hierarchy" and "folder ownership pattern" as named tools. Add "launch gate" as a governance mechanism.

3. **L3 "What Brien is building here."** Add a reference to Hannah Stulberg's Team OS as external validation. Note that her implementation is the knowledge layer (Layer 1 at team scope) without the loop (Layer 2) or observability (Layer 3). Intent provides the full stack.

**Also add to the Notes section:** Hannah Stulberg / Aakash Gupta Team OS as an adjacent signal, alongside the existing references to Dex Horthy, Ethan Mollick, Team Topologies, and Stafford Beer.

---

## 6. Relationship to Existing Personas

### Aakash Gupta

Aakash Gupta is already in Brien's reference awareness (thought leader in PM/growth). His role here is amplifier, not originator. The Team OS concept should be attributed to Hannah Stulberg; Aakash's contribution is distribution and framing.

### Hannah Stulberg (New Persona Candidate)

Hannah Stulberg should be added to Brien's persona awareness as a practitioner-architect (△) archetype:
- DoorDash PM, ex-Google APM
- 1,500+ hours in Claude Code — one of the highest-usage practitioners publicly documented
- Built a team-scale AI operating system from practice, not theory
- Publishes at hannahstulberg.substack.com ("In the Weeds")
- Running Maven workshops with Carl Vellotti
- Her framing ("make yourself unnecessary to the system") aligns with Intent's thesis

She represents the practitioner who independently built what Intent formalizes. Similar to Brien's conversation with engineer Ari — someone who discovered the pattern from practice.

---

## Notes

**Intellectual lineage:** This analysis connects Hannah Stulberg's Team OS → Aakash Gupta's amplification → Intent's L3 layer model → Leah Tharin's ratio-change thesis → Cagan's empowered product teams. The throughline: AI makes context a system property rather than a person property, which changes team composition and governance.

**Open questions:**
- Does Hannah's team have any signal capture mechanism we missed? Her "customer call summaries" skill suggests at least partial notice-phase coverage.
- What's the maintenance burden of the Team OS? Who updates the CLAUDE.md files when the team's context changes? This is the knowledge freshness problem Intent addresses with the Knowledge Engine's lint/enrichment pipeline.
- How does Hannah handle conflicting knowledge? Two PRDs that contradict each other, two metric definitions that disagree? Intent's DDR (Design Decision Record) pattern addresses this; Team OS appears not to.
