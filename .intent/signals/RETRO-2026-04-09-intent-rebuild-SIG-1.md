---
signal_id: RETRO-2026-04-09-intent-rebuild-SIG-1
title: Long multi-topic Claude Desktop sessions degrade UI state — need structured handoff earlier in the session
severity: high
detected: 2026-04-09
status: open
source: retroactive-extraction
trust_score: 0.75
autonomy: L3
---
# Long multi-topic Claude Desktop sessions degrade UI state

## Observation

The 2026-04-09 session ran for several hours across ~15 distinct work threads (panel review, signal extraction, safety contract, change mgmt, discovery scaffold, site v2-draft rebuild, banner rollout, hero SVG iterations, logo fix, session handoff). Toward the end, Brien reported seeing:

- Old text staying in the chat thread
- "Initialized your session" events appearing mid-conversation
- Fragmented tool call summaries
- UI chrome suggesting session state corruption or hitting limits

The work itself was safe (all commits pushed to git across 3 repos), but the session UI was degrading and reliable continuation was at risk.

## Context

This happened after the session had:
- Dispatched 8 parallel panels (48 sub-agents total) for the initial review
- Dispatched 5 parallel agents for the framing banner rollout (23 file edits)
- Written 3 new decision records, 14 new signals, 7 new intents, 3 psych safety docs, 6 discovery scaffolding docs, 10 v2-draft HTML pages, 1 operator persona, 1 panel-review skill scaffold, multiple plan files, and an extraction manifest
- Run 3-4 major back-and-forths on the hero SVG iteration
- Fetched/read dozens of existing files for context

The cumulative effect of parallel agent dispatches, long sequential file writes, and extensive reading pushed the session past typical UI reliability.

## Implication

Three things follow:

1. **Write the session-extraction BEFORE the session shows signs of stress**, not after. The handoff file should be a mid-session checkpoint, refreshed at milestones, not a last-minute scramble when UI is already degrading.

2. **Session-extraction skill should be triggered proactively** after each major milestone (panel review complete, architecture P0 complete, etc.), not only at session end. The skill's description should note this.

3. **Brien should have a "panic button" bootstrap prompt** — a single canonical prompt ready to paste into a fresh session that loads exactly the right context. This prompt should be stored persistently (not in any session) and updated after each major session.

Related: this observation is the source of the recursive meta-moment — Intent's work is literally about async handoff primitives, and the session hit its limits right as it was building those primitives.

## Recommended follow-up

- Add "checkpoint session-extraction" as a trigger to the skill's instructions (run at major milestone, not just session end)
- Write the bootstrap prompt (RETRO-2026-04-09-bootstrap-prompt.md or similar) as a standing artifact
- Surface this signal as a pattern in brien-operator's known failure modes: "Long sessions degrade before extraction happens"
- Consider: should panel-review calls emit a session-stress signal if they detect excessive parallel dispatch count?
