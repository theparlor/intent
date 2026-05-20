---
title: External Pattern Analysis Index
type: index
updated: 2026-05-08
depth_score: 4
depth_signals:
  file_size_kb: 20.8
  content_chars: 19672
  entity_count: 0
  slide_count: 0
  sheet_count: 0
  topic_count: 0
  has_summary: 0
vocab_density: 0.31
purpose: Maps external frameworks and patterns to Intent architecture decisions and adoption roadmap
---
# External Pattern Analysis Index

These reference documents analyze external frameworks, articles, and open-source projects against the Intent framework architecture. They surface specific adoption recommendations and validate existing architectural decisions.

## Documents

### 1. Rohit's 10 Production Agent Principles
**File:** reference/rohit-production-agent-principles-analysis.md
**Source:** @rohit4verse, "How to Build a Production-Grade AI Agent" (Feb 2026)
**Key finding:** All 10 principles map cleanly onto Intent's four-phase loop. Validates Intent as a production architecture pattern.
**Adopt immediately:** Structured error payloads in MCP tools, explicit completion conditions as code, field-level data classification
**Related signals:** SIG-031, SIG-032, SIG-033, SIG-034

### 2. Dex Horthy's Context Engineering & 12 Factor Agents
**File:** reference/dex-horthy-context-engineering-analysis.md
**Source:** @dexhorthy, HumanLayer founder, multiple repos
**Key finding:** The 40% context rule and harness engineering taxonomy directly apply to persona loading and Cowork plugin design.
**Adopt immediately:** Evaluate slopfiles plugin, apply context budget to persona loading, design plugin with harness taxonomy
**Related signals:** SIG-030 (Cowork plugin), persona loading optimization

### 3. Hermes/Obsidian Three-Tier Memory System
**File:** reference/hermes-obsidian-memory-analysis.md
**Source:** Community post on AI assistant long-term memory
**Key finding:** Validates Intent's three-layer architecture from a solo-practitioner starting point. Surfaces implementable patterns for scheduled automation and memory hygiene.
**Adopt immediately:** Morning briefing pipeline via scheduled task, 67% capacity trigger for memory promotion, USER.md/MEMORY.md separation
**Related signals:** Observe phase automation, auto-memory hygiene

