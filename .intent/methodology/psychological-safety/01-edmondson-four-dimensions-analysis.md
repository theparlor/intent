# Psychological Safety — Edmondson's Four Dimensions Applied to Intent

> Source: Amy Edmondson, *The Fearless Organization* (2018) and *Right Kind of Wrong* (2023). The four dimensions below are Edmondson's research framework; the Intent-specific analysis is new.

## Why this document exists

The 2026-04-09 multi-panel site review produced one critical finding (F10) that only one panel caught: **psychological safety is the biggest latent failure mode in Intent's methodology**. Amy Edmondson was the dominant voice of the Org Design panel, and she was specific:

> "Intent is built by engineers for engineers and treats safety as emergent. It isn't. Trust scoring is literally a scoring system applied to humans' clarity. If my specs keep scoring L1, am I the bottleneck? Signals capture friction with attribution — in a low-trust org this is a dossier mechanism. Who sees my signals? Can my manager read what I noticed? This is a performance-management shadow system waiting to happen."

That quote names a specific failure mode Intent has not designed against. This document works through Edmondson's four research dimensions and identifies which Intent mechanisms risk violating each one. Every risk becomes a design constraint for the forthcoming Psychological Safety Contract (see `02-safety-contract-v1.md`).

Brien's promotion of Edmondson to foundational tier (2026-04-09) means her voice is now always in every panel-review call. This analysis is the seed for that always-on reference.

## Edmondson's framework

Psychological safety is a *team-level* belief (not individual trait, not organizational policy) that it is safe to take interpersonal risks. Edmondson's research identifies four dimensions on which a team scores its safety level. Each dimension has specific observable behaviors that either build or destroy safety.

The four dimensions:

1. **Attitude toward risk and failure** — is it safe to fail here?
2. **Open conversation** — can I say the hard thing?
3. **Willingness to help** — will colleagues respond or withhold?
4. **Inclusion and diversity** — do I belong enough to speak at all?

For each dimension below: what the research says, what Intent's mechanisms risk, and what must be true for Intent to not destroy safety.

---

## Dimension 1 — Attitude toward risk and failure

### What Edmondson's research says

Teams with high psychological safety exhibit a specific counterintuitive pattern: **they report more errors, not fewer**. The original research was on hospital error rates, and the worst-performing teams initially looked like the best because they were reporting fewer mistakes. When Edmondson dug in, she found the opposite — the high-reporting teams had the LOWEST actual harm rates because they surfaced and corrected problems early.

Key insight: the absence of reported failure in a team is not safety, it is silence. Silence is the leading indicator of systemic failure, not of competence.

Edmondson also distinguishes three failure types: basic (preventable, know the process), complex (novel combinations), intelligent (deliberate experiments at the frontier). Organizations that treat all three the same either punish experimentation or excuse negligence.

### What Intent's mechanisms risk

Intent has two load-bearing surfaces that interact with failure:

**1. Trust scores on signals and specs.**
Trust scores classify a signal or spec on clarity, blast radius, reversibility, testability, and precedent. Each of these is fine as a technical assessment. The risk is when humans associate the score with their own performance. Low clarity on a spec the PM wrote ≠ "the PM is unclear thinking," but in a low-trust org that's exactly what the score will mean.

**2. Contract verification assertions (`contract.assertion.passed` / `.failed`).**
Every contract produces binary pass/fail events. The test itself is fine — that's how TDD works. The risk is the **attribution of failure**. If contract.assertion.failed fires, who is responsible? The spec author? The agent? The reviewer? The trust-level setter who authorized L3 execution? Diffuse accountability is a psych-safety nuclear option because everyone hides, no one learns, silence follows.

### What must be true for Intent not to destroy safety on Dimension 1

