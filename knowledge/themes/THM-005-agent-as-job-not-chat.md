---
id: THM-005
type: theme
created: 2026-05-16
updated: 2026-05-16
depth_score: 3
depth_signals:
  file_size_kb: 6.5
  content_chars: 6200
  entity_count: 0
  slide_count: 0
  sheet_count: 0
  topic_count: 0
  has_summary: 0
vocab_density: 0.52
name: Agent-as-Job, Not Agent-as-Chat
confidence: 0.7
origin: agent
sources:
  - raw/research/2026-05-16-rahul-ai-agent-team-playbook.md
related_personas:
  - PER-002
related_decisions:
  - DDR-002
  - DDR-003
  - DDR-006
  - DDR-008
signals:
  - SIG-036
  - SIG-037
  - SIG-038
---
# Theme: Agent-as-Job, Not Agent-as-Chat

## Parallax framing

This theme is a **parallax read**: the same architecture Intent derived from high-rigor sources (Karpathy, Boyd/Richards, Rotifer, HumanLayer 12-factor) seen from a low-rigor, market-facing vantage point (a popular solo-founder playbook). Parallax = depth from a second angle. The playbook has no empirical method and ends by selling managed agent hosting, so it carries **no independent evidential weight**. Its value is two-fold: (1) it independently re-derives several of Intent's core theses from outside the research lineage — that is *positioning* evidence (the market is now articulating the problem Intent solves), and (2) it contributes a small number of concrete structuring techniques worth absorbing.

## Insight

The playbook's organizing claim — *"a real agent is a job description + a trigger + an output, not a chat session... that is expensive autocomplete"* — is the same claim Intent encodes as the work ontology and the enrichment pipeline. Intent already has the rigorous version (Signal → Intent → Spec → Contract; trust-gated autonomy L0–L4; six enrichment agents each with a defined input/output). The playbook adds nothing to the theory but **sharpens three operational pressures Intent has under-specified**: real-time observability of running agents, always-on hosting, and human-review-capacity as a finite resource that caps autonomy rollout.

## Patterns extracted (mapped to Intent)

| Playbook pattern | Maps to | Status in Intent |
|---|---|---|
| Agent = job description + trigger + output (not chat) | Work ontology; 6-subagent architecture; spec-as-contract (Key Decision 6) | **Validated.** No change. |
| "Job description not a vibe" | Specs as verifiable contracts, not prose stories | **Validated.** Reinforces DDR / contracts. |
| Three-prompt-layer per agent: **system** (role) / **workflow** (what it does each cycle) / **output** (format + length caps) | Per-agent prompt contract for the 6 enrichment agents and the 4 spec-shaping personas | **Technique to absorb.** Intent has the four-persona shaping but no explicit system/workflow/output decomposition per agent. Cleaner contract than current AGENT_DEFINITIONS prose. |
| Quality-gate loop: score output (voice/hook/value/originality), auto-rewrite below threshold, loop until standard met | Multiplicative fitness function (accuracy × utility × consistency × recency, Rotifer/THM-001); LLM-as-judge (DDR-006); trust scoring (DDR-008) | **Validated + sharpened.** Confirms enrichment must *loop on a threshold*, not single-pass. |
| Shared knowledge base = the thing that makes independent agents a *team* | Three-layer architecture: compiled knowledge base as shared substrate; query-as-contribution (DDR-007); team-scale thesis (THM-003) | **Validated.** Independent re-derivation of THM-003's "individual leverage × team ≠ team leverage." |
| Topology: slash command vs. hook vs. hosted 24/7 script; 5 local / 8 must-be-always-on | 5-tier signal-capture adapters; deployment topology (local vs. hosted mode) | **Technique to absorb.** The local-vs-always-on split is a concrete heuristic for partitioning Intent's pipeline stages. |
| "You need to see what they are doing in real time / output becomes garbage around day 9, nobody notices" | Observe product; events.jsonl; overwatch + incestuous-amplification detection (RAT-003); staleness/decay (DDR-008) | **Gap pressure → SIG-036.** Observe is schema-ready but unvisualized; silent-degradation detection is unowned. |
| "Hosting on your laptop is not a strategy" / cron dies at 4am / nobody notices until Monday | Hosted deployment mode — always-on processing (open item in CLAUDE.md) | **Gap pressure → SIG-037.** Intent explicitly names Brien's laptop going offline during travel; this is the same failure, externally corroborated. |
| 90-day staged rollout: "ship everything in a weekend → drown in review tasks → lose the efficiency" | THM-002 (bottleneck-shift) at the approval gate; L0 gate; ceremony-tax framing | **Founding thesis rediscovered → SIG-038 → INT-014.** *Not* a new consideration: the bottleneck relocated to the human gate, it did not vanish. Jira/peer-review are its legacy instrumentation. Narrow architectural gap: trust rations per-signal, nothing rations aggregate human attention. |

## Evidence

- [Rahul playbook](../raw/research/2026-05-16-rahul-ai-agent-team-playbook.md) — "A real agent is a job description + a trigger + an output." / "This shared memory is what transforms three independent agents into a coordinated team." / "Most agents fail silently... the output becomes garbage around day 9, and nobody notices until a customer DMs you a screenshot." / "Hosting them on your laptop is not a strategy. 90% of builders die here." / "Don't try to ship everything in a weekend. You will overwhelm yourself with review tasks and lose all the efficiency you were trying to gain."

## Implications

1. **Positioning.** A non-research practitioner audience now frames the problem ("agents that survive contact with Monday morning") in terms structurally identical to Intent's. Intent's differentiator is precisely the rigor the playbook lacks: trust scoring, contracts, overwatch, double-loop. The market is articulating the wound; Intent has the surgical version. Useful for site/positioning copy — but cite as *market signal*, not evidence.
2. **Absorb two techniques.** (a) Decompose each enrichment/shaping agent definition into explicit **system / workflow / output** prompt layers with hard output caps. (b) Use the **local-vs-always-on partition** as the organizing axis for the hosted-mode deployment spec.
3. **Three gap signals raised** (below) — observability (SIG-036) and always-on hosting (SIG-037) are gap pressure; review-capacity (SIG-038) is **not** a gap discovery but the founding thesis (THM-002) rediscovered at the approval gate, promoted to **INT-014**. The correction matters: framing it as "new" would have hidden that Intent risks rebuilding the Jira/peer-review ceremony tax inside its own autonomy pipeline.

## Open Questions

- Does the three-prompt-layer decomposition belong in AGENT_DEFINITIONS.md, in per-skill SKILL.md files, or in a shared agent-contract template? (Touches the spec-shaping protocol — do not refactor without a DDR.)
- The playbook's economic claim (13 agents ≈ $1,300/mo) is unverified vendor-adjacent math. Do not propagate into any Intent costing artifact without independent sourcing.
- What is the actual human-review throughput ceiling for a solo practitioner (Brien), and how should it parameterize the concurrent-review budget? (SIG-038 → INT-014.)
</content>