### 4. AI-Native PM OS (Vishal Jaiswal Course)
**File:** reference/ai-native-pm-os-analysis.md
**Source:** [github.com/vishalmdi/ai-native-pm-os](https://github.com/vishalmdi/ai-native-pm-os) — 11-module, 63-lesson hands-on Claude Code course for PMs
**Key finding:** Validates Intent's core thesis from the grassroots: PMs are already building ad-hoc operating systems with CLAUDE.md hierarchies, file-based memory, and agent workflows. Intent provides the architecture that makes these patterns systematic and team-scale. The course's PRD workflow (Seed→Outline→Draft→Critique→Polish) closely parallels Intent's spec-shaping protocol.
**Adopt immediately:** Meridian company context template for engagement deliverables, executive one-pager structure (Situation→Opportunity→Evidence→Not Doing→Ask→Cost of Inaction), JTBD extraction pipeline from existing research
**Related patterns:** CLAUDE.md hierarchy as methodology, anti-style.md negative constraints, "Context > Prompting" as named design axiom, A/B test pre-registration discipline

### 5. CodeBurn — AI Coding Token Observability (AgentSeal)
**File:** reference/codeburn-analysis.md
**Source:** [github.com/getagentseal/codeburn](https://github.com/getagentseal/codeburn) — MIT, npm package, 3,900+ stars in 13 days
**Key finding:** Read-only cost observability tool that already reads Cowork/Claude Desktop session data from disk. Fills the empirical gap in Brien's model mixing architecture decision (Opus for synthesis vs Sonnet for retrieval). Provides per-session, per-model, per-task-category cost breakdown with one-shot success rates and cache hit tracking. JSON export can bridge into Intent's observations pipeline.
**Adopt immediately:** `npm install -g codeburn`, run for one week alongside Cowork dispatch enrichment, use `codeburn compare` to get empirical Opus vs Sonnet data, evaluate `optimize` for Cowork plugin waste patterns
**Related patterns:** Observe phase (Flow 5), Rohit's Principle 9 (observability), model mixing architecture, persona enrichment cost tracking

### 6. Enterprise AI Guides — Competitive Landscape Analysis (7 Guides)
**File:** reference/enterprise-ai-guides-analysis.md
**Sources:** Techpresso Free Guide (2025), Snowflake "A Practical Guide to AI Agents" (Mar 2025), PagerDuty "2026 State of AI-First Operations" (Mar 2026), Airtable AI Guides & Academy (2025-2026), Splunk "5 Big Myths of AI and Agentic AI Debunked" (2025), Splunk "State of Observability 2025" (2025), Confluent "Event-Driven Design for Agents and Multi-Agent Systems" (Apr 2025)
**Key finding:** All seven guides stop short of the operating model question. They now span a complete maturity curve from 101 to 301 across three Level 3 perspectives: outcomes measurement (PagerDuty), observability-as-business-catalyst (Splunk), and event-driven agent architecture (Confluent). None addresses the 401-level question: how to redesign team operating models when AI collapses implementation time. Intent sits atop all of them. Splunk's 1,855-person survey provides the hardest data: 65% say observability influences revenue, 64% say it impacts product roadmaps, 54% cite signal quality as the #1 ROI driver. Confluent's four multi-agent design patterns (Orchestrator-Worker, Hierarchical, Blackboard, Market-Based) directly validate Intent's architecture — the Blackboard pattern IS the Knowledge Engine.
**Adopt immediately:** Splunk's vocabulary ("business catalyst," "observability-as-code," "signal quality over signal volume"), Splunk's benchmark data (65% revenue impact, 125% ROI for leaders, 18% agentic AI adoption), Confluent's agents-as-microservices analogy, Confluent's Blackboard pattern as validation of Knowledge Engine. Intent's event schema should be Kafka-compatible for future hosted-mode migration. Call Intent's event system the "nervous system" of the loop. Add business context tags to events. Define formal event schema with validation rules.
**Market gap:** No one connects observability insights to operating model decisions. Splunk shows observability data influences product roadmaps but doesn't say HOW teams should change. Confluent shows how to architect event-driven agents but doesn't address what humans should do differently. Intent bridges: observe → notice → spec → execute → observe, with humans riding the loop.
**Related signals:** Observe phase (Splunk OTel validation, PagerDuty learning loop), event architecture (Confluent patterns), Intent site positioning, GTM strategy, hosted-mode event design, schema registry concept for events.jsonl

### 7. Hannah Stulberg's Team OS (via Aakash Gupta)
**File:** reference/aakash-gupta-team-os-analysis.md
**Sources:** Aakash Gupta Substack note (Apr 9, 2026), Hannah Stulberg Substack note (Apr 16, 2026), team-os-example-repo on GitHub
**Key finding:** A DoorDash PM independently built and named a "Team OS" — a shared GitHub repo serving as the knowledge substrate for a 20-person cross-functional team. Maps directly to Intent's L3 (Team OS) layer. Validates the term, the architecture pattern (CLAUDE.md hierarchy as compiled knowledge at team scope), and the market (Maven workshop selling at $200). Crucially, Team OS has no loop, no trust model, no signal capture, no observability, and no compilation — precisely the layers Intent adds.
**Adopt immediately:** "Launch gate" as L3 governance pattern (no feature ships without knowledge artifacts), progressive context loading by depth (3% context per query), folder ownership as lightweight knowledge stewardship model, "context bottleneck" as L3 problem framing
**Related signals:** SIG-038, INT-015, SPEC-productivity-os-layers

### Cross-Cutting Insight: Multi-Model Adversarial Synthesis (SIG-036)
**Signal:** `.intent/signals/2026-04-12-multi-model-adversarial-synthesis.md`
**Derived from:** Pawel Huryn (multi-LLM gateway), Dex Horthy (context engineering), LLM landscape analysis
**Key finding:** The multi-model gateway pattern (LiteLLM/OpenRouter) is not just cost optimization — it's a **quality assurance mechanism**. Running the same persona corpus or spec review through two frontier models and comparing outputs exposes sycophancy and optimistic synthesis that single-model validation cannot detect. Three applications: persona synthesis cross-validation, spec-shaping with genuine cognitive diversity (different models for different personas in the four-persona review), and depth score validation (independent scoring reveals where a model's synthesis was optimistic rather than evidence-based). Connects to depth scale v2.0 — cross-MODEL validation extends the concept of cross-persona validation (depth 17).
**Adopt:** Add optional "adversarial verification" step to persona synthesis pipeline; enable model-per-persona-role in spec-shaping protocol config

## Synthesis: What These Ten Sources Agree On

1. **Context is a scarce resource.** All four systems manage context budgets explicitly. Rohit says 40-50% overhead if you don't compress. Dex says 40% window max. Hermes uses a 67% trigger. AI-Native PM OS teaches token economics as a financial decision (Module 0.8). Intent's compilation model is the architectural answer but needs a runtime budget checker.

2. **Memory needs tiers.** Hot (per-session) → compiled (persistent reference) → event stream (timeline). All four systems arrive at this independently. AI-Native PM OS uses global/project/feature CLAUDE.md hierarchy. Intent's three-layer architecture (Knowledge Base → Transformation OS → Software) maps cleanly.

3. **Security must be mechanical, not trust-based.** Rohit says security outside the LLM loop. Dex says hooks are code and can't be argued with. Hermes says never delete without confirmation. AI-Native PM OS says "isolate the work" (always write to CLAUDE-OUTPUTS/, never overwrite active docs). Intent's L0-L4 trust levels and tool-level redaction are the framework response.

4. **Scheduled automation closes the loop.** Hermes has cron-driven briefings. Rohit has circuit breakers and drift monitoring. AI-Native PM OS has automated weekly digests via Cowork Dispatch. CodeBurn's menubar + auto-refresh provide passive monitoring. Intent specs the observe phase but hasn't implemented always-on processing. This is the biggest implementation gap.

5. **Multi-perspective critique produces better specs.** AI-Native PM OS uses role-based critique (engineer/designer/exec). Intent uses persona-based interrogation (△◇○◉). Both arrive independently at the same insight: a single-pass draft is never sufficient. The spec must survive pressure from multiple angles.

7. **Cross-model disagreement is a quality signal, not noise.** When two frontier models synthesize the same corpus differently, the delta reveals sycophancy and optimistic bias that single-model validation cannot detect. The multi-provider gateway (Pawel) + compiled artifacts (Dex) + multiple frontier models (landscape) combine into an adversarial synthesis pattern where model diversity becomes a quality assurance mechanism. (SIG-036)

6. **Cost observability is table stakes for agent-heavy workflows.** CodeBurn's explosive adoption (3,900 stars in 13 days) proves the demand. When agents are burning $50-200/day across parallel dispatch tasks, you need the same cost visibility you'd expect from cloud infrastructure. CodeBurn provides this passively (read-only, no proxy). Intent's Observe phase should treat token cost as a first-class observation metric alongside signal velocity and knowledge freshness.

8. **The market stops one level short of the operating model.** Enterprise AI guides address tools (101), platform deployment (201), workflow-embedded AI (251, Airtable), and measurement (301) — but none addresses the 401-level question of how to redesign team operating models for AI-collapsed execution timelines. Even with seven guides analyzed (adding Splunk Myths at 151, Splunk Observability at 301, and Confluent at 301), the pattern holds: three different Level 3 perspectives (outcomes, observability, architecture) and still no one connects them to operating model redesign. Intent fills the gap.

9. **Compilation beats retrieval, even when vendors don't use the term.** Airtable's "connected data" thesis — that AI output quality is a function of data connectivity across relational structures — independently validates Intent's "compilation over retrieval" principle. Their Field Agents compile understanding at the record level; Intent compiles at the domain level. Same architectural insight, different scope. This makes "connected data" a useful accessible synonym when explaining compilation to non-technical audiences.

10. **Signal quality > signal volume, and the data proves it.** Splunk's 1,855-person survey finds that 54% cite quality of alert detections as the #1 driver of observability ROI. Not volume, not speed — quality. And 73% experienced outages from suppressed alerts (ignoring low-quality signals). This directly validates Intent's trust scoring: signals need quality scores (confidence, trust) to route correctly, and no signal should be silently dropped. The Splunk data gives Intent empirical ammunition for the trust framework.

11. **Agents ARE the new microservices, and they need the same evolution.** Confluent's core insight — that AI agents function like microservices and need the same shift from request/response to event-driven communication — is the architectural foundation Intent builds on without naming it. Intent's loop phases (Notice, Spec, Execute, Observe) are specialized agents communicating through events. The four multi-agent patterns (Orchestrator-Worker, Hierarchical, Blackboard, Market-Based) all map to Intent's architecture. The Blackboard pattern IS the Knowledge Engine.

12. **Observability is becoming a business function, not a technical one.** Splunk's data shows 65% of respondents say observability positively influences revenue, 64% say it impacts product roadmaps. Leaders generate 125% annual ROI. OTel power users are 3x more likely to significantly impact employee productivity. This reframes Intent's Observe phase: it's not just "did this work?" — it's "what does the business learn?" Intent should position Observe as a business catalyst, not just loop closure.

13. **OTel isn't just a schema — it's a strategy.** Splunk's data shows organizations treating OpenTelemetry as a strategic investment (not just a data format) get dramatically better outcomes: 72% report positive revenue impact, power users are 2x more likely to impact customer experience. Intent already uses OTel-compatible events, but treats OTel as a convention rather than a strategy. The data says: lean into it harder.

14. **The knowledge layer is table stakes; the operating model is the product.** Hannah Stulberg's Team OS proves that a well-structured shared repo makes a 20-person team self-serving on context. But her system has no loop, no trust model, no signal capture, and no observability. It's Layer 1 (compiled knowledge at team scope) without Layer 2 (operating model) or the observe feedback. Intent's differentiation is not the knowledge base — that's becoming commoditized. It's the loop that rides on top of it.

## Action Items Derived From All Ten

| Action | Source | Priority | Intent Artifact |
|--------|--------|----------|-----------------|
| Add structured error payloads to MCP tools | Rohit P2 | HIGH | SIG-031 |
| Implement checkpointing as code in retrieval pipeline | Rohit P8 | HIGH | SIG-033, INT-013 |
| Evaluate slopfiles plugin for CLAUDE.md optimization | Dex | MEDIUM | Dex Horthy ingestion plan |
| Build morning briefing as scheduled Cowork task | Hermes | MEDIUM | Cowork plugin |
| Add context budget checker to persona loading | Dex | MEDIUM | Cowork plugin |
| Split auto-memory into USER.md + MEMORY.md | Hermes | LOW | Auto-memory refactor |
| Add memory hygiene section to enrichment dashboard | Hermes | LOW | Dashboard update |
| Add field-level data classification to KE schema | Rohit P5/P7 | MEDIUM | SIG-032 |
| Adapt Meridian context template for engagements | AI-Native PM OS | HIGH | knowledge-engine/templates/ |
| Add executive one-pager template to Intent templates | AI-Native PM OS | HIGH | .intent/templates/ |
| Extract JTBD pipeline as KE enrichment agent | AI-Native PM OS | MEDIUM | knowledge-engine/ |
| Cross-ref PRD workflow with spec-shaping protocol | AI-Native PM OS | MEDIUM | spec/ |
| Evaluate anti-style.md as governance pattern | AI-Native PM OS | LOW | methodology/ |
| Install codeburn, validate Cowork session discovery | CodeBurn | HIGH | Observe phase |
| Run `codeburn compare` after mixed-model enrichment | CodeBurn | HIGH | Model mixing decision |
| Build codeburn JSON → observations/metrics/ bridge | CodeBurn | MEDIUM | Observe pipeline |
| Evaluate `codeburn optimize` for Cowork plugin design | CodeBurn | MEDIUM | Cowork plugin |
| Add adversarial verification step to persona synthesis | SIG-036 (Pawel + Dex + landscape) | HIGH | Persona pipeline |
| Enable model-per-persona-role in spec-shaping config | SIG-036 | MEDIUM | spec-shaping-protocol.md |
| Validate depth scores cross-model (Opus vs GLM-5.1) | SIG-036 | MEDIUM | Depth scale v2.0 |
| Adopt "AI-First" prefix in Intent positioning | Enterprise guides | HIGH | Intent site, GTM |
| Cite PagerDuty 100%/48% learning loop gap as Observe validation | Enterprise guides | HIGH | Intent site, spec/ |
| Develop C-suite narrative for Intent | Enterprise guides | HIGH | GTM strategy |
| Frame Intent loop as tool-consolidation strategy | Enterprise guides | MEDIUM | Intent site |
| Collect practitioner case studies with measurable outcomes | Enterprise guides | HIGH | reference/, Intent site |
| Adopt "agentic AI" and "operational resilience" vocabulary | Enterprise guides | MEDIUM | site, spec/ |
| Develop adoption maturity model for Intent | Enterprise guides (Airtable) | HIGH | methodology/, Intent site |
| Use "connected data" as accessible framing for compilation | Enterprise guides (Airtable) | MEDIUM | Intent site, GTM |
| Study Airtable Field Agent pattern for enrichment pipeline design | Enterprise guides (Airtable) | MEDIUM | knowledge-engine/ |
| Frame Intent for non-engineering audiences (ops/product/marketing teams) | Enterprise guides (Airtable) | MEDIUM | Intent site, GTM |
| Cite Splunk 65% revenue / 125% ROI / 54% signal quality data in Intent guide | Splunk Observability | HIGH | Intent guide, site |
| Cite Splunk 18% agentic AI adoption as "Intent is ahead" evidence | Splunk Observability | HIGH | Intent guide, GTM |
| Cite 73% outage-from-suppressed-alerts as "never drop signals" validation | Splunk Observability | HIGH | Trust framework validation |
| Adopt "observability-as-code" vocabulary for Intent's file-native approach | Splunk Observability | MEDIUM | Intent site, spec/ |
| Adopt "business catalyst" framing for Observe phase | Splunk Observability | MEDIUM | Intent site, methodology/ |
| Add business context tags (engagement, client, phase) to event schema | Splunk Observability | MEDIUM | Event schema, spec/ |
| Position Observe as business intelligence, not just loop closure | Splunk Observability | HIGH | Observe phase spec |
| Make event schema Kafka-compatible for future hosted-mode migration | Confluent | HIGH | Event schema, spec/ |
| Define formal event schema with version and validation rules | Confluent | HIGH | spec/, events.jsonl |
| Name Intent's Blackboard pattern — Knowledge Engine IS a blackboard | Confluent | MEDIUM | Knowledge Engine docs |
| Design hosted-mode events as topic-based (one per event type or phase) | Confluent | MEDIUM | Hosted mode spec |
| Use trace_id (Intent ID) as natural partition key in event design | Confluent | MEDIUM | Event schema |
| Model enrichment pipeline as consumer group with load balancing | Confluent | LOW | Enrichment pipeline spec |
| Use agents-as-microservices analogy in Intent positioning | Confluent | MEDIUM | Intent guide, site |
| Validate autonomy levels framing against Splunk's trust thresholds language | Splunk Myths | LOW | Trust framework |
| Update L3 scope from "3-8" to "up to ~20 with shared KB" | Team OS (Stulberg) | HIGH | SPEC-productivity-os-layers |
| Add "launch gate" as named L3 governance pattern | Team OS (Stulberg) | HIGH | SPEC-productivity-os-layers |
| Add progressive context loading as persona/KB design principle | Team OS (Stulberg) | MEDIUM | Cowork plugin, persona loading |
| Add `steward` field to knowledge artifact frontmatter | Team OS (Stulberg) | MEDIUM | knowledge-engine/AGENTS.md |
| Position compilation as "Level 2 of Team OS" in messaging | Team OS (Stulberg) | HIGH | Intent site, course |
| Monitor Stulberg/Vellotti Maven workshop (May 10) | Team OS (Stulberg) | MEDIUM | Competitive intel |
| Add Hannah Stulberg as practitioner-architect persona | Team OS (Stulberg) | LOW | Persona library |

---

*This index should be read at the start of any roadmap planning session. It prevents rediscovery of already-analyzed patterns.*