**Design constraints:**
- Trust scores MUST be spec-level, not author-level. A spec scored L1 is not a statement about the human who wrote it.
- Trust scores MUST carry provenance. Who scored what, when, with what evidence. No anonymous low scores.
- Failure attribution MUST be explicit. When a contract fails, the event captures: (a) the spec author, (b) the reviewer, (c) the trust-level authorizer, (d) the executing agent. No diffusion.
- Intelligent failures MUST be distinguishable from preventable failures. The event catalog needs a `failure_type` field on contract.assertion.failed: {basic, complex, intelligent}. Intelligent failures on L3/L4 autonomy should be celebrated, not corrected.
- Silence MUST be observable. If a team's signal rate drops below a threshold, that is a safety signal, not a productivity win.

### Open questions

- What threshold of signal silence triggers a safety alert?
- Who reviews low-clarity specs in a way that doesn't shame the author?
- Can trust scores be reviewed/appealed by the author?

---

## Dimension 2 — Open conversation

### What Edmondson's research says

High-safety teams normalize **speaking up** with questions, concerns, mistakes, and ideas. Low-safety teams normalize silence or polite agreement. The difference isn't conflict avoidance vs. conflict addiction — it's whether the hard thing can be said without consequence.

Edmondson specifically warns against confusing psychological safety with "being nice" or "avoiding conflict." Safety *enables* candor. Comfort *disables* it. Her formulation: "Psychological safety is not a license to complain. It's a license to learn."

Signs of low open-conversation safety:
- Meetings where everyone agrees and then the real conversation happens in Slack DMs
- Decisions that "suddenly" get reversed after the decision meeting
- People not asking questions because they "should already know"
- Junior voices silenced by senior presence

### What Intent's mechanisms risk

**1. Signal capture with attribution.**
Intent's signal files include an `author` field. This is good for traceability and terrible for psychological safety if the signal is used as a performance record. "Who noticed X" becomes "Who complained about X" in a low-trust org.

In particular: signals about process friction ("the review gate is too slow") or about colleagues ("agent output for X was misaligned") are interpersonally risky to capture. If authors worry their complaints will be read by the complained-about, they will not capture signals — which is the silence failure mode from Dimension 1.

**2. The trust scoring formula's "clarity" factor.**
Clarity (0.30 weight) is the biggest factor in trust scoring. "Clarity" is subjective. Who judges? If clarity is judged by the reviewer, authors will write defensively to chase high clarity scores. If clarity is judged by the author, scores become meaningless. Either way, the scoring creates an optimization target that may not be the real goal.

**3. Spec-shaping protocol's four-persona interrogation.**
The "Intents become specs through four-persona interrogation" protocol (Architect, Product Leader, Quality Advocate, Agent) is designed for spec quality. It is interpersonally neutral when the personas are AI-rendered. But if humans are ever in these roles — if "the Architect pass" becomes "Dave reviews Alice's spec" — then the protocol becomes a formalized four-vector critique of the author. That can be fine if done well and devastating if done poorly.

### What must be true for Intent not to destroy safety on Dimension 2

**Design constraints:**
- Signal capture MUST support scoped visibility. Authors can mark signals as author-only, team-only, engagement-wide, or public. Default is team-only, not public.
- Signals about interpersonal friction MUST have a sensitive-flag that routes them to a private review path, not the open stream.
- Clarity scoring MUST distinguish "the spec lacks detail" (about the artifact) from "the thinking is muddled" (about the author). The formula scores the former, never the latter.
- Spec-shaping protocol MUST be understood as AI-persona-rendering when automated. Human critique via the protocol requires explicit opt-in and safety norms.
- Appeal surface for trust scores MUST exist. An author can challenge a clarity score and get a human review.
- The disambiguation signal pattern ("when stuck, generate a new signal asking a better question") MUST be psychologically safe. It cannot be read as "you failed to write a clear spec," it must be read as "the problem is still being shaped."

### Open questions

- How does signal visibility scoping work technically?
- Can authors see how their signals are being read downstream?
- Is there a convention for flagging "this is about me, I'm struggling" vs "this is about the system, the system is struggling"?

---

## Dimension 3 — Willingness to help

### What Edmondson's research says

