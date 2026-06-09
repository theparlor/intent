---
title: Productivity OS Layer Model — L1 Through L6
type: spec
maturity: draft
confidentiality: shareable
reusability: universal
domains:
  - consulting-operations
  - product-strategy
created: 2026-04-12
thought_leaders:
  - marty-cagan
  - matthew-skelton
  - manuel-pais
  - andrej-karpathy
  - chris-argyris
  - stafford-beer
  - john-kotter
  - mik-kersten
  - richard-rumelt
frameworks:
  - transformation-operating-system
summary: "How Intent's architecture — the loop, three layers, trust model, Knowledge Engine, and personas — manifests at six organizational altitudes from Personal OS to Enterprise OS."
depth_score: 7
depth_signals:
  file_size_kb: 43.2
  content_chars: 19215
  entity_count: 10
  slide_count: 0
  sheet_count: 0
  topic_count: 2
  has_summary: 1
vocab_density: 0.42
related_entities:
  - {pair: manuel-pais ↔ matthew-skelton, count: 382, strength: 0.698}
  - {pair: manuel-pais ↔ team-topologies, count: 344, strength: 0.884}
  - {pair: matthew-skelton ↔ team-topologies, count: 344, strength: 0.632}
  - {pair: marty-cagan ↔ teresa-torres, count: 291, strength: 0.419}
  - {pair: matthew-skelton ↔ mik-kersten, count: 233, strength: 0.373}
---
# Productivity OS Layer Model — L1 Through L6

> Intent isn't one operating system. It's a family of operating systems at different organizational altitudes. The architecture is the same — the loop, the three layers, the trust model. What changes is cadence, governance, knowledge scope, and the relationship between humans and agents.

**Status:** `draft`
**Created:** 2026-04-12
**Last touched:** 2026-04-12
**Intent:** INT-015
**Signal:** SIG-035

---

## 1. Intent

### What I Noticed

Intent's three-layer architecture (Compiled Knowledge Base → Transformation OS → Software Spec/Code) is powerful precisely because it's domain-agnostic. But "domain-agnostic" has been conflated with "scale-agnostic," and they aren't the same thing.

Brien is building tools at L1 (persona library, Knowledge Farm, Cowork plugin) and delivering consulting at L6 (Transformation Operating System, enterprise governance). The four-persona spec shaping protocol assumes L3 (a team with shared context). The federation spec assumes L4 (multiple teams coordinating across boundaries). But nobody has drawn the map that shows how these are the *same system operating at different altitudes.*

Think of it like a weather system. The physics are the same everywhere — thermodynamics, fluid dynamics, pressure gradients. But a sea breeze and a hurricane are profoundly different phenomena produced by those same physics at different scales. Intent's loop, trust model, and knowledge architecture are the physics. The layers are the scale at which those physics produce different organizational phenomena.

### Why It Matters Now

Three converging pressures:

1. **Product coherence.** Brien's work spans L1-L6 but lacks the connective tissue to explain why persona management and enterprise transformation are part of the same product family. This matters for the Intent site, consulting positioning, and course design.

2. **Market reality.** The AI productivity tool market is exploding at L1-L2 (individual AI workflows, personal knowledge management). Intent has an architecture that scales beyond this, but without the layer model, it looks like just another L1 tool or just another L6 consulting framework — never both.

3. **Design gaps.** L2 (independent builders) and L5 (department OS) are unaddressed. The layer model makes these gaps visible and designable.

### Desired Outcome

A practitioner, team lead, or enterprise sponsor can locate themselves on the L1-L6 model, understand what Intent provides at their altitude, see the path to adjacent layers, and trust that the architecture scales because it's the same architecture — not a different product at each level.

---

## 2. Shape

### The Six Layers

```
L6  ┌─────────────────────────────────────────────────┐
    │  ENTERPRISE OS                                   │
    │  Transformation governance, cross-department     │
    │  knowledge strategy, portfolio observability     │
L5  ├─────────────────────────────────────────────────┤
    │  DEPARTMENT OS                                   │
    │  Product organization governance, standard       │
    │  ontologies, autonomy ceilings, portfolio view   │
L4  ├─────────────────────────────────────────────────┤
    │  TEAM OF TEAMS                                   │
    │  Cross-team federation, Team API pattern,        │
    │  dependency health, boundary negotiation         │
L3  ├─────────────────────────────────────────────────┤
    │  TEAM OS                                         │
    │  Product trio + agents, shared .intent/,         │
    │  four-persona spec shaping, team dashboard       │
L2  ├─────────────────────────────────────────────────┤
    │  INDEPENDENT BUILDERS                            │
    │  Connected individuals, selective sharing,       │
    │  async coordination, shared reference artifacts  │
L1  ├─────────────────────────────────────────────────┤
    │  PERSONAL OS                                     │
    │  One person, one knowledge farm, one agent,      │
    │  continuous loop, maximum autonomy               │
    └─────────────────────────────────────────────────┘
```

