---
title: Spec-Shaping Protocol — Multi-Persona Intent Interrogation
type: spec
maturity: draft
created: 2026-04-06
thought_leaders:
  - marty-cagan
  - teresa-torres
  - jeff-patton
summary: "How intents become agent-ready specs through self-prompting with specific personas. Each persona interrogates the intent from a different angle, querying the knowledge base, until the spec is rich enough for execution."
depth_score: 6
depth_signals:
  file_size_kb: 9.3
  content_chars: 9415
  entity_count: 3
  slide_count: 0
  sheet_count: 0
  topic_count: 0
  has_summary: 1
vocab_density: 0.11
related_entities:
  - {pair: marty-cagan ↔ consulting-operations, count: 98, strength: 0.051}
  - {pair: marty-cagan ↔ turnberry, count: 46, strength: 0.065}
  - {pair: teresa-torres ↔ marty-cagan, count: 45, strength: 0.247}
  - {pair: marty-cagan ↔ mik-kersten, count: 43, strength: 0.002}
  - {pair: teresa-torres ↔ jeff-patton, count: 36, strength: 0.396}
---
# Spec-Shaping Protocol

> **Purpose:** The missing step between "intent proposed" and "spec ready for agent execution." A multi-persona interrogation that turns Brien-shaped prose into structured, agent-ready specifications.
>
> **Version:** 1.0 — 2026-04-06
>
> **Problem it solves:** Intents are captured as Problem/Outcome/Evidence/Constraints. That's enough for a human to understand what needs to change, but not enough for an agent to build against. The gap between "what needs to change" and "what to build" is where most specs fail.

---

## The Shape of an Agent-Ready Spec

Huryn's observation applies: most people use 2 of 10 dimensions. Most specs use 2 of the dimensions an agent needs. That's why execution results feel shallow.

An agent-ready spec must cover:

| Dimension | What it answers | Who typically provides it |
|-----------|----------------|-------------------------|
| **Role** | What stance should the agent take? Builder? Analyst? Reviewer? | △ Architect |
| **Task** | What concrete artifact is being produced? | △ Architect |
| **Goal** | What outcome does this serve? What behavior changes? | ◇ Product Leader |
| **Audience** | Who consumes the output? Brien? A client? The system itself? | ◇ Product Leader |
| **Context** | What does the knowledge base say? Prior decisions? Domain state? | All (via Flow 2 queries) |
| **Style** | What patterns, conventions, frameworks govern the output? | △ Architect + ○ Quality |
| **Structure** | What's the shape of the deliverable? File layout? Schema? | △ Architect |
| **Constraints** | What to avoid? What decisions are already made (DDRs)? Blast radius? | ○ Quality + ◉ Agent |
| **Output format** | Markdown? Code? YAML? Multiple files? | ◉ Agent |
| **Contract** | Observable verification criteria. How the agent proves it worked. | ○ Quality |

---

## The Four-Persona Interrogation

When an intent reaches `status: accepted`, the system runs it through four persona lenses. Each persona queries the knowledge base (Flow 2), checks existing decisions (DDRs), and generates structured questions and assertions.

### Pass 1: △ Practitioner-Architect (Shape)

**Questions this persona asks:**
- What's the technical approach? Which patterns apply?
- What's in scope and out of scope? Where are the boundaries?
- What decisions have I already made (grep `knowledge/decisions/`)? What decisions am I making now vs leaving to the agent?
- What existing specs does this relate to? What contracts does it need to satisfy?
- What's the file layout of the deliverable?

**Queries the knowledge base for:**
- `knowledge/decisions/DDR-*` — prior decisions that constrain this
- `knowledge/domain-models/DOM-*` — bounded contexts and entity relationships
- `knowledge/design-rationale/RAT-*` — reasoning that should inform the approach

**Output:** The Shape section of the spec — boundaries, approach, key decisions made, open decisions for the agent.

### Pass 2: ◇ Product-Minded Leader (Intent & Outcome)

**Questions this persona asks:**
- What outcome does this serve? Not the deliverable — the behavioral change.
- Who is this for? Which persona benefits?
- What does the knowledge base say about this persona's actual needs?
- How does this connect to the broader strategy?
- What doesn't matter? What can we explicitly deprioritize?

**Queries the knowledge base for:**
- `knowledge/personas/PER-*` — who this serves and what they need
- `knowledge/journeys/JRN-*` — where in the journey this intervenes
- `knowledge/themes/THM-*` — what cross-cutting insights apply

**Output:** The Intent section of the spec — why it matters, what outcome is expected, who benefits, Seiden-style behavioral change.

### Pass 3: ○ Design-Quality Advocate (Contract)

**Questions this persona asks:**
- How do we know this is done? Not "code compiles" — what observable outcome?
- What quality constraints exist? Performance? Accuracy? Coverage?
- What are the acceptance criteria? Can the agent self-verify?
- What validation criteria from prior DDRs apply?
- What could go wrong? What are the failure modes?

