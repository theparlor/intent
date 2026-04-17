---
id: SIG-032
timestamp: 2026-04-13T06:30:00Z
source: conversation
confidence: 0.95
trust: 0.7
autonomy_level: L3
status: captured
cluster: practitioner-validation
author: brien
related_intents: []
referenced_by: []
parent_signal: null
---

# Peer practitioner Chris Markus: 3-month conversation corpus as Intent signal source

## Summary

Chris Markus — senior architect (~25 YOE), managing outsourced 30-engineer team on multi-tenant SaaS platform — has been Brien's primary peer sounding board for Intent from Jan 21 through Apr 13, 2026. Over 500 iMessages and 40+ shared links, Chris has provided the highest-density external signal source for Intent's problem space: how senior practitioners relate to AI-augmented engineering, what confuses them about Intent specifically, and what the market actually needs.

## Signal Value

Chris represents a critical persona for Intent adoption: **the experienced IC/architect who is already using AI agents productively but lacks a governing framework**. He built a hardened K3s VM appliance in 16 hours with AI, runs agents against his outsourced team's output, and reads voraciously across the AI engineering space. He is not a skeptic — he is a practitioner who wants Intent to work but holds it to engineering standards.

His signal value is threefold:
1. **Practitioner feedback on Intent itself** — what he understands, what confuses him, what he wants collapsed
2. **Information diet as market barometer** — the articles he curates reveal what senior practitioners are reading/thinking about AI
3. **The "two-pager" request as product signal** — the market wants translation documents that bridge vision to practice

## Chris's Direct Feedback on Intent

### What He Grasps
- The signal-to-spec pipeline
- The documentation site structure
- Agent delegation and parallel execution value
- World-model expression for AI consumption: "It's all about laying out the world model of the business problem so the AI can understand efficiently" (2026-03-30)

### What Confuses Him
- **Trust mechanism:** "You are going to need to explain the trust thing to me at some point" (2026-04-11)
- **Agile lens trap:** "Imho what I am struggling with is the agile lens you have on it. I get it is a rune stone to light bend the slow to the modern but I think the larger agile solution need is one step higher." (2026-04-11)
- **Scale coordination:** "In a company what happens if there are 100 Brien's using your framework? Will we not worry about coordination costs anymore? Just 100 chaos agents sorting themselves out naturally?" (2026-04-11)

### His Challenges to Brien
1. **"Collapse it harder":** "You are very very close. But I don't think you are collapsing this hard enough. You need to implode it." (2026-04-11)
2. **The two-pager:** "I would love for you to produce a two pager on what agile dev looks like in the new future like this. Very glossy and hopium titles on the right, but if those roles will exist there will be a lot of messy details to do those jobs without either getting in the way or getting run over." (2026-04-12)
3. **Copyright gap:** "before you are done with your coffee in the morning you need to add a copyright and license to your GitHub/site" (2026-04-11)
4. **Continuous planning at scale:** "In an Agile-AI (or AI-Agile hmmm) world. What does continuous planning look like? Never understood the mechanics of CP but appreciate someone was doing it. But, when you have 100 Intent powered Brien's spawning 100 each, 1000 knock offs and shallow clones and 10 cowboy LLMs fighting in a co. What does that look like?" (2026-04-12)
5. **Vocabulary precision:** "Your depth and breadth of vocabulary could be a plus and a negative. You have a large toolbox to throw at the LLM, but that precision can both over steer and confuse." (2026-03-08)

### His Workflow (reveals the gap Intent closes)
Chris uses Perplexity for planning → manually transfers to a coding agent. That manual handoff is the exact seam Intent is designed to close. He said: "Seems kinda like my manual workflow where I have Perplexity do my planning and manually transfer to my coding agent" (2026-04-11).

## Information Diet — All Links Shared (Mar 28 – Apr 13)

### Links Chris Shared

**AI/Engineering Industry:**
- 2026-04-03: swyx/pmarca — "He is insufferable, but sums up a lot of stuff nicely"
- 2026-04-08: Kent Beck "Starving Genies" (Tidy First)
- 2026-04-11: "The Loop is the Lab" — "cherry pick some ideas from here and throw them at your project"
- 2026-04-12: Chris Dunlop "This Is What $1,400 of AI Looks Like" — "I listened to this article like 5x in a row. If you weren't in our position you probably would think he is talking future sci-fi."
- 2026-04-12: fafi25 "The System Works. That's the Problem." — "Author recommended by Michael Burry."
- 2026-04-12: The Algorithmic Bridge "AI Will Be Met With Violence" — "not promoting violence, but some people best start listening to the under currents"
- 2026-04-12: MS "The Agentic SOC" — sent with the two-pager request as example of "glossy and hopium titles"