### The Invariants (What Doesn't Change)

Across all six layers, the following architectural elements are constant:

1. **Three-layer architecture** — Compiled Knowledge Base → Transformation OS → Software Spec/Code exists at every altitude. What changes is scope, not structure.
2. **The loop** — Notice → Spec → Execute → Observe operates at every altitude. What changes is cadence.
3. **Trust/autonomy model** — L0-L4 autonomy levels apply at every altitude. What changes is who sets the thresholds and what the blast radius means.
4. **Event system** — OTel-compatible events are emitted at every altitude. What changes is aggregation scope.
5. **Work ontology** — Signal → Intent → Spec → Contract → Capability → Feature → Product applies at every altitude. What changes is the typical entry point and the governance around transitions.

### The Variables (What Changes By Layer)

Seven dimensions vary across the six layers. Each is specified in detail below.

---

## 2.1 Layer Definitions

### L1: Personal OS

**Scope:** One practitioner, one knowledge farm, one or more AI agents. The atomic unit of Intent.

**Archetype:** Brien running his consulting practice. A senior engineer with a personal Obsidian vault and Claude Code. A product manager building their own AI PM workflow.

**Knowledge Architecture:**
Personal knowledge farm — private compiled artifacts in a personal `knowledge/` directory. Sources include personal reading, conversation transcripts, meeting notes, bookmarks, and professional observations. The Knowledge Engine operates in single-tenant mode: one person's raw material compiled into one person's domain model.

Key characteristic: the knowledge base is *opinionated*. It reflects one person's synthesis, not a committee's consensus. This is a feature, not a bug — L1 knowledge is high-trust because it has a single author who can vouch for every artifact.

Federation: none required. The knowledge farm is self-contained. It may *export* artifacts to L2-L3 via selective sharing, but it has no upstream dependencies except publicly available reference material.

**Intent Loop Cadence:**
Continuous. Every conversation is a potential signal. The loop runs as fast as the practitioner thinks. There are no sprint boundaries, no standup ceremonies, no coordination costs.

Typical cadence: dozens of micro-loops per day (read something → notice a pattern → capture a signal → refine understanding). Larger loops (signal → intent → spec → execute) run on the natural rhythm of the practitioner's work, which might be hours or days.

