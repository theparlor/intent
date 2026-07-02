---
id: SIG-2026-07-02-MOBAI
timestamp: 2026-07-02T00:00:00Z
source: external-persona-research
confidence: 0.9
trust: 0.55
autonomy_level: L2
status: active
cluster: coherence-engineering-positioning
author: agent
related_intents: []
referenced_by: []
parent_signal: null
persona_source: michael-gothe
source_artifact: raw/competitors/2026-06-18-mobai-team-pilot-gothe.md
related_specs:
  - spec/SPEC-INTENT-COHERENCE-GATE-001.md
  - spec/SPEC-INTENT-FORMATION-FLIGHT-001.md
  - spec/SPEC-INTENT-MISSION-BRIEF-001.md
  - spec/team-os-alignment-annex.md
---

# MobAI (Göthe/Justice) Validates the Coherence Problem at the Human-Team Layer — and Hands Us a Facilitation Loop

## Signal

Michael Göthe (Crisp), building on Joe Justice's "MobAI" (coined at Tesla, built on Woody Zuill's mob programming), publishes the exact problem statement Intent's **coherence** work exists to solve — stated for **human teams** instead of **parallel AI agents**:

> "AI can make a group faster without making it a team. That is the dangerous trade."

This is a practitioner with no knowledge of Intent independently naming Intent's founding wager. It is convergent validation of the same shape as SIG-033 (Cagan) and the Team OS annex (Stulberg) — but it lands on the axis Intent has invested most heavily in over the last two months (formation flight, the coherence gate). That makes it the strongest external corroboration to date, and it also hands us a ready-made **facilitation format** for Brien's consulting practice.

---

## 1. Convergent problem statement (validation of the coherence thesis)

Göthe's fragmentation thesis is a line-for-line restatement of `SPEC-INTENT-FORMATION-FLIGHT-001` §1, with humans in the role our spec assigns to isolated agents:

| MobAI (human teams) | Intent / coherence (parallel agents) |
|---|---|
| "One person gets a copilot… easier to feel self-sufficient… reduce the felt need to involve others." | Worktree isolation "severs the coherence channel; each fan-out agent is, by design, ignorant of the system's intent, vocabulary, and 'don't do X' constraints." (FORMATION-FLIGHT §1) |
| "More output without becoming more capable together." / "faster apart." | "Naive parallelism is just faster incoherence." (FORMATION-FLIGHT §1) |
| "Individuals moving faster apart" — locally polished answers that diverge on assumptions, MVP meaning, scope. | **Formation breakup**: "Each agent reports 'airworthy'; the formation has already broken up." (FORMATION-FLIGHT §3) |
| "The bottleneck… becomes shared knowledge, judgment, coordination, and choice." | Intent's whole premise: when AI collapses implementation, the bottleneck moves upstream to discovery/spec/observation (CLAUDE.md). |

**The reframe both make is identical:** the value proposition of AI (individual speed / agent isolation) is the *exact opposite* of what actually needs protecting (team coherence / coherence-to-intent across boundaries). Two independent parties, same coat with two problems in it.

**How this sharpens our language.** Göthe gives us plain-English, leader-facing vocabulary for a thesis we currently state in aviation metaphor. Specifically, three phrases worth borrowing into positioning:
- **"Copilot → Team Pilot"** — the individual-productivity story is "too small." This is a cleaner one-line framing of Intent's "differentiation = spine + altitude, not engine" (DEC-013) than we currently have for a non-technical audience.
- **"AI can make a group faster without making it a team"** — the human-legible version of "false-green": local airworthiness, formation broken.
- **"The first useful backlog may not be a list of features. It may be a list of risks and assumptions to validate."** — this is Notice-phase framing (signals over stories) said in Cagan/Torres-native language.

## 2. Where Intent extends past MobAI (the positioning delta)

MobAI is a **human practice with no enforcement mechanism**. Göthe is explicit: "It is not enough to put people in a room with AI and hope collaboration happens" — and then his answer is *deliberate conditions* (time, shared workflow, right perspectives, reflection). That is a facilitation discipline, not a typed gate. The coherence problem is diagnosed but its detection stays manual and relies on a skilled facilitator noticing drift in the room.

That is precisely the gap Intent's machinery fills, mirroring the SIG-033 "context engineering ≠ context governance" move:

- **MobAI names the failure mode; the Coherence Gate detects it.** "Different meanings of MVP, proof of concept, and experiment" is exactly `SPEC-INTENT-COHERENCE-GATE-001` Stage A **vocabulary drift** (canonical-terms / forbidden-synonyms check). MobAI catches this only if the facilitator happens to hear it in a reflection round; Intent catches it structurally at synthesis time.
- **MobAI's "opening context" is the Mission Brief.** Göthe's most concrete result — transcribing "purpose, constraints, technical setup, challenge framing" and feeding it to the client's Copilot to seed sub-teams and prompts — *is* `SPEC-INTENT-MISSION-BRIEF-001`: the typed reference frame (glossary, invariants, non_goals, canonical terms) that travels with the work into isolation. MobAI does it as an ad-hoc transcript; Intent does it as a schema-pinned payload.
- **MobAI's reflection loop is the drift-clean loop, minus the stop predicate.** Göthe's pause-and-ask cadence keeps improving context "as the work unfolds," but has no convergence detector — no defined "done." Intent's drift-clean fixpoint ("K consecutive drift-clean passes ⇒ converged") is the missing terminal state.