**Queries the knowledge base for:**
- `knowledge/decisions/DDR-*` — validation criteria from related decisions
- `knowledge-engine/spec/contracts.md` — existing contracts that may be affected

**Output:** The Contract section of the spec — observable outcomes, verification commands, quality constraints, failure modes.

### Pass 4: ◉ AI Agent (Readiness Assessment)

**Questions this persona asks:**
- Is this spec clear enough for me to execute without asking Brien?
- What's ambiguous? Where will I have to make decisions the spec doesn't cover?
- What files do I need to read before starting?
- What tools/operations do I need?
- What's the trust score? Am I authorized to execute this autonomously?
- What events should I emit during execution?

**Queries:**
- The spec itself (produced by passes 1-3)
- Trust scoring formula against this spec

**Output:** Agent readiness assessment — trust score, ambiguity flags, required reads, recommended autonomy level. If trust < L2, the agent generates a disambiguation signal instead of executing.

---

## The Flow

```
INT-NNN (accepted)
  │
  ├── Pass 1: △ Architect shapes boundaries + approach
  │   └── queries: DDRs, domain models, rationale
  │
  ├── Pass 2: ◇ Product Leader clarifies outcome + audience
  │   └── queries: personas, journeys, themes
  │
  ├── Pass 3: ○ Quality Advocate writes contract
  │   └── queries: DDR validation criteria, existing contracts
  │
  └── Pass 4: ◉ Agent assesses readiness
      └── queries: the spec itself, trust formula
      │
      ├── IF trust ≥ L2 → SPEC-NNN created, ready for execution
      └── IF trust < L2 → disambiguation signal generated, Brien reviews
```

### Iteration

The four passes may iterate. If the Agent readiness pass (Pass 4) finds ambiguity, it generates specific questions. These go back through the relevant persona pass:

- Technical ambiguity → back to △ Architect
- Outcome ambiguity → back to ◇ Product Leader
- Verification ambiguity → back to ○ Quality Advocate

One or two iterations should be sufficient. If three iterations don't resolve ambiguity, the spec is blocked and Brien needs to intervene.

---

## Spec Template (Output of the Protocol)

```yaml
---
id: SPEC-NNN
title: ""
status: draft
intent: INT-NNN
trust_score: 0.0
autonomy_level: L0-L4
shaped_by: [architect, product, quality, agent]
personas_queried: [PER-NNN]
decisions_referenced: [DDR-NNN]
contracts: [CON-NNN]
created: YYYY-MM-DD
---
```

```markdown
# Spec: Title

## Intent (from Pass 2: ◇ Product Leader)
Why this matters. What outcome. Who benefits. What behavior changes.
Links to: [[PER-NNN]], [[JRN-NNN#stage]], [[THM-NNN]]

## Shape (from Pass 1: △ Architect)
Technical approach. Boundaries (in/out). Key decisions made.
Open decisions for the agent. File layout.
Links to: [[DDR-NNN]], [[DOM-NNN]], [[RAT-NNN]]

## Contract (from Pass 3: ○ Quality Advocate)
Observable outcomes. Verification commands. Quality constraints.
Failure modes. Acceptance criteria.
Links to: [[CON-NNN]]

## Agent Notes (from Pass 4: ◉ Agent)
Trust score breakdown. Required reads before execution.
Ambiguity flags (resolved or outstanding). Recommended model.
Events to emit during execution.
```

---

## Integration with the Loop

**Notice → Spec transition:** This protocol IS the transition. An intent enters; a spec exits. The knowledge base is queried throughout (Flow 2).

**Self-prompting, not manual authoring:** Brien doesn't write specs. He accepts intents and reviews the specs the protocol produces. He intervenes only when disambiguation signals surface.

**Persona alignment:** The four personas map to Brien's four-persona model (△◇○◉). Each persona has a defined role in the loop. The spec-shaping protocol makes that role concrete and executable.

**Knowledge Engine connection:** Every pass queries the compiled knowledge base. The richer the knowledge base, the better the specs. This is the practical payoff of compilation over retrieval — the personas have pre-compiled understanding to draw on, not just raw documents to search.

---

## What This Replaces

| Before | After |
|--------|-------|
| Brien writes specs manually in prose | System generates specs through persona interrogation |
| Agent guesses what Brien meant | Agent has structured dimensions covering role, task, goal, audience, context, style, structure, constraints, format, contract |
| Spec quality depends on Brien's energy | Spec quality depends on knowledge base richness + protocol rigor |
| Session drift when spec is underspecified | Readiness assessment catches ambiguity before execution |
| Brien reviews execution output | Brien reviews spec output (higher leverage — catch problems before building) |

---

*Spec-Shaping Protocol v1.0 — 2026-04-06*
*Insight trigger: Huryn's 10-part prompt structure → self-prompting with Intent's own personas*