**AI Tools & Agent Infrastructure:**
- 2026-04-02: Baseten inference engineering book — "Going to be diving into this book this weekend"
- 2026-04-05: Claude Certified Architect — "You going to get this cert?"
- 2026-04-11: oh-my-openagent hash-anchored edits — alternative to worktrees for agent collision
- 2026-04-11: Windsurf worktree docs
- 2026-04-11: rentahuman.ai — "Oh on the subject of human harnesses (meat sacks)"
- 2026-04-11: Brien's Intent repo — "I am going to play around with this this weekend" + "You need to implode it"

**AI Labor/Social Impact:**
- 2026-04-12: Google share link — "Elisha's boss's friend can fuck off in a corner also"

**Earlier (Jan–Mar) — from extended history:**
- 2026-01-29: "How AI is Learning to Think in Secret" (Substack)
- 2026-01-31: mob.sh — mob programming tool
- 2026-01-31: Nir Diamant note — "start grooming your agents to enter the octagon"
- 2026-02-01: Libby book rec — "should terrify"
- 2026-02-01: OpenClaw/ClawdBot warnings — "Stay away for now"
- 2026-02-01: Gary Marcus on Moltbot
- 2026-02-01: Algorithmic Bridge on Moltbook — "Ask yourself do I know anything real anymore"
- 2026-02-04: Pragmatic Engineer "Third Golden Age of Software" — "anecdotal evidence that AI amplifies good engineers"
- 2026-02-05: vibekanban.com
- 2026-02-07: Steve Yegge "The Anthropic Hive Mind" — "Dropping this here without comment"
- 2026-02-10: Thomas Dohmke (GitHub CEO) interview — "will know software development has fundamentally changed if git gets replaced"
- 2026-02-26: Rolls-Royce earnings — "We are so fucked"
- 2026-02-28: Gary Marcus "Code Red for Humanity" — "AI agents recommend first strike nuclear strike 95% of the time"
- 2026-03-02: Latent Space "Reviews Dead" — "Excellent article"
- 2026-03-06: Anthropic launches index tracking (Perplexity) — "stop already! FFS"
- 2026-03-08: Claude Code tools internals (sderosiaux)
- 2026-03-08: "Algorithm names are the new cognitive" — precision/vocabulary challenge
- 2026-03-08: Chris Dunlop "The YouTube Moment for Software"
- 2026-03-28: YouTube video — "For your commercialized dooming"
- 2026-04-08: Ed Zitron (YouTube Music) — "Don't let Elisha listen"

### Links Brien Shared
- 2026-01-31: Uncle Bob on AI — "death of programming"
- 2026-02-05: vibekanban.com
- 2026-02-10: Pawel Huryn piece
- 2026-02-20: Spotify podcast — "recommends not limiting tokens"
- 2026-03-28: Intent site (theparlor.github.io/intent/)
- 2026-03-30: Intent pitch page
- 2026-04-11: Intent v2 draft pitch
- 2026-04-12: Graphify (GitHub) — "based off of Karpathy's knowledge graph"
- 2026-04-12: Slate Magazine article — "will foreshadow the death arc"

## Recurring Themes (3 months)

1. **AI amplifies good engineers, exposes bad ones** — Chris's foundational belief, stated repeatedly
2. **Token economics will break the $20/mo model** — pricing anxiety as a leading indicator
3. **Agent-to-agent manipulation is a real threat** — early alarm on OpenClaw/Moltbot
4. **The engineering profession is bifurcating** — "agent wranglers" vs. "coat check clerks"
5. **Human-in-the-loop is the bottleneck, not capability** — independently arrived at Intent's trust problem
6. **Corporate middle class will face pitchforks** — growing anger layer beneath technical conversation
7. **Agile vocabulary is both entry point and trap** — Intent needs to transcend, not just translate

## The Two-Pager Brief

Chris sent an image (IMG_0677.png) from the MS Agentic SOC blog showing aspirational role titles for AI-augmented operations, then requested:

> "I would love for you to produce a two pager on what agile dev looks like in the new future like this. Very glossy and hopium titles on the right, but if those roles will exist there will be a lot of messy details to do those jobs without either getting in the way or getting run over."

**What he wants:** A concrete, shareable artifact that bridges the gap between corporate vision decks (glossy role titles) and operational reality (what those roles actually do). The specific tension: roles that exist "without getting in the way or getting run over" by agents.

**Why it matters as a signal:** The market needs translation documents. Chris doesn't want theory — he wants something he can hand to his boss's replacement or his outsourced team's leadership. This is Intent's first externally-requested deliverable.

Brien accepted: "Good challenge accepted" (2026-04-12)

## Proposed Actions

1. **Write the two-pager** — Intent's first externally-prompted thought leadership artifact
2. **Build Chris Markus persona** — first instance of new "peer" persona type in the registry
3. **Address the "collapse" feedback** — Intent's surface area is too large for practitioner adoption; needs a dramatically simpler entry point
4. **Explain trust mechanics** — Chris flagged this as opaque; needs a one-page explainer
5. **Add copyright/license to Intent repo** — governance gap Chris identified
