---
type: primary-source
depth_score: 4
depth_signals:
  file_size_kb: 7.1
  content_chars: 7002
  entity_count: 0
  slide_count: 0
  sheet_count: 0
  topic_count: 0
  has_summary: 0
vocab_density: 0.14
source: "https://karpathy.bearblog.dev/power-to-the-people/"
captured: 2026-04-12
origin: agent
confidence: 0.90
related_signals:
  - SIG-025
  - SIG-032
extraction_depth: high
author: Andrej Karpathy
published: 2025-04-07
---
# Karpathy — "Power to the People" — Full Extraction

Published: April 7, 2025. Roughly one year before his LLM Knowledge Bases tweet (April 3, 2026).

## 1. The Inversion Thesis

Central claim: LLMs represent the first major technology in history that benefited individuals before institutions — a complete inversion of the historical diffusion pattern.

Historical pattern: government/military → corporations → individuals. Nuclear power, the internet, GPS, transistors — all top-down cascade.

LLMs inverted it. ChatGPT reached 400 million weekly active users faster than any consumer product in history.

> "LLMs display a dramatic reversal of this pattern — they generate disproportionate benefit for regular people, while their impact is a lot more muted and lagging in corporations and governments."

## 2. The Power Shift: What Capabilities Move

The LLM capability profile: "quasi-expert knowledge/performance, but simultaneously across a very wide variety of domains."

**For individuals:** "Individuals will usually only be an expert in at most one thing, so the broad quasi-expertise offered by the LLM fundamentally allows them to do things they couldn't do before." Solo dev does legal review. Writer does competitive analysis. Consultant runs research across five domains simultaneously.

**For organizations:** Already concentrate diverse expertise. "While LLMs make these experts more efficient, the improvement takes the form of becoming better at things they could already do." Delta is smaller. Lift is incremental.

**What moved: cross-domain breadth.** What was an org-level resource (legal team, strategy team, research department) is now accessible to individuals directly.

## 3. Examples

- "Vibe coding" — building apps through natural language without deep expertise
- Writing a Rust tokenizer without Rust expertise
- Ephemeral single-use apps because code is "free, ephemeral, malleable, discardable"
- "Bill Gates talks to GPT-4o just like anyone else does" — leveling of access
- Non-experts entering programming because barrier collapsed

Implied spectrum: any individual who previously needed institutional access to a domain can now operate independently.

## 4. Connection to LLM Knowledge Base Work (April 2026)

The essay established the *why* (individuals have quasi-expert breadth). The Knowledge Base work is his *how* (operationalizing that power).

From April 2026 thread:
- "A large fraction of my recent token throughput is going less into manipulating code, and more into manipulating knowledge."
- Three layers: raw (immutable, human-curated) → LLM-compiled wiki → schema/configuration
- ~100 articles, ~400K words, self-maintaining
- "You never write the wiki yourself — the LLM writes and maintains all of it. You're in charge of sourcing, exploration, and asking the right questions."
- "The wiki is a persistent, compounding artifact."

**Direct link:** Essay argued individuals now have breadth. Knowledge Base demonstrates what one person does with it: compiles a personal operating intelligence.

## 5. Future: Individual vs. Institutional

**Critical threat to democratization: performance tiers.**

> "Frontier-grade LLM performance is currently very accessible and cheap — money can't buy better ChatGPT."

But: "The moment money can buy dramatically better ChatGPT changes things, as large organizations get to concentrate resources to buy more intelligence."

Two vectors where distribution could collapse:
1. **Training-time scaling** — more compute = better models, only well-resourced orgs can fund
2. **Test-time scaling** — longer inference costs more per query, creating pay-to-win tiers

Conclusion hedged but optimistic: "the future is already here, and it is shockingly distributed." But not claimed as permanent.

**Individuals have a window.** Open now because frontier capability is commodity-priced. Question is how long it stays open.

## 6. Team-Scale vs. Individual-Scale: The Gap

Karpathy's entire framework is individual-scale. Notable gap — and where Intent has real leverage.

**Structural problems at team scale in his framework:**
- **Contamination risk:** Agent-generated mixed with human notes. His recommendation ("separate vaults") is a workaround, not a solution.
- **No shared operating model:** His KB compiles what one person knows. Teams need to compile how a group works — decisions, handoffs, coordination norms, shared context.
- **No multi-curator workflow:** One human as "curator/questioner." Multi-human creates version conflicts, competing schemas, trust questions.
- **No signal about team leverage:** Doesn't model what happens when unit shifts from one person to a team with LLM breadth. Assumes team = organization = slower.

**The gap:** Karpathy proves what one person can do with a compiled knowledge base. Does NOT show what a team can do with a compiled operating model. Knowledge base vs. operating model, individual vs. team — exactly the seam Intent occupies.

## 7. Democratization Thesis: Four Components and Limits

1. **Access parity at frontier.** Everyone pays same for GPT-4o. *Limit:* contingent on pricing decisions. Can change.
2. **Capability profile matches individual needs.** Quasi-expert breadth more valuable to non-specialists. *Limit:* specialists gain less — already have depth.
3. **Low barrier to entry.** Natural language, free tier, any device. *Limit:* Interface is low-barrier; *use* is not. Karpathy's own KB requires significant meta-cognitive skill.
4. **Organizational inertia creates a window.** Individuals move fast while orgs fumble. *Limit:* Window closes as orgs solve integration.

**Deepest limit Karpathy doesn't fully name:** Individual democratization doesn't solve collective coordination. Even if every person on a team has a compiled KB, the team still has alignment and coordination problems. Individual LLM leverage × team ≠ team-level LLM leverage.

## Relevance to Intent THM-003 Positioning

THM-003's framing is well-supported and defensible.

**What Karpathy gives:**
- Source credibility (most respected voice on LLM practicalities)
- Setup (individuals gained institutional capabilities)
- Proof of concept (one person + compiled KB = multiplicative output)
- Implicit gap (never extended to team-scale coordination)

**What Intent adds beyond Karpathy:**
- **Team coordination layer:** Knowledge bases are personal; operating models are collective
- **Durability:** Compiled operating model persists across team changes; individual KBs die when person leaves
- **Organizational thesis:** The gap isn't individuals vs. corporations — it's adaptive teams vs. bureaucratic institutions. Intent makes a team operate at the speed Karpathy's individuals operate.

**Precise framing opportunity:**
> Karpathy's Knowledge Base solves "what does one person know."
> Intent solves "how does a group decide and move."
> Different problems at different levels of abstraction. No one has built the second with the rigor Karpathy applied to the first.