High-safety teams show a specific pattern of **reciprocal helpfulness**. When one member asks for help, others respond without judgment or territorial behavior. The key signal is how a team responds to ignorance or struggle — do they rush to help, or do they withhold, evaluate, or mock?

This dimension is closely linked to the Liz Wiseman research on Multipliers vs. Diminishers. Multipliers create contexts where asking for help is a growth moment; Diminishers create contexts where asking for help is a weakness admission.

### What Intent's mechanisms risk

**1. Autonomy levels (L0-L4) as capability judgments.**
Intent's autonomy levels are technically applied to signals/specs, but humans will read them as capability labels. A team where most signals are L2 vs. a team where most are L4 will feel like a capability judgment even though it's a spec-clarity judgment. This becomes a "we can't handle autonomy" stigma.

**2. Panel-review primitive (INT-007) when applied to human work.**
The panel-review skill is one of the most valuable primitives Intent is shipping. It is also a potential psych-safety nightmare if misapplied. A panel review of a human's spec is a 4-12-voice critique of the work — and by proxy, of the human. Even with genericized panel output, authors will absorb the critique personally.

**3. Challenge the Intent pass (SIG-050 → INT-007 integration).**
The proposed "Challenge the Intent" pass — where a rotating challenger (Rumelt, Christensen, Mintzberg) asks "should we even want this outcome?" — is double-loop learning at its best. It is also an interpersonal risk: someone has to hear "your intent might be wrong at the root." If this pass is AI-rendered, it's fine. If it's humans, it is a high-skill conversation that only high-safety teams can survive.

### What must be true for Intent not to destroy safety on Dimension 3

**Design constraints:**
- Panel-review outputs MUST separate the artifact critique from the author identity. Never: "Alice's spec is weak." Always: "The spec at SPEC-005 is weak in these ways."
- Panel-review MUST offer a "generative alternative" mode, not just critique. The panel can be asked "how would you strengthen this?" not just "what's wrong with this?"
- Autonomy level distributions MUST NOT be used as team health metrics in any public dashboard. They are technical indicators, not capability scores.
- Help-seeking MUST be structurally rewarded. When a signal includes "I'm stuck," the response should be a panel-review call or a disambiguation path, not a trust-score reduction.
- Challenge-the-Intent passes MUST be clearly labeled as premise-level critique, with explicit "this is not a critique of the author" framing.
- The disambiguation signal pattern explicitly normalizes asking for help: "when stuck, generate a new signal" is Intent's institutional permission to ask questions.

### Open questions

- Should panel-review have a mode that only outputs strengths first, and requires explicit request for weaknesses?
- How do we prevent autonomy-level distribution from becoming a manager's dashboard?
- Who is trained on how to read a Challenge-the-Intent response without ego damage?

---

## Dimension 4 — Inclusion and diversity

### What Edmondson's research says

Psychological safety depends on belonging. You cannot speak up in a team where you don't feel you belong in the first place. This dimension addresses who is in the room, whose voice is heard, and whether the team's norms exclude anyone structurally.

Edmondson is explicit: inclusion is not about demographic representation alone (though it starts there). It is about whether the team's working norms let all members contribute. A homogeneous team can have high safety for insiders and zero safety for anyone who doesn't match the pattern. A diverse team can be unsafe if the norms tacitly privilege one subgroup.

### What Intent's mechanisms risk

**1. The 178-persona library skews heavily named-human male Western.**
Brien's persona library, while extensive, is demographically narrow. When the panel-review primitive calls on "the voices" to critique an artifact, most of those voices are the same demographic pattern. An author whose background is not represented in the voices may feel the critique is coming from a consistent "other."

**2. Engineering-native vocabulary as a belonging signal.**
Intent's methodology uses terms like "signal," "trust score," "contract," "autonomy level," "atom," "event stream." This is engineering culture's native vocabulary. It is also a belonging signal: those who know the words belong; those who don't are outsiders. Designers, researchers, customer-facing roles, and newer practitioners will read the vocabulary as "this is not for me."