**Positioning line (for the Cagan/coherence-engineering deck):** *MobAI proves the coherence problem is real at human scale and that skilled facilitation mitigates it. Coherence engineering is what makes that mitigation a repeatable, observable, tool-enforced discipline instead of a talent-dependent one — the same "static context → governed context" upgrade, applied to teamwork instead of prompts.*

**Disconfirmation watch (the gift, per external-signals README §2):** Göthe's implicit claim is that the human reflection loop is *sufficient* if you create the conditions — no gate required. If that holds in his hackathons, it is a partial challenge to the premise that coherence needs to be *enforced* rather than *facilitated*. Intent's counter is scale and persistence: a room of 6 for a day can hold coherence in shared attention; a farm of N agents (or a distributed org over months) cannot. The gate earns its keep exactly where the room does not scale. Worth stating explicitly rather than assuming our side.

## 3. Teaching & learning techniques for Brien's own practice

This is the most directly actionable axis. Brien coaches/facilitates at the leadership and engagement tier (Subaru, ASA, F&G) — the tier Cagan (SIG-033) reserves for humans. MobAI is a **facilitation format Brien could run**, and its techniques map onto Intent artifacts so the sessions *dogfood the loop* rather than sitting beside it:

| MobAI technique | Adopt as | Intent artifact it produces |
|---|---|---|
| **Record opening context** (purpose, constraints, language, open questions) and feed it to the team's own AI | Run every engagement kickoff as a **Mission Brief authoring session** — the transcript IS the `reference_frame` | `SPEC-INTENT-MISSION-BRIEF-001` payload; canonical glossary for the engagement |
| **Short rotations + shared screen, AI in the flow** (not one prompter, not N private tools) | The engagement working session as a **formation** — team owns one output, AI visible in the room | Formation-flight session with a human Tower (Brien holds coherence, not the task) |
| **Pause-and-reflect loop** (right direction? / learned? / needs judgment? / missing? / what context feeds back?) | A **structured retro cadence** mid-session, not just at the end — Göthe's finding is that mid-work reflection produced the best context | Observe-phase reads; each reflection = a signal candidate |
| **Record the retrospective** (challenge, method, gaps, risks, next experiment) | Close every session by capturing learnings **as signals**, not slides | External/internal signals → next-loop Notice |
| **"First backlog = risks and assumptions, not features"** | Open engagements with an **assumption/risk map**, not a feature list | Notice-phase signal cluster; feeds Spec, not backlog |
| **Reflection reveals team questions, not AI questions** (scope, "good enough," who has missing context) | Treat AI output as an **X-ray of unclarified intent** — the divergences are the coaching material | Disambiguation signals ("the system never dead-ends") |

The deep alignment: MobAI's "make the human loop *better*, don't remove the human" is Intent's human-contact philosophy verbatim — phase gates, action gates, and voluntary `request_human_input` all exist to keep judgment in the loop, not to automate it away. Brien can present Intent to clients as **"MobAI with a memory and a gate"**: the same shared-work ethos, plus (a) context that persists and compounds across sessions instead of living in a one-day transcript, and (b) a coherence check so drift is caught by the tool, not only by whoever is facilitating that day.

## Hypotheses

- **H1:** The coherence/fragmentation problem is scale-invariant — the same failure mode ("faster apart") appears whether the parallel units are humans-with-copilots or isolated agents. Intent's coherence gate is the machine-layer instance of a general law MobAI states at the human layer. If true, "coherence engineering" generalizes beyond agents to team design, which widens Intent's addressable framing.
- **H2:** Brien's engagements will produce richer, more persistent context if run as MobAI-style formation sessions whose outputs are typed Intent artifacts (Mission Brief in, signals out) rather than ad-hoc transcripts. The gate/Brief upgrade over MobAI is demonstrable in a single side-by-side session.
- **H3:** "Copilot → Team Pilot" and "faster apart" are stronger leader-facing framings than Intent's current aviation metaphors for non-technical stakeholders, and should be adopted in the coherence-engineering positioning without displacing the internal flight-model vocabulary.

## Actions

- [ ] Fold "Copilot → Team Pilot" and "AI makes a group faster without making it a team" into the coherence-engineering positioning language (leader-facing register; keep flight-model vocabulary internal).
- [ ] Draft a **MobAI-style engagement session format** as a playbook (`playbooks/`) that maps rotations→formation, opening-context→Mission Brief, reflection→signals, retro→Observe. Position it as "MobAI + memory + gate."
- [ ] Add the human↔agent isomorphism (this signal's §1 table) as convergent-validation evidence in `SPEC-INTENT-FORMATION-FLIGHT-001` §8 provenance (Göthe/Justice as human-layer prior art for the *problem*, distinct from the borrowed *mechanics*).
- [ ] Cluster with SIG-033 (Cagan) and the Team OS annex under `coherence-engineering-positioning` — three independent external articulations of the same thesis now on file.
- [ ] Decision-surface for a future panel: is coherence *facilitated* (MobAI's bet) or *enforced* (Intent's bet)? Prepare the "the room doesn't scale" reframe (see §2 disconfirmation watch).

## Trust Factors

- **Clarity:** High — the problem statement maps cleanly; the extension delta is well-defined.
- **Blast radius:** Low — positioning + a new playbook; no code, no schema change.
- **Reversibility:** High — language and playbook, fully reversible.
- **Testability:** Medium — H2 (side-by-side session) and H3 (framing resonance) are testable in real engagements; H1 is conceptual.
- **Precedent:** Strong — SIG-033 established the external-convergence capture pattern this follows.
</content>
