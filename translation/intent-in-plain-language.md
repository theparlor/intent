---
title: Intent, in plain language
type: exposed-surface
audience: executives, engineers (no prior Intent context)
created: 2026-07-02
status: draft
related:
  - .intent/signals/external/SIG-2026-07-02-mobai-team-pilot-convergence.md (action C — the translation layer)
  - .intent/signals/SIG-2026-05-31-exposed-vocabulary-divergence-principle.md (internal↔exposed vocab must be managed)
  - spec/SPEC-INTENT-COHERENCE-GATE-001.md (internal source of truth for "coherence" / "false-green")
  - spec/SPEC-INTENT-FORMATION-FLIGHT-001.md (internal source of truth for "formation flight")
note: >
  This is the EXPOSED, plain-language surface for Intent. The internal source-of-truth vocabulary
  (λ, drift-clean, Stage A/B, etc.) lives in spec/. Keep this page jargon-free by design — it exists
  because direct feedback flagged Intent's materials as too complex and too jargon-loaded.
  Register exemplar: Göthe's "MobAI: From Copilot to Team Pilot" (raw/competitors/2026-06-18-...).
  Drafted with a prose-tuned model, verified against the specs above for faithfulness.
---
# Intent, in plain language

## The building got fast. The thinking didn't.

For most of software history, building was the slow part. You decided what to make, and then you waited weeks for it to exist. Whole management systems — sprints, standups, planning meetings — grew up around managing that wait.

AI just removed the wait. Work that took weeks now takes hours. But that doesn't make the job easy; it moves the hard part. When building is fast and cheap, the scarce skills become: deciding what's worth building, describing it clearly enough that someone — or something — can act on it, and checking that what came back actually adds up. The bottleneck moved upstream, from delivery to judgment.

Intent is a way of running product teams built for that reality. It replaces the ceremony of traditional Agile with one continuous loop: **notice what matters, describe it precisely, build it, watch what happens, repeat.** No sprint boundaries. No meetings held because the calendar says so. The team's energy follows the most important problem, whenever it shows up.

## The quiet failure AI creates

Here's the part most "AI productivity" conversations miss. AI makes each individual faster — and can quietly make the team worse.

Give everyone a copilot and everyone produces more. Everyone feels self-sufficient. The felt need to involve colleagues drops, because why wait for a person when the machine answers now? The organization looks more productive while becoming harder to align and harder to steer. People aren't just moving faster. They're moving faster **apart**.

That's the dangerous trade: AI can make a group faster without making it a team.

The same failure appears when you run many AI agents in parallel. Each one does locally sensible work. But the pieces drift: two agents use different words for the same idea, one quietly contradicts another, a third wanders outside the job it was given. Every piece reports "done and correct." The whole doesn't hold together.

## What Intent protects

Intent exists to protect one thing: that all the parallel work — human or AI — stays true to a single shared purpose (we call this **coherence**). The pieces have to add up.

The core risk, stated plainly: work can look finished and correct piece by piece while the whole is broken. Every light is green and the system is still wrong (in-house, a **"false-green"**).

Intent's answer is a checkpoint that runs whenever parallel work comes back together. It doesn't ask "does each piece look done?" It checks each piece against the brief it was actually given, and it hunts for three quiet failures: different words for the same idea, work that broke a rule it was told to hold, and work that crept outside its declared scope.

## Don't let the builder grade its own homework

A check is only trustworthy if it's independent of the thing it's checking. If the same AI that built the work also grades it, it already knows what "success" was supposed to look like — so its approval means almost nothing. You wouldn't let a student write and mark their own exam. You'd certainly never let them mark it while holding the answer key.

So in the strongest version of Intent, the checker comes from outside the builder: a different AI model entirely writes the tests and runs the checks, blind to how the work was built. Two things that don't share a brain can't collude.

## Why this isn't "just use AI"

The individual-productivity story — everyone gets a copilot — is real, but too small. The next gain doesn't come from better copilots. It comes from better team habits: AI working in the open where everyone can see it, humans keeping judgment in the loop, shared context that gets richer over time, and people learning together instead of faster apart. That's what Intent is for.

---

# Jargon → plain language

| In-house term | What it actually means |
|---|---|
| **Coherence** | All the parallel work — by people or AI — stays true to one shared purpose, so the pieces add up. |
| **False-green** | Every piece reports "done and correct," but the whole is broken. |
| **Drift** | Pieces of work slowly pulling apart: different words for the same idea, quiet contradictions, work wandering off-task. |
| **Coherence gate** | The checkpoint that runs when parallel work comes back together, checking each piece against the brief it was given — not just whether it looks done. |
| **Mission brief** | The written instructions a piece of work was given: the goal, the rules to hold, and the boundaries to stay inside. |
| **Formation flight** | Many people and AI systems working in parallel while staying aligned — moving fast *together*, not fast apart. |
| **Signal** | Something someone noticed that might matter — a problem, an idea, an anomaly — written down so it doesn't get lost. |
| **The loop (notice / spec / execute / observe)** | The working rhythm: notice what matters, describe it precisely, build it, watch what happens, repeat. |
| **Autonomy level** | How much an AI is trusted to do on its own for a given task — from "human decides everything" to "AI runs the whole task and a human watches the results." |
| **"Grading its own homework"** | Letting the same AI that built the work also check it — worthless, because it already knows what "success" was supposed to look like. The checker must be independent. |
</content>