**3. Git-native workflow assumption.**
Intent assumes git as the substrate. "Open a terminal, git clone, intent-signal capture..." is the onramp. For engineers this is frictionless. For PMs who don't live in git, designers who don't, research leads who don't — it is a wall. The onramp structurally excludes people whose Notice contributions would be most valuable (because they're noticing different things).

**4. The "practitioner-architect" target user framing.**
"Senior IC, system thinker, architect" is the implicit ideal user. This is a valid strategic choice (wedge strategy). It is also an inclusion choice: it centers a specific demographic pattern (typically male, typically engineering-tenured, typically technical-leader) and decenters others. This is fine as a strategy but should be named explicitly.

### What must be true for Intent not to destroy safety on Dimension 4

**Design constraints:**
- The persona library MUST expand to include more voices from historically underrepresented backgrounds in tech and product. This is not political correctness — it is signal quality. A library biased toward one demographic produces critiques biased toward that demographic's assumptions.
- Intent MUST offer non-git onramps for Notice capture. PMs, designers, and research leads should be able to contribute signals without touching a terminal.
- The vocabulary MUST have a plain-language translation layer. Every Intent term should have a "this is like the [familiar concept] in [adjacent practice]" gloss.
- The target user framing MUST be named explicitly, not assumed. "Intent is designed for practitioner-architects first. If that's not you, here's what we're doing to broaden the entry points."
- Belonging signals MUST be actively maintained. Whose voices get celebrated in public artifacts? Who's in the walkthrough examples? Whose names appear in the ADRs?

### Open questions

- Who is currently missing from the 178-persona library that we could add?
- What does a non-git Notice onramp look like? (Slack bot? Web form? Voice memo transcription?)
- How do we check for vocabulary exclusion before it becomes structural?

---

## Summary: Intent's psych safety risk profile

| Dimension | Risk level | Primary mechanism | Design constraint count |
|-----------|------------|-------------------|------------------------|
| 1. Risk and failure | HIGH | Trust scoring, contract failure attribution | 5 |
| 2. Open conversation | HIGH | Signal authorship, clarity scoring, four-persona protocol | 6 |
| 3. Willingness to help | MEDIUM-HIGH | Autonomy levels, panel-review, Challenge-the-Intent | 6 |
| 4. Inclusion and diversity | MEDIUM | Persona library, vocabulary, git-native, target framing | 5 |

**Overall assessment:** Intent is currently a system whose mechanisms could either support or destroy psychological safety depending entirely on how they are implemented. The difference is not cosmetic — it is structural. A team with Intent and high safety will use the tools as learning instruments. A team with Intent and low safety will use the same tools as surveillance and performance-evaluation instruments.

**The panels were right:** this is the biggest latent failure mode. It is not addressed by any current Intent mechanism. It requires a first-class design intervention: the Psychological Safety Contract.

## What happens next

1. **Psychological Safety Contract v1** (`02-safety-contract-v1.md`) — the document that codifies the design constraints above into an enforceable promise.
2. **Change management analysis** (`03-change-management-analysis.md`) — Bridges + Kotter applied to Intent adoption, with the power-shift table from the Org Design panel.
3. **INT-013** — an intent that treats safety + change as a named workstream, not an afterthought.
4. **Update INT-007** (panel-review primitive) — Edmondson is now foundational; her voice is always in the rotation.

## Lineage

- **The Fearless Organization** — Amy Edmondson (2018)
- **Right Kind of Wrong** — Amy Edmondson (2023)
- **Teaming** — Amy Edmondson (2012)
- **Multipliers** — Liz Wiseman (referenced for Dimension 3)
- **Theory X and Theory Y** — Douglas McGregor (referenced for Dimension 1)
- **Chris Argyris** — theory-in-use vs. espoused theory (referenced for Dimension 2 on candor)
- **Edgar Schein** — humble inquiry (referenced for Dimension 2 on question-asking)