**Trust/Autonomy Model:**
Maximum autonomy by default. At L1, the practitioner IS the governance. Most signals can run at L3-L4 autonomy (agent executes, human monitors or full autonomy) because:
- Blast radius is personal (only the practitioner's own files and workflows are affected)
- Reversibility is high (git revert, undo, regenerate)
- The practitioner has full context on their own domain

The trust formula still applies, but the inputs skew toward high trust: clarity is whatever the practitioner understands (no cross-team ambiguity), blast radius is bounded to personal scope, reversibility is maximal.

Exception: L0 actions that involve external communication (sending emails, posting to Slack, publishing content) still require the approval gate — even at L1, saying the wrong thing in public has unbounded blast radius.

**Persona Usage:**
Direct invocation. "What would Teresa say about this discovery approach?" is a tool call, not a team ritual. The practitioner accesses the full persona library as a personal advisory board.

At L1, personas serve as *thinking partners* — compensating for the individual's blind spots. A product-minded practitioner invokes the Design-Quality Advocate (○) persona to stress-test their spec. A technical architect invokes the Product-Minded Leader (◇) to check business alignment.

The 170+ expert personas (thought leaders like Cagan, Torres, Patton, Dunford) function as on-demand mentors. This is the AI PM OS course use case.

**Observability:**
Personal event log. Self-reflection is the primary observe mechanism. The practitioner reviews their own `events.jsonl`, notices patterns in their own signal capture (what topics keep recurring?), and adjusts their own loop.

Metrics are personal productivity metrics: signals captured per week, time from signal to spec, execution success rate, knowledge artifacts compiled. No team dashboards — just personal retrospection.

**Tools/Infrastructure:**
- Cowork (mobile/desktop dispatch)
- Claude Code (deep work sessions)
- Personal MCP servers (Knowledge Farm, Intent notice/spec/observe)
- Obsidian/Hermes (personal knowledge management feeding raw/)
- Git (single-player version control)
- Personal `.intent/` directory

**What Brien is building here:** Persona library, Knowledge Farm, Cowork plugin, auto-memory, AI PM OS course. **Status: ACTIVE.**

---

### L2: Independent Builders

**Scope:** Multiple individuals working separately but producing connected output. No shared backlog, no shared standup. Connected through shared artifacts, not shared process.

**Archetype:** Open source contributors to a shared repo. Freelance consultants collaborating on a client engagement. A research group where each member has their own knowledge farm but they share reference personas and domain models. Brien and a collaborator working on Intent from separate contexts.

**Knowledge Architecture:**
Independent knowledge farms with selective sharing. Each builder maintains their own L1 knowledge base. Shared artifacts exist in a common reference layer — shared personas, shared domain glossaries, shared research sources.

The key architectural question: what's the sharing primitive? At L2, it's the *artifact*, not the *base*. Builder A publishes a compiled persona. Builder B imports it into their own farm. Neither has write access to the other's knowledge base. Think git forks, not branches.

Federation model: peer-to-peer, selective. No inheritance hierarchy. Each builder chooses what to import and what to export. Conflicts are resolved by each builder independently — there is no canonical upstream (that's L3).

**Intent Loop Cadence:**
Daily to weekly. Async coordination. Each builder runs their own continuous L1 loop. Coordination happens through shared signal streams — builder A captures a signal that's visible to builder B, who may or may not act on it.

Sync points are event-driven, not calendar-driven: "I published a new spec" triggers a notification, not a meeting. The loop across builders is fundamentally async.

**Trust/Autonomy Model:**
Each builder sets their own autonomy levels within their own scope. Cross-builder actions (modifying shared artifacts, publishing to shared namespaces) require explicit agreement — either through a PR-like approval flow or pre-negotiated autonomy grants.

Trust is computed independently by each builder for their own signals. Shared signals inherit the lower of the two builders' trust assessments (conservative merge).

**Persona Usage:**
Shared persona library, independent invocation. Builders draw from a common pool of expert personas but invoke them in their own context. "What would Cagan say about this product decision?" uses the same persona artifact but applies it to each builder's distinct problem.

Shared personas serve as *alignment primitives* — when two builders both consult the same persona on the same question and get divergent answers, that's a signal worth investigating.

**Observability:**
Shared metrics, independent observation. Each builder has their own event log. A lightweight aggregation layer (shared dashboard, periodic digest) surfaces cross-builder patterns: where are signals converging? Where are specs diverging?

The observe layer at L2 is primarily about *coordination signals* — not team performance metrics.

**Tools/Infrastructure:**
- Shared Git repos (the coordination substrate)
- Shared MCP registry (common tool availability)
- Async communication (Slack, GitHub Issues, email)
- Independent `.intent/` directories with cross-references
- Shared `raw/` and selective `knowledge/` export/import

**What Brien is building here:** Not explicitly addressed. **Status: GAP.** The AI PM OS course and the Intent community (when it exists) will be the first L2 deployments.

---

### L3: Team OS

**Scope:** A product trio (PM, designer, engineer) or small team (3-8 people) with shared context, shared goals, and shared decision authority over a product area.

**Archetype:** A Cagan-style empowered product team. Brien's model team at an engagement. A startup founding team. Any team small enough that everyone can maintain shared context without formal coordination mechanisms.

**Knowledge Architecture:**
Team knowledge base with shared domain models and shared personas. The team maintains a single `knowledge/` directory with compiled artifacts that represent the team's shared understanding — not any individual's opinion, but the team's negotiated model of reality.

Key characteristic: knowledge artifacts at L3 have *team provenance*. A persona compiled by the team carries more weight than one compiled by an individual, because it's been through the four-persona interrogation protocol.

The team knowledge base inherits from Core (L4 federation) and may incorporate artifacts promoted from individual L1 farms. But team-compiled artifacts are the canonical versions within the team's scope.

**Intent Loop Cadence:**
Daily. The team's loop runs on the natural rhythm of collaborative work — typically one full loop (notice → spec → execute → observe) per day for small signals, weekly for larger intents.

Daily standup is replaced by daily signal review: what did we notice? Which signals should become intents? Which specs are ready for execution? What did we observe from yesterday's executions?

The four-persona spec shaping protocol (△ Shape, ◇ Outcome, ○ Contract, ◉ Readiness) runs synchronously within the team — this is where the methodology delivers the most immediate value.

**Trust/Autonomy Model:**
Team agrees on autonomy boundaries. The team configures `.intent/config.yml` with shared thresholds:
- Which signal types can agents auto-execute?
- What's the maximum blast radius for L3/L4 autonomy?
- Which team members can approve L2 actions?
- What circuit breakers apply?

Trust scoring at L3 incorporates team context: a signal about a shared service has higher blast radius (affecting the whole team) than the same signal at L1 (affecting only one person). The trust formula weights shift: blast radius and reversibility matter more because the consequence space is wider.

**Persona Usage:**
Four-persona spec shaping protocol. This is the primary L3 use case for personas:
- △ Practitioner-Architect shapes the technical approach
- ◇ Product-Minded Leader validates business alignment and outcomes
- ○ Design-Quality Advocate defines contracts and quality criteria
- ◉ AI Agent assesses execution readiness and automation potential

Expert personas (thought leaders) serve as external advisors during spec shaping. "Run this spec past the Torres lens — are we doing continuous discovery or discovery theater?"

At L3, personas shift from *thinking partners* (L1) to *process participants* — they have formal roles in the spec shaping workflow.

**Observability:**
Team dashboard with shared OTel traces. The observe layer at L3 tracks:
- Signal velocity (how fast signals move through the loop)
- Spec quality (what percentage of specs pass contract verification on first execution?)
- Execution efficiency (agent success rate, human intervention frequency)
- Learning rate (how often do observations update the knowledge base?)

The team dashboard is the primary artifact of the Observe product at L3.

**Tools/Infrastructure:**
- Shared `.intent/` directory (the team's single source of truth for work artifacts)
- Team MCP servers (shared notice/spec/observe/knowledge)
- Collaborative tools (shared IDE sessions, pair programming, design tools)
- Shared `raw/` and `knowledge/` directories
- Team event log (`events.jsonl`) aggregating all team members' and agents' events

**What Brien is building here:** Intent methodology, four-persona spec shaping protocol, signal trust framework. **Status: DEFINED.** This is the core product.

---

### L4: Team of Teams

**Scope:** Multiple L3 teams coordinating across boundaries. Team Topologies territory — stream-aligned teams, platform teams, enabling teams, complicated subsystem teams.

**Archetype:** A product group with 3-5 teams working on a shared product. Multiple Cagan-style empowered teams that need to coordinate without creating a coordination tax. Brien's larger consulting engagements where multiple teams adopt Intent simultaneously.

**Knowledge Architecture:**
Federated knowledge across team boundaries. This is the architecture described in `knowledge-engine/spec/federation.md`: inherit down from Core, promote up generalizable learnings, never leak sideways across confidentiality boundaries.

Each L3 team maintains its own knowledge base. The L4 layer provides:
- **Shared ontologies** — agreed-upon domain models that span team boundaries (the "ubiquitous language" in DDD terms)
- **Cross-team personas** — personas that represent shared users or stakeholders
- **Dependency maps** — which team's knowledge artifacts depend on which other team's artifacts
- **Promotion protocol** — how a team-specific learning becomes a shared asset

Key characteristic: L4 is where the federation model earns its keep. Without it, teams either duplicate knowledge (expensive) or share everything (dangerous). Federation gives them the third option: structured, bounded, governed sharing.

**Intent Loop Cadence:**
Weekly to sprint-cadence. Cross-team coordination can't run daily without becoming a standup-of-standups (which is the ceremony tax Intent exists to eliminate).

Instead, L4 operates on signal propagation: when a team's signal has cross-team implications (a dependency change, an API contract modification, a shared persona update), it propagates to affected teams as a new signal in their stream. Teams receive and triage cross-team signals at their own L3 cadence.

Synchronous L4 coordination happens at natural decision points: architecture review boards (ARBs), cross-team spec shaping for shared capabilities, retrospectives that span team boundaries.

**Trust/Autonomy Model:**
Autonomy levels negotiated at team boundaries. Each L3 team governs its own internal autonomy. L4 governance applies at the boundary:
- **Team API pattern** (Pais/Skelton): each team publishes a boundary contract — what it provides, what it requires, what changes require notification
- **Cross-team blast radius**: signals that affect multiple teams automatically escalate to lower autonomy levels (higher human involvement)
- **ARB as governance mechanism**: architectural changes that span team boundaries require multi-perspective review using the persona panel

Trust at L4 is inherently lower than at L3 because blast radius is larger and reversibility is harder (rolling back a cross-team change requires coordination).

**Persona Usage:**
Cross-team ARB review using the persona panel. At L4, the four Intent personas take on organizational roles:
- △ Practitioner-Architect reviews system-level technical coherence
- ◇ Product-Minded Leader ensures cross-team work aligns with product strategy
- ○ Design-Quality Advocate enforces consistency of user experience across teams
- ◉ AI Agent assesses cross-team automation opportunities and dependency health

Expert personas serve as *external perspective* on organizational decisions: "What would Skelton say about these team boundaries?"

**Observability:**
Cross-team metrics and dependency health. The observe layer at L4 tracks:
- Cross-team signal propagation time (how fast does a dependency change reach affected teams?)
- Boundary contract compliance (are teams honoring their APIs?)
- Federated knowledge health (are team knowledge bases diverging from shared ontologies?)
- Cross-team execution coordination (how often do cross-team specs require rework?)

**Tools/Infrastructure:**
- Federated `.intent/` across repos (each team's repo + shared cross-team coordination repo)
- Team API pattern (boundary contracts in a shared location)
- Cross-team MCP servers (or federated access to team-level servers)
- Shared observability infrastructure (aggregated OTel traces, cross-team dashboard)

**What Brien is building here:** Federation model, team boundaries, Knowledge Engine federation spec. **Status: SPECCED.**

---

### L5: Department OS

**Scope:** A product organization or business unit. Multiple L4 team-of-teams groups unified by a shared strategic direction, shared budget, and shared leadership.

**Archetype:** A VP of Product's organization with 20-50 people across multiple product areas. An R&D division. A business unit with its own P&L. The organizational level where "product strategy" and "portfolio management" become distinct activities.

**Knowledge Architecture:**
Department-wide knowledge governance with standard ontologies. At L5, knowledge management becomes a strategic function, not just a team practice:

- **Standard ontologies** — department-level agreement on domain models, persona definitions, and terminology. Not prescribed by fiat, but compiled from cross-team federation and curated by knowledge stewards.
- **Knowledge governance** — who can promote artifacts to department-wide status? What review process ensures quality? How are contradictions between team-level knowledge bases resolved?
- **Portfolio-level compilation** — the department maintains compiled artifacts that span product areas: market landscape models, competitive intelligence, customer segment maps, technology radar.

Federation model: the department is the "Core" in the `inherit down, promote up, never leak sideways` pattern. L3/L4 teams inherit department standards. Teams promote generalizable learnings through a governed pipeline.

**Intent Loop Cadence:**
Monthly to quarterly. The department-level loop operates on strategic review cycles:
- **Notice:** Strategic signals collected from L3/L4 signal streams, market research, executive input, customer advisory boards
- **Spec:** Strategic initiatives shaped through multi-team spec process (think "bets" in Cagan's terminology)
- **Execute:** Initiatives decomposed to L4/L3 teams for execution
- **Observe:** Portfolio health reviewed monthly, strategic direction reviewed quarterly

The department loop is not about individual features or bug fixes — it's about strategic direction, resource allocation, and organizational learning.

**Trust/Autonomy Model:**
Department-level governance sets autonomy ceilings. The department defines:
- Maximum autonomy level by signal category (e.g., "no L4-full-autonomy changes to customer-facing APIs")
- Mandatory review triggers (e.g., "any spec affecting more than 3 teams requires ARB approval")
- Escalation paths (e.g., "signals with estimated impact >$100K route to department leadership")
- Risk tolerance by product area (e.g., "the mature product has lower autonomy ceilings than the experimental product")

Teams still set their own internal autonomy within these ceilings. L5 governance constrains the ceiling, not the floor.

**Persona Usage:**
Persona-informed strategy review. At L5, personas serve a different function than at L1-L4:
- **Strategic personas** — department-level customer personas that represent market segments, not individual users. These are compiled from L3 team personas but abstracted to strategic level.
- **Advisory board pattern** — expert personas (thought leaders) invoked as a strategic advisory board: "Run our portfolio strategy past the Cagan lens. Are we organizing around empowered teams or are we just reshuffling the org chart?"
- **Cross-product persona panel** — ensuring that product decisions across teams serve a coherent user experience

**Observability:**
Department OKRs and portfolio health. The observe layer at L5 tracks:
- Portfolio health (which product areas are thriving, which are struggling?)
- Strategic signal velocity (how quickly do market signals reach the teams that need them?)
- Knowledge compilation rate (is the department getting smarter over time, or just busier?)
- Autonomy utilization (are teams operating at their granted autonomy levels, or are they bottlenecked on approvals?)
- Investment efficiency (what's the ratio of strategic intent to realized outcome?)

**Tools/Infrastructure:**
- Intent MCP servers as department infrastructure (hosted, multi-tenant, access-controlled)
- Portfolio-level dashboards (aggregated from L3/L4 team dashboards)
- Knowledge governance tooling (approval workflows for artifact promotion, ontology management)
- Strategic planning tools (roadmap aggregation, resource allocation, bet tracking)

**What Brien is building here:** Not explicitly addressed. **Status: GAP.** L5 is the natural consulting engagement scope — Brien's Subaru and F&G engagements are L5 deployments in practice, but without the formal model. Defining L5 explicitly will strengthen those engagements.

---

### L6: Enterprise OS

**Scope:** The entire enterprise. Multiple L5 departments, cross-functional governance, enterprise-wide knowledge strategy, transformation program management.

**Archetype:** Brien's Transformation Operating System concept. A Fortune 500 company's AI transformation program. An enterprise where multiple departments are adopting Intent-style operating models and need coherence across the whole organization.

**Knowledge Architecture:**
Enterprise knowledge strategy with cross-department compilation. At L6, knowledge is a *strategic asset* managed at the enterprise level:

- **Enterprise knowledge graph** — compiled understanding that spans departments: how does the supply chain department's domain model relate to the sales department's customer model?
- **Cross-department compilation** — the Knowledge Engine operates as enterprise infrastructure, compiling knowledge across department boundaries. This is Karpathy's "compilation over retrieval" at organizational scale.
- **Knowledge strategy** — which domains are core to enterprise competitiveness? Where should the enterprise invest in deeper knowledge compilation? Where is knowledge fragmented across departments?

Federation model: enterprise Core sits above department Cores. Enterprise-level ontologies (brand voice, company values, market positioning, regulatory framework) are inherited by all departments. Department-specific knowledge stays bounded but can be promoted to enterprise level through governed pipelines.

**Intent Loop Cadence:**
Quarterly to annual. The enterprise loop operates on transformation governance cycles:
- **Notice:** Enterprise-wide signals from market shifts, regulatory changes, competitive moves, technology disruptions, customer behavior changes
- **Spec:** Transformation initiatives shaped at the enterprise level (multi-year, multi-department)
- **Execute:** Initiatives decomposed to L5 departments and L4 team-of-teams
- **Observe:** Transformation progress reviewed quarterly, strategic direction reviewed annually

The enterprise loop is the slowest cadence but the highest leverage. A single enterprise-level notice ("the market is shifting from product-led to platform-led") cascades through every layer below.

**Trust/Autonomy Model:**
Enterprise risk framework constrains all layers. At L6, the trust model interfaces with enterprise governance:

- **Enterprise risk tolerance** — defines the global floor for trust thresholds. No team, regardless of internal autonomy, can exceed enterprise risk limits.
- **Compliance constraints** — regulatory requirements (SOX, GDPR, industry-specific) become hard constraints on autonomy. Some actions are L0-human-drives regardless of computed trust score.
- **Audit trail** — enterprise observability requires full traceability from L6 strategic intent through L5/L4/L3 execution to L1 individual action. This is Intent's event system at full scale.
- **Cross-department governance** — changes that affect multiple departments trigger enterprise-level review, analogous to L4 ARBs but at organizational scale.

**Persona Usage:**
Persona panel as enterprise advisory board. At L6, the persona system serves executive and transformation functions:
- **Enterprise personas** — represent organizational archetypes (the field sales rep, the warehouse operator, the customer success manager) compiled from department-level personas
- **Transformation advisory board** — expert personas invoked as strategic advisors: "What would Stafford Beer say about our organizational cybernetics? Are we building viable systems or just adding complexity?"
- **Cross-department perspective** — the four Intent personas (△◇○◉) operate at enterprise level to review transformation initiatives

**Observability:**
Enterprise transformation metrics. The observe layer at L6 tracks:
- Transformation progress (are enterprise-level intents translating into departmental action?)
- Cross-department knowledge health (is knowledge flowing or siloing?)
- Enterprise autonomy maturity (is the organization becoming more autonomous over time, or more dependent on human bottlenecks?)
- Strategic outcome metrics (Seiden: "what behavior changed? what became true that wasn't?")
- Grafana dashboards, executive scorecards, board-level reporting

**Tools/Infrastructure:**
- Hosted Knowledge Engine (multi-tenant, enterprise-grade, SLA-backed)
- Enterprise observability (aggregated OTel traces across all layers, Grafana/Tempo/Loki stack)
- Governance platform (enterprise-level approval workflows, compliance tracking, audit trail)
- Executive dashboards (portfolio-of-portfolios view)
- Enterprise MCP infrastructure (centrally managed, access-controlled, federated)

**What Brien is building here:** Transformation Operating System concept, Intent site positioning, enterprise consulting framework. **Status: ACTIVE** at the conceptual level. The Intent site tells this story. The consulting practice delivers it.

---

## 2.2 Cross-Layer Data Flows

The layers are not isolated strata — they're coupled through three directional data flows. These flows are what make Intent a coherent system rather than six disconnected operating models.

### Signals Flow UP

Observations at lower layers propagate upward as signals at higher layers. This is how the organization *notices*.

```
L1: Brien notices a pattern in Subaru support tickets
    ↓ captures as personal signal
L3: Brien's team reviews, recognizes cross-product relevance
    ↓ promotes to cross-team signal
L4: Cross-team triage identifies strategic implication
    ↓ escalates to department signal
L5: Department leadership reviews as strategic signal
    ↓ flags for enterprise attention
L6: Enterprise transformation team incorporates into strategic model
```

**Mechanics:**
- Signal promotion is explicit, not automatic. Each layer decides whether to promote.
- Promoted signals carry their provenance chain (who noticed, when, at what layer).
- Trust scores are recomputed at each layer (blast radius changes, clarity may change).
- Signals can skip layers when blast radius warrants it (an L1 security observation may jump directly to L5/L6).

**Anti-pattern:** Signals that propagate upward without recomputing trust. An L1 signal with trust 0.9 (low personal blast radius) should not retain 0.9 at L4 (high cross-team blast radius).

### Governance Flows DOWN

Policies, constraints, and autonomy ceilings propagate downward. This is how the organization *governs*.

```
L6: Enterprise sets risk tolerance: "no autonomous customer data changes"
    ↓ encoded as enterprise autonomy ceiling
L5: Department translates: "customer-facing API changes are L0-L1 max"
    ↓ encoded as department config.yml overlay
L4: Cross-team boundary: "shared schema changes require ARB approval"
    ↓ encoded as team API contract
L3: Team configures: .intent/config.yml inherits all upstream ceilings
    ↓ computed autonomy = min(computed_trust, layer_ceiling)
L1: Individual's personal autonomy bounded by all upstream constraints
```

**Mechanics:**
- Governance is inherited, not copied. Each layer inherits from the layer above and can tighten (never loosen) constraints.
- `.intent/config.yml` supports a `governance` block with `inherits_from` references.
- Autonomy at any layer = min(computed_trust, local_ceiling, inherited_ceiling).
- Circuit breakers at higher layers override lower-layer autonomy.

**Anti-pattern:** Governance that specifies *how* (micromanagement) rather than *limits* (boundary-setting). L6 should say "no autonomous customer data changes," not "use this specific approval workflow for customer data changes."

### Knowledge Flows LATERALLY

Domain knowledge flows between teams at the same altitude through the federation model. This is how the organization *learns*.

```
L3 Team A                     L3 Team B
  │                             │
  ├── compiles persona PER-042  │
  │                             │
  ├── promotes to L4 shared ──→ L4 federation layer
  │                             │
  │                   ←── Team B imports PER-042
  │                             │
  │                   ←── Team B enriches with own data
  │                             │
  │              Team B promotes enriched version to L4
  │                             │
  ├── Team A receives enriched version
```

**Mechanics:**
- Lateral flow operates through the L4 federation layer. Teams don't share directly (that would violate boundary contracts).
- The federation protocol from `knowledge-engine/spec/federation.md` governs: inherit down, promote up, never leak sideways.
- Knowledge artifacts carry origin tracking (`origin: human | agent | synthetic`) and provenance chains.
- Contradictions between team-level artifacts are surfaced as signals, not silently resolved.

**The Double-Loop Learning Connection:**
Cross-layer knowledge flow is where Argyris's double-loop learning happens at organizational scale. An L1 observation that contradicts an L5 strategic assumption doesn't just fix the immediate execution (single-loop) — it questions the assumption itself (double-loop). The vertical signal propagation path carries the observation upward until it reaches the layer where the assumption lives. This is flow 5 from the three-layer architecture: Observe → Knowledge.

---

## 2.3 Relationship to Existing Intent Architecture

This layer model doesn't replace anything — it's the altitude dimension that the existing architecture implicitly assumes but never formalizes.

| Existing Concept | How Layers Extend It |
|-----------------|---------------------|
| Three-layer architecture (KB → TOS → Software) | Exists at every layer. Scope of each tier changes by altitude. |
| The loop (Notice → Spec → Execute → Observe) | Operates at every layer. Cadence varies from continuous (L1) to annual (L6). |
| Trust/autonomy (L0-L4 levels) | Applies at every layer. Threshold configuration and blast radius computation vary. Governance inheritance adds ceiling constraints. |
| Work ontology (Signal → ... → Product) | Same ontology at every layer. Typical entry point shifts (L1 starts from Signal, L6 from Intent or Product). |
| Four personas (△◇○◉) | Present at every layer. Role shifts from thinking partner (L1) to process participant (L3) to organizational function (L5-L6). |
| Federation (inherit down, promote up, never leak sideways) | Becomes the cross-layer knowledge flow mechanism. Federation was designed for L4; this spec extends it to all boundaries. |
| Knowledge Engine | Shared infrastructure across all layers. Deployment topology varies (local at L1, hosted at L5-L6). |
| Event system (OTel-compatible) | Emits at every layer. Aggregation scope widens with altitude. |

---

## 2.4 Summary Matrix

| Dimension | L1 Personal | L2 Builders | L3 Team | L4 Team of Teams | L5 Department | L6 Enterprise |
|-----------|------------|------------|---------|-----------------|--------------|---------------|
| **Scope** | 1 person | N individuals, separate context | 3-8, shared context | Multiple L3 teams | 20-50+, shared strategy | Whole org |
| **Knowledge** | Personal farm | Selective sharing | Shared team KB | Federated across teams | Standard ontologies | Enterprise knowledge graph |
| **Loop cadence** | Continuous | Daily-weekly async | Daily | Weekly-sprint | Monthly-quarterly | Quarterly-annual |
| **Autonomy default** | High (L3-L4) | Per-builder | Team-configured | Boundary-negotiated | Ceiling-governed | Risk-framework-constrained |
| **Persona role** | Thinking partner | Shared library | Process participant | Cross-team ARB | Strategic advisor | Enterprise advisory board |
| **Observe focus** | Self-reflection | Coordination signals | Team dashboard | Dependency health | Portfolio health | Transformation metrics |
| **Tools** | Cowork, Claude Code, personal MCP | Shared git, async comms | Shared .intent/, team MCP | Federated repos, Team API | Dept infrastructure | Hosted KE, enterprise observability |
| **Brien's status** | ACTIVE | GAP | DEFINED | SPECCED | GAP | ACTIVE |

---

## 3. Contract

### Done When

- [ ] All six layers (L1-L6) are defined with scope, knowledge architecture, loop cadence, trust model, persona usage, observability, and tools
- [ ] Cross-layer data flows are specified: signals UP, governance DOWN, knowledge LATERALLY
- [ ] Each layer references existing Intent architecture elements (loop, trust, federation, Knowledge Engine) and explains how they manifest at that altitude
- [ ] L2 and L5 are explicitly called out as gaps with enough definition to begin designing for them
- [ ] The spec is usable as a consulting deliverable — a client at any layer can locate themselves and see the path to adjacent layers
- [ ] The layer model is consistent with all existing specs: federation, trust framework, spec shaping protocol, three-layer architecture
- [ ] Brien can present this to a client and use it to scope an engagement from L1 personal coaching through L6 enterprise transformation

### Smoke Test

```
# Read the spec and verify:
# 1. Each layer section has all seven dimensions defined
# 2. Cross-layer flows reference specific mechanisms (trust recomputation, federation protocol, governance inheritance)
# 3. "Brien's status" field identifies L2 and L5 as GAPs
# 4. No new concepts introduced that duplicate existing architecture elements
grep -c "## L[1-6]:" spec/SPEC-productivity-os-layers.md  # should be 0 (uses ### headers)
grep -c "### L[1-6]:" spec/SPEC-productivity-os-layers.md  # should be 6
grep -c "Status: GAP" spec/SPEC-productivity-os-layers.md  # should be 2
grep -c "Status: ACTIVE" spec/SPEC-productivity-os-layers.md  # should be 2
```

### Failure Modes to Watch

- **Layer rigidity** — treating layers as a strict hierarchy when in practice organizations skip, merge, or straddle layers. The spec should emphasize that layers are a framework, not a prescription.
- **New concept proliferation** — introducing new mechanisms instead of showing how existing ones (loop, trust, federation) vary by altitude. Every dimension should trace back to something that already exists in Intent.
- **L3 myopia** — over-specifying L3 (where Intent is most developed) at the expense of L1-L2 (where the market is hottest) or L5-L6 (where the consulting revenue is).
- **Cross-layer flow hand-waving** — describing flows in abstract terms without specifying the concrete mechanisms (trust recomputation, federation protocol, config inheritance).

### Observability

- Client engagement scoping references specific layers
- Intent site IA maps to layer model (L1 for "The Build" practitioners, L3-L4 for "The System" teams, L6 for "The Story" leaders)
- Persona library, Knowledge Farm, and Cowork plugin documentation references L1
- Federation spec and team boundary documentation references L4
- New specs for L2 and L5 emerge as follow-on intents

---

## Notes

**Intellectual lineage:** This spec draws from Team Topologies (Pais/Skelton) for the organizational altitude concept, Stafford Beer's Viable System Model for the recursive governance pattern, and Christopher Alexander's pattern languages for the idea that the same patterns operate at different scales.

**Connection to the three pillars (Intent site IA):**
- "The Story" speaks to L5-L6 buyers (department/enterprise leaders)
- "The System" speaks to L3-L4 buyers (team leads, architects)
- "The Build" speaks to L1-L2 buyers (practitioners, independent builders)

**Connection to consulting practice:**
- L1 coaching: AI PM OS course, personal productivity consulting
- L3 team workshops: Intent methodology adoption, four-persona protocol training
- L4-L5 organizational consulting: Federation setup, governance design, knowledge architecture
- L6 transformation programs: Full Transformation Operating System engagement

**Open question for Brien:** Should the layer model be the primary organizing principle for the Intent product roadmap? Currently the roadmap is organized by loop phase (Notice, Spec, Execute, Observe). An altitude-first organization (L1 → L2 → L3 → ...) might better reflect the go-to-market strategy of starting with practitioners and expanding outward.

**Adjacent signals to investigate:**
- Dex Horthy's "harness engineering" — independent validation of L1-L2 as a market
- Ethan Mollick's research on individual AI productivity — L1 evidence base
- Team Topologies community — L4 validation and potential collaboration
- Stafford Beer's Viable System Model — L5-L6 governance pattern deeper than what's specified here
